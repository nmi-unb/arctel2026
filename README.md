# Site Lideranças NMI

Site estático do curso de Lideranças do NMI (Núcleo de Estudos em Políticas, Direito, Economia e Tecnologia das Comunicações).

## Estrutura

```text
index.html
assets/
  css/        estilos (base, layout, components, pages)
  js/         scripts (app.js + components/pages)
  img/        logos, favicon, backgrounds
  data/       dados carregados via JS (ex.: avisos.json)
docs/         documentação técnica do projeto
```

## Mural de Avisos

A seção "Avisos" (`#avisos`) é alimentada por `assets/data/avisos.json`, lido por
`assets/js/components/notice-board.js`. Pra adicionar, editar ou encerrar um aviso,
basta mexer nesse JSON — nenhum HTML/JS precisa ser tocado.

Cada aviso é um objeto com estes campos:

| Campo | Obrigatório | Descrição |
| --- | --- | --- |
| `id` | sim | identificador único do aviso (string) |
| `titulo` | sim | título curto exibido em destaque |
| `mensagem` | sim | texto do aviso |
| `tipo` | sim | badge visual: `confirmacao`, `ao_vivo`, `alteracao`, `alerta`, `material` ou `encerrado` |
| `ativo` | sim | `true`/`false` — `false` manda o aviso direto pro histórico |
| `dataPublicacao` | não | ISO 8601 com fuso (ex. `2026-08-04T10:00:00-03:00`); usado para ordenar e para "Última atualização" |
| `dataInicio` / `dataFim` | não | se os dois estiverem presentes, o aviso vira uma "aula": aparece na coluna direita como **ao vivo** (se `agora` está entre as duas) ou **próxima aula** (se `dataInicio` é futuro) |
| `link` / `textoLink` | não | URL e texto do botão/link do aviso |
| `exibirLinkAPartirDe` | não | ISO 8601; o `link` só aparece a partir desse instante (útil pra liberar a transmissão minutos antes da aula) |
| `prioridade` | não | número — **maior valor ganha** o destaque principal; empate é resolvido pelo `dataPublicacao` mais recente |
| `arquivarApos` | não | ISO 8601; quando essa data passa, o aviso sai do mural principal e cai no histórico (modal "Ver histórico de avisos"), mesmo com `ativo: true` |

Um aviso só some do mural quando `ativo: false` ou quando `arquivarApos` já passou — em
nenhum dos dois casos ele é apagado do arquivo, só reclassificado para o histórico na
hora da renderização. O JS reavalia tudo a cada 60s (verifica localmente, sem exigir
reload) e, se o JSON falhar ou vier vazio, cai num estado de fallback discreto sem
quebrar o resto da página.
