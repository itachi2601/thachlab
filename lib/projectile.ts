/**
 * lib/projectile.ts
 *
 * Thuần các hàm Vật lý cho chuyển động ném xiên (bỏ qua sức cản không khí —
 * đúng phạm vi chương trình phổ thông) + hình học của thao tác "kéo ná cao su".
 * Không phụ thuộc React/DOM nên test và tái sử dụng được ở nơi khác.
 *
 * Quy ước:
 *  - v0: tốc độ ném ban đầu (m/s), α: góc ném so với phương ngang (độ)
 *  - g: gia tốc trọng trường (m/s²); t: thời gian (s)
 *  - x(t) = v0·cosα·t                    (m)
 *  - y(t) = v0·sinα·t − ½gt²              (m)
 *  - R = v0²·sin2α/g  (tầm xa) · h = v0²sin²α/(2g) (độ cao cực đại) · T = 2v0·sinα/g
 */

export type GravityKey = "earth" | "moon";

export interface GravityOption {
  key: GravityKey;
  label: string;
  g: number; // m/s²
}

/** Hai môi trường trọng trường cho tab chọn trên hero. */
export const GRAVITIES: Record<GravityKey, GravityOption> = {
  earth: { key: "earth", label: "Trái Đất", g: 9.8 },
  moon: { key: "moon", label: "Mặt Trăng", g: 1.6 },
};

/** Giới hạn tốc độ ném cho phép (m/s) — trần 20 m/s để tầm xa tối đa 40,8 m vừa khung hình. */
export const V0_MIN = 6;
export const V0_MAX = 20;

/** Góc ném cho phép (độ): chặn hai đầu để tia ném không nằm ngang/dựng đứng. */
export const ANGLE_MIN = 3;
export const ANGLE_MAX = 87;

/**
 * Góc cho tầm xa lớn nhất khi ném và rơi cùng độ cao. Kéo lệch trong
 * SNAP_TOLERANCE độ quanh giá trị này thì "dính" về đúng 45° — giảm nhiễu ngón
 * tay trên điện thoại, không làm hộ phần suy luận (học sinh vẫn phải tự tìm ra).
 */
export const OPTIMAL_ANGLE = 45;
export const SNAP_TOLERANCE = 1.5;

/** Thao tác kéo: kéo dài MAX_PULL_PX thì đạt tốc độ tối đa; dưới MIN_PULL_PX coi như chưa ném. */
export const MAX_PULL_PX = 88;
export const MIN_PULL_PX = 12;

/** Khoảng thời gian giữa hai "chấm" vẽ trên quỹ đạo (s) — mắt thấy vₓ không đổi. */
export const DOT_INTERVAL = 0.1;

export const toRad = (deg: number): number => (deg * Math.PI) / 180;

export function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

/** Tầm xa R = v0²·sin2α/g (m). */
export function rangeOf(v0: number, angleDeg: number, g: number): number {
  return (v0 * v0 * Math.sin(2 * toRad(angleDeg))) / g;
}

/** Độ cao cực đại h = v0²sin²α/(2g) (m). */
export function apexOf(v0: number, angleDeg: number, g: number): number {
  const sin = Math.sin(toRad(angleDeg));
  return (v0 * v0 * sin * sin) / (2 * g);
}

/** Thời gian bay T = 2v0·sinα/g (s). */
export function hangOf(v0: number, angleDeg: number, g: number): number {
  return (2 * v0 * Math.sin(toRad(angleDeg))) / g;
}

/** Vị trí vật tại thời điểm t (m). */
export function positionAt(
  t: number,
  v0: number,
  angleDeg: number,
  g: number
): { x: number; y: number } {
  const a = toRad(angleDeg);
  return {
    x: v0 * Math.cos(a) * t,
    y: v0 * Math.sin(a) * t - 0.5 * g * t * t,
  };
}

/** Lấy mẫu quỹ đạo từ lúc ném tới lúc chạm đất — dùng để vẽ nét liền/nét đứt. */
export function trajectoryPoints(
  v0: number,
  angleDeg: number,
  g: number,
  steps = 90
): { x: number; y: number }[] {
  const T = hangOf(v0, angleDeg, g);
  const points: { x: number; y: number }[] = [];
  for (let i = 0; i <= steps; i++) points.push(positionAt((T * i) / steps, v0, angleDeg, g));
  return points;
}

/**
 * Vị trí các chấm cách nhau đúng DOT_INTERVAL giây. Vì vₓ không đổi nên các
 * chấm cách đều theo phương ngang — đây là "công cụ tư duy" chính của mô phỏng.
 */
export function equalTimeDots(
  v0: number,
  angleDeg: number,
  g: number
): { x: number; y: number }[] {
  const T = hangOf(v0, angleDeg, g);
  const dots: { x: number; y: number }[] = [];
  for (let t = DOT_INTERVAL; t <= T + 1e-9; t += DOT_INTERVAL) {
    dots.push(positionAt(t, v0, angleDeg, g));
  }
  return dots;
}

