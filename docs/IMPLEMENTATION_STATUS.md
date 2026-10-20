# Current implementation — AI Financial Assistant

**AI Assistant is implemented full-stack in the existing FINCEPT AI application.** `/ai-assistant/*` now uses the shared authenticated shell, original Figma-inspired components/assets, a real server-side provider boundary, SQLite conversation persistence and read-only owner-scoped financial context. No separate app, fake production reply or model-driven financial write was introduced. See `ASSISTANT.md` for API/design/security/configuration contracts and `ASSISTANT_FILES.md` for the archive-checked source inventory.

**Live AI replies still require private server-side configuration.** No AI credentials were configured here. The actual missing-provider workflow is verified; production has an OpenAI adapter, while successful response contract/UI tests use explicitly isolated test doubles. The paid real-provider integration test was skipped, not reported as passing.

## Final executed checks

| Command | Result |
|---|---|
| `npm run build` | **PASS** — TypeScript + Vite production build |
| `npm test` | **80 passed**, 13 test files |
| `cd backend && .venv/bin/python -m pytest -q` | **105 passed, 1 skipped**, 2 upstream warnings; 63.30 seconds |
| Full `npm run test:e2e` with backend venv and system Chromium | **90 passed**, complete browser regression; 4.2m |
| `npm audit --omit=dev --json` | **0 runtime dependency vulnerabilities** |
| Original assistant SVG validation | **2 passed** — original viewBoxes/geometry, no raster/script/event/external dependency |

**275 distinct tests passed**, plus one skipped credential-dependent test. No repeated targeted runs are added to the total. Final command logs, original/implemented screenshots and machine-readable results are under `assistant-qa/`.

Backend coverage includes authentication/CSRF, owner/dataset isolation, additive migration, real financial summaries, exact decimal context minimization, persistence across restart, pagination, sanitized provider errors/timeouts, durable failure/retry, idempotent replay/concurrency/stale-lease fencing, persisted rate limits and production demo rejection. Unit tests cover original suggestions, escaped HTML-like output, deterministic summary cards, full free-form monetary privacy and receipt merging. Browser tests cover real unavailable-provider persistence/history/refresh/retry, whitespace/Enter/Shift+Enter, pending states, failure preservation, literal search, navigation, safe output, summary privacy and reduced motion. Successful rendering uses one explicitly labeled UI-only model fixture with actual backend demo calculations; it does not prove a live model call.

The full browser suite includes existing authentication, Overview, Transactions, Wallets, Budgets, Financial Goals, Insights and shared-shell regressions. Four desktop sizes (1440×900, 1366×768, 1280×800 and 1024×768), expanded/minimized sidebar and opened history were checked for overflow/usable controls. The actual 1440×1080 welcome and conversation rendering were visually compared with Figma; original geometry/colors/Manrope/layout were retained. Genuine status text, actual account data, conservative privacy, date/source captions and narrow-desktop history stacking intentionally replace illustrative Figma states. Browser rasterization/native textarea behavior and exact pixel identity are not claimed.

## Resolved checks and remaining boundaries

Initial integration checks corrected the existing four-value `period_range` contract, distinguished the v7 direct finance initializer from v8 full application startup, and used before/after canonical record counts rather than fabricated demo expectations. A production test needed the existing trusted-host setting. Browser fixture assertions now await asynchronous request arrival; the existing calendar keyboard test waits for requestAnimationFrame focus before the next key. A subsequent complete browser run exposed an intermittent first-send route/ref ordering issue on immediate failures; the active conversation is now recorded before URL navigation. The affected privacy/retry workflows passed 16 repeated checks, and every assistant browser case now asserts no unhandled page errors. No authentication, finance accounting, production calendar behavior or security rule was weakened. Earlier failing runs are not claimed as passing; final complete runs are the results above.

The backend's two warnings concern upstream Starlette/httpx TestClient deprecation and Pydantic field-alias handling in concurrency coverage. Existing development-only test tooling has 3 audit advisories (2 critical, 1 moderate); resolving them requires a separately reviewed major Vitest upgrade. Production dependency audit is clean; deployment readiness is not certified.

- Configure `AI_PROVIDER=openai`, an explicit compatible `AI_MODEL`, and private `OPENAI_API_KEY` in backend environment only. No `VITE_` AI secret, client provider SDK, automatic fallback or real-key placeholder is shipped.
- Additive v8 tables store owned conversations, requests/attempts and ordered role messages with optional deterministic summary snapshots. No DB lock is held across provider I/O. Failed/retried questions retain their request ID; completed receipts replay without another model call. External billing exactly-once after server crash is not guaranteed.
- Exact finances reuse existing canonical services. Context is bounded by intent and explicit period; no free-form transaction notes or user identifiers are shared. The model has no DB tools or financial writes. Limited English periods and default-month follow-ups are documented; arbitrary date parsing is not claimed.
- Global privacy conceals entire free-form message bodies/history labels and structured money/percentages, rather than relying on a model or currency regex. Presentation privacy does not alter stored data, API access or provider context; composer content remains an editable form value.
- No streaming/cancel, bank sync, model-driven financial changes, history rename/delete/archival, database-at-rest encryption or production deployment. Other finance pages remain usable when the provider is unavailable. Provider terms/disclosure and live response quality still require deployment review.
- The source package excludes private env values, databases, installed dependencies, caches, build output and runtime test state. Historical status sections below retain their original test counts and limitations, not the current delivery totals.

---

# Current implementation — Financial Insights & Analytics

**Insights is implemented end-to-end inside the existing FINCEPT AI project.** `/insights/*` now uses the real authenticated shell and financial records rather than a placeholder. The Figma Insights page/state references and original vectors informed the UI; independent illustrative Figma numbers are not substituted for canonical data. See `INSIGHTS.md` for design mapping, API/date/accounting contracts and limitations; `INSIGHTS_FILES.md` for the touched-file inventory.

## Latest executed checks

| Command | Result |
|---|---|
| `npm run build` | **PASS** — final TypeScript + Vite production build |
| `npm test` | **73 passed**, 12 files; final run after UI refinements |
| `cd backend && .venv/bin/python -m pytest -q` | **88 passed**, 2 upstream dependency warnings, 65.80 seconds; includes 13 Insights cases |
| Full `npm run test:e2e` with the backend venv and system Chromium | **79 passed**, 5.4 minutes; complete browser regression |
| Same browser command with `-- tests/insights.spec.ts tests/sidebar.spec.ts` | **17 passed**, 1.0 minute; final rerun after negative-cash-flow styling, menu focus-dismissal and CSV scope/import hardening |
| `npm audit --omit=dev` | **0 runtime dependency vulnerabilities** |
| Original Insights SVG validation | **6 passed**, original geometry/viewBoxes retained |

