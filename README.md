# FINCEPT AI — Authentication + Finance + Insights + AI Assistant + Planner

Desktop implementation of the original Figma Authentication, full Overview, functional Transactions, Wallets, Budgets and Financial Goals screens, with the shared expandable sidebar. React + TypeScript + Vite frontend, shared CSS components, local Manrope fonts and Figma assets, and a working FastAPI + SQLite authentication backend.

**Implemented: Authentication, shared sidebar/topbar, Overview, Transactions, Wallets, Budgets, Financial Goals, Insights, the AI Assistant and Planner.** Successful authentication opens the preserved confirmation route; click **Open Overview** to view your financial snapshot. New accounts have empty live data; explicitly choose **Explore sample data** to inspect the isolated development sample. Transactions supports real creation, editing, confirmation deletion, transfers/fees, categories, filters and CSV. Wallets supports real account creation/editing, active summaries, grid/list search/filter/sort, explicit Add Money accounting, reviewed atomic transfers, details and archive/restore. Budgets supports persistent category plans, shared expense allocation with Overview, period browsing, summaries, risk alerts, search/filters/sorting, real expense history and confirmed deletion that preserves transactions. See `docs/BUDGETS.md` for explicit-period and threshold rules; automatic recurrence is not implemented. Financial Goals adds persistent plans, active-only summaries, search/filter/sort, pause/resume, retained history and reviewed wallet allocations/external deposits. See `docs/GOALS.md` for accounting and legacy-funding limitations. Insights adds real period analytics, category drill-down and safe CSV export. The AI Assistant adds persistent owned conversations, grounded financial context, server-side OpenAI integration, safe retries and honest missing-configuration states; no AI credentials were configured for this delivery. Planner adds real calendar/task CRUD, date-correct navigation, occasion plans and canonical reviewed savings contributions. See `docs/PLANNER.md` for ownership, date/time, summaries, migration v9 and unavailable reminders. Debt & Loans and Financial Hub remain placeholders. This code was created in an isolated development workspace; it has not been installed on your PC or deployed.

## Requirements

- Node.js 22.12+ (Node 24 was used for verification)
- Python 3.11+ (Python 3.13 was used for verification)
- Two terminals, both initially opened in the extracted `fincept-ai` folder

## Run locally

### Terminal 1 — backend

```sh
cd backend
python -m venv .venv
```

Activate the virtual environment:

- Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
- Windows Command Prompt: `.venv\Scripts\activate.bat`
- macOS/Linux: `source .venv/bin/activate`

Then:

