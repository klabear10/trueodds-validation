# TrueOdds 2.1 Validation Protocol

## 1. Freeze the model before testing

Do not tune on the same observations used to evaluate performance.

## 2. Prevent look-ahead leakage

Every historical feature must be timestamped or reconstructable as information that existed before the bet decision.

Examples of forbidden leakage:

- postgame statistics
- final injury knowledge unavailable at decision time
- future depth-chart changes
- closing prices used as model predictors
- statistics calculated using games after the prediction date

## 3. Split chronologically

Preferred:

1. training period
2. calibration period
3. untouched test period

A rolling walk-forward evaluation is even better.

## 4. Evaluate probability quality

Track:

- Brier score
- log loss
- expected calibration error
- calibration table / reliability curve

## 5. Evaluate betting quality

Track:

- realized ROI
- average projected conservative EV
- CLV
- edge bucket monotonicity
- performance by market type
- performance with and without promotions

## 6. Parlays

Do not multiply marginals unless independence is justified.

Use shared-state simulations. Store the binary result of every leg in every simulation, then calculate:

- empirical joint probability
- independent-product probability
- difference between the two
- pairwise phi correlations
- correlation-risk score

## 7. Production readiness

Do not call the model production-ready merely because historical ROI is positive.

Minimum evidence should include:

- acceptable calibration
- stable results over multiple time segments
- no obvious look-ahead leakage
- positive or at least non-negative CLV on recommended bets
- sensible edge monotonicity
- separate evidence for parlays versus singles
- prospective shadow-mode tracking
