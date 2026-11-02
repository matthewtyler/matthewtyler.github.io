// Exercise the browser controller against the real publication/topic data.
// Run with Node; no extra packages are needed.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '../..');
const publications = JSON.parse(fs.readFileSync(path.join(root, '_data/publications.json')));
const metadata = JSON.parse(fs.readFileSync(path.join(root, '_data/research_topics.json')));
const source = fs.readFileSync(path.join(root, 'assets/js/research-filter.js'), 'utf8');
const buttons = [{ id: 'all', label: 'All research' }, ...metadata.topics].map(topic => ({
  dataset: { topic: topic.id }, textContent: topic.label, attributes: {},
  setAttribute(name, value) { this.attributes[name] = value; },
  addEventListener(event, listener) { this[event] = listener; }
}));
const status = { textContent: '' };
const controls = {
  hidden: true,
  querySelectorAll: () => buttons,
  querySelector: () => status
};
const sections = publications.map(section => {
  const items = section.items.map(paper => ({
    dataset: { topics: (metadata.papers[paper.title] || []).join(' ') }, hidden: false
  }));
  const count = {}, empty = { hidden: true }, navCount = {};
  return {
    items, count, empty, navCount, anchor: section.anchor,
    querySelectorAll: () => items,
    querySelector: selector => ({
      h3: { id: section.anchor }, '.section-count': count, '.filter-empty': empty
    })[selector]
  };
});
// Future papers without metadata must remain available under All research.
sections[0].items.push({ dataset: { topics: '' }, hidden: false });
const research = {
  querySelectorAll: () => sections,
  querySelector: selector => selector === '.research-filter' ? controls
    : sections.find(section => selector.includes(`#${section.anchor}`)).navCount
};
vm.runInNewContext(source, { document: { getElementById: () => research } });
assert.equal(controls.hidden, false);
const total = sections.flatMap(section => section.items).length;
assert.equal(status.textContent, `Showing all ${total} items.`);
for (const button of buttons) {
  button.click();
  let matches = 0;
  for (const section of sections) {
    const expected = section.items.filter(item => button.dataset.topic === 'all'
      || item.dataset.topics.split(' ').includes(button.dataset.topic));
    assert.deepEqual(section.items.filter(item => !item.hidden), expected);
    assert.equal(section.count.textContent, `${expected.length} ${expected.length === 1 ? 'item' : 'items'}`);
    assert.equal(section.navCount.textContent, expected.length);
    assert.equal(section.empty.hidden, expected.length > 0);
    matches += expected.length;
  }
  assert.equal(buttons.filter(b => b.attributes['aria-pressed'] === 'true').length, 1);
  assert.equal(button.attributes['aria-pressed'], 'true');
  if (button.dataset.topic !== 'all') {
    assert.equal(status.textContent, `Showing ${matches} of ${total} items: ${button.textContent}.`);
  }
}
buttons[0].click();
assert(sections.every(section => section.items.every(item => !item.hidden)));
assert(sections.every(section => section.empty.hidden));
// The script is harmless on a page without research.
vm.runInNewContext(source, { document: { getElementById: () => null } });
console.log('Research filters: every topic, counts, empty sections, reset, and untagged papers passed.');
