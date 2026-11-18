# Week 9 Quiz 4 Submission Feedback

## Submission reviewed

- Project: Transaction Risk Flagging API
- Rubric: `PRD.md`, Section 12, and the scores recorded in this file
- Review basis: submitted source code, README, PRD, tests, CI workflow, sample data, ATM planning documents, and the review scores provided

## Final score

**59.7/100 — Core implementation is present; edge-case handling, ownership, and communication need substantial improvement**

The submission has a clear Python package structure, a FastAPI app, transaction models, separate risk-rule and state modules, individual and batch endpoints, automated tests, and CI configuration. Several core risk checks and error paths are represented, and the student demonstrated the CLI/API working during review.

The score reflects the review scores provided: technical execution 66.7%, understanding and ownership 46%, problem-solving 58%, communication and demonstration 36%, and code quality/professional practice 90%. The strongest areas are modularity, tests, documentation, and repository practice. The main gaps are edge cases, explaining the code and outputs, tracing the complete data flow, and distinguishing risk flags from proof of fraud. The codebase review also found issues that should inform the next iteration: timezone conversion is not applied before unusual-hour checks, the exchange-rate response omits rate metadata and converted amount, and the ATM planning documents do not describe the required ATM withdrawal flow.

## Scoring breakdown

### 1. Technical execution — 20/30 weighted (66.7%)

| Criterion | Score | Feedback |
| --- | ---: | --- |
| Core features implemented | 4.5/5 | The project includes a FastAPI service, single and batch evaluation, exchange conversion logic, withdrawal history, and several explainable risk rules. Some PRD requirements are not fully realized in the response or design artifacts. |
| Correct Python logic | 3.5/5 | The main rule functions and API flow are implemented. Unusual-hour checks use the timestamp's own hour rather than converting it to configured `Africa/Lagos` time, and the exchange-rate path needs verification against its provider and expected response. |
| Functions and modules used appropriately | 5/5 | API routes, schemas, configuration, rules, exchange conversion, and state are separated into focused modules. |
| File handling, regex, errors, and tests work | 5/5 | There is no regex requirement in this project. Tests cover core rules, request validation, batch evaluation, and selected exchange errors; the API returns a service-unavailable response for conversion errors. |
| Edge cases handled | 0/5 | The review score indicates no demonstrated edge-case handling. Repository evidence also leaves important cases unverified, including timezone boundaries, exact rule-window boundaries, unsupported currencies, malformed provider responses, duplicate transactions, and missing or naive timestamps. |
| No major crashes or hard-coded paths | 2/5 | No fixed local file path drives the API, but provider behavior is not established end to end, and several request and configuration edge cases remain. The docs URL in the README also does not match the configured `/api/docs` path. |

**Raw score: 20/30; weighted score: 20/30**

### 2. Understanding and ownership — 9.2/20 weighted (46%)

| Criterion | Score | Feedback |
| --- | ---: | --- |
| Explains what each major module does | 1.5/5 | The review showed limited explanation of the modules, despite the code being separated into clear responsibilities. Practice describing each module's input, work, and output. |
| Understands key functions and decisions | 2/5 | The student showed partial understanding of key functions, but needs to explain why thresholds and risk levels are set as they are and how matched rules affect the result. |
| Can trace input through the program | 2.5/5 | Some flow was understood, but the complete route from request validation through conversion, history lookup, rules, state update, and response was not explained consistently. |
| Can identify and fix a bug | 3/5 | The student made some progress identifying and fixing a bug. Continue practicing a repeatable debugging approach: reproduce, isolate, change, and verify. |
| Can explain limitations honestly | 2.5/5 | Some limitations were discussed, but the project should be explained consistently as an educational simulation with in-memory state, and flags as signals for review rather than proof of fraud. |

**Raw score: 11.5/25; weighted score: 9.2/20**

### 3. Problem-solving and critical thinking — 11.6/20 weighted (58%)

