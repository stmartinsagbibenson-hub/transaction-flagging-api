# Transaction Risk Flagging API --- Product Requirements Document

## 1. Project Overview

Build a **FastAPI transaction risk-flagging service** that evaluates synthetic banking transactions using clear, explainable rules. The service checks transaction amounts against a configurable threshold, flags activity at unusual hours, and detects multiple rapid withdrawals. It also converts transaction amounts to a configured base currency using current exchange-rate data from a public API.

Before writing code, students must design the ATM withdrawal flow as a flowchart and pseudocode. This makes the decision sequence visible before it is implemented as API behavior.

This is an educational simulation. It does not authenticate real customers, connect to a bank, move money, block transactions, or prove fraud. A risk flag is a reason for review, not a finding that a customer or transaction is malicious.

## 2. Problem Statement

Financial systems combine many small decisions: whether a user is authenticated, whether an account has enough available balance, whether a withdrawal follows the rules, and whether the transaction should be completed. Separately, monitoring systems look for transaction patterns that may need review. Engineers should make these rules explicit, test their boundaries, and communicate what a system can and cannot conclude before connecting those rules to an application or external service.

This project brings together planning and flowcharts (Week 1), Python decisions and functions (Week 3), and APIs, external services, and professional Git workflow (Week 8). Students will first reason through a simulated ATM withdrawal, then implement a transaction risk checker as a documented API.

## 3. Goals and Success Criteria

### Goals

- Design an ATM withdrawal flow before implementation using a flowchart and pseudocode.
- Implement explainable transaction risk rules using Python conditionals and functions.
- Expose the checker through a FastAPI application with validation and useful responses.
- Convert transaction amounts to a base currency using current rates from a public exchange-rate API.
- Track recent withdrawals per synthetic account to identify rapid activity.
- Write automated tests for normal, boundary, invalid, and external-service failure cases.
- Document setup, endpoints, rules, assumptions, and limitations in a new GitHub repository.

### Success criteria

- A reviewer can understand the ATM decision flow without reading the implementation.
- The API flags each matched rule and explains why it matched.
- Transaction amount comparisons use a consistent base currency and decimal-safe arithmetic.
- Rapid-withdrawal rules are deterministic and covered by tests.
- Missing, invalid, or unavailable exchange-rate data produces a clear response, never a silent or fabricated conversion.
- The README explains how to run and test the service and how to interpret flags.

## 4. Scope

### In scope — required features

#### A. Pre-coding ATM flow design

Create a flowchart and matching pseudocode for a single simulated cash withdrawal. Include at least:

1. Card/account identifier supplied.
2. User authentication succeeds or fails.
3. Requested amount is valid, positive, and within the ATM's supported withdrawal rules.
4. Account is active and has sufficient available balance.
5. Withdrawal limits are checked (per transaction and, in the design, a daily limit).
6. The withdrawal is approved or declined with a clear reason.
7. On approval, the balance is updated exactly once and the transaction is recorded.
8. Completion/failure is communicated to the user.

The design is a reasoning deliverable. The FastAPI project does not implement real authentication, maintain real bank balances, dispense cash, or execute this ATM flow against real accounts.

#### B. Transaction risk rules

Evaluate each submitted transaction against documented, configurable rules:

- **Large amount:** the transaction's converted amount is greater than or equal to a configured base-currency threshold.
- **Unusual hour:** the transaction timestamp falls within a configurable local-time interval, including intervals that cross midnight. The timezone used for this rule must be explicit.
- **Rapid withdrawals:** a configured number of withdrawals for the same synthetic account occur within a rolling time window, including the current withdrawal.

Each matched rule must produce a stable rule identifier and a plain-language explanation. The response should include all applicable flags, not stop after the first match. A transaction with no matched rules should return an explicit no-flags result.

Use sensible documented defaults, such as a large-transaction threshold of NGN 500,000, an unusual-hours interval of 00:00–05:00 WAT, and 3 or more withdrawals within 10 minutes. These are teaching examples, not universal banking standards. Let configuration be changed through application settings or a documented configuration file; do not require code edits to tune the rules.

#### C. Exchange-rate conversion

- Integrate with a public exchange-rate API that supports the currencies used in the sample and demo. Verify currency availability when choosing the provider and document the provider, endpoint, attribution/terms, rate timestamp, and any usage limits.
- Allow a transaction currency and configured base currency (default `NGN`). Return the original amount/currency and converted amount/base currency, along with the rate and rate date/time used when available.
- Use `Decimal` (or another explicit decimal-safe approach) for monetary values and document rounding.
- Do not assume the API is always available. Apply a finite timeout, handle network errors, bad responses, unsupported currency pairs, and missing rates clearly, and never silently treat the source amount as the converted amount.
- Cache rates for a short documented period if useful, but identify the rate time in the response. Tests must not depend on a live external API; mock the provider client.

