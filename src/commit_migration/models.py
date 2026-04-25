from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class CandidateMatch:
    path: str
    score: int
    confidence: str
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MappingEntry:
    source: str
    kind: str
    status: str
    target: str | None = None
    candidates: list[str] = field(default_factory=list)
    candidate_details: list[CandidateMatch] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["candidate_details"] = [item.to_dict() for item in self.candidate_details]
        return data


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