**240 distinct tests passed** (73 unit + 88 backend + 79 browser). The final 17 repeat 9 Insights and 8 sidebar cases; they are not added to the distinct count. The full browser run passed after main integration/visual corrections; the final targeted run verifies the last small UI and backend export/import refinements. The latest complete backend/unit suites and production build passed on those final sources. Actual command logs, image inventory and results are retained in `insights-qa/logs/` and `insights-qa/verification.json`.

Coverage includes real live/demo dataset separation, authentication/ownership, totals reconciling with Overview/Budgets/Goals, transfer-principal exclusion and single fees, positive/negative/no-income cash flow, valid comparisons or honest unavailability, preset/custom inclusive dates, impossible/reversed/overlong ranges, URL refresh, hover/focus/keyboard chart tooltips, privacy across monetary DOM/aria/dialog/export preview, exact category drill-down including blank/null imported Other, real downloaded CSV with quoting/formula neutralization/masking/context markers, unavailable AI, genuine empty/loading/failure/retry and no-success-on-failed-export states. Financial success responses in the Insights browser suite reach FastAPI/SQLite, not mocked data. Only deliberate error/loading cases intercept its requests. Existing UI-only sidebar geometry tests retain their explicit fake-session fixture and return unavailable analytics rather than call a real endpoint without a cookie.

Four desktop sizes — 1440×900, 1366×768, 1280×800 and 1024×768 — were checked with both sidebar states, no horizontal page/section overflow, contained dialogs, keyboard navigation/focus/Escape, menu Tab dismissal and reduced motion. Original/implemented wide and narrow layouts were visually reviewed. Category button fills, original peach trend-icon treatment, largest-category amount hierarchy, source total scope, savings target alignment and the shared chevron were corrected. Screenshots under `insights-qa/` are evidence only, never runtime UI. Browser font rasterization/native date inputs may differ; pixel identity and new mobile layouts are not claimed.

## Resolved validation issues and remaining warnings

The restored workspace had no installed frontend dependencies or Git baseline; `npm ci` restored the pinned dependencies, and the inventory does not claim an unavailable archive diff. Early backend regressions used current-day noon records before noon, so the real as-of-now ledger correctly excluded them. Only the shared test helper's default timestamp was changed to midnight; production ledger/auth behavior was not weakened. A sidebar fake-session fixture initially hit the new real Insights endpoint without a cookie and remounted on 401 refresh; its UI-only unavailable response now preserves that fixture's intended scope. Initial tests assuming the illustrative Salary label or an uncolored category callback object were corrected to the actual category/structural contract. Subsequent complete/final runs passed.

The two final backend warnings are upstream Starlette/httpx TestClient deprecation and a Pydantic field-alias warning in concurrency coverage. Existing development-only Vitest tooling has 3 audit advisories (2 critical, 1 moderate); the audit recommends a major Vitest upgrade. This implementation does not silently change the test framework. Runtime dependency audit is clean; production readiness is not claimed.

## Delivery and accounting boundaries

- No new schema migration, service credentials or runtime dependency. Read the existing canonical owner/dataset-scoped transactions, shared period helper, `budget_service.evaluate` and active `goal_service` summaries. Integer minor units remain authoritative; CSV uses exact two-decimal amounts.
- Budgets compare report-range spending within each plan's dates to the full, unprorated saved limit. Ambiguous overlapping legacy matches are excluded/flagged; first three plans have a view-all count/link. Goals are explicitly dated current allocation snapshots, not selected-period savings or new assets.
- Presets resolve from the server's local date; Last 3 Months includes the current month. Custom ranges are inclusive, valid, 1901–2100 and at most 732 days. Full-month charts show context with the selected month highlighted; CSV labels context-only rows explicitly.
- Shared Money masks use `••••`, preserving the existing application convention rather than Figma's `৳ ****`. Insights hides percentage text in its UI too. Masked CSV promises monetary-column masking; percentages/counts/dates remain available. Presentation privacy is not API permission filtering.
- No AI provider is configured; AI-unavailable is honest. No bank sync, scheduled analysis, PDF export, production deployment, mobile redesign or completion of unrelated placeholder pages. Existing OAuth/reset/notification/legal/deployment limitations remain unchanged.
- Source delivery excludes private `.env` files, databases, installed dependencies, caches, test-runtime state and build output. Historical deliveries below are retained for context, not current test totals.

---

# Current implementation — Financial Goals

**Financial Goals is implemented end-to-end in the existing FINCEPT AI project.** The actual read-only Figma page, desktop, creation/detail/contribution/review/filter/action frames and accounting handoff were inspected first. The existing application shell, design tokens, original vector assets, authentication and previous pages were reused, not rebuilt. See GOALS.md for exact model/API/accounting rules and GOALS_FILES.md for the source inventory against FINCEPT-AI-With-Budgets.zip.

## Latest executed checks

| Command | Result |
|---|---|
| `npm run build` | PASS — TypeScript + Vite production build; final repeat after scoped calendar styling |
| `npm test` | **59 passed**, 10 files; final repeat |
| `cd backend && .venv/bin/python -m pytest -q` | **75 passed**, 2 upstream dependency warnings, 53.69 seconds |
| `PYTHON_BIN=…/backend/.venv/bin/python PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=$(which chromium) npm run test:e2e` | **70 passed**, full browser regression, 5.0 minutes |
| Same browser command with `-- tests/goals.spec.ts` | **8 passed**, final repeat with live loading assertion and reviewed-contribution geometry checks, 57.9 seconds |

**204 distinct tests passed** (59 unit + 75 backend + 70 browser). The final targeted eight repeat existing cases and are not added to the distinct count. The full run passed before the final Goals-only calendar style adjustment; the final production build/unit suite and eight Goals browser cases passed after it. Authentication, Overview, Transactions, Wallets, Budgets and shared sidebar regression cases are included in the full run. No successful financial API response was mocked.

Goals verification includes real database creation/edit/refresh, actual allocation and external deposit, idempotency/repeated click, optimistic versions, active summary/Overview consistency, pause/resume/completion/overfunding, soft-delete history and allocation release, search/category/status/sort/scope, meaningful review without early writes, income exclusion, CSRF/ownership, genuine additive v6-to-v7 migration, legacy provenance, competing allocation concurrency, forced late database failure rollback, inactive wallets and post-spending coverage shortfalls. Intentional UI failure tests intercept 503 responses; the slow list gate asserts the real loading state before failing/retrying. Production rejects demo workspaces.

Four desktop sizes (1440×900, 1366×768, 1280×800, 1024×768), expanded/minimized sidebar, page overflow, contained create/details/savings/review dialogs, focus/Escape, original SVG assets and reduced motion were checked. Original Figma desktop/create/add references and implementation screenshots were compared; final card backgrounds, original kebab icon, button typography/color, form/date treatment and narrower desktop layout were corrected/reviewed. Evidence is in goals-qa. Pixel-perfect browser/Figma font rasterization is not claimed.

