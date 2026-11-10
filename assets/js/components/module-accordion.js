import { eventos } from "../data/calendario.js";

// Deve bater com --modulo-open-duration / --modulo-text-delay em cards.css
const OPEN_DURATION_MS = 50;
const REVEAL_DELAY_MS = 10;

/* Módulo que começa aberto: o da próxima aula (a em andamento conta até
   terminar). Passado o último encontro, abre "Avaliação", onde estão os
   prazos que restam. */
function idDoModuloInicial(now) {
  const proxima = eventos
    .slice()
    .sort((a, b) => a.data.localeCompare(b.data) || a.inicio.localeCompare(b.inicio))
    .find((evento) => new Date(`${evento.data}T${evento.fim}:00-03:00`) >= now);
  return proxima ? `modulo-${proxima.modulo}` : "avaliacao-geral";
}

export function initModuleAccordion() {
  const modules = document.querySelectorAll(".module");
  let revealTimeout = null;

  const inicial = document.getElementById(idDoModuloInicial(new Date()));
  if (inicial?.classList.contains("module")) {
    inicial.classList.add("is-open");
    inicial.querySelector(".module__toggle").setAttribute("aria-expanded", "true");
  }

  modules.forEach((module) => {
    // Módulo já vem aberto (ver acima): mostra o texto direto, sem esperar o
    // delay que só faz sentido após uma animação de abertura.
    if (module.classList.contains("is-open")) {
      module.classList.add("is-reveal");
    }

    const toggle = module.querySelector(".module__toggle");
    toggle.addEventListener("click", () => {
      const isOpen = module.classList.contains("is-open");

      clearTimeout(revealTimeout);

      modules.forEach((m) => {
        m.classList.remove("is-open", "is-reveal");
        m.querySelector(".module__toggle").setAttribute("aria-expanded", "false");
      });

      if (!isOpen) {
        module.classList.add("is-open");
        toggle.setAttribute("aria-expanded", "true");
        revealTimeout = setTimeout(() => {
          module.classList.add("is-reveal");
        }, OPEN_DURATION_MS + REVEAL_DELAY_MS);
      }
    });
  });
}
