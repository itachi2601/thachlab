import { Hinh } from "@/components/lessons/cong-cu/GiaiCungHinh";
import { splitSolution } from "@/components/lessons/StepwiseSolution";
import type { LessonWorkedQuestion } from "@/features/lessons/types";
import type { ChieuBai, ChieuBuoc, ChieuDong, ChieuLuaChon } from "./types";

/**
 * Dựng bản chiếu từ một dạng bài tập mẫu ĐÃ SOẠN (skill soan-bai-tap-mau) — không cần soạn thêm gì:
 *  - đề: `problem_html`; tóm đề: `tom_de`; hình: `cong_cu` vẽ theo số bước đã giải (đúng như GiaiCungHinh);
 *  - "Kiến thức cần gọi lại": khung `.tl-box` đầu `solution_html`;
 *  - mỗi bước: tên + câu hỏi từ `buoc[i]`, phương án lớp chọn từ `chon_buoc_ke`, các dòng giải là từng khối con của
 *    `.bt-step` thứ i (đoạn văn / công thức khối / `.bt-ans` thành dòng kết quả), cuối bước thêm ⚠ `loi_hay_gap`;
 *  - đáp số: `.bt-final`.
 * `q.trinh_chieu` (tuỳ chọn) viết đè từng bước và thêm bảng trạng thái ①②.
 * Chạy ở trình duyệt (DOMParser) — trình chiếu chỉ mount phía client.
 */

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/** Công thức khối → dòng (để dòng tóm tắt bước gọn một dòng). */
const motDong = (html: string) => html.replace(/\$\$([\s\S]+?)\$\$/g, (_m, t: string) => `$${t.trim()}$`);

function tachDong(stepHtml: string): ChieuDong[] {
  const doc = new DOMParser().parseFromString(`<body>${stepHtml}</body>`, "text/html");
  const box = doc.body.querySelector(".bt-step") ?? doc.body;
  box.querySelector(".bt-step-title")?.remove();
  const out: ChieuDong[] = [];
  let inline = ""; // chữ/thẻ nội dòng nằm trần giữa các khối → gom thành một dòng
  const xa = () => {
    if (inline.trim()) out.push({ html: inline.trim() });
    inline = "";
  };
  box.childNodes.forEach((node) => {
    if (node.nodeType === Node.TEXT_NODE) {
      const t = node.textContent ?? "";
      // công thức khối $$…$$ đứng trần = một dòng riêng
      if (/^\s*\$\$[\s\S]*\$\$\s*$/.test(t)) {
        xa();
        out.push({ html: esc(t.trim()) });
      } else inline += esc(t);
      return;
    }
    if (!(node instanceof Element)) return;
    const tag = node.tagName.toLowerCase();
    if (["span", "strong", "b", "em", "i", "sub", "sup", "br"].includes(tag)) {
      inline += node.outerHTML;
      return;
    }
    xa();
    if (node.classList.contains("bt-ans")) out.push({ html: node.innerHTML.trim(), kieu: "ket_qua" });
    else out.push({ html: node.outerHTML });
  });
  xa();
  return out;
}

/** Trộn phương án cố định theo nội dung (đáp án đúng luôn đứng đầu trong dữ liệu — không để lộ vị trí). */
function tron(cs: ChieuLuaChon[]): ChieuLuaChon[] {
  const h = (s: string) => [...s].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7);
  return [...cs].sort((a, b) => h(a.text) - h(b.text));
}

export function tuDang(q: LessonWorkedQuestion, idx: number): ChieuBai {
  const parts = splitSolution(q.solution_html ?? "");
  const de = q.trinh_chieu;
  let kienThuc: string | undefined;
  let dapSo = "";
  if (parts) {
    const head = new DOMParser().parseFromString(`<body>${parts.head}</body>`, "text/html").body;
    const tl = head.querySelector(".tl-box");
    if (tl) {
      tl.querySelector(".tl-label")?.remove();
      kienThuc = tl.innerHTML.trim() || undefined;
    }
    const tail = new DOMParser().parseFromString(`<body>${parts.tail}</body>`, "text/html").body;
    const fin = tail.querySelector(".bt-final") ?? tail;
    const first = fin.firstElementChild;
    if (first && /^\s*Đáp số\s*$/i.test(first.textContent ?? "")) first.remove();
    dapSo = fin.innerHTML.trim();
  }

  const buoc: ChieuBuoc[] = (q.buoc ?? []).map((b, i) => {
    const dong = parts?.steps[i] ? tachDong(parts.steps[i]) : [];
    if (b.loi_hay_gap) dong.push({ html: b.loi_hay_gap, kieu: "bay" });
    const kq = [...dong].reverse().find((d) => d.kieu === "ket_qua");
    const ghiDe = de?.buoc?.[i] ?? null;
    return {
      tieu_de: b.tieu_de,
      hoi: ghiDe?.hoi ?? b.hoi,
      lua_chon: b.chon_buoc_ke?.length ? tron(b.chon_buoc_ke.map((c) => ({ text: c.text, dung: !!c.dung, vi_sao: c.vi_sao }))) : undefined,
      dong: ghiDe?.dong ?? dong,
      tom_tat: ghiDe?.tom_tat ?? (kq ? motDong(kq.html) : ""),
    };
  });

  // Dạng cũ không có buoc nhưng có .bt-step: vẫn chiếu được từng bước (tên bước lấy từ tiêu đề trong HTML).
  if (!buoc.length && parts?.steps.length) {
    parts.steps.forEach((s) => {
      const ten = new DOMParser().parseFromString(`<body>${s}</body>`, "text/html").body.querySelector(".bt-step-title")?.textContent?.replace(/^\s*\d+\s*/, "") ?? "Bước";
      const dong = tachDong(s);
      const kq = [...dong].reverse().find((d) => d.kieu === "ket_qua");
      buoc.push({ tieu_de: ten.trim(), dong, tom_tat: kq ? motDong(kq.html) : "" });
    });
  }

  const tool = q.cong_cu;
  const [so, ...ten] = (q.label || `Ví dụ ${idx + 1}`).split(" · ");
  return {
    nhan: so,
    dang: ten.join(" · ") || undefined,
    de_html: q.problem_html ?? q.body_html,
    tom_de: q.tom_de?.cho?.length || q.tom_de?.tim?.length ? q.tom_de : undefined,
    kien_thuc_html: kienThuc,
    hinh: tool ? ({ layer, step }) => <Hinh tool={tool} layer={layer} step={step} /> : undefined,
    bang: de?.bang,
    buoc,
    dap_so: dapSo,
    nhan_dang: q.nhan_dang,
    bay: de?.bay,
  };
}

/** Dạng chiếu được: có lời giải chia bước. */
export function chieuDuoc(q: LessonWorkedQuestion): boolean {
  return !!q.problem_html && !!splitSolution(q.solution_html ?? "")?.steps.length;
}
