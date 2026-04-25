from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class MappingEntry:
    source: str
    kind: str
    status: str
    target: str | None = None
    candidates: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AnalysisSelection:
    label: str
    files: list[str]
    diff_text: str


@dataclass
class FollowupItem:
    title: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)
