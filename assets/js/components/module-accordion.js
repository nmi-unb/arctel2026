export function initModuleAccordion() {
  const modules = document.querySelectorAll(".module");

  modules.forEach((module) => {
    const toggle = module.querySelector(".module__toggle");
    toggle.addEventListener("click", () => {
      const isOpen = module.classList.contains("is-open");

      modules.forEach((m) => {
        m.classList.remove("is-open");
        m.querySelector(".module__toggle").setAttribute("aria-expanded", "false");
      });

      if (!isOpen) {
        module.classList.add("is-open");
        toggle.setAttribute("aria-expanded", "true");
      }
    });
  });
}
