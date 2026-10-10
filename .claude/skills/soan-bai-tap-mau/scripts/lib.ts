// Kiểm + dựng dữ liệu "Bài tập mẫu có cấu trúc" (scripts/data/bai-tap-mau/<lesson_id>.json).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(here, "../../../..");
export const DATA_DIR = path.join(ROOT, "scripts/data/bai-tap-mau");
const TOPICS_FILE = path.join(ROOT, "scripts/data/question-topics.json");

export interface Topic { id: number; lesson_id: number; name: string; parent_id: number | null }
export function loadTopics(): Topic[] | null {
  return fs.existsSync(TOPICS_FILE) ? JSON.parse(fs.readFileSync(TOPICS_FILE, "utf8")) : null;
}

const dollarsBalanced = (s: string) => ((s.replace(/\\\$/g, "").match(/\$/g) ?? []).length % 2) === 0;
const ROLE_THAY = /\b(thầy|cô giáo)\b/i; // bài soạn cho HS không dùng vai "thầy" (feedback giọng văn 2/10/2026)

export interface Choice { text: string; dung?: boolean; vi_sao?: string }
export interface Step {
  tieu_de: string;
  hoi?: string;
  dap_so?: number;
  don_vi?: string;
  sai_so?: number;
  lua_chon?: Choice[];
  loi_hay_gap?: string;
  chon_buoc_ke?: Choice[];
}
export const FADING = ["mo_het", "giau_buoc_cuoi", "giau_tu_buoc_2", "giau_het"] as const;
export type Fading = (typeof FADING)[number];

export interface Dang {
  label: string;
  topic: string;
  topic_id?: number;
  form?: string;
  problem_html: string;
  analysis_html: string;
  solution_html: string;
  // Tự giải từng bước (thầy chốt 9/10/2026) — xem SKILL.md mục "Học sinh tự giải từng bước"
  buoc?: Step[];
  nhan_dang?: string;
  cap_do?: number;
  fading?: Fading;
  go_roi?: { buoc_hay_sai: number };
}

/** Bước nào bị giấu theo `fading` (0-based). Dùng chung cho validator và UI (components/lessons/StepwiseSolution.tsx chép lại logic này). */
export function hiddenSteps(fading: Fading | undefined, steps: { hoi?: string }[]): boolean[] {
  const last = steps.map((s) => !!s.hoi).lastIndexOf(true); // "bước cuối" = bước cuối CÓ câu hỏi (bước Kiểm tra không hỏi)
  return steps.map((s, i) =>
    !s.hoi ? false : fading === "giau_het" ? true : fading === "giau_tu_buoc_2" ? i >= 1 : fading === "giau_buoc_cuoi" ? i === last : false,
  );
}

const countWords = (s: string) => s.replace(/<[^>]+>/g, " ").trim().split(/\s+/).filter(Boolean).length;

