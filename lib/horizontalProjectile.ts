/**
 * lib/horizontalProjectile.ts
 *
 * Vật lí thuần cho chuyển động NÉM NGANG — bài toán "máy bay cứu hộ thả hàng"
 * (Vật lí 10, Bài 12. Chuyển động ném; bỏ qua sức cản không khí).
 * Không phụ thuộc React/DOM nên test và tái sử dụng được ở nơi khác.
 *
 * Quy ước:
 *  - Trục x nằm ngang theo chiều bay, tính bằng mét dọc theo mặt đất; gốc x = 0
 *    là chỗ máy bay bắt đầu lượt bay (mép trái khung nhìn).
 *  - Bãi đáp ở PAD_X, rộng 2·PAD_HALF. h: độ cao máy bay (m). v₀: tốc độ máy bay (m/s).
 *  - Gói hàng rời máy bay với vₓ đúng bằng v₀ và v_y = 0, nên nó LUÔN nằm thẳng
 *    dưới máy bay cho tới lúc chạm đất — đó là hình ảnh chứng minh hai phương
 *    chuyển động độc lập.
 *
 *  t = √(2h/g)   thời gian rơi — CHỈ phụ thuộc h, không phụ thuộc v₀
 *  L = v₀·t      khoảng cách phải thả trước bãi đáp
 *  x = v₀·t′     quãng ngang của gói sau t′ giây kể từ lúc thả
 */

import { DOT_INTERVAL, clamp } from "./projectile";

export { DOT_INTERVAL };

/** Gia tốc trọng trường dùng cho mô phỏng (m/s²). */
export const G_EARTH = 9.8;

/** Độ cao máy bay cho phép (m). */
export const H_RANGE = { min: 60, max: 110, step: 5, initial: 85 } as const;

/**
 * Tốc độ máy bay cho phép (m/s). Trần 50 chứ không cao hơn: điểm thả đúng phải
 * còn cách mép trái ít nhất RUNUP mét để học sinh kịp nhìn thấy máy bay trước khi
 * quyết định (xem thahang-check.mts, phép kiểm "có đà nhìn thấy máy bay").
 */
export const V0_RANGE = { min: 40, max: 50, step: 1, initial: 45 } as const;

/** Vị trí tâm bãi đáp (m) và nửa bề rộng bãi đáp (m) — thả lệch trong ±PAD_HALF là trúng. */
export const PAD_X = 300;
export const PAD_HALF = 20;

/** Khung nhìn: bề ngang (m) và chiều cao tối đa (m) — dùng để tính tỉ lệ px/m. */
export const VIEW_X = 360;
export const VIEW_Y = 132;

/**
 * Quãng chạy đà trước vùng thả. Máy bay xuất hiện sớm hơn điểm thả sớm nhất
 * chừng này để học sinh kịp nhìn thấy nó trước khi phải quyết định (~1,1–1,5 s),
 * nhưng không phải chờ lâu.
 */
export const RUNUP = 60;

/** Thời gian rơi t = √(2h/g) (s). */
export function fallTime(h: number, g: number = G_EARTH): number {
  return Math.sqrt((2 * h) / g);
}

/** Quãng đường ngang gói hàng đi được trong cả thời gian rơi: L = v₀·t (m). */
export function reachOf(v0: number, h: number, g: number = G_EARTH): number {
  return v0 * fallTime(h, g);
}

/** Vị trí máy bay phải thả để gói rơi trúng tâm bãi đáp (m). */
export function requiredReleaseX(v0: number, h: number, g: number = G_EARTH): number {
  return PAD_X - reachOf(v0, h, g);
}

/** Chỗ máy bay bắt đầu lượt bay (m) — sớm hơn điểm thả sớm nhất RUNUP mét. */
export function startXOf(v0: number, h: number, g: number = G_EARTH): number {
  return Math.max(0, requiredReleaseX(v0, h, g) - RUNUP);
}

/** Điểm gói hàng chạm đất nếu thả ở releaseX (m). */
export function landingOf(
  releaseX: number,
  v0: number,
  h: number,
  g: number = G_EARTH
): number {
  return releaseX + reachOf(v0, h, g);
}

/** Độ cao còn lại của gói sau t′ giây kể từ lúc thả (m, không âm). */
export function heightAt(tAfterDrop: number, h: number, g: number = G_EARTH): number {
  return Math.max(0, h - 0.5 * g * tAfterDrop * tAfterDrop);
}

/**
 * Vị trí gói hàng sau t′ giây kể từ lúc thả, trong hệ toạ độ của khung nhìn:
 * x dọc mặt đất (m), y là độ cao so với mặt đất (m) — dùng để vẽ quỹ đạo.
 */
export function packageAt(
  tAfterDrop: number,
  releaseX: number,
  v0: number,
  h: number,
  g: number = G_EARTH
): { x: number; y: number } {
  return { x: releaseX + v0 * tAfterDrop, y: heightAt(tAfterDrop, h, g) };
}

/**
 * Các chấm cách nhau đúng DOT_INTERVAL giây kể từ lúc thả. Cách đều theo phương
 * ngang (vₓ không đổi) nhưng mau dần theo phương thẳng đứng — công cụ tư duy
 * giống tab "Ném xiên".
 */
export function equalTimeDots(
  releaseX: number,
  v0: number,
  h: number,
  g: number = G_EARTH
): { x: number; y: number }[] {
  const T = fallTime(h, g);
  const dots: { x: number; y: number }[] = [];
  for (let t = DOT_INTERVAL; t <= T + 1e-9; t += DOT_INTERVAL) {
    dots.push(packageAt(t, releaseX, v0, h, g));
  }
  return dots;
}

