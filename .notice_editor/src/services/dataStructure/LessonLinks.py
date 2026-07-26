# Nome de arquivo mantido como LessonLinks.py (PascalCase) por pedido explícito
# do prompt de construção do MVP; não segue o snake_case usual de módulos Python.
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

_FIELD_BY_LINK_TYPE = ("teams", "youtubeLive", "youtubeRecorded")


@dataclass(frozen=True)
class LessonLinks:
    teams: Optional[str]
    youtube_live: Optional[str]
    youtube_recorded: Optional[str]

    def get(self, link_type: str) -> Optional[str]:
        if link_type not in _FIELD_BY_LINK_TYPE:
            raise ValueError(f"linkType inválido: {link_type!r}")
        return {
            "teams": self.teams,
            "youtubeLive": self.youtube_live,
            "youtubeRecorded": self.youtube_recorded,
        }[link_type]

    @classmethod
    def from_dict(cls, data: dict) -> "LessonLinks":
        return cls(
            teams=data.get("teams"),
            youtube_live=data.get("youtubeLive"),
            youtube_recorded=data.get("youtubeRecorded"),
        )


__all__ = ["LessonLinks"]
