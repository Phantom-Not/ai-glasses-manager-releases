(() => {
  'use strict';
  const viewer = document.querySelector('.photo-viewer');
  if (!viewer || typeof viewer.showModal !== 'function') return;
  const image = viewer.querySelector('#photo-viewer-image');
  const title = viewer.querySelector('#photo-viewer-title');
  const caption = viewer.querySelector('#photo-viewer-caption');
  const status = viewer.querySelector('.photo-viewer-status');
  const close = viewer.querySelector('.photo-viewer-close');
  let opener = null;
  let request = 0;

  document.addEventListener('click', event => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const link = event.target instanceof Element ? event.target.closest('.filter-photo a') : null;
    if (!link || viewer.open) return;
    const preview = link.querySelector('img');
    const card = link.closest('.filter-card');
    if (!preview || !card) return;
    event.preventDefault();
    opener = link;
    const current = ++request;
    title.textContent = card.querySelector('h3').textContent;
    caption.textContent = card.querySelector('p').textContent;
    viewer.dataset.filter = title.textContent;
    status.textContent = viewer.dataset.loading;
    status.hidden = false;
    image.style.opacity = '0';
    image.alt = preview.alt;
    image.width = Number(preview.getAttribute('width'));
    image.height = Number(preview.getAttribute('height'));
    image.loading = 'eager';
    image.src = link.href;
    viewer.showModal();
    document.documentElement.classList.add('photo-viewer-open');
    close.focus({ preventScroll: true });
    image.decode().then(() => {
      if (current !== request || !viewer.open) return;
      image.style.opacity = '1';
      status.hidden = true;
    }).catch(() => {
      if (current !== request || !viewer.open) return;
      status.textContent = viewer.dataset.error;
    });
  });

  close.addEventListener('click', () => viewer.close());
  viewer.addEventListener('click', event => {
    if (event.target !== viewer) return;
    const bounds = viewer.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) viewer.close();
  });
  viewer.addEventListener('close', () => {
    ++request;
    document.documentElement.classList.remove('photo-viewer-open');
    if (opener && opener.isConnected) opener.focus({ preventScroll: true });
  });
})();
