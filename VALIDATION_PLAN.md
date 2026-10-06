# TrueOdds Validation Plan

## No look-ahead rule

Historical predictions must use only information available at the historical decision time. No postgame statistics, final injury knowledge, retrospective depth-chart changes, or other hindsight information may leak into the model.

## Calibration

Compare predicted probability with actual frequency. Suggested buckets: 50–55%, 55–60%, 60–65%, 65–70%, 70–75%, and 75%+.

Track calibration separately by market type where sample size permits: moneyline, spread, total, passing props, rushing props, receiving props, touchdowns, and parlays.

## Proper scoring rules

Track Brier score and log loss to penalize overconfidence.

## Betting performance

For every recommendation record model version, timestamp, event, market, raw probability, calibrated probability, conservative probability, sportsbook odds at decision time, closing odds, projected EV, result, realized profit/loss, confidence score, data-quality flags, and promotion flag.

For parlays also record marginal probability per leg, dependency classification, correlation-risk score, joint probability, actual parlay payout, and whether it was +EV without promotion.

## Market benchmark

Track closing-line value (CLV). Positive CLV is not sufficient proof of profitability, but persistent negative CLV is a warning sign.

## Edge monotonicity

Larger projected edges should generally perform better over sufficiently large samples. If edge buckets are not monotonic, recalibration is likely needed.

## Out-of-sample testing

Do not judge the model on data used for fitting or calibration. Use rolling or season-based splits so validation occurs on untouched future periods.

## Shadow mode

Before production, log live recommendations prospectively and evaluate calibration, CLV and ROI after enough observations accumulate.
