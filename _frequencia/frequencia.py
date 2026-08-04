from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

_CSV_PATH = Path(__file__).parent / "entrada" / "Lista_de_presenca-Modulos.xlsx - Lista de presença.csv"
_HEADER_ROW_INDEX = 4  # linha com as datas ("4/8", "6/8", ...)
_FIRST_DATA_COLUMN = 3  # colunas 0,1,2 = número, email, nome
_FIRST_PARTICIPANT_ROW = 5

_DATE_FORMATS = ("%m/%d/%Y", "%d/%m/%Y", "%m/%d/%y", "%d/%m/%y")


def _parse_data(data: str) -> tuple[int, int]:
    data = data.strip()
    for fmt in _DATE_FORMATS:
        try:
            parsed = datetime.strptime(data, fmt)
        except ValueError:
            continue
        return parsed.day, parsed.month
    raise ValueError(f"data em formato não reconhecido: {data!r}")


def _read_rows() -> list[list[str]]:
    with _CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _find_date_column(rows: list[list[str]], day: int, month: int) -> int:
    header = rows[_HEADER_ROW_INDEX]
    target = f"{day}/{month}"
    for index, value in enumerate(header):
        if index < _FIRST_DATA_COLUMN:
            continue
        if value.strip() == target:
            return index
    raise ValueError(f"nenhuma coluna de frequência encontrada para a data {target!r}")


def _frequencia(data: str) -> list[str]:
    day, month = _parse_data(data)
    rows = _read_rows()
    column = _find_date_column(rows, day, month)

    emails: list[str] = []
    for row in rows[_FIRST_PARTICIPANT_ROW:]:
        if len(row) <= column:
            continue
        email = row[1].strip() if len(row) > 1 else ""
        if not email or "@" not in email:
            continue
        if row[column].strip().upper() == "P":
            emails.append(email)
    return emails


_LISTA_PATH = Path(__file__).parent / "saida" / "lista.md"


def _escrever_lista(data: str, emails: list[str]) -> Path:
    _LISTA_PATH.parent.mkdir(parents=True, exist_ok=True)
    linhas = [f"# Frequência — {data}", "", f"{len(emails)} presença(s):", ""]
    linhas.extend(f"- {email}" for email in emails)
    _LISTA_PATH.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return _LISTA_PATH


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("uso: python frequencia.py <data, ex: 8/4/2026>")
    resultado = _frequencia(sys.argv[1])
    caminho = _escrever_lista(sys.argv[1], resultado)
    print(f"{len(resultado)} e-mail(s) gravado(s) em {caminho}")
