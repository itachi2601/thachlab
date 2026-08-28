import * as XLSX from "xlsx";
import { getSupabase } from "@/services/supabase";
import { classifyGradeHeader } from "@/services/roster-schema";

export interface RosterStudentRow {
  stt: string;
  studentCode: string;
  fullName: string;
  birthDate: string;
  scores: Record<string, number | null>;
}

export interface ParsedRoster {
  className: string;
  teacherName: string;
  sessionType: string;
  scoreColumns: { key: string; label: string }[];
  students: RosterStudentRow[];
  /** "lt" nếu phát hiện cột KT HS1/HS2/Thi (mẫu môn lý thuyết), ngược lại "th". */
  template: "lt" | "th";
}

function cell(row: unknown[], index: number): string {
  const value = row[index];
  return value === undefined || value === null ? "" : String(value).trim();
}

function findHeaderValue(rows: string[][], label: string): string {
  for (const row of rows) {
    const labelIndex = row.findIndex((c) => c.replace(/:$/, "").trim().toLowerCase() === label.toLowerCase());
    if (labelIndex === -1) continue;
    for (let i = labelIndex + 1; i < row.length; i++) {
      if (row[i]?.trim()) return row[i].trim();
    }
  }
  return "";
}

export async function parseRosterFile(file: File): Promise<ParsedRoster> {
  const buffer = await file.arrayBuffer();
  const workbook = XLSX.read(buffer, { type: "array", cellDates: true });

  for (const sheetName of workbook.SheetNames) {
    const sheet = workbook.Sheets[sheetName];
    const rows = XLSX.utils.sheet_to_json<unknown[]>(sheet, {
      header: 1,
      raw: false,
      dateNF: "dd/mm/yyyy",
      defval: "",
    }).map((row) => row.map((v) => (v === undefined || v === null ? "" : String(v).trim())));

    const headerRowIndex = rows.findIndex((row) => row.some((c) => c.toLowerCase() === "mã sv"));
    if (headerRowIndex === -1) continue;

    const headerRow = rows[headerRowIndex];
    const colMaSV = headerRow.findIndex((c) => c.toLowerCase() === "mã sv");
    const colHo = headerRow.findIndex((c) => c.toLowerCase() === "họ");
    const colTen = headerRow.findIndex((c) => c.toLowerCase() === "tên");
    const colNgaySinh = headerRow.findIndex((c) => c.toLowerCase().includes("ngày sinh"));
    const colGhiChu = headerRow.findIndex((c) => c.toLowerCase().includes("ghi chú"));
    if (colMaSV === -1) continue;

    const scoreEnd = colGhiChu === -1 ? headerRow.length : colGhiChu;
    const counters: Record<string, number> = {};
    const scoreColumns: { key: string; label: string; colIndex: number }[] = [];
    for (let i = (colNgaySinh === -1 ? colMaSV : colNgaySinh) + 1; i < scoreEnd; i++) {
      const key = classifyGradeHeader(headerRow[i] ?? "", counters);
      if (key) scoreColumns.push({ key, label: headerRow[i], colIndex: i });
    }

    const students: RosterStudentRow[] = [];
    for (let r = headerRowIndex + 1; r < rows.length; r++) {
      const row = rows[r];
      const studentCode = cell(row, colMaSV);
      if (!studentCode) continue;
      const ho = colHo === -1 ? "" : cell(row, colHo);
      const ten = colTen === -1 ? "" : cell(row, colTen);
      const scores: Record<string, number | null> = {};
      for (const col of scoreColumns) {
        const raw = cell(row, col.colIndex).replace(",", ".");
        const num = raw === "" ? null : Number(raw);
        scores[col.key] = num === null || Number.isNaN(num) ? null : num;
      }
      students.push({
        stt: cell(row, headerRow.findIndex((c) => c.toLowerCase() === "stt")),
        studentCode,
        fullName: [ho, ten].filter(Boolean).join(" ").trim(),
        birthDate: colNgaySinh === -1 ? "" : cell(row, colNgaySinh),
        scores,
      });
    }

    const headBlock = rows.slice(0, headerRowIndex);
    const hasLtColumns = scoreColumns.some((c) => c.key.startsWith("kt_hs1_") || c.key.startsWith("kt_hs2_") || c.key.startsWith("thi_lan_"));

    return {
      className: findHeaderValue(headBlock, "Lớp học phần"),
      teacherName: findHeaderValue(headBlock, "Giáo viên"),
      sessionType: findHeaderValue(headBlock, "Loại"),
      scoreColumns: scoreColumns.map(({ key, label }) => ({ key, label })),
      students,
      template: hasLtColumns ? "lt" : "th",
    };
  }

  throw new Error("Không tìm thấy cột \"Mã SV\" trong file — kiểm tra lại đúng file danh sách lớp.");
}

export interface ImportResultRow {
  studentCode: string;
  status: "created" | "linked" | "error";
  message?: string;
}

export async function importRosterToCourse(
  courseId: number,
  students: { studentCode: string; fullName: string; className?: string; birthDate?: string }[],
): Promise<ImportResultRow[]> {
  const { data, error } = await getSupabase().functions.invoke("import-roster", {
    body: { courseId, students },
  });
  if (error) throw error;
  return (data?.results ?? []) as ImportResultRow[];
}

/** Nhập danh sách vào 1 khối lớp THPT: tạo tài khoản học sinh rồi thêm vào user_classes. */
export async function importRosterToClass(
  classId: number,
  students: { studentCode: string; fullName: string; className?: string; birthDate?: string }[],
): Promise<ImportResultRow[]> {
  const { data, error } = await getSupabase().functions.invoke("import-roster", {
    body: { classId, students },
  });
  if (error) throw error;
  return (data?.results ?? []) as ImportResultRow[];
}