If live rates are unavailable, the API may return a service-unavailable response for conversion-dependent evaluation. It must not claim a current-rate result using stale or hard-coded data without clearly identifying it as cached data and its timestamp.

#### D. FastAPI service

Provide a FastAPI app with:

- `GET /health` — confirms that the API process is running and identifies the application/version.
- `GET /rules` — returns the active rule settings, base currency, and timezone.
- `POST /transactions/evaluate` — validates and evaluates one synthetic transaction.
- `POST /transactions/evaluate/batch` — evaluates a bounded list of transactions and reports per-item results and validation failures. Batch support should preserve deterministic rapid-activity behavior by processing events in timestamp order and explaining that ordering in the API documentation.
- OpenAPI documentation available through FastAPI's standard docs route.

Exact route names may differ if the README documents equivalent behavior. Use request and response models. Return appropriate HTTP status codes and actionable validation or dependency errors. Avoid returning stack traces or internal secrets.

#### E. Transaction data and state

Use synthetic transactions only. A minimum request record should include:

| Field | Description | Example |
|---|---|---|
| `transaction_id` | Unique synthetic event identifier | `TXN-1001` |
| `account_id` | Synthetic account key used for grouping | `ACCT-001` |
| `timestamp` | ISO 8601 timestamp with timezone | `2026-11-12T01:15:00+01:00` |
| `transaction_type` | At minimum `withdrawal` or `purchase` | `withdrawal` |
| `amount` | Positive decimal amount | `750000.00` |
| `currency` | ISO 4217 currency code | `NGN` |

Rapid-withdrawal state must be implemented in a way suitable for the educational API: document whether it is in-memory for one process/run or stored locally. If in-memory, explain that restarts clear history and multiple workers do not share state. Do not imply it is production-ready distributed state.

Do not request or store passwords, PINs, card numbers, account credentials, or other real payment data. The `account_id` must be synthetic and non-sensitive.

#### F. Sample data and demonstration

Include a small synthetic sample dataset or ready-to-use request examples that demonstrate:

- A normal transaction with no flags.
- A large transaction.
- An unusual-hour transaction.
- A rapid-withdrawal flag on the transaction that reaches the configured count.
- A transaction triggering more than one rule.
- At least one non-base currency conversion.

The provided `tutor/week9/banking_transactions.csv` may be used as inspiration for the schema and scenario design, but it contains account-like identifiers. Do not copy those values into a new public repository; generate clearly synthetic identifiers and records.

### Out of scope

- Real bank, ATM, card-network, identity-provider, or payment-provider integration.
- Real authentication, PIN verification, cash dispensing, balance reads/updates, or transaction authorization.
- Blocking, reversing, or holding a real transaction.
- Machine learning, geolocation, external reputation lookups, or claims that a flag proves fraud.
- Storing real customer data or credentials.
- Production fraud detection, financial advice, or regulatory compliance certification.

## 5. Functional Requirements

### 5.1 ATM planning artifact

- Submit a readable flowchart (Mermaid, image, or another clear format) and pseudocode before or alongside the first implementation milestone.
- Include both approval and decline branches, and distinguish authentication failure from business-rule declines such as insufficient funds or a limit breach.
- State assumptions about available balance, withdrawal amount units, daily limit reset, and what happens if completion fails after approval.
- Ensure the flowchart and pseudocode express the same decision order.

### 5.2 Risk evaluation

- Validate transaction ID, synthetic account ID, positive finite amount, supported transaction type, currency code, and timezone-aware timestamp.
- Compare converted amount to the configured threshold using decimal-safe arithmetic and a documented inclusive/exclusive boundary.
- Evaluate unusual hours using the configured timezone, not the server's local timezone.
- Count rapid withdrawals separately per account, in a rolling time window, using timestamps rather than request arrival order. Document handling of duplicate IDs and out-of-order events.
- Return a risk level or summary derived from the matched rules, plus the full list of rule IDs, explanations, and relevant evidence (for example, threshold, converted amount, window count, or local hour).
- Make it clear that a flag indicates a pattern for review; it is not a confirmed attack or fraud determination.

### 5.3 API validation and errors

- Reject invalid request bodies with clear field-level messages.
- Bound batch size and reject empty or excessively large batches with a documented limit.
- Return useful errors for unsupported currencies and exchange-service failures.
- Use suitable HTTP status codes and consistent JSON error shapes.
- Do not expose tracebacks, API credentials, or sensitive request content in error responses or logs.

