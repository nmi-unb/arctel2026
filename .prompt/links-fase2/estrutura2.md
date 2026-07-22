# Fase 2 — Integração de `avisos.json` com o repositório de links

## Objetivo

Auditar todos os arquivos relacionados ao `assets/data/avisos.json` e fazer com que os avisos utilizem referências para os links centralizados, sem URLs duplicadas ou hardcoded.

## Escopo

Inspecionar, sem alterar arquivos não relacionados:

```text
assets/data/avisos.json
assets/js/components/notice-board.js
assets/js/pages/home-page.js
assets/js/app.js
index.html
modulos/*.html
```

Também localizar qualquer outro arquivo que:

* carregue `avisos.json`;
* manipule ou renderize avisos;
* contenha URLs relacionadas às aulas ou aos materiais;
* dependa do formato atual dos avisos.

## Fonte oficial dos links

Usar como fonte única a estrutura centralizada definida na Fase 1.

Caso a Fase 1 utilize arquivos separados por módulo, não criar um novo `links.json` global. Resolver os links pelo serviço central:

```text
assets/js/services/module-data-service.js
```

## Novo contrato de `avisos.json`

Substituir URLs diretas por referências estáveis:

```json
[
  {
    "id": "aviso-01",
    "title": "Aula ao vivo",
    "message": "A aula está confirmada.",
    "moduleId": "modulo-01",
    "lessonId": "aula-01",
    "linkType": "teams",
    "buttonText": "Entrar na sala",
    "active": true
  }
]
```

Valores permitidos para `linkType`:

```text
teams
youtubeLive
youtubeRecorded
```

Não usar caminhos genéricos como `aulas.teams`, pois os links pertencem a módulos e aulas específicas.

## Integração JavaScript

Atualizar `notice-board.js` para:

1. carregar `avisos.json`;
2. identificar `moduleId`, `lessonId` e `linkType`;
3. resolver a URL com:

```javascript
getLessonLink(moduleId, lessonId, linkType);
```

4. renderizar o botão somente quando a URL existir;
5. manter o aviso visível quando o link não puder ser resolvido;
6. registrar o erro no console sem interromper a interface.

Exemplo:

```javascript
import { getLessonLink } from '../services/module-data-service.js';

async function resolveNoticeLink(notice) {
  if (!notice.moduleId || !notice.lessonId || !notice.linkType) {
    return null;
  }

  try {
    return await getLessonLink(
      notice.moduleId,
      notice.lessonId,
      notice.linkType
    );
  } catch (error) {
    console.warn(`Link não encontrado para o aviso ${notice.id}`, error);
    return null;
  }
}
```

## Regras obrigatórias

* Remover URLs de aulas e materiais do `avisos.json`.
* Não duplicar URLs já existentes nos arquivos dos módulos.
* Não usar interpolação textual como `[[LINK:...]]` nesta fase.
* Não permitir HTML arbitrário dentro das mensagens dos avisos.
* Manter IDs e nomes de campos consistentes.
* Preservar o comportamento visual atual do mural.
* Ocultar apenas o botão quando o link estiver indisponível.
* Não usar `href="#"` como fallback.
* Não quebrar avisos informativos que não possuem link.

## Compatibilidade temporária

Durante a migração, aceitar avisos antigos com campo `url`, mas emitir aviso no console:

```javascript
if (notice.url) {
  console.warn(`URL legada encontrada no aviso ${notice.id}`);
}
```

Após migrar todos os registros, remover essa compatibilidade.

## Documentação

Criar:

```text
docs/NOTICE_LINK_INTEGRATION.md
```

Documentar somente:

* contrato atualizado de `avisos.json`;
* campos obrigatórios e opcionais;
* integração com `module-data-service.js`;
* comportamento quando o link não existir;
* procedimento para cadastrar um novo aviso;
* formato legado que deverá ser removido.

## Resultado esperado

```text
avisos.json
└── conteúdo e referências

module-N.json
└── URLs oficiais

module-data-service.js
└── resolução dos links

notice-board.js
└── carregamento, resolução e renderização
```

Nenhuma URL de aula ou material deve permanecer duplicada no `avisos.json` ou no código de renderização.
