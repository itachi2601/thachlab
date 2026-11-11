"use client";

/**
 * Sơ đồ tư duy tổng hợp một chương (mẫu 11/11/2026 — Vật lí 12, Chương 3).
 *
 * Vì sao hình dạng thế này (docs/QUY-TAC-THIET-KE.md):
 *  - G1/N2: 1 tâm + 5 nhánh, mỗi nhánh ≤ 4 ý con; chỉ MỘT nhánh mở tại một thời điểm (N5 — người học tự bấm).
 *  - Mã hoá kép (Paivio 1986; Mayer – multimedia): mỗi nhánh một hình khoá + một câu chốt + một công thức lõi (H1, H3, N8).
 *  - Nhánh đánh số theo thứ tự học và có câu "vì sao nối tiếp" → chương là MỘT mạch truyện, không phải 8 bài rời (B8).
 *  - L1 (testing effect): nút "Tự kiểm" che mọi công thức, em nhớ lại rồi chạm để lật.
 *  - D1/D2: điện thoại là thân cây dọc (không thu nhỏ sơ đồ toả tròn — chữ sẽ < 13px); màn ≥ 1024px mới toả tròn.
 *  - V5/B4: mô phỏng PhET chỉ nạp khi bấm; không có gì tự chuyển động.
 *  - CỐ Ý vượt M3: mỗi nhánh một màu. Lý do: màu ở đây là mã ghi nhớ của nhánh (N7 signaling), chỉ nằm ở nét nhánh + số
 *    thứ tự, không dùng cho chữ; M4 vẫn giữ vì nhánh còn phân biệt bằng số + hình.
 */

import { useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import HinhNhanh from "@/components/lessons/so-do/HinhNhanh";
import type { SoDoChuong, SoDoNhanh } from "@/features/lessons/so-do-tu-duy/types";
import s from "./SoDoTuDuy.module.css";

const MAU = [s.c1, s.c2, s.c3, s.c4, s.c5];
/** vị trí nút trên sơ đồ toả tròn (% khung), đọc theo chiều kim đồng hồ từ đỉnh — theo số nhánh (3, 4 hoặc 5) */
const VI_TRI_THEO_SO: Record<number, { x: number; y: number }[]> = {
  3: [
    { x: 50, y: 13 },
    { x: 80, y: 80 },
    { x: 20, y: 80 },
  ],
  4: [
    { x: 22, y: 20 },
    { x: 78, y: 20 },
    { x: 78, y: 84 },
    { x: 22, y: 84 },
  ],
  5: [
    { x: 50, y: 13 },
    { x: 84, y: 39 },
    { x: 73, y: 86 },
    { x: 27, y: 86 },
    { x: 16, y: 39 },
  ],
};

function CongThuc({
  tex,
  che,
  lat,
  onLat,
  block,
}: {
  tex: string;
  che: boolean;
  lat: boolean;
  onLat: () => void;
  block?: boolean;
}) {
  if (che && !lat)
    return (
      <span
        role="button"
        tabIndex={0}
        className={s.che}
        onClick={(e) => {
          e.stopPropagation();
          onLat();
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            e.stopPropagation();
            onLat();
          }
        }}
      >
        Nhớ lại · chạm để lật
      </span>
    );
  return <ContentHtml className={`${s.ct} ${block ? "" : "inline-block"}`} html={`$${tex}$`} />;
}

function MoPhong({ nhanh }: { nhanh: SoDoNhanh }) {
  const [chay, setChay] = useState(false);
  const mp = nhanh.moPhong;
  if (!mp) return null;
  return (
    <div className="mt-4 rounded-xl bg-surface-2 p-3">
      <p className="text-sm font-semibold text-muted">{mp.ten}</p>
      <ContentHtml className={`${s.dong} mt-1 text-base leading-relaxed text-ink`} html={mp.nhiemVu} />
      {mp.kieu === "phet" ? (
        chay ? (
          <div className="mt-3">
            <iframe
              src={mp.src}
              title={mp.ten}
              allowFullScreen
              className="block aspect-[4/3] w-full rounded-lg border border-line bg-white"
            />
            <p className="mt-2 text-sm text-muted">
              Mô phỏng PhET, Đại học Colorado Boulder — CC BY 4.0.{" "}
              <a href={mp.src} target="_blank" rel="noreferrer" className="font-semibold text-primary underline">
                Mở toàn màn hình
              </a>
            </p>
          </div>
        ) : (
          <button
            type="button"
            onClick={() => setChay(true)}
            className="mt-3 inline-flex min-h-11 items-center rounded-xl bg-primary px-5 text-base font-semibold text-white"
          >
            ▶ Thử mô phỏng
          </button>
        )
      ) : (
        <a
          href={mp.href}
          target="_blank"
          rel="noreferrer"
          className="mt-3 inline-flex min-h-11 items-center rounded-xl bg-primary px-5 text-base font-semibold text-white"
        >
          ▶ Mở trong bài học
        </a>
      )}
    </div>
  );
}

