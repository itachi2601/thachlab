/**
 * Chuyển công thức LaTeX (dạng `$...$`/`$$...$$` lưu trong body_html) sang OMML
 * (Office Math) để nhúng vào file .docx — chiều ngược của omml-to-latex.ts.
 * Dùng lại đúng các bảng ký hiệu/hàm của file đó cho khớp, khỏi lệch.
 *
 * Không cần phủ hết cú pháp LaTeX: chỉ cần đủ cho công thức Vật lí THPT thường
 * gặp (phân số, căn, chỉ số trên/dưới, tổng/tích phân, vector, Hy Lạp…). Công
 * thức nào parse lỗi thì rơi về chèn nguyên văn LaTeX dạng chữ thường — không
 * làm hỏng cả file .docx.
 */

import { DELIMS, FUNCS, NARY, SYMBOL_ENTRIES } from "./omml-to-latex";

// ---------- Bảng tra ngược ----------

const SYMBOL_CMD_TO_CHAR = new Map<string, string>();
for (const [ch, tex] of SYMBOL_ENTRIES) {
  const cmd = tex.trim();
  if (cmd.startsWith("\\") && !SYMBOL_CMD_TO_CHAR.has(cmd)) SYMBOL_CMD_TO_CHAR.set(cmd, ch);
}

const NARY_CMD_TO_CHR = new Map<string, string>();
for (const [chr, cmd] of Object.entries(NARY)) NARY_CMD_TO_CHR.set(cmd.slice(1), chr); // bỏ "\"

const ACCENT_CMD_TO_CHR: Record<string, string> = {
  vec: "⃗", hat: "̂", tilde: "̃", dot: "̇", ddot: "̈", check: "̌", acute: "́", grave: "̀",
};

// beg/end delimiter: token LaTeX (chữ trong \left / \right) -> ký tự OMML thật.
const DELIM_LATEX_TO_CHAR: Record<string, string> = { ".": "" };
for (const [ch, tex] of Object.entries(DELIMS)) {
  const key = tex.startsWith("\\") ? tex.slice(1) : tex;
  if (!(key in DELIM_LATEX_TO_CHAR)) DELIM_LATEX_TO_CHAR[key] = ch;
}

// Lệnh chỉ ảnh hưởng khoảng cách/định dạng, bỏ qua an toàn khi gặp trong công thức.
const SKIP_CMDS = new Set([",", ";", "!", " ", "quad", "qquad", "noindent", "par", "displaystyle", "textstyle", "limits", "nolimits"]);
const UPRIGHT_TEXT_CMDS = new Set(["text", "mathrm", "operatorname"]);

// ---------- Tokenizer ----------

type Token =
  | { t: "cmd"; name: string }
  | { t: "char"; v: string }
  | { t: "brace"; v: "{" | "}" }
  | { t: "sup" }
  | { t: "sub" };

function tokenize(src: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    if (c === "\\") {
      const j = i + 1;
      if (j < src.length && /[a-zA-Z]/.test(src[j])) {
        let k = j;
        while (k < src.length && /[a-zA-Z]/.test(src[k])) k++;
        tokens.push({ t: "cmd", name: src.slice(j, k) });
        i = k;
        if (src[i] === " ") i++; // khoảng trắng ngay sau control word bị LaTeX nuốt
      } else if (j < src.length) {
        tokens.push({ t: "cmd", name: src[j] }); // control symbol: \{, \}, \\, \,, \; …
        i = j + 1;
      } else {
        i++;
      }
      continue;
    }
    if (c === "{" || c === "}") {
      tokens.push({ t: "brace", v: c });
      i++;
      continue;
    }
    if (c === "^") {
      tokens.push({ t: "sup" });
      i++;
      continue;
    }
    if (c === "_") {
      tokens.push({ t: "sub" });
      i++;
      continue;
    }
    if (c === " " || c === "\n" || c === "\t" || c === "\r") {
      i++;
      continue;
    }
    if (c === "&") {
      i++; // dấu căn cột trong matrix/aligned — bỏ qua ở mức đơn giản
      continue;
    }
    tokens.push({ t: "char", v: c });
    i++;
  }
  return tokens;
}

// ---------- AST ----------

