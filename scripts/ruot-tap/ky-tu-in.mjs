// Ký tự ngoài bộ Source Sans 3 (latin/latin-ext/vietnamese) mà Chrome sẽ lấy phông hệ thống (Helvetica, Lucida, Apple Symbols)
// khi in PDF — sửa 17/11/2026 cho L12 Ch.4 (pdffonts báo Helvetica ở bài 14–18).
// 1) fontsBu: chữ Hy Lạp và ≈ lấy từ phông KaTeX (đã nhúng sẵn cho công thức): thường → Math-Italic (như $\alpha$), hoa/≈ → Main.
// 2) chuanHoa: chạy trong trang trước khi đo/in — đổi chỉ số trên/dưới Unicode (10⁻¹⁵, N₀) thành <sup>/<sub>,
//    trong SVG thành <tspan baseline-shift>. Chỉ đổi cụm có ký tự U+2070–209F; bỏ qua công thức KaTeX.
// Ký tự khác không có trong cả hai bộ (☐ ∛ ⅓ ̊) thì sửa ở nguồn bài. Kiểm: pdffonts <pdf> | grep -iE 'helvetica|lucida|symbols'.
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const K = resolve(dirname(require.resolve('katex/package.json')), 'dist/fonts') + '/KaTeX_';
const ff = (file, w, ur) =>
  `@font-face{font-family:BV;font-weight:${w};src:url("${pathToFileURL(K + file + '.woff2').href}");unicode-range:${ur}}`;
const THUONG = 'U+03B1-03C9,U+03D1,U+03D5,U+03F5';
const HOA = 'U+0391-03A9,U+2248';
export const fontsBu = ff('Math-Italic', 400, THUONG) + ff('Math-BoldItalic', 700, THUONG) + ff('Main-Regular', 400, HOA) + ff('Main-Bold', 700, HOA);

export const chuanHoa = () => {
  const SUP = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁺': '+', '⁻': '−' };
  const SUB = { '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9' };
  const RUN = /[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+|[₀-₉]+/g;
  const CAN = /[⁰-₟]/;
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (w.nextNode()) { const n = w.currentNode; if (CAN.test(n.data) && !n.parentElement.closest('.katex,style,script')) nodes.push(n); }
  for (const n of nodes) {
    const svg = n.parentElement.closest('svg');
    const s = n.data; const frag = document.createDocumentFragment(); let last = 0;
    for (const mm of s.matchAll(RUN)) {
      const run = mm[0]; if (!CAN.test(run)) continue;
      const up = run[0] in SUP;
      frag.append(s.slice(last, mm.index));
      let el;
      if (svg) { el = document.createElementNS('http://www.w3.org/2000/svg', 'tspan'); el.setAttribute('baseline-shift', up ? '0.32em' : '-0.18em'); el.setAttribute('font-size', '78%'); } // 'super' của Chrome nâng quá cao → chạm nét phía trên (β⁻ bài 17)
      else el = document.createElement(up ? 'sup' : 'sub');
      el.textContent = [...run].map((c) => (up ? SUP : SUB)[c]).join('');
      frag.append(el); last = mm.index + run.length;
    }
    frag.append(s.slice(last)); n.replaceWith(frag);
  }
  return nodes.length;
};
