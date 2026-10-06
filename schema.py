"""Schemas for historical/live model validation."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class BetRecord:
    event_id: str
    market: str
    model_version: str
    decision_timestamp: str
    raw_probability: float
    calibrated_probability: float
    conservative_probability: float
    offered_american_odds: float
    outcome: int
    closing_american_odds: float | None = None
    promoted_american_odds: float | None = None
    confidence_score: float | None = None
    data_quality_flag: str | None = None
