const filters = [...document.querySelectorAll('[data-filter]')];
const projects = [...document.querySelectorAll('[data-category]')];
const groups = [...document.querySelectorAll('[data-project-group]')];
const count = document.querySelector('#filter-status');
filters.forEach(button => button.addEventListener('click', () => {
  const category = button.dataset.filter;
  filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
  projects.forEach(project => { project.hidden = category !== 'all' && project.dataset.category !== category; });
  groups.forEach(group => {
    group.hidden = ![...group.querySelectorAll('[data-category]')].some(project => !project.hidden);
  });
  const visible = projects.filter(project => !project.hidden).length;
  if (count) count.textContent = `${visible} ${visible === 1 ? 'project' : 'projects'} shown.`;
}));
