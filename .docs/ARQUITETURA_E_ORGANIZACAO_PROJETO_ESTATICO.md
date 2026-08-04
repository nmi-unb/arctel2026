<link rel="stylesheet" href="../.css/style.css">

# Arquitetura e organização de projeto estático

Este documento propõe uma arquitetura **estática, robusta e expansível** para uma aplicação publicada no **GitHub Pages**, construída com **HTML, CSS e JavaScript puro**.

A proposta considera que o projeto pode começar com **uma única página**, mas já nasce preparado para crescer sem exigir uma reestruturação completa no futuro.

---

## 1. Objetivo da arquitetura

A arquitetura deve permitir que o projeto comece simples, mas consiga evoluir para:

- múltiplas páginas;
- componentes reutilizáveis;
- organização visual consistente;
- separação clara entre conteúdo, estilo, comportamento e assets;
- uso de imagens, logos, favicons, ícones e ilustrações;
- documentação interna por pasta;
- futura migração para framework, build tool ou back-end, se necessário.

A ideia central é evitar uma base estreita, na qual tudo fica misturado em poucos arquivos, dificultando manutenção, colaboração e expansão.

---

## 2. Escopo genérico da aplicação

### 2.1 Tipo de aplicação

Aplicação estática hospedada no GitHub Pages, usando:

- HTML para estrutura;
- CSS para apresentação visual;
- JavaScript para comportamento e interatividade;
- arquivos estáticos para imagens, fontes, dados e documentos.

### 2.2 Premissas iniciais

- A aplicação pode começar com apenas `index.html`.
- Não haverá back-end inicialmente.
- Não haverá banco de dados inicialmente.
- Os dados podem ser mantidos em arquivos `.json`, `.js` ou diretamente no HTML, conforme o caso.
- A estrutura deve permitir crescimento gradual.
- A publicação deve funcionar diretamente no GitHub Pages.
- Os caminhos devem ser preferencialmente relativos, para evitar problemas de hospedagem.

### 2.3 Possíveis evoluções futuras

A estrutura já prevê espaço para:

- novas páginas;
- novos componentes;
- carregamento de dados externos;
- separação de módulos JavaScript;
- temas visuais;
- internacionalização;
- automações simples;
- testes manuais ou automatizados;
- documentação técnica;
- integração futura com APIs.

---

## 3. Árvore principal do projeto

