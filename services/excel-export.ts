import ExcelJS from "exceljs";

export interface StudentExportData {
  stt: number;
  fullName: string;
  username: string;
  phone: string;
  parentPhone: string;
  email: string;
  birthDate: string;
  gender: string; // "1" = Nam, "0" = Nữ
  studentId: string;
  password: string;
  class: string;
}

export async function exportStudentToExcel(
  students: StudentExportData[]
): Promise<Blob> {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet("Học sinh");

  // Set column widths
  worksheet.columns = [
    { header: "STT", key: "stt", width: 5 },
    { header: "Họ và tên", key: "fullName", width: 20 },
    { header: "Username (VIP)", key: "username", width: 18 },
    { header: "Số điện thoại", key: "phone", width: 15 },
    { header: "Số điện thoại phụ huynh", key: "parentPhone", width: 20 },
    { header: "Email", key: "email", width: 25 },
    { header: "Ngày sinh", key: "birthDate", width: 12 },
    { header: "Giới tính", key: "gender", width: 10 },
    { header: "Số báo danh", key: "studentId", width: 12 },
    { header: "Mật khẩu", key: "password", width: 15 },
    { header: "Lớp", key: "class", width: 15 },
  ];

  // Style header row
  const headerRow = worksheet.getRow(1);
  headerRow.font = { bold: true, color: { argb: "FFFFFFFF" } };
  headerRow.fill = {
    type: "pattern",
    pattern: "solid",
    fgColor: { argb: "FF2563EB" },
  };
  headerRow.alignment = { horizontal: "center", vertical: "center" };

  // Add data rows
  students.forEach((student) => {
    worksheet.addRow({
      stt: student.stt,
      fullName: student.fullName,
      username: student.username,
      phone: student.phone,
      parentPhone: student.parentPhone,
      email: student.email,
      birthDate: student.birthDate,
      gender: student.gender === "1" ? "Nam" : student.gender === "0" ? "Nữ" : "",
      studentId: student.studentId,
      password: student.password,
      class: student.class,
    });
  });

  // Align all data cells
  worksheet.eachRow((row, rowNumber) => {
    if (rowNumber > 1) {
      row.eachCell((cell) => {
        cell.alignment = { horizontal: "left", vertical: "center" };
      });
    }
  });

  // Convert to buffer
  const buffer = await workbook.xlsx.writeBuffer();
  return new Blob([buffer], {
    type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  });
}
