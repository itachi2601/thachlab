"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import { splitTheorySections } from "@/features/lessons/theory-sections";
import styles from "./OnNamPhut.module.css";

/**
 * "Ôn 5 phút" sau bài học (thử 25/11/2026, L11 bài 22–24) — bản thu gọn của lý thuyết để HS tự nhớ lại.
 * Dữ liệu `content/on-tap/<slug>.json` rút từ ô Chốt mục + hộp bẫy bằng `scripts/on-tap/rut-the-on.py`.
 *
 * Quy tắc (docs/QUY-TAC-THIET-KE.md): mỗi màn một thẻ, HS bấm "tiếp" (N1, N5) · nhớ lại TRƯỚC rồi mới lật
 * (L1, testing effect) · ≤ 3 nút tự chấm (N2), đích chạm ≥ 44px (D) · thẻ chưa nhớ có "Ôn ngay" trỏ đúng
 * đoạn lý thuyết (L4) · không điểm, không RP, không xếp hạng (L3) · tiến độ theo bài (L2).
 * Thẻ lật thật (mặt trước câu hỏi + hình gợi nhớ, mặt sau đáp án gạch đầu dòng): hình đi cùng chữ giúp nhớ lâu
 * hơn chữ đơn thuần (M1, mã kép); một ý một dòng (N4). prefers-reduced-motion → đổi mặt không xoay.
 * Thẻ chưa nhớ lưu trên máy (localStorage, chỉ là tiện ích của bản thử) — lần mở sau ôn riêng các thẻ đó.
 */

export type TheOn =
  | { kieu: "lat"; muc: string; neo: string; hoi: string; dap: string; tieu_muc?: string; hinh?: string }
  | { kieu: "chon"; muc: string; neo: string; hoi?: string; html: string };

export interface BoOnTap {
  slug: string;
  lesson_title: string;
  the: TheOn[];
}

type DanhGia = "nho" | "lomo" | "quen";