```text
nome-do-projeto/
├── README.md
├── LICENSE
├── .gitignore
├── .editorconfig
├── index.html
├── 404.html
├── robots.txt
├── sitemap.xml
├── manifest.webmanifest
│
├── assets/
│   ├── README.md
│   ├── css/
│   │   ├── README.md
│   │   ├── main.css
│   │   ├── base/
│   │   │   ├── README.md
│   │   │   ├── reset.css
│   │   │   ├── variables.css
│   │   │   └── typography.css
│   │   ├── layout/
│   │   │   ├── README.md
│   │   │   ├── grid.css
│   │   │   ├── header.css
│   │   │   ├── footer.css
│   │   │   └── sections.css
│   │   ├── components/
│   │   │   ├── README.md
│   │   │   ├── buttons.css
│   │   │   ├── cards.css
│   │   │   ├── forms.css
│   │   │   ├── modals.css
│   │   │   └── navigation.css
│   │   ├── pages/
│   │   │   ├── README.md
│   │   │   └── home.css
│   │   ├── themes/
│   │   │   ├── README.md
│   │   │   ├── default.css
│   │   │   └── dark.css
│   │   └── utilities/
│   │       ├── README.md
│   │       ├── spacing.css
│   │       ├── visibility.css
│   │       └── helpers.css
│   │
│   ├── js/
│   │   ├── README.md
│   │   ├── app.js
│   │   ├── core/
│   │   │   ├── README.md
│   │   │   ├── config.js
│   │   │   ├── constants.js
│   │   │   └── state.js
│   │   ├── utils/
│   │   │   ├── README.md
│   │   │   ├── dom.js
│   │   │   ├── format.js
│   │   │   ├── storage.js
│   │   │   └── validators.js
│   │   ├── services/
│   │   │   ├── README.md
│   │   │   ├── data-service.js
│   │   │   ├── storage-service.js
│   │   │   └── navigation-service.js
│   │   ├── components/
│   │   │   ├── README.md
│   │   │   ├── card.js
│   │   │   ├── navbar.js
│   │   │   ├── modal.js
│   │   │   └── toast.js
│   │   ├── pages/
│   │   │   ├── README.md
│   │   │   └── home-page.js
│   │   └── data/
│   │       ├── README.md
│   │       ├── mock-data.js
│   │       └── schemas.js
│   │
│   ├── img/
│   │   ├── README.md
│   │   ├── logo/
│   │   │   ├── README.md
│   │   │   ├── logo.svg
│   │   │   ├── logo-light.svg
│   │   │   └── logo-dark.svg
│   │   ├── favicon/
│   │   │   ├── README.md
│   │   │   ├── favicon.ico
│   │   │   ├── favicon.svg
│   │   │   ├── apple-touch-icon.png
│   │   │   └── icon-512.png
│   │   ├── icons/
│   │   │   ├── README.md
│   │   │   └── icon-example.svg
│   │   ├── illustrations/
│   │   │   ├── README.md
│   │   │   └── illustration-example.svg
│   │   ├── backgrounds/
│   │   │   ├── README.md
│   │   │   └── background-example.webp
│   │   ├── screenshots/
│   │   │   ├── README.md
│   │   │   └── screenshot-example.png
│   │   └── placeholders/
│   │       ├── README.md
│   │       └── placeholder.svg
│   │
│   ├── fonts/
│   │   ├── README.md
│   │   └── local-font-example.woff2
│   │
│   ├── data/
│   │   ├── README.md
│   │   ├── content/
│   │   │   ├── README.md
│   │   │   └── home.json
│   │   ├── config/
│   │   │   ├── README.md
│   │   │   └── site.json
│   │   └── samples/
│   │       ├── README.md
│   │       └── example.json
│   │
│   └── vendor/
│       ├── README.md
│       └── vendor-lib-example/
│
├── pages/
│   ├── README.md
│   └── example.html
│
├── docs/
│   ├── README.md
│   ├── ARQUITETURA_E_ORGANIZACAO.md
│   ├── GUIA_DE_ESTILO.md
│   ├── DECISOES_TECNICAS.md
│   ├── CHECKLIST_PUBLICACAO.md
│   └── adr/
│       ├── README.md
│       └── 0001-arquitetura-estatica.md
│
├── scripts/
│   ├── README.md
│   ├── optimize-images.js
│   └── generate-sitemap.js
│
├── tests/
│   ├── README.md
│   ├── manual/
│   │   ├── README.md
│   │   └── checklist-navegacao.md
│   └── accessibility/
│       ├── README.md
│       └── checklist-a11y.md
│
└── .github/
    ├── README.md
    ├── workflows/
    │   ├── README.md
    │   └── pages.yml
    └── ISSUE_TEMPLATE/
        ├── README.md
        ├── bug_report.md
        └── feature_request.md
```

---

## 4. Organização por camada

A arquitetura pode ser entendida em camadas.

### 4.1 Raiz do projeto

A raiz contém os arquivos essenciais de entrada, configuração e publicação.

Responsabilidades:

- abrigar o `index.html`;
- conter arquivos usados diretamente pelo navegador;
- documentar o projeto;
- permitir publicação no GitHub Pages;
- manter arquivos institucionais e de configuração.

Arquivos principais:

| Arquivo | Função |
|---|---|
| `README.md` | Apresentação geral do projeto |
| `index.html` | Página inicial da aplicação |
| `404.html` | Página de erro personalizada |
| `robots.txt` | Orientação para mecanismos de busca |
| `sitemap.xml` | Mapa do site |
| `manifest.webmanifest` | Configuração de instalação/PWA futura |
| `.gitignore` | Arquivos ignorados pelo Git |
| `.editorconfig` | Padronização básica de edição |
| `LICENSE` | Licença do projeto |

