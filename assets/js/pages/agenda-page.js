import { eventos, marcos } from "../data/calendario.js";

const TIMEZONE = "America/Sao_Paulo";

const MONTH_LONG_BR = [
  "janeiro", "fevereiro", "março", "abril", "maio", "junho",
  "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
];

const WEEKDAY_SHORT_BR = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

function capitalize(text) {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function pad(n) {
  return String(n).padStart(2, "0");
}

/* "Hoje" sempre no fuso de Brasília, não no do dispositivo (mesma regra do
   componente calendario.js). Devolve "YYYY-MM-DD". */
function hojeEmBrasilia() {
  const parts = Object.fromEntries(
    new Intl.DateTimeFormat("en-US", {
      timeZone: TIMEZONE,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    })
      .formatToParts(new Date())
      .map((p) => [p.type, p.value]),
  );
  return `${parts.year}-${parts.month}-${parts.day}`;
}

/* Calendário é aritmética pura de ano/mês/dia — Date em UTC evita qualquer
   efeito de fuso/DST. */
function parseYMD(value) {
  const [year, month, day] = value.split("-").map(Number);
  return { year, month: month - 1, day };
}

function weekdayOf(year, month, day) {
  return new Date(Date.UTC(year, month, day)).getUTCDay();
}

function daysInMonth(year, month) {
  return new Date(Date.UTC(year, month + 1, 0)).getUTCDate();
}

/* Une encontros (aulas) e marcos (prazos) num formato único. */
function buildAtividades() {
  const aulas = eventos.map((evento) => ({
    id: evento.id,
    tipo: evento.tipo || "aula",
    data: evento.data,
    titulo: evento.titulo,
    descricao: evento.tema,
    horario: `${evento.inicio}–${evento.fim}`,
    href: `./modulos/modulo-${evento.modulo}.html`,
  }));

  const prazos = marcos.map((marco) => ({
    id: marco.id,
    tipo: marco.tipo || "prazo",
    data: marco.data,
    titulo: marco.titulo,
    descricao: marco.descricao,
    horario: "",
    href: "",
  }));

  return [...aulas, ...prazos].sort((a, b) =>
    a.data === b.data ? (a.horario || "").localeCompare(b.horario || "") : a.data.localeCompare(b.data),
  );
}

/* Só entram os meses que têm ao menos uma atividade. */
function buildMeses(atividades) {
  const chaves = [...new Set(atividades.map((a) => a.data.slice(0, 7)))].sort();
  return chaves.map((chave) => {
    const [year, month] = chave.split("-").map(Number);
    return { chave, year, month: month - 1 };
  });
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

/* Um mini-calendário por mês com atividade, todos visíveis ao mesmo tempo.
   Dia com atividade vira bloco inteiro colorido (verde = aula, laranja =
   prazo). Clicar no mês filtra a lista abaixo; clicar de novo mostra tudo. */
function renderMes(mes, state, onSelect) {
  const { year, month } = mes;
  const card = el("section", "agenda__mes");
  card.dataset.chave = mes.chave;
  if (state.filtro === mes.chave) card.classList.add("is-filtro");

  const titulo = el("button", "agenda__mes-titulo", `${capitalize(MONTH_LONG_BR[month])} ${year}`);
  titulo.type = "button";
  titulo.setAttribute("aria-pressed", String(state.filtro === mes.chave));
  titulo.addEventListener("click", () => onSelect(mes.chave));

  const grade = el("div", "agenda__grade");
  WEEKDAY_SHORT_BR.forEach((nome) => grade.append(el("div", "agenda__dow", nome.charAt(0))));

  const primeiro = weekdayOf(year, month, 1);
  for (let i = 0; i < primeiro; i += 1) grade.append(el("div", "agenda__dia agenda__dia--vazio"));

  const total = daysInMonth(year, month);
  for (let dia = 1; dia <= total; dia += 1) {
    const data = `${year}-${pad(month + 1)}-${pad(dia)}`;
    const doDia = state.atividades.filter((a) => a.data === data);
    const celula = el("div", "agenda__dia", String(dia));

    if (doDia.length) {
      const tipo = doDia.some((a) => a.tipo === "prazo") ? "prazo" : "aula";
      celula.classList.add("tem-atividade", `tem-atividade--${tipo}`);
      celula.title = doDia.map((a) => a.titulo).join(" | ");
    }
    if (data === state.hoje) celula.classList.add("is-hoje");

    grade.append(celula);
  }

  card.append(titulo, grade);
  return card;
}

function renderMeses(refs, state) {
  refs.meses.innerHTML = "";
  const onSelect = (chave) => {
    state.filtro = state.filtro === chave ? null : chave;
    renderMeses(refs, state);
    renderLista(refs, state);
  };
  state.meses.forEach((mes) => refs.meses.append(renderMes(mes, state, onSelect)));
}

/* Lista simples: uma linha por atividade, agrupada por mês. */
function renderLista(refs, state) {
  refs.lista.innerHTML = "";

  state.meses
    .filter((mes) => !state.filtro || mes.chave === state.filtro)
    .forEach((mes) => {
      const grupo = el("section", "agenda__grupo");
      grupo.append(el("h2", "agenda__grupo-titulo", `${capitalize(MONTH_LONG_BR[mes.month])} ${mes.year}`));

      const ul = el("ul", "agenda__itens");
      state.atividades
        .filter((a) => a.data.startsWith(mes.chave))
        .forEach((atividade) => {
          const { year, month, day } = parseYMD(atividade.data);
          const item = el("li", `agenda__item agenda__item--${atividade.tipo}`);

          const data = el("time", "agenda__item-data", `${pad(day)}/${pad(month + 1)} ${WEEKDAY_SHORT_BR[weekdayOf(year, month, day)]}`);
          data.dateTime = atividade.data;

          const texto = el("span", "agenda__item-texto");
          texto.append(el("strong", "", atividade.titulo));
          if (atividade.descricao) texto.append(document.createTextNode(` — ${atividade.descricao}`));
          if (atividade.horario) texto.append(el("span", "agenda__item-hora", ` (${atividade.horario})`));

          item.append(data, texto);
          ul.append(item);
        });

      grupo.append(ul);
      refs.lista.append(grupo);
    });
}

function initAgendaPage() {
  const root = document.querySelector("[data-agenda]");
  if (!root) return;

  const atividades = buildAtividades();
  const refs = {
    meses: root.querySelector("[data-agenda-meses]"),
    lista: root.querySelector("[data-agenda-lista]"),
  };
  const state = { atividades, meses: buildMeses(atividades), hoje: hojeEmBrasilia(), filtro: null };

  renderMeses(refs, state);
  renderLista(refs, state);
}

document.addEventListener("DOMContentLoaded", initAgendaPage);