function ChiTiet({
  nhanh,
  che,
  lat,
  onLat,
}: {
  nhanh: SoDoNhanh;
  che: boolean;
  lat: Set<string>;
  onLat: (k: string) => void;
}) {
  return (
    <div>
      <ul className="space-y-3">
        {nhanh.yCon.map((y, i) => {
          const k = `${nhanh.id}:${i}`;
          return (
            <li key={k} className="border-l-2 pl-3" style={{ borderColor: "var(--nh)" }}>
              <p className="text-base font-bold text-ink">{y.tu}</p>
              <ContentHtml className={`${s.dong} text-base leading-relaxed text-ink`} html={y.y} />
              {y.ct ? (
                <div className="mt-1.5">
                  <CongThuc tex={y.ct} che={che} lat={lat.has(k)} onLat={() => onLat(k)} />
                </div>
              ) : null}
            </li>
          );
        })}
      </ul>
      <div className="mt-4 flex gap-2 rounded-xl border border-line p-3">
        <span aria-hidden className="text-base">
          ⚠️
        </span>
        <div>
          <p className="text-sm font-semibold text-muted">Bẫy hay sập</p>
          <ContentHtml className={`${s.dong} text-base leading-relaxed text-ink`} html={nhanh.bay} />
        </div>
      </div>
      <MoPhong key={nhanh.id} nhanh={nhanh} />
      <p className="mt-4 flex flex-wrap gap-x-4 gap-y-1 text-base">
        {nhanh.bai.map((b) => (
          <a key={b.id} href={`/lop-hoc/bai/?id=${b.id}`} className="inline-flex min-h-11 items-center font-semibold text-primary underline">
            Bài {b.so}. {b.ten}
          </a>
        ))}
      </p>
    </div>
  );
}