---

### 4.2 `assets/`

A pasta `assets/` guarda tudo que é usado diretamente pela interface: estilos, scripts, imagens, fontes, dados e bibliotecas externas.

Ela funciona como a camada pública de recursos estáticos.

Responsabilidades:

- concentrar recursos da aplicação;
- evitar arquivos soltos na raiz;
- separar visual, comportamento e conteúdo;
- facilitar manutenção dos caminhos relativos.

---

### 4.3 `assets/css/`

Guarda os estilos da aplicação.

A recomendação é que `main.css` seja o ponto central de importação dos demais arquivos CSS.

Exemplo:

```css
@import url("./base/reset.css");
@import url("./base/variables.css");
@import url("./base/typography.css");

@import url("./layout/grid.css");
@import url("./layout/header.css");
@import url("./layout/footer.css");
@import url("./layout/sections.css");

@import url("./components/buttons.css");
@import url("./components/cards.css");
@import url("./components/forms.css");
@import url("./components/navigation.css");

@import url("./pages/home.css");

@import url("./utilities/spacing.css");
@import url("./utilities/visibility.css");
@import url("./utilities/helpers.css");
```

Subpastas recomendadas:

| Pasta | Função |
|---|---|
| `base/` | Reset, variáveis globais, tipografia |
| `layout/` | Estrutura da página: grid, header, footer, seções |
| `components/` | Estilos reutilizáveis de componentes |
| `pages/` | Estilos específicos de páginas |
| `themes/` | Temas visuais |
| `utilities/` | Classes utilitárias pequenas |

---

### 4.4 `assets/js/`

Guarda o JavaScript da aplicação.

A recomendação é que `app.js` seja o ponto de entrada principal da aplicação.

Subpastas recomendadas:

| Pasta | Função |
|---|---|
| `core/` | Configurações, constantes e estado global |
| `utils/` | Funções auxiliares genéricas |
| `services/` | Regras de acesso a dados, storage e navegação |
| `components/` | Componentes JS reutilizáveis |
| `pages/` | Scripts específicos de cada página |
| `data/` | Dados JS temporários, mocks e schemas |

Exemplo de organização do `app.js`:

```js
import { initHomePage } from "./pages/home-page.js";

document.addEventListener("DOMContentLoaded", () => {
  initHomePage();
});
```

Para isso funcionar no HTML, use:

```html
<script type="module" src="./assets/js/app.js"></script>
```

---

### 4.5 `assets/img/`

Guarda todas as imagens do projeto.

Subpastas recomendadas:

| Pasta | Função |
|---|---|
| `logo/` | Logos principais e variações |
| `favicon/` | Favicons e ícones de instalação |
| `icons/` | Ícones funcionais da interface |
| `illustrations/` | Ilustrações decorativas ou explicativas |
| `backgrounds/` | Imagens de fundo |
| `screenshots/` | Capturas de tela do projeto |
| `placeholders/` | Imagens temporárias ou genéricas |

Boas práticas:

- usar `.svg` para logos e ícones sempre que possível;
- usar `.webp` para imagens rasterizadas otimizadas;
- evitar imagens muito pesadas;
- manter nomes descritivos;
- não misturar logo, favicon, print e ilustração na mesma pasta.

Exemplos de nomes:

```text
logo-primary.svg
logo-light.svg
logo-dark.svg
icon-search.svg
hero-background.webp
card-placeholder.svg
screenshot-home-desktop.png
```

---

### 4.6 `assets/fonts/`

Guarda fontes locais, caso o projeto precise delas.

Recomendações:

- preferir `.woff2`;
- documentar origem e licença;
- evitar incluir muitas variações desnecessárias;
- não misturar fontes externas baixadas sem licença clara.

---

### 4.7 `assets/data/`

Guarda dados estáticos consumidos pela aplicação.

Pode conter:

