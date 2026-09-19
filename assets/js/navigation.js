// A disclosure, not a modal: native keyboard behavior and no focus trap.
// With JavaScript unavailable the server-rendered navigation stays open.
const menu = document.querySelector('.site-menu');
const desktop = window.matchMedia('(min-width: 900px)');
function setNavigationLayout() {
  menu.open = desktop.matches;
}
setNavigationLayout();
desktop.addEventListener('change', setNavigationLayout);
