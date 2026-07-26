# Notice Editor (MVP 1.0 — FASE 1)

Aplicação local em Python/Flet para administrar os avisos exibidos pelo
componente `notice-board.js` do site, sem editar diretamente o front-end.

Esta ferramenta é privada, fica em `.notice_editor/` (fora do deploy do
site — diretórios iniciados por `.` não participam da publicação) e **não
executa build, publicação ou deploy**.

## Escopo da FASE 1

A aplicação:

- edita `assets/data/avisos.json` (criar, editar, duplicar, desativar,
  reativar, excluir, mover, ordenar);
- consulta `assets/data/modulos/index.json` e `assets/data/modulos/modulo-N.json`
  em modo **somente leitura**, para oferecer seleção assistida de módulo,
  aula e tipo de link, e para verificar se o link correspondente existe;
- valida o contrato de dados descrito em `.docs/NOTICE_LINK_INTEGRATION.md`;
- ajuda a diagnosticar e migrar avisos com o campo legado `url`.

A edição dos dados dos módulos (`modulo-N.json`) fica reservada para a
**FASE 2**.

## Limitações conhecidas da FASE 1

- Não há confirmação nativa de fechamento de janela do sistema operacional
  (o Flet desta versão não expõe esse hook de forma estável); use sempre
  "Salvar arquivo" antes de fechar o aplicativo se houver alterações
  pendentes.
- Não há backup automático — o projeto já é versionado com Git; recomenda-se
  commitar antes de salvar (o próprio editor lembra disso na confirmação de
  salvamento).
- Não há merge automático quando o arquivo é alterado externamente; o editor
  apenas detecta a alteração e pergunta se deseja recarregar ou sobrescrever.
- Datas são digitadas em texto (ISO 8601 com offset), sem seletor de
  calendário — a validação impede salvar datas malformadas.

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) instalado.
- Python 3.10+ (o `uv sync` resolve/baixa um interpretador compatível
  automaticamente, se necessário).

Todo o gerenciamento de dependências e execução usa **UV**. Não use `pip
install`, `python -m pip`, `poetry`, `pipenv` ou `conda` diretamente neste
diretório.

## Comandos

```bash
cd .notice_editor
uv sync
uv run flet run src/main.py
```

## Arquivos que o editor altera

```text
assets/data/avisos.json
```

Só é gravado após clicar em **Salvar arquivo** e confirmar o aviso de
sobrescrita — todas as demais ações (Aplicar, Duplicar, Desativar, Mover,
Ordenar, Excluir) alteram apenas o estado em memória.

## Arquivos consultados em modo somente leitura

```text
assets/data/modulos/index.json
assets/data/modulos/modulo-1.json
...
assets/data/modulos/modulo-11.json
```

Usados para listar módulos/aulas, mostrar título/datas e verificar se o link
(`teams` / `youtubeLive` / `youtubeRecorded`) de uma aula já foi definido. O
editor nunca grava alterações nesses arquivos.

## Ausência de deploy

Não existe nenhuma ação "Publicar", "Deploy" ou "Git push" nesta aplicação.
O deploy do site continua sendo feito pelas ferramentas externas já
existentes no repositório.

## URLs legadas (campo `url`)

Avisos antigos podem conter um campo `url` com a URL direta da aula (formato
anterior à integração com `module-data-service.js`). O editor:

- identifica esses registros na tela de diagnóstico ("Diagnóstico de URLs
  legadas");
- sugere automaticamente uma referência de aula (`moduleId`/`lessonId`/
  `linkType`) quando a URL coincide com um link já cadastrado em algum
  `modulo-N.json`;
- permite migrar manualmente para referência de aula ou para `staticLink`;
- não cria novos avisos com `url` — essa opção só fica disponível ao editar
  um aviso que já possui `url` preenchido.

A remoção do suporte a `url` em `notice-board.js` só deve ocorrer depois que
todos os registros forem migrados, e é uma tarefa separada desta aplicação.

## Estrutura principal

```text
.notice_editor/
├── README.md
├── pyproject.toml
├── src/
│   ├── main.py
│   ├── app_state.py
│   ├── services/
│   │   ├── dataStructure/        # Notice, Module, Lesson, LessonLinks
│   │   ├── generic/
│   │   │   ├── paths/            # root.py, target.py (pathlib)
│   │   │   └── values/           # constants.py
│   │   ├── notice_repository.py  # ler/gravar avisos.json
│   │   ├── module_repository.py  # ler index.json / modulo-N.json (RO)
│   │   ├── validation_service.py
│   │   └── migration_service.py
│   └── views/
│       ├── main_view.py
│       ├── notice_list.py
│       ├── notice_form.py
│       ├── notice_preview.py
│       ├── confirmation_dialog.py
│       └── diagnostics_view.py
└── storage/
    ├── data/
    └── temp/
```

`storage/` está reservado para uso futuro (nenhum arquivo de estado é
gravado ali nesta fase).

## Roteiro de teste manual

1. `cd .notice_editor && uv sync && uv run flet run src/main.py`.
2. A lista deve carregar os avisos reais de `assets/data/avisos.json`
   (31 registros, no momento em que este README foi escrito).
3. Clique em um aviso de aula (ex.: "Aula do Módulo 1 — Parte 1
   programada") → **Editar**. Confirme que o formulário preenche
   módulo/aula/tipo de link e que a pré-visualização mostra "Link
   disponível.".
4. Troque a fonte do link para "Link estático"; confirme que aparece o
   aviso de perda de dados antes de limpar os campos de módulo/aula.
5. Clique em **Cancelar edição** sem aplicar — deve pedir confirmação
   (há alterações não aplicadas).
6. Clique em **Novo aviso**, preencha id/titulo/mensagem/tipo/
   dataPublicacao e clique em **Aplicar** — deve aparecer na lista com
   indicador "alterações não salvas".
7. Use **Duplicar**, **Desativar/Reativar**, **Mover para cima/baixo** em
   um registro e confirme que a lista reflete as mudanças.
8. Use **Ordenar por publicação** e **Ordenar por prioridade** — cada uma
   deve pedir confirmação antes de reordenar.
9. Tente **Excluir definitivamente** um aviso — deve pedir confirmação
   explícita.
10. Abra **Diagnóstico de URLs legadas** — com o arquivo original não deve
    haver registros legados; para testar a migração, edite manualmente um
    aviso de teste com `"url": "<link já existente em algum modulo-N.json>"`
    e recarregue.
11. Clique em **Salvar arquivo** — deve aparecer a confirmação recomendando
    commit. Confirme e verifique que `assets/data/avisos.json` foi
    atualizado e que o indicador "alterações não salvas" some.
12. Edite `assets/data/avisos.json` por fora do editor (outro programa),
    volte ao editor, altere algo e tente salvar — deve aparecer o aviso de
    alteração externa com as opções de recarregar ou sobrescrever.
13. Feche e reabra o editor com **Recarregar** havendo alterações não
    salvas — deve pedir confirmação antes de descartar.

## Itens reservados para a FASE 2

- Edição dos arquivos `assets/data/modulos/modulo-N.json` (links, materiais,
  datas das aulas).
- Remoção do suporte a `url` legado em `notice-board.js`, após migração
  completa dos registros.