- textos da página;
- listas de itens;
- dados de cards;
- configurações de site;
- dados de demonstração;
- conteúdo que futuramente poderia migrar para uma API.

Exemplo:

```json
{
  "siteName": "Nome do Projeto",
  "description": "Aplicação estática publicada no GitHub Pages."
}
```

---

### 4.8 `assets/vendor/`

Guarda bibliotecas externas adicionadas manualmente ao projeto.

Use somente quando necessário.

Exemplos:

- biblioteca JS sem npm;
- CSS externo baixado;
- polyfills;
- scripts de terceiros.

Sempre documentar:

- nome da biblioteca;
- versão;
- origem;
- licença;
- motivo de uso.

---

### 4.9 `pages/`

Guarda páginas HTML adicionais.

Mesmo que o projeto comece apenas com `index.html`, essa pasta já prepara o crescimento.

Exemplo futuro:

```text
pages/
├── about.html
├── catalog.html
├── contact.html
└── details.html
```

Recomendação:

- manter `index.html` na raiz;
- colocar páginas secundárias em `pages/`;
- usar caminhos relativos com cuidado;
- evitar duplicação excessiva de blocos HTML.

---

### 4.10 `docs/`

Guarda documentação técnica e organizacional.

Documentos recomendados:

| Arquivo | Função |
|---|---|
| `ARQUITETURA_E_ORGANIZACAO.md` | Explica a estrutura geral do projeto |
| `GUIA_DE_ESTILO.md` | Define padrões visuais e textuais |
| `DECISOES_TECNICAS.md` | Registra decisões importantes |
| `CHECKLIST_PUBLICACAO.md` | Checklist antes de publicar |
| `adr/` | Registros formais de decisões arquiteturais |

---

### 4.11 `scripts/`

Guarda scripts auxiliares de manutenção.

Mesmo em uma aplicação estática, podem existir scripts para:

- otimizar imagens;
- gerar sitemap;
- validar links;
- limpar arquivos temporários;
- preparar conteúdo.

Essa pasta não precisa ser usada no início, mas é útil para evolução.

---

### 4.12 `tests/`

Guarda testes, checklists e validações.

Para um projeto estático simples, a pasta pode começar com testes manuais:

```text
tests/manual/checklist-navegacao.md
tests/accessibility/checklist-a11y.md
```

Com o tempo, pode incluir:

- testes de interface;
- validação de acessibilidade;
- testes de links;
- testes de responsividade;
- testes de componentes JS.

---

### 4.13 `.github/`

Guarda configurações específicas do GitHub.

Pode conter:

- workflow de publicação;
- templates de issues;
- templates de pull request;
- configurações de automação.

Para GitHub Pages, pode haver um workflow como:

```text
.github/workflows/pages.yml
```

---

## 5. Convenção de nomes

### 5.1 Pastas

Usar nomes em inglês, minúsculos e com hífen quando necessário:

```text
assets/
components/
home-page.js
storage-service.js
checklist-publicacao.md
```

Evitar:

```text
Assets/
Componentes/
HomePage.js
meu arquivo.js
```

### 5.2 Arquivos HTML

Usar nomes curtos e claros:

```text
index.html
about.html
contact.html
details.html
```

### 5.3 Arquivos CSS

Usar nomes relacionados à função do estilo:

```text
buttons.css
cards.css
header.css
home.css
variables.css
```

### 5.4 Arquivos JS

Usar nomes relacionados à responsabilidade do módulo:

```text
app.js
config.js
dom.js
data-service.js
home-page.js
```

### 5.5 Imagens

Usar nomes descritivos:

```text
logo-primary.svg
hero-background.webp
icon-menu.svg
card-placeholder.svg
```

---

## 6. Diretrizes para `README.md` em cada pasta

Cada pasta deve ter um `README.md` curto explicando:

1. o objetivo da pasta;
2. que tipo de arquivo deve ficar ali;
3. que tipo de arquivo não deve ficar ali;
4. convenção de nomes;
5. exemplos;
6. observações importantes.

### 6.1 Modelo padrão de README por pasta

