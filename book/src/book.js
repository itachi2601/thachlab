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
    // Trang bài học còn trống ≥ 28 mm ở đáy → lấp bằng ô "Ghi chép" ca-rô (không để giấy trắng vô ích)
    if (document.querySelector('section.lesson')) document.querySelectorAll('.pagedjs_page').forEach(p => {
      const area = p.querySelector('.pagedjs_page_content'); if (!area || p.querySelector('.free')) return;
      const A = area.getBoundingClientRect(), P = p.getBoundingClientRect();
      let lb = A.top;
      const take = r => { if (r.height > 0 && r.width > 0 && r.bottom > lb && r.bottom <= A.bottom + 2) lb = r.bottom; };
      area.querySelectorAll('*').forEach(e => {   // khung có viền/nền, hình
        if ([...e.classList].some(c => c.startsWith('pagedjs'))) return;
        const cs = getComputedStyle(e);
        if (cs.display === 'none' || cs.position === 'absolute') return;
        if (/^(IMG|svg)$/.test(e.tagName) || parseFloat(cs.borderBottomWidth) > 0 || parseFloat(cs.borderLeftWidth) > 0 || cs.backgroundColor !== 'rgba(0, 0, 0, 0)') take(e.getBoundingClientRect());
      });
      const tw = document.createTreeWalker(area, NodeFilter.SHOW_TEXT), rg = document.createRange();
      for (let n; (n = tw.nextNode());) if (n.textContent.trim()) { rg.selectNodeContents(n); take(rg.getBoundingClientRect()); }
      const mm = 3.7795, free = (A.bottom - lb) / mm - 5;
      if (free < 28) return;
      const d = document.createElement('div'); d.className = 'fillnote';
      Object.assign(d.style, { position: 'absolute', left: (A.left - P.left) + 'px', top: (lb - P.top + 4 * mm) + 'px', width: A.width + 'px', height: Math.floor(free) + 'mm' });
      d.innerHTML = '<span>Ghi chép</span>';
      if (getComputedStyle(p).position === 'static') p.style.position = 'relative';
      p.appendChild(d);
    });
    window.__bookDone = true;
  } catch (e) { window.__bookError = String(e && e.stack || e); }
})();