function validateSteps(d: Dang, at: string, errors: string[], warnings: string[]) {
  const steps = d.buoc;
  if (!Array.isArray(steps) || steps.length < 2) { errors.push(`${at}: cần buoc[] ≥ 2 bước (tự giải từng bước, 9/10/2026)`); return; }
  const nStep = (d.solution_html.match(/class="bt-step"/g) ?? []).length;
  if (nStep !== steps.length) errors.push(`${at}: buoc có ${steps.length} bước nhưng solution_html có ${nStep} .bt-step — phải khớp 1-1 theo thứ tự`);
  if (!d.nhan_dang?.trim()) errors.push(`${at}: thiếu nhan_dang ("Thấy … → nghĩ tới …")`);
  else if (countWords(d.nhan_dang) > 25) warnings.push(`${at}: nhan_dang dài ${countWords(d.nhan_dang)} chữ (> 25)`);
  if (!Number.isInteger(d.cap_do) || d.cap_do! < 1 || d.cap_do! > 4) errors.push(`${at}: cap_do phải là 1–4`);
  if (d.fading && !FADING.includes(d.fading)) errors.push(`${at}: fading phải là ${FADING.join("|")}`);
  const hidden = hiddenSteps(d.fading, steps);
  if (d.go_roi && !(Number.isInteger(d.go_roi.buoc_hay_sai) && d.go_roi.buoc_hay_sai >= 0 && d.go_roi.buoc_hay_sai < steps.length))
    errors.push(`${at}: go_roi.buoc_hay_sai ngoài phạm vi 0..${steps.length - 1}`);
  const checkChoices = (cs: Choice[] | undefined, what: string, exact?: number) => {
    if (!Array.isArray(cs)) return errors.push(`${what}: thiếu`);
    if (exact ? cs.length !== exact : cs.length < 2) errors.push(`${what}: cần ${exact ?? "≥ 2"} lựa chọn`);
    if (cs.filter((c) => c.dung).length !== 1) errors.push(`${what}: phải có đúng 1 lựa chọn đúng`);
    cs.forEach((c, k) => {
      if (!c.text?.trim()) errors.push(`${what}: lựa chọn ${k + 1} trống`);
      if (!c.dung && !c.vi_sao?.trim()) errors.push(`${what}: lựa chọn sai "${c.text}" thiếu vi_sao`);
    });
  };
  steps.forEach((s, j) => {
    const sa = `${at} bước ${j + 1}`;
    if (!s.tieu_de?.trim()) errors.push(`${sa}: thiếu tieu_de`);
    const hasNum = typeof s.dap_so === "number", hasChoice = Array.isArray(s.lua_chon);
    if (s.hoi) {
      if (!hasNum && !hasChoice) errors.push(`${sa}: có hoi nhưng thiếu dap_so (số) hoặc lua_chon`);
      if (hasNum && !(typeof s.sai_so === "number" && s.sai_so >= 0)) errors.push(`${sa}: dap_so cần sai_so ≥ 0`);
      if (hasChoice) checkChoices(s.lua_chon, `${sa} lua_chon`);
      if (!s.loi_hay_gap?.trim()) errors.push(`${sa}: thiếu loi_hay_gap`);
    } else if (hidden[j] && j === steps.length - 1) warnings.push(`${sa}: bước cuối bị giấu nhưng không có hoi — sẽ tự mở`);
    if (hasNum && s.hoi && String(s.dap_so).replace("-", "").length >= 2) { // lựa chọn/tiêu đề không được lộ đáp số (bắt ở bài 57 dạng 6); số 1 chữ số bỏ qua (trùng chỉ số t_1)
      const vi = String(s.dap_so).replace(".", "{,}"), en = String(s.dap_so);
      const leak = [...(s.chon_buoc_ke ?? []), ...(s.lua_chon ?? [])].map((c) => c.text).concat(s.tieu_de, s.hoi ?? "")
        .filter((t) => t.includes(vi) || new RegExp(`(^|[^\\d.,_{])${en.replace(".", "\\.")}(?![\\d])`).test(t));
      if (leak.length) errors.push(`${sa}: lộ đáp số ${en} trong: ${leak.join(" | ")}`);
    }
    if (s.chon_buoc_ke) {
      if (j === 0) errors.push(`${sa}: bước 1 không có chon_buoc_ke`);
      else checkChoices(s.chon_buoc_ke, `${sa} chon_buoc_ke`, 3);
    } else if (hidden[j] && j > 0 && s.hoi) warnings.push(`${sa}: bước bị giấu nhưng chưa có chon_buoc_ke (3 lựa chọn)`);
  });
}

/** Gộp thành body_html để mọi nơi cũ (trang tĩnh, importer, accordion) vẫn đọc được. */
export function composeBody(d: Dang): string {
  return `${d.problem_html}\n<details><summary>Phân tích đề và lời giải</summary>\n${d.analysis_html}\n${d.solution_html}\n</details>`;
}