```md
# Nome da pasta

## Função

Explique em 2 ou 3 frases para que esta pasta existe.

## O que deve ficar aqui

- Tipo de arquivo 1;
- Tipo de arquivo 2;
- Tipo de arquivo 3.

## O que não deve ficar aqui

- Arquivos que pertencem a outra camada;
- Arquivos temporários;
- Arquivos sem relação com esta pasta.

## Convenção de nomes

Use nomes em minúsculas, sem espaços e com hífen quando necessário.

Exemplos:

```text
exemplo-arquivo.ext
outro-exemplo.ext
```

## Exemplos de uso

Explique como os arquivos desta pasta costumam ser referenciados no projeto.

## Observações

Inclua regras especiais, cuidados ou decisões importantes.
```

---

## 7. Conteúdo sugerido para os READMEs principais

### 7.1 `assets/README.md`

```md
# assets

Esta pasta concentra os recursos estáticos usados pela aplicação, como CSS, JavaScript, imagens, fontes, dados e bibliotecas externas.

## O que deve ficar aqui

- Estilos da interface;
- Scripts da aplicação;
- Imagens e ícones;
- Fontes locais;
- Dados estáticos;
- Bibliotecas externas adicionadas manualmente.

## O que não deve ficar aqui

- Documentação técnica geral;
- Arquivos de planejamento;
- Testes;
- Páginas HTML secundárias.

## Observações

Todos os caminhos usados no HTML devem considerar esta pasta como origem dos recursos públicos.
```

---

### 7.2 `assets/css/README.md`

```md
# css

Esta pasta reúne todos os arquivos de estilo da aplicação.

## O que deve ficar aqui

- CSS global;
- CSS de layout;
- CSS de componentes;
- CSS específico de páginas;
- Temas;
- Classes utilitárias.

## O que não deve ficar aqui

- JavaScript;
- Imagens;
- Dados;
- Arquivos HTML.

## Organização

O arquivo `main.css` deve funcionar como ponto central de entrada dos estilos.
```

---

### 7.3 `assets/js/README.md`

```md
# js

Esta pasta reúne os scripts da aplicação.

## O que deve ficar aqui

- Arquivo principal da aplicação;
- Módulos de configuração;
- Utilitários;
- Serviços;
- Componentes;
- Scripts específicos de páginas.

## O que não deve ficar aqui

- Estilos CSS;
- Imagens;
- Dados JSON de conteúdo final, salvo quando forem mocks em JavaScript;
- Bibliotecas externas grandes, que devem ficar em `assets/vendor/`.

## Organização

O arquivo `app.js` deve ser o ponto de entrada principal da aplicação.
```

---

### 7.4 `assets/img/README.md`

```md
# img

Esta pasta reúne todas as imagens usadas pela aplicação.

## O que deve ficar aqui

- Logos;
- Favicons;
- Ícones;
- Ilustrações;
- Imagens de fundo;
- Screenshots;
- Placeholders.

## O que não deve ficar aqui

- Arquivos CSS;
- Arquivos JS;
- Documentos;
- Imagens sem uso no projeto.

## Convenção

Prefira SVG para logos e ícones. Prefira WEBP para imagens rasterizadas otimizadas.
```

---

### 7.5 `assets/data/README.md`

```md
# data

Esta pasta guarda dados estáticos consumidos pela aplicação.

## O que deve ficar aqui

- Arquivos JSON de conteúdo;
- Configurações públicas do site;
- Dados de exemplo;
- Dados que futuramente poderiam vir de uma API.

## O que não deve ficar aqui

- Dados sensíveis;
- Senhas;
- Chaves privadas;
- Informações pessoais;
- Arquivos temporários.

## Observações

Como o projeto é estático, tudo nesta pasta pode ser acessado publicamente pelo navegador.
```

---

### 7.6 `docs/README.md`