export default function SoDoTuDuy({ data }: { data: SoDoChuong }) {
  const [mo, setMo] = useState<string | null>(null);
  const [che, setChe] = useState(false);
  const [lat, setLat] = useState<Set<string>>(new Set());
  const onLat = (k: string) => setLat((p) => new Set(p).add(k));
  const doiChe = () => {
    setChe((c) => !c);
    setLat(new Set());
  };
  const dangMo = data.nhanh.find((n) => n.id === mo) ?? null;
  const iMo = dangMo ? data.nhanh.indexOf(dangMo) : -1;
  const VI_TRI = VI_TRI_THEO_SO[data.nhanh.length] ?? VI_TRI_THEO_SO[5];

  return (
    <section className="mx-auto w-full max-w-6xl px-4 pb-16 pt-4 text-ink">
      <header className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2">
        <div>
          <p className="text-sm font-semibold text-muted">{data.lop} · Sơ đồ tư duy</p>
          <h1 className="text-xl font-bold leading-tight lg:text-2xl">{data.chuong}</h1>
        </div>
        <button
          type="button"
          onClick={doiChe}
          aria-pressed={che}
          className={`inline-flex min-h-11 items-center rounded-xl border px-4 text-base font-semibold ${
            che ? "border-primary bg-primary-soft text-primary" : "border-line-strong bg-panel text-ink"
          }`}
        >
          {che ? "Đang tự kiểm · hiện lại" : "Tự kiểm: che công thức"}
        </button>
      </header>

      {/* ---------- Điện thoại / máy tính bảng: thân cây dọc ---------- */}
      <div className="mt-4 lg:hidden">
        <div className="rounded-2xl bg-ink px-4 py-3 text-panel">
          <p className="text-lg font-bold">{data.tam}</p>
          <p className="text-base leading-snug opacity-90">{data.mach}</p>
        </div>
        <ol className={`${s.than} mt-0 list-none pt-4`}>
          {data.nhanh.map((n, i) => {
            const open = mo === n.id;
            return (
              <li key={n.id} className={MAU[i]}>
                {n.noiTiep ? <p className={s.noi}>↓ {n.noiTiep}</p> : null}
                <div className={`${s.nut} rounded-2xl bg-panel shadow-sm`}>
                  <button
                    type="button"
                    aria-expanded={open}
                    onClick={() => setMo(open ? null : n.id)}
                    className="flex w-full items-center gap-3 rounded-2xl p-3 text-left"
                  >
                    <HinhNhanh hinh={n.hinh} className="h-[75px] w-28 flex-none" />
                    <span className="min-w-0 flex-1">
                      <span className="flex items-center gap-2">
                        <span className={s.so}>{i + 1}</span>
                        <span className="text-[17px] font-bold leading-tight">{n.ten}</span>
                      </span>
                      <span className="mt-1 block text-[15px] leading-snug text-muted">{n.chot}</span>
                    </span>
                    <span aria-hidden className="flex-none text-lg text-muted">
                      {open ? "−" : "+"}
                    </span>
                  </button>
                  <div className="flex justify-center px-3 pb-3">
                    <CongThuc tex={n.ct} che={che} lat={lat.has(n.id)} onLat={() => onLat(n.id)} />
                  </div>
                  {open ? (
                    <div className="border-t border-line p-3">
                      <ChiTiet nhanh={n} che={che} lat={lat} onLat={onLat} />
                    </div>
                  ) : null}
                </div>
              </li>
            );
          })}
        </ol>
      </div>

      {/* ---------- Màn rộng: sơ đồ toả tròn + bảng chi tiết ---------- */}
      <div className="mt-4 hidden gap-6 lg:grid lg:grid-cols-[minmax(0,1.5fr)_minmax(320px,1fr)]">
        <div className={`${s.banDo} mt-4`}>
          <svg className={s.day} viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden>
            {VI_TRI.map((p, i) => {
              const q = VI_TRI[(i + 1) % VI_TRI.length];
              return (
                <g key={i} className={MAU[i]}>
                  <path
                    className={s.nhanhDay}
                    d={`M50 50 Q ${50 + (p.x - 50) * 0.35 + (p.y - 50) * 0.18} ${50 + (p.y - 50) * 0.35 - (p.x - 50) * 0.18} ${p.x} ${p.y}`}
                  />
                  {i < VI_TRI.length - 1 ? <path className={s.mach} d={`M${p.x} ${p.y} L${q.x} ${q.y}`} /> : null}
                </g>
              );
            })}
          </svg>
          <div className={s.tam}>
            <span className="text-xl font-bold">{data.tam}</span>
            <span className="px-3 text-[13px] opacity-90">Chạm một nhánh để mở</span>
          </div>
          {data.nhanh.map((n, i) => (
            <button
              key={n.id}
              type="button"
              aria-pressed={mo === n.id}
              onClick={() => setMo(n.id)}
              className={`${s.la} ${MAU[i]}`}
              style={{ left: `${VI_TRI[i].x}%`, top: `${VI_TRI[i].y}%` }}
            >
              <HinhNhanh hinh={n.hinh} className="mx-auto h-[75px] w-28" />
              <span className="mt-1 flex items-center justify-center gap-2">
                <span className={s.so}>{i + 1}</span>
                <span className="text-base font-bold leading-tight">{n.ten}</span>
              </span>
              <span className="mt-1.5 flex justify-center">
                <CongThuc tex={n.ct} che={che} lat={lat.has(n.id)} onLat={() => onLat(n.id)} />
              </span>
            </button>
          ))}
        </div>

        <aside className={`sticky top-4 self-start rounded-2xl bg-panel p-5 shadow-sm ${iMo >= 0 ? MAU[iMo] : ""}`}>
          {dangMo ? (
            <>
              <div className="flex items-center gap-2">
                <span className={s.so}>{iMo + 1}</span>
                <h2 className="text-xl font-bold">{dangMo.ten}</h2>
              </div>
              <p className="mt-1 text-base text-muted">{dangMo.noiTiep ?? dangMo.chot}</p>
              <div className="mt-4">
                <ChiTiet nhanh={dangMo} che={che} lat={lat} onLat={onLat} />
              </div>
            </>
          ) : (
            <>
              <h2 className="text-lg font-bold">Cả chương trong một mạch</h2>
              <p className="mt-1 text-base leading-relaxed">{data.mach}</p>
              <ol className="mt-3 list-none space-y-2.5">
                {data.nhanh.map((n, i) => (
                  <li key={n.id} className={`flex gap-2.5 ${MAU[i]}`}>
                    <span className={s.so}>{i + 1}</span>
                    <span className="text-base leading-snug">
                      <b>{n.ten}.</b> {n.noiTiep ?? n.chot}
                    </span>
                  </li>
                ))}
              </ol>
            </>
          )}
        </aside>
      </div>
    </section>
  );
}