type Node =
  | { k: "char"; v: string }
  | { k: "func"; name: string }
  | { k: "frac"; num: Node[]; den: Node[]; kind: "bar" | "noBar" }
  | { k: "sqrt"; deg?: Node[]; body: Node[] }
  | { k: "delim"; beg: string; end: string; body: Node[] }
  | { k: "nary"; chr: string; sub?: Node[]; sup?: Node[]; e?: Node[] }
  | { k: "acc"; chr: string; body: Node[] }
  | { k: "bar"; pos: "top" | "bot"; body: Node[] }
  | { k: "sup"; base: Node[]; exp: Node[] }
  | { k: "sub"; base: Node[]; sub: Node[] }
  | { k: "subsup"; base: Node[]; sub: Node[]; exp: Node[] };

interface Cursor {
  tokens: Token[];
  pos: number;
}

function peek(c: Cursor): Token | undefined {
  return c.tokens[c.pos];
}
function next(c: Cursor): Token | undefined {
  return c.tokens[c.pos++];
}
function isBrace(t: Token | undefined, v: "{" | "}"): boolean {
  return !!t && t.t === "brace" && t.v === v;
}

/** `{...}` (khớp ngoặc) hoặc, nếu không có `{`, một atom đơn (`\frac12` kiểu viết tắt). */
function parseArgGroup(c: Cursor): Node[] {
  if (isBrace(peek(c), "{")) {
    next(c);
    const nodes: Node[] = [];
    while (c.pos < c.tokens.length && !isBrace(peek(c), "}")) nodes.push(parseAtomWithScripts(c));
    if (isBrace(peek(c), "}")) next(c);
    return nodes;
  }
  return [parseAtomWithScripts(c)];
}

/** Một nguyên tử: ký tự, lệnh có cấu trúc (\frac, \sqrt, \left…), hoặc nhóm `{...}` trần. */
function parseAtom(c: Cursor): Node {
  const tok = next(c);
  if (!tok) return { k: "char", v: "" };

  if (tok.t === "brace" && tok.v === "{") {
    const nodes: Node[] = [];
    while (c.pos < c.tokens.length && !isBrace(peek(c), "}")) nodes.push(parseAtomWithScripts(c));
    if (isBrace(peek(c), "}")) next(c);
    // Nhóm 1 phần tử coi như chính phần tử đó (khỏi lồng thừa); nhiều phần tử
    // thì gộp lại bằng một dấu ngoặc ẩn — dùng delim rỗng để giữ thành 1 khối.
    return nodes.length === 1 ? nodes[0] : { k: "delim", beg: "", end: "", body: nodes };
  }

  if (tok.t === "char") return { k: "char", v: tok.v };

  if (tok.t === "cmd") {
    const name = tok.name;
    if (SKIP_CMDS.has(name)) return parseAtom(c); // bỏ qua, đọc tiếp atom kế
    if (name === "\\") return { k: "char", v: "" }; // \\ xuống dòng — không có ý nghĩa trong 1 công thức inline

    if (name === "frac" || name === "dfrac" || name === "tfrac") {
      const num = parseArgGroup(c);
      const den = parseArgGroup(c);
      return { k: "frac", num, den, kind: "bar" };
    }
    if (name === "binom") {
      const num = parseArgGroup(c);
      const den = parseArgGroup(c);
      return { k: "frac", num, den, kind: "noBar" };
    }
    if (name === "sqrt") {
      let deg: Node[] | undefined;
      if (peek(c)?.t === "char" && (peek(c) as { t: "char"; v: string }).v === "[") {
        next(c);
        deg = [];
        while (c.pos < c.tokens.length && !(peek(c)?.t === "char" && (peek(c) as { t: "char"; v: string }).v === "]"))
          deg.push(parseAtomWithScripts(c));
        if (peek(c)?.t === "char") next(c); // ']'
      }
      const body = parseArgGroup(c);
      return { k: "sqrt", deg, body };
    }
    if (name === "left") {
      const begTok = next(c);
      const beg = delimToChar(begTok);
      const body: Node[] = [];
      while (c.pos < c.tokens.length && !(peek(c)?.t === "cmd" && (peek(c) as { t: "cmd"; name: string }).name === "right"))
        body.push(parseAtomWithScripts(c));
      if (peek(c)?.t === "cmd") next(c); // 'right'
      const endTok = next(c);
      const end = delimToChar(endTok);
      return { k: "delim", beg, end, body };
    }
    if (name in NARY_MAP_REV) {
      return { k: "nary", chr: NARY_MAP_REV[name] };
    }
    if (name === "underline") return { k: "bar", pos: "bot", body: parseArgGroup(c) };
    if (name === "overline") return { k: "bar", pos: "top", body: parseArgGroup(c) };
    if (name in ACCENT_CMD_TO_CHR) return { k: "acc", chr: ACCENT_CMD_TO_CHR[name], body: parseArgGroup(c) };
    if (name === "bar") return { k: "acc", chr: "̄", body: parseArgGroup(c) };
    if (UPRIGHT_TEXT_CMDS.has(name)) {
      const inner = parseArgGroup(c);
      return { k: "func", name: nodesToPlainText(inner) };
    }
    if (FUNCS.has(name)) return { k: "func", name };
    const sym = SYMBOL_CMD_TO_CHAR.get(`\\${name}`);
    if (sym !== undefined) return { k: "char", v: sym };
    if (name === "{" || name === "}" || name === "%" || name === "&" || name === "#" || name === "$" || name === "_")
      return { k: "char", v: name };
    // Lệnh lạ không hỗ trợ: hiện tên trơn, không bung được cú pháp thì thà mất
    // định dạng còn hơn hỏng cả file.
    return { k: "char", v: name };
  }

  // sup/sub đứng đầu (thiếu cơ số) — bỏ qua, không nên xảy ra với input hợp lệ.
  return { k: "char", v: "" };
}

