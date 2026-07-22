# Implementação de Links Dinâmicos por Módulo

Crie uma estrutura escalável para centralizar os links de **11 módulos**, cada um contendo até **4 aulas**.

## 1. Estrutura de arquivos

```text
assets/
├── data/
│   ├── avisos.json
│   └── modulos/
│       ├── index.json
│       ├── modulo-01.json
│       ├── modulo-02.json
│       └── ... modulo-11.json
├── js/
│   ├── services/
│   │   └── module-data-service.js
│   └── pages/
│       └── module-page.js
└── README.md

docs/
├── MODULE_DATA_CONTRACT.md
└── MODULE_DATA_SERVICE.md
```

Não criar um único `links.json` global. Cada módulo deve possuir seu próprio arquivo para evitar crescimento excessivo, conflitos de edição e carregamento desnecessário.

## 2. Índice dos módulos

Arquivo: `assets/data/modulos/index.json`

```json
{
  "version": 1,
  "modules": [
    {
      "id": "modulo-01",
      "number": 1,
      "title": "Título do módulo",
      "dataFile": "modulo-01.json",
      "active": true
    }
  ]
}
```

Replicar até o módulo 11.

## 3. Contrato de cada módulo

Arquivo: `assets/data/modulos/modulo-01.json`

```json
{
  "version": 1,
  "id": "modulo-01",
  "number": 1,
  "title": "Título do módulo",
  "lessons": [
    {
      "id": "aula-01",
      "number": 1,
      "title": "Título da aula",
      "date": "2026-08-04",
      "status": "scheduled",
      "links": {
        "teams": null,
        "youtubeLive": null,
        "youtubeRecorded": null
      },
      "materials": {
        "professor": [
          {
            "id": "slides-aula-01",
            "type": "slides",
            "title": "Slides da aula",
            "url": "https://...",
            "available": true
          }
        ],
        "replacementCourses": [
          {
            "id": "curso-nivelamento",
            "title": "Curso de nivelamento",
            "url": "https://...",
            "available": true
          }
        ]
      }
    }
  ]
}
```

## 4. Regras obrigatórias

* `lessons` deve possuir no máximo 4 itens.
* Usar IDs estáveis: `modulo-01`, `aula-01`, `slides-aula-01`.
* Usar datas no formato `YYYY-MM-DD`.
* Links ainda indisponíveis devem receber `null`.
* Materiais devem ser arrays, não objetos com chaves arbitrárias.
* Cada recurso deve possuir `id`, `title`, `url` e `available`.
* Valores permitidos para `status`:

  * `scheduled`
  * `live`
  * `completed`
  * `cancelled`
* Não inserir URLs diretamente nos arquivos HTML.
* Não duplicar dados de módulos dentro de `avisos.json`.

## 5. Serviço JavaScript

Arquivo: `assets/js/services/module-data-service.js`

Implementar:

```javascript
const moduleCache = new Map();

export async function getModuleIndex() {}

export async function getModuleData(moduleId) {}

export async function getLessonData(moduleId, lessonId) {}

export async function getLessonLink(moduleId, lessonId, linkType) {}

export function clearModuleCache(moduleId = null) {}
```

### Comportamento

* `getModuleIndex()` carrega `assets/data/modulos/index.json`.
* `getModuleData("modulo-01")` localiza o módulo no índice e carrega seu arquivo.
* `getLessonData()` retorna uma aula específica.
* `getLessonLink()` aceita:

  * `teams`
  * `youtubeLive`
  * `youtubeRecorded`
* Utilizar `Map` para impedir múltiplos `fetch` do mesmo módulo.
* Verificar `response.ok`.
* Em caso de erro, lançar `Error` com contexto.
* Não retornar silenciosamente `null` para falhas de carregamento.
* Construir URLs com base em `import.meta.url`, evitando caminhos relativos dependentes da página atual.

Exemplo:

```javascript
const DATA_DIRECTORY = new URL('../../data/modulos/', import.meta.url);
```

## 6. Integração com as páginas

Em cada arquivo `modulos/modulo-N.html`, adicionar:

```html
<body data-module-id="modulo-01">
```

Carregar o script como módulo:

```html
<script type="module" src="../assets/js/pages/module-page.js"></script>
```

O arquivo `module-page.js` deve:

1. Ler `document.body.dataset.moduleId`.
2. Buscar os dados com `getModuleData()`.
3. Preencher elementos identificados por atributos `data-*`.

Exemplos:

```html
<a data-lesson="aula-01" data-link="teams">Entrar no Teams</a>

<a data-lesson="aula-01" data-link="youtubeRecorded">
  Assistir gravação
</a>

<div data-materials="aula-01"></div>
```

Links com valor `null` ou `available: false` devem permanecer ocultos ou desabilitados.

## 7. Documentação

Criar `docs/MODULE_DATA_CONTRACT.md` contendo:

* estrutura do `index.json`;
* estrutura dos arquivos de módulo;
* campos obrigatórios;
* valores permitidos;
* regras para IDs, datas, links e materiais;
* exemplo completo de um módulo.

Criar `docs/MODULE_DATA_SERVICE.md` contendo:

* funções exportadas;
* parâmetros e retornos;
* exemplos de importação;
* funcionamento do cache;
* tratamento de erros;
* integração com `module-page.js`.

## 8. Separação de responsabilidades

* `avisos.json`: somente avisos e comunicados.
* `index.json`: catálogo resumido dos módulos.
* `modulo-N.json`: aulas, links e materiais do módulo.
* `module-data-service.js`: leitura e acesso aos dados.
* `module-page.js`: atualização do DOM.
* HTML: apenas estrutura e atributos `data-*`.
