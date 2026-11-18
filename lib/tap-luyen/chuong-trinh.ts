// Chương trình tập A/B/C của thầy Thạch (lập lại 18/11/2026) — mục tiêu: tăng ngực + vai, giữ eo.
// Xuất phát: 1m60 · 53 kg · ngực 82 · eo 72 · mông 85 → ngực/eo 1,14, ngực < mông → thân trên chưa có dáng chữ V.
// Eo đã gọn (eo/chiều cao 0,45) nên KHÔNG giảm mỡ thêm; dồn thể tích vào ngực, vai, lưng xô; chân giữ mức
// đủ cho trượt băng 4 buổi/tuần. Tổng tuần (hiệp nặng): ngực ~15, vai giữa ~10, lưng ~10–14, chân ~15.
// Tăng tạ kiểu "double progression": mọi hiệp làm việc chạm đỉnh khoảng lặp → buổi sau tăng tạ bước nhỏ nhất.
// Sửa bài/hiệp ở đây; nội dung tóm tắt cho lịch tuần nằm ở .claude/skills/lich-tuan/references/lich-co-dinh.json.

export type Track = "kg_reps" | "reps" | "time";
export type Exercise = {
  id: string;
  name: string;
  group: "Ngực" | "Vai" | "Lưng" | "Chân" | "Mông" | "Core" | "Sức bật" | "Tay";
  track: Track;
  /** bước tăng tạ gợi ý (kg) */
  step?: number;
  /** ghi chú kỹ thuật hiện dưới tên bài */
  cue?: string;
};

export const EXERCISES: Exercise[] = [
  { id: "chest_press_machine", name: "Ép ngực máy", group: "Ngực", track: "kg_reps", step: 2.5, cue: "Ghế cho tay cầm ngang giữa ngực; ép vai ra sau, không nhún vai." },
  { id: "incline_db_press", name: "Đẩy ngực dốc lên tạ đơn", group: "Ngực", track: "kg_reps", step: 1, cue: "Ghế 30°; hạ chậm 2–3 giây tới khi căng ngực trên." },
  { id: "incline_machine_press", name: "Đẩy ngực dốc lên máy / Smith", group: "Ngực", track: "kg_reps", step: 2.5 },
  { id: "flat_db_press", name: "Đẩy ngực tạ đơn ghế phẳng", group: "Ngực", track: "kg_reps", step: 1 },
  { id: "pec_deck", name: "Ép ngực cáp / pec deck", group: "Ngực", track: "kg_reps", step: 2.5, cue: "Khuỷu hơi cong cố định; dừng 1 giây khi hai tay chụm." },
  { id: "push_up", name: "Hít đất", group: "Ngực", track: "reps" },
  { id: "shoulder_press_machine", name: "Đẩy vai máy", group: "Vai", track: "kg_reps", step: 2.5 },
  { id: "lateral_raise_db", name: "Dang vai bên tạ đơn (lateral raise)", group: "Vai", track: "kg_reps", step: 1, cue: "Nâng tới ngang vai, dẫn bằng khuỷu; tạ nhẹ, không đung đưa." },
  { id: "lateral_raise_cable", name: "Dang vai bên cáp", group: "Vai", track: "kg_reps", step: 1.25 },
  { id: "face_pull", name: "Face pull", group: "Vai", track: "kg_reps", step: 2.5 },
  { id: "reverse_pec_deck", name: "Bay vai sau (reverse pec deck)", group: "Vai", track: "kg_reps", step: 2.5 },
  { id: "lat_pulldown", name: "Kéo xô (lat pulldown)", group: "Lưng", track: "kg_reps", step: 2.5, cue: "Kéo thanh về ngực trên, ngực ưỡn nhẹ; thả lên hết tầm." },
  { id: "assisted_pull_up", name: "Kéo xà (có hỗ trợ nếu cần)", group: "Lưng", track: "reps", cue: "Máy hỗ trợ: ghi số kg hỗ trợ vào ghi chú, giảm dần." },
  { id: "seated_cable_row", name: "Kéo cáp ngồi", group: "Lưng", track: "kg_reps", step: 2.5 },
  { id: "squat", name: "Squat (hoặc goblet / hack squat)", group: "Chân", track: "kg_reps", step: 2.5, cue: "Cách thất bại 2–3 lần: chân phải còn tươi cho buổi băng." },
  { id: "rdl", name: "Romanian deadlift", group: "Chân", track: "kg_reps", step: 2.5 },
  { id: "bulgarian_split_squat", name: "Bulgarian split squat (mỗi chân)", group: "Chân", track: "kg_reps", step: 1 },
  { id: "calf_raise", name: "Nâng bắp chân", group: "Chân", track: "kg_reps", step: 2.5 },
  { id: "hip_abduction", name: "Dạng hông (máy / dây)", group: "Mông", track: "kg_reps", step: 2.5 },
  { id: "hip_thrust", name: "Hip thrust", group: "Mông", track: "kg_reps", step: 2.5 },
  { id: "box_jump", name: "Box jump", group: "Sức bật", track: "reps", cue: "Tiếp đất êm như tiếp băng; bước xuống, không nhảy xuống." },
  { id: "single_leg_hop", name: "Hop một chân (mỗi chân)", group: "Sức bật", track: "reps" },
  { id: "copenhagen_plank", name: "Copenhagen plank (mỗi bên)", group: "Core", track: "time" },
  { id: "pallof_press", name: "Pallof press (mỗi bên)", group: "Core", track: "kg_reps", step: 1.25 },
  { id: "dead_bug", name: "Dead bug", group: "Core", track: "reps" },
  { id: "side_plank", name: "Side plank (mỗi bên)", group: "Core", track: "time" },
  { id: "db_curl", name: "Cuốn tay trước tạ đơn", group: "Tay", track: "kg_reps", step: 1 },
  { id: "triceps_pushdown", name: "Duỗi tay sau cáp", group: "Tay", track: "kg_reps", step: 2.5 },
];
export const exerciseById = (id: string) => EXERCISES.find((e) => e.id === id);

