const backToTopButton = document.getElementById("back-to-top");

function handleBackToTopVisibility() {
  const hasScrolledPastThreshold = window.scrollY > 300;
  backToTopButton.classList.toggle("is-visible", hasScrolledPastThreshold);
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

backToTopButton.addEventListener("click", scrollToTop);
window.addEventListener("scroll", handleBackToTopVisibility);
handleBackToTopVisibility();
