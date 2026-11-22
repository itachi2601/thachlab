// Mục Sức khỏe › Kiểu build: từ số đo cơ thể → khung xương, % mỡ ước tính, dáng thân → gợi ý tập + ăn.
// Chỉ dùng cho người lớn tự theo dõi (số đo cơ thể KHÔNG mở cho học sinh — xem lib/suc-khoe/modules.ts).
// Mọi con số là ƯỚC LƯỢNG, sai số vài %: đủ để chọn hướng, không thay cho khám/đo chuyên môn.
//   • % mỡ: công thức Hải quân Mỹ (Hodgdon & Beckett 1984), sai số khoảng ±3–4 %.
//   • Khung xương: chỉ số chiều cao / cổ tay (Grant 1981).
//   • Ngưỡng ngực/eo, eo/chiều cao: cùng ngưỡng trang Số đo đang dùng (components/tap-luyen/SoDo.tsx).
import type { Measurement } from "@/lib/tap-luyen/store";
import { ROUTINES, exerciseById, weeklySets } from "@/lib/tap-luyen/chuong-trinh";
import type { Goal, Sex } from "@/lib/suc-khoe/dinh-duong";

export type FrameSize = "nho" | "vua" | "lon";
export const FRAME_LABEL: Record<FrameSize, string> = { nho: "Khung nhỏ", vua: "Khung vừa", lon: "Khung lớn" };
export type FatBand = "rat-thap" | "gon" | "trung-binh" | "cao";
export const FAT_LABEL: Record<FatBand, string> = { "rat-thap": "Mỡ rất thấp", gon: "Gọn", "trung-binh": "Mỡ trung bình", cao: "Mỡ cao" };
export type Shape = "chu-v" | "chu-nhat" | "qua-le" | "tron-bung";
export const SHAPE_LABEL: Record<Shape, string> = { "chu-v": "Dáng chữ V", "chu-nhat": "Dáng chữ nhật", "qua-le": "Dáng quả lê", "tron-bung": "Dáng tròn bụng" };

export type Priority = { group: "Ngực" | "Vai" | "Lưng" | "Chân" | "Mông" | "Core"; extraSets: number; why: string; ex: string[] };
export type BuildInfo = {
  sex: Sex;
  bmi: number | null;
  frame: { ratio: number; size: FrameSize } | null;
  bf: number | null;
  band: FatBand | null;
  shape: Shape | null;
  label: string;
  goal: Goal;
  goalWhy: string;
  expect: string;
  priorities: Priority[];
  tips: string[];
  /** số đo còn thiếu để kết quả chính xác hơn */
  missing: { key: "neck_cm" | "wrist_cm" | "hip_cm" | "chest_cm" | "waist_cm" | "weight_kg"; label: string; why: string }[];
};

/** % mỡ theo công thức Hải quân Mỹ (cm). Trả null nếu thiếu số đo hoặc số đo vô lý (eo ≤ cổ). */
export function navyBodyFat(sex: Sex, h: number, waist: number, neck: number, hip?: number | null): number | null {
  const x = sex === "nam" ? waist - neck : hip ? waist + hip - neck : NaN;
  if (!(x > 0) || !(h > 0)) return null;
  const bf =
    sex === "nam"
      ? 495 / (1.0324 - 0.19077 * Math.log10(x) + 0.15456 * Math.log10(h)) - 450
      : 495 / (1.29579 - 0.35004 * Math.log10(x) + 0.221 * Math.log10(h)) - 450;
  return Number.isFinite(bf) && bf > 2 && bf < 60 ? bf : null;
}

export function frameOf(sex: Sex, h: number, wrist: number): { ratio: number; size: FrameSize } {
  const r = h / wrist; // cao / cổ tay: càng lớn càng "mảnh"
  const [lo, hi] = sex === "nam" ? [9.6, 10.4] : [10.1, 11];
  return { ratio: r, size: r > hi ? "nho" : r >= lo ? "vua" : "lon" };
}

