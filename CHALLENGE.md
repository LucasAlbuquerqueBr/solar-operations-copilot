# Solar Operations Copilot

## Simulated sponsor brief

You are building for a hypothetical US solar operations team. The team has limited engineering time and wants to recover potentially avoidable production losses from an existing California solar installation.

Its monitoring tools show production, but do not reliably explain which deviations deserve attention. A cloudy day, missing sensor data, an inverter issue, and a change in site conditions can all produce misleading alerts.

**Your challenge: turn historical telemetry into an evidence-backed investigation queue that an asset manager can use.** Show expected versus measured generation, identify suspicious intervals or inverters, estimate the size of the opportunity, and recommend the next diagnostic action.

Your prototype must distinguish observations, model estimates, hypotheses, and business assumptions. It must be useful even when the data cannot establish a root cause.

## Real asset; simulated business scenario

- Asset: PVDAQ system 2107, Farm Solar Array, Arbuckle, California, United States.
- Nameplate DC capacity: 893 kW. This is not the same as AC export capacity.
- Configuration: fixed ground mount, nominal tilt 25 degrees and azimuth 180 degrees in the source metadata.
- Inputs: inverter electrical readings, irradiance, weather, and revenue-meter AC power.
- User: hypothetical operations manager, reviewing the site each morning.
- Decision: which equipment or time period warrants investigation, what evidence supports it, and what should the operator check next?

The data is historical. The exercise does not represent the site's current condition or demonstrate that its owner experienced any particular failure.

## Scope and time budget

Suggested practice budget: **16 focused working hours over two days**, plus a five-minute pitch. This is a preparation schedule, not the official event timetable.

Core product: retrospective performance monitoring and decision support. Forecasting is an optional extension. No battery, tariff, maintenance, curtailment, or fault-label dataset is supplied; avoid promising conclusions that require those inputs.

## Task 1 — Establish whether the data can be trusted

Deliver a short audit and a reproducible preparation pipeline.

- Identify actual start/end dates, sampling intervals, units, missing cells, missing timestamps, and physically implausible values.
- Resolve how five-minute and fifteen-minute streams will be aligned. Document bin boundaries, interval labels, and sample coverage.
- Investigate local timestamps and daylight-saving transitions. Preserve uncertain times or exclude them with counts; do not silently invent UTC offsets.
- Reconcile metadata dates against the actual file coverage.
- Preserve raw data. Record every conversion, exclusion, and imputation.
- Compare the sum of inverter AC power against the site meter on matched intervals; explain possible discrepancies without assuming either is ground truth in every circumstance.

Acceptance: someone else can reproduce your analysis table and understand how many records were retained and why. Missing data must remain distinguishable from zero production.

## Task 2 — Estimate expected production

Create an interpretable baseline, then evaluate whether a more capable model improves on it.

For the core performance model, estimate site AC power using contemporaneous irradiance and weather, plus justified calendar features. This is conditional performance estimation, not a future weather forecast.

- Baseline suggestion: a simple irradiance-to-power model calibrated only on training data.
- Alternative: a nonlinear regression model with temperature and calendar features.
- Do not use same-interval inverter power, site-meter power, or transformations of the target as input to a model claimed to predict expected site power from environmental conditions. Use electrical channels separately for diagnosis.
- Explain how unhealthy training periods may bias your expected-production estimate downward. An empirical prediction is not automatically a healthy-system counterfactual.

Use this fixed chronological split after preparation:

| Split | Local calendar dates | Purpose |
|---|---|---|
| Training | 2018-01-01 through 2020-12-31 | Fit models and preprocessing |
| Validation | 2021-01-01 through 2021-12-31 | Select model, thresholds, and features |
| Final test | 2022-01-01 through 2022-12-31 | Evaluate once after choices are frozen |
| Stress test | 2023-01-01 through 2023-10-31 | Examine later behavior and incomplete coverage |

2017 is available for onboarding and historical context. Do not use it to bypass the fixed evaluation design. Do not randomly split adjacent time-series rows. Fit scalers, imputation parameters, reference curves, and thresholds only on permitted development data.

Report MAE and RMSE in kW, both overall and for a declared daylight subset, such as observed POA irradiance above 50 W/m². That cutoff is an exercise convention, not an official site standard. Report sample counts and coverage with every score. Compare models on exactly the same evaluable rows. Avoid relying on percentage error near zero output.

Acceptance: a reproducible comparison with the baseline, honest held-out results, and examples of where the model is unreliable. There is no requirement to beat the baseline at all costs.

## Task 3 — Build an investigation queue

