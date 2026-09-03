import { createModalController } from "../components/notice-board.js";

document.addEventListener("DOMContentLoaded", () => {
  const openButton = document.getElementById("referencias-btn");
  const overlay = document.getElementById("referencias-modal");
  if (openButton && overlay) {
    createModalController(overlay, openButton);
  }

  /* lesson-accordion.js insere o aviso "links ficam disponíveis..." logo
     após [data-lesson-accordion] — nesse módulo, ele deve ficar depois do
     pseudo-accordion "Livros e Referências", não antes. */
  const notice = document.querySelector(".lesson-accordion__notice");
  const referenciasAccordion = document.getElementById("referencias-accordion");
  if (notice && referenciasAccordion) {
    referenciasAccordion.insertAdjacentElement("afterend", notice);
  }
});