Earlier attempts were resolved: the first backend command ran from an incorrect path and did not write the test file; it was corrected before counting Goals coverage. Two initial tests used `/api/overview` instead of the real `/api/overview/summary`; the tests were corrected and the complete suite passed. A later boundary-test edit also used a wrong relative path; the edit was then applied via the exact repository path and all 75 backend cases passed, including the genuine migration. Two overlarge read-only Figma queries hit the result-size bound; bounded queries succeeded. The final backend warnings are Starlette/httpx TestClient deprecation and an upstream Pydantic Field-alias warning; neither is a test failure. Production authentication/rate limiting is unchanged; test-only throttle resets remain isolated to the test database.

## Accounting and delivery boundaries

- Additive schema **v7** extends existing financial_goals with metadata and immutable contributions; no wallet/transaction replacement. Startup migrates automatically; back up the existing DB first. No new service credentials or dependencies.
- Allocating wallet funds changes saved allocations, **not wallet balances, assets, income or expenses**. New external deposits create exactly one wallet event plus one allocation atomically, not income. Wallet and goal summaries retain separate financial meanings and do not double-count assets.
- Active totals exclude paused/completed/deleted goals. Paused/completed allocations remain reserved. Delete releases earmarks, preserves balances, deposit events and read-only history. Completion is derived from reaching the target, reversible by raising the target; no money is created by status changes.
- Legacy savings without funding provenance remain explicitly unlinked. Earmarks are not hard locks on later spending; underfunding is shown honestly and new internal allocations are blocked. See GOALS.md for details.
- BDT/manual plans only; no bank synchronization, scheduled transfers, contribution reversals, manual completion/cancellation or production deployment. Deleted-goal history is readable; no restore command is advertised.
- Complete source ZIP excludes secrets/private DBs, installed dependencies, caches and build output. All baseline files are retained; unrelated prior QA PNGs are restored byte-for-byte. The sections below are retained historical deliveries, not current test counts.

---

# Current implementation — Budgets management

**Budgets is implemented inside the existing FINCEPT AI full-stack project.** Read-only inspection of the actual Figma Budgets page, desktop, creation/detail/filter/action frames and handoff informed the implementation. No Figma design or previous page layout was rebuilt. See BUDGETS.md for the model, API, accounting and explicit limits; BUDGETS_FILES.md records the exact source inventory against FINCEPT-AI-With-Wallets.zip.

## Latest executed checks

| Command | Result |
| --- | --- |
| `npm run build` | PASS — TypeScript and Vite production build |
| `npm test` | **56 passed**, 9 files |
| `cd backend && .venv/bin/python -m pytest -q` | **58 passed**, 2 dependency warnings |
| `PYTHON_BIN=…/backend/.venv/bin/python PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=$(which chromium) npm run test:e2e` | **62 passed**, full browser regression, 3.3 minutes |
| Same browser command with `-- tests/budgets.spec.ts` | **8 passed**, final repeat after details typography correction, 44.1 seconds |

**176 distinct tests passed** (56 unit + 58 backend + 62 browser). The targeted eight repeat existing cases and are not added to that total. The full browser run includes authentication, Overview, Transactions, calendar/category workflows, sidebar and Wallets regressions. The final targeted run refreshes budget screenshots after scoped CSS fixes; the production build and unit suite were also rerun after those fixes.

Browser checks cover actual saved creation/edit/refresh/deletion, transaction preservation, summaries/status/thresholds, period switching, category/search/sort, details history, global privacy, failures/retry/duplicate guards, shared calendar and keyboard behavior. Successful writes reach FastAPI and SQLite, not mocked success responses. Failure tests deliberately intercept failed/slow requests. Four requested desktop sizes (1440×900, 1366×768, 1280×800, 1024×768) were checked with minimized and expanded sidebars, page overflow assertions and contained dialogs. Original/implemented desktop, create and detail frames were visually compared; narrow expanded layout and final details typography were reviewed. Evidence is in budgets-qa. Browser-native rendering and font antialiasing can differ; pixel identity is not claimed.

Early attempts and resolutions: running pytest from the repository root lacked the backend module path; running from backend resolved it. Production-safety tests were corrected to use actual Settings/HTTPS conventions. An overbroad migration expectation edit was restored and limited to schema-version assertions. The first full browser run reached the existing registration throttle after additional test accounts; the final UI-only test fixture now clears throttling counters only in the isolated test database, matching the existing wallet fixture. Production authentication/rate limits are untouched. An attempted `npm run test:unit` script does not exist; the actual project command `npm test` was executed successfully. Final backend warnings are the existing Starlette/httpx TestClient deprecation and a Pydantic Field alias warning; neither failed tests.

## Accounting and delivery boundaries

- Existing canonical budgets and expense transactions are reused; additive schema **v6** stores metadata only. Startup applies the migration; back up the existing SQLite database before upgrading. No new credentials/services are required.
- Shared backend allocation powers both Overview and Budgets: exact category, inclusive intersected dates, integer minor units, unique assignment; income/transfers/adjustments excluded. Remaining can be negative; visual meters clamp only presentation. New overlapping category periods are rejected; ambiguous legacy spending is flagged/excluded rather than guessed.
- Risk follows the configured threshold (default 75%) or exceeded status; Near Limit begins at 85%, Exceeded strictly above 100%. Off disables threshold alerts, not over-budget status.
- Monthly/weekly/custom are explicit saved date windows, **not automatic recurring budgets**. No rollover, frozen historical snapshots, refund/reversal model or push/email alert service is claimed. Live on-page Budget Alerts work. See BUDGETS.md for full semantics.
- Full project ZIP excludes private environments, databases, installed dependencies, caches and build output. It is source delivery, not production deployment. Earlier sections below are retained historical verification of previous features, not current test totals.

---

# Current implementation — Wallets management

**Wallets is now implemented in the existing full-stack application.** Figma was inspected read-only (page 2001:7025, desktop 2001:58232 plus forms/actions/handoff), not edited. See WALLETS.md for component mapping, endpoint contracts, financial rules and explicit boundaries; WALLETS_FILES.md lists exact changes against the calendar/category-corrected ZIP.

Implemented real active summaries, grid/list, persistent view preference, search/category/sorts, original wallet vectors, create/edit/details, explicit Add Money classifications, reviewed internal transfers, adjustments, archive/restore and safe unused deletion. Existing shared shell/privacy/calendar/dialogs are reused. Original Authentication and Overview frontend source/assets, shared Sidebar/Preferences/Dialog and dependency manifests remain byte-identical to the previous ZIP. Header changes only the Wallets subtitle; Transactions integration excludes inactive wallets and supports complete wallet-scoped history. Overview backend balance reads now share the ledger with Wallets and financial guards.