/** Sau khi trang đã mở + cuộn tới mục lớn (flashTheorySection, ~1 s), cuộn tiếp tới tiểu mục <h4> khớp tên. */
export function cuonToiTieuMuc(sectionId: string, tieuMuc?: string) {
  if (!tieuMuc) return;
  window.setTimeout(() => {
    const sec = document.getElementById(sectionId);
    const h4 = [...(sec?.querySelectorAll("h4") ?? [])].find((h) => h.textContent?.trim().startsWith(tieuMuc));
    h4?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 1100);
}
const STORE = "thachlab-on-tap-";

const plain = (s: string) =>
  s
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();

/** "II. Kiến thức: …" → "mục II" — nhãn ngắn trên thẻ. */
function mucNgan(muc: string) {
  const m = /^([IVX]+)\./.exec(muc);
  return m ? `mục ${m[1]}` : muc;
}

function readWeak(slug: string): string[] {
  try {
    const raw = window.localStorage.getItem(STORE + slug);
    const v = raw ? (JSON.parse(raw) as { yeu?: string[] }) : null;
    return Array.isArray(v?.yeu) ? v.yeu : [];
  } catch {
    return [];
  }
}

function saveWeak(slug: string, yeu: string[]) {
  try {
    window.localStorage.setItem(STORE + slug, JSON.stringify({ at: new Date().toISOString(), yeu }));
  } catch {}
}

export default function OnNamPhut({
  bo,
  theoryHtml,
  theoryItemId,
  onOnNgay,
}: {
  bo: BoOnTap;
  /** body_html mục lý thuyết của bài — để tìm đúng đoạn cho nút "Ôn ngay". Không có thì ẩn nút. */
  theoryHtml?: string;
  theoryItemId?: number;
  /** Mở + cuộn tới đoạn lý thuyết `theory-sec-<itemId>-<n>`; có `tieuMuc` thì cuộn tiếp tới tiểu mục <h4> đó. */
  onOnNgay?: (sectionId: string, tieuMuc?: string) => void;
}) {
  const all = bo.the;
  // neo → id đoạn lý thuyết, chia đúng như trang đọc (splitTheorySections "doc").
  const secOf = useMemo(() => {
    const map = new Map<string, string>();
    if (!theoryHtml || theoryItemId == null) return map;
    const secs = splitTheorySections(theoryHtml, theoryItemId, "doc").sections.map((s) => ({
      id: s.id,
      text: plain(s.html),
    }));
    for (const t of all) {
      const hit = t.neo ? secs.find((s) => s.text.includes(t.neo)) : undefined;
      if (hit) map.set(t.neo, hit.id);
    }
    return map;
  }, [all, theoryHtml, theoryItemId]);

  const [order, setOrder] = useState<number[]>(() => all.map((_, i) => i));
  const [pos, setPos] = useState(0);
  const [lat, setLat] = useState(false);
  const [danhGia, setDanhGia] = useState<Record<number, DanhGia>>({});
  const [weakSaved, setWeakSaved] = useState<string[]>([]);
  const [started, setStarted] = useState(false);
  const quizRef = useRef<HTMLDivElement>(null);

  /* eslint-disable react-hooks/set-state-in-effect -- đọc localStorage đúng 1 lần lúc mở (không có khi SSR). */
  useEffect(() => {
    setWeakSaved(readWeak(bo.slug).filter((n) => all.some((t) => t.neo === n)));
  }, [bo.slug, all]);
  /* eslint-enable react-hooks/set-state-in-effect */

  const done = pos >= order.length;
  const idx = order[pos];
  const the = done ? null : all[idx];
  const rated = idx != null ? danhGia[idx] : undefined;

  // Thẻ chọn đáp án: chấm theo phương án em bấm (tl-ok = nhớ, tl-no = quên); phản hồi gọi tên lỗi có sẵn trong HTML.
  useEffect(() => {
    const box = quizRef.current;
    if (!box || the?.kieu !== "chon") return;
    function onChange(e: Event) {
      const input = e.target as HTMLInputElement;
      if (input.type !== "radio" || !input.id || input.name.endsWith("-conf")) return;
      const label = box!.querySelector<HTMLLabelElement>(`label[for="${CSS.escape(input.id)}"]`);
      if (!label?.classList.contains("tl-opt")) return;
      const ok = label.classList.contains("tl-ok");
      setDanhGia((d) => (d[idx] ? d : { ...d, [idx]: ok ? "nho" : "quen" }));
    }
    box.addEventListener("change", onChange);
    return () => box.removeEventListener("change", onChange);
  }, [the, idx]);

  function batDau(list: number[]) {
    setOrder(list);
    setPos(0);
    setLat(false);
    setDanhGia({});
    setStarted(true);
  }

  function tiep() {
    setLat(false);
    const next = pos + 1;
    setPos(next);
    if (next >= order.length) {
      const yeu = order.filter((i) => danhGia[i] && danhGia[i] !== "nho").map((i) => all[i].neo);
      saveWeak(bo.slug, yeu);
      setWeakSaved(yeu);
    }
  }

  function cham(d: DanhGia) {
    setDanhGia((cur) => ({ ...cur, [idx]: d }));
    if (d === "nho") {
      // Nhớ rõ thì sang thẻ sau luôn — bớt một lần bấm cho thẻ đã thuộc.
      setLat(false);
      const next = pos + 1;
      setPos(next);
      if (next >= order.length) {
        const yeu = order.filter((i) => i !== idx && danhGia[i] && danhGia[i] !== "nho").map((i) => all[i].neo);
        saveWeak(bo.slug, yeu);
        setWeakSaved(yeu);
      }
    }
  }

  function onNgayBtn(t: TheOn) {
    const sec = secOf.get(t.neo);
    if (!sec || !onOnNgay) return null;
    return (
      <button type="button" className={styles.ghost} onClick={() => onOnNgay(sec, t.kieu === "lat" ? t.tieu_muc : undefined)}>
        📖 Ôn ngay {mucNgan(t.muc)}
      </button>
    );
  }

  // Màn mở đầu: hợp đồng ngắn (số thẻ, thời gian) + lựa chọn ôn riêng thẻ chưa nhớ lần trước.
  if (!started) {
    const weakIdx = all.map((t, i) => (weakSaved.includes(t.neo) ? i : -1)).filter((i) => i >= 0);
    return (
      <section className={styles.wrap} aria-label="Ôn 5 phút">
        <p className={styles.kicker}>Ôn 5 phút</p>
        <h2 className={styles.title}>{bo.lesson_title}</h2>
        <p className={styles.lead}>
          {all.length} thẻ · khoảng {Math.max(3, Math.round(all.length * 0.7))} phút. Mỗi thẻ: tự nhớ lại trước, rồi
          mới lật xem.
        </p>
        <div className={styles.actions}>
          {weakIdx.length > 0 && (
            <button type="button" className={styles.primary} onClick={() => batDau(weakIdx)}>
              Ôn {weakIdx.length} thẻ lần trước chưa nhớ
            </button>
          )}
          <button
            type="button"
            className={weakIdx.length > 0 ? styles.ghost : styles.primary}
            onClick={() => batDau(all.map((_, i) => i))}
          >
            {weakIdx.length > 0 ? "Ôn cả bài" : "Bắt đầu"}
          </button>
        </div>
      </section>
    );
  }

  if (done) {
    const yeu = order.filter((i) => danhGia[i] && danhGia[i] !== "nho");
    const nho = order.length - yeu.length;
    return (
      <section className={styles.wrap} aria-label="Ôn 5 phút — kết quả">
        <p className={styles.kicker}>Ôn 5 phút · xong</p>
        <h2 className={styles.title}>
          Nhớ rõ {nho}/{order.length} thẻ
        </h2>
        {yeu.length > 0 ? (
          <>
            <p className={styles.lead}>Các ý cần xem lại — lần sau mở mục này sẽ ôn riêng chúng:</p>
            <ul className={styles.weakList}>
              {yeu.map((i) => {
                const t = all[i];
                return (
                  <li key={i}>
                    <ContentHtml html={t.hoi || t.neo} className={styles.weakQ} />
                    {onNgayBtn(t)}
                  </li>
                );
              })}
            </ul>
            <div className={styles.actions}>
              <button type="button" className={styles.primary} onClick={() => batDau(yeu)}>
                Ôn lại {yeu.length} thẻ này
              </button>
            </div>
          </>
        ) : (
          <p className={styles.lead}>Bài này em nhớ chắc. Vài hôm nữa mở lại một lần để giữ lâu hơn.</p>
        )}
      </section>
    );
  }

  return (
    <section className={styles.wrap} aria-label="Ôn 5 phút">
      <div className={styles.top}>
        <p className={styles.kicker}>
          Ôn 5 phút · {mucNgan(the!.muc)}
        </p>
        <p className={styles.count}>
          {pos + 1}/{order.length}
        </p>
      </div>
      <div
        className={styles.bar}
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={order.length}
        aria-valuenow={pos}
      >
        <span style={{ width: `${(pos / order.length) * 100}%` }} />
      </div>

      {the!.kieu === "lat" ? (
        <div className={styles.card}>
          <div key={pos} className={`${styles.flip} ${lat ? styles.flipped : ""}`}>
            <div
              className={`${styles.face} ${styles.front}`}
              role="button"
              tabIndex={lat ? -1 : 0}
              inert={lat}
              aria-label="Lật thẻ xem đáp án"
              onClick={() => setLat(true)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  setLat(true);
                }
              }}
            >
              <span className={styles.tag}>Câu hỏi</span>
              {the!.hinh && <ContentHtml html={the!.hinh} className={styles.hinh} />}
              <ContentHtml html={the!.hoi} className={styles.q} />
              <span className={styles.tapHint}>Nói thành lời trước · chạm để lật ↻</span>
            </div>
            <div className={`${styles.face} ${styles.back}`} inert={!lat} onClick={() => !rated && setLat(false)}>
              <span className={`${styles.tag} ${styles.tagBack}`}>Đáp án</span>
              <ContentHtml html={the!.hoi} className={styles.qSmall} />
              <ContentHtml html={the!.dap} className={styles.a} />
            </div>
          </div>
          {lat &&
            (!rated ? (
              <>
                <p className={styles.hint}>Em nhớ tới đâu?</p>
                <div className={styles.rate}>
                  <button type="button" onClick={() => cham("nho")}>
                    😀 Nhớ rõ
                  </button>
                  <button type="button" onClick={() => cham("lomo")}>
                    🤔 Lơ mơ
                  </button>
                  <button type="button" onClick={() => cham("quen")}>
                    😶 Quên
                  </button>
                </div>
              </>
            ) : (
              <div className={styles.actions}>
                {onNgayBtn(the!)}
                <button type="button" className={styles.primary} onClick={tiep}>
                  Thẻ tiếp
                </button>
              </div>
            ))}
        </div>
      ) : (
        <div className={styles.card} ref={quizRef}>
          <div className={`${styles.face} ${styles.quiz}`}>
            <span className={styles.tag}>Chọn đáp án</span>
            <ContentHtml html={the!.html} />
          </div>
          {rated && (
            <div className={styles.actions}>
              {rated !== "nho" && onNgayBtn(the!)}
              <button type="button" className={styles.primary} onClick={tiep}>
                Thẻ tiếp
              </button>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
