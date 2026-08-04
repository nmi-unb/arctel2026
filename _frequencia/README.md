# Frequência — Módulos

Scripts pra ler a frequência dos participantes do curso ARCTEL 2026 a partir da planilha de controle ("Lista de presença").

## Arquivos

```text
_frequencia/
├── entrada/
│   └── Lista_de_presenca-Modulos.xlsx - Lista de presença.csv   # dados locais (fonte de leitura)
├── saida/
│   └── lista.md                                                  # gerado por frequencia.py (não versionado)
├── sync_planilha.py                                              # baixa a planilha do Drive e sobrescreve o CSV em entrada/
├── frequencia.py                                                 # _frequencia(data) -> lista de e-mails presentes
└── credentials.json                                              # chave da service account (não versionado)
```

## Formato da planilha

```text
linha 1-3: em branco / título
linha 4:   módulos (M1, M1, M2, M2, M3, M3, M3, ...)
linha 5:   datas de cada coluna ("4/8", "6/8", "11/8", ...)
linha 6+:  participantes — col A = número, col B = e-mail, col C = nome,
           col D em diante = presença ("P") por data
```

Uma linha em branco separa os dois grupos de participantes (turma 1 / turma 2),
o que não afeta a leitura.

## `frequencia.py` — consultar presença

```python
from frequencia import _frequencia

_frequencia("8/4/2026")  # -> lista de e-mails com "P" na coluna 4/8
```

- Aceita a data em `M/D/Y` ou `D/M/Y` (com ou sem zero à esquerda), casando
  contra a coluna cujo cabeçalho (linha 5) seja o mesmo dia/mês.
- Lê sempre o CSV em `entrada/` **local** — não acessa a internet.
- Levanta `ValueError` se a data não bater com nenhuma coluna.

Uso via linha de comando — grava o resultado em `saida/lista.md` (cria a
pasta se não existir; sobrescreve a cada execução):

```bash
uv run _frequencia/frequencia.py "8/4/2026"
```

## `sync_planilha.py` — atualizar o CSV local com a planilha online

A planilha do Google é **privada**; não dá pra baixar sem autenticação.
O script usa uma *service account* do Google Cloud pra ler a planilha e
sobrescrever o CSV local com os dados mais recentes.

### Configuração (uma vez só)

1. Crie uma service account em
   https://console.cloud.google.com/iam-admin/serviceaccounts (qualquer
   projeto Google Cloud; não precisa ativar billing pra isso).
2. Gere uma chave em formato **JSON** pra essa service account e salve o
   arquivo exatamente como `_frequencia/credentials.json`.
3. Abra a planilha no navegador → botão **Compartilhar** → adicione o e-mail
   `client_email` que está dentro do JSON, com papel **Leitor**.

### Uso

```bash
uv run _frequencia/sync_planilha.py
```

Sobrescreve `entrada/Lista_de_presenca-Modulos.xlsx - Lista de presença.csv`
com o conteúdo atual da aba (gid `1456578391`) da planilha (cria `entrada/`
se não existir).

Sem `credentials.json`, o script apenas imprime as instruções acima e para
— não quebra nada nem apaga o CSV existente.

### Segurança

`credentials.json` dá acesso de leitura à planilha (e a qualquer outro
recurso compartilhado com essa service account). Nunca commitar esse
arquivo — já está no `.gitignore` da raiz do repositório, junto com
`_frequencia/saida/` (contém e-mails de participantes).

## Dependências

Nenhuma instalação manual necessária — os scripts declaram suas próprias
dependências (`gspread`, `google-auth`) via metadata inline (PEP 723). Rode
sempre com `uv run`, que resolve e isola as dependências automaticamente.
