"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import { splitTheorySections } from "@/features/lessons/theory-sections";
import { getSupabase } from "@/services/supabase";
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

export type TheOn = (
  | { kieu: "lat"; muc: string; neo: string; hoi: string; dap: string; tieu_muc?: string; hinh?: string }
  | { kieu: "chon"; muc: string; neo: string; hoi?: string; html: string }
) & {
  /** 8 ký tự sha1(neo) — khoá lịch ôn (bảng on_tap_the). */
  id: string;
  /** Chỉ có ở lượt trộn nhiều bài (/lop-hoc/on-the): slug + tên bài của thẻ. */
  slug?: string;
  bai?: string;
};

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

/**
 * Thẻ quên/lơ mơ quay lại sau ĐỆM thẻ nữa trong cùng lượt, chỉ LAP_TOI_DA lần: lượt 7 thẻ quên hết dài tối đa
 * 14 thẻ (thử với 2 lần ra 19 — quá "5 phút", N5). Phần còn lại để lịch ôn ngày mai lo: giãn cách hơn nhồi.
 */
const DEM = 3;
const LAP_TOI_DA = 1;

type Lich = { the_id: string; han_on: string };

function ngayVN(iso: string) {
  const d = new Date(iso);
  return `${d.getDate()}/${d.getMonth() + 1}`;
}

