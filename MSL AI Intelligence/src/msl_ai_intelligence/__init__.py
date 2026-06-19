"""MSL AI Intelligence package."""

from .scoring import DEFAULT_WEIGHTS, priority_band, score_opportunity
from .templates import render_opportunity_brief

__all__ = [
    "DEFAULT_WEIGHTS",
    "priority_band",
    "render_opportunity_brief",
    "score_opportunity",
]

__version__ = "0.1.0"
