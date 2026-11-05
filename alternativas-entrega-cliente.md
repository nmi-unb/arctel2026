# Alternativas de entrega para o cliente

Anotações de uma conversa sobre como entregar o site do curso de outra forma que não a hospedagem atual (GitHub Pages). O ponto de partida: o cliente talvez queira uma versão do site dentro do **Google Sites**, ou uma aplicação/arquivo externo.

Status: só discussão. Nada disso foi implementado nem testado.

## Contexto técnico

O site é HTML, CSS e JavaScript puros, sem build. Duas características pesam em qualquer alternativa que seja "um arquivo só":

- Os dados (módulos, avisos, calendário) são carregados por `fetch` de arquivos JSON.
- O JS usa ES modules (`type="module"`).

Os dois **não funcionam abrindo o `.html` com duplo clique** (`file://`): o navegador bloqueia. Por isso, qualquer versão "arquivo único" precisa antes embutir os dados e juntar os scripts no próprio arquivo.

A lista do que é publicado já existe em `_docs/dFilter.py` (`assets/`, `modulos/`, `index.html`, sem pastas privadas nem arquivos de convite). Qualquer geração automática deve partir dela.

## Pergunta a fazer ao cliente primeiro

Por que o Google Sites?

- **Pelo endereço ou pelo login institucional:** a opção 1 abaixo resolve.
- **Para ele mesmo conseguir editar o conteúdo:** a opção 1 não resolve, porque o conteúdo continua no código.
- **Porque "tudo precisa estar dentro do Sites":** só a opção 4 atende, e é a pior.

## Se for Google Sites

O Google Sites não aceita CSS nem JavaScript próprios na página. Ele tem o bloco "Incorporar", que mostra outro conteúdo dentro de uma moldura.

| # | Opção | Como fica | Pontos a conferir |
|---|---|---|---|
| 1 | **Incorporar o site já publicado** (recomendada) | Página do Sites com bloco "Incorporar → Por URL" apontando para o GitHub Pages, em tela cheia. Mantém animações, menu, acordeões e módulos. | O site precisa estar em `https://`. Em celular, a rolagem dentro da moldura pode ficar estranha. |
| 2 | **HTML único dentro do Sites** | Bloco "Incorporar" na aba de código, com o HTML autocontido colado. Não depende de hospedagem externa. | Há limite de tamanho no código colado; imagens precisam ser leves. Roda em moldura isolada. |
| 3 | **Sites só como vitrine** | Páginas nativas com texto e imagens, e botões que levam ao site real. | O Sites vira capa; a experiência real fica no site. |
| 4 | **Recriar tudo nativo no Sites** | Refazer página por página com os componentes do Sites. | Perde animações, calendário dinâmico e avisos. Pior opção. |

Recomendação: **opção 1**. Nada muda no site nem no fluxo de deploy. Antes de propor ao cliente, vale testar se o site abre dentro de uma moldura sem problemas.

## Se for um arquivo ou aplicação externa

| Formato | Navegação | Animação | Observação |
|---|---|---|---|
| **HTML único autocontido** | Mantém (menu, acordeões, módulos como seções do mesmo arquivo) | Mantém | Abre com duplo clique, em qualquer sistema, sem internet nem aviso de segurança. Recomendado. |
| **PDF** | Sumário, marcadores e links internos | Perde | Cada página vira uma ou mais páginas. Acordeões saem abertos. Bom para enviar ou imprimir. |
| **Pasta/zip com o site** | Mantém | Mantém | Só funciona se a pessoa rodar um servidor local. |
| **Vídeo (MP4/GIF)** | Só o roteiro gravado | Mantém | Não é clicável. Serve como demonstração. |
| **Slides (PPTX)** | Por slide, com links | Só efeitos simples | Dá mais trabalho e perde a fidelidade com o site. |

### HTML único: como seria

1. Juntar o JS num script só, sem módulos.
2. Embutir os JSON de módulos, avisos e calendário no arquivo.
3. Embutir imagens (base64) e inlinear o CSS.
4. Trocar a navegação entre página inicial e módulos por seções dentro do arquivo.
5. Rodar tudo por um comando, usando o filtro do `dFilter.py`.

O arquivo pode passar de vários MB por causa de imagens e fontes; comprimir as imagens ajuda.

## Executável (.exe)

Dá para empacotar o site num executável que abre o site funcionando. Não resolve o Google Sites: é só outra forma de entregar.

| Opção | Como funciona | Tamanho aproximado |
|---|---|---|
| Mini servidor + navegador (Python + PyInstaller) | `.exe` sobe um servidor local e abre o site no navegador padrão. Mais simples. | ~10–20 MB |
| Janela própria (pywebview ou Tauri) | Site numa janela de aplicativo, sem barra de endereço. Usa o WebView2 do Windows. | ~10–30 MB |
| Electron | Embute um navegador inteiro. | ~100 MB ou mais |

Limitações:

- Um `.exe` roda em um só sistema; Mac e Linux exigem outro build.
- Executável sem assinatura digital costuma disparar SmartScreen e antivírus, e muitos clientes corporativos bloqueiam. É o maior risco para cliente institucional.
- Atualizar o site exige gerar e enviar um `.exe` novo.
- Leva junto os dados reais (links do Teams, avisos, nomes), a menos que sejam trocados por exemplos.

Para entregar a cliente, o executável costuma ser pior que o HTML único.

## Portfólio

Separado do pedido do cliente: transformar o site em um portfólio.

- Copiar o site filtrado (`dFilter.py`) para uma pasta nova, sem reescrever arquivos, mantendo aspecto, funcionalidades e animações.
- Trocar dados reais por exemplos: links do Teams, avisos, nomes de professoras e convidadas. Pode ser necessário ter autorização para mostrar nomes reais.
- Opcional: página de apresentação com descrição, tecnologia usada e capturas de tela.
- Melhor como gerador (um comando no toolbox) do que como pasta fixa, para não ficar desatualizado.

## Resumo

1. Descobrir o motivo real do cliente querer o Google Sites.
2. Se for endereço ou login: **incorporar o site publicado** (opção 1).
3. Se for arquivo para entregar: **HTML único** e, se quiser, um **PDF** para leitura e impressão.
4. Executável só se o cliente pedir um programa para instalar.
