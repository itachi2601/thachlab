"use client";

/**
 * components/physics/do-luong/chung.tsx — phần dùng chung của bốn dụng cụ đo (Gói A,
 * docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 3): chọn chế độ, đọc số học sinh gõ, ô Luyện đọc, tiến độ localStorage.
 *
 * Quy tắc UI (docs/QUY-TAC-THIET-KE.md): N2 (≤ 4 nút mỗi hàng), N6 (Xem cách đọc trước, Luyện đọc sau), D2 (đích chạm 44 px),
 * D6 (inputmode="decimal", dấu phẩy hoặc chấm đều nhận), L1/L4 (chấm ngay, chỉ đúng chỗ sai và việc tiếp theo),
 * L2 (tiến độ theo nhiệm vụ đang làm), L3 (không điểm, không rank), M4 (đúng/sai có ✓/✗ kèm chữ).
 * Không gọi Supabase: tiến độ ở localStorage (bọc try/catch, chạy được khi bị chặn).
 */

import { useCallback, useEffect, useState, type ReactNode } from "react";

export type CheDo = "xem" | "luyen";

/** Số lần đúng liên tiếp để xong một nhiệm vụ luyện đọc. */
export const DAT_LIEN_TIEP = 5;

export const segBtn = (on: boolean) =>
  `min-h-11 flex-1 rounded-lg px-2 text-sm font-medium transition active:scale-[0.98] ${
    on ? "bg-primary text-white" : "border border-line-strong bg-panel text-ink hover:bg-primary-soft"
  }`;

export const phuBtn =
  "min-h-11 min-w-11 rounded-lg border border-line-strong bg-panel px-3 text-sm font-medium text-ink transition hover:bg-primary-soft active:scale-[0.98] disabled:opacity-40";

export function ChonCheDo({ value, onChange }: { value: CheDo; onChange: (v: CheDo) => void }) {
  return (
    <div className="flex gap-2" role="tablist" aria-label="Chế độ">
      <button type="button" role="tab" aria-selected={value === "xem"} className={segBtn(value === "xem")} onClick={() => onChange("xem")}>
        Xem cách đọc
      </button>
      <button
        type="button"
        role="tab"
        aria-selected={value === "luyen"}
        className={segBtn(value === "luyen")}
        onClick={() => onChange("luyen")}
      >
        Luyện đọc
      </button>
    </div>
  );
}

/** Hàng nút chọn một trong vài giá trị (thang đo, độ chính xác…), ≤ 4 nút (N2). */
export function HangChon<T extends string | number>({
  label,
  items,
  value,
  onChange,
}: {
  label: string;
  items: { value: T; text: string }[];
  value: T;
  onChange: (v: T) => void;
}) {
  return (
    <div className="flex items-center gap-2">
      <span className="shrink-0 text-sm text-muted">{label}</span>
      <div className="flex flex-1 gap-2">
        {items.map((it) => (
          <button key={String(it.value)} type="button" className={segBtn(it.value === value)} onClick={() => onChange(it.value)}>
            {it.text}
          </button>
        ))}
      </div>
    </div>
  );
}

/* ---------------- Số kiểu Việt ---------------- */

/** "12,34", "12.34", " 12,34 mm " → {value: 12.34, decimals: 2}. Chuỗi lạ → null. */
export function docSo(raw: string): { value: number; decimals: number } | null {
  const s = raw
    .trim()
    .replace(/\s+/g, "")
    .replace(/[a-zA-ZΩµμ]+$/u, "")
    .replace("−", "-")
    .replace(",", ".");
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const dot = s.indexOf(".");
  return { value: Number(s), decimals: dot < 0 ? 0 : s.length - dot - 1 };
}

/** Số nguyên đơn vị nhỏ (ví dụ phần trăm mm) → chuỗi dấu phẩy với đúng `decimals` chữ số: (1234, 2) → "12,34". */
export function soNguyenRaChuoi(units: number, decimals: number): string {
  const neg = units < 0;
  const s = String(Math.abs(units)).padStart(decimals + 1, "0");
  const body = decimals === 0 ? s : `${s.slice(0, s.length - decimals)},${s.slice(s.length - decimals)}`;
  return (neg ? "−" : "") + body;
}

/* ---------------- Tiến độ localStorage ---------------- */

export type TienDo = { streak: number; done: boolean };