export type RoutineItem = {
  ex: string;
  sets: number;
  /** khoảng lặp (hoặc giây với track "time") */
  lo: number;
  hi: number;
  rest: number; // giây
  warmup?: number; // số hiệp khởi động gợi ý
};
export type Routine = { key: "A" | "B" | "C"; name: string; focus: string; when: string; items: RoutineItem[] };

export const ROUTINES: Routine[] = [
  {
    key: "A",
    name: "A · Thân trên — ngực, vai",
    focus: "Buổi trọng tâm của tuần: nhiều hiệp nhất cho ngực, vai giữa, lưng xô. Cách thất bại 1–2 lần ở mọi hiệp làm việc.",
    when: "Hợp với ngày có trượt băng (chân để nguyên). Tuần nào cũng phải có.",
    items: [
      { ex: "chest_press_machine", sets: 4, lo: 8, hi: 12, rest: 120, warmup: 2 },
      { ex: "lat_pulldown", sets: 4, lo: 8, hi: 12, rest: 120, warmup: 1 },
      { ex: "shoulder_press_machine", sets: 3, lo: 8, hi: 10, rest: 120, warmup: 1 },
      { ex: "incline_db_press", sets: 3, lo: 8, hi: 12, rest: 90 },
      { ex: "lateral_raise_db", sets: 4, lo: 12, hi: 20, rest: 60 },
      { ex: "seated_cable_row", sets: 3, lo: 10, hi: 12, rest: 90 },
      { ex: "pec_deck", sets: 2, lo: 12, hi: 15, rest: 60 },
      { ex: "face_pull", sets: 2, lo: 15, hi: 20, rest: 60 },
    ],
  },
  {
    key: "B",
    name: "B · Chân + ngực, vai phụ",
    focus: "Chân giữ sức cho trượt băng (cách thất bại 2–3 lần), thêm một lượt ngực dốc lên và vai bên để ngực–vai được tập 3 lần/tuần.",
    when: "Không đặt ngay trước buổi nhảy trên băng.",
    items: [
      { ex: "squat", sets: 3, lo: 6, hi: 8, rest: 150, warmup: 2 },
      { ex: "rdl", sets: 3, lo: 8, hi: 10, rest: 120, warmup: 1 },
      { ex: "bulgarian_split_squat", sets: 2, lo: 8, hi: 10, rest: 90 },
      { ex: "incline_machine_press", sets: 3, lo: 8, hi: 12, rest: 90, warmup: 1 },
      { ex: "lateral_raise_cable", sets: 3, lo: 12, hi: 20, rest: 60 },
      { ex: "calf_raise", sets: 3, lo: 12, hi: 15, rest: 60 },
      { ex: "hip_abduction", sets: 2, lo: 15, hi: 20, rest: 45 },
    ],
  },
  {
    key: "C",
    name: "C · Toàn thân + sức bật",
    focus: "Bật nhảy làm trước khi mỏi; sau đó kéo xà, ngực phẳng, vai bên, vai sau, core chống xoay cho spin.",
    when: "Ngày còn lại; cách buổi A ít nhất 1 ngày.",
    items: [
      { ex: "box_jump", sets: 3, lo: 5, hi: 5, rest: 90 },
      { ex: "single_leg_hop", sets: 3, lo: 5, hi: 5, rest: 60 },
      { ex: "hip_thrust", sets: 3, lo: 8, hi: 10, rest: 120, warmup: 1 },
      { ex: "assisted_pull_up", sets: 3, lo: 6, hi: 10, rest: 120 },
      { ex: "flat_db_press", sets: 3, lo: 8, hi: 12, rest: 90, warmup: 1 },
      { ex: "lateral_raise_db", sets: 3, lo: 12, hi: 20, rest: 60 },
      { ex: "reverse_pec_deck", sets: 2, lo: 15, hi: 20, rest: 60 },
      { ex: "copenhagen_plank", sets: 2, lo: 20, hi: 30, rest: 45 },
      { ex: "pallof_press", sets: 2, lo: 10, hi: 12, rest: 45 },
    ],
  },
];

