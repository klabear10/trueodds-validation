# TrueOdds 2.1 Parlay Safety Layer

## Core rule

Parlay EV must use a joint probability P(A ∩ B ∩ C ...), not blindly multiply marginal probabilities unless independence is justified.

## Dependency classes

Each pair of legs should be classified as positive correlation, negative correlation, approximately independent, or uncertain/common-cause dependent. Uncertain dependence widens uncertainty rather than defaulting to zero correlation.

## Preferred framework

For three legs:

P(A ∩ B ∩ C) = P(A) × P(B | A) × P(C | A, B)

For same-game parlays, use shared-state simulation where possible. Shared factors can include pace/plays, scoring environment, game script, team efficiency, player usage, injuries/availability, weather, and garbage-time effects.

## Correlation risk score

- 0–20: little meaningful dependency
- 21–40: mild
- 41–60: material
- 61–80: strong
- 81–100: highly dependent / difficult to model

The score changes confidence and uncertainty, not whether a wager is automatically good or bad.

## Probability layers

Track raw probability, calibrated probability, and conservative probability. The conservative probability is the preferred input for strict EV decisions.

## Classification

PASS, LEAN, BET, STRONG BET, or PROMO-ONLY BET.

## Promo handling

Always report unboosted break-even probability, boosted break-even probability, raw EV, conservative EV, and promo-adjusted EV. If the base wager is unattractive but the promotion makes conservative EV positive, classify it as PROMO-ONLY BET.

## Market disagreement safeguard

Large model-vs-market discrepancies trigger review of injuries, starters, weather, stale statistics, role changes, opponent adjustment, timestamps/look-ahead leakage, market definition, and simulation assumptions.
