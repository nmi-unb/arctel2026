## Prompt — Construção do MVP 1.0 do `.notice_editor`

````md
# Solicitação de construção — MVP 1.0 do `.notice_editor`

## 1. Objetivo geral

Construa o **MVP 1.0** de uma aplicação local em **Python 3**, utilizando a biblioteca **Flet**, para administrar os avisos exibidos pelo componente `notice-board.js` do site.

O nome e diretório da aplicação serão:

```text
.notice_editor/
````

Essa aplicação é uma ferramenta privada de manutenção e não pertence ao corpo público do site. Sua finalidade é permitir que o usuário edite dados estruturados sem inserir informações diretamente no código-fonte do front-end.

O MVP 1.0 corresponde à **FASE 1**:

* editar `assets/data/avisos.json`;
* consultar os módulos e as aulas em modo somente leitura;
* selecionar referências de módulo, aula e tipo de link sem digitação manual;
* validar o contrato de dados;
* aplicar as alterações no estado interno da interface;
* salvar as alterações em `avisos.json`;
* não editar os arquivos dos módulos;
* não executar publicação ou deploy.

A edição dos links e demais informações dos módulos ficará para a **FASE 2**.

---

## 2. Contexto obrigatório do projeto

Antes de criar ou alterar qualquer arquivo:

1. confirme que o trabalho está sendo realizado na branch:

   ```text
   maintenance
   ```

2. leia e considere as instruções existentes nas pastas:

   ```text
   .codex/
   .claude/
   ```

3. leia o arquivo:

   ```text
   tree_focada.txt
   ```

   Esse arquivo resume a estrutura atual do repositório.

4. leia o arquivo:

   ```text
   _docs/dFilter.py
   ```

   Ele define quais arquivos e diretórios participam do deploy.

5. considere que, por padrão, qualquer diretório cujo nome comece com `.` não participa do deploy.

6. leia integralmente:

   ```text
   NOTICE_LINK_INTEGRATION.md
   ```

   Esse documento é a fonte de verdade para os contratos de integração entre:

   * `avisos.json`;
   * arquivos dos módulos;
   * aulas;
   * links;
   * `module-data-service.js`;
   * `notice-board.js`.

O contrato determina, entre outros pontos, que os avisos de aula devem referenciar os links por meio de `moduleId`, `lessonId` e `linkType`, sem armazenar diretamente a URL da aula em `avisos.json`. 

---

## 3. Regras de comportamento durante a implementação

### 3.1. Testes executados pela IA

Não execute loops de testes, testes repetitivos ou processos automatizados de tentativa e erro quando a funcionalidade puder ser verificada manualmente pelo usuário.

Nesses casos:

1. implemente a funcionalidade;
2. informe exatamente como o usuário deverá testá-la;
3. aguarde o retorno do usuário.

Testes adicionais executados pelo agente devem ocorrer somente quando:

* o usuário relatar um erro silencioso;
* a origem do erro não puder ser identificada pela inspeção direta;
* houver necessidade real de observar o estado intermediário da aplicação;
* o usuário solicitar explicitamente a execução dos testes.

Não crie loops de execução da interface Flet.

Não mantenha a aplicação aberta aguardando interação durante a implementação.

---

### 3.2. Arquivos Python públicos e privados

Ao criar um arquivo `.py` que será importado por outro módulo:

1. todas as funções, classes, variáveis e constantes internas devem começar com `_`;

2. todos os elementos públicos devem ser declarados explicitamente ao final do arquivo:

   ```python
   __all__ = [
       "ElementoPublico",
       "funcao_publica",
       "CONSTANTE_PUBLICA",
   ]
   ```

3. `__all__` deve conter somente os elementos efetivamente destinados ao uso por outros módulos;

4. não coloque funções privadas em `__all__`;

5. evite tornar público qualquer elemento que não precise ser importado externamente.

Quando um arquivo Python não for destinado à importação por outros módulos, sua primeira linha deverá ser:

```python
# ignore file
```

Essa regra se aplica, por exemplo, a scripts isolados, utilitários executáveis ou arquivos auxiliares que não façam parte da API interna da aplicação.

---

### 3.3. Arquivos `__init__.py`

Crie um arquivo `__init__.py` vazio em cada diretório Python que funcione como pacote.

Os arquivos devem permanecer completamente vazios.

Não adicione:

* imports;
* comentários;
* docstrings;
* `__all__`;
* metadados;
* lógica de inicialização.

Existe uma aplicação separada que posteriormente recriará esses arquivos de forma detalhada.

---

## 4. Gerenciamento do projeto com UV

O uso de **UV** é obrigatório.

Toda instalação, sincronização ou execução deve ser feita por meio de comandos como:

```bash
uv sync
uv add flet
uv run python ...
uv run flet ...
```

Não utilize diretamente:

```bash
pip install
python -m pip
poetry
pipenv
conda
```

Antes de alterar `pyproject.toml`, inspecione o arquivo existente.

---

## 5. Cuidados com `flet create`

O comando:

```bash
uv run flet create
```

pode substituir arquivos existentes, especialmente:

```text
README.md
pyproject.toml
```

Portanto:

1. não execute `uv run flet create` na raiz do repositório;
2. não execute esse comando antes de verificar se o diretório de destino já contém arquivos;
3. não permita que ele sobrescreva o `pyproject.toml` principal do projeto;
4. caso seja realmente necessário utilizá-lo, execute somente dentro de um diretório isolado e vazio;
5. prefira criar manualmente a estrutura da aplicação quando isso evitar sobrescritas;
6. preserve integralmente os arquivos existentes do repositório.

A aplicação deverá ficar dentro de:

```text
.notice_editor/
```

---

## 6. Atualização automática do Flet

Considere o comportamento atual do Flet:

* ao final de `main()`, a página é atualizada automaticamente;
* ao final de cada event handler, a página ou o ancestral isolado mais próximo também é atualizado automaticamente;
* não é necessário chamar `page.update()` na maioria dos handlers.

Portanto:

1. não use `page.update()` indiscriminadamente;

2. não mantenha chamadas herdadas de padrões antigos do Flet 0.x sem necessidade;

3. use atualização explícita somente quando o comportamento exigir;

4. para operações em lote, poderá ser utilizado:

   ```python
   ft.context.disable_auto_update()
   ```

   seguido de uma única atualização explícita;

5. documente brevemente qualquer ponto em que o auto-update seja desativado.

---

## 7. Escopo funcional do MVP 1.0

### 7.1. Arquivo editável

O MVP deverá editar exclusivamente:

```text
assets/data/avisos.json
```

A aplicação deverá:

* carregar os avisos existentes;
* preservar campos válidos previstos no contrato;
* criar avisos;
* editar avisos;
* duplicar avisos;
* desativar avisos;
* reativar avisos;
* excluir avisos definitivamente mediante confirmação;
* alterar a posição física dos avisos;
* ordenar avisos por publicação;
* ordenar avisos por prioridade;
* validar todos os registros antes da gravação;
* salvar o array completo novamente em `avisos.json`.

---

### 7.2. Arquivos consultados em modo somente leitura

A aplicação deverá consultar, sem alterar:

```text
assets/data/modulos/index.json
assets/data/modulos/modulo-1.json
...
assets/data/modulos/modulo-11.json
```

Esses arquivos serão utilizados para:

* listar os módulos;
* mostrar seus títulos;
* listar as aulas de cada módulo;
* mostrar número, título, início e fim da aula;
* verificar os links disponíveis;
* validar `moduleId`;
* validar `lessonId`;
* validar `linkType`;
* informar se o link correspondente existe ou está `null`.

O MVP não poderá salvar alterações nesses arquivos.

---

### 7.3. Sem publicação

Não deverá existir nenhuma ação denominada:

```text
Publicar
Deploy
Enviar para produção
Git push
```

A aplicação deverá se limitar às ações:

```text
Editar
Aplicar
Salvar arquivo
```

Significados:

* **Editar:** abrir ou colocar um aviso no formulário de edição;
* **Aplicar:** transferir os dados válidos do formulário para o estado interno da aplicação;
* **Salvar arquivo:** gravar o estado atual da aplicação em `assets/data/avisos.json`.

O deploy continuará sendo realizado por ferramentas externas já existentes.

---

## 8. Resolução da raiz do repositório

Use exclusivamente `pathlib` para manipular caminhos.

Não utilize concatenação manual de strings para construir caminhos.

Exemplo permitido:

```python
PROJECT_ROOT / "assets" / "data" / "avisos.json"
```

Exemplo não desejado:

```python
str(PROJECT_ROOT) + "/assets/data/avisos.json"
```

A aplicação está localizada em `.notice_editor`, dentro do próprio repositório. Portanto, deverá ser criada uma estratégia centralizada e testável para localizar a raiz real do projeto.

A resolução da raiz não deve depender exclusivamente do diretório de execução atual.

A raiz poderá ser validada verificando a existência de arquivos como:

```text
tree_focada.txt
assets/data/avisos.json
assets/data/modulos/index.json
```

Se a raiz não puder ser encontrada:

* não grave nenhum arquivo;
* apresente uma mensagem clara na interface;
* informe quais marcadores não foram encontrados.

---

## 9. Organização de caminhos e constantes

Use a seguinte base estrutural para caminhos e valores compartilhados:

```text
.notice_editor/
└── src/
    └── services/
        └── generic/
            ├── __init__.py
            ├── paths/
            │   ├── __init__.py
            │   ├── root.py
            │   └── target.py
            └── values/
                ├── __init__.py
                └── constants.py
