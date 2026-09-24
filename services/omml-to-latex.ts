/**
 * Chuyển công thức Office Math (OMML — công thức gõ bằng Word Alt+=, hoặc MathType
 * sau khi bấm "Convert Equations → Microsoft Office Math") sang LaTeX cho KaTeX.
 *
 * Công thức MathType để nguyên dạng OLE thì trong file .docx chỉ là ảnh WMF —
 * không đọc được ở trình duyệt; `docx-reader` sẽ đếm và báo riêng.
 */

// export: dùng lại ở latex-to-omml.ts (chiều ngược) để hai bên khớp nhau, khỏi lệch bảng.
export const FUNCS = new Set([
  "sin", "cos", "tan", "cot", "sec", "csc", "sinh", "cosh", "tanh", "coth",
  "arcsin", "arccos", "arctan", "log", "ln", "lg", "exp", "lim", "max", "min",
  "det", "deg", "gcd", "sup", "inf",
]);

export const NARY: Record<string, string> = {
  "∑": "\\sum", "∏": "\\prod", "∐": "\\coprod",
  "∫": "\\int", "∬": "\\iint", "∭": "\\iiint",
  "∮": "\\oint", "⋃": "\\bigcup", "⋂": "\\bigcap",
};

export const ACCENTS: Record<string, string> = {
  "⃗": "\\vec", "⃑": "\\vec", "→": "\\vec",
  "̂": "\\hat", "̃": "\\tilde", "̄": "\\bar", "̅": "\\overline",
  "̇": "\\dot", "̈": "\\ddot", "̌": "\\check",
  "́": "\\acute", "̀": "\\grave",
};

export const DELIMS: Record<string, string> = {
  "": ".", "(": "(", ")": ")", "[": "[", "]": "]",
  "{": "\\{", "}": "\\}", "|": "|", "‖": "\\|",
  "⟨": "\\langle", "⟩": "\\rangle", "⌊": "\\lfloor", "⌋": "\\rfloor",
  "⌈": "\\lceil", "⌉": "\\rceil",
};

/**
 * Ký hiệu Unicode Word hay chèn → lệnh LaTeX tương ứng.
 * Giữ dạng cặp thô (export) để latex-to-omml.ts dùng lại theo chiều ngược;
 * SYMBOLS bên dưới là bản đã biên dịch regex, chỉ dùng nội bộ file này.
 */
export const SYMBOL_ENTRIES: [string, string][] = Object.entries({
  "α": "\\alpha ", "β": "\\beta ", "γ": "\\gamma ", "δ": "\\delta ", "ε": "\\varepsilon ",
  "ζ": "\\zeta ", "η": "\\eta ", "θ": "\\theta ", "ι": "\\iota ", "κ": "\\kappa ",
  "λ": "\\lambda ", "μ": "\\mu ", "ν": "\\nu ", "ξ": "\\xi ", "π": "\\pi ",
  "ρ": "\\rho ", "σ": "\\sigma ", "τ": "\\tau ", "υ": "\\upsilon ", "φ": "\\varphi ",
  "ϕ": "\\phi ", "χ": "\\chi ", "ψ": "\\psi ", "ω": "\\omega ",
  "Γ": "\\Gamma ", "Δ": "\\Delta ", "Θ": "\\Theta ", "Λ": "\\Lambda ", "Ξ": "\\Xi ",
  "Π": "\\Pi ", "Σ": "\\Sigma ", "Φ": "\\Phi ", "Ψ": "\\Psi ", "Ω": "\\Omega ",
  "×": "\\times ", "÷": "\\div ", "±": "\\pm ", "∓": "\\mp ", "⋅": "\\cdot ", "·": "\\cdot ",
  "≤": "\\le ", "≥": "\\ge ", "≠": "\\ne ", "≈": "\\approx ", "≡": "\\equiv ", "∼": "\\sim ",
  "∞": "\\infty ", "∈": "\\in ", "∉": "\\notin ", "⊂": "\\subset ", "∪": "\\cup ", "∩": "\\cap ",
  "→": "\\rightarrow ", "←": "\\leftarrow ", "↔": "\\leftrightarrow ", "⇒": "\\Rightarrow ",
  "⇔": "\\Leftrightarrow ", "∆": "\\Delta ", "∂": "\\partial ", "∇": "\\nabla ",
  "√": "\\sqrt ", "°": "^{\\circ}", "∥": "\\parallel ", "⊥": "\\perp ", "∠": "\\angle ",
  "′": "'", "″": "''", "…": "\\dots ", "ℏ": "\\hbar ", "∅": "\\varnothing ",
  " ": " ",
});
const SYMBOLS: [RegExp, string][] = SYMBOL_ENTRIES.map(([k, v]) => [new RegExp(k, "g"), v]);

