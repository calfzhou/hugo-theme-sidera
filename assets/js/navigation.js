// In-flow native disclosures. No script leaves every region reachable and open.
for (const [selector, query] of [
  ['.site-menu', '(min-width: 761px)'],
  ['.context-menu', '(min-width: 1231px)']
]) {
  const disclosure = document.querySelector(selector);
  if (!disclosure) continue;
  const wide = matchMedia(query);
  const update = () => { disclosure.open = wide.matches; };
  update();
  wide.addEventListener('change', update);
}
