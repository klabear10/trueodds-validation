# TrueOdds Validation

TrueOdds is an experimental sports-betting probability and validation framework.

## Current stage

TrueOdds 2.1 development / validation.

Immediate priorities:

- calibrated probabilities rather than raw confidence
- explicit parlay joint-probability modeling
- correlation-aware same-game parlay evaluation
- conservative uncertainty adjustments
- sportsbook break-even and EV calculations
- promotion-aware classification
- historical and out-of-sample validation

## Decision pipeline

raw probability -> calibrated probability -> uncertainty adjustment -> conservative probability -> dependency/correlation analysis -> joint probability -> sportsbook break-even probability -> raw EV -> conservative EV -> promo-adjusted EV -> BET / PROMO-ONLY BET / PASS

A positive modeled EV is not proof of a real-world edge until it survives calibration and out-of-sample testing.
