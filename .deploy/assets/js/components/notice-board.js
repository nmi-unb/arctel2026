const DATA_URL = "./assets/data/avisos.json";
const REFRESH_INTERVAL_MS = 60000;
const TIMEZONE = "America/Sao_Paulo";

const BADGES = {
  confirmacao: { className: "notice-board__badge--confirmacao", label: "Aula confirmada" },
  ao_vivo: { className: "notice-board__badge--ao_vivo", label: "Ao vivo agora" },
  alteracao: { className: "notice-board__badge--alteracao", label: "Alteração importante" },
  alerta: { className: "notice-board__badge--alerta", label: "Alerta" },
  material: { className: "notice-board__badge--material", label: "Material disponível" },
  encerrado: { className: "notice-board__badge--encerrado", label: "Encerrado" },
};

function parseDate(value) {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

function isValidAviso(aviso) {
  return (
    aviso &&
    typeof aviso.id === "string" &&
    typeof aviso.titulo === "string" &&
    typeof aviso.mensagem === "string" &&
    typeof aviso.tipo === "string" &&
    typeof aviso.ativo === "boolean"
  );
}

function formatDateTime(date) {
  return date.toLocaleString("pt-BR", {
    timeZone: TIMEZONE,
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatDate(date) {
  return date.toLocaleDateString("pt-BR", { timeZone: TIMEZONE, day: "2-digit", month: "2-digit", year: "numeric" });
}

function formatTime(date) {
  return date.toLocaleTimeString("pt-BR", { timeZone: TIMEZONE, hour: "2-digit", minute: "2-digit" });
}

function renderBadge(tipo) {
  const badge = BADGES[tipo] || BADGES.alteracao;
  const span = document.createElement("span");
  span.className = `notice-board__badge ${badge.className}`;
  const dot = document.createElement("span");
  dot.className = "notice-board__badge-dot";
  dot.setAttribute("aria-hidden", "true");
  span.append(dot, document.createTextNode(badge.label));
  return span;
}

/* Classifica avisos entre "atuais" e "histórico".
   Atual = ativo && (sem arquivarApos ou arquivarApos ainda não passou). */
function classifyAvisos(avisos, now) {
  const current = [];
  const archived = [];

  avisos.forEach((aviso) => {
    const arquivarApos = parseDate(aviso.arquivarApos);
    const isArchived = !aviso.ativo || (arquivarApos && arquivarApos <= now);
    (isArchived ? archived : current).push(aviso);
  });

  return { current, archived };
}

/* Maior prioridade primeiro; empate resolvido pela publicação mais recente. */
function pickPrincipal(current) {
  if (!current.length) return null;
  return current
    .slice()
    .sort((a, b) => {
      const prioridadeDiff = (b.prioridade || 0) - (a.prioridade || 0);
      if (prioridadeDiff !== 0) return prioridadeDiff;
      const dateA = parseDate(a.dataPublicacao)?.getTime() || 0;
      const dateB = parseDate(b.dataPublicacao)?.getTime() || 0;
      return dateB - dateA;
    })[0];
}

function pickAula(current, now) {
  const comHorario = current.filter((a) => parseDate(a.dataInicio) && parseDate(a.dataFim));

  const aoVivo = comHorario
    .filter((a) => parseDate(a.dataInicio) <= now && now <= parseDate(a.dataFim))
    .sort((a, b) => (b.prioridade || 0) - (a.prioridade || 0));

  if (aoVivo.length) return { aviso: aoVivo[0], status: "ao_vivo" };

  const proximas = comHorario
    .filter((a) => parseDate(a.dataInicio) > now)
    .sort((a, b) => parseDate(a.dataInicio) - parseDate(b.dataInicio));

  if (proximas.length) return { aviso: proximas[0], status: "proxima" };

  return null;
}

function linkPodeAparecer(aviso, now) {
  if (!aviso.link) return false;
  const exibirA_partir = parseDate(aviso.exibirLinkAPartirDe);
  return !exibirA_partir || now >= exibirA_partir;
}

function renderLink(aviso, now, className) {
  if (!linkPodeAparecer(aviso, now)) return null;
  const a = document.createElement("a");
  a.className = className;
  a.href = aviso.link;
  a.textContent = aviso.textoLink || "Acessar";
  if (/^https?:\/\//i.test(aviso.link)) {
    a.target = "_blank";
    a.rel = "noopener noreferrer";
  }
  return a;
}

function renderHighlight(container, principal) {
  container.innerHTML = "";

  if (!principal) {
    const empty = document.createElement("p");
    empty.className = "notice-board__empty";
    empty.textContent = "Nenhum aviso disponível no momento.";
    container.append(empty);
    return;
  }

  const title = document.createElement("p");
  title.className = "notice-board__title";
  title.textContent = principal.titulo;

  const message = document.createElement("p");
  message.className = "notice-board__message";
  const dataPublicacao = parseDate(principal.dataPublicacao);
  message.textContent = dataPublicacao
    ? `${principal.mensagem} · ${formatDateTime(dataPublicacao)}`
    : principal.mensagem;

  container.append(renderBadge(principal.tipo), title, message);
}

function renderAula(container, aulaInfo, now) {
  if (!aulaInfo) {
    container.hidden = true;
    container.innerHTML = "";
    return;
  }

  container.hidden = false;
  container.innerHTML = "";

  const { aviso, status } = aulaInfo;
  const inicio = parseDate(aviso.dataInicio);
  const fim = parseDate(aviso.dataFim);

  const title = document.createElement("p");
  title.className = "notice-board__title";
  title.textContent = aviso.titulo;

  const message = document.createElement("p");
  message.className = "notice-board__message";
  message.textContent =
    status === "ao_vivo"
      ? `Até ${formatTime(fim)}`
      : `${formatDate(inicio)} · ${formatTime(inicio)}–${formatTime(fim)}`;

  container.append(renderBadge(status === "ao_vivo" ? "ao_vivo" : "confirmacao"), title, message);

  const link = renderLink(aviso, now, "btn btn--solid btn--sm notice-board__cta");
  if (link) container.append(link);
}

function renderUpdatedAt(el, avisos) {
  const latest = avisos
    .map((a) => parseDate(a.dataPublicacao))
    .filter(Boolean)
    .sort((a, b) => b - a)[0];

  el.textContent = latest ? `Última atualização: ${formatDateTime(latest)}` : "";
}

function renderHistoryList(listEl, archived) {
  listEl.innerHTML = "";

  if (!archived.length) {
    const empty = document.createElement("p");
    empty.className = "notice-modal__empty";
    empty.textContent = "Nenhum aviso no histórico.";
    listEl.append(empty);
    return;
  }

  const sorted = archived.slice().sort((a, b) => {
    const dateA = parseDate(a.dataPublicacao)?.getTime() || 0;
    const dateB = parseDate(b.dataPublicacao)?.getTime() || 0;
    return dateB - dateA;
  });

  sorted.forEach((aviso) => {
    const item = document.createElement("li");
    item.className = "notice-modal__item";

    const title = document.createElement("p");
    title.className = "notice-modal__item-title";
    title.textContent = aviso.titulo;

    const message = document.createElement("p");
    message.className = "notice-modal__item-message";
    message.textContent = aviso.mensagem;

    const date = document.createElement("p");
    date.className = "notice-modal__item-date";
    const dataPublicacao = parseDate(aviso.dataPublicacao);
    date.textContent = dataPublicacao ? formatDateTime(dataPublicacao) : "";

    item.append(renderBadge(aviso.tipo), title, message, date);

    const link = renderLink(aviso, new Date(), "notice-modal__item-link");
    if (link) item.append(link);

    listEl.append(item);
  });
}

function createModalController(overlay, openButton) {
  const closeButton = overlay.querySelector("[data-notice-modal-close]");
  const focusableSelector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
  let lastFocused = null;

  function getFocusables() {
    return Array.from(overlay.querySelector(".notice-modal").querySelectorAll(focusableSelector));
  }

  function handleKeydown(event) {
    if (event.key === "Escape") {
      event.preventDefault();
      close();
      return;
    }

    if (event.key === "Tab") {
      const focusables = getFocusables();
      if (!focusables.length) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  }

  function handleOverlayClick(event) {
    if (event.target === overlay) close();
  }

  function open() {
    lastFocused = document.activeElement;
    overlay.hidden = false;
    document.body.classList.add("notice-modal-open");
    document.addEventListener("keydown", handleKeydown);
    overlay.addEventListener("click", handleOverlayClick);
    (getFocusables()[0] || overlay).focus();
  }

  function close() {
    overlay.hidden = true;
    document.body.classList.remove("notice-modal-open");
    document.removeEventListener("keydown", handleKeydown);
    overlay.removeEventListener("click", handleOverlayClick);
    if (lastFocused) lastFocused.focus();
  }

  closeButton.addEventListener("click", close);
  openButton.addEventListener("click", open);

  return { open, close };
}

function renderFallback(refs) {
  renderHighlight(refs.highlight, null);
  renderAula(refs.aula, null, new Date());
  refs.updated.textContent = "";
  refs.historyBtn.disabled = true;
  renderHistoryList(refs.historyList, []);
}

function render(avisos, refs) {
  const now = new Date();
  const { current, archived } = classifyAvisos(avisos, now);

  renderHighlight(refs.highlight, pickPrincipal(current));
  renderAula(refs.aula, pickAula(current, now), now);
  refs.panel.classList.toggle("notice-board__panel--single", refs.aula.hidden);
  renderUpdatedAt(refs.updated, avisos);
  renderHistoryList(refs.historyList, archived);
  refs.historyBtn.disabled = false;
}

export function initNoticeBoard() {
  const board = document.querySelector("[data-notice-board]");
  if (!board) return;

  const refs = {
    panel: board.querySelector("[data-notice-panel]"),
    highlight: board.querySelector("[data-notice-highlight]"),
    aula: board.querySelector("[data-notice-aula]"),
    updated: board.querySelector("[data-notice-updated]"),
    historyBtn: document.getElementById("notice-history-btn"),
    historyList: document.querySelector("[data-notice-history-list]"),
  };

  const modalOverlay = document.querySelector("[data-notice-modal]");
  if (modalOverlay) createModalController(modalOverlay, refs.historyBtn);

  function load() {
    fetch(DATA_URL)
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
      })
      .then((data) => {
        const avisos = Array.isArray(data) ? data.filter(isValidAviso) : [];
        if (!avisos.length) throw new Error("Nenhum aviso válido encontrado em avisos.json");
        render(avisos, refs);
      })
      .catch((error) => {
        console.error("[notice-board] falha ao carregar avisos:", error);
        renderFallback(refs);
      });
  }

  load();
  setInterval(load, REFRESH_INTERVAL_MS);
}
