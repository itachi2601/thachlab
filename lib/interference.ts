/**
 * lib/interference.ts
 *
 * Thuần các hàm Vật lí cho giao thoa sóng nước của HAI NGUỒN KẾT HỢP CÙNG PHA
 * (bỏ qua tắt dần theo khoảng cách — đúng phạm vi chương trình phổ thông) + hình
 * học khay sóng. Không phụ thuộc React/DOM nên test và tái sử dụng được ở nơi
 * khác (nhúng vào bài, phiếu bài tập, mô phỏng khe Young...).
 *
 * Nguồn gốc: `content/thi-nghiem/tn-l11-giaothoa-01.json` (Bài 12. Giao thoa
 * sóng, Vật lí 11) — tham số, khoảng giá trị và bẫy hiểu sai lấy từ file đó.
 *
 * Quy ước đơn vị (theo đúng thí nghiệm khay sóng, không đổi sang SI):
 *  - f: tần số cần rung (Hz) · v: tốc độ truyền sóng (cm/s) · λ = v/f (cm)
 *  - AB: khoảng cách hai nguồn (cm) · d₁ = MA, d₂ = MB (cm)
 *  - Hiệu đường đi: Δd = d₂ − d₁
 *  - Cực đại: Δd = kλ · Cực tiểu: Δd = (k + ½)λ  (k = 0, ±1, ±2, …)
 *  - N_max: số k nguyên thoả −AB/λ < k < AB/λ  (không lấy hai đầu A, B)
 *  - N_min: số k nguyên thoả −AB/λ − ½ < k < AB/λ − ½
 *
 * Vì sao dùng bao hình chứ không phải li độ tức thời: vân giao thoa trên mặt
 * nước là các đường SÁNG/TỐI ĐỨNG YÊN (thí nghiệm chỉ thấy chúng đứng yên), nên
 * biên độ tổng hợp tại M — |2a·cos(πΔd/λ)| — mới là thứ cần vẽ; nó không phụ
 * thuộc thời gian, nhờ vậy mô phỏng không cần vòng lặp hình ảnh nào.
 */

/** Kích thước khay sóng vẽ trên màn hình (cm) — cố định để toạ độ điểm M ổn định. */
export const TANK = { widthCm: 20, heightCm: 10 } as const;

/** Khoảng giá trị điều chỉnh, lấy từ `tham_so` của spec thí nghiệm. */
export const F_RANGE = { min: 10, max: 60, step: 5 } as const;
export const V_RANGE = { min: 10, max: 60, step: 5 } as const;
export const AB_RANGE = { min: 3, max: 15, step: 0.5 } as const;

/**
 * Giá trị mặc định: f = 20 Hz, v = 30 cm/s, AB = 6 cm ⇒ λ = 1,5 cm và AB = 4λ —
 * đúng hình 2 của bài (7 đường cực đại, 8 đường cực tiểu, trung trực là k = 0).
 */
export const TANK_DEFAULTS = { f: 20, v: 30, AB: 6 } as const;

/** Điểm M mặc định: nằm trên đường trung trực (cực đại k = 0) để học sinh thấy ngay một vân. */
export const DEFAULT_MARKER = { x: TANK.widthCm / 2, y: 2.6 } as const;

/** Hai nguồn luôn nằm trên đường giữa khay, đối xứng qua trung trực. */
export function sourcePositions(AB: number): {
  a: { x: number; y: number };
  b: { x: number; y: number };
} {
  const y = TANK.heightCm / 2;
  return {
    a: { x: TANK.widthCm / 2 - AB / 2, y },
    b: { x: TANK.widthCm / 2 + AB / 2, y },
  };
}

/** λ = v/f (cm). */
export function wavelength(frequency: number, speed: number): number {
  return speed / frequency;
}

/** Khoảng cách hai điểm (cm). */
export function distance(
  x1: number,
  y1: number,
  x2: number,
  y2: number
): number {
  const dx = x2 - x1;
  const dy = y2 - y1;
  return Math.sqrt(dx * dx + dy * dy);
}