/**
 * Kéo kiểu ná cao su: vector kéo tính bằng px màn hình (dxs, dys — màn hình có
 * y hướng xuống) → góc ném (độ) và tốc độ (m/s). Ném ngược hướng kéo.
 *
 * @param snap bật "dính" về 45° khi lệch trong SNAP_TOLERANCE độ.
 */
export function aimFromPull(
  dxs: number,
  dys: number,
  snap = true
): { angle: number; v0: number; pullLength: number } {
  const pullLength = Math.hypot(dxs, dys);
  let angle = (Math.atan2(-dys, dxs) * 180) / Math.PI;
  angle = clamp(angle, ANGLE_MIN, ANGLE_MAX);
  if (snap && Math.abs(angle - OPTIMAL_ANGLE) <= SNAP_TOLERANCE) angle = OPTIMAL_ANGLE;

  const ratio = clamp((pullLength - MIN_PULL_PX) / MAX_PULL_PX, 0, 1);
  return { angle, v0: V0_MIN + (V0_MAX - V0_MIN) * ratio, pullLength };
}

/** Một lần ném đã hoàn tất — đầu vào cho phần nhận xét. */
export interface Shot {
  angle: number;
  v0: number;
  gKey: GravityKey;
  range: number;
}

export interface Feedback {
  text: string;
  kind: "goal" | "best" | "win";
}

/**
 * Câu nhận xét sau mỗi lần ném. Thứ tự ưu tiên: đạt tầm xa cực đại (điều đáng
 * nhớ nhất) → cặp góc phụ nhau cho cùng tầm xa → kỷ lục mới → gợi ý chỉnh góc.
 * Tách khỏi React để đổi giọng văn mà không phải đụng vào mô phỏng.
 */
export function feedbackFor(
  shot: Shot,
  history: Shot[],
  format: (value: number, digits?: number) => string
): Feedback {
  const g = GRAVITIES[shot.gKey].g;
  const maxRange = (shot.v0 * shot.v0) / g;
  // g nhỏ hơn 6 lần → cùng v₀ bay xa và bay lâu hơn ~6 lần: nói rõ để không bị hiểu là lỗi mô phỏng.
  const moonNote =
    shot.gKey === "moon" ? " Trên Mặt Trăng g nhỏ 6 lần nên cùng v₀ bay xa gấp ~6 lần." : "";

  // Đạt đúng góc tối ưu: đây là điều đáng nhớ nhất nên nói thẳng ra công thức.
  if (Math.abs(shot.angle - OPTIMAL_ANGLE) <= 0.6) {
    return {
      kind: "win",
      text:
        `Đúng rồi: α = ${OPTIMAL_ANGLE}° cho tầm xa lớn nhất khi ném và rơi cùng độ cao. ` +
        `R = v₀²/g = ${format(shot.range, 1)} m — công thức này em vừa tìm ra bằng cách ném.` +
        moonNote,
    };
  }

  // Sát cực đại nhưng chưa đúng 45°: nói thật con số, đừng gán cho học sinh góc họ chưa ném.
  if (shot.range >= maxRange * 0.99) {
    const gap = maxRange - shot.range;
    return {
      kind: "best",
      text:
        `Sát cực đại rồi: α = ${Math.round(shot.angle)}° cho R = ${format(shot.range, 1)} m, ` +
        `chỉ kém tầm xa lớn nhất ${format(gap, 2)} m. Thử quanh ${OPTIMAL_ANGLE}° xem có hơn không.` +
        moonNote,
    };
  }

  // Hai góc phụ nhau (α và 90° − α) cho cùng tầm xa — chỉ khác độ cao và thời gian bay.
  const pair = history.find(
    (s) =>
      s.gKey === shot.gKey &&
      Math.abs(s.v0 - shot.v0) < 0.3 &&
      Math.abs(s.range - shot.range) / Math.max(shot.range, 1) < 0.02 &&
      Math.abs(s.angle + shot.angle - 90) <= 2.5
  );
  if (pair) {
    return {
      kind: "win",
      text:
        `Hai góc phụ nhau (${Math.round(pair.angle)}° và ${Math.round(shot.angle)}°) cho cùng tầm xa ` +
        `${format(shot.range, 1)} m — chỉ khác độ cao và thời gian bay.` +
        moonNote,
    };
  }

  const previousBest = history.reduce((max, s) => Math.max(max, s.range), 0);
  if (history.length > 0 && shot.range > previousBest + 0.05) {
    return {
      kind: "best",
      text:
        `Xa nhất từ trước tới giờ: ${format(shot.range, 1)} m ở α = ${Math.round(shot.angle)}°. ` +
        `Còn góc nào xa hơn không?` +
        moonNote,
    };
  }

  return {
    kind: "goal",
    text:
      `R = ${format(shot.range, 1)} m ở α = ${Math.round(shot.angle)}°. ` +
      `Thử lệch vài độ quanh góc này xem tầm xa tăng hay giảm.` +
      moonNote,
  };
}
