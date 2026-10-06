# TrueOdds 2.1

Executable validation framework for a sports-betting probability model.

## What this version does

- converts American odds to implied break-even probabilities
- computes raw and conservative EV
- calibrates model probabilities from historical outcomes
- measures Brier score, log loss, calibration error, ROI, and CLV
- estimates joint parlay probability from shared simulation outcomes
- measures pairwise dependence between parlay legs
- applies an uncertainty haircut
- distinguishes BET, PROMO-ONLY BET, LEAN, and PASS
- supports out-of-sample validation without requiring market odds as model inputs

## Important limitation

This package is the validation/safety engine. It does **not** magically create a proven football forecasting edge by itself. A football model still needs historical pregame features and outcomes. The included logistic probability model is a trainable baseline that can consume those features once supplied.

## Layout

- `src/trueodds/pricing.py` — odds and EV math
- `src/trueodds/calibration.py` — calibration and proper scoring rules
- `src/trueodds/uncertainty.py` — conservative probability logic
- `src/trueodds/parlay.py` — joint probability / dependence analysis
- `src/trueodds/validation.py` — backtest metrics, ROI, CLV, edge buckets
- `src/trueodds/model.py` — simple trainable logistic probability model
- `src/trueodds/schema.py` — validation record schema
- `tests/` — executable tests
- `docs/VALIDATION_PLAN.md` — protocol for leakage-free testing

## Quick start

```bash
python -m pip install -e ".[dev]"
pytest
```

A positive modeled EV is not proof of a real-world edge until it survives out-of-sample calibration and live/shadow tracking.
