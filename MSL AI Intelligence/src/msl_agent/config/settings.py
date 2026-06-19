"""Runtime settings for the MSL Agent proof of concept.

The module intentionally keeps configuration small. Real enterprise deployment
settings should be added only when the corresponding integration is approved.
"""

from __future__ import annotations

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class AgentSettings:
    """Basic runtime settings loaded from environment variables."""

    environment: str = "local"
    data_cutoff: str = "2026-06-19"
    default_indication: str = "NSCLC"

    @classmethod
    def from_env(cls) -> "AgentSettings":
        """Create settings from environment variables."""

        return cls(
            environment=getenv("MSL_AGENT_ENV", "local"),
            data_cutoff=getenv("MSL_AGENT_DATA_CUTOFF", "2026-06-19"),
            default_indication=getenv("MSL_AGENT_DEFAULT_INDICATION", "NSCLC"),
        )