```

Responsabilidades esperadas:

### `root.py`

Responsável por:

* identificar a raiz do repositório;
* validar os marcadores da raiz;
* expor o caminho da raiz;
* não conhecer detalhes específicos de cada arquivo de dados.

### `target.py`

Responsável por construir caminhos derivados, como:

* `avisos.json`;
* índice de módulos;
* diretório de módulos;
* arquivos individuais de módulo;
* documentos necessários para diagnóstico.

### `constants.py`

Responsável por constantes compartilhadas, por exemplo:

* tipos de aviso permitidos;
* tipos de link permitidos;
* nomes de campos;
* opções de fonte de link;
* formatos de exibição;
* valores padrão;
* textos reutilizados pela interface.

Não transforme `constants.py` em um arquivo com regras de negócio.

---

## 10. Modelos de estrutura de dados

Use a seguinte organização:

```text
.notice_editor/
└── src/
    └── services/
        └── dataStructure/
            ├── __init__.py
            ├── notice.py
            ├── module.py
            ├── lesson.py
            └── LessonLinks.py
```

Mantenha exatamente o nome `dataStructure`, conforme solicitado.

Mantenha inicialmente o nome de arquivo `LessonLinks.py`, mas registre em comentário técnico ou documentação que ele não segue o padrão `snake_case` normalmente recomendado para módulos Python. Não o renomeie sem autorização.

### `notice.py`

Deverá representar todos os campos previstos no contrato de `avisos.json`.

### `module.py`

Deverá representar um módulo consultado nos arquivos de módulos.

### `lesson.py`

Deverá representar uma aula pertencente a um módulo.

### `LessonLinks.py`

Deverá representar:

```text
teams
youtubeLive
youtubeRecorded
```

Os modelos devem:

* converter dados vindos do JSON;
* preservar os nomes externos definidos no contrato;
* permitir uma representação Python consistente;
* realizar ou delegar validações;
* evitar espalhar dicionários não tipados pela aplicação.

Escolha uma solução coerente entre:

* `dataclasses`;
* classes tradicionais tipadas;
* outro mecanismo já adotado pelo projeto.

Não introduza uma dependência externa apenas para modelagem sem necessidade clara.

---

## 11. Contrato de `avisos.json`

Cada aviso poderá conter os campos:

```text
id
titulo
mensagem
tipo
dataPublicacao
dataInicio
dataFim
moduleId
lessonId
linkType
staticLink
url
textoLink
prioridade
ativo
arquivarApos
exibirLinkAPartirDe
```

Campos obrigatórios:

```text
id
titulo
mensagem
tipo
dataPublicacao
ativo
```

Tipos de aviso permitidos:

```text
confirmacao
ao_vivo
alteracao
alerta
material
encerrado
```

Tipos de link de aula permitidos:

```text
teams
youtubeLive
youtubeRecorded
```

O editor deve respeitar integralmente o contrato descrito em `NOTICE_LINK_INTEGRATION.md`. 

---

## 12. Fonte do link

A interface deverá apresentar uma seleção explícita de fonte:

```text
Sem link
Referência de aula
Link estático
URL legada
```

Entretanto:

* `URL legada` poderá ser visualizada e migrada;
* novos avisos não deverão ser criados com `url`;
* o modo legado deve ser claramente identificado como pendente de migração.

Um aviso poderá utilizar no máximo uma fonte:

1. `moduleId` + `lessonId` + `linkType`;
2. `staticLink`;
3. `url`, apenas em registro legado;
4. nenhuma fonte.

Nunca permita que duas fontes sejam aplicadas simultaneamente.

Ao trocar o tipo de fonte, limpe do estado editável os campos incompatíveis, mas somente depois de confirmação quando isso causar perda de informação preenchida.

---

## 13. Seleção assistida de módulo e aula

Quando a fonte escolhida for `Referência de aula`, apresente:

1. seletor de módulo;
2. seletor de aula;
3. seletor do tipo de link;
4. indicador de disponibilidade do link.

O usuário não deverá precisar digitar manualmente:

```text
modulo-2
aula-3
youtubeLive
```

O valor salvo deverá seguir o padrão:

```json
{
  "moduleId": "modulo-2",
  "lessonId": "aula-3",
  "linkType": "youtubeLive"
}
```

Não utilize zeros à esquerda.

Os identificadores deverão ser derivados dos dados reais dos módulos, respeitando o contrato. 

---

## 14. Ausência de link

Quando a combinação de módulo, aula e tipo de link for válida, mas o valor da URL estiver `null`:

* não bloqueie a ação `Aplicar`;
* não bloqueie o salvamento;
* apresente um alerta visual;
* informe que o aviso será exibido no site sem botão enquanto o link não existir.

Isso deve refletir o comportamento de `notice-board.js`, no qual a ausência do link não impede a exibição do aviso. 

Uma combinação estruturalmente inválida, como módulo inexistente ou aula inexistente, deverá bloquear a aplicação da alteração.

---

## 15. Datas e fuso horário

Utilize datas ISO 8601 com offset explícito.

O fuso padrão será:

```text
America/Sao_Paulo
```

A serialização esperada deverá seguir o formato:

```text
2026-08-21T08:00:00-03:00
```

A interface poderá exibir datas em formato brasileiro:

```text
21/08/2026, 08:00
```

Mas o arquivo JSON deverá preservar o padrão ISO com offset.

Validações obrigatórias:

* `dataPublicacao` válida;
* `dataInicio` e `dataFim` devem estar ambas preenchidas ou ambas ausentes;
* `dataFim` deve ser posterior a `dataInicio`;
* `arquivarApos`, quando preenchido, deve ser uma data válida;
* `exibirLinkAPartirDe`, quando preenchido, deve ser uma data válida.

Validações recomendadas como aviso, e não necessariamente como bloqueio:

* `arquivarApos` anterior ao término da aula;
* `exibirLinkAPartirDe` posterior ao término da aula;
* data de publicação posterior ao arquivamento.

---

## 16. IDs dos avisos

O campo `id` deve ser:

* obrigatório;
* não vazio;
* único no array;
* estável;
* legível;
* preferencialmente semântico.

Exemplos:

```text
aula-modulo-2-parte-3
cronograma-confirmado-2026
material-modulo-4
```

A aplicação poderá sugerir um ID com base no título, mas:

* o usuário deverá poder revisá-lo antes da primeira aplicação;
* a aplicação não deverá alterar automaticamente IDs existentes;
* ao editar um ID já salvo, apresente um aviso de confirmação;
* IDs duplicados deverão bloquear a ação `Aplicar`.

---

## 17. Interface principal

Organize a interface em três regiões funcionais.

### 17.1. Lista de avisos

Exiba, no mínimo:

* posição;
* status;
* título;
* tipo;
* data de publicação;
* início da aula, quando houver;
* prioridade;
* origem do link;
* indicação de legado.

Ofereça filtros:

```text
Todos
Ativos
Histórico
Aulas
Informativos
Com link
Sem link
Legados
```

---

### 17.2. Formulário de edição

Organize os campos em grupos:

```text
Identificação
Conteúdo
Classificação
Agendamento
Fonte do link
Arquivamento
```

Ações do formulário:

```text
Aplicar
Cancelar edição
Limpar formulário
```

`Aplicar` deverá:

1. validar o formulário;
2. mostrar os erros encontrados;
3. atualizar apenas o estado interno;
4. não gravar imediatamente o arquivo;
5. marcar a aplicação como contendo alterações não salvas.

---

### 17.3. Pré-visualização

Apresente uma prévia aproximada do aviso contendo:

* badge;
* título;
* mensagem;
* datas;
* texto do link;
* indicação de botão oculto quando o link não estiver disponível.

Não é necessário reproduzir perfeitamente o CSS do site no MVP.

A prévia deve permitir identificar:

* títulos excessivamente longos;
* mensagens extensas;
* ausência de texto de link;
* status;
* datas inconsistentes;
* link indisponível.

---

## 18. Estado de alterações não salvas

A aplicação deverá distinguir:

```text
Estado carregado do arquivo
Estado alterado internamente
Estado salvo no arquivo
```

Após qualquer ação que altere o estado interno, apresente um indicador como:

```text
Alterações não salvas
```

Ao tentar:

* fechar a janela;
* recarregar o arquivo;
* trocar a raiz do projeto;
* descartar a edição;
* substituir o estado em memória;

apresente uma confirmação quando existirem alterações não salvas.

---

## 19. Salvamento e confirmação

Não implemente sistema de backups automáticos.

O projeto já está versionado com Git e possui pequena magnitude. Backups adicionais são considerados desnecessários para este MVP.

Ao clicar em `Salvar arquivo`, apresente obrigatoriamente uma janela de confirmação com mensagem equivalente a:

```text
Esta ação sobrescreverá assets/data/avisos.json.

