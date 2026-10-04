/**
 * lib/circularProjection.ts
 *
 * Thuần các hàm Vật lí cho mô hình "hình chiếu của chuyển động tròn đều đồng nhịp
 * với con lắc lò xo" (mô hình thứ 4 của hero trang chủ). Không phụ thuộc
 * React/DOM nên test riêng và nhúng lại được vào bài học.
 *
 * Nguồn gốc: `content/thi-nghiem/tn-l11-daodongdieuhoa-03.json` (Bài 1. Dao động
 * điều hoà, Vật lí 11, lesson 20) — thí nghiệm "bóng của van xe đạp", mục 5 "Liên
 * hệ với chuyển động tròn đều". Spec đã có mô hình hình chiếu (A, ω, φ); mô hình
 * này ghép THÊM con lắc lò xo thật vào cùng một trục để trả lời câu hỏi mà hình
 * chiếu đơn thuần không trả lời được: *cái gì* quyết định nhịp.
 *
 * Hai hệ, một trục x:
 *  - Bóng (hình chiếu của M quay đều):  x₁(t) = A₁·cos(ω_b·t)
 *  - Con lắc lò xo nằm ngang:           x₂(t) = A₂·cos(ω_c·t),  ω_c = √(k/m)
 *
 * Điểm cốt lõi của mô hình (và là chỗ dễ hiểu sai nhất):
 *  - "ĐỒNG NHỊP" nghĩa là cùng chu kì T (⇔ ω_b = ω_c) — KHÔNG phải cùng vị trí.
 *    Hai bên vẫn giữ đúng nhịp khi A₁ ≠ A₂ (chúng chỉ không chồng lên nhau).
 *  - Chu kì con lắc T = 2π√(m/k) KHÔNG chứa A: kéo con lắc ra xa gấp đôi thì nhịp
 *    y nguyên. Đây là hiểu nhầm tốn điểm nhất ở chương Dao động.
 *
 * Vì sao ω_b phải bằng ω_c mới giữ được nhịp: hiệu pha Δφ(t) = (ω_b − ω_c)·t, chỉ
 * đứng yên khi ω_b = ω_c. Lệch 1% thì sau 50 chu kì hai bên đã ngược pha.
 *
 * Quy ước đơn vị (theo đúng bài học, không đổi hết sang SI):
 *  - A₁ (bán kính đường tròn), A₂ (biên độ con lắc): cm
 *  - ω: rad/s · T: s · m: kg · k: N/m
 */

/** Độ cứng lò xo dùng trong mô hình (N/m) — cho sẵn như đề bài, học sinh chỉnh m. */
export const SPRING_K = 4;

/** Khối lượng vật nặng treo vào lò xo (kg). */
export const MASS_RANGE = { min: 0.05, max: 0.5, step: 0.01, initial: 0.1 } as const;

/** Biên độ con lắc A₂ = chỗ thả vật (cm). Kéo ra xa bao nhiêu là biến số của thí nghiệm. */
export const PENDULUM_AMPLITUDE_RANGE = { min: 2, max: 10, step: 0.5, initial: 4 } as const;

/** Tốc độ quay của bánh xe / tần số góc của hình chiếu (rad/s). */
export const WHEEL_OMEGA_RANGE = { min: 2, max: 12, step: 0.01, initial: 4 } as const;

/** Bán kính đường tròn A₁ (cm) — cố định để biến số duy nhất của biên độ là A₂. */
export const SHADOW_AMPLITUDE = 6;

/** Trục x vẽ từ −10 cm tới +10 cm (bằng biên độ lớn nhất cho phép). */
export const AXIS_MAX_CM = PENDULUM_AMPLITUDE_RANGE.max;

/**
 * Hai bên coi là ĐỒNG NHỊP khi ω lệch nhau dưới 0,5%. Con số này không phải để
 * "dễ tính": nút "Khớp nhịp" đặt ω_b đúng bằng ω_c (làm tròn 2 chữ số) nên sai số
 * thật chỉ ~0,07%; 0,5% là ngưỡng để một lần kéo thanh trượt bằng tay không bị
 * báo "đồng nhịp" oan.
 */
export const RHYTHM_TOLERANCE = 0.005;

/**
 * Coi là "cùng pha" khi hiệu pha nhỏ hơn 10°.
 *
 * Vì sao cần ngưỡng này: khớp ω chỉ làm hiệu pha THÔI TĂNG, không xoá phần đã lệch
 * tích luỹ trước đó. Hai bên có thể cùng chu kì mà vẫn lệch pha — đó là một bài học
 * riêng (cùng nhịp ≠ trùng nhau), không được lẫn với "đồng nhịp".
 */
export const PHASE_ALIGN_TOLERANCE_DEG = 10;