const NARY_MAP_REV: Record<string, string> = Object.fromEntries(NARY_CMD_TO_CHR.entries());

function delimToChar(tok: Token | undefined): string {
  if (!tok) return "";
  if (tok.t === "char") return DELIM_LATEX_TO_CHAR[tok.v] ?? tok.v;
  if (tok.t === "cmd") return DELIM_LATEX_TO_CHAR[tok.name] ?? "";
  return "";
}

function nodesToPlainText(nodes: Node[]): string {
  return nodes
    .map((n) => (n.k === "char" ? n.v : n.k === "func" ? n.name : ""))
    .join("");
}

/** Đọc 1 nguyên tử rồi gộp `^`/`_` theo sau (nếu có) thành sup/sub/subsup. */
function parseAtomWithScripts(c: Cursor): Node {
  const base = parseAtom(c);
  let sup: Node[] | undefined;
  let sub: Node[] | undefined;
  for (;;) {
    const t = peek(c);
    if (t?.t === "sup" && sup === undefined) {
      next(c);
      sup = parseArgGroup(c);
    } else if (t?.t === "sub" && sub === undefined) {
      next(c);
      sub = parseArgGroup(c);
    } else break;
  }
  if (sup && sub) return { k: "subsup", base: [base], sub, exp: sup };
  if (sup) return { k: "sup", base: [base], exp: sup };
  if (sub) return { k: "sub", base: [base], sub };
  return base;
}

function parseSequence(c: Cursor): Node[] {
  const nodes: Node[] = [];
  while (c.pos < c.tokens.length && !isBrace(peek(c), "}")) nodes.push(parseAtomWithScripts(c));
  return attachNaryBodies(nodes);
}

/** Lấy nary gốc của 1 node (xuyên qua lớp sup/sub/subsup bọc ngoài), nếu có. */
function naryRoot(n: Node): Extract<Node, { k: "nary" }> | null {
  if (n.k === "nary") return n;
  if ((n.k === "sup" || n.k === "sub" || n.k === "subsup") && n.base.length === 1) return naryRoot(n.base[0]);
  return null;
}

/**
 * Bộ chuyển xuôi (latex-converter.ts) luôn phát `\sum_{a}^{b}{than_than}` —
 * khối `{...}` theo ngay sau cận trên/dưới chính là thân tổng/tích phân.
 * Gộp nó vào làm `e` của nary thay vì để đứng tách rời trong câu.
 */
function attachNaryBodies(nodes: Node[]): Node[] {
  const out: Node[] = [];
  for (let i = 0; i < nodes.length; i++) {
    const n = nodes[i];
    const root = naryRoot(n);
    const bodyNode = nodes[i + 1];
    if (root && !root.e && bodyNode) {
      // Thân tổng/tích phân có thể là 1 nguyên tử trần (vd `a_i`, khớp thẳng
      // parseAtomWithScripts) hoặc 1 nhóm `{...}` nhiều phần tử (đã được
      // parseAtom gói vào 1 "plain group") — cả hai đều gộp làm `e`.
      root.e = isPlainGroup(bodyNode) ? bodyNode.body : [bodyNode];
      out.push(n);
      i++;
      continue;
    }
    out.push(n);
  }
  return out;
}

function isPlainGroup(n: Node): n is Extract<Node, { k: "delim" }> {
  return n.k === "delim" && n.beg === "" && n.end === "";
}

// ---------- Render AST -> OMML ----------