export default function OnNamPhut({
  bo,
  theoryHtml,
  theoryItemId,
  onOnNgay,
  tron = false,
}: {
  bo: BoOnTap;
  /** body_html mục lý thuyết của bài — để tìm đúng đoạn cho nút "Ôn ngay". Không có thì ẩn nút. */
  theoryHtml?: string;
  theoryItemId?: number;
  /** Mở + cuộn tới đoạn lý thuyết `theory-sec-<itemId>-<n>`; có `tieuMuc` thì cuộn tiếp tới tiểu mục <h4> đó. */
  onOnNgay?: (sectionId: string, tieuMuc?: string) => void;
  /** Lượt trộn thẻ đến hạn của nhiều bài: mỗi thẻ mang slug riêng, không tra lịch theo bài. */
  tron?: boolean;
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
  // Đánh giá theo LƯỢT GẶP (pos) — một thẻ có thể gặp lại trong cùng lượt.
  const [danhGia, setDanhGia] = useState<Record<number, DanhGia>>({});
  // Đánh giá LẦN ĐẦU của mỗi thẻ (idx) — đây mới là số đo trí nhớ thật, dùng để xếp lịch.
  const [dau, setDau] = useState<Record<number, DanhGia>>({});
  const [ghi, setGhi] = useState("");
  const [weakSaved, setWeakSaved] = useState<string[]>([]);
  const [lich, setLich] = useState<Lich[] | null>(null);
  const [dangNhap, setDangNhap] = useState(false);
  const [started, setStarted] = useState(false);
  const [now] = useState(() => Date.now());
  const daLuu = useRef(false);
  const quizRef = useRef<HTMLDivElement>(null);

  /* eslint-disable react-hooks/set-state-in-effect -- đọc localStorage/lịch ôn đúng 1 lần lúc mở (không có khi SSR). */
  useEffect(() => {
    setWeakSaved(readWeak(bo.slug).filter((n) => all.some((t) => t.neo === n)));
    if (tron) return;
    let huy = false;
    void (async () => {
      const sb = getSupabase();
      const { data: ss } = await sb.auth.getSession();
      if (huy || !ss.session) return;
      setDangNhap(true);
      const { data, error } = await sb.rpc("on_tap_trang_thai", { p_slug: bo.slug });
      if (!huy && !error && Array.isArray(data)) setLich(data as Lich[]);
    })();
    return () => {
      huy = true;
    };
  }, [bo.slug, all, tron]);
  /* eslint-enable react-hooks/set-state-in-effect */

  const done = pos >= order.length;
  const idx = order[pos];
  const the = done ? null : all[idx];
  const rated = danhGia[pos];

  function ghiNhan(d: DanhGia) {
    setDanhGia((cur) => (cur[pos] ? cur : { ...cur, [pos]: d }));
    setDau((cur) => (cur[idx] ? cur : { ...cur, [idx]: d }));
    if (d !== "nho") {
      // Thẻ chưa nhớ quay lại sau vài thẻ (Duolingo: sai thì hỏi lại trong cùng buổi), kết lượt bằng lần làm lại.
      setOrder((o) => {
        const lan = o.slice(0, pos + 1).filter((i) => i === idx).length;
        if (lan > LAP_TOI_DA) return o;
        const at = Math.min(pos + 1 + DEM, o.length);
        return [...o.slice(0, at), idx, ...o.slice(at)];
      });
    }
  }

  // Thẻ chọn đáp án: chấm theo phương án em bấm (tl-ok = nhớ, tl-no = quên); phản hồi gọi tên lỗi có sẵn trong HTML.
  useEffect(() => {
    const box = quizRef.current;
    if (!box || the?.kieu !== "chon") return;
    function onChange(e: Event) {
      const input = e.target as HTMLInputElement;
      if (input.type !== "radio" || !input.id || input.name.endsWith("-conf")) return;
      const label = box!.querySelector<HTMLLabelElement>(`label[for="${CSS.escape(input.id)}"]`);
      if (!label?.classList.contains("tl-opt")) return;
      ghiNhan(label.classList.contains("tl-ok") ? "nho" : "quen");
    }
    box.addEventListener("change", onChange);
    return () => box.removeEventListener("change", onChange);
    // ghiNhan chỉ đọc pos/idx — effect chạy lại mỗi lần đổi thẻ nên luôn có bản mới.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [the, pos]);

  // Hết lượt: lưu lịch ôn (đăng nhập) + danh sách thẻ yếu trên máy (khách). Chỉ một lần mỗi lượt.
  useEffect(() => {
    if (!started || !done || daLuu.current) return;
    daLuu.current = true;
    const yeu = Object.entries(dau)
      .filter(([, d]) => d !== "nho")
      .map(([i]) => all[+i].neo);
    if (!tron) {
      saveWeak(bo.slug, yeu);
      // eslint-disable-next-line react-hooks/set-state-in-effect -- cập nhật đúng 1 lần lúc hết lượt
      setWeakSaved(yeu);
    }
    const theoBai = new Map<string, { id: string; danh_gia: DanhGia }[]>();
    for (const [i, d] of Object.entries(dau)) {
      const t = all[+i];
      const slug = t.slug ?? bo.slug;
      theoBai.set(slug, [...(theoBai.get(slug) ?? []), { id: t.id, danh_gia: d }]);
    }
    void (async () => {
      const sb = getSupabase();
      const { data: ss } = await sb.auth.getSession();
      if (!ss.session) return;
      for (const [slug, kq] of theoBai) await sb.rpc("on_tap_ghi", { p_slug: slug, p_ket_qua: kq });
      if (!tron) {
        const { data } = await sb.rpc("on_tap_trang_thai", { p_slug: bo.slug });
        if (Array.isArray(data)) setLich(data as Lich[]);
      }
    })();
  }, [started, done, dau, all, bo.slug, tron]);

  function batDau(list: number[]) {
    setOrder(list);
    setPos(0);
    setLat(false);
    setGhi("");
    setDanhGia({});
    setDau({});
    daLuu.current = false;
    setStarted(true);
  }

  function tiep() {
    setLat(false);
    setGhi("");
    setPos((p) => p + 1);
  }

  function cham(d: DanhGia) {
    ghiNhan(d);
    // Nhớ rõ thì sang thẻ sau luôn — bớt một lần bấm cho thẻ đã thuộc.
    if (d === "nho") tiep();
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

  // Màn mở đầu: hợp đồng ngắn (số thẻ, thời gian) + lựa chọn ôn thẻ đến hạn (đăng nhập) / chưa nhớ lần trước (khách).
  if (!started) {
    const daCo = new Map((lich ?? []).map((r) => [r.the_id, r.han_on]));
    const denHanIdx = lich
      ? all.map((t, i) => (daCo.has(t.id) && Date.parse(daCo.get(t.id)!) <= now ? i : -1)).filter((i) => i >= 0)
      : [];
    const weakIdx = lich ? [] : all.map((t, i) => (weakSaved.includes(t.neo) ? i : -1)).filter((i) => i >= 0);
    const uuTien = denHanIdx.length > 0 ? denHanIdx : weakIdx;
    const hanToi =
      lich && lich.length > 0 && denHanIdx.length === 0
        ? lich.map((r) => r.han_on).sort()[0]
        : null;
    return (
      <section className={styles.wrap} aria-label="Ôn 5 phút">
        <p className={styles.kicker}>{tron ? "Ôn thẻ đến hạn" : "Ôn 5 phút"}</p>
        <h2 className={styles.title}>{bo.lesson_title}</h2>
        <p className={styles.lead}>
          {all.length} thẻ · khoảng {Math.max(3, Math.round(all.length * 0.7))} phút. Mỗi thẻ: gõ vài chữ em nhớ được,
          rồi mới lật so đáp án.
        </p>
        {hanToi && <p className={styles.lead}>Bài này chưa tới hạn ôn — lần tới: {ngayVN(hanToi)}.</p>}
        <div className={styles.actions}>
          {uuTien.length > 0 && (
            <button type="button" className={styles.primary} onClick={() => batDau(uuTien)}>
              {denHanIdx.length > 0
                ? `Ôn ${denHanIdx.length} thẻ đến hạn`
                : `Ôn ${weakIdx.length} thẻ lần trước chưa nhớ`}
            </button>
          )}
          <button
            type="button"
            className={uuTien.length > 0 ? styles.ghost : styles.primary}
            onClick={() => batDau(all.map((_, i) => i))}
          >
            {uuTien.length > 0 ? "Ôn cả bài" : "Bắt đầu"}
          </button>
        </div>
      </section>
    );
  }

  if (done) {
    const daGap = Object.keys(dau).map(Number);
    const yeu = daGap.filter((i) => dau[i] !== "nho");
    const nho = daGap.length - yeu.length;
    return (
      <section className={styles.wrap} aria-label="Ôn 5 phút — kết quả">
        <p className={styles.kicker}>{tron ? "Ôn thẻ đến hạn · xong" : "Ôn 5 phút · xong"}</p>
        <h2 className={styles.title}>
          Nhớ ngay lần đầu {nho}/{daGap.length} thẻ
        </h2>
        {(dangNhap || tron) && (
          <ul className={styles.lichList}>
            <li>Thẻ chưa nhớ: gặp lại ngày mai.</li>
            <li>Thẻ nhớ rõ: giãn dần 3 → 7 → 21 ngày.</li>
          </ul>
        )}
        {yeu.length > 0 ? (
          <>
            <p className={styles.lead}>Các ý cần xem lại:</p>
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
          </>
        ) : (
          <p className={styles.lead}>Em nhớ chắc cả lượt. Lần ôn tới sẽ giãn xa hơn.</p>
        )}
      </section>
    );
  }

  const t = the!;
  const nhan = tron && t.bai ? `${t.bai} · ${mucNgan(t.muc)}` : `Ôn 5 phút · ${mucNgan(t.muc)}`;
  const lanLai = order.slice(0, pos).includes(idx);

  return (
    <section className={styles.wrap} aria-label="Ôn 5 phút">
      <div className={styles.top}>
        <p className={styles.kicker}>
          {nhan}
          {lanLai && " · gặp lại"}
        </p>
        <p className={styles.count}>
          {pos + 1}/{order.length}
        </p>
      </div>
      <div className={styles.bar} role="progressbar" aria-valuemin={0} aria-valuemax={order.length} aria-valuenow={pos}>
        <span style={{ width: `${(pos / order.length) * 100}%` }} />
      </div>

      {t.kieu === "lat" ? (
        <div className={styles.card}>
          <div key={pos} className={`${styles.flip} ${lat ? styles.flipped : ""}`}>
            <div className={`${styles.face} ${styles.front}`} inert={lat}>
              <span className={styles.tag}>Câu hỏi</span>
              {t.hinh && <ContentHtml html={t.hinh} className={styles.hinh} />}
              <ContentHtml html={t.hoi} className={styles.q} />
              <form
                className={styles.ghiForm}
                onSubmit={(e) => {
                  e.preventDefault();
                  if (ghi.trim().length >= 2) setLat(true);
                }}
              >
                <label className={styles.ghiLabel} htmlFor={`on-ghi-${pos}`}>
                  Em nhớ được gì? Gõ vài chữ khoá
                </label>
                <input
                  id={`on-ghi-${pos}`}
                  className={styles.ghiInput}
                  value={ghi}
                  onChange={(e) => setGhi(e.target.value)}
                  autoComplete="off"
                  maxLength={200}
                  enterKeyHint="done"
                />
                <div className={styles.ghiBtns}>
                  <button type="submit" className={styles.primary} disabled={ghi.trim().length < 2}>
                    Lật so đáp án
                  </button>
                  <button
                    type="button"
                    className={styles.ghost}
                    onClick={() => {
                      ghiNhan("quen");
                      setLat(true);
                    }}
                  >
                    Chưa nhớ ra
                  </button>
                </div>
              </form>
            </div>
            <div className={`${styles.face} ${styles.back}`} inert={!lat}>
              <span className={`${styles.tag} ${styles.tagBack}`}>Đáp án</span>
              <ContentHtml html={t.hoi} className={styles.qSmall} />
              {ghi.trim() && (
                <p className={styles.emGhi}>
                  <span>Em ghi:</span> {ghi.trim()}
                </p>
              )}
              <ContentHtml html={t.dap} className={styles.a} />
            </div>
          </div>
          {lat &&
            (!rated ? (
              <>
                <p className={styles.hint}>So với đáp án, em nhớ tới đâu?</p>
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
                {onNgayBtn(t)}
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
            <ContentHtml key={pos} html={t.html} />
          </div>
          {rated && (
            <div className={styles.actions}>
              {rated !== "nho" && onNgayBtn(t)}
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
