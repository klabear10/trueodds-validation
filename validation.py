"""Backtesting, calibration, ROI and CLV analysis."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .calibration import brier_score, log_loss, expected_calibration_error
from .pricing import break_even_probability, american_to_decimal, expected_value
from .schema import BetRecord


@dataclass(frozen=True)
class BacktestSummary:
    n: int
    win_rate: float
    brier: float
    log_loss: float
    calibration_error: float
    roi: float
    average_projected_ev: float
    average_clv_probability_points: float | None


def realized_profit(outcome: int, american_odds: float, stake: float = 1.0) -> float:
    if outcome not in (0, 1):
        raise ValueError("outcome must be 0 or 1")
    if outcome == 0:
        return -stake
    return stake * (american_to_decimal(american_odds) - 1.0)


def classify_wager(
    conservative_probability: float,
    american_odds: float,
    *,
    boosted_american_odds: float | None = None,
    bet_threshold_pp: float = 3.0,
    strong_threshold_pp: float = 6.0,
) -> str:
    be = break_even_probability(american_odds)
    edge_pp = (conservative_probability - be) * 100.0

    boosted_edge_pp = None
    if boosted_american_odds is not None:
        boosted_be = break_even_probability(boosted_american_odds)
        boosted_edge_pp = (conservative_probability - boosted_be) * 100.0

    if boosted_edge_pp is not None and edge_pp < bet_threshold_pp <= boosted_edge_pp:
        return "PROMO-ONLY BET"
    if edge_pp >= strong_threshold_pp:
        return "STRONG BET"
    if edge_pp >= bet_threshold_pp:
        return "BET"
    if edge_pp > 0:
        return "LEAN"
    return "PASS"


def summarize_backtest(records: list[BetRecord], bins: int = 10) -> BacktestSummary:
    if not records:
        raise ValueError("records cannot be empty")

    p = np.array([r.calibrated_probability for r in records], dtype=float)
    y = np.array([r.outcome for r in records], dtype=float)

    profits = np.array([
        realized_profit(r.outcome, r.offered_american_odds) for r in records
    ], dtype=float)

    projected_ev = np.array([
        expected_value(r.conservative_probability, r.offered_american_odds)
        for r in records
    ], dtype=float)

    clvs = []
    for r in records:
        if r.closing_american_odds is not None:
            offered_be = break_even_probability(r.offered_american_odds)
            closing_be = break_even_probability(r.closing_american_odds)
            # Positive means bettor beat the closing implied probability.
            clvs.append((closing_be - offered_be) * 100.0)

    return BacktestSummary(
        n=len(records),
        win_rate=float(y.mean()),
        brier=brier_score(p, y),
        log_loss=log_loss(p, y),
        calibration_error=expected_calibration_error(p, y, bins=bins),
        roi=float(profits.mean()),
        average_projected_ev=float(projected_ev.mean()),
        average_clv_probability_points=(float(np.mean(clvs)) if clvs else None),
    )


def edge_bucket_report(records: list[BetRecord], edges=(0, 2, 4, 7, 10, float("inf"))) -> list[dict]:
    if not records:
        return []

    rows = []
    for low, high in zip(edges[:-1], edges[1:]):
        selected = []
        for r in records:
            edge_pp = (
                r.conservative_probability
                - break_even_probability(r.offered_american_odds)
            ) * 100.0
            if low <= edge_pp < high:
                selected.append((r, edge_pp))

        if not selected:
            continue

        profits = [
            realized_profit(r.outcome, r.offered_american_odds)
            for r, _ in selected
        ]
        rows.append({
            "edge_low_pp": low,
            "edge_high_pp": high,
            "n": len(selected),
            "mean_edge_pp": float(np.mean([e for _, e in selected])),
            "win_rate": float(np.mean([r.outcome for r, _ in selected])),
            "roi": float(np.mean(profits)),
        })
    return rows
