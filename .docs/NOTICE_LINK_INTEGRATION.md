# Integração de `avisos.json` com os links de módulo

## Contrato atualizado — `assets/data/avisos.json`

Array de objetos. Cada aviso:

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | string | sim | identificador estável do aviso |
| `titulo` | string | sim | título exibido |
| `mensagem` | string | sim | texto do aviso (sem HTML) |
| `tipo` | string | sim | usado para o badge (`confirmacao`, `ao_vivo`, `alteracao`, `alerta`, `material`, `encerrado`) |
| `dataPublicacao` | string ISO com offset | sim | data de publicação, usada em ordenação e exibição |
| `dataInicio` / `dataFim` | string ISO com offset ou `null` | não | presença de ambos marca o aviso como "aula" (ver `pickAula` em `notice-board.js`) |
| `moduleId` | string | não | ex.: `"modulo-1"`. Junto com `lessonId`/`linkType`, resolve o link via `module-data-service.js` |
| `lessonId` | string | não | ex.: `"aula-1"` (padrão `aula-{numero}`, sem zero à esquerda) |
| `linkType` | `"teams"` \| `"youtubeLive"` \| `"youtubeRecorded"` | não | qual link da aula buscar |
| `staticLink` | string | não | link fixo que **não** pertence a uma aula (ex.: `"#modulos"`). Não passa pelo `module-data-service.js` |
| `url` | string | não, **legado** | ver seção "Formato legado" abaixo |
| `textoLink` | string | não | texto do botão/link. Padrão `"Acessar"` |
| `prioridade` | number | não | maior vence em caso de empate na exibição principal |
| `ativo` | boolean | sim | `false` move o aviso para o histórico |
| `arquivarApos` | string ISO com offset ou `null` | não | após essa data o aviso vai para o histórico |
| `exibirLinkAPartirDe` | string ISO com offset ou `null` | não | antes dessa data o botão de link fica oculto, mesmo que o link já exista |

Um aviso referencia no máximo **uma** fonte de link: `moduleId`+`lessonId`+`linkType`, **ou** `staticLink`, **ou** `url` (legado). Um aviso sem nenhum dos três é válido — é um aviso informativo sem botão.

Nenhuma URL de aula ou material é armazenada diretamente neste arquivo.

## Contrato de referência — `assets/data/modulos/modulo-1.json`

```json
{
  "modulo": 1,
  "titulo": "Impactos do Ecossistema Digital na Comunicação Social",
  "lessons": [
    {
      "numero": 1,
      "titulo": "Aula 1",
      "dataInicio": "2026-08-04T07:30:00-03:00",
      "dataFim": "2026-08-04T10:30:00-03:00",
      "links": { "teams": "https://...", "youtubeLive": null, "youtubeRecorded": null },
      "materials": { "professor": [], "replacementCourses": [] }
    }
  ]
}
```

Os demais arquivos `modulo-2.json` … `modulo-11.json` seguem o mesmo formato. `moduleId` no `avisos.json` é `"modulo-{modulo}"` (ex.: módulo `2` → `"modulo-2"`); `lessonId` é `"aula-{numero}"` (ex.: aula `1` → `"aula-1"`). Não há zero à esquerda — os nomes de arquivo (`modulo-1.json`, não `modulo-01.json`) e os `data-modulo="1"` em `modulos/*.html` já seguem esse padrão, então `moduleId`/`lessonId` foram alinhados a eles para não exigir renomear arquivos existentes.

## Integração com `module-data-service.js`

`assets/js/services/module-data-service.js` expõe:

- `getModuleIndex()` — carrega `assets/data/modulos/index.json` (catálogo dos 11 módulos).
- `getModuleData(moduleId)` — localiza o módulo no índice e carrega seu arquivo; cacheado em `Map`.
- `getLessonData(moduleId, lessonId)` — retorna a aula (`lessonId` no formato `aula-{numero}`).
- `getLessonLink(moduleId, lessonId, linkType)` — retorna a URL (ou `null`, se ainda não definida) ou lança `Error` se `moduleId`/`lessonId`/`linkType` forem inválidos.
- `clearModuleCache(moduleId = null)` — limpa o cache de um módulo específico ou de todos.

`notice-board.js` importa apenas `getLessonLink`.

## Comportamento quando o link não existe

Em `notice-board.js`, `resolveNoticeLink(aviso)`:

1. Se `aviso.url` (legado) existir, usa-o e registra aviso no console.
2. Senão, se `aviso.staticLink` existir, usa-o diretamente.
3. Senão, se `moduleId`+`lessonId`+`linkType` existirem, chama `getLessonLink(...)`.
4. Qualquer falha (aula não encontrada, `linkType` inválido, erro de rede) é capturada, registrada com `console.warn` e resolve para `null` — nunca lança para fora da função.

O resultado fica em `aviso._link`. O aviso continua visível (título, mensagem, badge, datas); apenas o botão de ação some quando `aviso._link` é `null`. Nunca é usado `href="#"` como fallback — o botão simplesmente não é criado (ver `renderLink`/`linkPodeAparecer` em `notice-board.js`).

## Como cadastrar um novo aviso

Para um aviso de aula, adicionar em `assets/data/avisos.json`:

```json
{
  "id": "aula-modulo-2-parte-3",
  "titulo": "Aula do Módulo 2 — Parte 3 programada",
  "mensagem": "...",
  "tipo": "confirmacao",
  "dataPublicacao": "2026-08-20T08:00:00-03:00",
  "dataInicio": "2026-08-21T08:00:00-03:00",
  "dataFim": "2026-08-21T10:00:00-03:00",
  "moduleId": "modulo-2",
  "lessonId": "aula-3",
  "linkType": "teams",
  "textoLink": "Entrar na aula",
  "prioridade": 3,
  "ativo": true,
  "arquivarApos": "2026-08-21T10:30:00-03:00",
  "exibirLinkAPartirDe": "2026-08-21T07:15:00-03:00"
}
```

O link em si (URL do Teams/YouTube) deve existir em `assets/data/modulos/modulo-2.json`, na aula correspondente — nunca colado diretamente no aviso.

Para um aviso informativo sem link, basta omitir `moduleId`/`lessonId`/`linkType`/`staticLink`/`url`.

## Formato legado a remover

Avisos antigos podem trazer um campo `url` com a URL direta (formato anterior a esta migração). Ele ainda funciona, mas `notice-board.js` emite `console.warn("[notice-board] URL legada encontrada no aviso ...")` a cada carregamento. Após migrar todos os avisos existentes para `moduleId`/`lessonId`/`linkType` (ou `staticLink`, quando não for um link de aula), remover:

- o campo `url` de todos os registros em `avisos.json`;
- o bloco de tratamento de `aviso.url` em `resolveNoticeLink()` (`assets/js/components/notice-board.js`).
