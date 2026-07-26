/**
 * Cria (ou ATUALIZA) um Google Form baseado no formulário de
 * "Extensão > Cadastrar Participantes" do SIGAA/UnB.
 *
 * COMO USAR:
 * 1. Acesse https://script.google.com e crie um novo projeto.
 * 2. Cole este código no arquivo Codigo.gs.
 * 3. Rode a função `criarOuAtualizarFormulario` (botão "Executar").
 * 4. Autorize o acesso quando solicitado (primeira vez).
 * 5. Os links aparecem em "Execução > Registros" (Logger).
 *
 * RE-RODAR: o ID do formulário fica salvo nas propriedades do script,
 * então rodar de novo LIMPA os campos e reconstrói TUDO no mesmo
 * formulário — ótimo para pequenas correções. Basta editar o código
 * abaixo e executar novamente.
 *
 * Para começar do zero (novo formulário), rode `resetarFormulario` uma vez.
 *
 * FLUXO POR PÁGINAS (com ramificação):
 *   Página 1 (Início): "Estrangeiro?"  ->  Não = página Brasileiro
 *                                          Sim = página Estrangeiro
 *   Página Brasileiro : CPF + UF        -> segue para Dados Pessoais
 *   Página Estrangeiro: Passaporte + País (CPLP) -> segue para Dados Pessoais
 *   Dados Pessoais -> Endereço -> Contato -> Autenticação -> Enviar
 */

const TITULO_FORM = 'Extensão - Cadastrar Participantes';

const DESCRICAO_FORM =
  'Realize um novo cadastro para poder inscrever o participante em ' +
  'algum dos cursos ou eventos de extensão oferecidos.\n\n' +
  'Observação: Será enviado um e-mail para o usuário com a senha gerada ' +
  'pelo sistema para acesso ao mesmo. Após realizar o login o participante ' +
  'poderá alterar a senha para uma de sua escolha.';

// 27 unidades federativas (Distrito Federal aparece como padrão no SIGAA)
const UFS = [
  'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará',
  'Distrito Federal', 'Espírito Santo', 'Goiás', 'Maranhão',
  'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará',
  'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro',
  'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima',
  'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'
];

// Países do CPLP (Brasil omitido porque esta página é só para estrangeiros;
// se quiser incluí-lo, é só adicionar 'Brasil' na lista).
const PAISES_CPLP = [
  'Angola', 'Cabo Verde', 'Guiné-Bissau', 'Guiné Equatorial',
  'Moçambique', 'Portugal', 'São Tomé e Príncipe', 'Timor-Leste'
];


