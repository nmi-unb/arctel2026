# Handoff: Mural de Avisos (formato 1c — painel dividido)

## Overview
Transforma a seção "Avisos" do site em um mural compacto de 2 colunas + faixa inferior, substituindo o placeholder "Em Desenvolvimento" atual.

## About the Design Files
`mural-referencia.html` é uma **referência de design em HTML** — mostra layout, hierarquia e estados pretendidos, não é código de produção para copiar direto. Recrie no ambiente já existente do repositório `arctel2026` (HTML/CSS/JS estático), seguindo a arquitetura de `assets/css/` já em uso, e conectando aos dados carregados via JSON (ver seção "Dados").

## Fidelity
**Alta fidelidade (hifi)** — cores, tipografia, espaçamento e estrutura devem ser seguidos como especificado. Conteúdo é placeholder (`[[...]]`) e será preenchido via JS a partir de um JSON de avisos (lógica de carregamento fora deste escopo).

## Screens / Views

### Mural de Avisos — painel dividido (1c)
**Propósito:** mostrar em poucos segundos o aviso mais importante, a aula atual/próxima com ação de acesso, e um atalho para o histórico.

**Layout:**
- Container: `max-width: var(--container-max-width)` (1140px), centrado, mesmo grid das outras seções do site.
- **Painel superior** (`.split-panel`): `display:grid; grid-template-columns: 1.1fr 1fr`, borda `1px solid var(--color-gray-200)`, `border-radius:12px`, `overflow:hidden`.
  - **Coluna esquerda** (aviso em destaque): padding `20px 22px`, borda direita `1px solid var(--color-gray-200)`, fundo branco. Contém: badge de tipo (ver Estados), título (15px, weight 800, `var(--navy-700)`), mensagem + data (13px, cor #555).
  - **Coluna direita** (aula atual/próxima): mesmo padding, fundo `#f6fbf8` (tint claro sobre verde). Contém: badge "Ao vivo agora" (quando aplicável), título do módulo/aula, horário, e botão `.btn.btn--solid.btn--sm` "Acessar aula ao vivo" (só aparece durante a transmissão).
- **Faixa inferior** (`.split-strip`): fora do grid, mesma largura do painel, borda lateral e inferior seguindo o mesmo `border-radius` (0 0 12px 12px), `border-top:1px solid var(--color-gray-200)`, padding `12px 22px`, `display:flex; justify-content:space-between`. Contém texto "Última atualização: [[DATA_E_HORA]]" e botão pill "Ver histórico de avisos" (borda `1px solid var(--verde-600)`, texto `var(--verde-700)`, hover preenche com `var(--verde-600)`/texto branco).

## Interactions & Behavior
- Botão "Ver histórico de avisos" abre um modal (reutilizar o modal já especificado no handoff anterior de avisos, se existente no projeto — título "Histórico de avisos", lista cronológica decrescente, botão fechar, `Esc` fecha, foco retorna ao botão).
- Botão "Acessar aula ao vivo" só é renderizado quando o aviso tiver status `ao_vivo`; caso contrário mostrar "Próxima aula" com data/horário e sem botão de ação (ou botão desabilitado, a critério do dev).
- Indicador do badge "Ao vivo agora" pulsa suavemente (`@keyframes pulse`, 1.6s) apenas quando `prefers-reduced-motion: no-preference`.

## State Management
Sem estado de interação além do modal (aberto/fechado). Conteúdo é 100% dirigido por dados (ver `Dados`).

## Design Tokens
- `--verde-600: #4bbe6e`, `--verde-700: #64c080`
- `--navy-500: #497c7e`, `--navy-700: #275254`
- `--color-gray-200: #d9d9d9`
- Fundo tint da coluna "ao vivo": `#f6fbf8` (derivado do verde, não está nas variáveis — considerar adicionar ao design system)
- `border-radius: 12px` (painel), `14px` (badges), `18px` (botão pill)
- Fonte: `"Roboto", "Inter", Arial, sans-serif` (`--font-base`)

## Estados do badge (tipo de aviso)
Cada tipo tem cor de fundo, cor de texto e ponto colorido — nunca dependa só da cor, o texto do badge sempre acompanha:
- Aula confirmada: fundo `#e9f8ee`, texto `var(--verde-700)`, ponto `var(--verde-600)`
- Ao vivo agora: fundo `var(--navy-700)`, texto branco, ponto vermelho `#ff6161` (pulsante)
- Alteração importante: fundo `#fff4e0`, texto `#8a5a00`, ponto `#e0a300`
- Alerta: fundo `#fdeaea`, texto `#a12b2b`, ponto `#d64545`
- Material disponível: fundo `#eaf3ff`, texto `#1f5c9e`, ponto `#3f83c9`
- Encerrado: fundo `#f0eee9`, texto `#7a7a7a`, ponto `#aaa`

## Responsividade
- Desktop/tablet largo: grid de 2 colunas conforme especificado.
- Mobile (≤640px): `.split-panel` vira `grid-template-columns: 1fr` (colunas empilhadas, coluna esquerda com borda inferior no lugar da lateral); `.split-strip` empilha texto e botão (`flex-direction:column`).
- Sem rolagem horizontal em nenhuma largura.

## Assets
Nenhum asset novo — apenas cores/estilos do design system existente.

## Dados esperados (JSON)
```
aviso_destaque: { tipo, titulo, mensagem, data }
aula: { status: "ao_vivo" | "proxima", titulo, horario, urlTransmissao? }
info_complementar: { ultimaAtualizacao }
```

## Files
- `mural-referencia.html` — referência visual completa do formato 1c (HTML + CSS inline, usa `assets/css/main.css` do repo para tokens/tipografia/botões).
