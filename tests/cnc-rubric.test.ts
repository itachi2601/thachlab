// Khoá chấm rubric thi thực hành CNC (services/cnc-rubric.ts) — nền để chuyển chấm về server không đổi kết quả.
import { describe, expect, it } from "vitest";
import { RUBRIC_BY_MACHINE, gradeRubricExam, isRubricComplete, rubricMaxScore, type RubricLevel } from "@/services/cnc-rubric";

for (const machine of ["tien", "phay"] as const) {
  describe(`rubric ${machine}`, () => {
    const rubric = RUBRIC_BY_MACHINE[machine];
    const all = (lv: RubricLevel) => Object.fromEntries(rubric.groups.flatMap((g) => g.criteria.map((c) => [c.id, lv])));
    const zt = (ok: boolean) => Object.fromEntries(rubric.zeroTolerance.map((_, i) => [i, ok]));

    it("tổng điểm tối đa = 10 (snapshot)", () => {
      expect(rubricMaxScore(rubric)).toMatchInlineSnapshot(`10`);
    });
    it("toàn E → điểm tối đa, Xuất sắc", () => {
      const r = gradeRubricExam(rubric, all("E"), zt(true));
      expect(r.totalScore).toBe(rubricMaxScore(rubric));
      expect(r.xepLoai).toBe("Xuất sắc (Excellent)");
      expect(r.gatePassed).toBe(true);
    });
    it("toàn F → 0, không đạt", () => {
      const r = gradeRubricExam(rubric, all("F"), zt(true));
      expect(r.totalScore).toBe(0);
      expect(r.gatePassed).toBe(false);
      expect(r.xepLoai).toBe("Không đạt (Failed)");
    });
    it("lỗi loại trực tiếp ghi đè xếp loại nhưng KHÔNG đổi điểm", () => {
      const r = gradeRubricExam(rubric, all("E"), { ...zt(true), 0: false });
      expect(r.zeroToleranceFailed).toBe(true);
      expect(r.xepLoai).toBe("Không đạt (lỗi loại trực tiếp)");
      expect(r.totalScore).toBe(rubricMaxScore(rubric));
    });
    it("chưa xác nhận lỗi loại trực tiếp (object rỗng) = coi như vi phạm", () => {
      expect(gradeRubricExam(rubric, all("E"), {}).zeroToleranceFailed).toBe(rubric.zeroTolerance.length > 0);
    });
    it("luật chặn: nhóm kỹ thuật dưới ngưỡng → nhóm thành phần bị tính 0", () => {
      const levels = { ...all("E"), ...Object.fromEntries(rubric.groups.find((g) => g.id === rubric.gateGroupId)!.criteria.map((c) => [c.id, "F"])) };
      const r = gradeRubricExam(rubric, levels, zt(true));
      expect(r.gatePassed).toBe(false);
      expect(r.totalScore).toBe(r.groupScores[rubric.gateGroupId]);
      expect(r.groupScores[rubric.gatedGroupId]).toBeGreaterThan(0); // groupScores giữ điểm thô, chỉ totalScore bị chặn
    });
    it("isRubricComplete", () => {
      expect(isRubricComplete(rubric, all("P"))).toBe(true);
      expect(isRubricComplete(rubric, {})).toBe(false);
    });
    it("bảng điểm mức E/G/P/F khoá cứng (snapshot)", () => {
      expect((["E", "G", "P", "F"] as const).map((lv) => gradeRubricExam(rubric, all(lv), zt(true)))).toMatchSnapshot();
    });
  });
}