/** Tiến độ luyện đọc theo từng nhiệm vụ (khoá con, ví dụ "0.02"). Đọc sau khi mount để không lệch SSR. */
export function useTienDo(storageKey: string) {
  const [data, setData] = useState<Record<string, TienDo>>({});

  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(storageKey);
      if (raw) setData(JSON.parse(raw) as Record<string, TienDo>);
    } catch {
      /* private mode / bị chặn: chạy không lưu */
    }
  }, [storageKey]);

  const ghi = useCallback(
    (nhiemVu: string, dung: boolean) => {
      setData((prev) => {
        const cu = prev[nhiemVu] ?? { streak: 0, done: false };
        const streak = dung ? cu.streak + 1 : 0;
        const next = { ...prev, [nhiemVu]: { streak, done: cu.done || streak >= DAT_LIEN_TIEP } };
        try {
          window.localStorage.setItem(storageKey, JSON.stringify(next));
        } catch {
          /* bỏ qua */
        }
        return next;
      });
    },
    [storageKey],
  );

  return { tienDo: data, ghi };
}

/* ---------------- Ô Luyện đọc ---------------- */

export type KetQuaCham = {
  /** dung: đúng cả giá trị lẫn cách ghi; chu-so: đúng giá trị, ghi sai số chữ số (không tính); sai. */
  loai: "dung" | "chu-so" | "sai";
  /** Câu chỉ chỗ sai / xác nhận (L4). */
  loi: string;
};

export function LuyenDoc({
  cauKey,
  donVi,
  nhan,
  cham,
  onDaCham,
  onCauMoi,
  tienDo,
  tenNhiemVu,
}: {
  /** Đổi khi có câu mới → xoá ô nhập. */
  cauKey: string;
  donVi: string;
  nhan: ReactNode;
  cham: (raw: string) => KetQuaCham | null;
  onDaCham: (kq: KetQuaCham) => void;
  onCauMoi: () => void;
  tienDo: TienDo | undefined;
  tenNhiemVu: string;
}) {
  const [raw, setRaw] = useState("");
  const [kq, setKq] = useState<KetQuaCham | null>(null);
  const [loiNhap, setLoiNhap] = useState(false);

  useEffect(() => {
    setRaw("");
    setKq(null);
    setLoiNhap(false);
  }, [cauKey]);

  const kiemTra = () => {
    if (kq) return;
    const r = cham(raw);
    if (!r) {
      setLoiNhap(true);
      return;
    }
    setLoiNhap(false);
    setKq(r);
    onDaCham(r);
  };

  const streak = tienDo?.streak ?? 0;
  return (
    <div className="rounded-xl border border-line bg-surface-2 p-3">
      <label className="block text-base text-ink" htmlFor={`o-${cauKey}`}>
        {nhan}
      </label>
      <div className="mt-2 flex gap-2">
        <div className="flex min-w-0 flex-1 items-center rounded-lg border border-line-strong bg-panel pr-3 focus-within:ring-2 focus-within:ring-primary">
          <input
            id={`o-${cauKey}`}
            inputMode="decimal"
            autoComplete="off"
            value={raw}
            disabled={!!kq}
            onChange={(e) => setRaw(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && kiemTra()}
            placeholder="ví dụ 12,34"
            className="min-h-11 w-full min-w-0 rounded-lg bg-transparent px-3 text-base text-ink outline-none placeholder:text-slate-500"
          />
          <span className="shrink-0 text-base text-muted">{donVi}</span>
        </div>
        {kq ? (
          <button type="button" className="min-h-11 rounded-lg bg-primary px-4 text-sm font-semibold text-white" onClick={onCauMoi}>
            Câu khác
          </button>
        ) : (
          <button type="button" className="min-h-11 rounded-lg bg-primary px-4 text-sm font-semibold text-white" onClick={kiemTra}>
            Kiểm tra
          </button>
        )}
      </div>
      {loiNhap && <p className="mt-2 text-sm text-warn">Gõ một số, ví dụ 12,34 (dấu phẩy hay dấu chấm đều được).</p>}
      {kq && (
        <p className="mt-2 text-base leading-relaxed text-ink" aria-live="polite">
          <span className={kq.loai === "dung" ? "font-semibold text-ok" : kq.loai === "chu-so" ? "font-semibold text-warn" : "font-semibold text-danger"}>
            {kq.loai === "dung" ? "✓ Đúng." : kq.loai === "chu-so" ? "≈ Đúng giá trị." : "✗ Chưa đúng."}
          </span>{" "}
          {kq.loi}
        </p>
      )}
      <p className="mt-2 text-sm text-muted">
        {tienDo?.done ? (
          <span className="font-semibold text-ok">✓ Đã xong nhiệm vụ {tenNhiemVu}.</span>
        ) : (
          <>
            Đúng liên tiếp {Math.min(streak, DAT_LIEN_TIEP)}/{DAT_LIEN_TIEP} lần là xong nhiệm vụ {tenNhiemVu}.
          </>
        )}
      </p>
    </div>
  );
}