export function validate(data: any, topics: Topic[] | null): { errors: string[]; warnings: string[] } {
  const errors: string[] = [], warnings: string[] = [];
  if (!data || typeof data !== "object") return { errors: ["không phải object JSON"], warnings };
  if (!Number.isInteger(data.lesson_id)) errors.push("thiếu lesson_id (số nguyên)");
  if (!data.review?.checked) errors.push("review.checked chưa true — chưa qua bước kiểm chéo");
  const ds: Dang[] = data.dang_bai;
  if (!Array.isArray(ds) || ds.length < 2 || ds.length > 12) { errors.push("dang_bai cần 2–12 dạng, xếp từ dễ đến khó"); return { errors, warnings }; }
  ds.forEach((d, i) => {
    const at = `dạng ${i + 1}`;
    for (const k of ["label", "topic", "problem_html", "solution_html"] as const)
      if (typeof d[k] !== "string" || !d[k].trim()) errors.push(`${at}: thiếu ${k}`);
    if (typeof d.analysis_html !== "string" || !/tl-table--data/.test(d.analysis_html))
      errors.push(`${at}: thiếu analysis_html (bảng Câu trong đề | Dữ liệu | Kiến thức liên quan, class tl-table--data)`);
    else if (!/⚠/.test(d.analysis_html)) errors.push(`${at}: bảng phân tích chưa có hàng ⚠ điều kiện áp dụng (AI-TUTOR 9.1)`);
    if (!/<svg[\s\S]*<animate/.test(d.problem_html ?? "")) warnings.push(`${at}: đề chưa có mô phỏng chuyển động ngay dưới đề`);
    const all = [d.problem_html, d.solution_html, d.analysis_html].join("\n");
    if (!dollarsBalanced(all)) errors.push(`${at}: số dấu $ lẻ`);
    if (/[<>]/.test((all.match(/\$[^$]*\$/g) ?? []).join(""))) errors.push(`${at}: công thức có < hoặc > — viết \\lt / \\gt`);
    if (ROLE_THAY.test(all)) errors.push(`${at}: có vai "thầy/cô" trong nội dung bài`);
    if (d.buoc || d.nhan_dang || d.cap_do || data.tu_giai_tung_buoc) validateSteps(d, at, errors, warnings);
    else warnings.push(`${at}: chưa có buoc[]/nhan_dang (tự giải từng bước) — bài soạn mới phải có`);
    if (ROLE_THAY.test(JSON.stringify(d.buoc ?? "") + (d.nhan_dang ?? ""))) errors.push(`${at}: buoc/nhan_dang có vai "thầy/cô"`);
    if (topics) {
      const hit = topics.find((t) => t.name.trim() === d.topic?.trim());
      if (!hit) errors.push(`${at}: topic "${d.topic}" không có trong question-topics.json`);
      else if (hit.parent_id === null) warnings.push(`${at}: topic là chủ đề cha — nên chọn YCCĐ con sát dạng`);
    } else warnings.push("chưa có question-topics.json — không kiểm topic");
  });
  // bắc cầu: cấp và mức giấu không giảm khi đi xuống danh sách dạng
  const stepped = ds.filter((d) => d.buoc);
  for (let i = 1; i < stepped.length; i++) {
    const a = stepped[i - 1], b = stepped[i];
    if ((b.cap_do ?? 0) < (a.cap_do ?? 0)) errors.push(`${b.label}: cap_do giảm so với dạng trước`);
    if (FADING.indexOf(b.fading ?? "mo_het") < FADING.indexOf(a.fading ?? "mo_het")) errors.push(`${b.label}: fading giảm so với dạng trước`);
  }
  if (data.tu_luan && (!data.tu_luan.label || !String(data.tu_luan.body_html ?? "").trim())) errors.push("tu_luan cần label + body_html");
  return { errors, warnings };
}
