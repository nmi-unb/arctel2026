export function initHamburgerMenu() {
  const btn = document.querySelector(".hamburger-btn");
  const overlay = document.querySelector(".site-nav-overlay");
  if (!btn || !overlay) return;

  function openMenu() {
    overlay.classList.add("is-open");
    btn.setAttribute("aria-expanded", "true");
  }

  function closeMenu() {
    overlay.classList.remove("is-open");
    btn.setAttribute("aria-expanded", "false");
  }

  btn.addEventListener("click", (event) => {
    event.stopPropagation();
    if (overlay.classList.contains("is-open")) closeMenu();
    else openMenu();
  });

  overlay.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  // Overlay cobre a tela inteira - "clicar fora" é clicar no fundo dele,
  // fora dos links de navegação.
  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) closeMenu();
  });

  window.addEventListener("scroll", () => {
    btn.classList.toggle("is-scrolled", window.scrollY > 10);
  });
}
