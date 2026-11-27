"use client";

/**
 * components/physics/gcpt/chung.tsx — phần dùng chung của các mô phỏng môn "Các phương pháp gia công phi truyền thống"
 * (lớp CTTC `gcpt`, docs/MON-GCPT-QUY-CACH.md). Mỗi mô phỏng gắn vào bài bằng hộp
 * `<div class="tl-box tl-note tl-mo-phong" data-mo-phong="gcpt-…">` (components/lessons/MoPhongPortals.tsx).
 *
 * Quy tắc UI (docs/QUY-TAC-THIET-KE.md): T2/V7 (đoán trước rồi mới mở), D2 (thanh trượt, nút cao 44 px),
 * N2 (≤ 4 nút mỗi hàng), N8 (số đo đặt ngay cạnh hình), M4 (cảnh báo có chữ, không chỉ màu), B4 (không gì tự chạy).
 * Số liệu là mô hình đơn giản hoá để thấy xu hướng; khoảng số ghi "tham khảo" như trong bài.
 */

import { useState, type ReactNode } from "react";
import { PredictGate, type PredictOption } from "../PredictGate";

export const segBtn = (on: boolean) =>
  `min-h-11 flex-1 rounded-lg px-2 text-sm font-medium transition active:scale-[0.98] ${
    on ? "bg-primary text-white" : "border border-line-strong bg-panel text-ink hover:bg-primary-soft"
  }`;

export const nutChinh =
  "min-h-11 rounded-lg bg-primary px-4 text-sm font-semibold text-white transition active:scale-[0.98] disabled:opacity-40";
export const nutPhu =
  "min-h-11 rounded-lg border border-line-strong bg-panel px-3 text-sm font-medium text-ink transition hover:bg-primary-soft active:scale-[0.98] disabled:opacity-40";

/** Khung chung: tiêu đề + câu đoán khoá mô phỏng. */
export function KhungMoPhong({
  ten,
  doan,
  children,
}: {
  ten: string;
  doan: { question: string; options: PredictOption[]; hint?: string };
  children: ReactNode;
}) {
  const [chon, setChon] = useState<number | null>(null);
  return (
    <section className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5" aria-label={ten}>
      <h2 className="font-display text-lg font-semibold">{ten}</h2>
      <div className="mt-3">
        <PredictGate question={doan.question} options={doan.options} choice={chon} onChoose={setChon} hint={doan.hint} />
      </div>
      {chon === null ? (
        <p className="mt-2 text-sm text-muted">🔒 Mô phỏng mở sau khi chọn một phương án.</p>
      ) : (
        <div className="mt-4">{children}</div>
      )}
    </section>
  );
}

/** Thanh trượt có nhãn + giá trị hiển thị. */
export function TruotSo({
  nhan,
  giaTri,
  hien,
  min,
  max,
  step,
  onChange,
}: {
  nhan: ReactNode;
  giaTri: number;
  hien: string;
  min: number;
  max: number;
  step: number;
  onChange: (v: number) => void;
}) {
  return (
    <label className="block text-sm">
      <span className="flex justify-between gap-2 text-muted">
        <span>{nhan}</span>
        <span className="font-mono text-ink">{hien}</span>
      </span>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={giaTri}
        onChange={(e) => onChange(Number(e.target.value))}
        className="h-11 w-full cursor-pointer accent-[var(--color-primary)]"
        aria-label={typeof nhan === "string" ? nhan : undefined}
      />
    </label>
  );
}

/** Hàng nút chọn một giá trị (≤ 4 nút, N2). */
export function HangNut<T extends string | number>({
  nhan,
  items,
  value,
  onChange,
}: {
  nhan: string;
  items: { value: T; text: string }[];
  value: T;
  onChange: (v: T) => void;
}) {
  return (
    <div className="space-y-1 text-sm">
      <span className="block text-muted">{nhan}</span>
      <div className="flex gap-2" role="group" aria-label={nhan}>
        {items.map((it) => (
          <button
            key={String(it.value)}
            type="button"
            aria-pressed={it.value === value}
            className={segBtn(it.value === value)}
            onClick={() => onChange(it.value)}
          >
            {it.text}
          </button>
        ))}
      </div>
    </div>
  );
}

/** Ô số đo. */
export function O({ nhan, so, phu }: { nhan: ReactNode; so: ReactNode; phu?: ReactNode }) {
  return (
    <div className="rounded-lg bg-surface-2 p-2">
      <dt className="text-xs text-muted">{nhan}</dt>
      <dd className="font-mono text-base font-semibold text-ink">{so}</dd>
      {phu && <dd className="text-xs text-muted">{phu}</dd>}
    </div>
  );
}

/** Thanh mức tương đối 0–1 có nhãn chữ (M4: không chỉ màu). */
export function ThanhMuc({ nhan, muc, chu, mau = "var(--color-primary)" }: { nhan: string; muc: number; chu: string; mau?: string }) {
  const m = Math.max(0, Math.min(1, muc));
  return (
    <div className="text-sm">
      <div className="flex justify-between gap-2">
        <span className="text-muted">{nhan}</span>
        <span className="text-ink">{chu}</span>
      </div>
      <div className="mt-1 h-2.5 overflow-hidden rounded-full bg-surface-2" aria-hidden>
        <div className="h-full rounded-full" style={{ width: `${Math.max(3, m * 100)}%`, background: mau }} />
      </div>
    </div>
  );
}

/** Dòng cảnh báo (có ký hiệu + chữ). */
export function CanhBao({ loai, children }: { loai: "ok" | "warn" | "danger"; children: ReactNode }) {
  const cls = loai === "ok" ? "border-ok text-ok" : loai === "warn" ? "border-warn text-warn" : "border-danger text-danger";
  const kh = loai === "ok" ? "✓" : loai === "warn" ? "⚠" : "✗";
  return (
    <p className={`rounded-lg border-l-4 bg-surface-2 px-3 py-2 text-sm ${cls}`} aria-live="polite">
      <span className="font-semibold">{kh}</span> <span className="text-ink">{children}</span>
    </p>
  );
}

/** Ghi chú mô hình ở cuối mô phỏng. */
export function GhiChuMoHinh({ children }: { children: ReactNode }) {
  return <p className="mt-3 text-xs leading-relaxed text-muted">{children}</p>;
}
