const header = document.querySelector(".site-header");
const menuToggle = document.querySelector(".menu-toggle");
const menuBackdrop = document.querySelector(".menu-backdrop");
const navLinks = document.querySelectorAll(".site-nav__link");

function openMenu() {
  header.classList.add("menu-is-open");
  document.body.classList.add("menu-open");
  menuToggle.setAttribute("aria-expanded", "true");
  menuToggle.setAttribute("aria-label", "Fechar menu");
}

function closeMenu() {
  header.classList.remove("menu-is-open");
  document.body.classList.remove("menu-open");
  menuToggle.setAttribute("aria-expanded", "false");
  menuToggle.setAttribute("aria-label", "Abrir menu");
}

function toggleMenu() {
  if (header.classList.contains("menu-is-open")) {
    closeMenu();
  } else {
    openMenu();
  }
}

function setActiveNavLink() {
  const currentHash = window.location.hash || "#inicio";

  navLinks.forEach((link) => {
    link.classList.toggle("is-active", link.getAttribute("href") === currentHash);
  });
}

function handleNavLinkClick(event) {
  const href = this.getAttribute("href");
  const isSectionLink = href.length > 1 && href.startsWith("#");

  if (isSectionLink) {
    const target = document.querySelector(href);
    if (target) {
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      history.pushState(null, "", href);
      setActiveNavLink();
    }
  }

  closeMenu();
}

menuToggle.addEventListener("click", toggleMenu);
menuBackdrop.addEventListener("click", closeMenu);

navLinks.forEach((link) => {
  link.addEventListener("click", handleNavLinkClick);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeMenu();
  }
});

window.addEventListener("hashchange", setActiveNavLink);

setActiveNavLink();

function handleMenuButtonScroll() {
  const hasScrolled = window.scrollY > 40;

  if (hasScrolled) {
    menuToggle.classList.add("is-scrolled");
  } else {
    menuToggle.classList.remove("is-scrolled");
  }
}

window.addEventListener("scroll", handleMenuButtonScroll);
handleMenuButtonScroll();
