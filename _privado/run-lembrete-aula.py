# /// script
# requires-python = ">=3.10"
# dependencies = ["pyperclip>=1.8"]
# ///
from __future__ import annotations

import re
from pathlib import Path

import pyperclip

_HTML_PATH = Path(__file__).parent.parent / "lembrete-aula.html"
_TABELA_PATH = Path(__file__).parent.parent / ".info" / "links_aulas_teams.md"

_DATAS_LINKS = {
    "11/08": "https://teams.microsoft.com/meet/232970188565064?p=cpFmv1kYWNw4W81Fqw",
    "13/08": "https://teams.microsoft.com/meet/244469534286203?p=kZoHrdSKZg9eeAY6hN",
    "18/08": "https://teams.microsoft.com/meet/270882030824432?p=kfAj7sUSjIJIT1MFqz",
    "20/08": "https://teams.microsoft.com/meet/230309599603786?p=MCOB8w1EjqjEFKOenO",
    "25/08": "https://teams.microsoft.com/meet/286222844758846?p=g7mQhQgkfQ7r5EvjEl",
    "27/08": "https://teams.microsoft.com/meet/276375285420830?p=EPNbCPvbCAp62GnzyL",
    "01/09": "https://teams.microsoft.com/meet/243604603397655?p=qJQahuXs5sfSrHZwSR",
    "03/09": "https://teams.microsoft.com/meet/2216236358191?p=eh7Cj5mdPAlnqJm4xo",
    "08/09": "https://teams.microsoft.com/meet/265717928354071?p=p2ozBgLlMeXRgPBA2p",
    "10/09": "https://teams.microsoft.com/meet/224941917665953?p=oozouSYXwhJhdLdaNJ",
    "15/09": "https://teams.microsoft.com/meet/29754870339274?p=oiNYjm4Kr5vgRFEHUC",
    "17/09": "https://teams.microsoft.com/meet/248617763073881?p=3PcsivJgHkFn1Mqcwu",
    "22/09": "https://teams.microsoft.com/meet/27404076549794?p=b7f9mnpmxi6xx27W3P",
    "24/09": "https://teams.microsoft.com/meet/236519130651261?p=pB8sSfdnKnFsHFZnwy",
    "29/09": "https://teams.microsoft.com/meet/292016512995698?p=JxeYx9YWv5r5O9hW1K",
    "01/10": "https://teams.microsoft.com/meet/246670935871693?p=ikhsMvQ5i7K0QZ8Oru",
    "06/10": "https://teams.microsoft.com/meet/261201745670347?p=rNiuV2ybaBMHSulKXg",
    "08/10": "https://teams.microsoft.com/meet/2421574592161?p=3P0OJYfQpVhBDo1kaX",
    "13/10": "https://teams.microsoft.com/meet/223337149942064?p=zVOEcB5PgMKzngK3AQ",
    "15/10": "https://teams.microsoft.com/meet/27191828360552?p=Xk019df77KNS5Wkq3z",
    "20/10": "https://teams.microsoft.com/meet/274555399737937?p=VX74MumA9uuu2F87Tg",
    "22/10": "https://teams.microsoft.com/meet/272223791649605?p=oFbvzJi1x7qJdaeEcu",
    "24/10": "https://teams.microsoft.com/meet/288516193797680?p=uiCe0XQ8NhfZoft2TP",
    "29/10": "https://teams.microsoft.com/meet/221232043114894?p=LcDFHCGHhEPfCxxTr7",
    "03/11": "https://teams.microsoft.com/meet/280486001865369?p=Zr5k738NVHJPtErVo7",
    "05/11": "https://teams.microsoft.com/meet/292607075753504?p=DiMLM78zQ62LGaonL3",
}

