import { eventos } from "../data/calendario.js";

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

function pad2(n) {
  return String(n).padStart(2, "0");
}

function toIcsTimestamp(date) {
  return (
    date.getUTCFullYear() +
    pad2(date.getUTCMonth() + 1) +
    pad2(date.getUTCDate()) +
    "T" +
    pad2(date.getUTCHours()) +
    pad2(date.getUTCMinutes()) +
    pad2(date.getUTCSeconds()) +
    "Z"
  );
}

function escapeIcsText(text) {
  return String(text).replace(/([,;])/g, "\\$1");
}

/* icsUrl no dado é o "escape hatch" pra apontar um arquivo hospedado de
   verdade no futuro; sem ele, gera o .ics on-the-fly a partir dos próprios
   campos do evento — não depende de hospedagem externa, então o botão
   "Adicionar à agenda" nunca fica sem link. */
function buildIcsHref(evento) {
  if (evento.icsUrl) return evento.icsUrl;

  const inicio = buildInstant(evento, "inicio");
  const fim = buildInstant(evento, "fim");
  const linhas = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//NMI//Calendario do curso//PT-BR",
    "BEGIN:VEVENT",
    `UID:${evento.id}@arctel2026.nmi`,
    `DTSTAMP:${toIcsTimestamp(new Date())}`,
    `DTSTART:${toIcsTimestamp(inicio)}`,
    `DTEND:${toIcsTimestamp(fim)}`,
    `SUMMARY:${escapeIcsText(`${evento.titulo} — ${evento.tema}`)}`,
    evento.teamsUrl ? `DESCRIPTION:${escapeIcsText(evento.teamsUrl)}` : "",
    "END:VEVENT",
    "END:VCALENDAR",
  ].filter(Boolean);

  return `data:text/calendar;charset=utf-8,${encodeURIComponent(linhas.join("\r\n"))}`;
}

function encontrarProximoEvento(lista, now) {
  const ordenados = lista.slice().sort((a, b) => buildInstant(a, "inicio") - buildInstant(b, "inicio"));
  const proximo = ordenados.find((evento) => buildInstant(evento, "inicio") >= now);
  return { proximo: proximo || null, ultimo: ordenados[ordenados.length - 1] || null };
}

function clampMonth(mes) {
  const key = (m) => m.year * 12 + m.month;
  if (key(mes) < key(COURSE_START)) return { ...COURSE_START };
  if (key(mes) > key(COURSE_END)) return { ...COURSE_END };
  return mes;
}

function renderDestaque(refs, proximo, ultimo) {
  const card = refs.highlight;

  if (!proximo) {
    card.classList.add("calendario__highlight--encerrado");
    refs.highlightTitulo.textContent = "Curso encerrado";
    refs.highlightTema.textContent = "";
    refs.highlightTema.hidden = true;
    refs.highlightData.textContent = ultimo
      ? `Último encontro: ${formatDataHora(buildInstant(ultimo, "inicio"), buildInstant(ultimo, "fim"))}`
      : "";
    refs.highlightActions.hidden = true;
    return;
  }

  card.classList.remove("calendario__highlight--encerrado");
  refs.highlightActions.hidden = false;
  refs.highlightTema.hidden = false;

  refs.highlightTitulo.textContent = proximo.titulo;
  refs.highlightTema.textContent = proximo.tema;

  const inicio = buildInstant(proximo, "inicio");
  const fim = buildInstant(proximo, "fim");
  refs.highlightDataTime.setAttribute("datetime", inicio.toISOString());
  refs.highlightData.textContent = formatDataHora(inicio, fim);

  const teamsHref = proximo.teamsUrl;
  refs.teamsBtn.href = teamsHref || "#";
  refs.teamsBtn.toggleAttribute("aria-disabled", !teamsHref);
  refs.teamsBtn.classList.toggle("calendario__btn--disabled", !teamsHref);
  if (!teamsHref) refs.teamsBtn.removeAttribute("target");
  else {
    refs.teamsBtn.target = "_blank";
    refs.teamsBtn.rel = "noopener noreferrer";
  }

  refs.icsBtn.href = buildIcsHref(proximo);
  refs.icsBtn.download = `${proximo.id}.ics`;
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

export function initCalendario() {
  const section = document.querySelector("[data-calendario]");
  if (!section) return;

  const refs = {
    highlight: section.querySelector("[data-calendario-highlight]"),
    highlightTitulo: section.querySelector("[data-calendario-titulo]"),
    highlightTema: section.querySelector("[data-calendario-tema]"),
    highlightData: section.querySelector("[data-calendario-datahora]"),
    highlightDataTime: section.querySelector("[data-calendario-datahora-time]"),
    highlightActions: section.querySelector("[data-calendario-actions]"),
    teamsBtn: section.querySelector("[data-calendario-teams]"),
    icsBtn: section.querySelector("[data-calendario-ics]"),
    monthLabel: section.querySelector("[data-calendario-month]"),
    weeksRange: section.querySelector("[data-calendario-weeks-range]"),
    weeksGrid: section.querySelector("[data-calendario-weeks-grid]"),
    prevBtn: section.querySelector("[data-calendario-prev]"),
    nextBtn: section.querySelector("[data-calendario-next]"),
    navGroup: section.querySelector("[data-calendario-nav-group]"),
    liveRegion: section.querySelector("[data-calendario-live]"),
  };

  const now = new Date();
  const { proximo, ultimo } = encontrarProximoEvento(eventos, now);
  const referencia = proximo || ultimo;
  const dataReferencia = referencia ? parseYMD(referencia.data) : utcDate(COURSE_START.year, COURSE_START.month, 1);

  const state = {
    mesAtual: clampMonth({ year: dataReferencia.getUTCFullYear(), month: dataReferencia.getUTCMonth() }),
    proximo,
  };

  renderDestaque(refs, proximo, ultimo);
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

  /* Recalcula "próxima aula" periodicamente — sem isso, uma aba aberta
     atravessando o horário de início/fim de um encontro mostraria o card
     desatualizado até um F5 (mesmo intervalo de notice-board.js). Só
     atualiza o card e a marcação is-current; nunca pula o mês que a pessoa
     esteja navegando manualmente. */
  setInterval(() => {
    const agora = new Date();
    const proxima = encontrarProximoEvento(eventos, agora);
    state.proximo = proxima.proximo;
    renderDestaque(refs, proxima.proximo, proxima.ultimo);
    renderMes(refs, state);
  }, REFRESH_INTERVAL_MS);
}