/** Một lượt thả: cài đặt chuyến bay + chỗ thả thật (null = không bấm thả). */
export interface DropAttempt {
  h: number;
  v0: number;
  releaseX: number | null;
}

/** Kết quả một lượt thả. */
export interface DropOutcome {
  tFall: number;
  landingX: number | null;
  delta: number | null; // landingX − PAD_X (m); âm = rơi trước bãi đáp
  hit: boolean;
  kind: "win" | "best" | "goal";
}

/**
 * Phân loại kết quả: trúng bãi đáp (|Δ| ≤ PAD_HALF) → win; sát (|Δ| ≤ 2·PAD_HALF)
 * → best; còn lại và trường hợp không thả → goal.
 */
export function outcomeOf(attempt: DropAttempt, g: number = G_EARTH): DropOutcome {
  const tFall = fallTime(attempt.h, g);
  if (attempt.releaseX === null) {
    return { tFall, landingX: null, delta: null, hit: false, kind: "goal" };
  }
  const landingX = landingOf(attempt.releaseX, attempt.v0, attempt.h, g);
  const delta = landingX - PAD_X;
  const hit = Math.abs(delta) <= PAD_HALF;
  return { tFall, landingX, delta, hit, kind: hit ? "win" : Math.abs(delta) <= 2 * PAD_HALF ? "best" : "goal" };
}

export interface Feedback {
  text: string;
  kind: "goal" | "best" | "win";
}

/** Câu mở đầu khi máy bay còn đứng ở mép trái, chưa bay. */
export function readyFeedback(
  h: number,
  v0: number,
  format: (value: number, digits?: number) => string
): Feedback {
  return {
    kind: "goal",
    text:
      `Máy bay ở độ cao h = ${format(h, 1)} m, bay ngang v₀ = ${format(v0, 1)} m/s. ` +
      `Bấm "Cho máy bay bay" rồi bấm "Thả hàng" đúng lúc để gói rơi trúng bãi đáp. ` +
      `Thời gian rơi t = √(2h/g) = ${format(fallTime(h), 2)} s.`,
  };
}

/**
 * Câu nhận xét sau mỗi lượt thả. Tách khỏi React để đổi giọng văn mà không phải
 * đụng vào mô phỏng.
 *
 * `prev` là lượt thả liền trước (nếu có) — dùng để chỉ ra điều đáng nhớ nhất:
 * đổi v₀ mà giữ h thì thời gian rơi KHÔNG đổi, chỉ chỗ phải thả đổi.
 */
export function describeDrop(
  attempt: DropAttempt,
  outcome: DropOutcome,
  prev: DropAttempt | null,
  format: (value: number, digits?: number) => string
): Feedback {
  const L = reachOf(attempt.v0, attempt.h);
  const numberNote =
    prev && prev.releaseX !== null && Math.abs(prev.h - attempt.h) < 0.01 && Math.abs(prev.v0 - attempt.v0) > 0.01
      ? ` Lần trước v₀ = ${format(prev.v0, 1)} m/s, t rơi vẫn là ${format(fallTime(attempt.h), 2)} s — tốc độ máy bay chỉ đổi CHỖ phải thả, không đổi thời gian rơi.`
      : "";

  if (attempt.releaseX === null) {
    return {
      kind: "goal",
      text:
        `Máy bay đã bay qua bãi đáp mà chưa thả hàng. Thả từ đây thì gói luôn rơi quá: ` +
        `phải thả trước bãi đáp L = v₀·√(2h/g) = ${format(L, 1)} m, tức là tại vạch "phải thả ở đây".${numberNote}`,
    };
  }

  const delta = outcome.delta ?? 0;
  const short = delta < 0;
  const where = short
    ? `rơi lệch ${format(Math.abs(delta), 1)} m về phía TRƯỚC bãi đáp (thả sớm quá)`
    : `rơi lệch ${format(Math.abs(delta), 1)} m QUÁ bãi đáp (thả muộn quá)`;

  if (outcome.hit) {
    return {
      kind: "win",
      text:
        `Trúng bãi đáp! Gói rơi mất t = √(2h/g) = ${format(outcome.tFall, 2)} s; trong ngần ấy thời gian ` +
        `máy bay đi được L = v₀t = ${format(attempt.v0, 1)} · ${format(outcome.tFall, 2)} ≈ ${format(L, 1)} m ` +
        `— đúng bằng khoảng cách em phải thả trước bãi đáp.${numberNote}`,
    };
  }

  if (outcome.kind === "best") {
    return {
      kind: "best",
      text:
        `Sát rồi: gói ${where}. Cần thả khi máy bay còn cách bãi đáp ${format(L, 1)} m ` +
        `(em thả lúc còn ${format(PAD_X - attempt.releaseX, 1)} m).${numberNote}`,
    };
  }

  return {
    kind: "goal",
    text:
      `Trượt: gói ${where}. Cần thả khi máy bay còn cách bãi đáp L = v₀·√(2h/g) = ${format(L, 1)} m ` +
      `(em thả lúc còn ${format(PAD_X - attempt.releaseX, 1)} m).${numberNote}`,
  };
}

/** Kẹp giá trị thanh trượt về đúng khoảng cho phép (dùng chung cho UI và phím mũi tên). */
export function clampHeight(h: number): number {
  return clamp(h, H_RANGE.min, H_RANGE.max);
}

export function clampSpeed(v0: number): number {
  return clamp(v0, V0_RANGE.min, V0_RANGE.max);
}
