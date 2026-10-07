// Chạy trong trang trước khi in: dựng công thức, mã QR, rồi dàn trang bằng Paged.js.
(async () => {
  try {
    renderMathInElement(document.body, {
      delimiters: [{ left: '$$', right: '$$', display: true }, { left: '$', right: '$', display: false }],
      throwOnError: false, strict: 'ignore', output: 'html',
    });
    document.querySelectorAll('.qr[data-url]').forEach(el => {
      const qr = qrcode(0, 'M'); qr.addData(el.dataset.url); qr.make();
      el.innerHTML = qr.createSvgTag({ cellSize: 3, margin: 0, scalable: true });
    });
    await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.decode ? i.decode().catch(() => {}) : 0));
    await window.PagedPolyfill.preview();
    const st = parseInt(document.body.dataset.start || '1', 10);
    document.querySelectorAll('.pagedjs_page').forEach((p, i) => { p.style.counterReset = 'page ' + (st + i - 1); });
    window.__bookDone = true;
  } catch (e) { window.__bookError = String(e && e.stack || e); }
})();