### 5.4 Exchange rates

- Use current public rate data for evaluations requiring currency conversion.
- Include the rate source and rate timestamp/date in successful converted results.
- Use a timeout and handle HTTP failures, invalid JSON, absent currency pairs, and malformed numeric values.
- Make network-dependent code separable from risk-rule logic so it can be mocked in tests.
- Do not make the test suite depend on network access or on the exchange provider's current response.

## 6. Technical Expectations

- Python 3.11 or later and FastAPI; use Pydantic request/response models.
- Use `Decimal` for amount/rate arithmetic and timezone-aware `datetime` values.
- Separate API routes, schemas, risk rules, exchange-rate client, configuration, and state/storage concerns.
- Keep rule functions small and explainable. Avoid one large route handler containing parsing, networking, state, and all rule logic.
- Load thresholds, time windows, timezone, and base currency from configuration with safe defaults and validation.
- Keep secrets out of the repository. Prefer a public endpoint that needs no key; if a provider requires a key, include `.env.example`, ignore real `.env` files, and document setup without committing credentials.
- Include automated tests for the core rules, API response behavior, validation, and mocked exchange service.
- Provide dependency and run instructions, such as `requirements.txt` or `pyproject.toml` and a documented `uvicorn` command.

## 7. Suggested Project Structure

```text
transaction-risk-api/
├── README.md
├── PRD.md
├── .gitignore
├── pyproject.toml
├── docs/
│   ├── atm_withdrawal_flowchart.md
│   └── atm_withdrawal_pseudocode.md
├── data/
│   └── sample_transactions.json
├── src/
│   └── transaction_risk_api/
│       ├── __init__.py
│       ├── main.py
│       ├── api.py
│       ├── schemas.py
│       ├── config.py
│       ├── rules.py
│       ├── exchange_rates.py
│       └── state.py
└── tests/
    ├── test_rules.py
    ├── test_api.py
    └── test_exchange_rates.py
```

Students may adapt the structure if API, validation, rule logic, exchange-rate access, and state responsibilities remain clear and testable.

## 8. Delivery Window: 30 Hours

**Total elapsed time:** 30 hours from the cohort's announced start time. The instructor will communicate the exact start and deadline. The milestone windows below are elapsed hours from that start.

| Stage | Elapsed window | Focus | Expected output |
|---|---:|---|---|
| 1. Understand and plan | Hours 0–3 | Read the brief and sample transactions. State assumptions, sketch the ATM decisions, choose the currency provider, and outline API routes and data models. | Initial design notes, repository created, ATM flowchart and pseudocode draft. |
| 2. Finish design and project setup | Hours 3–6 | Check that flowchart and pseudocode agree. Create the FastAPI app skeleton, dependencies, configuration, and health/rules routes. | Reviewable ATM design, running API skeleton, README setup outline. |
| 3. Transaction schemas and validation | Hours 6–10 | Define request/response models and validate identifiers, timestamps, amounts, currencies, transaction types, and batch limits. | Working validation and documented request examples. |
| 4. Risk rules | Hours 10–15 | Implement large-amount, unusual-hour, and rolling rapid-withdrawal rules with explicit evidence in results. | Rule engine with deterministic behavior and initial unit tests. |
| 5. Exchange-rate integration | Hours 15–19 | Implement the public API client, timeout/error behavior, rate metadata, decimal-safe conversion, and mocked tests. | Conversion works for supported pairs; failures are clear and covered. |
| 6. API integration and state | Hours 19–23 | Connect single and batch evaluation routes, rapid-activity state, configuration, and response/error models. | End-to-end API behavior with OpenAPI docs and sample requests. |
| 7. Tests, documentation, and cleanup | Hours 23–27 | Complete rule/API/error tests, document setup and limitations, review secrets and repository hygiene, and improve examples. | Complete tests and README; synthetic data and clean repository. |
| 8. Final verification and submission | Hours 27–30 | Run documented checks, demonstrate endpoints, confirm repository description and PR, and record the walkthrough. | New GitHub repository, final PR, test evidence, and demo of 25 minutes or less. |

Students should solve and document the ATM decision problem before spending time polishing API features. Prioritize correct, explainable core rules and failure behavior over extra endpoints or deployment.

## 9. GitHub Workflow and New Repository

