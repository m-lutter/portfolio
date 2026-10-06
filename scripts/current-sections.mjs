const escape = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));

export function lifecycle(items, name='Design lifecycle') {
  return `<ol class="lifecycle" aria-label="${escape(name)}">${items.map(item => `<li class="stage-${escape(item.state)}"${item.state === 'current' ? ' aria-current="step"' : ''}><span class="stage-marker" aria-hidden="true"></span><strong>${escape(item.label)}</strong><span>${escape(item.detail)}</span>${item.state === 'current' ? '<b class="stage-status">Current checkpoint</b>' : ''}</li>`).join('')}</ol>`;
}
