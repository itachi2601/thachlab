// Bộ sửa TỰ ĐỘNG các lỗi mất định dạng "chắc chắn" (độ C, đơn vị mũ, số mũ âm dính liền, chỉ số dưới, LaTeX vỡ,
// tiền tố "Câu 11."/"[VD]"). Ca mơ hồ KHÔNG sửa, trả về trong `nghiNgo` để thầy duyệt.
// Dùng chung cho script sửa hàng loạt (scripts/sua-dinh-dang-hang-loat.mts) — một hàm, áp cho CẢ question_bank lẫn exams.questions.

export type MaSua = "doC" | "doMath" | "donViMu" | "muAm" | "muSauDau" | "chiSo" | "vecVo" | "phanTram" | "tienTo";
export type KetQua = { text: string; sua: MaSua[]; nghiNgo: string[] };

const NHIET = /nhiệt|sôi|nóng chảy|đông đặc|°|độ C|\bt\s*=|t_|ấm|lạnh|thể lỏng|thể rắn|thể khí|nhiệt kế|đun|hơi nước|nước đá|môi trường/i;
const DV = String.raw`(?:Pa|J|N|W|V|Hz|mol|kg|g|m\/s|m|C|T|Ω|F|K|eV|A|s|lít|nm|cm|mm|km|kWh|electron|êlectron)`;

/** Áp fn lên phần NGOÀI $…$ và ngoài thẻ HTML; fm lên phần trong $…$. */
function tach(s: string, fn: (t: string) => string, fm: (t: string) => string): string {
  const out: string[] = [];
  const re = /(\$\$[\s\S]*?\$\$|\$[^$]*\$|<[^>]*>)/g;
  let last = 0;
  for (let m; (m = re.exec(s)); ) {
    out.push(fn(s.slice(last, m.index)));
    out.push(m[0].startsWith("$") ? fm(m[0]) : m[0]);
    last = m.index + m[0].length;
  }
  out.push(fn(s.slice(last)));
  return out.join("");
}

