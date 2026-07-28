import { initModuleAccordion } from "../components/module-accordion.js";
import { initNoticeBoard } from "../components/notice-board.js";
import { initCalendario } from "../components/calendario.js";

export function initHomePage() {
  initModuleAccordion();
  initNoticeBoard();
  initCalendario();
}
