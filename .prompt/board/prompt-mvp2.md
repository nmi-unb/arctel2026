# Solicitação de implementação — FASE 2 do `.notice_editor`

## 1. Objetivo geral

Implemente a **FASE 2** da aplicação local `.notice_editor`, construída em Python 3 com Flet e gerenciada obrigatoriamente por UV.

A FASE 1 já está concluída e funcional. Ela permite editar `assets/data/avisos.json`, consultar módulos e aulas em modo somente leitura, validar referências, trabalhar com `liveLinks`, migrar URLs legadas e salvar os avisos com confirmação.

A FASE 2 deverá ampliar a aplicação para permitir a edição controlada dos arquivos:

```text
assets/data/modulos/modulo-1.json
assets/data/modulos/modulo-2.json
...
assets/data/modulos/modulo-11.json
````

A implementação deverá preservar integralmente as funcionalidades já concluídas na FASE 1.

Não implemente publicação, deploy, `git commit`, `git push` ou alteração automática de branch.

---

## 2. Estado atual da aplicação

Antes de alterar qualquer arquivo, leia integralmente:

```text
.report/notice-editor/2026-07-26.md
```

Esse relatório descreve:

* estrutura final da FASE 1;
* funcionalidades concluídas;
* limitações conhecidas;
* atualizações pós-MVP;
* suporte a `liveLinks`;
* arquivos existentes;
* metodologia de validação;
* itens reservados para a FASE 2.

Considere o relatório como referência do estado atual, mas confirme cada informação diretamente nos arquivos do repositório antes de realizar alterações.

A FASE 1 já possui, entre outros elementos:

```text
.notice_editor/src/app_state.py

.notice_editor/src/services/dataStructure/
├── notice.py
├── module.py
├── lesson.py
└── LessonLinks.py

.notice_editor/src/services/
├── notice_repository.py
├── module_repository.py
├── validation_service.py
└── migration_service.py

.notice_editor/src/views/
├── main_view.py
├── notice_list.py
├── notice_form.py
├── notice_preview.py
├── confirmation_dialog.py
└── diagnostics_view.py
```

Não recrie a aplicação do zero.

Evolua a estrutura existente.

---

## 3. Regras obrigatórias de preparação

Antes de implementar:

1. confirme que a branch atual é:

   ```text
   maintenance
   ```

2. leia e considere as skills e instruções existentes em:

   ```text
   .codex/
   .claude/
   ```

3. leia:

   ```text
   tree_focada.txt
   ```

4. leia:

   ```text
   _docs/dFilter.py
   ```

5. leia o contrato atualizado de integração:

   ```text
   .docs/NOTICE_LINK_INTEGRATION.md
   ```

6. inspecione:

   ```text
   assets/data/modulos/index.json
   ```

7. inspecione todos os arquivos:

   ```text
   assets/data/modulos/modulo-1.json
   ...
   assets/data/modulos/modulo-11.json
   ```

8. inspecione:

   ```text
   assets/js/services/module-data-service.js
   assets/js/components/notice-board.js
   ```

9. inspecione os arquivos atuais da aplicação `.notice_editor`.

10. confirme as correções manuais realizadas após a FASE 1.

Não faça alterações antes de apresentar um diagnóstico inicial objetivo.

---

## 4. Regras de comportamento durante a implementação

### 4.1. Testes executados pela IA

Não execute loops de testes ou processos repetitivos quando o usuário puder verificar manualmente o comportamento da interface.

Quando a funcionalidade puder ser testada manualmente:

1. implemente;
2. informe o roteiro de teste;
3. aguarde o retorno do usuário.

Testes adicionais executados pelo agente devem ocorrer apenas quando:

* o usuário relatar erro silencioso;
* a inspeção direta não permitir identificar a causa;
* houver necessidade real de verificar estado intermediário;
* o usuário solicitar explicitamente.

São permitidas verificações únicas e não interativas, por exemplo:

```text
carregar um JSON
validar uma estrutura
instanciar uma view uma única vez
serializar e reler um arquivo sandbox
verificar sintaxe Python
```

Não mantenha a aplicação Flet aberta em loop para teste automatizado.

---

### 4.2. Arquivos Python públicos e privados

Ao criar ou alterar um arquivo `.py` importado por outros módulos:

* funções, classes, variáveis e constantes internas devem começar com `_`;
* elementos públicos devem ser declarados ao final em:

```python
__all__ = [
    "ElementoPublico",
]
```

Não inclua elementos privados em `__all__`.

Quando um arquivo Python não for importado por outro módulo, sua primeira linha deverá ser:

```python
# ignore file
```

---

### 4.3. Arquivos `__init__.py`

Todos os `__init__.py` devem permanecer completamente vazios.

Não adicione:

* imports;
* comentários;
* docstrings;
* `__all__`;
* lógica.

Quando um novo pacote for criado, crie o respectivo `__init__.py` vazio.

---

## 5. UV obrigatório

Toda instalação, sincronização e execução deverá usar UV.

Comandos esperados:

```bash
cd .notice_editor
uv sync
uv run flet run src/main.py
```

Não utilize:

```text
pip
python -m pip
poetry
pipenv
conda
```

Não execute `flet create` na raiz do repositório.

Não permita que `README.md` ou `pyproject.toml` existentes sejam sobrescritos.

---

## 6. Regras relativas ao Flet

Considere o auto-update da versão atual do Flet utilizada pelo projeto.

Não chame `page.update()` indiscriminadamente.

Utilize atualização explícita apenas quando realmente necessária.

Caso use:

```python
ft.context.disable_auto_update()
```

documente tecnicamente o motivo e faça apenas uma atualização final explícita.

Não tente resolver nesta fase as limitações já identificadas sobre:

* tamanho mínimo da janela;
* interceptação confiável do fechamento da janela;
* tema escuro.

Preserve o tema claro atual, salvo decisão posterior expressa do usuário.

---

# ESCOPO FUNCIONAL DA FASE 2

## 7. Objetivo funcional principal

A aplicação deverá passar a editar os dados dos módulos e das aulas.

O usuário deverá conseguir:

* selecionar um módulo;
* visualizar seus dados;
* editar o título do módulo;
* visualizar suas aulas;
* selecionar uma aula;
* editar os dados da aula;
* editar os links da aula;
* editar os materiais da aula;
* aplicar alterações somente em memória;
* salvar o arquivo `modulo-N.json` correspondente;
* detectar conflitos com avisos existentes;
* preservar as funcionalidades da FASE 1.

---

## 8. Arquivos editáveis na FASE 2

A aplicação poderá editar exclusivamente:

```text
assets/data/avisos.json