export function fatBand(sex: Sex, bf: number): FatBand {
  const cut = sex === "nam" ? [8, 18, 25] : [16, 25, 32];
  return bf < cut[0] ? "rat-thap" : bf < cut[1] ? "gon" : bf < cut[2] ? "trung-binh" : "cao";
}

const setsNow = (g: string) => weeklySets(ROUTINES).find(([k]) => k === g)?.[1] ?? 0;
export const currentWeeklySets = setsNow;

export function analyzeBuild(m: Measurement, sex: Sex): BuildInfo | null {
  const h = m.height_cm;
  if (!h) return null;
  const bmi = m.weight_kg ? m.weight_kg / (h / 100) ** 2 : null;
  const frame = m.wrist_cm ? frameOf(sex, h, m.wrist_cm) : null;
  const bf = m.waist_cm && m.neck_cm ? navyBodyFat(sex, h, m.waist_cm, m.neck_cm, m.hip_cm) : null;
  const band = bf != null ? fatBand(sex, bf) : null;

  const cw = m.chest_cm && m.waist_cm ? m.chest_cm / m.waist_cm : null;
  const wht = m.waist_cm ? m.waist_cm / h : null;
  const hipOverChest = m.chest_cm != null && m.hip_cm != null && m.hip_cm >= m.chest_cm;
  const shape: Shape | null =
    wht == null && cw == null
      ? null
      : (wht ?? 0) >= 0.55 || band === "cao"
        ? "tron-bung"
        : hipOverChest
          ? "qua-le"
          : cw != null && cw >= 1.2
            ? "chu-v"
            : "chu-nhat";

  // ---- mục tiêu ăn ----
  const fatHigh = band === "cao" || (band == null && ((wht ?? 0) >= 0.55 || (bmi ?? 0) >= 25));
  const fatMid = band === "trung-binh";
  const light = bmi != null && bmi < 18.5;
  let goal: Goal;
  let goalWhy: string;
  if (fatHigh) {
    goal = "giam";
    goalWhy = band ? `Mỡ ước tính ${Math.round(bf!)} % thuộc nhóm cao` : "Eo/chiều cao hoặc BMI đang cao";
  } else if (fatMid && frame?.size !== "nho") {
    goal = "giu";
    goalWhy = `Mỡ ước tính ${Math.round(bf!)} % ở mức trung bình — ăn bằng mức duy trì, tập tạ để thay mỡ bằng cơ`;
  } else {
    goal = "tang";
    goalWhy = light
      ? "BMI dưới 18,5 — cần ăn dư để lên cân"
      : band
        ? `Mỡ ước tính ${Math.round(bf!)} % ở mức gọn — còn dư địa tăng cơ`
        : "Chưa có % mỡ; eo/chiều cao còn an toàn nên tăng cơ chậm, theo dõi eo";
  }
  const expect =
    !frame
      ? "Đo thêm vòng cổ tay để biết cỡ khung xương — khung quyết định nhịp lên cơ bạn nên kỳ vọng."
      : frame.size === "nho"
      ? "Khung nhỏ: tăng cơ chậm hơn người khung lớn và nhìn rõ nhất ở vai, ngực — kiên nhẫn, đừng ăn dư quá tay để rồi tăng mỡ."
      : frame.size === "lon"
        ? "Khung lớn: lên cân và lên tạ nhanh hơn, dễ tích mỡ nếu ăn dư — giữ mức dư nhỏ và canh vòng eo."
        : "Khung vừa: nhịp tăng cơ trung bình; 4 tuần đo lại một lần để chỉnh.";

  // ---- ưu tiên tập ----
  const priorities: Priority[] = [];
  if (cw != null && cw < 1.2) {
    priorities.push({
      group: "Vai",
      extraSets: cw < 1.15 ? 4 : 2,
      why: `Ngực/eo ${cw.toFixed(2).replace(".", ",")} (dưới 1,20): vai bên rộng hơn làm dáng chữ V rõ hơn bất kể vòng ngực`,
      ex: ["lateral_raise_db", "lateral_raise_cable"],
    });
    priorities.push({
      group: "Ngực",
      extraSets: cw < 1.15 ? 3 : 2,
      why: "Ngực/eo còn thấp: thêm một lượt ngực dốc lên ở cuối tuần",
      ex: ["incline_db_press", "pec_deck"],
    });
  }
  if (hipOverChest) {
    priorities.push({
      group: "Lưng",
      extraSets: 3,
      why: "Hông rộng hơn ngực: lưng xô nở ra hai bên làm thân trên rộng hơn; kéo (lưng) nên bằng hoặc hơn đẩy (ngực)",
      ex: ["lat_pulldown", "seated_cable_row", "assisted_pull_up"],
    });
  }
  if (goal === "giam" || shape === "tron-bung") {
    priorities.push({
      group: "Mông",
      extraSets: 0,
      why: "Giữ bài chân/mông nặng (squat, hip thrust) để không mất cơ khi ăn thiếu; không dồn thêm hiệp cho bụng — tập bụng không đốt mỡ bụng riêng",
      ex: ["squat", "hip_thrust"],
    });
  }

  const tips: string[] = [];
  if (goal === "tang") tips.push("Ăn dư 200–300 kcal/ngày; cân tăng 0,15–0,3 kg/tuần là đúng nhịp. Eo tăng quá 1 cm thì bớt 150 kcal.");
  if (goal === "giu") tips.push("Ăn bằng mức duy trì, đạm cao (~2 g/kg), tập tạ 3 buổi/tuần: cân gần như đứng yên nhưng eo nhỏ dần là đang đúng.");
  if (goal === "giam") tips.push("Ăn thiếu vừa phải (~400 kcal/ngày), giảm tối đa 0,5 kg/tuần; đạm 2 g/kg để giữ cơ; vẫn tập tạ nặng, thêm đi bộ nhanh 2×30′/tuần.");
  if (frame && frame.size === "nho" && cw != null && cw < 1.2) tips.push("Khung nhỏ nên vai/ngực là chỗ đổi dáng nhanh nhất — ưu tiên đúng hai nhóm này trước chân.");
  if (priorities.some((p) => p.group === "Vai" || p.group === "Ngực")) tips.push("Mỗi nhóm cơ tập 2 lần/tuần; thêm hiệp vào buổi B/C (giữ buổi A nguyên) để chân vẫn còn sức cho trượt băng.");

  const missing: BuildInfo["missing"] = [];
  if (!m.weight_kg) missing.push({ key: "weight_kg", label: "Cân nặng", why: "tính BMI và năng lượng" });
  if (!m.waist_cm) missing.push({ key: "waist_cm", label: "Eo", why: "dáng thân, % mỡ" });
  if (!m.chest_cm) missing.push({ key: "chest_cm", label: "Ngực", why: "tỉ lệ ngực/eo" });
  if (!m.hip_cm) missing.push({ key: "hip_cm", label: "Mông", why: sex === "nu" ? "% mỡ (nữ cần vòng mông)" : "so ngực với mông" });
  if (!m.neck_cm) missing.push({ key: "neck_cm", label: "Cổ", why: "ước tính % mỡ" });
  if (!m.wrist_cm) missing.push({ key: "wrist_cm", label: "Cổ tay", why: "xác định cỡ khung xương" });

  const parts = [frame ? FRAME_LABEL[frame.size] : null, band ? FAT_LABEL[band] : null, shape ? SHAPE_LABEL[shape] : null].filter(Boolean);
  return { sex, bmi, frame, bf, band, shape, label: parts.length ? parts.join(" · ") : "Chưa đủ số đo", goal, goalWhy, expect, priorities, tips, missing };
}

/** Tên bài tập (cho UI) từ id; bỏ id không tồn tại. */
export const exNames = (ids: string[]) => ids.map((id) => exerciseById(id)?.name).filter((n): n is string => !!n);