Use the performance residuals and inverter comparisons to surface sustained deviations. Aggregate adjacent alerts into events so the operator does not receive hundreds of duplicate notifications.

For each event, show:

- Start/end time, affected inverter or site, and data completeness.
- Expected and observed power, duration, and estimated energy shortfall.
- Evidence for the alert, an uncertainty statement, and an alternative explanation.
- A suggested next check: sensor validation, inverter-log review, site inspection, comparison with peers, or another justified action.

Missing maintenance logs mean you cannot certify a hardware fault, cleaning requirement, or soiling cause. There are no verified fault labels in this package, so do not report real-world fault-detection accuracy, precision, recall, or F1 as if labels existed.

Evaluate at least five candidate events and five apparently normal comparison windows. If fewer credible events exist, report that finding rather than manufacturing failures. Examine alert volume and sensitivity to threshold changes. Optional injected faults must live in separate derived files and be explicitly labeled synthetic; evaluate them separately from real observations.

## Task 4 — Translate evidence into a decision

Rank investigation opportunities using estimated energy, uncertainty, and intervention cost. Use these **invented practice assumptions**, supplied in `templates/scenario_assumptions.csv`:

- Energy value: $0.08, $0.12, and $0.18 per kWh for low/base/high scenarios.
- Investigation visit: $250 per visit.
- Recoverable share of the estimated shortfall: 25%, 50%, and 75%.

For valid, complete fifteen-minute average-power intervals:

`estimated shortfall kWh = max(expected kW - observed kW, 0) × 0.25`

`scenario net value = shortfall kWh × recoverable share × energy value - visit cost`

This positive-residual sum can overstate losses because model noise contributes to it. Aggregate sustained events, inspect model bias, and discuss uncertainty. Never extrapolate across missing hours as though they were measured. Historical shortfall is not proof of future recoverable revenue; explain any recurrence assumption used to recommend a visit. Do not double-count site and inverter losses.

Do not claim avoided CO₂ without an identified emissions factor and explicit method. A carbon calculation is an optional extension requiring additional sourced inputs.

Acceptance: the user can see why an investigation might or might not be worthwhile under different assumptions.

## Task 5 — Demonstrate a usable product

Build a small interactive app, dashboard, or reproducible notebook with an operator-facing summary. Your choice of stack is unrestricted.

Required views:

1. Site overview: observed generation, expected generation, coverage, and uncertainty.
2. Investigation queue: prioritized events with evidence and suggested actions.
3. Event detail: time series, related inverter behavior, and sensor context.
4. Business scenario: editable assumptions and estimated value, clearly labeled as a simulation.

A language model is optional. If used, ground explanations in computed results and source metadata. The numerical analysis must remain independently reproducible.

## Optional stretch challenges

- Predict site power one hour ahead using only measurements available at the forecast issue time. Compare with persistence and a previous-day baseline. Account for interval completion and data latency. Future measured irradiance or temperature must not be used as if it were a forecast.
- Test robustness when one sensor stream disappears.
- Estimate uncertainty intervals and check their empirical coverage.
- Explain how the product would generalize to a second site and what additional data would be required.
- Add a map using the supplied coordinates; no external map service is required for the core exercise.

## Required submission

- Reproducible preparation and modeling code, with setup instructions.
- Data-quality report and channel/unit decisions.
- Model comparison with fixed temporal splits and coverage.
- Event investigation table using the supplied schema.
- Working demo and five-minute pitch.
- One-page decision memo: customer, decision, evidence, limitations, economics, and next pilot step.

The preparation package deliberately contains no trained solution or claimed failure ground truth.

## Simulated judging rubric — 100 points

| Criterion | Points | Evidence |
|---|---:|---|
| Data integrity and reproducibility | 25 | Units, timestamps, coverage, joins, rerunnable pipeline |
| Modeling and evaluation | 20 | Baseline, chronological evaluation, leakage control, uncertainty |
| Investigation quality | 20 | Useful events, supporting evidence, alternative explanations |
| Business and environmental reasoning | 15 | Explicit assumptions, realistic value calculation, no unsupported impact claims |
| Product and communication | 20 | Clear workflow, working demo, concise pitch, credible next step |

No points are awarded for claiming a specific fault without evidence. A simpler reliable model can score higher than a complex model with leakage.

## Suggested working schedule

Day 1: 2 hours for data understanding, 3 hours for preparation and baseline, 3 hours for modeling and event investigation.

Day 2: 3 hours for the prototype, 2 hours for economic scenarios, 2 hours for testing and reproducibility, 1 hour for the pitch.

Pitch sequence: customer problem → real data → live workflow → held-out evidence → potential value and limitations → proposed pilot.
