NOTICE_TYPES: tuple[str, ...] = (
    "confirmacao",
    "ao_vivo",
    "alteracao",
    "alerta",
    "material",
    "encerrado",
)

LINK_TYPES: tuple[str, ...] = ("teams", "youtubeLive", "youtubeRecorded")

LINK_TYPE_LABELS: dict[str, str] = {
    "teams": "Teams",
    "youtubeLive": "YouTube (ao vivo)",
    "youtubeRecorded": "YouTube (gravação)",
}

LINK_SOURCE_NONE = "none"
LINK_SOURCE_LESSON = "lesson"
LINK_SOURCE_STATIC = "static"
LINK_SOURCE_LIVE = "live"
LINK_SOURCE_LEGACY = "legacy"

LINK_SOURCE_LABELS: dict[str, str] = {
    LINK_SOURCE_NONE: "Sem link",
    LINK_SOURCE_LESSON: "Referência de aula",
    LINK_SOURCE_STATIC: "Link estático",
    LINK_SOURCE_LIVE: "Ao vivo avulso (Teams + YouTube)",
    LINK_SOURCE_LEGACY: "URL legada",
}

DATE_OFFSET_OPTIONS: tuple[str, ...] = ("-05:00", "-04:00", "-03:00", "-02:00", "+00:00")
DEFAULT_DATE_OFFSET = "-03:00"

DEFAULT_TEXTO_LINK = "Acessar"

TIMEZONE_NAME = "America/Sao_Paulo"

DATE_DISPLAY_FORMAT = "%d/%m/%Y, %H:%M"

NOTICE_REQUIRED_FIELDS: tuple[str, ...] = (
    "id",
    "titulo",
    "mensagem",
    "tipo",
    "dataPublicacao",
    "ativo",
)

LIST_FILTERS: tuple[str, ...] = (
    "Todos",
    "Ativos",
    "Histórico",
    "Aulas",
    "Informativos",
    "Com link",
    "Sem link",
    "Legados",
)

AVISOS_ID_FORBIDDEN_CHARS = " \t\n"

__all__ = [
    "NOTICE_TYPES",
    "LINK_TYPES",
    "LINK_TYPE_LABELS",
    "LINK_SOURCE_NONE",
    "LINK_SOURCE_LESSON",
    "LINK_SOURCE_STATIC",
    "LINK_SOURCE_LIVE",
    "LINK_SOURCE_LEGACY",
    "LINK_SOURCE_LABELS",
    "DEFAULT_TEXTO_LINK",
    "TIMEZONE_NAME",
    "DATE_DISPLAY_FORMAT",
    "NOTICE_REQUIRED_FIELDS",
    "LIST_FILTERS",
    "AVISOS_ID_FORBIDDEN_CHARS",
    "DATE_OFFSET_OPTIONS",
    "DEFAULT_DATE_OFFSET",
]
