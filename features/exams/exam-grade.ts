/**
 * Đoán khối lớp (9/10/11/12) từ tiêu đề đề thi đăng hàng loạt không gán lớp — "Cuối HK1 2025 – 11 – THPT …",
 * "Giữa HK2 – Lớp 10 – …", "Vật lí 12 – …". 687/899 đề đã đăng (17/10/2026) không gán lớp nào nên kệ đề lớp 12
 * đang bày cả đề lớp 11; chừng nào chưa gán lớp trong DB thì lọc bằng tiêu đề. Không đoán được → null (toàn trường).
 */
export function gradeFromExamTitle(title: string): string | null {
  const t = title.toLowerCase();
  const m =
    t.match(/[–\-]\s*(9|10|11|12)\s*[–\-]/) ??
    t.match(/\b(?:lớp|khối|vật lí|vật lý|vl|khtn)\s*(9|10|11|12)\b/) ??
    t.match(/\b(?:hk\s*[12]|học kì\s*[12i]+)\s*(?:–|-)?\s*(9|10|11|12)\b/);
  return m ? m[1] : null;
}

/**
 * Đề không gán lớp có thuộc về lớp khối `grade` không: ưu tiên bài học chứa đề (examChapterGrade), rồi tới tiêu đề;
 * không có manh mối nào thì coi là toàn trường (giữ).
 */
export function unassignedExamFitsGrade(
  examId: number,
  title: string,
  grade: string | null,
  examGradeByLesson: Map<number, string | null>,
): boolean {
  if (!grade) return true;
  const byLesson = examGradeByLesson.get(examId);
  if (byLesson !== undefined) return byLesson === null || byLesson === grade;
  const byTitle = gradeFromExamTitle(title);
  return byTitle === null || byTitle === grade;
}
