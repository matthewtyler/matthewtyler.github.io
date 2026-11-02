// Section highlighting is optional; every navigation link works without JavaScript.
(() => {
  const links = [...document.querySelectorAll('[data-section]')];
  const research = document.getElementById('research');
  const header = document.querySelector('.site-header');
  if (!research || !header) return;
  let pending = false;
  function update() {
    const headerHeight = getComputedStyle(header).position === 'sticky' ? header.offsetHeight : 0;
    const active = research.getBoundingClientRect().top <= headerHeight + 32 ? 'research' : 'about';
    links.forEach(link => {
      if (link.dataset.section === active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    pending = false;
  }
  function schedule() {
    if (!pending) {
      pending = true;
      requestAnimationFrame(update);
    }
  }
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  update();
})();