/** Văn bản trong công thức → LaTeX an toàn. */
export function mathText(raw: string): string {
  let s = raw.replace(/\\/g, "\\backslash ");
  s = s.replace(/([%&#$_{}])/g, "\\$1");
  for (const [re, tex] of SYMBOLS) s = s.replace(re, tex);
  return s;
}

function els(parent: Element): Element[] {
  return Array.from(parent.children);
}

function child(parent: Element, name: string): Element | null {
  return els(parent).find((e) => e.localName === name) ?? null;
}

function childrenNamed(parent: Element, name: string): Element[] {
  return els(parent).filter((e) => e.localName === name);
}

/** Giá trị thuộc tính m:val của thẻ con (vd <m:chr m:val="∑"/>). */
function propVal(parent: Element, tag: string): string | null {
  const pr = els(parent).find((e) => e.localName.endsWith("Pr"));
  const node = pr ? child(pr, tag) : child(parent, tag);
  if (!node) return null;
  for (const attr of Array.from(node.attributes)) {
    if (attr.localName === "val") return attr.value;
  }
  return "";
}

/** Bọc ngoặc nhọn khi cần làm đối số của \frac, ^, _… */
function arg(tex: string): string {
  const s = tex.trim();
  if (s.length === 1 || /^\\[a-zA-Z]+$/.test(s)) return s;
  return `{${s}}`;
}

function convertChildren(parent: Element): string {
  return els(parent).map(convert).join("");
}

/** Nội dung của <m:e>, <m:num>… (thẻ bọc một biểu thức con). */
function part(parent: Element, name: string): string {
  const node = child(parent, name);
  return node ? convertChildren(node) : "";
}

function convert(el: Element): string {
  switch (el.localName) {
    case "t":
      return mathText(el.textContent ?? "");
    case "r":
      return childrenNamed(el, "t").map((t) => mathText(t.textContent ?? "")).join("");
    case "f": {
      const type = propVal(el, "type");
      const num = part(el, "num");
      const den = part(el, "den");
      if (type === "lin") return `${arg(num)}/${arg(den)}`;
      // Luôn đóng ngoặc nhọn cho phân số: người dùng còn sửa tay trong trình soạn,
      // `\frac{s}{t}` dễ đọc hơn `\frac st`.
      if (type === "noBar") return `\\binom{${num}}{${den}}`;
      return `\\frac{${num}}{${den}}`;
    }
    case "sSup":
      return `${arg(part(el, "e"))}^${arg(part(el, "sup"))}`;
    case "sSub":
      return `${arg(part(el, "e"))}_${arg(part(el, "sub"))}`;
    case "sSubSup":
      return `${arg(part(el, "e"))}_${arg(part(el, "sub"))}^${arg(part(el, "sup"))}`;
    case "sPre":
      return `{}_${arg(part(el, "sub"))}^${arg(part(el, "sup"))}${arg(part(el, "e"))}`;
    case "rad": {
      const hideDeg = propVal(el, "degHide");
      const deg = part(el, "deg");
      const body = arg(part(el, "e"));
      return hideDeg === "1" || hideDeg === "on" || !deg.trim()
        ? `\\sqrt${body}`
        : `\\sqrt[${deg}]${body}`;
    }
    case "nary": {
      const chr = propVal(el, "chr") ?? "∫";
      const op = NARY[chr] ?? "\\int";
      const sub = part(el, "sub");
      const sup = part(el, "sup");
      const body = part(el, "e");
      return `${op}${sub.trim() ? `_${arg(sub)}` : ""}${sup.trim() ? `^${arg(sup)}` : ""}{${body}}`;
    }
    case "d": {
      const beg = DELIMS[propVal(el, "begChr") ?? "("] ?? "(";
      const end = DELIMS[propVal(el, "endChr") ?? ")"] ?? ")";
      const sep = propVal(el, "sepChr") || ",";
      const inner = childrenNamed(el, "e").map(convertChildren).join(sep);
      return `\\left${beg}${inner}\\right${end}`;
    }
    case "func": {
      const nameNode = child(el, "fName");
      const raw = nameNode ? convertChildren(nameNode).trim() : "";
      const fn = FUNCS.has(raw) ? `\\${raw}` : raw;
      return `${fn}\\left(${part(el, "e")}\\right)`;
    }
    case "limLow": {
      const base = part(el, "e").trim();
      const lim = part(el, "lim");
      const plain = base.replace(/^\\/, "");
      if (FUNCS.has(plain)) return `\\${plain}_${arg(lim)}`;
      return `\\underset${arg(lim)}${arg(base)}`;
    }
    case "limUpp":
      return `\\overset${arg(part(el, "lim"))}${arg(part(el, "e"))}`;
    case "acc": {
      const chr = propVal(el, "chr") ?? "̂";
      return `${ACCENTS[chr] ?? "\\hat"}${arg(part(el, "e"))}`;
    }
    case "bar":
      return `${propVal(el, "pos") === "bot" ? "\\underline" : "\\overline"}${arg(part(el, "e"))}`;
    case "groupChr":
      return arg(part(el, "e"));
    case "box":
    case "borderBox":
      return part(el, "e");
    case "m": {
      const rows = childrenNamed(el, "mr")
        .map((r) => childrenNamed(r, "e").map(convertChildren).join(" & "))
        .join(" \\\\ ");
      return `\\begin{matrix}${rows}\\end{matrix}`;
    }
    case "eqArr": {
      const rows = childrenNamed(el, "e").map(convertChildren).join(" \\\\ ");
      return `\\begin{aligned}${rows}\\end{aligned}`;
    }
    case "phant":
      return "";
    case "rPr":
    case "ctrlPr":
      return "";
    default:
      if (el.localName.endsWith("Pr")) return ""; // các khối thuộc tính
      return convertChildren(el);
  }
}

/** <m:oMath> / <m:oMathPara> → chuỗi LaTeX (chưa kèm dấu $). */
export function ommlToLatex(node: Element): string {
  return convertChildren(node).replace(/\s+/g, " ").trim();
}