/** Khoảng thời gian giữa hai chấm liên tiếp của dụng cụ "chấm mỗi 0,1 s". */
export const DOT_INTERVAL = 0.1;

export const TWO_PI = 2 * Math.PI;

/** ω của con lắc lò xo: ω = √(k/m) (rad/s). */
export function omegaOfSpring(k: number, mass: number): number {
  return Math.sqrt(k / mass);
}

/** Chu kì từ tần số góc: T = 2π/ω (s). */
export function periodOf(omega: number): number {
  return TWO_PI / omega;
}

/** Số vòng quay mỗi giây của bánh xe: n = ω/2π (vòng/s). */
export function turnsPerSecond(omega: number): number {
  return omega / TWO_PI;
}

/**
 * Li độ của một dao động điều hoà: x(t) = A·cos(ωt + φ).
 * Dùng cho cả bóng (A₁, ω_b) lẫn con lắc (A₂, ω_c) — chúng chỉ khác tham số.
 */
export function displacementAt(
  amplitude: number,
  omega: number,
  t: number,
  phase = 0
): number {
  return amplitude * Math.cos(omega * t + phase);
}

/** Hiệu pha Δφ = ω_b − ω_c sau thời gian t, đã gói về (−π, π] (rad). */
export function phaseDifference(theta: number, phi: number): number {
  let diff = (theta - phi) % TWO_PI;
  if (diff > Math.PI) diff -= TWO_PI;
  if (diff <= -Math.PI) diff += TWO_PI;
  return diff;
}

/** Hiệu pha theo độ (âm = bóng chậm hơn con lắc). */
export function phaseDifferenceDeg(theta: number, phi: number): number {
  return (phaseDifference(theta, phi) * 180) / Math.PI;
}

/** Hai bên có đang gần như cùng pha không (cùng qua VTCB, cùng tới biên). */
export function alignedPhase(
  theta: number,
  phi: number,
  toleranceDeg = PHASE_ALIGN_TOLERANCE_DEG
): boolean {
  return Math.abs(phaseDifferenceDeg(theta, phi)) <= toleranceDeg;
}

/**
 * Hai bên có cùng nhịp không — so TƯƠNG ĐỐI, không so tuyệt đối (thanh trượt chỉ
 * có bước 0,01 rad/s nên không bao giờ gõ đúng từng chữ số thập phân).
 */
export function sameRhythm(
  omegaWheel: number,
  omegaSpring: number,
  tolerance = RHYTHM_TOLERANCE
): boolean {
  return Math.abs(omegaWheel - omegaSpring) / omegaSpring <= tolerance;
}

/** Số dao động đã hoàn thành sau khi pha tích luỹ được `phase` rad. */
export function oscillationCount(phase: number): number {
  return Math.floor(phase / TWO_PI);
}

export interface DotSample {
  t: number;
  x: number;
}

/**
 * Chấm mỗi `interval` giây cho hình chiếu của bóng — dụng cụ để thấy ngay bóng
 * KHÔNG chuyển động đều: chấm dồn lại khi bóng gần biên, giãn ra khi bóng ở giữa
 * (đúng hiểu nhầm đã ghi trong `hien_tuong_hay_sai` của spec: "cho rằng bóng chuyển
 * động đều như van xe").
 *
 * Neo theo PHA HIỆN TẠI (phase) chứ không theo lưới thời gian tuyệt đối: các chấm là
 * "sau 0,1 s nữa bóng ở đâu", nên chúng luôn khớp với vị trí đang thấy, không nhảy
 * khi bấm Dừng, và không bị tính lại sai khi học sinh kéo thanh ω giữa chừng (cách
 * neo theo lưới tuyệt đối sẽ vẽ lại cả quá khứ bằng ω mới).
 *
 * Trả về trọn một chu kì (≈ 1/interval chấm) để mật độ chấm đọc được ngay.
 */
export function equalTimeDots(
  amplitude: number,
  omega: number,
  phase: number,
  interval = DOT_INTERVAL
): DotSample[] {
  const period = periodOf(omega);
  const last = Math.floor((period - 1e-9) / interval);
  const samples: DotSample[] = [];
  for (let k = 0; k <= last; k++) {
    const t = k * interval;
    samples.push({ t, x: amplitude * Math.cos(phase + omega * t) });
  }
  return samples;
}

export type ProjectionMessageKind =
  | "idle"
  | "drift"
  | "samePeriod"
  | "inphase"
  | "inphaseEqual";

export interface ProjectionMessage {
  kind: ProjectionMessageKind;
  text: string;
}

export interface RhythmInput {
  playing: boolean;
  omegaWheel: number;
  omegaSpring: number;
  shadowAmplitude: number;
  pendulumAmplitude: number;
  /** Hiệu pha hiện tại có nằm trong ngưỡng cùng pha không (xem alignedPhase). */
  aligned: boolean;
}

