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
  group: "Ngực" | "Vai" | "Lưng" | "Chân" | "Mông" | "Core" | "Sức bật" | "Tay" | "Tim mạch";
  track: Track;
  /** bước tăng tạ gợi ý (kg) */
  step?: number;
  /** ghi chú kỹ thuật hiện dưới tên bài */
  cue?: string;
  /** cách làm khó hơn khi đã đủ số lần mọi hiệp (bài không tạ) */
  harder?: string;
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

export type RoutineItem = {
  ex: string;
  sets: number;
  /** khoảng lặp (hoặc giây với track "time") */
  lo: number;
  hi: number;
  rest: number; // giây
  warmup?: number; // số hiệp khởi động gợi ý
};
export type Routine = { key: string; name: string; focus: string; when: string; items: RoutineItem[] };

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
export function weeklySets(routines: Routine[] = ROUTINES) {
  const m = new Map<string, number>();
  for (const r of routines) for (const it of r.items) {
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

// ---------------------------------------------------------------------------------------------
// Chương trình HỌC SINH (19/11/2026) — mở cho mọi học sinh, sinh viên đăng nhập (THPT và CTTC).
// Không dụng cụ, tập ở nhà hoặc sân trường, ~30 phút/buổi, 3 buổi/tuần. Tiến bộ đo bằng số lần / số giây,
// KHÔNG đo cân nặng, vòng ngực–eo, không gợi ý ăn dư calo (nguy cơ lo về vóc dáng tuổi 14–18; docs/QUY-TAC-THIET-KE.md G2).
// Khung theo khuyến nghị WHO 2020 cho 5–17 tuổi: trung bình 60 phút vận động vừa–mạnh mỗi ngày,
// bài tăng sức cơ–xương ít nhất 3 ngày/tuần. Giấc ngủ 8–10 giờ cho 13–18 tuổi (AASM 2016).
export const EXERCISES_HS: Exercise[] = [
  { id: "hs_jumping_jack", name: "Bật nhảy dang tay chân", group: "Tim mạch", track: "time", cue: "Tiếp đất bằng nửa trước bàn chân, gối hơi chùng." },
  { id: "hs_jump_rope", name: "Nhảy dây (không có dây: nhảy tại chỗ)", group: "Tim mạch", track: "time", cue: "Nhảy thấp, nhịp đều; mỏi thì đi bộ tại chỗ rồi nhảy tiếp." },
  { id: "hs_mountain_climber", name: "Leo núi tại chỗ", group: "Tim mạch", track: "time", cue: "Tay thẳng dưới vai, hông không nhô cao; kéo gối về ngực luân phiên.", harder: "Kéo gối nhanh hơn, giữ hông thấp." },
  { id: "hs_push_up_incline", name: "Hít đất chống tay lên bàn / ghế", group: "Ngực", track: "reps", cue: "Thân thẳng từ đầu tới gót, ngực chạm gần mép bàn.", harder: "Chuyển sang hít đất chống gối trên sàn." },
  { id: "hs_push_up_knee", name: "Hít đất chống gối", group: "Ngực", track: "reps", cue: "Thân thẳng từ đầu tới gối, khuỷu khép khoảng 45° so với thân.", harder: "Chuyển sang hít đất trên mũi chân (hít đất thường)." },
  { id: "hs_push_up", name: "Hít đất", group: "Ngực", track: "reps", cue: "Siết bụng và mông, hạ chậm 2 giây.", harder: "Hạ chậm 3 giây, hoặc kê chân lên bậc thấp." },
  { id: "hs_backpack_row", name: "Cúi người kéo balo", group: "Lưng", track: "reps", cue: "Balo vài quyển sách (3–5 kg). Gập hông, lưng thẳng, kéo balo về bụng, siết hai bả vai.", harder: "Thêm 1–2 quyển sách vào balo." },
  { id: "hs_superman", name: "Nằm sấp nâng tay chân (siêu nhân)", group: "Lưng", track: "time", cue: "Nâng tay và chân vừa khỏi sàn, mắt nhìn sàn, không ngửa cổ.", harder: "Giữ lâu hơn 5–10 giây." },
  { id: "hs_squat", name: "Squat tay không", group: "Chân", track: "reps", cue: "Đẩy hông ra sau, đùi xuống gần song song sàn, gối theo hướng mũi chân, gót không nhấc.", harder: "Hạ chậm 3 giây, dừng 1 giây ở dưới." },
  { id: "hs_lunge", name: "Bước chùng (mỗi chân)", group: "Chân", track: "reps", cue: "Bước dài, gối sau gần chạm sàn, thân thẳng.", harder: "Đeo balo sách khi tập." },
  { id: "hs_wall_sit", name: "Ngồi dựa tường", group: "Chân", track: "time", cue: "Lưng áp tường, đùi song song sàn, gối thẳng trên cổ chân.", harder: "Giữ lâu hơn 10 giây." },
  { id: "hs_squat_jump", name: "Bật nhảy từ tư thế squat", group: "Sức bật", track: "reps", cue: "Tiếp đất êm, gối chùng; nghỉ đủ giữa hiệp.", harder: "Nhảy cao hơn, vẫn tiếp đất êm." },
  { id: "hs_glute_bridge", name: "Nằm ngửa nâng hông", group: "Mông", track: "reps", cue: "Gót gần mông, đẩy hông lên tới thân thẳng từ vai tới gối, giữ 1 giây.", harder: "Làm một chân (mỗi bên)." },
  { id: "hs_plank", name: "Plank", group: "Core", track: "time", cue: "Khuỷu dưới vai, thân thẳng, siết bụng; võng lưng thì dừng hiệp.", harder: "Giữ lâu hơn 5–10 giây." },
  { id: "hs_side_plank", name: "Plank nghiêng (mỗi bên)", group: "Core", track: "time", cue: "Hông nâng cao, thân thẳng một đường; khó quá thì chống gối.", harder: "Giữ lâu hơn 5 giây." },
  { id: "hs_dead_bug", name: "Nằm ngửa duỗi tay chân đối bên (dead bug)", group: "Core", track: "reps", cue: "Lưng dưới áp sàn suốt bài; duỗi chậm tay trái + chân phải rồi đổi bên.", harder: "Duỗi chậm hơn, dừng 2 giây khi duỗi hết." },
];

export const ROUTINES_HS: Routine[] = [
  {
    key: "1",
    name: "1 · Toàn thân cơ bản",
    focus: "Làm quen các động tác gốc: squat, hít đất, kéo, giữ thân. Đúng động tác quan trọng hơn số lần.",
    when: "Buổi đầu tuần. Tập ở nhà hoặc sân trường, khoảng 30 phút.",
    items: [
      { ex: "hs_jumping_jack", sets: 2, lo: 30, hi: 45, rest: 30 },
      { ex: "hs_squat", sets: 3, lo: 10, hi: 15, rest: 60 },
      { ex: "hs_push_up_incline", sets: 3, lo: 8, hi: 12, rest: 60 },
      { ex: "hs_backpack_row", sets: 3, lo: 10, hi: 15, rest: 60 },
      { ex: "hs_glute_bridge", sets: 2, lo: 12, hi: 15, rest: 45 },
      { ex: "hs_plank", sets: 3, lo: 20, hi: 40, rest: 45 },
    ],
  },
  {
    key: "2",
    name: "2 · Chân và thân giữa",
    focus: "Chân khoẻ, thân giữa vững giúp chạy nhảy, chơi thể thao và ngồi học đỡ mỏi lưng.",
    when: "Cách buổi 1 ít nhất một ngày.",
    items: [
      { ex: "hs_jump_rope", sets: 3, lo: 30, hi: 60, rest: 45 },
      { ex: "hs_lunge", sets: 3, lo: 8, hi: 12, rest: 60 },
      { ex: "hs_wall_sit", sets: 2, lo: 30, hi: 45, rest: 60 },
      { ex: "hs_glute_bridge", sets: 3, lo: 12, hi: 20, rest: 45 },
      { ex: "hs_dead_bug", sets: 2, lo: 8, hi: 12, rest: 45 },
      { ex: "hs_side_plank", sets: 2, lo: 15, hi: 30, rest: 30 },
    ],
  },
  {
    key: "3",
    name: "3 · Thân trên và sức bền",
    focus: "Hít đất, kéo, lưng, cộng phần tim mạch ngắn để tăng sức bền.",
    when: "Cuối tuần, cách buổi 2 ít nhất một ngày.",
    items: [
      { ex: "hs_jumping_jack", sets: 2, lo: 30, hi: 45, rest: 30 },
      { ex: "hs_push_up_knee", sets: 3, lo: 6, hi: 12, rest: 60 },
      { ex: "hs_backpack_row", sets: 3, lo: 10, hi: 15, rest: 60 },
      { ex: "hs_superman", sets: 3, lo: 15, hi: 30, rest: 45 },
      { ex: "hs_mountain_climber", sets: 3, lo: 20, hi: 30, rest: 45 },
      { ex: "hs_squat_jump", sets: 2, lo: 6, hi: 8, rest: 60 },
      { ex: "hs_plank", sets: 2, lo: 20, hi: 40, rest: 45 },
    ],
  },
];

export const RULES_TEXT_HS = [
  "3 buổi/tuần, mỗi buổi khoảng 30 phút, các buổi cách nhau ít nhất 1 ngày. Không cần dụng cụ.",
  "Trước buổi: khởi động 5 phút (xoay cổ, vai, hông, gối, cổ chân; đi bộ nhanh tại chỗ). Sau buổi: giãn cơ 5 phút.",
  "Mỗi hiệp dừng khi còn làm được 1–2 lần nữa mà động tác vẫn đúng. Sai động tác thì dừng hiệp, không cố.",
  "Làm đủ số lần (số giây) cao nhất ở mọi hiệp → buổi sau làm khó hơn một chút: thêm lần, giữ lâu hơn hoặc đổi kiểu khó hơn.",
  "Đau nhói ở khớp, chóng mặt, tức ngực, khó thở bất thường → dừng ngay và báo người lớn. Mỏi cơ 1–2 ngày sau buổi đầu là bình thường.",
  "Ngoài 3 buổi này, tuổi các em nên vận động vừa đến mạnh khoảng 60 phút mỗi ngày: đi bộ, đạp xe, đá bóng, cầu lông, bơi (WHO).",
  "Ngủ 8–10 tiếng, uống đủ nước, ăn đủ ba bữa. Không ăn kiêng, không dùng thuốc hay bột tăng cơ khi chưa hỏi bác sĩ.",
];

const ALL_EXERCISES = [...EXERCISES, ...EXERCISES_HS];
export const exerciseById = (id: string) => ALL_EXERCISES.find((e) => e.id === id);

/** Chương trình theo người dùng: giáo viên dùng chương trình A/B/C của thầy (có số đo); học sinh dùng chương trình không dụng cụ. */
export type Program = {
  kind: "thay" | "hoc-sinh";
  routines: Routine[];
  rules: string[];
  exercises: Exercise[];
  /** nhóm hiện ở thẻ "Hiệp 7 ngày qua" */
  groups: string[];
  /** thời lượng ước tính mỗi buổi */
  minutes: string;
  /** được dùng phần Số đo cơ thể (cân nặng, vòng đo)? */
  measurements: boolean;
};
export const PROGRAM_THAY: Program = {
  kind: "thay",
  routines: ROUTINES,
  rules: RULES_TEXT,
  exercises: EXERCISES,
  groups: ["Ngực", "Vai", "Lưng", "Chân", "Mông", "Sức bật", "Core"],
  minutes: "khoảng 75–90 phút",
  measurements: true,
};
export const PROGRAM_HS: Program = {
  kind: "hoc-sinh",
  routines: ROUTINES_HS,
  rules: RULES_TEXT_HS,
  exercises: EXERCISES_HS,
  groups: ["Tim mạch", "Ngực", "Lưng", "Chân", "Mông", "Core"],
  minutes: "khoảng 30 phút",
  measurements: false,
};
export const programFor = (role?: string | null): Program => (role === "admin" || role === "instructor" ? PROGRAM_THAY : PROGRAM_HS);
