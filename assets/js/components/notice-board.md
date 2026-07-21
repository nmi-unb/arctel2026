# Notice Board

Este documento explica a lógica implementada em `assets/js/components/notice-board.js`.

O componente monta o mural da seção `#avisos` da página inicial. Ele busca os dados em `assets/data/avisos.json`, escolhe quais avisos aparecem no painel principal, quais aparecem no painel de aula, quais vão para o histórico e atualiza tudo automaticamente a cada 60 segundos.

## Arquivos envolvidos

- `assets/js/components/notice-board.js`: contém toda a lógica de carregamento, classificação e renderização dos avisos.
- `assets/data/avisos.json`: contém os avisos cadastrados.
- `index.html`: contém a estrutura HTML onde o componente insere os avisos.
- `assets/css/components/notice-board.css`: define o layout visual do mural, badges e modal de histórico.
- `assets/js/pages/home-page.js`: chama `initNoticeBoard()` quando a página inicial é inicializada.

## Fluxo geral

1. `home-page.js` chama `initNoticeBoard()`.
2. `notice-board.js` procura no HTML o elemento com `data-notice-board`.
3. Se o elemento existir, o componente guarda referências para:
   - painel principal;
   - painel de aula;
   - texto de última atualização;
   - botão de histórico;
   - lista do modal de histórico.
4. O componente faz `fetch("./assets/data/avisos.json")`.
5. O JSON é filtrado para manter apenas avisos válidos.
6. Os avisos válidos são classificados entre atuais e arquivados.
7. O componente escolhe:
   - um aviso principal;
   - um aviso de aula, se houver;
   - a lista de histórico.
8. A tela é renderizada.
9. A cada 60 segundos, o JSON é carregado de novo e a tela é recalculada.

## Estrutura visual

No HTML, o mural tem duas colunas dentro de `data-notice-panel`:

- `data-notice-highlight`: coluna do aviso principal.
- `data-notice-aula`: coluna do aviso de aula.

Também existe uma faixa inferior com:

- `data-notice-updated`: texto com a última atualização.
- `notice-history-btn`: botão que abre o histórico.

O histórico fica em um modal separado, controlado por `data-notice-modal`.

## São dois painéis: como a informação de cada um é definida?

Na prática, o componente trabalha com duas áreas visuais:

1. Aviso principal
2. Aviso de aula

### 1. Aviso principal

O aviso principal vem da função `pickPrincipal(current)`.

Ela recebe os avisos considerados atuais, **descarta os que têm `dataInicio` e `dataFim`
válidos** (esses são avisos de aula — ver seção 2, eles não concorrem ao destaque principal) e
escolhe um único aviso entre os restantes usando esta regra:

1. maior `prioridade`;
2. em caso de empate, maior `dataPublicacao`;
3. se não houver nenhum aviso elegível, aparece a mensagem `Nenhum aviso disponível no momento.`

Por que descartar avisos de aula: `dataPublicacao` no futuro não impede um aviso de aparecer como
atual (ver seção "É possível agendar mensagens?" mais abaixo). Com 30 avisos de aula cadastrados,
prioridade empatada e `dataPublicacao` espalhada de agosto a novembro, o destaque principal sempre
escolheria a aula com a publicação mais distante no futuro — um evento isolado, sem contexto, meses
antes de acontecer. O destaque principal é para comunicados institucionais/vigentes; a aula
específica já tem sua própria coluna (`pickAula`).

No painel principal aparecem:

- badge do tipo do aviso;
- `titulo`;
- `mensagem`;
- `dataPublicacao`, quando existir e for uma data válida.

O painel principal não renderiza link, mesmo que o aviso tenha `link`.

### 2. Aviso de aula

O aviso de aula vem da função `pickAula(current, now)`.

Ela considera apenas avisos atuais que tenham:

- `dataInicio` válida;
- `dataFim` válida.

A escolha segue esta regra:

1. Se existir uma aula acontecendo agora, ela aparece como `Ao vivo agora`.
2. Se não houver aula ao vivo, aparece a próxima aula futura.
3. Se não houver aula ao vivo nem aula futura, o painel de aula fica oculto.

Uma aula é considerada ao vivo quando:

```text
dataInicio <= agora <= dataFim
```

Uma aula é considerada próxima quando:

```text
dataInicio > agora
```

Quando existe aula ao vivo, a mensagem exibida é:

```text
Até HH:MM
```

Quando existe aula futura, a mensagem exibida é:

```text
DD/MM/AAAA · HH:MM-HH:MM
```

O painel de aula pode renderizar um botão/link se o aviso tiver `link` e se a regra de exibição do link permitir.

## O painel pode virar uma coluna só?

Sim.

Quando não existe aviso de aula para mostrar, `data-notice-aula` fica com `hidden = true`.

Nesse caso, o painel recebe a classe:

```text
notice-board__panel--single
```

Essa classe faz o mural usar apenas uma coluna visual.

## Um mesmo aviso pode aparecer nos dois painéis?

Não.

`pickPrincipal` descarta explicitamente qualquer aviso com `dataInicio`+`dataFim` válidos (ver
seção 1), e só esses avisos entram em `pickAula`. Os dois painéis usam conjuntos de avisos
mutuamente exclusivos — um aviso de aula nunca aparece no destaque principal, e um aviso sem
horário nunca aparece na coluna de aula.

## O que é um aviso atual?

A classificação acontece em `classifyAvisos(avisos, now)`.

Um aviso é atual quando:

```text
ativo === true
```

e também:

```text
arquivarApos não existe
```

ou:

```text
arquivarApos > agora
```

Ou seja: `ativo` precisa ser `true`, e a data de arquivamento não pode ter passado.

## O que vai para o histórico?

Um aviso vai para o histórico quando:

```text
ativo === false
```

ou:

```text
arquivarApos <= agora
```

O histórico é exibido no modal aberto pelo botão `Ver histórico de avisos`.

Dentro do histórico, os avisos são ordenados por `dataPublicacao`, do mais recente para o mais antigo.

No histórico aparecem:

- badge do tipo;
- `titulo`;
- `mensagem`;
- `dataPublicacao`, quando válida;
- link, se existir e puder aparecer.

## É possível agendar mensagens?

Depende do que se entende por agendar.

### O que já é possível

É possível controlar datas relacionadas a aula, arquivamento e link:

- `dataInicio`: define quando uma aula começa.
- `dataFim`: define quando uma aula termina.
- `arquivarApos`: define quando o aviso sai dos avisos atuais e vai para o histórico.
- `exibirLinkAPartirDe`: define quando o link passa a aparecer.

Com isso, é possível cadastrar uma aula futura e deixar o painel de aula mostrar automaticamente a próxima aula.

Também é possível deixar um link escondido até um horário específico, por exemplo, liberar o link da aula apenas pouco antes do início.

### O que ainda não existe

Não existe uma regra de publicação futura do aviso.

O campo `dataPublicacao` é usado para exibir a data e desempatar prioridade, mas ele não impede o aviso de aparecer antes dessa data.

Portanto, se um aviso estiver com:

```json
"ativo": true
```

e ainda não tiver sido arquivado, ele pode aparecer como aviso atual mesmo que `dataPublicacao` esteja no futuro.

Para implementar agendamento real de publicação, o código precisaria considerar algo como:

```text
dataPublicacao <= agora
```

ou criar um campo novo, por exemplo:

```json
"publicarAPartirDe": "2026-08-04T07:45:00-03:00"
```

## Anatomia estrutural de um aviso

Um aviso no JSON segue esta estrutura geral:

```json
{
  "id": "aviso-001",
  "titulo": "Aula do Módulo 1 confirmada",
  "mensagem": "A aula do Módulo 1 está confirmada.",
  "tipo": "confirmacao",
  "dataPublicacao": "2026-07-20T09:00:00-03:00",
  "dataInicio": "2026-08-04T09:30:00-03:00",
  "dataFim": "2026-08-04T12:00:00-03:00",
  "link": null,
  "textoLink": null,
  "prioridade": 3,
  "ativo": true,
  "arquivarApos": "2026-08-04T12:00:00-03:00",
  "exibirLinkAPartirDe": "2026-08-04T07:45:00-03:00"
}
```

## Campos obrigatórios

Para um item do JSON ser considerado válido, ele precisa passar por `isValidAviso(aviso)`.

Campos obrigatórios:

- `id`: texto.
- `titulo`: texto.
- `mensagem`: texto.
- `tipo`: texto.
- `ativo`: booleano, ou seja, `true` ou `false`.

Se algum desses campos faltar ou tiver tipo errado, o aviso é ignorado.

## Campos opcionais

Campos opcionais, mas usados pela lógica:

- `dataPublicacao`: aparece na tela e ajuda a desempatar avisos de mesma prioridade.
- `dataInicio`: permite que o aviso entre na lógica de aula.
- `dataFim`: permite que o aviso entre na lógica de aula.
- `link`: endereço do botão/link.
- `textoLink`: texto exibido no botão/link.
- `prioridade`: peso usado para escolher o aviso principal.
- `arquivarApos`: data em que o aviso passa para o histórico.
- `exibirLinkAPartirDe`: data em que o link começa a aparecer.

## Tipos de aviso

Os tipos conhecidos ficam no objeto `BADGES`.

Tipos cadastrados no código:

- `confirmacao`: aparece como `Aula confirmada`.
- `ao_vivo`: aparece como `Ao vivo agora`.
- `alteracao`: aparece como `Alteração importante`.
- `alerta`: aparece como `Alerta`.
- `material`: aparece como `Material disponível`.
- `encerrado`: aparece como `Encerrado`.

Se um aviso tiver um `tipo` desconhecido, ele ainda pode ser renderizado, mas o badge cai no visual e texto de `alteracao`.

Observação: no painel de aula, o tipo visual não vem diretamente do campo `tipo` do JSON. O código força:

- `ao_vivo`, quando a aula está acontecendo agora;
- `confirmacao`, quando a aula é futura.

## Exemplo: aviso simples

Use este formato para um aviso geral que deve aparecer no painel principal, mas não no painel de aula:

```json
{
  "id": "aviso-material-001",
  "titulo": "Material disponível",
  "mensagem": "O material de apoio já pode ser consultado.",
  "tipo": "material",
  "dataPublicacao": "2026-07-21T09:00:00-03:00",
  "dataInicio": null,
  "dataFim": null,
  "link": "#modulos",
  "textoLink": "Ver módulos",
  "prioridade": 2,
  "ativo": true,
  "arquivarApos": null,
  "exibirLinkAPartirDe": null
}
```

Mesmo com `link`, esse aviso não mostrará botão no painel principal. O link só poderá aparecer no histórico.

## Exemplo: aula futura

Use este formato para uma aula que deve aparecer no painel de aula:

```json
{
  "id": "aula-modulo-2",
  "titulo": "Aula do Módulo 2 confirmada",
  "mensagem": "A aula do Módulo 2 está confirmada.",
  "tipo": "confirmacao",
  "dataPublicacao": "2026-07-21T09:00:00-03:00",
  "dataInicio": "2026-08-11T09:30:00-03:00",
  "dataFim": "2026-08-11T12:00:00-03:00",
  "link": "https://exemplo.com/sala",
  "textoLink": "Entrar na aula",
  "prioridade": 3,
  "ativo": true,
  "arquivarApos": "2026-08-11T12:00:00-03:00",
  "exibirLinkAPartirDe": "2026-08-11T09:00:00-03:00"
}
```

Antes de `exibirLinkAPartirDe`, a aula pode aparecer no painel de aula sem botão.

Depois desse horário, o botão aparece.

Durante a aula, o badge muda para `Ao vivo agora`.

Depois de `arquivarApos`, o aviso sai dos atuais e entra no histórico.

## Exemplo: aviso encerrado manualmente

Use `ativo: false` para mandar um aviso diretamente para o histórico:

```json
{
  "id": "aviso-resolvido-001",
  "titulo": "Instabilidade resolvida",
  "mensagem": "A instabilidade de acesso foi normalizada.",
  "tipo": "alerta",
  "dataPublicacao": "2026-07-21T09:00:00-03:00",
  "dataInicio": null,
  "dataFim": null,
  "link": null,
  "textoLink": null,
  "prioridade": 1,
  "ativo": false,
  "arquivarApos": null,
  "exibirLinkAPartirDe": null
}
```

## Regras de link

Um link aparece apenas se `link` existir.

Se `exibirLinkAPartirDe` estiver vazio, o link pode aparecer imediatamente.

Se `exibirLinkAPartirDe` tiver uma data válida, o link só aparece quando:

```text
agora >= exibirLinkAPartirDe
```

Links externos começando com `http://` ou `https://` abrem em nova aba com:

```html
target="_blank"
rel="noopener noreferrer"
```

Links internos, como `#modulos`, abrem na mesma página.

## Última atualização