/**
 * Biên độ tổng hợp chuẩn hoá tại điểm có hiệu đường đi Δd (0 = nút, 1 = bụng):
 * |2a·cos(πΔd/λ)| / 2a. Không phụ thuộc thời gian.
 */
export function envelopeIntensity(
  d1: number,
  d2: number,
  lambda: number
): number {
  return Math.abs(Math.cos((Math.PI * (d2 - d1)) / lambda));
}

/**
 * Một nguồn duy nhất (đã tắt nguồn B): mặt nước chỉ còn sóng tròn. Ảnh chụp
 * tức thời của sóng tròn là các vành đồng tâm cách nhau λ/2 (sáng/tối xen kẽ).
 */
export function singleSourceIntensity(
  r: number,
  lambda: number
): number {
  return Math.abs(Math.cos((Math.PI * r) / lambda));
}

export type FringeKind = "max" | "min" | "mid";

/**
 * Độ giảm biên độ do sóng toả tròn trên mặt nước — CHỈ dùng cho phần VẼ.
 *
 * Vì sao cần: spec `tn-l11-giaothoa-01` giả thiết bỏ qua tắt dần để tính vân,
 * nhưng nếu vẽ đúng giả thiết đó thì vùng xa hai nguồn (Δd → ±AB) sáng đều
 * thành một mảng lớn và mắt không còn thấy "vân" nữa; khay sóng thật bao giờ
 * cũng mờ dần ở xa. Hệ số này KHÔNG được dùng cho việc đếm vân hay phân loại
 * điểm M — hai việc đó vẫn theo đúng mô hình bỏ qua tắt dần.
 */
export function spreadingFalloff(r: number, lambda: number): number {
  const r0 = 6 * lambda;
  return Math.sqrt(r0 / (r0 + Math.max(0, r)));
}

/** Cường độ vẽ tại M khi hai nguồn cùng phát: bao hình × độ tắt dần theo khoảng cách. */
export function twoSourceFieldIntensity(
  d1: number,
  d2: number,
  lambda: number
): number {
  return envelopeIntensity(d1, d2, lambda) * spreadingFalloff((d1 + d2) / 2, lambda);
}

/** Cường độ vẽ khi đã tắt nguồn B: vành sóng tròn quanh A, mờ dần ở xa. */
export function singleSourceFieldIntensity(r: number, lambda: number): number {
  return singleSourceIntensity(r, lambda) * spreadingFalloff(r, lambda);
}

// ---------------------------------------------------------------------------
// Ảnh động (li độ tức thời) — tách sẵn pha để mỗi khung hình thật rẻ
// ---------------------------------------------------------------------------
//
// Li độ tại M: u(t) = Σ aᵢ·cos(ωt − k·dᵢ) với k = 2π/λ, aᵢ là biên độ (đã tính
// độ tắt dần). Khai triển cos(ωt − kd) = cosωt·cos(kd) + sinωt·sin(kd):
//
//     u(t) = cos(ωt)·C + sin(ωt)·S,   C = Σ aᵢ·cos(k·dᵢ),  S = Σ aᵢ·sin(k·dᵢ)
//
// C và S KHÔNG phụ thuộc thời gian → tính một lần cho mỗi điểm ảnh khi đổi f, v,
// AB; mỗi khung hình chỉ còn u = cosφ·C + sinφ·S (2 phép nhân), không gọi cos/sin
// trong vòng lặp vẽ. Đây là lý do ảnh động chạy được 60 khung hình/giây trên
// điện thoại mà không cần thư viện nào.

/** Hệ số pha k = 2π/λ (rad/cm). */
export function waveNumber(lambda: number): number {
  return (2 * Math.PI) / lambda;
}

export interface Phasor {
  c: number;
  s: number;
}

/**
 * Phasor của hai nguồn tại điểm cách chúng d₁, d₂. Biên độ lấy theo đúng độ tắt
 * dần dùng cho phần vẽ, chia 2 để u ∈ [−1, 1] (khớp thang sáng của ảnh đứng yên).
 */
