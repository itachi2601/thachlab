import ExcelJS from "exceljs";
import { getSupabase } from "@/services/supabase";

export type HomeroomTerm = "hk1" | "hk2" | "ca_nam";
export type ConductGrade = "tot" | "kha" | "tb" | "yeu";

export interface HomeroomTermRecord {
  course_id: number;
  student_id: string;
  term: HomeroomTerm;
  exam_score: number | null;
  conduct: ConductGrade | null;
  note: string;
  updated_at: string;
}

export const CONDUCT_LABEL: Record<ConductGrade, string> = {
  tot: "Tốt",
  kha: "Khá",
  tb: "Trung bình",
  yeu: "Yếu",
};

export const HOMEROOM_TERMS: { key: HomeroomTerm; label: string }[] = [
  { key: "hk1", label: "Học kì 1" },
  { key: "hk2", label: "Học kì 2" },
];

export async function fetchHomeroomTermRecords(courseId: number) {
  const { data, error } = await getSupabase()
    .from("homeroom_term_records")
    .select("course_id, student_id, term, exam_score, conduct, note, updated_at")
    .eq("course_id", courseId);
  if (error) throw error;
  return (data ?? []) as HomeroomTermRecord[];
}

export async function setHomeroomTermRecord(
  courseId: number,
  studentId: string,
  term: HomeroomTerm,
  patch: { exam_score?: number | null; conduct?: ConductGrade | null; note?: string },
) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const payload: Record<string, unknown> = {
    course_id: courseId,
    student_id: studentId,
    term,
    updated_by: auth.user?.id ?? null,
    updated_at: new Date().toISOString(),
  };
  if ("exam_score" in patch) {
    payload.exam_score =
      patch.exam_score === null || patch.exam_score === undefined
        ? null
        : Math.min(10, Math.max(0, patch.exam_score));
  }
  if ("conduct" in patch) payload.conduct = patch.conduct ?? null;
  if ("note" in patch) payload.note = patch.note ?? "";
  const { error } = await supabase
    .from("homeroom_term_records")
    .upsert(payload, { onConflict: "course_id,student_id,term" });
  if (error) throw error;
}

export interface HomeroomExportRow {
  studentCode: string;
  fullName: string;
  birthDate: string;
  examHk1: number | null;
  conductHk1: ConductGrade | null;
  examHk2: number | null;
  conductHk2: ConductGrade | null;
  average: number | null;
  attendanceRate: number | null;
  note: string;
}

export async function exportHomeroomGradebook(opts: { className: string; schoolYear: string; rows: HomeroomExportRow[] }): Promise<Blob> {
  const workbook = new ExcelJS.Workbook();
  const sheet = workbook.addWorksheet("Bảng điểm");
  const headers = ["STT", "Mã SV", "Họ và tên", "Ngày sinh", "Điểm KT HK1", "Hạnh kiểm HK1", "Điểm KT HK2", "Hạnh kiểm HK2", "TB cả năm", "Chuyên cần (%)", "Ghi chú"];
  const lastCol = String.fromCharCode(64 + headers.length);

  sheet.mergeCells(`A1:${lastCol}1`);
  sheet.getCell("A1").value = "BẢNG ĐIỂM MÔN GIÁO DỤC ĐẠO ĐỨC VÀ PHÁT TRIỂN NGHỀ NGHIỆP";
  sheet.getCell("A1").font = { bold: true, size: 13 };
  sheet.getCell("A1").alignment = { horizontal: "center" };
  sheet.getCell("A2").value = `Lớp: ${opts.className}`;
  sheet.getCell("A3").value = `Năm học: ${opts.schoolYear}`;

  const headerRow = sheet.addRow(headers);
  headerRow.font = { bold: true };
  headerRow.alignment = { horizontal: "center", wrapText: true };

  opts.rows.forEach((row, index) => {
    sheet.addRow([
      index + 1,
      row.studentCode,
      row.fullName,
      row.birthDate,
      row.examHk1 ?? "",
      row.conductHk1 ? CONDUCT_LABEL[row.conductHk1] : "",
      row.examHk2 ?? "",
      row.conductHk2 ? CONDUCT_LABEL[row.conductHk2] : "",
      row.average ?? "",
      row.attendanceRate ?? "",
      row.note,
    ]);
  });

  sheet.columns.forEach((column, index) => {
    column.width = index === 2 ? 28 : index === 10 ? 30 : index === 0 ? 6 : 14;
  });

  const buffer = await workbook.xlsx.writeBuffer();
  return new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
}