## Actually executed verification

| Command | Result |
| --- | --- |
| `npm run build` | PASS — TypeScript + Vite production build |
| `npm test` | **53 passed**, 8 files |
| `cd backend && .venv/bin/python -m pytest -q` | **41 passed** |
| `PYTHON_BIN=…/backend/.venv/bin/python PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=$(which chromium) npm run test:e2e` | **54 passed**, complete browser regression (3.8m) |
| Same browser command with `-- tests/wallets.spec.ts` | **8 passed** — final rerun after select sizing and expanded geometry assertions |

**148 distinct automated tests passed** in the successful regression runs (53 unit + 41 backend + 54 browser). The wallet-only rerun repeats 8 of those tests; it is not counted as 8 additional distinct tests. All 46 prior browser tests pass, including real auth, Overview, Transactions, sidebar, calendar and custom-category behavior. New backend tests cover persisted metadata/events, application restart, integer reconciliation, classifications, optimistic/idempotent retries, owner/dataset isolation, inactive/archive/delete rules, future-entry rollback, concurrent transfers and long wallet-scoped history. Browser financial writes reach the actual FastAPI/SQLite backend and are verified after refresh; only intentional loading/failure scenarios use failed-response interception.

Wallet grid, list and Add Wallet/Add Money/Transfer dialogs are checked at 1440×900, 1366×768, 1280×800 and 1024×768 with both sidebar states, no horizontal page overflow and dialogs within the viewport. Focus trapping, keyboard open/Escape and reduced motion are checked. Original/implemented wide grid, list, create form and narrow expanded-sidebar captures were visually reviewed; measurements, source icons, card spacing and narrow card header alignment were corrected. Evidence is under wallets-qa, not runtime UI. Native select rendering/font antialiasing may differ slightly; pixel identity is not claimed.

Two non-blocking dependency warnings were observed in the final backend run: Starlette/httpx TestClient deprecation and a Pydantic Field alias warning during the concurrent TestClient test. No test failures are hidden. Early browser failures exposed inaccessible compound form labels (fixed with explicit label/control IDs). A combined rerun later reached the existing 30-per-IP registration threshold; isolated browser fixtures now clear only test-DB throttling counters before the Wallets spec. Production rate limiting/authentication code is unchanged. The full run was then executed successfully against a fresh isolated database.

## Financial and deployment boundaries

- Manual **BDT** tracking, not bank synchronization. Opening balances, external owned-fund deposits and adjustments are not income. Internal principal is a single atomic transfer, not new income/expense; Savings is included once in active Total Funds.
- External/adjustment audit events are persisted separately and visible in Wallet Details (latest 50); the existing Transactions CRUD page retains income/expense/transfer records. No complete paginated adjustment-audit interface is claimed.
- Additive schema **v5** applies on backend startup; back up an existing database/private `.env` before upgrading. No new service credentials are required.
- Existing OAuth, password-reset email, final legal content, real AI/notification integration and production deployment configuration remain as previously documented. No unfinished financial sections were implemented.
- Full source ZIP excludes databases, private environments, installed dependencies, caches and build output. This is not an installation on the user's machine or a production deployment.

---

# Prior follow-up — calendar and Create custom category correction

Only the requested Transactions calendar/date-time controls and category-creation UI were corrected from the existing Figma. The rest of Authentication, Overview, shared shell and financial accounting remain unchanged. Read CALENDAR_CATEGORY_CORRECTION.md for the original frame/component mapping and exact behavior; CALENDAR_CATEGORY_FILES.md lists the changes against the previous whole-project ZIP.

- Original Figma calendar grid, selected-day state, Today/Yesterday, 24-hour input and Apply; functional month navigation and keyboard date selection.
- Original centered Create custom category dialog, Income/Expense toggle, six original-vector icon choices, six color choices and footer. Icon/color appearance persists via small additive schema-v4 metadata; original category/ledger columns and ownership rules are preserved.
- Feature-scoped CSS. No global token, authentication, Overview, sidebar or header redesign. No Figma modifications, new dependencies or external service configuration.

## Actual final verification

**126 automated tests passed**, plus the production build:

- `npm run build`: PASS (TypeScript + Vite).
- `npm test`: **49 passed**, 7 files (including 5 calendar unit tests).
- Backend `.venv/bin/python -m pytest -q`: **31 passed**; 1 existing upstream Starlette/httpx deprecation warning.
- `PYTHON_BIN=/data/fincept-ai/backend/.venv/bin/python PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=$(which chromium) npm run test:e2e`: **46 passed** (1.7m), including all previous auth/Overview/sidebar/Transactions regressions and 6 new calendar/category browser checks.
- Calendar and category dialogs checked at 1440×900, 1366×768, 1280×800 and 1024×768. Date/time is saved through the actual backend and verified after refresh. Category icon/color/type persistence, duplicate errors and canceled drafts are tested.
- All six original category SVGs XML-validated. Actual 1440 calendar/category and 1024 calendar-context captures visually compared with original Figma references. Screenshot evidence is under ui-correction-qa/. Unrelated historical auth/Overview/sidebar screenshot files are preserved byte-for-byte from the previous ZIP.

During verification, a category SQL quoting error and a test-only unsupported TypeScript option were corrected before the successful full runs. The visual comparison also caught nested drawer styles leaking into the category heading; targeted specificity now preserves the original 28px inset. No failing check is being reported as a pass.

No new external configuration is required. Existing OAuth/reset/legal/LLM/notification limitations remain as documented. This is a local source package, not a deployment or installation on the user's computer. Back up existing databases/private environment files before upgrade.

---

# Previous Transactions delivery (historical verification counts)

# Current implementation status — Transactions

The Transactions page is implemented in the existing application, not a standalone mock or replacement project. Authentication, Overview and the shared persistent sidebar/topbar remain integrated. Figma was inspected read-only, including individual frames and component masters; no design nodes were changed.

## Delivered

- Real `/transactions/*` page, four database-calculated summary cards, type tabs, search/category/wallet/date/amount filters, advanced filters, active chips/reset, sorting and pagination (10/25/50).
- Shared add/edit form with exact safe calculator, type validation, source/destination wallets, transfer/withdraw/fee support, local date/time, description/context/notes, pending/error feedback and unsaved-change confirmation.
- Authenticated SQLite CRUD, optimistic versions, idempotent retries, ownership checks, atomic transfer principal/fee operations and historical balance validation. Transfers do not inflate income/expenses.
- Persistent custom categories with rename/reassignment, minimal wallet setup for new accounts, actual filtered CSV export with quoting/formula protection and explicit privacy consent.
- Existing global monetary privacy state across cards, table, forms and details. Existing Overview actions now connect to actual Transactions operations.
- Subtle authenticated button/dialog/dropdown/sidebar feedback, keyboard focus behavior, native modal background blocking and reduced-motion support. No new dependency.