assets/data/modulos/modulo-1.json
...
assets/data/modulos/modulo-11.json
```

O arquivo:

```text
assets/data/modulos/index.json
```

não deverá ser diretamente editado por formulário no primeiro incremento da FASE 2.

Primeiro analise sua função real e escolha uma destas políticas:

### Política preferencial

Atualização automática e restrita do índice quando um campo efetivamente duplicado entre o índice e o módulo for alterado.

### Política alternativa

Manter o índice somente leitura e bloquear alterações que provoquem inconsistência.

Não escolha silenciosamente.

Após analisar o formato real, documente qual política será adotada e por quê.

Não permita edição livre e arbitrária do JSON do índice.

---

## 9. Campos editáveis do módulo

A interface deverá permitir editar, conforme o contrato real encontrado:

```text
modulo
titulo
lessons
```

O número do módulo:

```text
modulo
```

deverá ser tratado inicialmente como identificador estrutural e não deverá ser livremente editável.

Exiba-o como somente leitura.

Não permita renumerar módulos na primeira versão da FASE 2.

O campo:

```text
titulo
```

poderá ser editado.

Se o título também estiver presente em `index.json`, aplique a política definida para sincronização do índice.

---

## 10. Campos editáveis da aula

A aplicação deverá permitir editar:

```text
numero
titulo
dataInicio
dataFim
links
materials
```

O campo `numero` deverá ser tratado com cautela.

Na primeira versão da FASE 2:

* exiba o número da aula;
* permita alteração somente se a validação cruzada estiver implementada;
* antes de alterar, verifique referências em `avisos.json`;
* mostre claramente que a alteração muda o `lessonId`;
* solicite confirmação;
* atualize as referências dos avisos somente mediante ação explícita do usuário.

Não altere automaticamente referências sem confirmação.

---

## 11. Links da aula

A interface deverá permitir editar:

```text
links.teams
links.youtubeLive
links.youtubeRecorded
```

Cada campo poderá conter:

```text
URL válida
null
```

A interface deverá distinguir:

```text
não informado
informado e válido
informado e inválido
```

Não use string vazia no JSON final quando o contrato utiliza `null`.

Ao aplicar:

* campo vazio deve ser convertido para `null`;
* URL preenchida deve ser validada;
* a URL deve preservar o valor digitado sem normalizações destrutivas.

Não tente acessar a URL pela internet para validar sua existência.

Valide apenas sua estrutura.

---

## 12. Materiais da aula

Antes de implementar o formulário, levante o formato real utilizado em:

```text
materials.professor
materials.replacementCourses
```

Não presuma que os elementos são apenas strings.

Inspecione todos os módulos e identifique:

* campos presentes;
* tipos;
* variações;
* valores nulos;
* arrays vazios;
* objetos aninhados;
* eventuais contratos inconsistentes.

Com base nesse diagnóstico, implemente modelos tipados compatíveis com os dados reais.

O formulário deverá permitir:

* listar materiais;
* adicionar material;
* editar material;
* remover material;
* reordenar materiais;
* preservar campos desconhecidos válidos quando possível.

Não descarte silenciosamente propriedades ainda não conhecidas pelo editor.

Se houver mais de um formato incompatível, interrompa essa parte da implementação e apresente uma proposta de normalização antes de alterar os arquivos.

---

## 13. Arquitetura de estados

A aplicação deverá distinguir pelo menos:

```text
avisos carregados
avisos alterados em memória
avisos salvos

