# /// script
# requires-python = ">=3.10"
# dependencies = ["gspread>=6.1", "google-auth>=2.29"]
# ///
from __future__ import annotations

import csv
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SHEET_ID = "1ScxjU3xgY1OEiSlhh_KWLfzMRkRTUA3N"
WORKSHEET_GID = 1456578391
CREDENTIALS_PATH = Path(__file__).parent / "credentials.json"
OUTPUT_PATH = Path(__file__).parent / "entrada" / "Lista_de_presenca-Modulos.xlsx - Lista de presença.csv"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def _load_client() -> gspread.Client:
    if not CREDENTIALS_PATH.is_file():
        raise SystemExit(
            f"Credenciais não encontradas em {CREDENTIALS_PATH}.\n\n"
            "1. Crie uma service account em https://console.cloud.google.com/iam-admin/serviceaccounts\n"
            "2. Gere uma chave JSON e salve exatamente nesse caminho.\n"
            "3. Compartilhe a planilha (botão Compartilhar) com o e-mail 'client_email' do JSON, papel Leitor."
        )
    creds = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=SCOPES)
    return gspread.authorize(creds)


def sync() -> Path:
    client = _load_client()
    spreadsheet = client.open_by_key(SHEET_ID)
    worksheet = spreadsheet.get_worksheet_by_id(WORKSHEET_GID)
    rows = worksheet.get_all_values()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerows(rows)

    return OUTPUT_PATH


if __name__ == "__main__":
    path = sync()
    print(f"Planilha sincronizada: {path}")
