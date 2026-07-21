# Instruções — aplicar modelo 1A em "Aulas, gravações e recursos"

Aplicar em todas as páginas de módulo (`modulo-1.html` a `modulo-11.html`), substituindo o bloco atual:
```html
<h3>Aulas, gravações e recursos</h3>
<p class="module-page-materials">Os materiais, aulas e recursos deste módulo serão adicionados posteriormente.</p>
```

## Estrutura (accordion por aula)
Para cada aula de `assets/data/modulos/modulo-XX.json` (`lessons[]`), renderizar um item de accordion:
- Header sempre visível: número (círculo navy, `.lesson-num`), título da aula, badge de status, data.
- Corpo (expande ao clicar no header): 3 subgrupos, só exibidos se tiverem conteúdo:
  - **Transmissão**: pill link para `links.teams` e `links.youtubeLive` quando presentes; se `youtubeRecorded` existir, pill "Gravação"; se ausente, mostrar pill desabilitada "Gravação (em breve)".
  - **Materiais do professor**: pill por item em `materials.professor` (usar `title`, linkar `url`; se `available:false`, desabilitar).
  - **Cursos substitutos**: pill por item em `materials.replacementCourses` (mesma regra de `available`).
- Apenas um item aberto por vez (comportamento accordion), controlado via JS (toggle de classe, sem framework).

## Badge de status (`status` da aula)
- `scheduled` → badge azul "Agendada" (`#eaf3ff`/`#1f5c9e`, ponto `#3f83c9`)
- `live` → badge navy "Ao vivo" (`var(--navy-700)`/branco, ponto vermelho `#ff6161`, pulsante com `prefers-reduced-motion: no-preference`)
- `done`/concluída → badge cinza "Concluída" (`#f0eee9`/`#7a7a7a`, ponto `#aaa`)

## Estilo (variáveis já existentes no projeto)
- Item: `border:1px solid var(--color-gray-200); border-radius:10px`
- Número: círculo 28px, fundo `var(--navy-700)`, texto branco, bold
- Pills de link: `border-radius:14px`, `padding:6px 13px`, `font-size:12px`, cores por tipo — Teams `#eaf3ff/#1f5c9e`, YouTube `#fdeaea/#a12b2b`, Material `#e9f8ee/var(--verde-700)`, Curso `#fff4e0/#8a5a00`
- Pill desabilitada: fundo `#f0eee9`, texto `#aaa`, sem link ativo

## Dados
Ler `assets/data/modulos/modulo-XX.json` (schema já definido, `lessons[].links` e `lessons[].materials`). Não inventar links/materiais ausentes — omitir a subseção correspondente quando vazia.

## Reuso
Implementar como componente/partial único reutilizado pelas 11 páginas (mesma lógica de template já usada para o restante da página do módulo), não duplicar HTML manualmente em cada página.

Referência visual completa: `aulas-recursos-exploracao.html` (opção 1a).
