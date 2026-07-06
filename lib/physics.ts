/**
 * lib/physics.ts
 *
 * Thuần các hàm Vật lý cho dao động điều hòa (SHM) của con lắc lò xo.
 * Không phụ thuộc React — dễ test độc lập, dễ tái sử dụng ở nơi khác
 * (đồ thị, mô phỏng, phiếu bài tập tương tác...).
 *
 * Quy ước:
 *  - A: biên độ (m)
 *  - f: tần số (Hz)
 *  - t: thời gian (s)
 *  - ω (omega): tần số góc (rad/s) = 2πf
 *  - x(t) = A cos(ωt)         vị trí (m)
 *  - v(t) = -Aω sin(ωt)       vận tốc (m/s)
 *  - a(t) = -ω²x(t)           gia tốc (m/s²)
 */

export interface HarmonicParams {
  amplitude: number; // A, mét
  frequency: number; // f, Hz
}

export interface HarmonicState {
  t: number; // thời điểm hiện tại, giây
  x: number; // vị trí
  v: number; // vận tốc
  a: number; // gia tốc
  omega: number; // tần số góc
  period: number; // chu kỳ T = 1/f
}

/** Giới hạn biên độ cho phép trên UI (mét). */
export const AMPLITUDE_RANGE = { min: 0.02, max: 0.2, step: 0.005 } as const;

/** Giới hạn tần số cho phép trên UI (Hz). */
export const FREQUENCY_RANGE = { min: 0.5, max: 3, step: 0.05 } as const;

/** Tần số góc ω = 2πf (rad/s). */
export function angularFrequency(frequency: number): number {
  return 2 * Math.PI * frequency;
}

/** Chu kỳ T = 1/f (s). */
export function period(frequency: number): number {
  return 1 / frequency;
}

/** Vị trí x(t) = A cos(ωt). */
export function positionAt(t: number, amplitude: number, frequency: number): number {
  const omega = angularFrequency(frequency);
  return amplitude * Math.cos(omega * t);
}

/** Vận tốc v(t) = -Aω sin(ωt). */
export function velocityAt(t: number, amplitude: number, frequency: number): number {
  const omega = angularFrequency(frequency);
  return -amplitude * omega * Math.sin(omega * t);
}

/** Gia tốc a(t) = -ω²x(t). */
export function accelerationAt(t: number, amplitude: number, frequency: number): number {
  const omega = angularFrequency(frequency);
  const x = positionAt(t, amplitude, frequency);
  return -(omega * omega) * x;
}

/** Tính trọn bộ trạng thái dao động tại thời điểm t — dùng chung cho mọi component. */
export function computeHarmonicState(t: number, params: HarmonicParams): HarmonicState {
  const { amplitude, frequency } = params;
  const omega = angularFrequency(frequency);
  const x = positionAt(t, amplitude, frequency);
  const v = velocityAt(t, amplitude, frequency);
  const a = -(omega * omega) * x;
  return { t, x, v, a, omega, period: period(frequency) };
}

/** Giới hạn một giá trị trong khoảng [min, max]. */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

/**
 * Lấy mẫu x(t) trên một cửa sổ thời gian [t - windowDuration, t] để vẽ đồ thị
 * dạng "oscilloscope" cuộn theo thời gian thực — không cần lưu lịch sử vì
 * chuyển động là hàm xác định (deterministic).
 */
export function sampleWindow(
  t: number,
  amplitude: number,
  frequency: number,
  windowDuration: number,
  numPoints = 240
): { t: number; x: number }[] {
  const start = t - windowDuration;
  const points: { t: number; x: number }[] = [];
  for (let i = 0; i <= numPoints; i++) {
    const s = start + (windowDuration * i) / numPoints;
    points.push({ t: s, x: positionAt(s, amplitude, frequency) });
  }
  return points;
}

/** Định dạng số với số chữ số thập phân cố định, dùng cho các ô thông số. */
export function formatNumber(value: number, digits = 2): string {
  return value.toFixed(digits);
}
