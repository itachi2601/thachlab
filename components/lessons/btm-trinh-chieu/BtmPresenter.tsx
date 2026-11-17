"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { ChevronLeft, ChevronRight, Maximize2, Minimize2, Moon, RotateCcw, Sun, X } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import type { ChieuBai } from "@/features/lessons/btm-trinh-chieu/types";
import s from "./BtmPresenter.module.css";

/**
 * components/lessons/btm-trinh-chieu/BtmPresenter.tsx — TRÌNH CHIẾU BÀI TẬP MẪU (thầy duyệt mẫu 17/11/2026).
 *
 * Bố cục như bảng thầy khi chữa bài: TRÁI cố định = tóm đề (Cho/Tìm) + hình theo bước + bảng trạng thái ①② điền dần;
 * PHẢI = lời giải theo bước. Mỗi lần bấm (→ / Space / PageDown — bút trình chiếu gửi PageDown) hiện đúng MỘT thứ:
 * câu hỏi của bước (lớp nghĩ/chọn phương án) rồi từng dòng giải như viết bảng (N1, N5). Bước đã qua thu lại một dòng.
 *
 * Khung (thanh trên, thanh dưới dạng viên thuốc, nền sáng/tối, phím tắt) dùng chung lớp `.lesson-presenter` với trình
 * chiếu lý thuyết để thầy không phải học hai giao diện; nền sáng/tối nhớ chung khoá `thachlab-presenter-bg`.
 */

type Nhip = { k: "de" } | { k: "kt" } | { k: "buoc"; b: number; n: number } | { k: "het" };
type Bg = "light" | "dark";
const BG_STORE = "thachlab-presenter-bg";
const ABC = ["A", "B", "C", "D"];

function docBg(): Bg {
  try {
    return localStorage.getItem(BG_STORE) === "dark" ? "dark" : "light";
  } catch {
    return "light";
  }
}

const H = ({ html, className = "" }: { html: string; className?: string }) => <ContentHtml html={html} className={className} />;