function criarOuAtualizarFormulario() {
  const props = PropertiesService.getScriptProperties();
  let form = null;

  // Tenta reabrir o MESMO formulário de execuções anteriores.
  // O try/catch aqui cobre SÓ a abertura (openById) — de propósito.
  // Antes, a limpeza dos itens também estava dentro deste try/catch;
  // como o formulário tem ramificação (setGoToPage), apagar um item
  // que ainda é "destino" de outro lança um erro. Esse erro era
  // engolido pelo catch, o script achava que o ID salvo era inválido
  // e criava um formulário NOVO a cada execução — era o bug relatado.
  const idSalvo = props.getProperty('FORM_ID');
  if (idSalvo) {
    try {
      form = FormApp.openById(idSalvo);
    } catch (e) {
      form = null; // ID inválido (formulário foi excluído manualmente)
    }
  }

  if (form) {
    limparFormulario(form); // remove navegação e itens antigos, SEM engolir erros
  } else {
    form = FormApp.create(TITULO_FORM);
    props.setProperty('FORM_ID', form.getId());
  }

  form.setTitle(TITULO_FORM);
  form.setDescription(DESCRICAO_FORM);
  form.setCollectEmail(false); // usamos campo de e-mail próprio, como no SIGAA

  // ----- Validações reaproveitadas -----
  const validacaoEmail = FormApp.createTextValidation()
    .setHelpText('Informe um e-mail válido.')
    .requireTextIsEmail()
    .build();

  // Passaporte: aceita letras E números (sem espaços/símbolos)
  const validacaoPassaporte = FormApp.createTextValidation()
    .setHelpText('Use apenas letras e números (ex.: AB1234567).')
    .requireTextMatchesPattern('^[A-Za-z0-9]+$')
    .build();

  // ========== PÁGINA 1 - INÍCIO ==========
  form.addSectionHeaderItem()
    .setTitle('Identificação')
    .setHelpText('Selecione abaixo para direcionar o cadastro.');

  // Criamos o item de ramificação agora, mas definimos os destinos
  // depois de criar as páginas de destino.
  const estrangeiro = form.addMultipleChoiceItem()
    .setTitle('Estrangeiro?')
    .setRequired(true);

  // ========== PÁGINA "BRASILEIRO" ==========
  const pgBrasileiro = form.addPageBreakItem()
    .setTitle('Documento (Brasileiro)');

  form.addTextItem()
    .setTitle('CPF')
    .setHelpText('Somente números.')
    .setRequired(true);

  form.addListItem()
    .setTitle('UF')
    .setChoiceValues(UFS)
    .setRequired(true);

  // ========== PÁGINA "ESTRANGEIRO" ==========
  const pgEstrangeiro = form.addPageBreakItem()
    .setTitle('Documento (Estrangeiro)');

  form.addTextItem()
    .setTitle('Número do Passaporte')
    .setValidation(validacaoPassaporte)
    .setRequired(true);

  form.addListItem()
    .setTitle('País (CPLP)')
    .setChoiceValues(PAISES_CPLP)
    .setRequired(true);

  // ========== PÁGINA - DADOS PESSOAIS (comum) ==========
  const pgPessoais = form.addPageBreakItem()
    .setTitle('Dados Pessoais');

  form.addTextItem()
    .setTitle('Nome Completo')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Nome Social');

  form.addMultipleChoiceItem()
    .setTitle('Foi solicitado o uso do Nome Social nos documentos oficiais?')
    .setChoiceValues(['Sim', 'Não']);

  form.addDateItem()
    .setTitle('Data de Nascimento')
    .setRequired(true);

  // ========== PÁGINA - ENDEREÇO (comum) ==========
  form.addPageBreakItem().setTitle('Endereço');

  form.addTextItem()
    .setTitle('CEP')
    .setRequired(true)
    .setHelpText('Somente números (8 dígitos).');

  form.addTextItem().setTitle('Rua/Av.');
  form.addTextItem().setTitle('Número');
  form.addTextItem().setTitle('Bairro');
  form.addTextItem().setTitle('Complemento');
  form.addTextItem().setTitle('Município');

  // ========== PÁGINA - CONTATO (comum) ==========
  form.addPageBreakItem().setTitle('Contato');

  form.addTextItem()
    .setTitle('Telefone Fixo')
    .setHelpText('Ex.: (99) 9999-9999');

  form.addTextItem()
    .setTitle('Celular')
    .setRequired(true)
    .setHelpText('Ex.: (99) 99999-9999');

  // ========== PÁGINA - AUTENTICAÇÃO (comum) ==========
  form.addPageBreakItem().setTitle('Autenticação');

  form.addTextItem()
    .setTitle('E-mail')
    .setRequired(true)
    .setValidation(validacaoEmail);

  form.addTextItem()
    .setTitle('Confirmação de E-mail')
    .setHelpText('Digite o mesmo e-mail informado acima.')
    .setRequired(true)
    .setValidation(validacaoEmail);

  // ========== RAMIFICAÇÃO ==========
  // "Não" -> página Brasileiro | "Sim" -> página Estrangeiro
  estrangeiro.setChoices([
    estrangeiro.createChoice('Não', pgBrasileiro),
    estrangeiro.createChoice('Sim', pgEstrangeiro)
  ]);

  // Convergência: ao TERMINAR qualquer um dos dois ramos, ir para a
  // página "Dados Pessoais". É preciso definir isso EM CADA ramo — se
  // só um tiver destino, o outro "cai" no fluxo linear e a página
  // seguinte não é exibida corretamente (ex.: Dados Pessoais vazio).
  pgBrasileiro.setGoToPage(pgPessoais);   // após a seção Brasileiro
  pgEstrangeiro.setGoToPage(pgPessoais);  // após a seção Estrangeiro

  // Configuração da mensagem de conclusão do formulário
  form.setConfirmationMessage(
    'Sua manifestação de interesse foi registrada com sucesso!\n\n' +
    'Agradecemos pelo preenchimento do formulário e pelo interesse em participar do curso ' +
    '"Fortalecimento de Lideranças Regulatórias Femininas das Comunicações".\n\n' +
    'As informações sobre o curso estarão organizadas e atualizadas na página oficial:\n' +
    'https://nmi-unb.github.io/arctel2026/\n\n' +
    'Em breve, a coordenação encaminhará novas orientações às pessoas participantes.\n\n' +
    'Coordenação do Curso\n' +
    'CCOM-UnB — Centro de Políticas, Direito, Economia e Tecnologias das Comunicações da Universidade de Brasília'
  );

  // ========== LINKS ==========
  Logger.log('Editar formulário: ' + form.getEditUrl());
  Logger.log('Responder formulário: ' + form.getPublishedUrl());
}


/**
 * Remove TODOS os itens de um formulário existente, preparando-o para
 * ser reconstruído do zero.
 *
 * Antes de apagar, reseta qualquer navegação por página (setGoToPage e
 * escolhas com destino de página) para o padrão "continuar". Isso é
 * necessário porque o Forms recusa apagar um item que ainda é destino
 * de navegação de outro item — sem esse reset, a exclusão lança um
 * erro no meio do processo.
 */
function limparFormulario(form) {
  const itens = form.getItems();

  // 1) Neutraliza qualquer referência de navegação
  itens.forEach(function (item) {
    if (item.getType() === FormApp.ItemType.PAGE_BREAK) {
      item.asPageBreakItem().setGoToPage(FormApp.PageNavigationType.CONTINUE);
    }
    if (item.getType() === FormApp.ItemType.MULTIPLE_CHOICE) {
      const mc = item.asMultipleChoiceItem();
      const valoresSimples = mc.getChoices().map(function (c) {
        return c.getValue();
      });
      mc.setChoiceValues(valoresSimples); // remove qualquer destino de página
    }
  });

  // 2) Agora é seguro apagar todos os itens, do último para o primeiro
  for (let i = itens.length - 1; i >= 0; i--) {
    form.deleteItem(itens[i]);
  }
}


/**
 * Apaga a referência salva para que a próxima execução crie um
 * formulário NOVO do zero. (Não exclui o formulário antigo do Drive.)
 */
function resetarFormulario() {
  PropertiesService.getScriptProperties().deleteProperty('FORM_ID');
  Logger.log('Referência limpa. A próxima execução criará um novo formulário.');
}