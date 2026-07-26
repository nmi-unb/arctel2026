from __future__ import annotations

import json
from dataclasses import dataclass

from .dataStructure.notice import Notice
from .generic.paths.target import get_avisos_path


class NoticeRepositoryError(Exception):
    pass


@dataclass(frozen=True)
class FileFingerprint:
    mtime_ns: int
    size: int


def _read_fingerprint() -> FileFingerprint:
    stat = get_avisos_path().stat()
    return FileFingerprint(mtime_ns=stat.st_mtime_ns, size=stat.st_size)


def load_notices() -> tuple[list[Notice], FileFingerprint]:
    path = get_avisos_path()
    if not path.is_file():
        raise NoticeRepositoryError(f"Arquivo não encontrado: {path}")
    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise NoticeRepositoryError(f"Falha ao ler {path}: {exc}") from exc
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise NoticeRepositoryError(f"JSON malformado em {path}: {exc}") from exc
    if not isinstance(data, list):
        raise NoticeRepositoryError(f"{path} deve conter um array na raiz")
    try:
        notices = [Notice.from_dict(item) for item in data]
    except (KeyError, TypeError, ValueError) as exc:
        raise NoticeRepositoryError(f"Registro inválido em {path}: {exc}") from exc
    return notices, _read_fingerprint()


def has_changed_externally(fingerprint: FileFingerprint) -> bool:
    path = get_avisos_path()
    if not path.is_file():
        return True
    return _read_fingerprint() != fingerprint


def save_notices(notices: list[Notice]) -> FileFingerprint:
    path = get_avisos_path()
    payload = [notice.to_dict() for notice in notices]
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    try:
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise NoticeRepositoryError(f"Falha ao gravar {path}: {exc}") from exc

    try:
        reread = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise NoticeRepositoryError(
            f"Arquivo gravado, mas releitura de verificação falhou: {exc}"
        ) from exc
    if not isinstance(reread, list):
        raise NoticeRepositoryError("Releitura pós-gravação retornou conteúdo inesperado")

    return _read_fingerprint()


__all__ = [
    "NoticeRepositoryError",
    "FileFingerprint",
    "load_notices",
    "save_notices",
    "has_changed_externally",
]