/** Tổng hiệp làm việc/tuần theo nhóm cơ (để hiện ở trang Chương trình). */
export function weeklySets() {
  const m = new Map<string, number>();
  for (const r of ROUTINES) for (const it of r.items) {
    const g = exerciseById(it.ex)?.group ?? "?";
    m.set(g, (m.get(g) ?? 0) + it.sets);
  }
  return [...m.entries()].sort((a, b) => b[1] - a[1]);
}

/** Mục tiêu đo lường — thầy chốt 18/11/2026. */
export const TARGET = {
  start: { date: "2026-11-18", height: 160, weight: 53, chest: 82, waist: 72, hip: 85 },
  chestGainCm: [3, 4] as const, // mỗi chu kỳ ~4 tuần đầu
  waistMax: 72,
  weightGainPerWeek: [0.15, 0.3] as const, // kg/tuần: tăng cơ chậm, ít mỡ
  proteinGPerKg: [1.6, 2.2] as const,
  surplusKcal: [200, 300] as const,
  remeasureDays: 28,
};

export const RULES_TEXT = [
  "Khởi động 10′ (hông, cổ chân, xoay ngực) + 1–2 hiệp nhẹ cho bài đầu mỗi nhóm.",
  "Hiệp làm việc dừng khi còn 1–2 lần nữa là hỏng (chân: 2–3 lần, để giữ sức cho băng).",
  "Mọi hiệp chạm đỉnh khoảng lặp → buổi sau tăng tạ bước nhỏ nhất, quay về đáy khoảng lặp.",
  "Ăn nhỉnh hơn duy trì ~200–300 kcal/ngày, đạm 1,6–2,2 g/kg (≈ 90–110 g/ngày); ngày trượt băng ăn thêm tinh bột.",
  "Cân tăng >0,4 kg/tuần hai tuần liền hoặc eo tăng >1 cm → bớt 150–200 kcal. Cân đứng yên 2 tuần → thêm 150 kcal.",
  "Đo lại mỗi 4 tuần: cùng giờ (sáng, trước ăn), cùng thước, cùng chỗ đặt thước.",
  "Mỗi 6–8 tuần hoặc khi tạ đứng yên 2 buổi liền: một tuần nhẹ (bớt 1/3 số hiệp).",
];
