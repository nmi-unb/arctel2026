const header = document.querySelector(".site-header");
const menuToggle = document.querySelector(".menu-toggle");
const menuBackdrop = document.querySelector(".menu-backdrop");
const menuClose = document.querySelector(".site-nav__close");
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

function setActiveNavLink(hash) {
  const currentHash = hash || window.location.hash || "#inicio";

  navLinks.forEach((link) => {
    link.classList.toggle("is-active", link.getAttribute("href") === currentHash);
  });
}

/* Scrollspy: pílula acompanha a seção visível, não fica presa no "Início".
   Só roda na home (onde as seções #inicio/#modulos/#avisos/#contato existem
   de fato); nas páginas de módulo os links apontam pra ../index#... e não há
   seção correspondente no DOM local.
   Não dá pra usar IntersectionObserver por intersectionRatio aqui: #inicio é
   o <main>, ancestral das outras seções, então sua própria área é a página
   inteira — a razão de interseção dele fica sempre menor que a de uma seção
   pequena, mesmo quando #inicio é visualmente quem está no topo. Em vez
   disso, pega a última seção cujo topo já passou de uma linha de referência
   (clássico scrollspy por posição). */
const sectionIds = ["inicio", "modulos", "avisos", "contato"];
const sections = sectionIds
  .map((id) => document.getElementById(id))
  .filter(Boolean);

function updateActiveSection() {
  /* Linha de referência logo abaixo do header sticky, não no meio da tela —
     com o header fixo no topo, é essa faixa que decide qual seção "conta"
     como visível; usar 40% da viewport fazia a próxima seção ganhar assim
     que só espiava por baixo, mesmo com a seção anterior ainda dominando
     a tela (ex: "O Curso" é curto, "Módulos" some por virava ativo cedo
     demais). */
  const referenceLine = 130;
  const atBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2;
  let currentId = atBottom ? sections[sections.length - 1].id : sections[0].id;

  if (!atBottom) {
    sections.forEach((section) => {
      if (section.getBoundingClientRect().top <= referenceLine) {
        currentId = section.id;
      }
    });
  }

  setActiveNavLink(`#${currentId}`);
}

if (sections.length === sectionIds.length) {
  window.addEventListener("scroll", updateActiveSection);
  updateActiveSection();
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
menuClose?.addEventListener("click", closeMenu);

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

function handlePinnedHeader() {
  const shouldPin = window.scrollY > 80;
  header.classList.toggle("is-pinned", shouldPin);
}

window.addEventListener("scroll", handlePinnedHeader);
handlePinnedHeader();