export default function BtmPresenter({
  bais,
  start = 0,
  title,
  onClose,
}: {
  bais: ChieuBai[];
  start?: number;
  /** Tên bài học — hiện ở thanh trên. */
  title?: string;
  onClose?: () => void;
}) {
  const [d, setD] = useState(() => Math.min(Math.max(start, 0), Math.max(bais.length - 1, 0)));
  const bai = bais[d];
  const [k, setK] = useState(0);
  // Chỉ mount phía client (next/dynamic ssr:false) nên đọc nền đã nhớ ngay lúc khởi tạo được.
  const [bg, setBg] = useState<Bg>(docBg);
  const [full, setFull] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const cuoiRef = useRef<HTMLDivElement>(null);

  // Dãy nhịp bấm: đề → kiến thức → (mỗi bước: câu hỏi, dòng 1..n) → tổng kết.
  const nhip = useMemo<Nhip[]>(() => {
    const out: Nhip[] = [{ k: "de" }];
    if (bai.kien_thuc_html) out.push({ k: "kt" });
    bai.buoc.forEach((buoc, b) => {
      const coHoi = !!buoc.hoi || !!buoc.lua_chon?.length || !buoc.dong.length;
      for (let n = coHoi ? 0 : 1; n <= buoc.dong.length; n++) out.push({ k: "buoc", b, n });
    });
    out.push({ k: "het" });
    return out;
  }, [bai]);

  const hienTai = nhip[Math.min(k, nhip.length - 1)];
  const buocHienTai = hienTai.k === "buoc" ? hienTai.b : hienTai.k === "het" ? bai.buoc.length : -1;
  const dongHienTai = hienTai.k === "buoc" ? hienTai.n : 0;
  const soDongHien = useCallback(
    (b: number) => (b < buocHienTai ? bai.buoc[b].dong.length : b === buocHienTai ? dongHienTai : 0),
    [bai, buocHienTai, dongHienTai],
  );
  /** Số bước đã giải xong (lớp hình của cong_cu — đúng như GiaiCungHinh: hình của bước chỉ vẽ khi bước xong). */
  const daXong = buocHienTai < 0 ? 0 : buocHienTai >= bai.buoc.length ? bai.buoc.length : buocHienTai + (dongHienTai >= bai.buoc[buocHienTai].dong.length ? 1 : 0);

  // Lớp hình tự đặt tên + bảng trạng thái, cộng dồn theo các dòng đã hiện.
  const { lop, bang, moi } = useMemo(() => {
    const lop = new Set(bai.hinh_dau ?? []);
    const bang: Record<string, string> = {};
    let moi: string[] = [];
    bai.buoc.forEach((buoc, b) => {
      const hien = soDongHien(b);
      buoc.dong.slice(0, hien).forEach((dd, i) => {
        dd.hinh?.forEach((h) => lop.add(h));
        if (dd.bang) {
          Object.assign(bang, dd.bang);
          if (b === buocHienTai && i === hien - 1) moi = Object.keys(dd.bang);
        }
      });
    });
    return { lop, bang, moi };
  }, [bai, soDongHien, buocHienTai]);

  const tiep = useCallback(() => setK((x) => Math.min(x + 1, nhip.length - 1)), [nhip.length]);
  const lui = useCallback(() => setK((x) => Math.max(x - 1, 0)), []);
  const nhayBuoc = useCallback((b: number) => setK(Math.max(0, nhip.findIndex((x) => x.k === "buoc" && x.b === b))), [nhip]);
  const doiDang = useCallback(
    (delta: number) => {
      setD((x) => {
        const y = Math.min(Math.max(x + delta, 0), bais.length - 1);
        if (y !== x) setK(0);
        return y;
      });
    },
    [bais.length],
  );
  const doiBg = useCallback(() => {
    setBg((t) => {
      const moiBg = t === "light" ? "dark" : "light";
      try {
        localStorage.setItem(BG_STORE, moiBg);
      } catch {}
      return moiBg;
    });
  }, []);
  const batFull = useCallback(() => {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    else rootRef.current?.requestFullscreen?.().catch(() => {});
  }, []);
  const thoat = useCallback(() => {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    onClose?.();
  }, [onClose]);

  useEffect(() => {
    const f = () => setFull(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", f);
    // khoá cuộn trang bài học phía sau lớp phủ
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("fullscreenchange", f);
      document.body.style.overflow = prev;
    };
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
      if (["ArrowRight", "ArrowDown", "PageDown", " ", "Enter"].includes(e.key)) {
        e.preventDefault();
        tiep();
      } else if (["ArrowLeft", "ArrowUp", "PageUp", "Backspace"].includes(e.key)) {
        e.preventDefault();
        lui();
      } else if (e.key === "Home") setK(0);
      else if (e.key === "End") setK(nhip.length - 1);
      else if (e.key === "]") doiDang(1);
      else if (e.key === "[") doiDang(-1);
      else if (e.key === "f" || e.key === "F") batFull();
      else if (e.key === "b" || e.key === "B") doiBg();
      else if (e.key === "Escape" && !document.fullscreenElement) thoat();
      else if (/^[1-9]$/.test(e.key) && Number(e.key) <= bai.buoc.length) nhayBuoc(Number(e.key) - 1);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [tiep, lui, batFull, doiBg, thoat, doiDang, nhayBuoc, nhip.length, bai.buoc.length]);

  // Cuộn tới dòng vừa hiện (chỉ trong cột phải — cột tối thiểu 0 nên không kéo lệch khung).
  useEffect(() => {
    cuoiRef.current?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }, [k, d]);

  const nhanTienDo =
    hienTai.k === "de"
      ? "Đọc đề"
      : hienTai.k === "kt"
        ? "Gọi lại kiến thức"
        : hienTai.k === "het"
          ? "Tổng kết"
          : `Bước ${buocHienTai + 1}/${bai.buoc.length}${dongHienTai === 0 ? " · hỏi lớp" : ` · dòng ${dongHienTai}/${bai.buoc[buocHienTai].dong.length}`}`;
  const nutTiep = hienTai.k === "buoc" && dongHienTai === 0 ? "Hiện lời giải" : hienTai.k === "de" ? "Bắt đầu giải" : "Tiếp";

  return (
    <div ref={rootRef} className={`lesson-presenter is-chrome ${s.root}`} data-bg={bg} role="dialog" aria-label="Trình chiếu bài tập mẫu">
      <header className="presenter-top">
        <div className="presenter-info">
          <strong>
            {bai.nhan}
            {bai.dang ? ` · ${bai.dang}` : ""}
          </strong>
          <span>
            {title ? `${title} · ` : ""}
            {bais.length > 1 ? `Dạng ${d + 1}/${bais.length} · ` : ""}
            {nhanTienDo}
          </span>
        </div>
        <div className="presenter-actions">
          {bais.length > 1 && (
            <>
              <button type="button" onClick={() => doiDang(-1)} disabled={d === 0} title="Dạng trước ([)">
                <ChevronLeft size={16} aria-hidden />
                <span className="presenter-btn-text">Dạng trước</span>
              </button>
              <button type="button" onClick={() => doiDang(1)} disabled={d === bais.length - 1} title="Dạng sau (])">
                <span className="presenter-btn-text">Dạng sau</span>
                <ChevronRight size={16} aria-hidden />
              </button>
            </>
          )}
          <button type="button" onClick={doiBg} title="Đổi nền sáng / tối (B)">
            {bg === "light" ? <Sun size={16} aria-hidden /> : <Moon size={16} aria-hidden />}
            <span className="presenter-btn-text">{bg === "light" ? "Nền sáng" : "Nền tối"}</span>
          </button>
          <button type="button" onClick={batFull} title="Toàn màn hình (F)">
            {full ? <Minimize2 size={16} aria-hidden /> : <Maximize2 size={16} aria-hidden />}
            <span className="presenter-btn-text">{full ? "Thu nhỏ" : "Toàn màn hình"}</span>
          </button>
          {onClose && (
            <button type="button" className="presenter-close" onClick={thoat} title="Thoát trình chiếu (Esc)">
              <X size={16} aria-hidden />
              <span className="presenter-btn-text">Thoát</span>
            </button>
          )}
        </div>
      </header>

      <div className={s.than} key={d}>
        {/* ── TRÁI: tóm đề — luôn trước mắt, như góc trái bảng ── */}
        <aside className={s.trai} aria-label="Tóm đề">
          {bai.tom_de ? (
            <div className={s.tomDe}>
              <div className={s.choTim}>
                <span className={s.choNhan}>Cho</span>
                <ul>
                  {bai.tom_de.cho.map((c) => (
                    <li key={c}>
                      <H html={c} className="inline" />
                    </li>
                  ))}
                </ul>
              </div>
              <div className={s.choTim}>
                <span className={`${s.choNhan} ${s.timNhan}`}>Tìm</span>
                <ul>
                  {bai.tom_de.tim.map((c) => (
                    <li key={c}>
                      <H html={c} className="inline" />
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            hienTai.k !== "de" && <H html={bai.de_html} className={`block ${s.deNho}`} />
          )}

          {bai.hinh && <div className={s.hinh}>{bai.hinh({ layer: daXong, step: Math.max(0, Math.min(buocHienTai, bai.buoc.length - 1)), lop })}</div>}

          {bai.bang && (
            <table className={s.bang}>
              <thead>
                <tr>
                  <th />
                  {bai.bang.cot.map((c, i) => (
                    <th key={c.id} className={i === 0 ? s.c1 : s.c2}>
                      {c.nhan}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {bai.bang.hang.map((h) => (
                  <tr key={h.id}>
                    <th scope="row">
                      <H html={`$${h.nhan}$`} className="inline" />
                      {h.don_vi && <span className={s.donVi}>({h.don_vi})</span>}
                    </th>
                    {bai.bang!.cot.map((c, i) => {
                      const key = `${h.id}.${c.id}`;
                      const v = bang[key];
                      return (
                        <td key={key} className={`${i === 0 ? s.c1 : s.c2} ${moi.includes(key) ? s.moi : ""}`}>
                          {v ? (
                            <H html={`$${v}$`} className="inline" />
                          ) : bai.bang!.can_tim?.includes(key) ? (
                            <span className={s.hoiCham}>?</span>
                          ) : (
                            <span className={s.trong}>·</span>
                          )}
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
                key={i}
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
            {hienTai.k === "de" ? (
              <div className={s.deTo}>
                <p className={s.kicker}>Đề bài</p>
                {/* nhịp đọc đề: không cuộn (trên điện thoại cuộn tới cuối đề sẽ che mất đầu đề) */}
                <H html={bai.de_html} className="block" />
              </div>
            ) : (
              <>
                {bai.kien_thuc_html && (
                  hienTai.k === "kt" ? (
                    <article className={`${s.buoc} ${s.kienThuc}`}>
                      <p className={s.kicker}>Kiến thức cần gọi lại</p>
                      <H html={bai.kien_thuc_html} className="block" />
                      <div ref={cuoiRef} />
                    </article>
                  ) : (
                    <button type="button" className={s.buocXong} onClick={() => setK(1)}>
                      <span className={s.buocXongSo}>✦</span>
                      <span className={s.buocXongTen}>Kiến thức cần gọi lại</span>
                      <span />
                    </button>
                  )
                )}
                {bai.buoc.map((b, i) => {
                  if (i > buocHienTai) return null;
                  if (i < buocHienTai)
                    return (
                      <button key={i} type="button" className={s.buocXong} onClick={() => nhayBuoc(i)}>
                        <span className={s.buocXongSo}>{i + 1}</span>
                        <span className={s.buocXongTen}>{b.tieu_de}</span>
                        {b.tom_tat ? <H html={b.tom_tat} className={`inline ${s.buocXongKq}`} /> : <span />}
                      </button>
                    );
                  const hien = soDongHien(i);
                  return (
                    <article key={i} className={s.buoc}>
                      <h2 className={s.buocTen}>
                        <span className={s.buocSo}>{i + 1}</span>
                        <span>{b.tieu_de}</span>
                      </h2>
                      {(b.hoi || b.lua_chon) && (
                        <div className={s.hoi} data-mo={hien === 0}>
                          <span className={s.hoiNhan}>Hỏi lớp</span>
                          <div>
                            {b.hoi && <H html={b.hoi} className="block" />}
                            {b.lua_chon && (
                              <ol className={s.luaChon}>
                                {b.lua_chon.map((c, j) => (
                                  <li key={j} data-ket={hien === 0 ? "" : c.dung ? "dung" : "sai"}>
                                    <span className={s.abc}>{hien > 0 && c.dung ? "✓" : `${ABC[j]}.`}</span>
                                    <span>
                                      <H html={c.text} className="inline" />
                                      {hien > 0 && !c.dung && c.vi_sao && (
                                        <span className={s.viSao}>
                                          {" "}
                                          — <H html={c.vi_sao} className="inline" />
                                        </span>
                                      )}
                                    </span>
                                  </li>
                                ))}
                              </ol>
                            )}
                          </div>
                        </div>
                      )}
                      <div className={s.dongs}>
                        {b.dong.slice(0, hien).map((dd, j) => (
                          <div key={j} className={`${s.dong} ${dd.kieu ? s[dd.kieu] : ""}`}>
                            {dd.kieu === "bay" && <span className={s.bayNhan}>⚠ Lỗi hay gặp</span>}
                            <H html={dd.html} className="block" />
                          </div>
                        ))}
                      </div>
                      <div ref={cuoiRef} />
                    </article>
                  );
                })}
                {hienTai.k === "het" && (
                  <article className={s.tongKet}>
                    {bai.dap_so && (
                      <div className={s.dapSo}>
                        <span className={s.kicker}>Đáp số</span>
                        <H html={bai.dap_so} className="block" />
                      </div>
                    )}
                    {bai.nhan_dang && (
                      <div className={s.the}>
                        <p className={s.theNhan}>🔎 Nhận dạng</p>
                        <H html={bai.nhan_dang} className="block" />
                      </div>
                    )}
                    {bai.bay && (
                      <div className={`${s.the} ${s.theBay}`}>
                        <p className={s.theNhan}>⚠ Bẫy hay gặp</p>
                        <ul>
                          {bai.bay.map((x) => (
                            <li key={x}>
                              <H html={x} className="inline" />
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {d < bais.length - 1 && (
                      <button type="button" className={s.sangDang} onClick={() => doiDang(1)}>
                        Sang {bais[d + 1].nhan} <ChevronRight size={18} aria-hidden />
                      </button>
                    )}
                    <div ref={cuoiRef} />
                  </article>
                )}
              </>
            )}
          </div>
        </section>
      </div>

      <footer className="presenter-bar">
        <button type="button" onClick={() => setK(0)} title="Về đầu (Home)" aria-label="Về đầu">
          <RotateCcw size={16} aria-hidden />
        </button>
        <button type="button" onClick={lui} disabled={k === 0} title="Lùi (←)">
          <ChevronLeft size={16} aria-hidden />
          <span className="presenter-btn-text">Lùi</span>
        </button>
        <span className={s.tienDo} aria-live="polite">
          {nhanTienDo}
        </span>
        <button type="button" className={s.nutChinh} onClick={tiep} disabled={k >= nhip.length - 1} title="Tiếp (→ / Space / PageDown)">
          {nutTiep}
          <ChevronRight size={16} aria-hidden />
        </button>
      </footer>
      <div className="presenter-progress" aria-hidden>
        <span style={{ width: `${(k / Math.max(nhip.length - 1, 1)) * 100}%` }} />
      </div>
    </div>
  );
}
