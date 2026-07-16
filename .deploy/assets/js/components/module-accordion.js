// Deve bater com --modulo-open-duration / --modulo-text-delay em cards.css
const OPEN_DURATION_MS = 50;
const REVEAL_DELAY_MS = 10;

export function initModuleAccordion() {
  const modules = document.querySelectorAll(".module");
  let revealTimeout = null;

  modules.forEach((module) => {
    // Módulo já vem aberto no HTML (ex.: módulo 1): mostra o texto direto,
    // sem esperar o delay que só faz sentido após uma animação de abertura.
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
