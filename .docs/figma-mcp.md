<link rel="stylesheet" href="../.css/style.css">

# Figma MCP — guia de comandos

MCP (Model Context Protocol) do Figma conecta Claude Code ao Figma direto — ler designs, gerar código, escrever de volta no Figma. Ferramentas abaixo, agrupadas por uso.

## Antes de usar
Sempre carregar skill correspondente antes de chamar a tool (regra do server, evita erro comum):
- `use_figma` → carregar skill `figma-use` antes
- `create_new_file` → carregar skill `figma-create-new-file` antes
- `generate_diagram` → carregar skill `figma-generate-diagram` antes

Skill = `Skill` tool, não comando manual. Ex: pedir "cria arquivo novo no Figma" já dispara isso sozinho.

## Ler design do Figma (Figma → código)

| Tool | Uso |
|---|---|
| `get_design_context` | Extrai estrutura, texto, estilos de um node/frame Figma pra virar código |
| `get_screenshot` | Tira print de um node/frame — útil pra ver visual antes de implementar |
| `get_metadata` | Retorna metadados do arquivo/node (ids, tipos, hierarquia) |
| `get_variable_defs` | Lista variáveis/tokens de design (cores, spacing, etc) definidas no arquivo |
| `get_figjam` | Lê conteúdo de board FigJam (fluxos, notas, diagramas) |
| `get_motion_context` | Extrai dados de animação/motion de um node |
| `search_design_system` | Busca componentes existentes no design system do arquivo |
| `get_libraries` | Lista bibliotecas de componentes disponíveis |
| `list_shader_effects` / `get_shader_effect` | Lista/inspeciona efeitos de shader aplicados |
| `list_shader_fills` / `get_shader_fill` | Lista/inspeciona preenchimentos shader |

**Como pedir:** cola URL do frame/node do Figma (ex: `figma.com/design/ABC123/...?node-id=1-2`) e diz o que quer — "implementa esse componente em React", "tira print disso", "lista as cores usadas".

## Escrever no Figma (código → Figma)

| Tool | Uso |
|---|---|
| `use_figma` | Executa JS no contexto do arquivo — criar/editar/deletar nodes, layout, fills, variáveis, variantes. Motor genérico de escrita |
| `create_new_file` | Cria arquivo Figma/FigJam/Slides novo em branco |
| `generate_figma_design` | Gera design completo a partir de descrição/código |
| `generate_diagram` | Gera diagrama (fluxograma, arquitetura, ERD, sequência) direto em FigJam via Mermaid |
| `upload_assets` / `download_assets` | Sobe ou baixa imagens/assets do arquivo |
| `export_video` | Exporta prototype/animação como vídeo |

**Como pedir:** "cria uma tela de login no Figma baseada nesse componente React", "gera diagrama da arquitetura desse fluxo de auth".

## Code Connect (ligar componente Figma ↔ componente de código)

| Tool | Uso |
|---|---|
| `get_code_connect_map` / `add_code_connect_map` | Lê/grava mapeamento node Figma → arquivo de código |
| `get_context_for_code_connect` | Contexto extra pra gerar o mapeamento |
| `get_code_connect_suggestions` | Sugestões automáticas de mapeamento |
| `send_code_connect_mappings` | Envia mapeamentos gerados de volta pro Figma |

**Como pedir:** "cria Code Connect pro componente Button entre Figma e `src/components/Button.tsx`".

## Utilitário

| Tool | Uso |
|---|---|
| `whoami` | Confirma qual conta Figma está autenticada |

## Fluxo típico

1. Cola link do Figma (frame, componente, ou arquivo inteiro).
2. Pede ação em português normal — "implementa isso em Next.js", "mostra como tá esse frame", "sincroniza com o Figma".
3. Claude escolhe a tool certa (não precisa nomear tool manualmente) e carrega skill se preciso.
4. Pra escrever de volta no Figma, ação é irreversível-ish — confirma antes se for mudança grande em arquivo compartilhado.

## Erros comuns
- "no MCP figma" → autorização não feita, precisa autorizar via configurações claude.ai ou `/mcp`.
- Tool falha sem skill carregada → sempre deixa Claude carregar skill antes (não pula esse passo).
