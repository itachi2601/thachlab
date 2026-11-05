// Bộ điều khiển "học sinh ảo" cho /dev/btm (dán vào javascript_tool của Browser pane, viewport 375x812).
// 1) npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --xem-thu ; mở <cổng>/dev/btm (tải lại).
// 2) Dán file này; gọi: await HSAO.mo(4)  -> mở dạng 4 + bấm "Giải từng bước" (đóng dạng khác trước).
// 3) await HSAO.chay(buoc, toi)  với buoc = dang_bai[i].buoc trong scripts/data/bai-tap-mau/<id>.json (chỉ cần
//    hoi/lua_chon/chon_buoc_ke/dap_so); chạy tới bước `toi` (1-based), trả lời đúng rồi dừng ở bước đó.
// 4) Chụp: computer screenshot scale 0.6; HSAO.cuon() cuộn .cc-split lên đầu để thấy hình dính.
// 5) Mỗi bước: chọn bước kế (chon_buoc_ke) -> nhập đáp số vào input -> hoặc chọn lua_chon đúng -> bấm ▶ (Bước sau).
window.HSAO = (() => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  // Chuẩn hoá chữ: thay KaTeX bằng mã TeX gốc, bỏ $ và khoảng trắng
  const norm = (s) => s.replace(/\$/g, '').replace(/\\[,; ]|\\%|\s+/g, '').replace(/\{,\}/g, ',').replace(/\\(dfrac|tfrac)/g, '\\frac');
  const textOf = (el) => {
    const c = el.cloneNode(true);
    c.querySelectorAll('.katex').forEach((k) => {
      const a = k.querySelector('annotation[encoding="application/x-tex"]');
      k.replaceWith(document.createTextNode(a ? a.textContent : ''));
    });
    return norm(c.textContent);
  };
  const root = () => document.querySelector('.cc-split');
  async function mo(n) {
    // đóng các dạng đang mở, mở dạng n
    const hs = [...document.querySelectorAll('button,summary')].filter((b) => /^\d\s*Dạng|^\d\s*Bài tập tự luận/.test(b.innerText.trim()));
    for (const h of hs) if (h.getAttribute('aria-expanded') === 'true') { h.click(); await sleep(300); }
    const d = [...document.querySelectorAll('button,summary')].find((b) => new RegExp('^' + n + '\\s*Dạng').test(b.innerText.trim()));
    d.click(); await sleep(600);
    const g = [...document.querySelectorAll('button')].filter((b) => b.innerText.trim() === 'Giải từng bước');
    g[g.length - 1].click(); await sleep(800);
    return !!root();
  }
  async function traLoi(b) {
    const area = document.querySelector('.cc-steps');
    // 1) chọn bước kế / lựa chọn đúng (nút .bt-choice) khớp văn bản "dung": true
    const dung = (arr) => (arr || []).filter((x) => x.dung).map((x) => norm(x.text));
    const want = [...dung(b.chon_buoc_ke), ...dung(b.lua_chon)];
    for (let k = 0; k < 4; k++) {
      const btns = [...area.querySelectorAll('button.bt-choice')];
      const hit = btns.find((x) => want.some((w) => textOf(x).includes(w.slice(0, 25)) || w.includes(textOf(x).slice(0, 25))));
      if (!hit) break;
      hit.click(); await sleep(500);
      if (area.querySelector('input')) break;
    }
    // 2) nhập đáp số
    const inp = area.querySelector('input:not([disabled])');
    if (inp && b.dap_so != null) {
      const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
      set.call(inp, String(b.dap_so).replace('.', ','));
      inp.dispatchEvent(new Event('input', { bubbles: true })); await sleep(200);
      const ok = [...area.querySelectorAll('button')].find((x) => /Kiểm tra|Xác nhận|Gửi/.test(x.innerText));
      if (ok) ok.click(); else inp.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
      await sleep(500);
    }
  }
  async function chay(buoc, toi) {
    for (let i = 1; i <= toi; i++) {
      const t = root().querySelector('.cc-step-title').innerText.slice(0, 12);
      if (!t.includes('Bước ' + i)) { console.log('lệch bước', t); }
      if (i === toi) { await traLoi(buoc[i - 1]); break; }
      await traLoi(buoc[i - 1]);
      root().querySelector('[aria-label="Bước sau"]').click(); await sleep(700);
    }
    return root().querySelector('.cc-step-title').innerText.slice(0, 20);
  }
  function cuon() { root().scrollIntoView(); }
  return { mo, chay, cuon, traLoi, textOf };
})();
