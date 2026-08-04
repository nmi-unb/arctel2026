# Notice Editor (FASE 1 + FASE 2)

Aplicação local em Python/Flet para administrar os avisos exibidos pelo
componente `notice-board.js` do site e os dados de módulos/aulas usados por
`module-data-service.js`, sem editar diretamente o front-end.

Esta ferramenta é privada, fica em `.notice_editor/` (fora do deploy do
site — diretórios iniciados por `.` não participam da publicação) e **não
executa build, publicação ou deploy**.

## Escopo da FASE 1

A aplicação:

- edita `assets/data/avisos.json` (criar, editar, duplicar, desativar,
  reativar, excluir, mover, ordenar);
- consulta `assets/data/modulos/index.json` e `assets/data/modulos/modulo-N.json`
  para oferecer seleção assistida de módulo, aula e tipo de link, e para
  verificar se o link correspondente existe;
- valida o contrato de dados descrito em `.docs/NOTICE_LINK_INTEGRATION.md`;
- ajuda a diagnosticar e migrar avisos com o campo legado `url`.

## Escopo da FASE 2

A área **"Módulos e aulas"** (alternável pelo seletor no topo da janela)
permite editar `assets/data/modulos/modulo-N.json`:

- selecionar um módulo, ver número (somente leitura) e editar o título;
- listar, selecionar, criar, duplicar, editar, remover, mover e ordenar aulas;
- editar `dataInicio`/`dataFim` (mesmo componente data/hora/fuso da FASE 1),
  `links` (`teams`/`youtubeLive`/`youtubeRecorded`) e `materials`
  (`professor`/`replacementCourses`, cada item com `title`/`url`/`available`);
- analisar o impacto de remover ou renumerar uma aula sobre os avisos que a
  referenciam, antes de aplicar a mudança;
- diagnosticar inconsistências entre `index.json`, os arquivos de módulo e
  os avisos ("Diagnóstico de módulos").

A remoção do suporte a `url` legado em `notice-board.js` continua **fora do
escopo** desta aplicação (ver seção "URLs legadas" abaixo).

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

## Limitações conhecidas da FASE 2

- `assets/data/modulos/index.json` não tem formulário próprio: apenas o
  campo `title` é sincronizado automaticamente com o `titulo` do módulo, no
  momento de "Salvar módulo" (ver política abaixo). `number`/`id`/`dataFile`
  não são editáveis nesta fase.
- Renumerar uma aula que já tenha avisos associados oferece a opção de
  atualizar o `lessonId` desses avisos em memória, mas isso **não salva
  `avisos.json` automaticamente** — é preciso salvar avisos e módulo
  separadamente, e o app pode ficar temporariamente inconsistente em disco
  entre um salvamento e outro.
- Remover uma aula referenciada por avisos nunca altera `avisos.json`
  silenciosamente: sempre pergunta se deve manter os avisos "inválidos"
  (apontando para uma aula inexistente) ou desativá-los.