Antes de continuar, recomenda-se criar um commit com o estado atual do
repositório, para que seja possível restaurá-lo posteriormente.

Deseja realmente salvar as alterações?
```

Ações:

```text
Cancelar
Salvar mesmo assim
```

Somente após confirmação:

1. valide novamente o estado completo;
2. serialize todo o array;
3. grave `avisos.json`;
4. recarregue o arquivo gravado uma única vez para confirmar que o JSON é sintaticamente válido;
5. atualize o indicador de alterações não salvas.

Essa releitura única faz parte da segurança da operação e não deve se transformar em loop de testes.

Não crie:

* diretório de backup;
* cópia com timestamp;
* histórico paralelo;
* arquivo temporário permanente;
* integração automática com Git.

---

## 20. Preservação e alteração da ordem

Preserve a ordem física atual do array por padrão.

Ofereça explicitamente:

```text
Ordenar por publicação
Ordenar por prioridade
Mover para cima
Mover para baixo
```

Regras:

* as ordenações só alteram o estado interno até o usuário salvar;
* antes de ordenar todo o conjunto, solicite confirmação;
* `Mover para cima` e `Mover para baixo` devem atuar sobre o aviso selecionado;
* não reordene automaticamente durante o carregamento;
* não reordene automaticamente ao editar prioridade ou publicação;
* preserve uma ordenação estável em caso de empate.

---

## 21. Desativação e exclusão

A ação principal para retirar um aviso da exibição deverá ser:

```text
Desativar
```

Ela deverá alterar:

```json
"ativo": false
```

Também ofereça:

```text
Reativar
```

A exclusão definitiva poderá existir, mas deverá:

* ficar em ação secundária;
* exigir confirmação explícita;
* informar que o registro será removido do JSON;
* recomendar commit antes do salvamento;
* alterar apenas o estado interno até `Salvar arquivo`.

---

## 22. Diagnóstico e migração de URLs legadas

Crie uma visão ou seção de diagnóstico que identifique avisos com o campo:

```text
url
```

Apresente:

* quantidade de registros legados;
* ID;
* título;
* URL atual;
* possível destino da migração.

Permita migrar um registro legado para:

```text
Referência de aula
Link estático
```

Ao concluir a migração no estado interno:

* remova `url`;
* preencha somente a nova fonte escolhida;
* valide a exclusividade da fonte;
* não altere `notice-board.js`;
* não remova ainda o suporte legado do JavaScript.

A remoção do suporte a `url` em `notice-board.js` ocorrerá somente em outra tarefa, após todos os registros serem migrados. 

---

## 23. Estrutura sugerida da aplicação

Adapte a estrutura somente quando houver justificativa concreta baseada no repositório:

```text
.notice_editor/
├── README.md
├── pyproject.toml
├── src/
│   ├── main.py
│   ├── assets/
│   ├── models/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── dataStructure/
│   │   │   ├── __init__.py
│   │   │   ├── notice.py
│   │   │   ├── module.py
│   │   │   ├── lesson.py
│   │   │   └── LessonLinks.py
│   │   ├── generic/
│   │   │   ├── __init__.py
│   │   │   ├── paths/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── root.py
│   │   │   │   └── target.py
│   │   │   └── values/
│   │   │       ├── __init__.py
│   │   │       └── constants.py
│   │   ├── notice_repository.py
│   │   ├── module_repository.py
│   │   ├── validation_service.py
│   │   └── migration_service.py
│   └── views/
│       ├── __init__.py
│       ├── main_view.py
│       ├── notice_list.py
│       ├── notice_form.py
│       ├── notice_preview.py
│       ├── confirmation_dialog.py
│       └── diagnostics_view.py
└── storage/
    ├── data/
    └── temp/