```md
# docs

Esta pasta guarda a documentação técnica, organizacional e arquitetural do projeto.

## O que deve ficar aqui

- Explicações da arquitetura;
- Guias de estilo;
- Decisões técnicas;
- Checklists de publicação;
- Registros de decisão arquitetural.

## O que não deve ficar aqui

- Código da aplicação;
- Imagens usadas diretamente pela interface;
- Arquivos temporários.

## Observações

Sempre que uma decisão importante for tomada, ela deve ser registrada nesta pasta.
```

---

### 7.7 `scripts/README.md`

```md
# scripts

Esta pasta guarda scripts auxiliares para manutenção do projeto.

## O que deve ficar aqui

- Scripts para otimizar imagens;
- Scripts para gerar sitemap;
- Scripts para validar links;
- Scripts para preparar dados;
- Scripts de manutenção.

## O que não deve ficar aqui

- Código executado diretamente pela interface no navegador;
- Arquivos CSS;
- Arquivos HTML;
- Dados finais da aplicação.

## Observações

Scripts desta pasta podem depender de Node.js ou outra ferramenta local, mas não devem ser necessários para abrir a aplicação básica.
```

---

### 7.8 `tests/README.md`

```md
# tests

Esta pasta guarda testes, checklists e validações do projeto.

## O que deve ficar aqui

- Checklists manuais;
- Testes de navegação;
- Testes de acessibilidade;
- Testes de responsividade;
- Testes futuros automatizados.

## O que não deve ficar aqui

- Código principal da aplicação;
- Documentação arquitetural;
- Imagens da interface.

## Observações

No início, os testes podem ser apenas checklists manuais em Markdown.
```

---

### 7.9 `.github/README.md`

```md
# .github

Esta pasta guarda configurações específicas do GitHub.

## O que deve ficar aqui

- Workflows do GitHub Actions;
- Templates de issues;
- Templates de pull request;
- Configurações relacionadas ao repositório.

## O que não deve ficar aqui

- Código principal da aplicação;
- Assets da interface;
- Documentação geral que deveria estar em `docs/`.

## Observações

Essa pasta é usada pelo GitHub e pode ser expandida conforme o projeto amadurece.
```

---

## 8. Organização recomendada do HTML

Mesmo começando com uma página única, o `index.html` deve ser organizado por seções claras.

Exemplo:

```html
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- SEO básico -->
    <title>Nome do Projeto</title>
    <meta name="description" content="Descrição breve do projeto." />

    <!-- Favicons -->
    <link rel="icon" href="./assets/img/favicon/favicon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="./assets/img/favicon/apple-touch-icon.png" />

    <!-- Manifest -->
    <link rel="manifest" href="./manifest.webmanifest" />

    <!-- CSS principal -->
    <link rel="stylesheet" href="./assets/css/main.css" />
  </head>

  <body>
    <header class="site-header">
      <!-- Cabeçalho -->
    </header>

    <main id="main-content">
      <section class="hero-section">
        <!-- Seção principal -->
      </section>

      <section class="content-section">
        <!-- Conteúdo -->
      </section>
    </main>

    <footer class="site-footer">
      <!-- Rodapé -->
    </footer>

    <script type="module" src="./assets/js/app.js"></script>
  </body>
</html>
```

---

## 9. Organização recomendada do CSS

A ordem sugerida dos estilos é:

1. reset;
2. variáveis;
3. tipografia;
4. layout;
5. componentes;
6. estilos específicos de páginas;
7. temas;
8. utilitários.

### 9.1 Exemplo de `variables.css`

```css
:root {
  --color-primary: #2158a5;
  --color-secondary: #152f4d;
  --color-accent: #e63616;

  --color-background: #ffffff;
  --color-surface: #f2f2f2;
  --color-text: #0f1626;

  --font-family-base: Arial, Helvetica, sans-serif;
  --font-family-heading: Arial, Helvetica, sans-serif;

  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
  --spacing-xl: 4rem;

  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;

  --container-width: 1120px;
}
```

### 9.2 Exemplo de componente CSS

```css
.card {
  border-radius: var(--radius-md);
  background: var(--color-surface);
  padding: var(--spacing-md);
}

.card__title {
  margin-bottom: var(--spacing-sm);
}

.card__description {
  color: var(--color-text);
}
```

