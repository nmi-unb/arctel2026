import { eventos } from "../data/calendario.js";
import { calcularJanelaAcesso } from "../services/access-window.js";

const TIMEZONE = "America/Sao_Paulo";
const REFRESH_INTERVAL_MS = 60000;

const COURSE_START = { year: 2026, month: 7 }; // agosto/2026 (mês 0-indexado)
const COURSE_END = { year: 2026, month: 10 }; // novembro/2026

const WEEKDAY_LONG_BR = {
  Sun: "Domingo",
  Mon: "Segunda",
  Tue: "Terça",
  Wed: "Quarta",
  Thu: "Quinta",
  Fri: "Sexta",
  Sat: "Sábado",
};

const WEEKDAY_SHORT_BR = {
  Sun: "Dom",
  Mon: "Seg",
  Tue: "Ter",
  Wed: "Qua",
  Thu: "Qui",
  Fri: "Sex",
  Sat: "Sáb",
};

const MONTH_LONG_BR = [
  "janeiro", "fevereiro", "março", "abril", "maio", "junho",
  "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
];

const MONTH_SHORT_BR = [
  "jan", "fev", "mar", "abr", "mai", "jun",
  "jul", "ago", "set", "out", "nov", "dez",
];

function capitalize(text) {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

/* Todo componente de data/hora exibido vem daqui — nunca de Date#getDay()/
   getMonth() direto, que leem o fuso do dispositivo de quem acessa a
   página, não o de Brasília (mesma regra aplicada em notice-board.js). */
function partsInTimezone(date) {
  const formatter = new Intl.DateTimeFormat("en-US", {
    timeZone: TIMEZONE,
    weekday: "short",
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
  const parts = Object.fromEntries(formatter.formatToParts(date).map((p) => [p.type, p.value]));
  return {
    weekday: parts.weekday,
    day: parts.day,
    month: Number(parts.month) - 1,
    year: Number(parts.year),
    hour: parts.hour,
    minute: parts.minute,
  };
}

function buildInstant(evento, campo) {
  return new Date(`${evento.data}T${evento[campo]}:00-03:00`);
}

function formatHora(date) {
  const { hour, minute } = partsInTimezone(date);
  return `${hour}:${minute}`;
}

function formatDataHora(inicio, fim) {
  const { weekday, day, month } = partsInTimezone(inicio);
  const weekdayLabel = WEEKDAY_LONG_BR[weekday] || weekday;
  return `${weekdayLabel}, ${day} de ${MONTH_LONG_BR[month]} · ${formatHora(inicio)}–${formatHora(fim)}`;
}

/* Datas de calendário (grade de semanas) são aritmética de calendário pura —
   ano/mês/dia, sem hora — por isso usam Date em UTC (meio-dia arbitrário via
   Date.UTC) em vez de TIMEZONE: isso evita qualquer efeito de fuso horário
   ou DST ao somar/subtrair dias, o que instantes reais (início/fim de aula)
   precisariam considerar. */
function utcDate(year, month, day) {
  return new Date(Date.UTC(year, month, day));
}

function addDaysUTC(date, days) {
  const result = new Date(date);
  result.setUTCDate(result.getUTCDate() + days);
  return result;
}

function mondayOfWeekUTC(date) {
  const day = date.getUTCDay();
  const offset = (day + 6) % 7;
  return addDaysUTC(date, -offset);
}

function parseYMD(value) {
  const [year, month, day] = value.split("-").map(Number);
  return utcDate(year, month - 1, day);
}

/* Semana "pertence" ao mês que contém sua quinta-feira — mesma lógica da
   numeração ISO de semanas. Isso rende 4 ou 5 semanas por mês, nunca 6
   (nenhum trim aqui: cru, sem cortar nada). */
function getRawWeeksOfMonth(year, month) {
  let monday = mondayOfWeekUTC(utcDate(year, month, 1));

  while (true) {
    const thursday = addDaysUTC(monday, 3);
    if (thursday.getUTCFullYear() === year && thursday.getUTCMonth() === month) break;
    monday = addDaysUTC(monday, 7);
  }

  const weeks = [];
  while (true) {
    const thursday = addDaysUTC(monday, 3);
    if (thursday.getUTCFullYear() !== year || thursday.getUTCMonth() !== month) break;
    weeks.push({ start: monday, end: addDaysUTC(monday, 6) });
    monday = addDaysUTC(monday, 7);
  }

  return weeks;
}

function prevMonthOf(year, month) {
  return month === 0 ? { year: year - 1, month: 11 } : { year, month: month - 1 };
}

function isAntesDoInicioDoCurso(year, month) {
  return year * 12 + month < COURSE_START.year * 12 + COURSE_START.month;
}

/* Grade fixa em 4 colunas — mês com 5 semanas-por-quinta (ver acima) nunca
   PERDE a semana excedente: ela é empurrada pro mês seguinte (aparece lá
   como a 1ª semana), em vez de simplesmente desaparecer do calendário. Só
   não carrega nada pro primeiro mês navegável do curso, pra não puxar uma
   semana de um mês que nem existe na navegação (ex.: julho antes de
   agosto/2026). */
function getWeeksOfMonth(year, month) {
  const raw = getRawWeeksOfMonth(year, month);
  const anterior = prevMonthOf(year, month);
  const rawAnterior = isAntesDoInicioDoCurso(anterior.year, anterior.month)
    ? []
    : getRawWeeksOfMonth(anterior.year, anterior.month);
  const carregada = rawAnterior.length > 4 ? rawAnterior[rawAnterior.length - 1] : null;
  const combinadas = carregada ? [carregada, ...raw] : raw;
  return combinadas.slice(0, 4);
}

function eventoNaSemana(evento, semana) {
  const data = parseYMD(evento.data);
  return data >= semana.start && data <= semana.end;
}

function formatIntervaloSemana(semana) {
  const startY = semana.start.getUTCFullYear();
  const startM = semana.start.getUTCMonth();
  const startD = String(semana.start.getUTCDate()).padStart(2, "0");
  const endM = semana.end.getUTCMonth();
  const endD = String(semana.end.getUTCDate()).padStart(2, "0");

  if (startM === endM) {
    return `${startD}–${endD} ${MONTH_SHORT_BR[startM]}`;
  }
  return `${startD} ${MONTH_SHORT_BR[startM]} – ${endD} ${MONTH_SHORT_BR[endM]}`;
}

/* "Próxima aula" usa o FIM do evento como corte, não o início: uma aula em
   andamento (entre início e fim) continua sendo a "próxima/atual" até
   terminar — senão, no minuto em que ela começa, o card já pularia pra
   seguinte e a janela de acesso ao Teams (30min antes até 30min depois do
   início) nunca teria efeito prático nesse intervalo pós-início. */
function encontrarProximasAulas(lista, now) {
  const ordenados = lista.slice().sort((a, b) => buildInstant(a, "inicio") - buildInstant(b, "inicio"));
  const indice = ordenados.findIndex((evento) => buildInstant(evento, "fim") >= now);
  const proximo = indice === -1 ? null : ordenados[indice];
  const seguinte = indice === -1 ? null : ordenados[indice + 1] || null;
  return { proximo, seguinte, ultimo: ordenados[ordenados.length - 1] || null };
}

function calcularJanelaTeams(evento, now) {
  return calcularJanelaAcesso(buildInstant(evento, "inicio"), now);
}

function clampMonth(mes) {
  const key = (m) => m.year * 12 + m.month;
  if (key(mes) < key(COURSE_START)) return { ...COURSE_START };
  if (key(mes) > key(COURSE_END)) return { ...COURSE_END };
  return mes;
}

function renderTeamsBtn(btn, evento, now) {
  btn.classList.remove("calendario__btn--disabled", "calendario__btn--wait");
  btn.removeAttribute("title");

  const teamsHref = evento.teamsUrl;

  if (!teamsHref) {
    btn.href = "#";
    btn.removeAttribute("target");
    btn.setAttribute("aria-disabled", "true");
    btn.classList.add("calendario__btn--disabled");
    return;
  }

  const { dentro, aindaNaoAbriu } = calcularJanelaTeams(evento, now);

  if (!dentro) {
    btn.href = "#";
    btn.removeAttribute("target");
    btn.setAttribute("aria-disabled", "true");
    btn.classList.add("calendario__btn--wait");
    btn.title = aindaNaoAbriu
      ? "Esta atividade ainda não começou."
      : "O horário de acesso a esta atividade já passou.";
    return;
  }

  btn.href = teamsHref;
  btn.target = "_blank";
  btn.rel = "noopener noreferrer";
  btn.removeAttribute("aria-disabled");
}

/* Cada card (a próxima aula e a que vem depois dela) usa a mesma marcação —
   cardRefs vem de buildCardRefs(), um por elemento [data-calendario-highlight].
   Sem evento (não há "próxima depois da próxima", ou curso encerrado): o
   card correspondente só some — não há o que mostrar nele. */
function renderCard(cardRefs, evento, now) {
  if (!evento) {
    cardRefs.card.hidden = true;
    return;
  }

  cardRefs.card.hidden = false;
  cardRefs.card.classList.remove("calendario__highlight--encerrado");
  cardRefs.actions.hidden = false;
  cardRefs.tema.hidden = false;

  cardRefs.titulo.textContent = evento.titulo;
  cardRefs.tema.textContent = evento.tema;

  const inicio = buildInstant(evento, "inicio");
  const fim = buildInstant(evento, "fim");
  cardRefs.dataTime.setAttribute("datetime", inicio.toISOString());
  cardRefs.data.textContent = formatDataHora(inicio, fim);
  cardRefs.liveBadge.hidden = !(now >= inicio && now <= fim);

  renderTeamsBtn(cardRefs.teamsBtn, evento, now);
}

function renderCardEncerrado(cardRefs, ultimo) {
  cardRefs.card.hidden = false;
  cardRefs.card.classList.add("calendario__highlight--encerrado");
  cardRefs.liveBadge.hidden = true;
  cardRefs.titulo.textContent = "Curso encerrado";
  cardRefs.tema.textContent = "";
  cardRefs.tema.hidden = true;
  cardRefs.data.textContent = ultimo
    ? `Último encontro: ${formatDataHora(buildInstant(ultimo, "inicio"), buildInstant(ultimo, "fim"))}`
    : "";
  cardRefs.actions.hidden = true;
}

function renderDestaque(cards, proximo, seguinte, ultimo, now) {
  if (!proximo) {
    renderCardEncerrado(cards[0], ultimo);
    renderCard(cards[1], null, now);
    return;
  }

  renderCard(cards[0], proximo, now);
  renderCard(cards[1], seguinte, now);
}

function renderEvento(evento) {
  const item = document.createElement("li");
  item.className = "calendario__evento";

  const inicio = buildInstant(evento, "inicio");
  const fim = buildInstant(evento, "fim");
  const { weekday, day } = partsInTimezone(inicio);

  const data = document.createElement("time");
  data.className = "calendario__evento-data";
  data.dateTime = inicio.toISOString();
  data.textContent = `${WEEKDAY_SHORT_BR[weekday] || weekday} ${day}`;

  const titulo = document.createElement("p");
  titulo.className = "calendario__evento-titulo";
  titulo.textContent = evento.titulo;

  const horario = document.createElement("p");
  horario.className = "calendario__evento-horario";
  horario.textContent = `${formatHora(inicio)}–${formatHora(fim)}`;

  item.append(data, titulo, horario);
  return item;
}

function renderSemana(semana, index, eventosDaSemana, semanaAtualEvento) {
  const card = document.createElement("div");
  card.className = "calendario__semana";

  const isCurrent = semanaAtualEvento && eventoNaSemana(semanaAtualEvento, semana);
  if (isCurrent) card.classList.add("is-current");

  const label = document.createElement("p");
  label.className = "calendario__semana-label";
  label.textContent = `Semana ${index + 1}`;

  const intervalo = document.createElement("p");
  intervalo.className = "calendario__semana-intervalo";
  intervalo.textContent = formatIntervaloSemana(semana);

  const lista = document.createElement("ul");
  lista.className = "calendario__semana-eventos";

  if (!eventosDaSemana.length) {
    const vazio = document.createElement("li");
    vazio.className = "calendario__semana-vazio";
    vazio.textContent = "Sem encontros";
    lista.append(vazio);
  } else {
    eventosDaSemana
      .slice()
      .sort((a, b) => buildInstant(a, "inicio") - buildInstant(b, "inicio"))
      .forEach((evento) => lista.append(renderEvento(evento)));
  }

  card.append(label, intervalo, lista);
  return card;
}

function renderMes(refs, state) {
  const { year, month } = state.mesAtual;
  const semanas = getWeeksOfMonth(year, month);

  refs.monthLabel.textContent = `${capitalize(MONTH_LONG_BR[month])} ${year}`;
  refs.weeksRange.textContent = `Semanas 1–${semanas.length}`;

  refs.weeksGrid.innerHTML = "";

  semanas.forEach((semana, index) => {
    const eventosDaSemana = eventos.filter((evento) => eventoNaSemana(evento, semana));
    refs.weeksGrid.append(renderSemana(semana, index, eventosDaSemana, state.proximo));
  });

  const noPrimeiro = year === COURSE_START.year && month === COURSE_START.month;
  const noUltimo = year === COURSE_END.year && month === COURSE_END.month;
  refs.prevBtn.disabled = noPrimeiro;
  refs.prevBtn.setAttribute("aria-disabled", String(noPrimeiro));
  refs.nextBtn.disabled = noUltimo;
  refs.nextBtn.setAttribute("aria-disabled", String(noUltimo));

  refs.liveRegion.textContent = `${capitalize(MONTH_LONG_BR[month])} ${year}`;
}

function irParaMes(refs, state, delta) {
  const totalAtual = state.mesAtual.year * 12 + state.mesAtual.month + delta;
  const proposto = clampMonth({ year: Math.floor(totalAtual / 12), month: ((totalAtual % 12) + 12) % 12 });
  if (proposto.year === state.mesAtual.year && proposto.month === state.mesAtual.month) return;
  state.mesAtual = proposto;
  renderMes(refs, state);
}

/* Um cardRefs por elemento [data-calendario-highlight] (são 2: a próxima
   aula e a que vem depois dela) — cada um busca seus próprios campos
   escopados dentro do card, não por id (as duas marcações são idênticas). */
function buildCardRefs(cardEl) {
  const teamsBtn = cardEl.querySelector("[data-calendario-teams]");

  teamsBtn.addEventListener("click", (event) => {
    if (teamsBtn.getAttribute("aria-disabled") === "true") event.preventDefault();
  });

  return {
    card: cardEl,
    liveBadge: cardEl.querySelector("[data-calendario-live]"),
    titulo: cardEl.querySelector("[data-calendario-titulo]"),
    tema: cardEl.querySelector("[data-calendario-tema]"),
    data: cardEl.querySelector("[data-calendario-datahora]"),
    dataTime: cardEl.querySelector("[data-calendario-datahora-time]"),
    actions: cardEl.querySelector("[data-calendario-actions]"),
    teamsBtn,
  };
}

export function initCalendario() {
  const section = document.querySelector("[data-calendario]");
  if (!section) return;

  const cards = [...section.querySelectorAll("[data-calendario-highlight]")].map(buildCardRefs);

  const refs = {
    monthLabel: section.querySelector("[data-calendario-month]"),
    weeksRange: section.querySelector("[data-calendario-weeks-range]"),
    weeksGrid: section.querySelector("[data-calendario-weeks-grid]"),
    prevBtn: section.querySelector("[data-calendario-prev]"),
    nextBtn: section.querySelector("[data-calendario-next]"),
    navGroup: section.querySelector("[data-calendario-nav-group]"),
    liveRegion: section.querySelector("[data-calendario-live]"),
  };

  const now = new Date();
  const { proximo, seguinte, ultimo } = encontrarProximasAulas(eventos, now);
  const referencia = proximo || ultimo;
  const dataReferencia = referencia ? parseYMD(referencia.data) : utcDate(COURSE_START.year, COURSE_START.month, 1);

  const state = {
    mesAtual: clampMonth({ year: dataReferencia.getUTCFullYear(), month: dataReferencia.getUTCMonth() }),
    proximo,
  };

  renderDestaque(cards, proximo, seguinte, ultimo, now);
  renderMes(refs, state);

  refs.prevBtn.addEventListener("click", () => irParaMes(refs, state, -1));
  refs.nextBtn.addEventListener("click", () => irParaMes(refs, state, 1));

  refs.navGroup?.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      irParaMes(refs, state, -1);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      irParaMes(refs, state, 1);
    }
  });

  /* Recalcula "próximas aulas" e a janela de acesso ao Teams periodicamente
     — sem isso, uma aba aberta atravessando o horário de início/fim de um
     encontro mostraria o card e o botão desatualizados até um F5 (mesmo
     intervalo de notice-board.js). Só atualiza os cards e a marcação
     is-current; nunca pula o mês que a pessoa esteja navegando manualmente. */
  setInterval(() => {
    const agora = new Date();
    const proximas = encontrarProximasAulas(eventos, agora);
    state.proximo = proximas.proximo;
    renderDestaque(cards, proximas.proximo, proximas.seguinte, proximas.ultimo, agora);
    renderMes(refs, state);
  }, REFRESH_INTERVAL_MS);
}
