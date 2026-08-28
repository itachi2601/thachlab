import ExcelJS from "exceljs";
import { LT_GRADE_COLUMNS, TH_GRADE_COLUMNS } from "@/services/roster-schema";

export interface ExportStudentRow {
  stt: number;
  studentCode: string;
  fullName: string;
  birthDate: string;
  scores: Record<string, number | null>;
}

export interface ExportRosterOptions {
  className: string;
  teacherName: string;
  sessionType: string;
  template: "lt" | "th";
  students: ExportStudentRow[];
}

/** Tách "Họ" / "Tên" theo đúng quy ước file mẫu: từ cuối cùng là Tên, phần còn lại là Họ. */
function splitName(fullName: string) {
  const tokens = fullName.trim().split(/\s+/).filter(Boolean);
  const ten = tokens.pop() ?? "";
  return { ho: tokens.join(" "), ten };
}

export async function exportCourseRoster(opts: ExportRosterOptions): Promise<Blob> {
  const columns = opts.template === "lt" ? LT_GRADE_COLUMNS : TH_GRADE_COLUMNS;
  const workbook = new ExcelJS.Workbook();
  const sheet = workbook.addWorksheet("DSSV");

  const baseCols = ["STT", "Mã SV", "Họ", "Tên", "Ngày Sinh"];
  const headers = [...baseCols, ...columns.map((c) => c.label), "Ghi Chú"];
  const lastColLetter = String.fromCharCode(64 + headers.length);

  sheet.mergeCells(`A1:${lastColLetter}1`);
  sheet.getCell("A1").value = "BẢNG NHẬP ĐIỂM MÔN HỌC";
  sheet.getCell("A1").font = { bold: true, size: 14 };

  sheet.getCell("C2").value = "Lớp học phần:";
  sheet.getCell("D2").value = opts.className;
  sheet.getCell("C3").value = "Giáo viên:";
  sheet.getCell("D3").value = opts.teacherName;
  sheet.getCell("C4").value = "Loại:";
  sheet.getCell("D4").value = opts.sessionType;
  for (const addr of ["C2", "C3", "C4"]) sheet.getCell(addr).font = { bold: true };

  const headerRow = sheet.getRow(5);
  headerRow.values = headers;
  headerRow.font = { bold: true };
  headerRow.alignment = { horizontal: "center", vertical: "middle", wrapText: true };

  opts.students.forEach((student, index) => {
    const { ho, ten } = splitName(student.fullName);
    const row = [
      student.stt || index + 1,
      student.studentCode,
      ho,
      ten,
      student.birthDate,
      ...columns.map((c) => student.scores[c.key] ?? ""),
      "",
    ];
    sheet.addRow(row);
  });

  sheet.columns.forEach((col, index) => {
    col.width = index < baseCols.length ? [6, 14, 22, 14, 12][index] ?? 12 : 11;
  });

  const buffer = await workbook.xlsx.writeBuffer();
  return new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
}