_EMAILS = [
    "adelaide.fahe@ager.st",
    "adjilza.pinho@ager.st",
    "ailine.conceicao@arme.cv",
    "alimato.ture@arn.gw",
    "amelia.muachilela@inacom.gov.ao",
    "ana.robalo@arme.cv",
    "ana.lima@arme.cv",
    "abilale@incm.gov.mz",
    "carine.monteiro@arme.cv",
    "cialvi.86@gmail.com",
    "elvira.diogo@inacom.gov.ao",
    "erica.santos@inacom.gov.ao",
    "eveliny.dalomba@hotmail.com",
    "genivalda.marinho@inacom.gov.ao",
    "tenangisela@arn.gw",
    "imatsinhe@incm.gov.mz",
    "jandira.sanches@arme.cv",
    "turenelly85@gmail.com",
    "judicelma.americano@inacom.gov.ao",
    "katia.joao@inacom.gov.ao",
    "leonilde.santos@arme.cv",
    "luisabernardo2023@hotmail.com",
    "maria.mendes@ager.st",
    "maria.rodrigues@inacom.gov.ao",
    "marise.lima@arme.cv",
    "mbumba.goncalves@inacom.gov.ao",
    "mmacamo@incm.gov.mz",
    "miralda.dos.santos@arn.gw",
    "preciosa.freitas@ager.st",
    "rolandatavares1@gmail.com",
    "rosalina.canjila@inacom.gov.ao",
    "samanta.carvalho@arn.gw",
    "samira.reis@arme.cv",
    "sassuncao@incm.gov.mz",
    "suzete.centeio@arme.cv",
    "tchibesakunda@incm.gov.mz",
    "valodia.tiny@ager.st",
    "vanyfernandes@gmail.com",
    "aiemwassila277@gmail.com",
    "yasmine.pereira@arn.gw",
    "zenaide.cruz@inacom.gov.ao",
    "anacs@anatel.gov.br",
    "angelab@anatel.gov.br",
    "andreiacosta@anatel.gov.br",
    "carladanielabadauy@gmail.com",
    "cibelexd@anatel.gov.br",
    "cynthia@anatel.gov.br",
    "edvanniamaryse@anatel.gov.br",
    "elainepaula@anatel.gov.br",
    "elisangela@anatel.gov.br",
    "erikaluciano@anatel.gov.br",
    "gabrielamendes@anatel.gov.br",
    "gesilea@anatel.gov.br",
    "giselle@anatel.gov.br",
    "irani@anatel.gov.br",
    "katiadutra.df@gmail.com",
    "marial@anatel.gov.br",
    "mari.pedroza@gmail.com",
    "madriane@gmail.com",
    "mfalmeida@anatel.gov.br",
    "patriciav@anatel.gov.br",
    "paula.macedo@anatel.gov.br",
    "crende72@gmail.com",
    "taisrosandra@anatel.gov.br",
    "talita.passos@anatel.gov.br",
]

_LINK_PATTERN = re.compile(r'href="https://teams\.microsoft\.com/meet/[^"]*"')
_DATA_BODY_PATTERN = re.compile(r"dia <strong>\d{2}/\d{2}</strong>")
_DATA_TITLE_PATTERN = re.compile(r"A aula do dia \d{2}/\d{2} está para começar")
_TABELA_LINHA_PATTERN = re.compile(r"^\d{2}/\d{2}$")


def _carregar_modulo_parte() -> dict[str, tuple[str, str]]:
    resultado: dict[str, tuple[str, str]] = {}
    modulo_atual = "?"
    for linha in _TABELA_PATH.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha.startswith("|"):
            continue
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        if len(celulas) < 3:
            continue
        modulo, data, parte = celulas[0], celulas[1], celulas[2]
        if modulo:
            modulo_atual = modulo
        if not _TABELA_LINHA_PATTERN.match(data):
            continue
        resultado[data] = (modulo_atual, parte)
    return resultado


def _atualizar_html(data: str, link: str) -> None:
    conteudo = _HTML_PATH.read_text(encoding="utf-8")

    conteudo, n_link = _LINK_PATTERN.subn(f'href="{link}"', conteudo)
    conteudo, n_body = _DATA_BODY_PATTERN.subn(f"dia <strong>{data}</strong>", conteudo)
    conteudo, n_title = _DATA_TITLE_PATTERN.subn(f"A aula do dia {data} está para começar", conteudo)

    if n_link == 0:
        print("  aviso: não achei o href do Teams pra substituir.")
    if n_body == 0:
        print("  aviso: não achei a data no corpo do e-mail pra substituir.")
    if n_title == 0:
        print("  aviso: não achei a data no <title> pra substituir.")

    _HTML_PATH.write_text(conteudo, encoding="utf-8")


def main() -> None:
    modulo_parte = _carregar_modulo_parte()
    lista_emails = "; ".join(_EMAILS)
    total = len(_DATAS_LINKS)

    for indice, (data_bruta, link_bruto) in enumerate(_DATAS_LINKS.items(), start=1):
        data = data_bruta.strip()
        link = link_bruto.strip()
        modulo, parte = modulo_parte.get(data, ("?", "?"))
        assunto = f"ArcTel: Módulo {modulo} {parte}"

        print(f"\n=== Aula {indice}/{total} — {data} ({assunto}) ===")

        input("[1/3] Enter para copiar a lista de e-mails (Bcc)...")
        pyperclip.copy(lista_emails)
        print(f"  {len(_EMAILS)} e-mails copiados.")

        input("[2/3] Enter para copiar o assunto...")
        pyperclip.copy(assunto)
        print(f"  assunto copiado: {assunto}")

        input("[3/3] Enter para atualizar lembrete-aula.html...")
        _atualizar_html(data, link)
        print(f"  lembrete-aula.html atualizado com a aula de {data}.")

    print(f"\nTodas as {total} aulas foram processadas.")


if __name__ == "__main__":
    main()
