"""FINCEPT API. HttpOnly cookie sessions and shared financial reporting."""
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import logging
import os
from pathlib import Path
import re
import secrets
import sqlite3
import time

from argon2 import PasswordHasher, Type
from argon2.exceptions import VerificationError, InvalidHashError
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, field_validator
from starlette.middleware.trustedhost import TrustedHostMiddleware

load_dotenv()

@dataclass(frozen=True)
class Settings:
    database_path: str = os.getenv('DATABASE_PATH', './data/fincept.sqlite3')
    frontend_origins: tuple[str, ...] = tuple(x.strip() for x in os.getenv('FRONTEND_ORIGINS', 'http://127.0.0.1:5173,http://localhost:5173').split(',') if x.strip())
    cookie_secure: bool = os.getenv('COOKIE_SECURE', 'false').lower() == 'true'
    environment: str = os.getenv('APP_ENV', 'development')
    session_hours: int = int(os.getenv('SESSION_HOURS', '8'))
    remember_days: int = int(os.getenv('REMEMBER_DAYS', '30'))

class Login(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=512)
    remember: bool = False

    @field_validator('email', mode='before')
    @classmethod
    def normalize_email(cls, value):
        return value.strip().lower() if isinstance(value, str) else value

class Registration(Login):
    full_name: str = Field(min_length=2, max_length=100)
    confirm_password: str = Field(max_length=512)
    accepted_terms: bool

    @field_validator('full_name', mode='before')
    @classmethod
    def normalize_name(cls, value):
        return ' '.join(value.split()) if isinstance(value, str) else value

class PublicUser(BaseModel):
    id: str
    full_name: str
    email: str

class UserResult(BaseModel):
    user: PublicUser

def password_valid(value: str) -> bool:
    return (8 <= len(value) <= 512 and bool(re.search('[a-z]', value))
            and bool(re.search('[A-Z]', value)) and bool(re.search('[0-9]', value))
            and bool(re.search(r'[^\w\s]', value, re.ASCII)))