/**
 * Câu nhận xét dưới mô phỏng — nguồn sự thật duy nhất cho phần chữ, tách khỏi
 * React và tách khỏi số đo tức thời.
 *
 * Năm trạng thái, và trạng thái thứ ba là chỗ dễ nói sai nhất:
 *  - idle: chưa bấm Chạy.
 *  - drift: ω lệch nhau → hiệu pha TĂNG dần, không bao giờ giữ nhịp được.
 *  - samePeriod: ω đã bằng nhau nhưng hiệu pha đang khác 0 — khớp ω chỉ làm hiệu pha
 *    THÔI TĂNG chứ không xoá phần đã lệch; muốn trùng nhau phải thả cùng lúc.
 *  - inphase / inphaseEqual: cùng ω và cùng pha (khác hoặc bằng biên độ).
 *
 * CỐ Ý không nhận `t` hay giá trị hiệu pha: câu này nằm trong vùng
 * `role="status" aria-live="polite"`, nội dung đổi theo từng khung hình thì trình
 * đọc màn hình sẽ đọc liên tục không dừng. Chỉ nhận `aligned` (một boolean, đổi rất
 * thưa); số đo tức thời để ở bảng số đọc bên dưới, không đánh dấu aria-live.
 */
export function messageForProjection(
  input: RhythmInput,
  format: (value: number, digits?: number) => string
): ProjectionMessage {
  const {
    playing,
    omegaWheel,
    omegaSpring,
    shadowAmplitude,
    pendulumAmplitude,
    aligned,
  } = input;
  const periodWheel = periodOf(omegaWheel);
  const periodSpring = periodOf(omegaSpring);

  if (!playing) {
    return {
      kind: "idle",
      text:
        `Bóng quay ω = ${format(omegaWheel, 2)} rad/s (T = ${format(periodWheel, 2)} s), ` +
        `con lắc có ω = √(k/m) = ${format(omegaSpring, 2)} rad/s (T = ${format(periodSpring, 2)} s). ` +
        `Bấm "Chạy": cả hai cùng xuất phát từ biên phải, rồi chỉnh tốc độ quay cho khớp để giữ nhịp.`,
    };
  }

  if (!sameRhythm(omegaWheel, omegaSpring)) {
    const faster = omegaWheel > omegaSpring ? "bóng" : "con lắc";
    const ratio = periodWheel / periodSpring;
    return {
      kind: "drift",
      text:
        `CHƯA đồng nhịp: T bóng = ${format(periodWheel, 2)} s, T con lắc = ${format(periodSpring, 2)} s ` +
        `(tỉ số ${format(ratio, 2)} ≠ 1) nên ${faster} đi nhanh hơn. Hiệu pha Δφ = (ω bánh xe − ω con ` +
        `lắc)·t lớn dần theo thời gian — xem ô "Lệch pha". Hai dao động chỉ giữ nhịp khi ω bằng nhau.`,
    };
  }

  if (!aligned) {
    return {
      kind: "samePeriod",
      text:
        `CÙNG CHU KÌ nhưng KHÁC PHA: ω hai bên đã bằng nhau (${format(omegaWheel, 2)} rad/s, ` +
        `T = ${format(periodWheel, 2)} s) nên hiệu pha THÔI TĂNG — nhưng phần lệch đã tích luỹ ` +
        `thì giữ nguyên, xem ô "Lệch pha" và Δx (hai số đó không còn chạy nữa). Cùng nhịp là ` +
        `cùng T; muốn hai bên trùng nhau thì phải THẢ CÙNG LÚC: bấm "Đặt lại" rồi "Chạy".`,
    };
  }

  if (Math.abs(pendulumAmplitude - shadowAmplitude) > 0.05) {
    return {
      kind: "inphase",
      text:
        `ĐỒNG NHỊP: ω hai bên bằng nhau (${format(omegaWheel, 2)} rad/s, T = ${format(periodWheel, 2)} s) ` +
        `nên bóng và con lắc cùng qua vị trí cân bằng, cùng tới biên ở mọi thời điểm — ` +
        `dù biên độ khác nhau (${format(shadowAmplitude, 1)} cm và ${format(pendulumAmplitude, 1)} cm). ` +
        `Chu kì T = 2π√(m/k) không chứa A: kéo con lắc ra xa gấp đôi thì nhịp vẫn y nguyên.`,
    };
  }

  return {
    kind: "inphaseEqual",
    text:
      `ĐỒNG NHỊP và cùng biên độ (${format(shadowAmplitude, 1)} cm): vòng tròn rỗng — chỗ bóng chiếu ` +
      `xuống làn con lắc — trùng khít với vật nặng. Cùng ω, cùng A thì hai bên là một.`,
  };
}