export function twoSourcePhasors(d1: number, d2: number, lambda: number): Phasor {
  const k = waveNumber(lambda);
  const a1 = spreadingFalloff(d1, lambda) / 2;
  const a2 = spreadingFalloff(d2, lambda) / 2;
  return {
    c: a1 * Math.cos(k * d1) + a2 * Math.cos(k * d2),
    s: a1 * Math.sin(k * d1) + a2 * Math.sin(k * d2),
  };
}

/** Phasor khi chỉ còn nguồn A (nguồn B đã tắt): mặt nước chỉ có sóng tròn từ A. */
export function singleSourcePhasor(r: number, lambda: number): Phasor {
  const k = waveNumber(lambda);
  const a = spreadingFalloff(r, lambda) / 2;
  return { c: a * Math.cos(k * r), s: a * Math.sin(k * r) };
}

/** Li độ chuẩn hoá tại thời điểm có pha ωt: u = cosφ·C + sinφ·S. */
export function displacementFromPhasor(
  phasor: Phasor,
  cosPhase: number,
  sinPhase: number
): number {
  return phasor.c * cosPhase + phasor.s * sinPhase;
}

/**
 * Chu kỳ HIỂN THỊ của ảnh động (giây) — cố ý không phải chu kỳ thật 1/f.
 *
 * Sóng thật ở thí nghiệm này có f = 10–60 Hz, mắt chỉ thấy nhoè; nên hình được
 * tua chậm: tốc độ lan trên màn hình 6 cm/s, kẹp trong 0,4–1,5 s mỗi chu kỳ để
 * vừa theo được bằng mắt vừa không nhấp nháy (bước sóng nhỏ thì chu kỳ ngắn,
 * chạm sàn 0,4 s). Bước sóng VẼ vẫn đúng bằng λ thật — chỉ thời gian bị tua.
 */
export const VISUAL_SPEED_CM_PER_S = 6;
export const VISUAL_PERIOD_RANGE = { min: 0.4, max: 1.5 } as const;

export function visualPeriod(lambda: number): number {
  return Math.min(
    VISUAL_PERIOD_RANGE.max,
    Math.max(VISUAL_PERIOD_RANGE.min, lambda / VISUAL_SPEED_CM_PER_S)
  );
}

/** Sai số cho phép khi coi M nằm ĐÚNG trên một vân (tính theo λ). */
export const FRINGE_TOLERANCE = 0.06;

/** Δd/λ: số nguyên ⇒ cực đại, nguyên + ½ ⇒ cực tiểu. */
export function fringeRatio(d1: number, d2: number, lambda: number): number {
  return (d2 - d1) / lambda;
}

/**
 * Phân loại một điểm theo hiệu đường đi. `tolerance` tính theo λ (mặc định 6%):
 * ngón tay không đặt chính xác được nên phải có vùng "gần đúng", nhưng KHÔNG
 * tự kéo điểm M về vân — học sinh vẫn phải tự tìm chỗ sáng/tối.
 */
export function classifyPoint(
  d1: number,
  d2: number,
  lambda: number,
  tolerance = FRINGE_TOLERANCE
): { kind: FringeKind; ratio: number; order: number } {
  const ratio = fringeRatio(d1, d2, lambda);
  const nearestMax = Math.round(ratio);
  if (Math.abs(ratio - nearestMax) <= tolerance) {
    return { kind: "max", ratio, order: nearestMax };
  }
  const nearestMin = Math.round(ratio - 0.5) + 0.5;
  if (Math.abs(ratio - nearestMin) <= tolerance) {
    return { kind: "min", ratio, order: nearestMin - 0.5 };
  }
  return { kind: "mid", ratio, order: Math.floor(ratio) };
}

export interface ExtremaCount {
  /** AB/λ — càng lớn thì vân càng dày. */
  ratio: number;
  maxima: number;
  minima: number;
  maxOrders: number[];
  minOrders: number[];
}

