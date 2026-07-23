import { parseDate } from "./notice-board.js";

function computeStatus(dataInicio, dataFim, now) {
  const inicio = parseDate(dataInicio);
  const fim = parseDate(dataFim);
  if (!inicio || !fim) return "scheduled";
  if (now < inicio) return "scheduled";
  if (now > fim) return "done";
  return "live";
}

const STATUS_LABELS = {
  scheduled: { badgeClass: "notice-board__badge--confirmacao", label: "Agendada" },
  live: { badgeClass: "notice-board__badge--ao_vivo", label: "Ao vivo" },
  done: { badgeClass: "notice-board__badge--encerrado", label: "Concluída" },
};

function renderStatusBadge(status) {
  const info = STATUS_LABELS[status] || STATUS_LABELS.scheduled;
  const span = document.createElement("span");
  span.className = `notice-board__badge ${info.badgeClass}`;
  const dot = document.createElement("span");
  dot.className = "notice-board__badge-dot";
  dot.setAttribute("aria-hidden", "true");
  span.append(dot, document.createTextNode(info.label));
  return span;
}

function formatLessonDate(date) {
  return date.toLocaleDateString("pt-BR", {
    timeZone: "America/Sao_Paulo",
    day: "2-digit",
    month: "2-digit",
  });
}

/* Pill é sempre <a> (mesmo indisponível, com href="#" e pointer-events:none
   via .lesson-pill--disabled) — nunca <span>, nunca omitida. */
function createPill({ className, href, text, disabled }) {
  const el = document.createElement("a");
  el.className = `lesson-pill ${className}${disabled ? " lesson-pill--disabled" : ""}`;
  el.textContent = text;
  el.href = disabled ? "#" : href;
  if (!disabled && /^https?:\/\//i.test(href)) {
    el.target = "_blank";
    el.rel = "noopener noreferrer";
  }
  return el;
}

function renderGroup(container, titleText, pills) {
  const title = document.createElement("p");
  title.className = "lesson-group__title";
  title.textContent = titleText;
  const list = document.createElement("div");
  list.className = "lesson-group__pills";
  list.append(...pills);
  container.append(title, list);
}

function buildTransmissaoPills(links) {
  const teamsHref = links?.teams;
  const gravacaoHref = links?.youtubeRecorded || links?.youtubeLive;

  return [
    createPill({ className: "lesson-pill--teams", href: teamsHref, text: "Teams", disabled: !teamsHref }),
    createPill({
      className: "lesson-pill--youtube",
      href: gravacaoHref,
      text: gravacaoHref ? "Gravação" : "Gravação (em breve)",
      disabled: !gravacaoHref,
    }),
  ];
}

/* Array vazio -> 1 pill opaca genérica. Array com itens -> 1 pill por item,
   opaca por item quando available:false ou sem url (nunca some da lista). */
function buildMaterialPills(items, className, placeholderText) {
  const list = items || [];

  if (!list.length) {
    return [createPill({ className, text: placeholderText, disabled: true })];
  }

  return list.map((item) => {
    const disabled = !item || item.available === false || !item.url;
    return createPill({ className, href: item?.url, text: item?.title || placeholderText, disabled });
  });
}

function renderLesson(lesson, moduloNumero, now) {
  const id = `modulo-${moduloNumero}-aula-${lesson.numero}`;
  const status = computeStatus(lesson.dataInicio, lesson.dataFim, now);
  const inicio = parseDate(lesson.dataInicio);

  const item = document.createElement("article");
  item.className = "lesson-item";

  const heading = document.createElement("h4");
  heading.className = "lesson-item__heading";

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "lesson-item__header";
  toggle.id = `${id}-toggle`;
  toggle.setAttribute("aria-expanded", "false");
  toggle.setAttribute("aria-controls", `${id}-panel`);

  const num = document.createElement("span");
  num.className = "lesson-num";
  num.textContent = lesson.numero;

  const title = document.createElement("span");
  title.className = "lesson-item__title";
  title.textContent = lesson.titulo;

  const date = document.createElement("span");
  date.className = "lesson-item__date";
  date.textContent = inicio ? formatLessonDate(inicio) : "";

  const icon = document.createElement("span");
  icon.className = "lesson-item__toggle-icon";
  icon.setAttribute("aria-hidden", "true");

  toggle.append(num, title, renderStatusBadge(status), date, icon);
  heading.append(toggle);

  const panel = document.createElement("div");
  panel.className = "lesson-item__body";
  panel.id = `${id}-panel`;
  panel.setAttribute("role", "region");
  panel.setAttribute("aria-labelledby", toggle.id);

  const inner = document.createElement("div");
  inner.className = "lesson-item__body-inner";

  renderGroup(inner, "Transmissão", buildTransmissaoPills(lesson.links));
  renderGroup(
    inner,
    "Materiais do professor",
    buildMaterialPills(lesson.materials?.professor, "lesson-pill--material", "Slides (em breve)")
  );
  renderGroup(
    inner,
    "Atividades substitutas",
    buildMaterialPills(lesson.materials?.replacementCourses, "lesson-pill--curso", "Atividade substituta (em breve)")
  );

  panel.append(inner);
  item.append(heading, panel);

  toggle.addEventListener("click", () => {
    const isOpen = item.classList.contains("is-open");
    item.parentElement.querySelectorAll(".lesson-item").forEach((other) => {
      other.classList.remove("is-open");
      other.querySelector(".lesson-item__header").setAttribute("aria-expanded", "false");
    });
    if (!isOpen) {
      item.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
    }
  });

  return item;
}

function renderEmpty(container) {
  const empty = document.createElement("p");
  empty.className = "module-page-materials";
  empty.textContent = "Os materiais, aulas e recursos deste módulo serão adicionados posteriormente.";
  container.append(empty);
}

export function initLessonAccordion() {
  const container = document.querySelector("[data-lesson-accordion]");
  if (!container) return;

  const moduloNumero = container.dataset.modulo;
  if (!moduloNumero) return;

  fetch(`../assets/data/modulos/modulo-${moduloNumero}.json`)
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((data) => {
      const lessons = Array.isArray(data?.lessons) ? data.lessons : [];
      container.innerHTML = "";

      if (!lessons.length) {
        renderEmpty(container);
        return;
      }

      const now = new Date();
      lessons
        .slice()
        .sort((a, b) => a.numero - b.numero)
        .forEach((lesson) => container.append(renderLesson(lesson, moduloNumero, now)));
    })
    .catch((error) => {
      console.error("[lesson-accordion] falha ao carregar aulas:", error);
      container.innerHTML = "";
      renderEmpty(container);
    });
}