```sh
python -m pip install -r requirements-dev.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

A development SQLite database is initialized automatically at `backend/data/fincept.sqlite3`. No pre-created account is shipped. Register your own test account through the app. Use disposable test credentials during development.

### Terminal 2 — frontend

```sh
npm ci
npm run dev
```

Open **http://127.0.0.1:5173/sign-up** or **http://127.0.0.1:5173/sign-in**.

## Run with Docker

Docker Compose builds the frontend and backend, serves the compiled SPA through
Nginx, proxies `/api` to FastAPI, and persists the SQLite database in the
`fincept-data` volume:

```sh
docker compose up --build
```

Open **http://localhost:8080/sign-up** or **http://localhost:8080/sign-in**.
Stop the stack with `docker compose down`; the named database volume is
preserved. To remove the persisted database too, use
`docker compose down -v`.

Compose reads optional deployment values from a root `.env` file. The defaults
are suitable for local Docker use. For an HTTPS production deployment, set
`APP_ENV=production`, `COOKIE_SECURE=true`, and provide exact
`FRONTEND_ORIGINS` and `TRUSTED_HOSTS` values behind a TLS-terminating proxy.
Keep `OPENAI_API_KEY` server-side and never add it to Vite variables.

### Render deployment

When deploying the frontend and backend as separate Render web services, the
Compose hostname `backend` does not exist on Render. Set the frontend service
environment variable below to the backend service's public URL, without a
trailing slash:

```text
BACKEND_URL=https://your-backend-service.onrender.com
```

The frontend image uses this value when Nginx starts, so `/api/*` requests are
proxied to the Render backend without requiring a rebuild. On the backend
service, set:

```text
APP_ENV=production
COOKIE_SECURE=true
FRONTEND_ORIGINS=https://your-frontend-service.onrender.com
TRUSTED_HOSTS=your-backend-service.onrender.com
```

Enable HTTPS on both services and use the backend's `/api/health` endpoint for
the backend health check. If frontend and backend are deployed as one service,
keep the default `BACKEND_URL=http://backend:8000` only when that hostname is
provided by the service network.

The Vite development server proxies `/api` to the backend on port 8000. Environment examples are included; local defaults work without copying them. To customize them, copy root `.env.example` to `.env.local`, and `backend/.env.example` to `backend/.env`. Restart servers after configuration changes.

## Authentication behavior

- Registration requires a full name, valid email, matching passwords, and terms acceptance.
- Password policy: 8+ characters, upper and lowercase letters, a number, and a symbol; maximum 512 characters. The strength meter responds to the real value.
- Passwords are hashed using Argon2id, never persisted in plaintext.
- Sessions use random opaque HttpOnly cookies. Only hashed session identifiers are stored in the database. No tokens or passwords are stored in localStorage or returned in JSON.
- Remember Me creates a 30-day persistent cookie. Otherwise, the cookie is browser-session scoped with an 8-hour server-side expiry. Browser session-restore behavior is browser-dependent.
- Login rotates the current session; logout revokes it. Protected routes verify the session with the backend.
- Field errors, wrong credentials, server/network failures, request loading and repeated-submit prevention are implemented.
- The shared brand panel and financial illustration are implemented once.

## Not configured / not production-ready

- **Google OAuth:** button preserves the design but reports that authentication is not configured. No fake Google success is generated. Activation requires provider credentials, registered redirect URIs, verified server-side callback/state handling, account linking policy, and secret configuration.
- **Forgot password:** the navigation works, but no reset email is sent. A delivery provider and a secure expiring, single-use reset-token flow are still required.
- **Terms and Privacy:** routes are explicitly labeled development placeholders. Supply approved documents and update the recorded terms version before real users accept them.
- Desktop reference is 1440 × 980; smaller windows scroll. No mobile or tablet layouts are included.
- Some original Figma colors do not meet normal-text WCAG AA contrast. They were preserved for design fidelity; obtain approval for a contrast adjustment before claiming AA compliance.
- Production needs HTTPS, `APP_ENV=production`, `COOKIE_SECURE=true`, exact `FRONTEND_ORIGINS`, and `TRUSTED_HOSTS` for the actual API host. Prefer same-origin frontend/API hosting. Arbitrary cross-site cookie hosting is not configured.
- Production serving must proxy `/api` to FastAPI and fall back to `index.html` for frontend routes. The Vite development proxy is not a production server. `npm run preview` is a static preview and does not configure that API proxy.
- Review deployment security, backups, database permissions, session cleanup, rate limiting and operational monitoring before launch. No email verification, MFA, or external identity provider is implemented in this segment.

## Checks

Frontend unit/component tests and production build:

```sh
npm test
npm run build
```

Backend tests (activate its virtual environment first):

```sh
cd backend
python -m pytest -q
```

Browser tests (from the project root, with the backend virtual environment active):

```sh
npx playwright install chromium
npm run test:e2e
```

Browser tests start isolated servers on ports 5180 and 8090 and use a separate database under `test-results/`. These ports must be free. `PYTHON_BIN` can specify the virtual environment's Python executable if it is not on PATH. `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` optionally selects a system Chromium.

Verification: **49 frontend + 31 backend + 46 browser tests passed (126 total); production build passed.** Exact executed commands and boundaries are recorded in `docs/IMPLEMENTATION_STATUS.md`. Backend testing emits one upstream Starlette/httpx deprecation warning. See `docs/IMPLEMENTATION_STATUS.md` for evidence, file inventory, endpoint list, and remaining configuration.


## Vector asset correction

Authentication uses the original SVG logo mark with a live Manrope wordmark and a shared React/CSS/SVG financial illustration. The old brand/illustration PNGs remain only as unused reference assets. Original chart, category icons and password-eye SVGs are local under `public/assets/auth/`. The original Google asset is unchanged. A local, licensed Noto Sans Bengali subset supplies only the taka character missing from Manrope; all Latin typography remains Manrope.

Both authentication pages were tested and visually reviewed at native Chromium browser zoom 100%, 125%, and 150%. At higher zoom the existing desktop-only minimum canvas scrolls rather than switching to a mobile layout. Captures and machine-readable checks are in `docs/asset-correction-zooms/`.

To repeat native zoom verification, start the frontend and backend, then run `node tests/verify-asset-zoom.mjs`. This uses a local test-only Chromium extension and requires a Chromium build supporting unpacked extensions; `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` can select the executable. The extension is not part of the application or its production build.


## Combined project package

This ZIP already contains the vector-corrected Authentication implementation and the sidebar integration. No manual file merging is required. Start with START_HERE.md. The existing backend/frontend commands remain unchanged; no new dependency or provider configuration is required for the sidebar. The full read-side Overview is included, with real authenticated read APIs and explicit, isolated sample data. The Transactions segment shares the same canonical database, privacy state and layout. Other financial segments remain labeled integration placeholders. See docs/OVERVIEW.md and docs/TRANSACTIONS.md for accounting and scope. Back up existing databases before the additive v3 upgrade.

## Calendar/category correction

Transactions now uses the original Figma calendar and centered Create custom category dialog, including persistent icon/color choices. All other feature designs and financial accounting are preserved. See docs/CALENDAR_CATEGORY_CORRECTION.md and docs/CALENDAR_CATEGORY_FILES.md. This complete corrected ZIP replaces the previous project ZIP; no manual merge is needed.

## Wallets package

Open **Wallets** in the shared sidebar. Create a manual BDT account, then use Add Money or Transfer; opening balances are not income. Existing databases receive additive schema v5 at startup. Back up your database and `.env` before upgrading. See `docs/WALLETS.md` for endpoints/accounting/archive rules, `docs/WALLETS_FILES.md` for the exact source inventory, and `docs/IMPLEMENTATION_STATUS.md` for executed checks. This is one complete project ZIP, not a patch to merge with earlier archives.

## Financial Goals package

Open **Financial Goals** in the shared sidebar. Create a plan at zero saved, then Add Savings and review the funding source before recording. Existing wallet allocation does not change total assets or income; an external deposit creates one linked wallet event. Startup applies additive schema **v7**; back up your database first. No new credentials or dependencies. See `docs/GOALS.md`, `docs/GOALS_FILES.md` and the latest `docs/IMPLEMENTATION_STATUS.md` for contracts, exact changes and executed verification. This ZIP is the complete current project, not a patch to merge with earlier archives.


## Financial Insights & Analytics

`/insights` is implemented against the existing authenticated financial records: real period filters, summaries, interactive charts, category drill-down, income categories, current goal progress, selected-range budget performance and privacy-aware CSV downloads. No AI provider is connected; the AI panel states that explicitly. See `docs/INSIGHTS.md`, `docs/INSIGHTS_FILES.md` and the latest `docs/IMPLEMENTATION_STATUS.md` for exact accounting, API, tests and limits. Use `/insights?dataset=demo` only after explicitly creating the development sample workspace through the existing Overview workflow; production rejects it.


## AI Financial Assistant

Open `/ai-assistant` after signing in. Read `docs/ASSISTANT.md` for the inspected Figma component map, provider setup, schema v8, endpoints, persistence, read-only financial grounding, privacy and tested limits; see `docs/ASSISTANT_FILES.md` for the file inventory. The assistant works in the existing shell without rebuilding other pages. Conversation history is in SQLite, not browser-only state.

For actual model-generated replies, set **server-side only** `AI_PROVIDER=openai`, `AI_MODEL` to an enabled compatible Chat Completions model, and `OPENAI_API_KEY` in `backend/.env`, then restart the backend. Never use a `VITE_` credential. No provider/model allowance is assumed. Without configuration, saved history and all other finance pages remain usable; send returns a clear unavailable error rather than a fake reply.

The assistant is informational/read-only, not a financial-action agent. It sends bounded relevant account summaries and limited completed conversation context to the configured provider. The shared privacy toggle conceals structured money and all free-form chat/history text; this is display privacy, not a change to stored data or provider context. Review provider terms/retention and user disclosures before deployment. No streaming, cancellation, bank connection or financial writes are claimed.

Backend tests include one opt-in paid live-provider check, skipped unless `RUN_LIVE_AI_TEST=1` with valid provider configuration. Explicit test-double/HTTP mock transport/browser fixture success is not evidence of a real model call. Final executed counts are in `docs/IMPLEMENTATION_STATUS.md` and `docs/assistant-qa/verification.json`.

### Debt & Loans and Financial Hub
New full-stack routes `/debt-loans` and `/financial-hub` use additive schema v10. See [Debt & Loans](docs/DEBT_LOANS.md) and [Financial Hub](docs/FINANCIAL_HUB.md) for accounting, APIs and provider behavior. Loans/payments and purchases are tracking-only; no funds silently move. Currency conversion uses genuine ExchangeRate-API open-access data (no key; outbound HTTPS required), not Figma sample rates.