/**
 * Đếm cực đại / cực tiểu TRÊN ĐOẠN AB (hai nguồn cùng pha, không lấy hai đầu):
 *  - Cực đại: −AB/λ < k < AB/λ
 *  - Cực tiểu: −AB/λ − ½ < k < AB/λ − ½
 */
export function countExtrema(AB: number, lambda: number): ExtremaCount {
  const ratio = AB / lambda;
  const eps = 1e-9;
  const limit = Math.ceil(ratio) + 1;
  const maxOrders: number[] = [];
  const minOrders: number[] = [];
  for (let k = -limit; k <= limit; k++) {
    if (-ratio < k - eps && k + eps < ratio) maxOrders.push(k);
    if (-ratio - 0.5 < k - eps && k + eps < ratio - 0.5) minOrders.push(k);
  }
  return {
    ratio,
    maxima: maxOrders.length,
    minima: minOrders.length,
    maxOrders,
    minOrders,
  };
}

export type InterferenceMessageKind = FringeKind | "off";

export interface InterferenceMessage {
  kind: InterferenceMessageKind;
  text: string;
}

/**
 * Câu nhận xét dưới khay sóng — nguồn sự thật duy nhất cho phần chữ của mô
 * phỏng, tách khỏi React để đổi giọng văn mà không đụng vào phần vẽ.
 *
 * Cố ý trả lời thẳng bẫy trong `hien_tuong_hay_sai` của spec: điểm cực tiểu
 * KHÔNG phải chỗ không có sóng tới — hai sóng vẫn tới và triệt tiêu nhau.
 * Khi tắt nguồn B thì không còn gì để triệt tiêu → nói rõ như thí nghiệm
 * "bịt một loa" trong bài (tiếng to lên chứ không phải nhỏ đi).
 */
export function messageFor(
  d1: number,
  d2: number,
  lambda: number,
  format: (value: number, digits?: number) => string
): InterferenceMessage {
  const delta = d2 - d1;
  const { kind, ratio, order } = classifyPoint(d1, d2, lambda);
  const numbers =
    `d₁ = ${format(d1, 2)} cm · d₂ = ${format(d2, 2)} cm · ` +
    `d₂ − d₁ = ${format(delta, 2)} cm = ${format(ratio, 2)}λ`;

  if (kind === "max") {
    const bac = Math.abs(order);
    return {
      kind,
      text:
        `${numbers} = kλ (k = ${order}) → M là CỰC ĐẠI bậc ${bac}: hai sóng tới M cùng pha, ` +
        `biên độ 2a — mạnh nhất.`,
    };
  }

  if (kind === "min") {
    const k = Math.round(order);
    return {
      kind,
      text:
        `${numbers} = (k + ½)λ (k = ${k}) → M là CỰC TIỂU: hai sóng tới M ngược pha nên ` +
        `triệt tiêu nhau. Cả hai sóng vẫn tới M — không phải "không có sóng tới".`,
    };
  }

  const nearestMax = Math.round(ratio);
  const nearestMinK = Math.round(ratio - 0.5);
  return {
    kind,
    text:
      `${numbers} → M nằm giữa vân cực đại bậc ${nearestMax} và vân cực tiểu (k = ${nearestMinK}), ` +
      `biên độ trung gian. Kéo M sang đường sáng hoặc đường tối gần nhất.`,
  };
}

/** Câu nhận xét khi đã tắt nguồn B (nhấc một mũi nhọn / bịt một loa). */
export const SOURCE_B_OFF_MESSAGE: InterferenceMessage = {
  kind: "off",
  text:
    "Đã tắt nguồn B. Vân giao thoa biến mất, khay chỉ còn sóng tròn từ A: mỗi điểm chỉ nhận " +
    "MỘT sóng nên không còn chỗ nào triệt tiêu — đúng như khi bịt một loa, chỗ trước kia nghe " +
    "nhỏ nhất lại to lên. Bật lại nguồn B rồi kéo M về đúng một đường tối để so.",
};