## Executed verification

**113 automated tests passed**, plus the production build:

| Command (project root unless noted) | Result |
|---|---|
| `npm run build` | PASS — TypeScript + Vite production bundle |
| `npm test` | 44 tests, 6 files passed |
| Backend: `.venv/bin/python -m pytest -q` | 29 passed, 1 existing upstream Starlette/httpx deprecation warning |
| `PYTHON_BIN=/data/fincept-ai/backend/.venv/bin/python PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=$(which chromium) npm run test:e2e` | 40 browser tests passed |

The browser suite starts isolated FastAPI/Vite servers and a disposable SQLite database. It exercises real auth and financial requests; sidebar-only tests deliberately use session/empty-query fixtures. New backend tests cover ownership/CSRF, v2 schema preservation, persistence, atomic rollback, concurrent debits, stale versions/idempotency, transfer fees, filters/CSV and category reassignment. New browser tests verify create-refresh-edit-delete against the backend, overdraft error draft retention, transfers, filters/pagination/export, privacy, categories, loading/error/retry, dirty close, keyboard focus and reduced motion.

Desktop page and dialog geometry is checked at **1440×900, 1366×768, 1280×800 and 1024×768**, minimized and expanded. The document has no horizontal overflow; wide tables scroll within their card. Rendered screenshots and original Figma reference exports are in `transactions-qa/`.

Initial browser failures exposed amount input focus formatting and a modal scroll container covering the transfer submit footer. Both were fixed and regression tests rerun successfully. A sidebar-only session fixture was extended to cover the newly real Transactions API queries; this does not replace real CRUD tests.

## Remaining boundaries

No deployment or installation on the user's computer is claimed. Run locally using START_HERE.md. Back up existing SQLite data before the additive schema v3 upgrade. No new provider keys are required for Transactions. Google OAuth, password recovery, final legal text, LLM/chat and a notification backend retain their previous configuration/implementation limitations. Full Wallets, Budgets, Goals and remaining feature pages are not part of this segment. Native date/time pickers and font antialiasing may differ from Figma. The explicitly labeled development sample has its existing actual records, not fabricated live financial values. See TRANSACTIONS.md for accounting/filtering contracts and documented visual differences, TRANSACTIONS_FILES.md for exact changes.

---

# Historical Overview-only delivery (superseded scope/counts)

# Current implementation status — Overview correction

The full Overview is now implemented in application code, not only the sidebar. The earlier sidebar-only handoff was incomplete relative to the request; this delivery supersedes it.

## Implemented now

- `/overview`: live summary, period filters, historical income/expense chart, category donut/links, budgets, rule-based insight, goals and real server-filtered/paged recent transactions with read-only details.
- Shared original-vector topbar: page search, privacy, profile/settings/signout and honest notifications/AI integration boundaries. Existing persistent sidebar remains shared.
- Additive canonical finance schema and authenticated summary/insight/recent APIs; ledger accounting and explicit, isolated development-only sample workspace.
- Preserved corrected Authentication form/state/validation/assets/security. Post-login confirmation now has an Open Overview link.

Configuration, accounting definitions, endpoints, current limitations, visual differences and start/test commands are detailed in OVERVIEW.md. Exact changed files are in OVERVIEW_FILES.md. No new frontend/backend dependencies or provider secrets are required. Google OAuth/reset/final legal documents and future financial write flows remain unconfigured/unimplemented; Overview does not fake them.

## Current verification

Final verification: **71 automated tests passed**, plus the production build. Earlier counts in the historical sections apply only to those past passes.

- `npm run build`: TypeScript + Vite PASS.
- `npm test`: 22 unit/component tests passed.
- `npm run test:e2e`: 30 browser tests passed (real Authentication, Overview and shared sidebar).
- Backend `python -m pytest -q`: 19 tests passed; one existing Starlette/httpx deprecation warning.
- Test setup corrections: sidebar-only mocked sessions now use explicit empty finance fixtures; Node reads the JSON fixture through fs. Production-sample test uses HTTPS, secure cookies and a trusted local test host. These corrections were followed by successful full reruns, not hidden failures.
- Browser suite used system Chromium and the existing Python virtualenv through the documented executable overrides. No extra runtime dependency was added.

- Actual 1440px sample Overview opened and compared with Figma; 1024px expanded page opened for visual QA. Original scalable icons/charts and live text verified in the running UI.
- Automated geometry covers all four requested desktop viewports in both sidebar states; table scrolling is internal, not page overflow.
- Sample data remains separated from live accounts and is rejected in production.

---

# Historical implementation notes (superseded where noted)

# Authentication implementation status

## Outcome and scope

Implemented a new authentication-only project. Inspection of the available workspace found no existing application repository, framework, router, backend, reusable application components, or run/test scripts to preserve. Therefore React + TypeScript + Vite, React Router, plain CSS, and FastAPI + SQLite were established. Tailwind was not assumed or added. No existing user repository or Figma design was overwritten.

Only Sign Up, Sign In, and supporting authentication routes were implemented. Overview and Transactions are intentionally absent. Authentication success uses `/auth/complete`, a minimal backend-verified protected placeholder. Google OAuth and password reset are not represented as functional.

## Design inspection and fidelity

The actual individual Figma frames were inspected through Figma's connected tools, including frame/component structure and properties, screenshots, and asset export:

- File: `kpEbLoKLaLiUcB8Q6xxgRl`
- Authentication canvas: `2001:5217`
- Sign Up / Desktop: `2001:5220`
- Sign In / Desktop: `2001:5306`

The existing split layout, 1440 × 980 reference, 749/691 column proportions, 500px card, Manrope typography, orange #F9733B, warm #F7F7F4 background, form geometry, financial illustration, brand asset, and Google icon were preserved. Assets are local; no temporary Figma URL is used at runtime. The illustration's transparent export preserves its native aspect ratio, including shadow bounds.

Rendered screenshots were opened and compared against the original frames. An initial illustration scaling/background mismatch was corrected. The final Sign Up, Sign In, validation, loading, invalid-credentials, and protected-placeholder screenshots were individually visually reviewed. Reference and rendered captures are included in this folder. This is manual fidelity QA, not a claim of pixel-identical cross-platform rendering.

## Created files (no existing application files modified)