módulo carregado
módulo alterado em memória
módulo salvo
```

Não use um único indicador genérico quando houver alterações independentes.

Apresente indicadores como:

```text
Avisos: alterações não salvas
Módulo 3: alterações não salvas
```

O usuário poderá editar avisos e módulos na mesma sessão.

O salvamento de avisos não deverá salvar módulos automaticamente.

O salvamento de módulo não deverá salvar avisos automaticamente.

---

## 14. Navegação principal

A interface deverá passar a ter duas áreas funcionais principais:

```text
Avisos
Módulos e aulas
```

Pode ser utilizado:

* `NavigationRail`;
* abas;
* seletor segmentado;
* outro componente compatível com a estrutura atual.

Não reconstrua toda a interface sem necessidade.

Preserve o painel retrátil de avisos já implementado quando estiver na área de avisos.

Na área de módulos, ofereça:

```text
Lista de módulos
Dados do módulo
Lista de aulas
Formulário da aula
Pré-visualização ou resumo
```

---

## 15. Tela de módulos

A tela deverá permitir:

1. selecionar um módulo;
2. visualizar o número e o título;
3. editar o título;
4. listar as aulas;
5. selecionar uma aula;
6. criar uma nova aula;
7. duplicar uma aula;
8. editar uma aula;
9. remover uma aula com confirmação;
10. mover aula para cima;
11. mover aula para baixo;
12. ordenar aulas por número;
13. ordenar aulas por data;
14. aplicar alterações em memória;
15. salvar o módulo selecionado.

A ordem física do array `lessons` deverá ser preservada por padrão.

Não ordene automaticamente ao carregar ou editar.

---

## 16. Criação de aula

Ao criar uma nova aula:

* sugira automaticamente o próximo número disponível;
* permita alterar antes de aplicar;
* valide duplicidade;
* sugira um título inicial como:

```text
Aula N
```

* mantenha links como `null`;
* inicialize materiais conforme o contrato real;
* não grave o arquivo imediatamente.

A criação deve alterar apenas o estado interno até `Salvar módulo`.

---

## 17. Duplicação de aula

Ao duplicar:

* gere novo número não utilizado;
* ajuste o título de maneira identificável;
* preserve datas somente mediante decisão explícita;
* preserve links somente mediante confirmação;
* preserve materiais por padrão;
* não aplique automaticamente referências em avisos.

Antes de implementar, escolha um comportamento claro para datas e links e documente-o no retorno inicial.

Preferência recomendada:

```text
materiais: copiar
datas: limpar
links: limpar
```

---

## 18. Remoção de aula

Antes de remover uma aula, pesquise em memória todos os avisos que utilizem:

```text
moduleId
lessonId
```

Se houver referências, apresente uma janela contendo:

* quantidade de avisos afetados;
* IDs;
* títulos;
* status ativo/inativo;
* tipo de link usado.

Ofereça:

```text
Cancelar
Remover aula e manter avisos inválidos
Remover aula e desativar avisos
```

Não remova automaticamente os avisos.

A opção de manter avisos inválidos deverá exigir confirmação adicional.

A opção de atualizar os avisos para outra aula não precisa ser implementada no primeiro incremento, salvo se a arquitetura atual permitir isso com segurança.

---

## 19. Alteração do número da aula

Alterar:

```text
numero: 2
```

pode mudar:

```text
lessonId: aula-2
```

Antes de aplicar essa alteração:

1. localize avisos que usam o `lessonId` antigo;
2. apresente a lista;
3. ofereça:

```text
Cancelar
Alterar apenas a aula
Alterar a aula e atualizar os avisos em memória
```

A atualização dos avisos deverá:

* acontecer apenas em memória;
* marcar avisos como não salvos;
* exigir salvamento separado de `avisos.json`;
* não salvar automaticamente os dois arquivos.

Mostre claramente quando o sistema ficar em estado temporariamente inconsistente porque um arquivo foi salvo e o outro não.

---

## 20. Alteração de datas

Utilize o mesmo componente e padrão criado na FASE 1:

```text
data
hora
fuso
```

O fuso padrão será:

```text
-03:00
```

As datas deverão ser serializadas em ISO 8601 com offset.

Validações:

* `dataInicio` obrigatória para aula válida, se o contrato real assim exigir;
* `dataFim` obrigatória quando `dataInicio` existir;
* `dataFim` posterior a `dataInicio`;
* formatos válidos;
* número de aula único dentro do módulo.

Caso os dados reais contenham aulas sem data, preserve essa possibilidade somente se ela já estiver prevista no contrato real.

Não imponha uma regra incompatível com os arquivos existentes.

---

## 21. Validação cruzada com avisos

Implemente um serviço específico para analisar relações entre módulos, aulas e avisos.

Sugestão de arquivo:

```text
.notice_editor/src/services/reference_service.py
```

Responsabilidades:

* encontrar avisos de um módulo;
* encontrar avisos de uma aula;
* detectar módulo inexistente;
* detectar aula inexistente;
* detectar `linkType` ausente na estrutura;
* detectar link `null`;
* verificar efeitos da alteração de número;
* verificar efeitos da remoção de aula;
* produzir dados para confirmação na interface.

Não coloque essa lógica diretamente nas views.

---

## 22. Evolução dos modelos

Revise os modelos atuais:

```text
module.py
lesson.py
LessonLinks.py
```

Adapte-os ao contrato real da FASE 2.

Crie modelos adicionais apenas se necessários, por exemplo:

```text
ProfessorMaterial
ReplacementCourse
LessonMaterials
ModuleIndexEntry
```

Os nomes finais deverão refletir o formato real encontrado.

Não crie classes especulativas antes de inspecionar os dados.

Todos os modelos deverão:

* suportar `from_dict`;
* suportar `to_dict`;
* preservar o contrato externo;
* preservar campos desconhecidos quando necessário;
* ter tipagem coerente;
* declarar APIs públicas em `__all__`.

---

## 23. Repositório de módulos

Evolua:

```text
module_repository.py
```

Ele deverá passar a suportar:

```text
load_module
load_all_modules
save_module
has_module_changed_externally
reload_module
validate_module_file
```

Os nomes reais podem ser adaptados à convenção existente.

A gravação deverá:

1. validar o módulo completo;
2. serializar o objeto;
3. sobrescrever somente o arquivo correspondente;
4. reler uma única vez;
5. confirmar JSON válido;
6. atualizar o fingerprint;
7. não alterar outros módulos;
8. não criar backup automático.

Use `pathlib`.

Não use concatenação manual de caminhos.

---

## 24. Detecção de alterações externas

A mesma política usada para `avisos.json` deverá ser aplicada a cada arquivo de módulo.

No carregamento, registre fingerprint usando a estratégia existente.

Antes de salvar, verifique se o arquivo foi alterado externamente.

Quando houver alteração externa, apresente:

```text
Cancelar
Recarregar módulo
Sobrescrever mesmo assim
```

Não implemente merge automático.

Não use o fingerprint de um módulo para outro.

---

## 25. Salvamento de módulo

A ação deverá se chamar:

```text
Salvar módulo
```

Antes de sobrescrever, apresente obrigatoriamente:

```text
Esta ação sobrescreverá:

assets/data/modulos/modulo-N.json

Antes de continuar, recomenda-se criar um commit com o estado atual do
repositório.

Deseja realmente salvar as alterações?
```

Ações:

```text
Cancelar
Salvar mesmo assim
```

Após a confirmação:

1. valide o módulo;
2. valide referências cruzadas;
3. mostre alertas não bloqueantes;
4. detecte alteração externa;
5. grave o módulo;
6. releia uma única vez;
7. atualize o estado salvo;
8. mantenha alterações de avisos separadas.

---

## 26. Atualização de `index.json`

Analise o conteúdo real de:

```text
assets/data/modulos/index.json
```

Determine:

* quais campos são duplicados;
* quais são usados por `module-data-service.js`;
* se o título do módulo precisa ser sincronizado;
* se o caminho do arquivo é fixo;
* se o índice pode ser derivado dos módulos.

A partir disso, implemente uma política segura.

### Requisitos mínimos

* nenhuma inconsistência silenciosa;
* nenhuma edição manual livre do JSON;
* confirmação antes de sobrescrever;
* detecção de alteração externa;
* salvamento separado ou claramente acoplado ao módulo;
* documentação da regra no README.

Caso o índice precise ser atualizado junto com o módulo, a janela de confirmação deverá informar explicitamente os dois arquivos que serão sobrescritos.

---

## 27. Validação do módulo

Crie ou expanda a validação para verificar:

### Módulo

* objeto raiz válido;
* número válido;
* título obrigatório;
* `lessons` como array;
* módulo compatível com o nome do arquivo;
* módulo compatível com o índice.

### Aula

* número válido;
* número único no módulo;
* título obrigatório;
* datas válidas;
* fim posterior ao início;
* `links` válido;
* `materials` válido;
* campos obrigatórios conforme contrato real.

### Links

* somente chaves permitidas;
* URL válida ou `null`;
* string vazia convertida para `null`;
* sem tipos incorretos.

### Materiais

* arrays válidos;
* objetos válidos;
* campos obrigatórios;
* preservação de propriedades reconhecidas;
* rejeição de formato estruturalmente inválido.

Separe:

```text
erros bloqueantes
alertas
```

---

## 28. Diagnóstico geral

Adicione uma área de diagnóstico de módulos capaz de identificar:

* módulos ausentes;
* módulos não listados no índice;
* entradas do índice sem arquivo;
* números de módulo incompatíveis;
* aulas duplicadas;
* datas inválidas;
* referências inválidas em avisos;
* links de aula ausentes;
* materiais fora do contrato;
* avisos que apontam para aulas inexistentes.

Não altere arquivos automaticamente a partir do diagnóstico.

Ofereça navegação para o módulo, aula ou aviso afetado quando viável.

---

## 29. Remoção do suporte legado a `url`

Antes de alterar `notice-board.js`, confirme novamente:

```text
0 registros com url em assets/data/avisos.json
```

Também pesquise se há:

* exemplos;
* fixtures;
* documentação;
* arquivos históricos ativos;
* código Python que ainda dependa de `url`.

Somente após confirmação e autorização do usuário, poderá ser realizada uma etapa separada para:

* remover o tratamento de `aviso.url` em `notice-board.js`;
* remover `url` do modelo `Notice`;
* remover `url` da validação;
* remover a opção legado do formulário;
* atualizar a documentação.

Não faça essa remoção automaticamente junto com a edição de módulos.

Trate-a como subfase final e independente.

---

## 30. Estrutura sugerida

A estrutura poderá evoluir para algo semelhante a:

```text
.notice_editor/
└── src/
    ├── app_state.py
    ├── services/
    │   ├── dataStructure/
    │   │   ├── module.py
    │   │   ├── lesson.py
    │   │   ├── LessonLinks.py
    │   │   └── novos modelos de materials, se necessários
    │   ├── module_repository.py
    │   ├── notice_repository.py
    │   ├── validation_service.py
    │   ├── reference_service.py
    │   └── generic/
    └── views/
        ├── main_view.py
        ├── module_view.py
        ├── module_list.py
        ├── module_form.py
        ├── lesson_list.py
        ├── lesson_form.py
        ├── lesson_preview.py
        └── module_diagnostics_view.py
