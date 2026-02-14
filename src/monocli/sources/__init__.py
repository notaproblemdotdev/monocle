"""Data sources package for monocli.

Provides source protocols and implementations for fetching data from
various platforms (GitLab, GitHub, Jira, Todoist, Linear, etc.).
"""

from monocli.sources.base import (
    APIBaseAdapter,
    CLIBaseAdapter,
    CodeReviewSource,
    PieceOfWorkSource,
    Source,
)
from monocli.sources.registry import SourceRegistry

__all__ = [
    "Source",
    "PieceOfWorkSource",
    "CodeReviewSource",
    "CLIBaseAdapter",
    "APIBaseAdapter",
    "SourceRegistry",
]
