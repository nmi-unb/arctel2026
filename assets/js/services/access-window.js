/* Janela de acesso a um link ao vivo (Teams etc.): 30min antes do início até
   30min depois — fora dela o botão fica desabilitado (visível, não clicável). */
export const JANELA_ANTES_MS = 30 * 60 * 1000;
export const JANELA_DEPOIS_MS = 30 * 60 * 1000;

export function calcularJanelaAcesso(inicio, now) {
  const abre = new Date(inicio.getTime() - JANELA_ANTES_MS);
  const fecha = new Date(inicio.getTime() + JANELA_DEPOIS_MS);
  return { dentro: now >= abre && now <= fecha, aindaNaoAbriu: now < abre };
}