| Criterion | Score | Feedback |
| --- | ---: | --- |
| Identifies assumptions and risks | 3.5/5 | The student identified several assumptions and risks. Make assumptions explicit around timestamps, state lifetime, duplicate events, exchange-rate availability, and thresholds. |
| Tests malformed, empty, missing, or unexpected input | 4/5 | The tests cover invalid amounts and selected exchange failures. Add evidence for missing required fields, empty or oversized batches, unsupported currencies, malformed provider data, and timezone edge cases. |
| Explains trade-offs | 2.5/5 | Some trade-offs were recognized, but the student should be able to explain choices such as in-memory state, rule thresholds, batch ordering, and external rate availability. |
| Distinguishes suspicious activity from confirmed attacks | 1.5/5 | This distinction was not explained clearly enough. A large, unusual-hour, or rapid transaction is only a reason to review; it does not establish malicious intent. |
| Suggests realistic improvements | 3/5 | The student suggested some improvements. Strengthen them by naming a concrete change and explaining what risk or user problem it addresses. |

**Raw score: 14.5/25; weighted score: 11.6/20**

### 4. Communication and demonstration — 5.4/15 weighted (36%)

| Criterion | Score | Feedback |
| --- | ---: | --- |
| Clear project explanation | 1/5 | The explanation did not clearly establish the problem, the API's role, and what a risk flag means. Start with those points before showing implementation details. |
| Well-organized walkthrough | 1/5 | The walkthrough needs a clearer sequence. Present one transaction from request to response, then demonstrate a rule trigger, a batch, and an error case. |
| Demonstrates the CLI/API working | 4/5 | The student demonstrated the service working. Include the exact request, response, and command in the walkthrough so the result is easy to follow. |
| Explains outputs in plain language | 1/5 | The risk level and flag reasons were not translated into clear user-facing meaning. Explain what each output says and what it does not prove. |
| Answers questions directly and confidently | 2/5 | Answers were sometimes unclear or incomplete. First answer the question directly, then give a short example or limitation. |

**Raw score: 9/25; weighted score: 5.4/15**

### 5. Code quality and professional practice — 13.5/15 weighted (90%)

| Criterion | Score | Feedback |
| --- | ---: | --- |
| Meaningful names and readable formatting | 3/5 | Most names are understandable. Improve consistency in formatting and make complex expressions easier to scan. |
| Small, focused functions | 4/5 | Rule checks and major responsibilities are split into functions and modules. Some API and rule logic could be made clearer with explicit types and smaller steps. |
| Useful README and run instructions | 5/5 | The README includes setup, run, endpoint, test, and lint instructions, along with a limitations section. Correct the API documentation URL to `/api/docs` and document active rule settings and exchange-rate details. |
| Automated tests included | 5/5 | Automated tests cover rules, API routes, validation, batch evaluation, and selected exchange-rate behavior. Expand boundary and failure-case coverage as the implementation improves. |
| Clean Git history or branch workflow | 5/5 | The review score indicates the repository history and workflow were satisfactory. A CI workflow is present for lint, formatting, and tests. |
| No secrets or sensitive data committed | 5/5 | The reviewed sample data uses synthetic identifiers, and no secrets or sensitive customer data were identified. |

**Raw score: 27/30; weighted score: 13.5/15**

## Priority improvements

1. Practice explaining the project in a short, structured walkthrough: purpose and limits, request schema, one transaction through the full data flow, rule result, and one error case.
2. Add and demonstrate edge-case coverage for timezone-aware timestamps, unusual-hours boundaries, exact amount/window thresholds, empty and invalid batches, unsupported currencies, and malformed or unavailable exchange responses.
3. Convert transaction timestamps to `Africa/Lagos` before unusual-hour evaluation, and require timezone-aware timestamps in the request model.
4. Verify the chosen exchange provider's endpoint and NGN support. Return the original and converted amounts plus rate, source, and rate timestamp; document the rounding policy and failure behavior.
5. Explain explicitly that a risk flag is an investigation signal rather than confirmation of fraud, and that in-memory history resets on restart and is not shared across workers.
6. Replace the ATM planning notes with a flowchart and matching pseudocode for the specified simulated withdrawal flow, including authentication, amount validation, balance, limits, approval/decline, recording, and the user response.
7. Run the documented checks before submission and show the successful CI result in the walkthrough.

## Recommendation

The project has a solid structural foundation and evidence of core feature work. The next step is to strengthen ownership and review communication while closing the edge-case gaps. A focused walkthrough and tests around timezones, exchange-service failures, and rule boundaries would make the implementation easier to explain and more reliable to evaluate.

**Recommended status: Revise and resubmit.**
