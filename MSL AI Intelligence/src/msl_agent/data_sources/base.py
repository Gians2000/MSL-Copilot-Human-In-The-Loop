"""Base data-source types.

Concrete connectors should return structured source metadata and raw snippets
without converting unsupported content into clinical claims.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SourceQuery:
    """A search request sent to a literature, trial, or regulatory source."""

    query: str
    source_name: str
    filters: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievedSource:
    """A retrieved source record with enough metadata for traceability."""

    source_id: str
    title: str
    url: str
    source_type: str
    publication_date: str | None = None
    raw_excerpt: str | None = None

    # TODO: Add checksum/version metadata when real source ingestion is implemented.