- Create a **new repository** for this project; do not place the implementation in the cohort repository.
- Suggested repository name: **`transaction-risk-flagging-api`**.
- Suggested repository description: **“An educational FastAPI service that evaluates synthetic transactions using explainable amount, unusual-hour, and rapid-withdrawal rules, with live exchange-rate conversion.”**
- Include the PRD or a link to the assignment, an informative README, source, tests, and synthetic examples.
- Create a feature branch and open a pull request targeting the new repository's `main` branch. Do not push project work directly to `main`.
- Keep commits focused, use a clear PR description, and include the commands run and evidence that tests passed.
- Do not commit secrets, local virtual environments, caches, generated artifacts, or real financial data.

## 10. Submission Deliverables

- New repository named `transaction-risk-flagging-api` (or another suitable, clearly named equivalent) with a useful description of the tool.
- FastAPI source code, dependency configuration, and `.gitignore`.
- ATM withdrawal flowchart and matching pseudocode, completed before or alongside implementation.
- README with installation, configuration, run instructions, endpoint examples, rule defaults, exchange-rate provider details, and limitations.
- Synthetic sample transactions or request examples covering all required rules and a non-base currency.
- Automated tests and instructions for running them, with the exchange API mocked in tests.
- A final pull request in the new repository with test evidence.
- A walkthrough video of no more than 25 minutes demonstrating design reasoning, API docs, a normal evaluation, each risk flag, conversion, and at least one error case.

## 11. Acceptance Criteria

- [ ] ATM flowchart and pseudocode cover authentication, amount validation, balance, withdrawal limits, approval/decline, recording, and user response; their decision order agrees.
- [ ] FastAPI starts locally and provides health, active rules, and transaction evaluation endpoints.
- [ ] Request and response schemas are validated and documented through OpenAPI.
- [ ] Large amount, unusual local hour, and rapid withdrawal rules work at documented boundaries.
- [ ] Results include stable rule IDs and plain-language reasons for every matched rule.
- [ ] Exchange conversion uses a live public rate, decimal-safe calculations, and reports the rate source and date/time.
- [ ] Exchange-service and invalid-input errors are handled clearly without fake conversions or stack traces.
- [ ] Rapid-withdrawal grouping, ordering, state lifetime, and duplicate handling are documented.
- [ ] Automated tests cover each rule, boundary cases, invalid requests, and mocked exchange API failures.
- [ ] README includes setup, sample requests, configuration, tests, provider details, and educational limitations.
- [ ] The implementation is in a new repository with a suitable name and description; no real credentials or sensitive data are committed.
- [ ] Final PR targets `main` in the new repository and includes test evidence and a walkthrough link.

## 12. Evaluation Rubric (100 points)

| Criterion | Points | What is assessed |
|---|---:|---|
| Pre-coding problem solving | 15 | ATM flowchart and pseudocode are complete, readable, consistent, and state assumptions. |
| Core risk rules | 20 | Amount, unusual-hour, and rapid-withdrawal rules work and return explainable evidence. |
| API design and validation | 15 | FastAPI routes, schemas, status codes, batch behavior, and errors are clear and usable. |
| Exchange-rate integration | 15 | Public API integration, conversion, rate metadata, timeouts, failure handling, and mockability. |
| Correctness and edge cases | 10 | Boundaries, timezones, ordering, duplicate IDs, malformed input, and state behavior are considered. |
| Testing | 10 | Automated tests cover rules, API behavior, errors, and mocked external-service behavior. |
| Code quality and repository practice | 5 | Readable modular code, meaningful names, clean history, suitable new repo, and no sensitive data. |
| Documentation and communication | 10 | README, assumptions, endpoint examples, demo, and clear interpretation/limitations. |
| **Total** | **100** | |

## 13. Security, Assumptions, and Limitations

- All transaction and account data must be synthetic. Never use real account, card, PIN, or customer data.
- This service only flags patterns in supplied requests. It does not authenticate users, approve or decline real transactions, or prevent loss.
- A large amount, late hour, or rapid sequence can have legitimate explanations. Flags are not proof of fraud or malicious intent.
- Exchange rates vary over time and providers may be delayed, unavailable, rate-limited, or unsupported for a currency. Show the rate date/time and provider; do not present a conversion as current without rate metadata.
- In-memory rapid-withdrawal state is suitable only for a local learning project. It may reset on restart and is not shared across worker processes.
- Timestamp interpretation must be timezone-aware and documented. Server timezone must not silently control the unusual-hour rule.
- Thresholds and example rules are illustrative. Real institutions require domain analysis, privacy controls, audits, and careful false-positive management.

## 14. Guiding Principle

**Solve the decision problem first, then encode it as rules, then expose those rules through an API.** Make every flag explainable, every assumption visible, and every limitation honest.
