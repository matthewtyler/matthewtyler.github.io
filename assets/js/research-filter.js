// Progressive enhancement: all citations and topic labels render without JavaScript.
(() => {
  const research = document.getElementById('research');
  if (!research) return;
  const controls = research.querySelector('.research-filter');
  if (!controls) return;
  const buttons = [...controls.querySelectorAll('button[data-topic]')];
  const status = controls.querySelector('.filter-status');
  const sections = [...research.querySelectorAll('.research-section')].map(section => {
    const heading = section.querySelector('h3');
    return {
      items: [...section.querySelectorAll('.paper-list > li')],
      count: section.querySelector('.section-count'),
      empty: section.querySelector('.filter-empty'),
      navCount: research.querySelector(`.section-nav a[href="#${heading.id}"] .count`)
    };
  });
  const total = sections.reduce((sum, section) => sum + section.items.length, 0);

  function applyFilter(button) {
    const topic = button.dataset.topic;
    let matches = 0;
    sections.forEach(section => {
      let count = 0;
      section.items.forEach(item => {
        const visible = topic === 'all' || item.dataset.topics.split(/\s+/).includes(topic);
        item.hidden = !visible;
        if (visible) count += 1;
      });
      matches += count;
      section.count.textContent = `${count} ${count === 1 ? 'item' : 'items'}`;
      section.navCount.textContent = count;
      section.empty.hidden = count !== 0;
    });
    buttons.forEach(candidate => candidate.setAttribute('aria-pressed', String(candidate === button)));
    status.textContent = topic === 'all'
      ? `Showing all ${total} items.`
      : `Showing ${matches} of ${total} items: ${button.textContent.trim()}.`;
  }

  buttons.forEach(button => button.addEventListener('click', () => applyFilter(button)));
  applyFilter(buttons.find(button => button.dataset.topic === 'all'));
  controls.hidden = false;
})();
