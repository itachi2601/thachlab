"use client";

import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import katex from "katex";
import { ChevronLeft, ChevronRight, Maximize2, Minimize2, Presentation, RotateCcw } from "lucide-react";
import type { ChieuBai } from "@/features/lessons/btm-trinh-chieu/types";
import s from "./BtmPresenter.module.css";

/**
 * components/lessons/btm-trinh-chieu/BtmPresenter.tsx — TRÌNH CHIẾU BÀI TẬP MẪU (mẫu thử 17/11/2026).
 *
 * Bố cục như bảng thầy khi chữa bài: TRÁI cố định = tóm đề (Cho/Tìm) + hình + bảng trạng thái ①② điền dần;
 * PHẢI = lời giải theo bước. Mỗi lần bấm (→ / Space / PageDown — bút trình chiếu gửi PageDown) hiện đúng MỘT thứ:
 * câu hỏi của bước (để lớp nghĩ) rồi từng dòng giải như viết bảng. Bước đã qua thu lại thành một dòng tóm tắt.
 * Lớp 0 là đề đầy đủ chữ to để cả lớp đọc.
 */

type Nhip = { b: number; n: number } | { b: "de" } | { b: "het" };

const THEME_STORE = "thachlab-btm-chieu-theme";

function tex(html: string): string {
  return html.replace(/\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g, (_m, khoi: string | undefined, dong: string | undefined) =>
    katex.renderToString((khoi ?? dong ?? "").trim(), { displayMode: !!khoi, throwOnError: false }),
  );
}

function Tex({ html, className, as = "span" }: { html: string; className?: string; as?: "span" | "div" | "p" }) {
  const out = useMemo(() => tex(html), [html]);
  const Tag = as;
  return <Tag className={className} dangerouslySetInnerHTML={{ __html: out }} />;
}