export function suaChuoi(input: string, ngu?: { canhNhiet?: boolean; dauCau?: boolean }): KetQua {
  const sua = new Set<MaSua>();
  const nghiNgo: string[] = [];
  const canhNhiet = ngu?.canhNhiet ?? NHIET.test(input);
  let s = input;
  const rep = (t: string, re: RegExp, by: string | ((...a: string[]) => string), ma: MaSua) => {
    const n = t.replace(re, by as never);
    if (n !== t) sua.add(ma);
    return n;
  };

  // Tiền tố đầu câu (chỉ ở trường đề bài)
  if (ngu?.dauCau) {
    if (/^\s*Câu\s*\d+\s*\([^)]*\)\s*[.:]/i.test(s)) nghiNgo.push("tiền tố có nguồn trong ngoặc: " + s.slice(0, 40));
    else s = rep(s, /^\s*(?:Câu\s*\d+\s*[.:]|\[(?:NB|TH|VD|VDC)\])\s*/i, "", "tienTo");
  }

  s = tach(
    s,
    (t) => {
      // Độ C mất dấu: "40,00C" → "40,0 °C", "300C" → "30 °C" (chỉ khi câu nói về nhiệt)
      t = t.replace(/(?<![\d.,A-Za-z])(\d{1,3}(?:[.,]\d+)?)0C(?![A-Za-z0-9])/g, (m, a) => {
        if (!canhNhiet) { nghiNgo.push("độ C ngoài ngữ cảnh nhiệt: " + m); return m; }
        sua.add("doC");
        return `${a} °C`;
      });
      // Đơn vị mũ: m/s2, cm3, m2, kg/m3 (đơn vị chiều dài/thời gian ngay sau số hoặc "/")
      t = rep(t, /(?<=\d\s?|\/)(m|cm|dm|mm|km)([23])(?![\d\w])/g, (_m, u, k) => `${u}${k === "2" ? "²" : "³"}`, "donViMu");
      t = rep(t, /(?<=\/)(s|h)2(?![\d\w])/g, (_m, u) => `${u}²`, "donViMu");
      // Số mũ âm dính liền: "1,6.10-19 C", "10 – 4 N", "(10-9 N)"
      t = t.replace(new RegExp(String.raw`(?<![\d,])(\d+(?:,\d+)?\s?[.×·x]\s?|\()?10\s?[-−–‒]\s?(\d{1,2})(?=\s*${DV}\b|\s*\))`, "g"), (m, pre, k) => {
        if (!pre && /\s/.test(m)) { nghiNgo.push("10 - k có dấu cách, không có hệ số: " + m); return m; }
        sua.add("muAm");
        return `${pre ?? ""}$10^{-${k}}$`;
      });
      // Số mũ dương sau dấu nhân: "x.1018 electron", "2.105 Pa", "1,5.106 J"
      t = rep(t, new RegExp(String.raw`(?<=(?:\d|\b[xyab])\s?[.×·]\s?)10([2-9]|1\d|2\d|3\d)(?=\s*${DV}\b|\s*[(;,.]|\s*$)`, "g"), (_m, k) => `$10^{${k}}$`, "muSauDau");
      // Số mũ dương KHÔNG có hệ số ("105 Pa") — mơ hồ, chỉ báo
      for (const m of t.matchAll(new RegExp(String.raw`(?<![\d,.^{$])10([4-9]|1\d|2\d)\s*(?:Pa|J|N|W|Hz|kg|eV|electron)\b`, "g")))
        nghiNgo.push("số mũ không hệ số: " + m[0]);
      // Chỉ số dưới viết liền: "v0 = 10", "R1 = 8", "T2 = 4T1", "m1, m2"
      t = rep(t, /(?<![\w$\\_{&#;])([vtpVTSRxNmqUIEFWhℓ])([0-2])(?=\s*[=,;:)]|\s+(?:và|nối)(?=\s)|\s*$)/g, (_m, a, k) => `$${a}_${k}$`, "chiSo");
      return t;
    },
    (m) => {
      let r = m;
      // Độ trong công thức: 90^0, 30^{0}, 4^oC → ^\circ (trừ cơ số 10: có thể là 10⁰ = 1)
      r = rep(r, /(?<![\d.,])(?!10\^)(\d+(?:[.,]\d+)?)\s?\^\s?\{?\s?(?:0|o)\s?\}?(?![\d])/g, (_x, a) => `${a}^\\circ `, "doMath");
      r = rep(r, /\\vec([A-Za-z])/g, (_x, a) => `\\vec ${a}`, "vecVo");
      r = rep(r, /(?<!\\)%/g, "\\%", "phanTram");
      return r.replace(/\^\\circ \s*C/g, "^\\circ\\text{C}").replace(/\^\\circ (?=[}$\s,.)])/g, "^\\circ");
    },
  );
  return { text: s, sua: [...sua], nghiNgo };
}

const BO_QUA = /^(image|images|img|src|url|figure|svg|id|bank_id|type|qtype|answer|correct|key|level|difficulty)$/i;

/** Sửa mọi chuỗi trong một câu hỏi (question/options/statements/explanation…); trả về bản mới + mã sửa + nghi ngờ. */
export function suaCau(q: unknown): { q: unknown; sua: MaSua[]; nghiNgo: string[] } {
  const sua = new Set<MaSua>();
  const nghi: string[] = [];
  const canhNhiet = NHIET.test(JSON.stringify(q));
  const walk = (v: unknown, key: string): unknown => {
    if (typeof v === "string") {
      const r = suaChuoi(v, { canhNhiet, dauCau: key === "question" });
      r.sua.forEach((x) => sua.add(x));
      nghi.push(...r.nghiNgo);
      return r.text;
    }
    if (Array.isArray(v)) return v.map((x) => walk(x, key));
    if (v && typeof v === "object")
      return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, BO_QUA.test(k) ? x : walk(x, k)]));
    return v;
  };
  return { q: walk(q, ""), sua: [...sua], nghiNgo: nghi };
}
