/**
 * Mô hình vật lí của thí nghiệm "Hai bạn đẩy nhau trên giày trượt" (tn-l10-newton3-04, xem
 * content/thi-nghiem/tn-l10-newton3-04.json). Hàm thuần, không React, để kiểm bằng script.
 *
 * Quy ước: A ở bên trái (x âm khi trượt đi), B ở bên phải. Ban đầu hai bạn đứng yên, tay chạm nhau tại
 * x = 0. Trong khoảng chạm 0 ≤ t ≤ tc mỗi bạn chịu đúng một lực F (bằng nhau, ngược chiều — định luật III),
 * không có ma sát; sau tc không còn lực nên chuyển động thẳng đều.
 *   a_A = F/m_A, a_B = F/m_B (định luật II);  v = a·tc khi rời tay;  m_A·a_A = m_B·a_B = F.
 */
export interface PushParams {
  mA: number; // kg
  mB: number; // kg
  F: number; // N, lực mỗi bên
  tc: number; // s, thời gian hai tay còn chạm nhau
}

export interface PushState {
  t: number;
  /** vị trí tâm mỗi bạn, tính từ điểm chạm (m); A âm, B dương */
  xA: number;
  xB: number;
  /** vận tốc có dấu (m/s) */
  vA: number;
  vB: number;
  contact: boolean;
}

/** Khoảng cách ban đầu từ điểm chạm tới tâm mỗi bạn (m), chỉ để vẽ. */
export const HALF_GAP = 0.45;

export const accel = (F: number, m: number) => F / m;

export function stateAt(p: PushParams, t: number): PushState {
  const aA = accel(p.F, p.mA);
  const aB = accel(p.F, p.mB);
  const tt = Math.max(0, t);
  const dt = Math.min(tt, p.tc);
  const rest = Math.max(0, tt - p.tc);
  const vA = aA * dt; // độ lớn, A đi về bên trái
  const vB = aB * dt;
  const sA = 0.5 * aA * dt * dt + vA * rest;
  const sB = 0.5 * aB * dt * dt + vB * rest;
  return { t: tt, xA: -HALF_GAP - sA, xB: HALF_GAP + sB, vA: -vA, vB, contact: tt < p.tc };
}

/** Thời điểm kết thúc mô phỏng: khi một bạn ra khỏi khung `halfWidthM` hoặc quá `maxT` giây. */
export function endTime(p: PushParams, halfWidthM: number, maxT = 4): number {
  const aA = accel(p.F, p.mA);
  const aB = accel(p.F, p.mB);
  const aMax = Math.max(aA, aB);
  const vMax = aMax * p.tc;
  const sAtContact = 0.5 * aMax * p.tc * p.tc;
  const need = halfWidthM - HALF_GAP - sAtContact;
  const tExit = need <= 0 ? p.tc : p.tc + need / vMax;
  return Math.min(maxT, Math.max(p.tc + 0.4, tExit));
}

/** Đáp án câu dự đoán: bạn nào có gia tốc lớn hơn ("A" | "B" | "bang"). */
export function biggerAccel(p: PushParams): "A" | "B" | "bang" {
  if (Math.abs(p.mA - p.mB) < 1e-9) return "bang";
  return p.mA < p.mB ? "A" : "B";
}