export default function BtmPresenter({ bai, hinh }: { bai: ChieuBai; hinh: (lop: Set<string>) => ReactNode }) {
  // Dãy nhịp bấm: đề → (mỗi bước: câu hỏi, dòng 1..n) → tổng kết.
  const nhip = useMemo<Nhip[]>(() => {
    const out: Nhip[] = [{ b: "de" }];
    bai.buoc.forEach((buoc, b) => {
      for (let n = 0; n <= buoc.dong.length; n++) out.push({ b, n });
    });
    out.push({ b: "het" });
    return out;
  }, [bai]);

  const [k, setK] = useState(0);
  const [theme, setTheme] = useState<"sang" | "bang">("sang");
  const [full, setFull] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const cuoiRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    try {
      const t = localStorage.getItem(THEME_STORE);
      if (t === "bang" || t === "sang") setTheme(t);
    } catch {}
  }, []);
  const doiTheme = useCallback(() => {
    setTheme((t) => {
      const moi = t === "sang" ? "bang" : "sang";
      try {
        localStorage.setItem(THEME_STORE, moi);
      } catch {}
      return moi;
    });
  }, []);

  const hienTai = nhip[k];
  const buocHienTai = hienTai.b === "de" ? -1 : hienTai.b === "het" ? bai.buoc.length : hienTai.b;
  const dongHienTai = typeof hienTai.b === "number" ? (hienTai as { n: number }).n : 0;

  /** Dòng đã hiện của bước b (bước đã qua = hết). */
  const soDongHien = useCallback(
    (b: number) => (b < buocHienTai ? bai.buoc[b].dong.length : b === buocHienTai ? dongHienTai : 0),
    [bai, buocHienTai, dongHienTai],
  );

  // Hình + bảng cộng dồn theo các dòng đã hiện.
  const { lop, bang, moi } = useMemo(() => {
    const lop = new Set(bai.hinh_dau);
    const bang: Record<string, string> = {};
    let moi: string[] = [];
    bai.buoc.forEach((buoc, b) => {
      const hien = soDongHien(b);
      buoc.dong.slice(0, hien).forEach((d, i) => {
        d.hinh?.forEach((h) => lop.add(h));
        if (d.bang) {
          Object.assign(bang, d.bang);
          if (b === buocHienTai && i === hien - 1) moi = Object.keys(d.bang);
        }
      });
    });
    return { lop, bang, moi };
  }, [bai, soDongHien, buocHienTai]);

  const tiep = useCallback(() => setK((x) => Math.min(x + 1, nhip.length - 1)), [nhip.length]);
  const lui = useCallback(() => setK((x) => Math.max(x - 1, 0)), []);
  const nhayBuoc = useCallback((b: number) => setK(nhip.findIndex((x) => x.b === b)), [nhip]);

  const batFull = useCallback(() => {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    else rootRef.current?.requestFullscreen?.().catch(() => {});
  }, []);
  useEffect(() => {
    const f = () => setFull(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", f);
    return () => document.removeEventListener("fullscreenchange", f);
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA")) return;
      if (["ArrowRight", "PageDown", " ", "Enter"].includes(e.key)) {
        e.preventDefault();
        tiep();
      } else if (["ArrowLeft", "PageUp", "Backspace"].includes(e.key)) {
        e.preventDefault();
        lui();
      } else if (e.key === "Home") setK(0);
      else if (e.key === "End") setK(nhip.length - 1);
      else if (e.key === "f" || e.key === "F") batFull();
      else if (e.key === "b" || e.key === "B") doiTheme();
      else if (/^[1-9]$/.test(e.key) && Number(e.key) <= bai.buoc.length) nhayBuoc(Number(e.key) - 1);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [tiep, lui, batFull, doiTheme, nhayBuoc, nhip.length, bai.buoc.length]);

  // Cuộn tới dòng vừa hiện.
  useEffect(() => {
    cuoiRef.current?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }, [k]);

  const nhanTienDo =
    hienTai.b === "de"
      ? "Đọc đề"
      : hienTai.b === "het"
        ? "Tổng kết"
        : `Bước ${buocHienTai + 1}/${bai.buoc.length}${dongHienTai === 0 ? " · câu hỏi" : ` · dòng ${dongHienTai}/${bai.buoc[buocHienTai].dong.length}`}`;

  return (
    <div ref={rootRef} className={s.root} data-theme={theme}>
      <header className={s.top}>
        <div className={s.topTen}>
          <span className={s.nhan}>{bai.nhan}</span>
          <span className={s.dang}>{bai.dang}</span>
        </div>
        <div className={s.topNut}>
          <button type="button" className={s.nut} onClick={doiTheme} title="Đổi nền sáng / bảng xanh (B)">
            <Presentation size={18} aria-hidden /> {theme === "sang" ? "Bảng xanh" : "Nền sáng"}
          </button>
          <button type="button" className={s.nut} onClick={batFull} title="Toàn màn hình (F)">
            {full ? <Minimize2 size={18} aria-hidden /> : <Maximize2 size={18} aria-hidden />}
          </button>
        </div>
      </header>

      <div className={s.than}>
        {/* ── TRÁI: tóm đề — luôn trước mắt, như góc trái bảng ── */}
        <aside className={s.trai} aria-label="Tóm đề">
          <div className={s.tomDe}>
            <div className={s.choTim}>
              <span className={s.choNhan}>Cho</span>
              <ul>
                {bai.tom_de.cho.map((c) => (
                  <li key={c}>
                    <Tex html={c} />
                  </li>
                ))}
              </ul>
            </div>
            <div className={s.choTim}>
              <span className={`${s.choNhan} ${s.timNhan}`}>Tìm</span>
              <ul>
                {bai.tom_de.tim.map((c) => (
                  <li key={c}>
                    <Tex html={c} />
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className={s.hinh}>{hinh(lop)}</div>

          {bai.bang && (
            <table className={s.bang}>
              <thead>
                <tr>
                  <th />
                  {bai.bang.cot.map((c) => (
                    <th key={c.id} className={c.id === "1" ? s.c1 : s.c2}>
                      {c.nhan}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {bai.bang.hang.map((h) => (
                  <tr key={h.id}>
                    <th scope="row">
                      <Tex html={`$${h.nhan}$`} />
                      {h.don_vi && <span className={s.donVi}>({h.don_vi})</span>}
                    </th>
                    {bai.bang!.cot.map((c) => {
                      const key = `${h.id}.${c.id}`;
                      const v = bang[key];
                      const canTim = bai.bang!.can_tim?.includes(key);
                      return (
                        <td key={key} className={`${c.id === "1" ? s.c1 : s.c2} ${moi.includes(key) ? s.moi : ""}`}>
                          {v ? <Tex html={`$${v}$`} /> : canTim ? <span className={s.hoiCham}>?</span> : <span className={s.trong}>·</span>}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </aside>

        {/* ── PHẢI: lời giải theo bước ── */}
        <section className={s.phai} aria-live="polite">
          <nav className={s.ray} aria-label="Các bước">
            {bai.buoc.map((b, i) => (
              <button
                key={b.tieu_de}
                type="button"
                className={s.rayNut}
                data-trang-thai={i < buocHienTai ? "xong" : i === buocHienTai ? "dang" : "chua"}
                onClick={() => nhayBuoc(i)}
                title={`${i + 1}. ${b.tieu_de} (phím ${i + 1})`}
              >
                <span className={s.raySo}>{i < buocHienTai ? "✓" : i + 1}</span>
                <span className={s.rayTen}>{b.tieu_de}</span>
              </button>
            ))}
          </nav>

          <div className={s.cuon}>
            {hienTai.b === "de" ? (
              <div className={s.deTo}>
                <div className={s.deNhan}>Đề bài</div>
                <Tex as="p" html={bai.de_html} />
                <div ref={cuoiRef} />
              </div>
            ) : (
              <>
                {bai.buoc.map((b, i) => {
                  if (i > buocHienTai) return null;
                  if (i < buocHienTai)
                    return (
                      <button key={b.tieu_de} type="button" className={s.buocXong} onClick={() => nhayBuoc(i)}>
                        <span className={s.buocXongSo}>{i + 1}</span>
                        <span className={s.buocXongTen}>{b.tieu_de}</span>
                        <Tex className={s.buocXongKq} html={b.tom_tat} />
                      </button>
                    );
                  const hien = soDongHien(i);
                  return (
                    <article key={b.tieu_de} className={s.buoc}>
                      <h2 className={s.buocTen}>
                        <span className={s.buocSo}>{i + 1}</span>
                        {b.tieu_de}
                      </h2>
                      {b.hoi && (
                        <div className={s.hoi} data-mo={hien === 0}>
                          <span className={s.hoiNhan}>Hỏi lớp</span>
                          <Tex html={b.hoi} />
                        </div>
                      )}
                      <div className={s.dongs}>
                        {b.dong.slice(0, hien).map((d, j) => (
                          <Tex
                            key={j}
                            as="div"
                            html={d.html}
                            className={`${s.dong} ${d.kieu === "ket_qua" ? s.ketQua : ""} ${d.kieu === "ghi_chu" ? s.ghiChu : ""}`}
                          />
                        ))}
                      </div>
                      <div ref={cuoiRef} />
                    </article>
                  );
                })}
                {hienTai.b === "het" && (
                  <article className={s.tongKet}>
                    <div className={s.dapSo}>
                      <span>Đáp số</span>
                      <Tex html={bai.dap_so} />
                    </div>
                    {bai.nhan_dang && (
                      <div className={s.the}>
                        <div className={s.theNhan}>🔎 Nhận dạng</div>
                        <Tex as="p" html={bai.nhan_dang} />
                      </div>
                    )}
                    {bai.bay && (
                      <div className={`${s.the} ${s.theBay}`}>
                        <div className={s.theNhan}>⚠ Bẫy hay gặp</div>
                        <ul>
                          {bai.bay.map((x) => (
                            <li key={x}>
                              <Tex html={x} />
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    <div ref={cuoiRef} />
                  </article>
                )}
              </>
            )}
          </div>
        </section>
      </div>

      <footer className={s.day}>
        <button type="button" className={s.nut} onClick={() => setK(0)} title="Về đầu (Home)" aria-label="Về đầu">
          <RotateCcw size={18} aria-hidden />
        </button>
        <button type="button" className={s.nut} onClick={lui} disabled={k === 0} aria-label="Lùi">
          <ChevronLeft size={20} aria-hidden /> Lùi
        </button>
        <div className={s.tienDo}>
          <div className={s.tienDoChu}>{nhanTienDo}</div>
          <div className={s.thanhTienDo}>
            <div style={{ width: `${(k / (nhip.length - 1)) * 100}%` }} />
          </div>
        </div>
        <button type="button" className={`${s.nut} ${s.nutChinh}`} onClick={tiep} disabled={k === nhip.length - 1}>
          {dongHienTai === 0 && typeof hienTai.b === "number" ? "Hiện lời giải" : "Tiếp"} <ChevronRight size={20} aria-hidden />
        </button>
      </footer>
    </div>
  );
}