```

Não crie todos esses arquivos obrigatoriamente.

Primeiro avalie a arquitetura atual.

Evite:

* arquivos excessivamente grandes;
* views com regras de negócio;
* serviços que dependam de Flet;
* duplicação do componente de datas;
* duplicação de validações;
* novos pacotes sem necessidade.

Todos os novos `__init__.py` deverão ser vazios.

---

## 31. Integração com `app_state.py`

Evolua o estado da aplicação para coordenar:

```text
avisos
módulos
módulo selecionado
aula selecionada
alterações não salvas de avisos
alterações não salvas por módulo
fingerprints
diagnósticos
referências cruzadas
```

Não transforme `app_state.py` em um arquivo monolítico.

Caso a complexidade cresça excessivamente, proponha uma divisão, por exemplo:

```text
NoticeState
ModuleState
EditorState
```

Não faça a divisão apenas por estética.

Faça-a se reduzir acoplamento e facilitar a manutenção.

---

## 32. Preservação de dados desconhecidos

Ao carregar e salvar módulos, não descarte silenciosamente campos desconhecidos existentes nos JSON.

Adote uma estratégia como:

```text
extra_fields
```

ou equivalente.

Antes de salvar, confirme que:

* campos conhecidos foram atualizados;
* campos desconhecidos permaneceram preservados;
* a ordem lógica principal não foi destruída sem necessidade.

A serialização não precisa preservar byte a byte a formatação original, mas deve preservar semanticamente os dados.

Use indentação consistente com os arquivos atuais.

---

## 33. Relatórios

Eventuais relatórios, diagnósticos extensos, levantamentos de contrato ou inventários deverão ser gravados exclusivamente em:

```text
.report/
```

Preferencialmente:

```text
.report/notice-editor/
```

Não crie relatórios:

* na raiz;
* dentro de `.notice_editor`;
* em `assets`;
* em `_docs`.

A pasta `.report` tem caráter privado e explicativo.

Não coloque nela arquivos necessários ao funcionamento lógico da aplicação.

Não é obrigatório criar relatório quando o retorno textual for suficiente.

---

## 34. README

Atualize:

```text
.notice_editor/README.md
```

Inclua:

* descrição da FASE 2;
* edição de módulos;
* arquivos editáveis;
* política do índice;
* salvamento separado de avisos e módulos;
* riscos de referências cruzadas;
* confirmação antes de sobrescrever;
* recomendação de commit;
* roteiro de teste manual;
* limitações;
* funcionalidades ainda não implementadas.

Preserve a documentação da FASE 1.

Não substitua o README da raiz.

---

# ETAPAS DE IMPLEMENTAÇÃO

## 35. Etapa 1 — diagnóstico

Antes de alterar arquivos, retorne:

1. estrutura encontrada;
2. diferenças em relação ao relatório;
3. correções manuais identificadas;
4. formato real de `index.json`;
5. formato real dos módulos;
6. formato real de `materials`;
7. dependências de `module-data-service.js`;
8. riscos de referência cruzada;
9. política proposta para `index.json`;
10. arquivos que serão criados;
11. arquivos que serão alterados;
12. ordem de implementação.

Se houver incompatibilidade estrutural relevante, interrompa e solicite decisão.

---

## 36. Etapa 2 — modelos

* revisar `Module`;
* revisar `Lesson`;
* revisar `LessonLinks`;
* modelar `materials`;
* preservar campos desconhecidos;
* criar ou adaptar métodos de serialização;
* atualizar `__all__`.

Retorne roteiro de teste manual ou verificação única apropriada.

---

## 37. Etapa 3 — repositório de módulos

* implementar gravação;
* fingerprint por módulo;
* releitura única;
* detecção de alteração externa;
* política de índice;
* erros compreensíveis.

Não alterar arquivos reais durante testes automatizados.

Utilize arquivo sandbox temporário quando necessário.

---

## 38. Etapa 4 — validação e referências

* validar módulo;
* validar aulas;
* validar links;
* validar materiais;
* mapear avisos relacionados;
* detectar efeitos de remoção e renumeração.

---

## 39. Etapa 5 — estado da aplicação

* incluir módulos editáveis;
* manter alterações separadas;
* coordenar seleção;
* coordenar diagnósticos;
* evitar regressões na FASE 1.

---

## 40. Etapa 6 — interface de módulos

* navegação Avisos/Módulos;
* lista de módulos;
* formulário do módulo;
* lista de aulas;
* formulário da aula;
* edição de links;
* edição de materiais;
* prévia ou resumo;
* indicadores de alterações.

---

## 41. Etapa 7 — operações de aula

* criar;
* duplicar;
* editar;
* aplicar;
* cancelar;
* remover;
* mover;
* ordenar;
* renumerar com análise de impacto.

---

## 42. Etapa 8 — salvamento

* confirmação;
* recomendação de commit;
* validação final;
* fingerprint;
* gravação;
* releitura única;
* atualização eventual do índice;
* mensagem de sucesso ou erro.

---

## 43. Etapa 9 — diagnóstico geral

* inconsistências do índice;
* módulos inválidos;
* aulas inválidas;
* referências quebradas;
* links ausentes;
* materiais inválidos.

---

## 44. Etapa 10 — documentação

* atualizar README;
* registrar limitações;
* roteiro de teste manual;
* relação de arquivos alterados;
* itens pendentes.

Não remova o suporte legado a `url` sem autorização específica.

---

# CRITÉRIOS DE ACEITE

## 45. Critérios de aceite da FASE 2

A FASE 2 será considerada concluída quando:

1. a aplicação continuar iniciando com UV;
2. as funcionalidades da FASE 1 permanecerem operacionais;
3. for possível navegar entre Avisos e Módulos;
4. os 11 módulos forem carregados;
5. for possível editar o título do módulo;
6. for possível listar e selecionar aulas;
7. for possível criar aula;
8. for possível editar aula;
9. for possível duplicar aula;
10. for possível remover aula com análise de impacto;
11. for possível mover aulas;
12. for possível ordenar aulas;
13. datas forem editadas no formato data/hora/fuso;
14. links Teams, YouTube Live e gravação forem editáveis;
15. campos vazios de links forem salvos como `null`;
16. materiais forem editáveis conforme o contrato real;
17. campos desconhecidos forem preservados;
18. números duplicados de aula forem bloqueados;
19. referências de avisos forem analisadas;
20. alteração de número de aula oferecer atualização dos avisos em memória;
21. alterações de avisos e módulos forem independentes;
22. o módulo só for gravado após `Salvar módulo`;
23. a confirmação recomendar commit;
24. alteração externa do módulo for detectada;
25. o arquivo salvo for relido uma única vez;
26. `index.json` seguir uma política explícita e segura;
27. diagnósticos identificarem inconsistências;
28. nenhum deploy for executado;
29. nenhum backup automático for criado;
30. nenhum teste em loop for executado;
31. `pathlib` for utilizado para caminhos;
32. `__init__.py` permanecerem vazios;
33. APIs públicas usarem `__all__`;
34. elementos privados começarem com `_`;
35. arquivos não importáveis começarem com `# ignore file`;
36. eventuais relatórios forem destinados a `.report/`;
37. o README for atualizado;
38. o suporte a `url` legado não for removido sem autorização.

---

## 46. Retorno esperado do agente

Antes da implementação, retorne:

1. resumo do estado atual;
2. correções manuais detectadas;
3. formato real dos módulos;
4. formato real dos materiais;
5. análise do índice;
6. riscos;
7. estrutura mínima proposta;
8. arquivos existentes que serão alterados;
9. arquivos novos que serão criados;
10. etapas de implementação.

Depois de cada etapa, retorne somente:

* arquivos criados;
* arquivos alterados;
* decisões técnicas relevantes;
* verificações únicas realizadas;
* roteiro curto de teste manual;
* pendências da próxima etapa;
* caminho de eventual relatório criado em `.report/`.

Ao final da FASE 2, retorne:

1. estrutura final;
2. comandos com UV;
3. funcionalidades concluídas;
4. política adotada para `index.json`;
5. regras de validação;
6. comportamento das referências cruzadas;
7. limitações;
8. roteiro completo de validação manual;
9. arquivos alterados;
10. relatórios eventualmente produzidos em `.report/`;
11. itens ainda dependentes de autorização, especialmente a remoção do suporte legado a `url`.

```