| Area | Files |
| --- | --- |
| Root/config | `package.json`, `package-lock.json`, `index.html`, `tsconfig.json`, `vite.config.ts`, `.env.example`, `.gitignore`, `playwright.config.ts`, `README.md` |
| Entrypoint/routing/styles | `src/main.tsx`, `src/app/App.tsx`, `src/styles/auth.css` |
| Authentication forms/state | `src/features/auth/AuthForms.tsx`, `src/features/auth/AuthProvider.tsx`, `src/features/auth/validation.ts` |
| API separation | `src/features/auth/services/authApi.ts` |
| Shared auth components | `src/features/auth/components/AuthLayout.tsx`, `src/features/auth/components/FormControls.tsx` |
| Local design assets | `public/assets/auth-financial-illustration.png`, `public/assets/fincept-brand.png`, `public/assets/google.svg` |
| Backend | `backend/app/__init__.py`, `backend/app/main.py`, `backend/requirements.txt`, `backend/requirements-dev.txt`, `backend/.env.example` |
| Tests | `src/test-setup.ts`, `src/features/auth/validation.test.ts`, `src/features/auth/components/FormControls.test.tsx`, `backend/tests/test_auth.py`, `tests/auth.spec.ts` |
| Documentation/evidence | This document, `docs/ASSETS.md`, `docs/licenses/Manrope-OFL.txt`, `docs/figma-*.png`, `docs/rendered-*.png` |

Shared components include AuthLayout, AuthBrandPanel, AuthFinancialIllustration, AuthCard, FormField, PasswordField, PasswordStrength, PrimaryButton, SocialAuthButton, FormError and AuthDivider. Presentation, validation, API requests and session state are separated.

## Backend endpoints

| Method | Route | Behavior |
| --- | --- | --- |
| GET | `/api/health` | Backend readiness |
| GET | `/api/auth/config` | Google and reset capabilities are false |
| POST | `/api/auth/register` | Validate, create user, create cookie session; 201 |
| POST | `/api/auth/login` | Verify Argon2id password, rotate session; 200 |
| GET | `/api/auth/me` | Public user details or 401 |
| POST | `/api/auth/logout` | Revoke current session, clear cookie; 204 |

SQLite initialization creates only users, sessions and rate_limits with schema version 1. Passwords are Argon2id-hashed; random session values are SHA256-hashed before storage. Login responses contain public user details, not passwords, hashes, or token JSON. Cookie sessions are HttpOnly/SameSite=Lax and Secure in production. POST requests require the application custom header and allowed origins. CORS uses an explicit allowlist. Backend validation errors omit rejected input values. IP and per-email rate limiting are stored server-side. Production rejects insecure cookie configuration.

Registration also stores acceptance time and a development draft terms version; replace the legal placeholders and update that version before launch. This is automatic schema initialization, not a production migration framework.

## Verification results

| Check | Result |
| --- | --- |
| `npm test` | PASS — 11 tests (8 validation + 3 shared component) |
| `python -m pytest -q` in backend | PASS — 11 tests; one upstream deprecation warning |
| `npm run test:e2e` | PASS — 11 Chromium browser tests |
| `npm run build` | PASS — TypeScript and Vite production build |
| `npm audit --omit=dev` | PASS — zero production dependency vulnerabilities at verification |
| Desktop visual comparison | PASS — final core pages and captured interaction states reviewed |

Total: **33 automated tests passed.** Browser tests ran with the installed system Chromium and virtual environment Python using `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` and `PYTHON_BIN` overrides.

Covered: both screens, navigation, required fields, invalid email, changing password strength, show/hide password, confirmation mismatch, terms acceptance, real registration, duplicate registration, real login, invalid credentials, loading/repeated-submit prevention, server/network errors and value retention, Remember Me cookies, logout, session expiry/rotation, protected-route behavior and service outage, CSRF/origin rejection, rate limiting, production cookie rules, and truthful unavailable-provider behavior. Test accounts were disposable; no real user credentials or test databases are shipped.

## Known issues and remaining configuration

1. Google OAuth and email password reset require provider/backend configuration and implementation; they are intentionally unavailable.
2. Terms/Privacy content is a clearly marked development placeholder.
3. Original brand/placeholder/disclaimer colors have some normal-text contrast limitations. Full WCAG AA compliance is not claimed.
4. Upstream Starlette TestClient warns about its deprecated httpx integration; tests currently pass.
5. No mobile/tablet variants; small desktop windows use scrolling. Only Chromium has been browser-tested here.
6. Production deployment/security review, HTTPS/reverse proxy, trusted hosts/origins, durable storage/backups, maintenance/session cleanup, and monitoring remain the deployer's responsibility. SQLite and the included local rate limiter are not a claim of distributed production scale.
7. No email verification, MFA, Google account linking, or reset-token lifecycle is implemented. No financial models/APIs exist.

## Run commands

See the root README for Windows/macOS/Linux virtual environment activation and full setup.

Backend (in `backend`, with its venv active):

```sh
python -m pip install -r requirements-dev.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend (project root, separate terminal):

```sh
npm ci
npm run dev
```

Open `http://127.0.0.1:5173/sign-up` or `/sign-in`. Production artifacts are generated with `npm run build`; serve them with an API reverse proxy and SPA route fallback, not as an unauthenticated static-only app.

**Implementation stops at Authentication.**

## Subsequent Figma-first policy audit — documentation only

Added root `CLAUDE.md`, `docs/DESIGN_SYSTEM.md`, `docs/AUTHENTICATION_ASSET_AUDIT.md`, and seven original SVG audit exports under `docs/asset-audit/`; updated `docs/ASSETS.md`. Runtime sources, authentication behavior and Figma content are unchanged.

The prior visual-fidelity/test results remain historical implementation results, **not vector-policy compliance**. The raster brand and flattened illustration require correction; the password-eye icon also differs in provenance from the now-retrieved original. The Google SVG path geometry/fills match the freshly exported original. Original Figma master components and asset availability were inspected and documented. SVG XML/no-embedded-image checks passed for all seven audit exports. No runtime tests were rerun for these documentation-only changes. Wait for the next implementation instruction before performing the correction pass.

## Authentication vector correction — IMPLEMENTED

This completed runtime correction supersedes the earlier audit-only blockers. No backend/authentication logic was changed.

### Actual code and asset changes

- Added AuthBrand with the original SVG logo mark and live Manrope wordmark; used it in AuthBrandPanel and the protected confirmation.
- Replaced AuthFinancialIllustration's flattened PNG with a shared HTML/CSS/SVG composition: live savings/category/disclaimer text, reusable category cards, original chart/icons and vector progress ring.
- Replaced the Lucide password-eye rendering with the original Figma eye SVG, preserving the existing show/hide state, labels and input behavior. The same original eye is retained for both states; no original eye-off asset is claimed.
- Promoted six saved audit SVGs to `public/assets/auth/` without re-fetching. Existing `public/assets/google.svg` is unchanged and remains on SocialAuthButton.
- Removed every `fincept-brand.png` and `auth-financial-illustration.png` reference from application sources. Both source PNGs remain in the repository as unused legacy references.
- Added a locally licensed U+09F3-only Noto Sans Bengali subset because Manrope does not contain the taka glyph; all Latin typography remains Manrope.
- Updated the asset audit, provenance and design instructions to reflect integration rather than pending work. Exact changed/added files are in `docs/ASSET_CORRECTION_FILES.md`.