```

Todos os `__init__.py` devem ser criados vazios.

Não presuma que toda a estrutura precise ser criada imediatamente. Implemente somente os arquivos necessários ao MVP, mantendo separação clara entre:

* interface;
* modelos;
* leitura e escrita;
* caminhos;
* validação;
* migração.

---

## 24. Repositórios e serviços

### `notice_repository.py`

Responsável por:

* carregar `avisos.json`;
* verificar se o conteúdo raiz é um array;
* converter registros para o modelo de aviso;
* serializar os modelos;
* salvar o arquivo após confirmação da interface;
* não conter controles Flet.

### `module_repository.py`

Responsável por:

* carregar `index.json`;
* carregar os arquivos de módulos;
* localizar módulo;
* localizar aula;
* consultar disponibilidade de links;
* operar somente em leitura na FASE 1.

### `validation_service.py`

Responsável por:

* validar um aviso;
* validar o conjunto completo;
* detectar IDs duplicados;
* validar exclusividade da fonte de link;
* verificar referências de módulo e aula;
* separar erros bloqueantes de alertas.

### `migration_service.py`

Responsável por:

* identificar registros com `url`;
* auxiliar a conversão para `staticLink`;
* auxiliar a conversão para referência de aula;
* não alterar arquivos automaticamente.

---

## 25. Tratamento de erros

Apresente mensagens compreensíveis para:

* arquivo inexistente;
* JSON malformado;
* raiz não localizada;
* índice de módulos inválido;
* módulo ausente;
* aula ausente;
* linkType inválido;
* campo obrigatório vazio;
* ID duplicado;
* erro de permissão durante gravação;
* arquivo alterado externamente desde o carregamento.

Não silencie exceções relevantes.

Não apresente traceback bruto ao usuário final na interface.

Registre detalhes técnicos no terminal ou mecanismo de log adotado pelo projeto, preservando uma mensagem simples na interface.

---

## 26. Alterações externas no arquivo

Registre, no momento do carregamento, alguma referência simples ao estado do arquivo, como:

* horário de modificação;
* tamanho;
* ou hash.

Antes de salvar, verifique se `avisos.json` foi alterado externamente.

Quando houver alteração externa:

* não sobrescreva imediatamente;
* apresente uma confirmação específica;
* ofereça cancelar e recarregar;
* informe que salvar poderá substituir alterações feitas fora do editor.

Não implemente merge automático no MVP.

---

## 27. README da aplicação

Crie um README específico dentro de `.notice_editor`.

Ele deverá explicar:

* finalidade da ferramenta;
* escopo da FASE 1;
* limitações;
* pré-requisitos;
* uso obrigatório de UV;
* comando de sincronização;
* comando para iniciar;
* arquivos que podem ser alterados;
* arquivos consultados em modo somente leitura;
* ausência de deploy;
* recomendação de commit antes de salvar;
* regras sobre URLs legadas;
* estrutura principal.

Não substitua o README da raiz do repositório.

---

## 28. Comandos esperados

A aplicação deverá poder ser preparada e executada com comandos equivalentes a:

```bash
cd .notice_editor
uv sync
uv run flet run src/main.py
```

Ajuste o comando final conforme a estrutura e a versão efetivamente configuradas no `pyproject.toml`.

Não informe um comando que não tenha correspondência com a configuração criada.

---

## 29. Etapas de implementação

Implemente em etapas pequenas.

### Etapa 1 — inspeção

* confirmar branch;
* ler `.codex`;
* ler `.claude`;
* ler `tree_focada.txt`;
* ler `_docs/dFilter.py`;
* ler `NOTICE_LINK_INTEGRATION.md`;
* inspecionar `avisos.json`;
* inspecionar `index.json`;
* inspecionar pelo menos um arquivo de módulo;
* inspecionar o `pyproject.toml` existente;
* apresentar um resumo objetivo antes de alterar arquivos.

### Etapa 2 — base do projeto

* criar `.notice_editor`;
* configurar UV;
* criar estrutura mínima;
* criar `__init__.py` vazios;
* implementar caminhos;
* implementar constantes.

### Etapa 3 — modelos

* implementar `Notice`;
* implementar `Module`;
* implementar `Lesson`;
* implementar `LessonLinks`;
* garantir `__all__`.

### Etapa 4 — acesso aos dados

* implementar leitura de avisos;
* implementar leitura de módulos;
* implementar validação;
* implementar consulta de links.

### Etapa 5 — interface básica

* lista de avisos;
* formulário;
* seleção de módulo e aula;
* prévia;
* estado de alterações não salvas.

### Etapa 6 — operações

* criar;
* editar;
* duplicar;
* aplicar;
* desativar;
* reativar;
* excluir;
* mover;
* ordenar.

### Etapa 7 — gravação

* confirmação com recomendação de commit;
* validação final;
* detecção de alteração externa;
* gravação;
* releitura única;
* mensagem de sucesso ou erro.

### Etapa 8 — diagnóstico legado

* identificar `url`;
* mostrar registros;
* migrar para referência de aula ou `staticLink`.

### Etapa 9 — documentação

* concluir README;
* informar comandos;
* listar limitações;
* fornecer roteiro de teste manual.

Não avance para a FASE 2.

---

## 30. Critérios de aceite do MVP 1.0

O MVP será considerado concluído quando:

1. iniciar por UV;
2. localizar corretamente a raiz do repositório;
3. carregar `avisos.json`;
4. carregar módulos e aulas em modo somente leitura;
5. listar avisos;
6. criar e editar avisos;
7. validar campos obrigatórios;
8. impedir IDs duplicados;
9. impedir múltiplas fontes de link;
10. permitir selecionar módulo e aula sem digitação manual;
11. alertar, sem bloquear, quando o link da aula estiver ausente;
12. mostrar prévia;
13. preservar a ordem física por padrão;
14. permitir mover registros;
15. permitir ordenar por publicação;
16. permitir ordenar por prioridade;
17. permitir desativar e reativar;
18. confirmar exclusões;
19. detectar URLs legadas;
20. auxiliar a migração das URLs legadas;
21. manter alterações apenas em memória após `Aplicar`;
22. gravar somente após `Salvar arquivo`;
23. mostrar a confirmação recomendando um commit;
24. não criar backups automáticos;
25. não editar arquivos de módulos;
26. não implementar deploy;
27. não executar testes em loop;
28. manter todos os `__init__.py` vazios;
29. declarar APIs públicas por meio de `__all__`;
30. prefixar elementos internos com `_`;
31. iniciar arquivos não importáveis com `# ignore file`;
32. usar `pathlib` para todos os caminhos;
33. respeitar as instruções encontradas em `.codex` e `.claude`;
34. não incluir `.notice_editor` no deploy.