---

## 10. Organização recomendada do JavaScript

O JavaScript deve ser separado por responsabilidade.

### 10.1 Exemplo de `app.js`

```js
import { initHomePage } from "./pages/home-page.js";

document.addEventListener("DOMContentLoaded", () => {
  initHomePage();
});
```

### 10.2 Exemplo de `pages/home-page.js`

```js
import { createCard } from "../components/card.js";

export function initHomePage() {
  const container = document.querySelector("[data-cards]");

  if (!container) {
    return;
  }

  const card = createCard({
    title: "Exemplo",
    description: "Card criado por JavaScript."
  });

  container.appendChild(card);
}
```

### 10.3 Exemplo de `components/card.js`

```js
export function createCard({ title, description }) {
  const article = document.createElement("article");
  article.classList.add("card");

  article.innerHTML = `
    <h2 class="card__title">${title}</h2>
    <p class="card__description">${description}</p>
  `;

  return article;
}
```

---

## 11. Organização dos dados

Se o conteúdo começar a crescer, evite deixar tudo fixo no HTML.

Use arquivos em `assets/data/content/`.

Exemplo de `home.json`:

```json
{
  "hero": {
    "title": "Título principal",
    "subtitle": "Subtítulo da aplicação"
  },
  "cards": [
    {
      "title": "Item 1",
      "description": "Descrição do item 1"
    },
    {
      "title": "Item 2",
      "description": "Descrição do item 2"
    }
  ]
}
```

O JavaScript pode carregar esse arquivo com `fetch`.

```js
export async function loadHomeContent() {
  const response = await fetch("./assets/data/content/home.json");

  if (!response.ok) {
    throw new Error("Não foi possível carregar o conteúdo da página inicial.");
  }

  return response.json();
}
```

---

## 12. Diretrizes para imagens

### 12.1 Logos

Guardar em:

```text
assets/img/logo/
```

Recomendado:

```text
logo.svg
logo-light.svg
logo-dark.svg
logo-horizontal.svg
logo-symbol.svg
```

### 12.2 Favicons

Guardar em:

```text
assets/img/favicon/
```

Recomendado:

```text
favicon.ico
favicon.svg
apple-touch-icon.png
icon-192.png
icon-512.png
```

### 12.3 Ícones

Guardar em:

```text
assets/img/icons/
```

Recomendado:

```text
icon-menu.svg
icon-close.svg
icon-search.svg
icon-arrow-right.svg
```

### 12.4 Ilustrações

Guardar em:

```text
assets/img/illustrations/
```

Recomendado:

```text
hero-illustration.svg
empty-state.svg
success-state.svg
```

### 12.5 Fundos

Guardar em:

```text
assets/img/backgrounds/
```

Recomendado:

```text
hero-background.webp
section-pattern.svg
```

### 12.6 Screenshots

Guardar em:

```text
assets/img/screenshots/
```

Recomendado:

```text
home-desktop.png
home-mobile.png
feature-example.png
```

---

## 13. Diretrizes para documentação

A documentação deve responder a três perguntas:

1. O que existe no projeto?
2. Por que existe?
3. Como deve ser mantido?

Documentos recomendados:

```text
docs/
├── ARQUITETURA_E_ORGANIZACAO.md
├── GUIA_DE_ESTILO.md
├── DECISOES_TECNICAS.md
├── CHECKLIST_PUBLICACAO.md
└── adr/
    └── 0001-arquitetura-estatica.md
```

### 13.1 `GUIA_DE_ESTILO.md`

Deve documentar:

- paleta de cores;
- tipografia;
- espaçamentos;
- botões;
- cards;
- ícones;
- tom de voz;
- regras para imagens;
- padrões de responsividade.

### 13.2 `DECISOES_TECNICAS.md`

Deve registrar decisões como:

- por que usar HTML/CSS/JS puro;
- por que publicar no GitHub Pages;
- por que separar assets por responsabilidade;
- por que não usar framework inicialmente;
- quais limitações foram aceitas.