O texto de última atualização vem da maior `dataPublicacao` encontrada entre todos os avisos válidos, incluindo avisos atuais e arquivados.

Ele não indica necessariamente a hora em que o arquivo JSON foi carregado. Indica a data de publicação mais recente cadastrada nos avisos.

## Datas e fuso horário

Todas as comparações (`ao vivo`, `próxima aula`, arquivamento, liberação de link) são feitas
entre objetos `Date`, que representam um instante absoluto (timestamp UTC internamente) — não
uma string formatada. Por isso a comparação em si já funciona igual para qualquer usuário, em
qualquer país: `dataInicio <= agora <= dataFim` dá o mesmo resultado em São Paulo, Lisboa ou Tóquio,
**desde que a data cadastrada tenha o offset de fuso explícito**.

As datas exibidas na tela (formatação, não comparação) usam o fuso:

```text
America/Sao_Paulo
```

Por isso o formato **obrigatório** no JSON é ISO com fuso explícito:

```text
2026-08-04T09:30:00-03:00
```

`parseDate(value)` valida isso: se a string não terminar em `Z` ou em um offset (`±HH:MM`), a
data é **rejeitada** (tratada como ausente) e um aviso é registrado no console com o prefixo
`[notice-board]`. Motivo: uma data sem offset, tipo `"2026-08-04T09:30:00"`, é interpretada pelo
`new Date()` do navegador na hora **local de quem está vendo a página**, não em Brasília — isso
faria a mesma aula parecer "ao vivo" em horários diferentes pra usuários em fusos diferentes.

Limite que a validação não resolve: a comparação depende do relógio do próprio dispositivo do
usuário (`new Date()` local). Se esse relógio estiver errado, o "agora" calculado também erra —
isso é inerente a qualquer lógica 100% client-side, sem servidor de hora, e está fora do que este
componente estático consegue garantir.

### Aviso de fuso para quem não está em Brasília

Forçar a formatação pra `America/Sao_Paulo` resolve o cálculo, mas cria um problema de
comunicação: um usuário em outro fuso vê a mesma hora renderizada e, sem contexto, tende a lê-la
como sendo a hora local dele — o que é falso.

`VIEWER_IS_IN_ANOTHER_TIMEZONE` compara o fuso do navegador
(`Intl.DateTimeFormat().resolvedOptions().timeZone`) com `America/Sao_Paulo`. Quando diferem,
`withBrasiliaNote(texto)` acrescenta o sufixo `(horário de Brasília)` em toda data/hora exibida
(aviso principal, aula ao vivo/próxima, "Última atualização" e histórico). Para quem já está em
Brasília, o sufixo não aparece — a hora mostrada já é a hora local dele, o aviso seria ruído.

## O que acontece se o JSON falhar?

Se o `fetch` falhar, se o JSON não for uma lista ou se nenhum aviso válido for encontrado, o componente chama `renderFallback(refs)`.

Nesse fallback:

- aparece `Nenhum aviso disponível no momento.`;
- o painel de aula fica oculto;
- o texto de última atualização fica vazio;
- o botão de histórico fica desabilitado;
- o histórico fica vazio.

O erro também é registrado no console do navegador com o prefixo:

```text
[notice-board] falha ao carregar avisos:
```

## Cuidados ao cadastrar avisos

- Use `ativo: true` para avisos que devem concorrer aos painéis atuais.
- Use `ativo: false` para avisos resolvidos ou encerrados manualmente.
- Use `arquivarApos` para arquivamento automático.
- Use `dataInicio` e `dataFim` apenas quando o aviso representar uma aula ou evento com horário.
- Use `prioridade` maior para avisos mais importantes.
- Não confie em `dataPublicacao` para esconder avisos futuros, porque essa regra ainda não existe.
- Se quiser que um link apareça só perto da aula, use `exibirLinkAPartirDe`.
- Mantenha `id` único para facilitar manutenção, mesmo que o código atual não valide duplicidade.

## Resumo rápido

- O mural carrega `assets/data/avisos.json`.
- O painel principal mostra o aviso atual de maior prioridade.
- O painel de aula mostra a aula ao vivo ou a próxima aula futura.
- Avisos inativos ou vencidos por `arquivarApos` vão para o histórico.
- Links podem ser liberados por horário com `exibirLinkAPartirDe`.
- Não há agendamento real de publicação por `dataPublicacao`.
- O componente recarrega os avisos automaticamente a cada 60 segundos.
