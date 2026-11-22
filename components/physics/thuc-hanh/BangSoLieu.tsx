"use client";

/**
 * components/physics/thuc-hanh/BangSoLieu.tsx — khung dùng chung của các thí nghiệm ảo Gói C
 * (docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5): bảng số liệu xếp dọc, ô học sinh tự tính được chấm,
 * trục so các khoảng kết quả, câu kiểu đề, hộp "Chưa nói được gì".
 * UI: H2 (bảng ít cột, xếp dọc ở 375 px), D2 (đích chạm 44 px), D6 (inputmode decimal), M1/M7 (token màu),
 * M4 (✓/✗ kèm chữ), C1/H4 (chữ trong hình 16 px), E1 (nhãn A. B. C. D. như đề thật).
 */

import { useId, useState, type ReactNode } from "react";
import { docSo, type KetQuaCham } from "@/components/physics/do-luong/chung";
import { vnSo } from "./cham-chung";

/* ---------------- Bảng số liệu ---------------- */

export type CotBang = { nhan: ReactNode; phu?: boolean };

/** Bảng ít cột (≤ 5) để vừa 360 px; bảng dài hơn thì tách hai bảng chồng lên nhau (H2). Ô rỗng ghi "—". */
export function BangSoLieu({
  tieuDe,
  cot,
  hang,
}: {
  tieuDe?: ReactNode;
  cot: CotBang[];
  hang: (ReactNode | undefined)[][];
}) {
  return (
    <div>
      {tieuDe && <p className="text-base font-semibold">{tieuDe}</p>}
      <table className="mt-1 w-full border-collapse text-base tabular-nums">
        <thead>
          <tr className="text-left text-sm text-muted">
            {cot.map((c, i) => (
              <th key={i} className="border-b border-line py-1 pr-2 font-medium last:pr-0">
                {c.nhan}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {hang.map((h, i) => (
            <tr key={i}>
              {h.map((o, j) => (
                <td
                  key={j}
                  className={`border-b border-line py-1.5 pr-2 last:pr-0 ${j > 0 ? "font-mono" : ""} ${cot[j]?.phu ? "text-muted" : ""}`}
                >
                  {o === undefined ? "—" : o}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/* ---------------- Ô tự tính ---------------- */

/** Ô nhập một số + chấm một lần; sai thì hiện cách tính đúng rồi cho đi tiếp. */
export function ONhapCham({
  nhan,
  donVi,
  cham,
  onXong,
  vidu,
}: {
  nhan: ReactNode;
  donVi: string;
  cham: (raw: string) => KetQuaCham | null;
  onXong: (kq: KetQuaCham, giaTri: number) => void;
  vidu: string;
}) {
  const [raw, setRaw] = useState("");
  const [kq, setKq] = useState<KetQuaCham | null>(null);
  const [loiNhap, setLoiNhap] = useState(false);
  const id = useId();
  const kiemTra = () => {
    if (kq) return;
    const r = cham(raw);
    if (!r) return setLoiNhap(true);
    setLoiNhap(false);
    setKq(r);
    onXong(r, docSo(raw)?.value ?? NaN);
  };
  return (
    <div className="rounded-xl border border-line bg-surface-2 p-3">
      <label className="block text-base text-ink" htmlFor={id}>
        {nhan}
      </label>
      <div className="mt-2 flex gap-2">
        <div className="flex min-w-0 flex-1 items-center rounded-lg border border-line-strong bg-panel pr-3 focus-within:ring-2 focus-within:ring-primary">
          <input
            id={id}
            inputMode="decimal"
            autoComplete="off"
            value={raw}
            disabled={!!kq}
            onChange={(e) => setRaw(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && kiemTra()}
            placeholder={`ví dụ ${vidu}`}
            className="min-h-11 w-full min-w-0 rounded-lg bg-transparent px-3 text-base text-ink outline-none placeholder:text-muted"
          />
          <span className="shrink-0 text-base text-muted">{donVi}</span>
        </div>
        {!kq && (
          <button
            type="button"
            className="min-h-11 rounded-lg bg-primary px-4 text-sm font-semibold text-white"
            onClick={kiemTra}
          >
            Kiểm tra
          </button>
        )}
      </div>
      {loiNhap && <p className="mt-2 text-sm text-warn">Gõ một số, ví dụ {vidu} (dấu phẩy hay dấu chấm đều được).</p>}
      {kq && (
        <p className="mt-2 text-base leading-relaxed text-ink" aria-live="polite">
          <span className={kq.loai === "dung" ? "font-semibold text-ok" : "font-semibold text-danger"}>
            {kq.loai === "dung" ? "✓ Đúng." : "✗ Chưa đúng."}
          </span>{" "}
          {kq.loi}
        </p>
      )}
    </div>
  );
}

/* ---------------- Trục so các khoảng kết quả ---------------- */

export type DoanTruc = { nhan: string; giua: number; ban: number; phu?: boolean };

/**
 * Trục số: mỗi phép đo là một đoạn giua ± ban, vạch đứng xanh lá đứt ở giá trị mốc (giá trị thật, hoặc tỉ số 1).
 * `phu`: đoạn vẽ màu cam (điều kiện có sai số hệ thống).
 */
export function TrucKhoang({
  lo,
  hi,
  vach,
  moc,
  ds,
  ghiVach,
  aria,
  chuThich,
}: {
  lo: number;
  hi: number;
  vach: number[];
  moc: number;
  ds: DoanTruc[];
  ghiVach: (v: number) => string;
  aria: string;
  chuThich: ReactNode;
}) {
  const x = (g: number) => 24 + ((Math.min(hi, Math.max(lo, g)) - lo) / (hi - lo)) * 312;
  const h = 36 + ds.length * 30;
  return (
    <figure>
      <svg viewBox={`0 0 360 ${h}`} className="block w-full text-ink" role="img" aria-label={aria}>
        <line x1={24} x2={336} y1={h - 20} y2={h - 20} stroke="currentColor" strokeWidth={1.5} />
        {vach.map((v) => (
          <g key={v}>
            <line x1={x(v)} x2={x(v)} y1={h - 25} y2={h - 15} stroke="currentColor" />
            <text x={x(v)} y={h - 1} textAnchor="middle" fontSize={16} fill="var(--color-muted)">
              {ghiVach(v)}
            </text>
          </g>
        ))}
        <line
          x1={x(moc)}
          x2={x(moc)}
          y1={6}
          y2={h - 20}
          stroke="var(--color-ok)"
          strokeWidth={2}
          strokeDasharray="4 3"
        />
        {ds.map((d, i) => {
          const y = 22 + i * 30;
          const mau = d.phu ? "var(--color-warn)" : "var(--color-primary)";
          return (
            <g key={i}>
              <line
                x1={x(d.giua - d.ban)}
                x2={x(d.giua + d.ban)}
                y1={y}
                y2={y}
                stroke={mau}
                strokeWidth={5}
                strokeLinecap="round"
              />
              <circle cx={x(d.giua)} cy={y} r={5} fill={mau} />
              <text x={Math.max(x(d.giua - d.ban) - 6, 30)} textAnchor="end" y={y + 5} fontSize={16} fill={mau}>
                {d.nhan}
              </text>
            </g>
          );
        })}
      </svg>
      <figcaption className="mt-1 text-sm text-muted">{chuThich}</figcaption>
    </figure>
  );
}

/* ---------------- Câu kiểu đề + "Chưa nói được gì" ---------------- */

/** Câu 4 phương án kiểu đề (T9): tìm phát biểu SAI, chọn một lần, hiện vì sao từng phương án đúng/sai. */
export function CauKieuDe({ de, cac }: { de: string; cac: { text: string; dung?: boolean; why: string }[] }) {
  const [chon, setChon] = useState<number | null>(null);
  const L = ["A", "B", "C", "D"];
  return (
    <div className="rounded-xl border border-line-strong bg-panel p-3">
      <p className="text-xs font-semibold uppercase tracking-wide text-primary">Câu hỏi kiểu đề thi</p>
      <div className="exam-paper mt-1">
        <p className="exam-content text-ink">{de}</p>
        <div className="exam-content mt-2 grid gap-2">
          {cac.map((o, i) => {
            const daChon = chon !== null;
            const mau = !daChon
              ? "border-line-strong hover:bg-primary-soft"
              : o.dung
                ? "border-ok"
                : i === chon
                  ? "border-danger"
                  : "border-line opacity-80";
            return (
              <button
                key={i}
                type="button"
                disabled={daChon}
                onClick={() => setChon(i)}
                className={`flex min-h-11 w-full flex-col items-start rounded-lg border bg-panel px-3 py-2 text-left text-ink transition ${mau}`}
              >
                <span>
                  <b>{L[i]}.</b> {o.text}
                </span>
                {daChon && (
                  <span className="mt-1 font-sans text-sm text-muted">
                    <b className={o.dung ? "text-ok" : "text-muted"}>
                      {o.dung ? "✓ Đây là phát biểu sai cần tìm." : "Phát biểu đúng."}
                    </b>{" "}
                    {o.why}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>
      {chon !== null && (
        <p className="mt-2 text-base text-ink" aria-live="polite">
          {cac[chon].dung ? <b className="text-ok">✓ Đúng.</b> : <b className="text-danger">✗ Chưa đúng.</b>} Đáp án{" "}
          {L[cac.findIndex((o) => o.dung)]}.
        </p>
      )}
    </div>
  );
}

/** Hộp T5: học sinh nghĩ trước rồi mới mở. */
export function ChuaNoiDuoc({ y }: { y: ReactNode[] }) {
  return (
    <details className="rounded-xl border border-line bg-surface-2 p-3">
      <summary className="min-h-11 cursor-pointer py-2 text-base font-semibold">
        Thí nghiệm này chưa nói được gì? Nghĩ một câu rồi mở.
      </summary>
      <ul className="mt-1 list-disc space-y-1 pl-5 text-base leading-relaxed">
        {y.map((v, i) => (
          <li key={i}>{v}</li>
        ))}
      </ul>
    </details>
  );
}

export { vnSo };