### 13.3 `CHECKLIST_PUBLICACAO.md`

Deve conter verificações antes de publicar:

- links funcionando;
- imagens otimizadas;
- favicon carregando;
- responsividade conferida;
- contraste adequado;
- `404.html` funcionando;
- `README.md` atualizado;
- erros no console corrigidos.

### 13.4 ADRs

ADR significa Architectural Decision Record.

Cada ADR registra uma decisão importante.

Exemplo:

```text
docs/adr/0001-arquitetura-estatica.md
```

Estrutura sugerida:

```md
# 0001 — Uso de arquitetura estática

## Status

Aceita.

## Contexto

O projeto será publicado inicialmente no GitHub Pages.

## Decisão

Usar HTML, CSS e JavaScript puro, sem back-end inicial.

## Consequências

A aplicação será simples de publicar, mas dados sensíveis e lógicas privadas não poderão ficar no front-end.
```

---

## 14. Checklist inicial de implementação

Para começar de forma organizada:

- criar a estrutura de pastas;
- criar `README.md` na raiz;
- criar `README.md` em cada pasta principal;
- criar `index.html`;
- criar `assets/css/main.css`;
- criar `assets/css/base/variables.css`;
- criar `assets/js/app.js`;
- criar `assets/img/logo/`;
- criar `assets/img/favicon/`;
- criar `docs/ARQUITETURA_E_ORGANIZACAO.md`;
- criar `docs/GUIA_DE_ESTILO.md`;
- criar `docs/CHECKLIST_PUBLICACAO.md`;
- testar localmente abrindo o `index.html`;
- publicar no GitHub Pages.

---

## 15. Estrutura mínima para começar sem perder robustez

Se a árvore completa parecer grande demais para o primeiro commit, é possível começar com uma versão reduzida:

```text
nome-do-projeto/
├── README.md
├── index.html
├── 404.html
├── manifest.webmanifest
├── assets/
│   ├── README.md
│   ├── css/
│   │   ├── README.md
│   │   ├── main.css
│   │   ├── base/
│   │   │   ├── README.md
│   │   │   ├── reset.css
│   │   │   └── variables.css
│   │   ├── layout/
│   │   │   ├── README.md
│   │   │   └── sections.css
│   │   └── components/
│   │       ├── README.md
│   │       └── buttons.css
│   ├── js/
│   │   ├── README.md
│   │   ├── app.js
│   │   ├── utils/
│   │   │   ├── README.md
│   │   │   └── dom.js
│   │   └── pages/
│   │       ├── README.md
│   │       └── home-page.js
│   └── img/
│       ├── README.md
│       ├── logo/
│       │   └── README.md
│       └── favicon/
│           └── README.md
└── docs/
    ├── README.md
    ├── ARQUITETURA_E_ORGANIZACAO.md
    └── CHECKLIST_PUBLICACAO.md
```

Essa versão já mantém separação adequada sem criar arquivos demais logo no início.

---

## 16. Regras gerais de manutenção

1. Não colocar CSS dentro do HTML, salvo exceções pequenas e justificadas.
2. Não colocar JavaScript inline no HTML, salvo casos mínimos.
3. Não misturar imagens de tipos diferentes na mesma pasta.
4. Não criar arquivos com nomes genéricos demais, como `teste.js`, `novo.css` ou `imagem1.png`.
5. Sempre documentar decisões relevantes.
6. Sempre atualizar o README quando uma pasta mudar de função.
7. Sempre otimizar imagens antes de publicar.
8. Nunca colocar dados sensíveis em projeto estático.
9. Usar caminhos relativos.
10. Manter a raiz do projeto limpa.

---

## 17. Regra de ouro

A aplicação pode ser simples no funcionamento, mas não precisa ser desorganizada na estrutura.

A separação por responsabilidade permite que o projeto comece como uma página única e evolua, se necessário, para uma aplicação maior, com múltiplas páginas, dados estruturados, componentes reutilizáveis e documentação técnica consistente.