### Checks rerun after final code changes

| Check | Result |
| --- | --- |
| `npm run build` | PASS — TypeScript + Vite |
| `npm test` | PASS — 13 tests |
| `npm run test:e2e` | PASS — 12 browser tests |
| Backend `python -m pytest -q` | PASS — 11 tests; one existing upstream warning |
| Original asset integrity | PASS — six promoted SVG files byte-identical to saved originals, no raster/script/external-href content |
| No logic/backend drift | PASS — 15 protected backend/auth logic/Google/dependency/config files unchanged by hash |
| Both live pages at native browser zoom | PASS — 100%, 125%, 150%; six captures, all assets loaded, live text, no PNG requests, visibility toggles work |

**36 regression tests passed**, plus six native-zoom page checks. Vite and the existing FastAPI backend were actually run. Both actual routes were opened. Captures were inspected individually; the 100% rendering was compared to the original Figma reference. Validation, loading, invalid-credential and protected-confirmation captures were refreshed and reviewed.

Zoom method: test-only Chromium extension calling chrome.tabs.setZoom/getZoom, CSS zoom unchanged, initial deviceScaleFactor 1. The physical viewport is 1440 × 980. Effective CSS viewports at 125%/150% are narrower and the existing desktop minimum canvas scrolls; no mobile/tablet layout was introduced. Full-document captures account for native zoom rather than clipping to the reduced CSS viewport. Evidence: `docs/asset-correction-zooms/verification.json` and six PNG captures. Script: `tests/verify-asset-zoom.mjs` (requires running local frontend/backend and Chromium with unpacked-extension support).

### Remaining visual/configuration limits

No missing assets, missing glyphs or unintended overlap observed. Minor browser antialiasing, CSS shadow rasterization and currency fallback metric differences from Figma may remain; pixel identity is not claimed. Manrope lacks U+09F3 and Figma does not identify its own fallback for that glyph. The original eye icon remains in both visibility states, with the existing accessible Show/Hide labels and aria-pressed state.

Google OAuth, password reset, legal placeholders and production deployment configuration remain as previously documented. This correction does not configure those services or change authentication behavior. No other segment was implemented.

## Combined project ZIP — corrected Authentication + shared Sidebar

Recovered the actual `FINCEPT-AI-Authentication-Vector-Corrected.zip` from the earlier session delivery, then merged the shared sidebar into that base. The combined ZIP already includes all needed source; no user-side file merging is required. The previous sidebar-only workspace limitation no longer applies to this combined package.

Original corrected authentication components, auth CSS, local vector assets/font fallback and backend source are preserved. The shared route parent retains the corrected AuthBrand on the protected landing. A visual check found the shell's generic word-wrapping rule could split that wordmark; a scoped `.application-main .brand-logo` nowrap rule fixes this without changing authentication component source. Tests assert this behavior. One sidebar test typing issue was corrected before the successful TypeScript build.

Validation is recorded in `docs/COMBINED_PROJECT.md`. Full Overview/other financial segments remain placeholders. Google OAuth and email reset remain unconfigured. No production credentials or user/test databases are shipped. Start with root `START_HERE.md`.

## Combined verification results

- Production TypeScript/Vite build: PASS.
- Unit/component tests: 17 passed.
- Browser tests: 20 passed, including real registration/login, corrected auth vector references, protected routes, sidebar persistence/navigation and all four specified viewport sizes.
- Backend tests: 11 passed; one existing Starlette/httpx deprecation warning.
- Total: **48 automated tests passed**.
- Visually reopened combined Sign Up, Sign In, protected landing and expanded 1024px sidebar captures. Preserved vector illustrations, local Manrope font, Taka fallback and original SVG icons. Fixed and rechecked protected-landing wordmark wrapping. Sidebar geometry tests pass at all requested sizes.
- Compared 24 corrected-base source/asset/dependency files byte-for-byte; unchanged. No old auth PNG references remain in React components.

Build/test commands are the existing package scripts and backend pytest command. Browser tests used system Chromium and the existing Python virtualenv via PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH/PYTHON_BIN overrides. Dependencies are installed locally inside the project for testing; node_modules and virtualenv are deliberately excluded from the ZIP.

## Planner — Calendar & Tasks release verification
Implemented in the existing application at `/planner`; no Figma writes. See PLANNER.md for design inspection, exact API/date semantics, accounting and limitations, and PLANNER_FILES.md for file map. Additive schema v9; canonical Financial Goals IDs/contributions are reused rather than duplicated. All task/calendar and create/edit/archive/reviewed-contribution plan controls connect to real authenticated SQLite-backed APIs. New users remain empty. No reminder delivery, automatic transfers or fabricated financial calendar entries.

### Actual final commands and outcomes
- `npm run build` — passed. Vite warns that the main minified JS chunk is approximately524kB, above its500kB advisory threshold; no compile/build errors.
- `npm test` — **92 passed**,14 files. Includes10 Planner civil-date cases (every month1901–2100), and2 new Assistant abort/invalid-body regression cases.
- `PYTHONPATH=backend backend/.venv/bin/python -m pytest backend/tests -q` — **138 passed,1 skipped**. The skip is the existing opt-in paid liveAI test requiring configured provider/model/key and RUN_LIVE_AI_TEST=1. Existing Starlette/httpx deprecation and Pydantic alias warnings remain. New Planner file independently passed33 tests.
- `PYTHON_BIN="$PWD/backend/.venv/bin/python" PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/local/bin/chromium npm run test:e2e` — **99 passed** in5.0minutes, including9 Planner scenarios and existing authentication, shell, Overview, Transactions, Wallets, Budgets, Goals, Insights and Assistant regression coverage.
- `npm audit --omit=dev --json` — **zero reported production dependency vulnerabilities**.
- Planner SVG XML validation — passed, original vector retained; provenance/SHA-256 supplied.

Desktop browser checks:1440×900,1366×768,1280×800,1024×768; both sidebar states, document overflow, internally scrollable task forms, privacy and keyboard navigation. Original references and real running captures are in planner-qa. Source screenshot sample values were not copied into application data.