def create_app(settings: Settings | None = None, *, assistant_provider=None):
    config = settings or Settings()
    if config.environment == 'production' and not config.cookie_secure:
        raise RuntimeError('Production requires COOKIE_SECURE=true and HTTPS.')
    if not config.frontend_origins or '*' in config.frontend_origins:
        raise RuntimeError('Configure explicit FRONTEND_ORIGINS; wildcard credential origins are not permitted.')
    if config.session_hours < 1 or config.remember_days < 1:
        raise RuntimeError('Session durations must be positive.')
    hasher = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2, type=Type.ID)
    dummy_hash = hasher.hash(secrets.token_urlsafe(32))
    cookie_name = '__Host-fincept_session' if config.cookie_secure else 'fincept_session'

    @contextmanager
    def db():
        Path(config.database_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(config.database_path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys=ON')
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @asynccontextmanager
    async def lifespan(app):
        with db() as conn:
            conn.executescript('''
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                accepted_terms_at TEXT NOT NULL,
                terms_version TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                expires_at INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_sessions_expiry ON sessions(expires_at);
            CREATE TABLE IF NOT EXISTS rate_limits (
                bucket TEXT PRIMARY KEY, hits INTEGER NOT NULL, reset_at INTEGER NOT NULL
            );

            ''')
            from .finance.schema import initialize
            initialize(conn)
            from .assistant.schema import initialize as initialize_assistant
            initialize_assistant(conn)
            from .planner.schema import initialize as initialize_planner
            initialize_planner(conn)
            from .debt.schema import initialize as initialize_debt_hub
            initialize_debt_hub(conn)
        yield

    api = FastAPI(title='FINCEPT AI', version='0.1.0', lifespan=lifespan)
    api.add_middleware(CORSMiddleware, allow_origins=list(config.frontend_origins),
                       allow_credentials=True, allow_methods=['GET','POST','PATCH','DELETE'],
                       allow_headers=['Content-Type','X-Fincept-Request'])
    # Set TRUSTED_HOSTS at deployment to the actual API host(s).
    trusted_hosts = [
        host.strip()
        for host in os.getenv(
            'TRUSTED_HOSTS',
            'localhost,127.0.0.1,testserver'
        ).split(',')
        if host.strip()
    ]
    api.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts)

    @api.middleware('http')
    async def security_headers(request, call_next):
        if request.method in ('POST','PATCH','DELETE'):
            origin = request.headers.get('origin')
            if request.headers.get('x-fincept-request') != '1' or (origin and origin not in config.frontend_origins):
                return JSONResponse({'message':'Request could not be verified. Refresh and try again.'}, status_code=403)
            try:
                if int(request.headers.get('content-length', '0')) > 16384:
                    return JSONResponse({'message':'Request is too large.'}, status_code=413)
            except ValueError:
                return JSONResponse({'message':'Invalid request.'}, status_code=400)
        response = await call_next(request)
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    @api.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        fields = {}
        for error in exc.errors():
            key = str(error['loc'][-1])
            fields[key] = 'Enter a valid email address.' if key == 'email' else 'Check this field and try again.'
        # Deliberately omit Pydantic's input values: they may contain passwords.
        return JSONResponse({'message':'Please check the highlighted fields.', 'field_errors':fields}, status_code=422)

    @api.exception_handler(HTTPException)
    async def http_error(request, exc):
        data = exc.detail if isinstance(exc.detail, dict) else {'message':exc.detail}
        return JSONResponse(data, status_code=exc.status_code, headers=exc.headers)

    @api.exception_handler(Exception)
    async def unexpected_error(request, exc):
        logging.getLogger('fincept.auth').error('Authentication service failure (%s)', type(exc).__name__)
        return JSONResponse({'message':'The authentication service is temporarily unavailable. Please try again.'}, status_code=500)

    def rate_limit(request: Request, kind: str, email: str = ''):
        now = int(time.time())
        # No trust in forwarded IP headers; configure a trusted reverse proxy explicitly in production.
        ip = request.client.host if request.client else 'unknown'
        keys = [(f'{kind}:ip:{ip}', 30)]
        if email:
            keys.append((f'{kind}:account:{hashlib.sha256(email.encode()).hexdigest()}', 10))
        blocked = False
        with db() as conn:
            conn.execute('BEGIN IMMEDIATE')
            conn.execute('DELETE FROM rate_limits WHERE reset_at <= ?', (now,))
            for key, limit in keys:
                conn.execute('INSERT INTO rate_limits VALUES (?,1,?) ON CONFLICT(bucket) DO UPDATE SET hits=hits+1', (key, now+900))
                hits = conn.execute('SELECT hits FROM rate_limits WHERE bucket=?', (key,)).fetchone()['hits']
                blocked = blocked or hits > limit
        if blocked:
            raise HTTPException(429, 'Too many attempts. Please try again in 15 minutes.', headers={'Retry-After':'900'})

    def public_user(row):
        return {'id':row['id'], 'full_name':row['full_name'], 'email':row['email']}

    def token_hash(token):
        return hashlib.sha256(token.encode()).hexdigest()

    def set_session(conn, request, response, user_id, remember):
        old = request.cookies.get(cookie_name)
        if old:
            conn.execute('DELETE FROM sessions WHERE token_hash=?', (token_hash(old),))
        token = secrets.token_urlsafe(48)
        ttl = config.remember_days*86400 if remember else config.session_hours*3600
        conn.execute('DELETE FROM sessions WHERE expires_at <= ?', (int(time.time()),))
        conn.execute('INSERT INTO sessions VALUES (?,?,?)', (token_hash(token), user_id, int(time.time())+ttl))
        response.set_cookie(cookie_name, token, max_age=ttl if remember else None,
                            secure=config.cookie_secure, httponly=True, samesite='lax', path='/')

    def current_user(request: Request):
        token = request.cookies.get(cookie_name)
        if not token or len(token) > 256:
            raise HTTPException(401, 'Please sign in to continue.')
        with db() as conn:
            row = conn.execute('SELECT u.id,u.full_name,u.email FROM users u JOIN sessions s ON u.id=s.user_id WHERE s.token_hash=? AND s.expires_at>?', (token_hash(token), int(time.time()))).fetchone()
        if row is None:
            raise HTTPException(401, 'Your session has expired. Please sign in again.')
        return public_user(row)

    @api.get('/api/health')
    def health():
        return {'status':'ok'}

    @api.get('/api/auth/config')
    def auth_config():
        return {'google_enabled':False, 'password_reset_enabled':False}

    @api.post('/api/auth/register', response_model=UserResult, status_code=201)
    def register(data: Registration, request: Request, response: Response):
        email = str(data.email).lower()
        rate_limit(request, 'register', email)
        errors = {}
        if not password_valid(data.password):
            errors['password'] = 'Use 8+ characters, upper & lowercase letters, a number and a symbol.'
        if data.password != data.confirm_password:
            errors['confirm_password'] = 'Passwords do not match.'
        if not data.accepted_terms:
            errors['accepted_terms'] = 'Accept the Terms of Service and Privacy Policy to continue.'
        if errors:
            raise HTTPException(422, {'message':'Please check the highlighted fields.', 'field_errors':errors})
        now = datetime.now(timezone.utc).isoformat()
        user = {'id':secrets.token_hex(16), 'full_name':data.full_name, 'email':email}
        hashed = hasher.hash(data.password)
        with db() as conn:
            try:
                conn.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?)', (user['id'], data.full_name, email, hashed, now, 'development-draft-v1', now))
            except sqlite3.IntegrityError:
                raise HTTPException(409, {'message':'Unable to create an account with this email. Try signing in.', 'field_errors':{'email':'This email may already be registered.'}})
            set_session(conn, request, response, user['id'], False)
        return {'user':user}

    @api.post('/api/auth/login', response_model=UserResult)
    def login(data: Login, request: Request, response: Response):
        email = str(data.email).lower()
        rate_limit(request, 'login', email)
        with db() as conn:
            row = conn.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
            try:
                valid = hasher.verify(row['password_hash'] if row else dummy_hash, data.password)
            except (VerificationError, InvalidHashError):
                valid = False
            if not row or not valid:
                raise HTTPException(401, 'Email or password is incorrect.')
            if hasher.check_needs_rehash(row['password_hash']):
                conn.execute('UPDATE users SET password_hash=? WHERE id=?', (hasher.hash(data.password), row['id']))
            set_session(conn, request, response, row['id'], data.remember)
            user = public_user(row)
        return {'user':user}

    @api.get('/api/auth/me', response_model=UserResult)
    def me(user=Depends(current_user)):
        return {'user':user}

    @api.post('/api/auth/logout', status_code=204)
    def logout(request: Request, response: Response):
        token = request.cookies.get(cookie_name)
        if token:
            with db() as conn:
                conn.execute('DELETE FROM sessions WHERE token_hash=?', (token_hash(token),))
        response.delete_cookie(cookie_name, path='/', secure=config.cookie_secure, httponly=True, samesite='lax')
        response.status_code = 204
        return response

    from .finance.routes import overview_router
    api.include_router(overview_router(db, current_user, config.environment))
    from .finance.transactions import transaction_router
    api.include_router(transaction_router(db, current_user, config.environment))
    from .finance.wallets import wallet_router
    api.include_router(wallet_router(db, current_user, config.environment))
    from .finance.budgets import budget_router
    api.include_router(budget_router(db, current_user, config.environment))
    from .finance.goals import goal_router
    api.include_router(goal_router(db, current_user, config.environment))
    from .finance.insights import insights_router
    api.include_router(insights_router(db, current_user, config.environment))
    from .assistant.provider import OpenAIProvider, ProviderConfig
    from .assistant.routes import assistant_router
    api.include_router(assistant_router(db, current_user, config.environment, assistant_provider or OpenAIProvider(ProviderConfig())))
    from .planner.routes import planner_router
    api.include_router(planner_router(db, current_user, config.environment))
    from .debt.routes import debt_router
    api.include_router(debt_router(db, current_user, config.environment))
    from .hub.routes import hub_router
    api.include_router(hub_router(db, current_user, config.environment))
    return api

app = create_app()