---

## 31. Retorno esperado do agente

Antes da implementação, retorne:

1. resumo do que foi encontrado no repositório;
2. riscos ou incompatibilidades identificados;
3. estrutura mínima que será criada;
4. arquivos existentes que serão alterados;
5. arquivos novos que serão criados;
6. ordem das etapas.

Depois de cada etapa, retorne somente:

* arquivos criados;
* arquivos alterados;
* decisões técnicas relevantes;
* roteiro curto de teste manual;
* pendências para a próxima etapa.

Relatórios mais extensos ou arquivos de acompanhamento eventualmente produzidos deverão ser gravados exclusivamente em:

```text
.report/
```

Esse diretório já existe na raiz do projeto principal e deve ser utilizado como destino centralizado para relatórios, diagnósticos, levantamentos, inventários e registros técnicos gerados durante a implementação.

Regras para `.report/`:

* não criar relatórios em `.notice_editor/`;
* não criar relatórios na raiz do repositório;
* não usar `.report/` para arquivos necessários ao funcionamento lógico da aplicação;
* não importar módulos Python a partir de `.report/`;
* tratar seu conteúdo como privado, explicativo e descartável;
* usar `pathlib` para construir seus caminhos;
* não criar um novo diretório de relatórios quando `.report/` já existir;
* não alterar relatórios anteriores sem necessidade ou autorização;
* informar no retorno o caminho de cada relatório criado.

Não é obrigatório produzir um arquivo de relatório após cada etapa. Quando o retorno textual for suficiente, responda diretamente ao usuário sem criar arquivos adicionais.

Não execute testes repetitivos quando o usuário puder testar a interface manualmente.

Ao final do MVP, retorne:

1. estrutura final;
2. comandos com UV;
3. funcionalidades concluídas;
4. limitações da FASE 1;
5. roteiro completo de validação manual;
6. itens explicitamente reservados para a FASE 2;
7. relação dos eventuais relatórios produzidos em `.report/`.


```
```
