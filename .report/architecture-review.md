# Revisão da arquitetura

- Data: 2026-08-18
- Escopo: comportamento do cabeçalho sticky e organização relacionada
- Compatibilidade com GitHub Pages: compatível
- Diagnóstico geral: a aplicação usa HTML, CSS e JavaScript estáticos, com caminhos relativos válidos. O defeito do cabeçalho vinha de uma mudança de geometria no estado fixado, não de uma limitação do GitHub Pages.

## Achados críticos

Nenhuma ocorrência encontrada nesta categoria.

## Achados importantes

### [ARQ-001] Estado fixado alterava a altura do documento

- Severidade: Importante
- Local: `assets/css/layout/header.css`
- Problema: ao receber `is-pinned`, o cabeçalho e seus links reduziam o padding.
- Por que importa: em páginas curtas, a redução da altura total pode fazer o `scrollY` atravessar o limite de 80 px nos dois sentidos, alternando continuamente o estado do menu.
- Solução sugerida: manter a geometria do cabeçalho constante e limitar `is-pinned` a mudanças visuais que não alterem o fluxo, como fundo, sombra e borda.
- Situação: solução implementada neste atendimento a pedido do usuário.

#### Decisão do usuário

- [ ] Aceito a solução sugerida
- [ ] Não aceito a solução sugerida
- [ ] Quero propor uma solução diferente

Sugestão ou observação do usuário:

> Preencher aqui.

### [ARQ-002] Há duas implementações de menu no projeto

- Severidade: Importante
- Local: `assets/js/menu.js` e `assets/js/components/hamburger-menu.js`
- Problema: as páginas carregam `menu.js`, enquanto existe outra implementação independente de menu hambúrguer que não é inicializada por `app.js`.
- Por que importa: duas versões da mesma responsabilidade podem divergir e fazer uma correção ser aplicada no arquivo que não está em uso.
- Solução sugerida: consolidar o comportamento em um único componente importado por `assets/js/app.js` e remover a implementação obsoleta após validar todas as páginas.

#### Decisão do usuário

- [ ] Aceito a solução sugerida
- [ ] Não aceito a solução sugerida
- [ ] Quero propor uma solução diferente

Sugestão ou observação do usuário:

> Preencher aqui.

## Melhorias

### [ARQ-003] Documentação técnica está fora da pasta convencional

- Severidade: Melhoria
- Local: `_docs/`
- Problema: a documentação e scripts auxiliares ficam em `_docs/`, incluindo artefatos locais como `__pycache__`, enquanto não existe `docs/`.
- Por que importa: mistura documentação com utilitários locais e reduz a previsibilidade da estrutura para manutenção.
- Solução sugerida: separar documentação em `docs/`, scripts locais em uma pasta própria e manter caches fora do repositório.

#### Decisão do usuário

- [ ] Aceito a solução sugerida
- [ ] Não aceito a solução sugerida
- [ ] Quero propor uma solução diferente

Sugestão ou observação do usuário:

> Preencher aqui.

### [ARQ-004] Não há página 404 própria

- Severidade: Melhoria
- Local: raiz do projeto
- Problema: não foi encontrado `404.html`.
- Por que importa: rotas inválidas no GitHub Pages não terão uma resposta visual coerente com a aplicação.
- Solução sugerida: criar uma página `404.html` estática com link de retorno à página inicial.

#### Decisão do usuário

- [ ] Aceito a solução sugerida
- [ ] Não aceito a solução sugerida
- [ ] Quero propor uma solução diferente

Sugestão ou observação do usuário:

> Preencher aqui.