### Failures found and fixed before the final pass
- Initial browser binary path was wrong; verification used the installed `/usr/local/bin/chromium`.
- Four existing backend migration-version assertions were updated8→9; business assertions unchanged.
- Explicit form labels, pending checkbox feedback, keyboard focus across month changes, invalid URL month feedback and occasion/status filtering were corrected.
- Original four status tabs restored; All includes cancelled records instead of adding a cramped fifth tab.
- Playwright screenshot cleanup could delete the live test DB in its output directory. `outputDir` now isolates generated artifacts under `test-results/artifacts`, preserving the DB at its established test path.
- Full regression exposed an intermittent **existing Assistant** response-body abort race: JSON cancellation was swallowed into an empty success object, then history accessed missing items. A minimal API transport fix preserves aborts/reports malformed JSON, with2 added unit tests. No Assistant redesign.

### Explicit release limits
Not deployed or installed on the user's PC. Planner needs no API key. Reminder fields are intentionally disabled; no email/push/calendar delivery or recurrence infrastructure exists. Optional task time is wall-time metadata, not an instant/alarm. Richer prototype-only expense-breakdown editors and Planner contribution edit/delete/release panels are not implemented/exposed. Existing Goals history/allocation rules remain authoritative. Other previously documented OAuth/reset/AI configuration requirements remain. No pixel-identical, production-ready or WCAG-certification claim is made.


## Debt & Loans + Financial Hub release (schema v10)

Existing React/FastAPI application extended, not replaced. Read-only Figma preflight and original SVG provenance are recorded in DEBT_HUB_DESIGN_MAP.md and ASSETS.md. No Figma writes. New accounts have no fabricated debt, shopping or calendar records.

Debt includes Borrowed/Lent/EMI tabs, real persisted creation/editing, reviewed schedule preview, partial/full tracked payments, immutable correction reversals, settled-only archive, derived commitments/history, filters/sort, and global monetary privacy. Hub reads canonical wallet balances, supports persisted shopping list/item CRUD and purchase tracking, routes shortcuts/wallet activity, derives upcoming actual Planner/EMI activities and provides genuine indicative FX.

## Executed checks
- `npm run build`: passed after final code/style changes. Vite main minified JS 574.70 kB, above its 500 kB advisory; no TypeScript/build errors.
- `npm test`: **103 passed**, 15 files.
- `PYTHONPATH=backend backend/.venv/bin/python -m pytest backend/tests -q`: **166 passed, 1 skipped**. Existing credential-dependent live-AI test skipped; one existing Starlette/httpx deprecation warning.
- Full `npm run test:e2e` with PYTHON_BIN and PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH overrides: **108 passed** in 7.2 minutes, including all previous feature regressions and the first nine new Debt/Hub scenarios.
- After the final original-icon/CSS refinements, `npm run test:e2e -- tests/debt-hub.spec.ts`: **12 passed** in 1.1 minutes. This rerun overlaps nine cases from the full suite and adds three; it is not a separate 120-test unique total. All twelve ran against final code.
- `npm audit --omit=dev --json`: **zero reported production dependency vulnerabilities**.
- A genuine authenticated `/api/hub/rates?base=BDT` request, without mocked provider data, returned HTTP 200 and ten supported currencies. See `live-provider-check.json` for provider/fetch timestamps. No API key was required.

The browser suite used the existing FastAPI/SQLite app and isolated real accounts/records. FX success/error/cache states in deterministic browser screenshots use explicit test response fixtures (including intentionally synthetic 1:1 rates); those screenshots are not evidence of a real quoted exchange rate. Genuine live-provider evidence is separate. No fixtures are used as application fallback rates.

## Desktop visual QA
1440×900, 1366×768, 1280×800 and 1024×768, with sidebar states and dialog/overflow checks; also 1440×1320 and 1440×1620 reference-size captures. Borrowed/Lent/EMI/Hub captures are saved here alongside forms, reviewed payment, privacy and error states. Final 1440 reference captures were reopened for visual inspection. Original Figma main frame references are QA-only, never runtime UI.

Hierarchy, widths, surfaces, color, typography and original icons follow the reference. Real saved data, provider attribution/freshness and extra supported archive/error states legitimately differ from sample frame content. Browser font/rasterization and content-dependent section heights differ; pixel identity is not claimed. Screenshots include isolated test data only, not shipped live database rows.

## Boundaries and setup
- Additive SQLite schema **v10**; back up an existing database before startup migration. Existing auth, canonical ledger, Goals, Planner and Assistant data are preserved.
- Debt payments are **manual tracking only**: no wallet movements, bank transfers or income/expense records. Initial principal and down-payment metadata likewise do not move money. EMI principal is included once in borrowed totals.
- Interest supports an explicit agreed fixed total, not APR/amortization/accrual. Dates use civil dates and the browser IANA timezone; dates passing do not automatically mark payments paid.
- Shopping actual costs are entered tracking values, not verified expenses. No automatic transaction matching/linking or expense creation; Open Transactions is navigation only.
- No email/push reminders, bank connectivity or external payment execution. FX is indicative, daily-provider dependent, cached one hour, stale visibly bounded to 48 hours; outbound HTTPS is required. There is no production deployment in this delivery.
- Existing Google OAuth/password-recovery/legal/optional AI credential limits remain documented elsewhere. New Debt/Hub features need no new secrets.

## File map
Frontend: `src/features/debt/{Debts,DebtForms}.tsx`, `api.ts`; `src/features/hub/{Hub,ShoppingForms,CurrencyConverter}.tsx`, `api.ts`, `hub.test.ts`; `src/styles/debt-hub.css`; route/header wiring; minimal Wallets deep-link handling.
Backend: `backend/app/debt/{schema,routes}.py`, `backend/app/hub/{routes,fx}.py`, main startup/router wiring; `backend/tests/test_debt_hub.py`. Shared schema-version test assertions advance to v10 without changing their business assertions.
Docs: DEBT_LOANS.md, FINANCIAL_HUB.md, DEBT_HUB_DESIGN_MAP.md, assets provenance, architecture/status/setup notes and this evidence folder. No new runtime dependencies.
## Docker deployment

- Added a multi-stage frontend image that builds the Vite app and serves it
  through Nginx with SPA fallback and `/api` proxying.
- Added a FastAPI image with a non-root runtime user and a persistent SQLite
  data volume.
- Added `docker compose up --build` as the single-command local container
  deployment. Docker validation is environment-dependent and should be run on
  a host with Docker Engine/Compose available.
- Made the Nginx backend upstream configurable through `BACKEND_URL` for
  container environments where the backend hostname differs.
- Updated the primary README workflow to be Docker-only: host users no longer
  install or start npm, Node.js, Python, pip, FastAPI, or Uvicorn manually.
- Restricted Nginx template substitution to `BACKEND_URL` so normal Nginx
  runtime variables are preserved and the frontend container starts reliably.