function escapeXml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function run(text: string, upright = false): string {
  if (text === "") return "";
  const pr = upright ? "<m:rPr><m:sty m:val=\"p\"/></m:rPr>" : "";
  return `<m:r>${pr}<m:t xml:space="preserve">${escapeXml(text)}</m:t></m:r>`;
}

function renderNodes(nodes: Node[]): string {
  let out = "";
  let textBuf = "";
  const flush = () => {
    if (textBuf) {
      out += run(textBuf);
      textBuf = "";
    }
  };
  for (const n of nodes) {
    if (n.k === "char") {
      textBuf += n.v;
      continue;
    }
    flush();
    out += renderNode(n);
  }
  flush();
  return out;
}

function renderNode(n: Node): string {
  switch (n.k) {
    case "char":
      return run(n.v);
    case "func":
      return run(n.name, true);
    case "frac":
      return `<m:f><m:fPr><m:type m:val="${n.kind}"/></m:fPr><m:num>${renderNodes(n.num)}</m:num><m:den>${renderNodes(n.den)}</m:den></m:f>`;
    case "sqrt":
      return `<m:rad><m:radPr><m:degHide m:val="${n.deg ? "0" : "1"}"/></m:radPr><m:deg>${n.deg ? renderNodes(n.deg) : ""}</m:deg><m:e>${renderNodes(n.body)}</m:e></m:rad>`;
    case "delim":
      if (n.beg === "" && n.end === "")
        // nhóm ẩn (từ `{...}` chứa nhiều phần tử) — không vẽ dấu ngoặc, chỉ gom khối.
        return renderNodes(n.body);
      return `<m:d><m:dPr><m:begChr m:val="${escapeXml(n.beg)}"/><m:endChr m:val="${escapeXml(n.end)}"/></m:dPr><m:e>${renderNodes(n.body)}</m:e></m:d>`;
    case "acc":
      return `<m:acc><m:accPr><m:chr m:val="${escapeXml(n.chr)}"/></m:accPr><m:e>${renderNodes(n.body)}</m:e></m:acc>`;
    case "bar":
      return `<m:bar><m:barPr><m:pos m:val="${n.pos}"/></m:barPr><m:e>${renderNodes(n.body)}</m:e></m:bar>`;
    case "nary": {
      const hide = n.sub === undefined && n.sup === undefined;
      return `<m:nary><m:naryPr><m:chr m:val="${escapeXml(n.chr)}"/><m:limLoc m:val="undOvr"/>${hide ? '<m:subHide m:val="1"/><m:supHide m:val="1"/>' : ""}</m:naryPr><m:sub>${n.sub ? renderNodes(n.sub) : ""}</m:sub><m:sup>${n.sup ? renderNodes(n.sup) : ""}</m:sup><m:e>${n.e ? renderNodes(n.e) : ""}</m:e></m:nary>`;
    }
    case "sup": {
      const root = naryRoot(n.base[0]);
      if (root) {
        root.sup = n.exp;
        return renderNode(root);
      }
      return `<m:sSup><m:e>${renderNodes(n.base)}</m:e><m:sup>${renderNodes(n.exp)}</m:sup></m:sSup>`;
    }
    case "sub": {
      const base0 = n.base[0];
      const root = naryRoot(base0);
      if (root) {
        root.sub = n.sub;
        return renderNode(root);
      }
      if (base0.k === "func")
        return `<m:limLow><m:e>${renderNode(base0)}</m:e><m:lim>${renderNodes(n.sub)}</m:lim></m:limLow>`;
      return `<m:sSub><m:e>${renderNodes(n.base)}</m:e><m:sub>${renderNodes(n.sub)}</m:sub></m:sSub>`;
    }
    case "subsup": {
      const root = naryRoot(n.base[0]);
      if (root) {
        root.sub = n.sub;
        root.sup = n.exp;
        return renderNode(root);
      }
      return `<m:sSubSup><m:e>${renderNodes(n.base)}</m:e><m:sub>${renderNodes(n.sub)}</m:sub><m:sup>${renderNodes(n.exp)}</m:sup></m:sSubSup>`;
    }
  }
}

/** `latex` chưa kèm `$`. Trả về nội dung bên trong `<m:oMath>` (chưa bọc thẻ đó). */
export function latexToOmml(latex: string): string {
  try {
    const cursor: Cursor = { tokens: tokenize(latex), pos: 0 };
    return renderNodes(parseSequence(cursor));
  } catch {
    // Cú pháp lạ không parse được — chèn nguyên văn để không hỏng cả file .docx.
    return run(latex);
  }
}