- Não há suporte a renumerar/mover módulos inteiros, nem a criar ou excluir
  arquivos `modulo-N.json` — apenas editar o conteúdo de um módulo existente.

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
assets/data/modulos/modulo-1.json
...
assets/data/modulos/modulo-11.json
assets/data/modulos/index.json   (apenas o campo "title", ver política abaixo)
```

- `avisos.json` só é gravado após **Salvar arquivo**; todas as demais ações
  da área "Avisos" (Aplicar, Duplicar, Desativar, Mover, Ordenar, Excluir)
  alteram apenas o estado em memória.
- Cada `modulo-N.json` só é gravado após **Salvar módulo** (na área
  "Módulos e aulas"); criar/editar/duplicar/remover/mover/ordenar aulas e
  editar o título do módulo alteram apenas o estado em memória até então.
- **Salvar avisos nunca salva módulos, e salvar um módulo nunca salva
  avisos** — são ações independentes, cada uma com seu próprio indicador de
  "alterações não salvas".

### Política de `index.json`

`module-data-service.js` só lê `id` e `dataFile` de cada entrada do índice —
nunca `title`/`number`. Mesmo assim, para não deixar o índice desatualizado
para humanos/ferramentas futuras, o editor sincroniza automaticamente e de
forma restrita: ao **salvar um módulo**, se o `titulo` mudou, o campo
`title` da entrada correspondente em `index.json` é atualizado junto (a
confirmação de salvamento não precisa listar os dois arquivos porque o
`index.json` não tem formulário próprio — é um efeito colateral direto e
único do "Salvar módulo"). `number`, `id` e `dataFile` nunca são escritos
pelo editor.

## Arquivos consultados (leitura auxiliar)

```text
.docs/NOTICE_LINK_INTEGRATION.md
```

Usado para validar o contrato de referência de aula/link ao editar avisos.

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
│   ├── app_state.py               # AppState — avisos (FASE 1)
│   ├── services/
│   │   ├── dataStructure/
│   │   │   ├── notice.py
│   │   │   ├── module.py          # Module, ModuleSummary
│   │   │   ├── lesson.py          # Lesson (+materials, +extra_fields)
│   │   │   ├── LessonLinks.py
│   │   │   └── lesson_materials.py  # LessonMaterialItem, LessonMaterials
│   │   ├── generic/
│   │   │   ├── paths/             # root.py, target.py (pathlib)
│   │   │   ├── values/            # constants.py
│   │   │   └── file_fingerprint.py  # FileFingerprint compartilhado
│   │   ├── notice_repository.py   # ler/gravar avisos.json
│   │   ├── module_repository.py   # ler/gravar modulo-N.json, sync de index.json
│   │   ├── module_state.py        # ModuleState — módulos/aulas (FASE 2)
│   │   ├── reference_service.py   # avisos ↔ módulos/aulas, impacto de remoção/renumeração
│   │   ├── validation_service.py
│   │   └── migration_service.py
│   └── views/
│       ├── main_view.py           # navegação Avisos / Módulos e aulas
│       ├── form_widgets.py        # DateTimeInput, info_row (compartilhado)
│       ├── notice_list.py
│       ├── notice_form.py
│       ├── notice_preview.py
│       ├── confirmation_dialog.py
│       ├── diagnostics_view.py    # diagnóstico de URLs legadas
│       ├── module_view.py         # orquestra a área "Módulos e aulas"
│       ├── module_list.py
│       ├── module_form.py
│       ├── lesson_list.py
│       ├── lesson_form.py
│       ├── lesson_preview.py
│       └── module_diagnostics_view.py
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

## Roteiro de teste manual — FASE 2

1. Clique no seletor "Módulos e aulas" no topo da janela.
2. Selecione um módulo na coluna esquerda — número (somente leitura) e
   título devem aparecer no meio, e as aulas na lista abaixo.
3. Edite o título do módulo — o indicador "Módulo N: alterações não salvas"
   deve aparecer imediatamente.
4. Selecione uma aula — resumo (à direita, topo) e formulário (à direita,
   embaixo) devem preencher com os dados reais.
5. Clique em **Aula** (criar) — deve sugerir o próximo número disponível e
   título "Aula N"; edite e clique em **Aplicar aula**.
6. Selecione uma aula existente, clique em **Duplicar** — confirme que a
   cópia preserva materiais mas limpa datas e links (comportamento
   recomendado adotado nesta fase).
7. Use as setas para mover uma aula e os botões "Ordenar por número"/
   "Ordenar por data" — cada ordenação deve pedir confirmação antes de
   substituir a ordem física do array.
8. Escolha uma aula referenciada por algum aviso (ex.: módulo 1, aula 1) e
   clique em **Remover** — deve listar os avisos afetados e oferecer
   Cancelar / manter avisos inválidos (com confirmação extra) / desativar
   avisos.
9. Em "Alterar número..." de uma aula referenciada por avisos, informe um
   novo número — deve listar os avisos afetados e oferecer Cancelar /
   alterar só a aula / alterar a aula e atualizar os avisos em memória.
10. Clique em **Salvar módulo** — deve aparecer a confirmação recomendando
    commit; confirme e verifique que `assets/data/modulos/modulo-N.json`
    (e `index.json`, se o título mudou) foram atualizados, e que o
    indicador de alterações não salvas some.
11. Edite o arquivo do módulo por fora do editor, tente salvar de novo —
    deve aparecer o aviso de alteração externa com as opções de recarregar
    ou sobrescrever.
12. Abra **Diagnóstico de módulos** — deve listar módulos/aulas inválidos
    (se houver) e avisos com referência quebrada, sem alterar nada.
13. Volte para "Avisos" e confirme que a lista, formulário e diagnóstico de
    URLs legadas continuam funcionando normalmente (a edição de módulos não
    interfere na FASE 1).

## Itens reservados / não implementados nesta fase

- Renumerar ou excluir módulos inteiros, e criar novos arquivos
  `modulo-N.json` — fora do escopo da FASE 2.
- Atualizar automaticamente os avisos ao remover uma aula (só é oferecido
  desativar ou manter inválidos; redirecionar para outra aula não foi
  implementado).
- Remoção do suporte a `url` legado em `notice-board.js`, após migração
  completa dos registros — tratada como subfase final e independente,
  pendente de autorização explícita do usuário.
