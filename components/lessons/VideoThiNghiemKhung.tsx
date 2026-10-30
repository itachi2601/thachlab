"use client";

import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import { Check, Lock, Play, Target } from "lucide-react";

/**
 * Video thí nghiệm tự dựng (9:16, không lời) + khung sáu ô bên cạnh, bản thử 29/10/2026.
 *
 * - Khung sáu ô = khung hộp thí nghiệm (QUY-TAC-THI-NGHIEM-TRONG-BAI): Giả thuyết → Dự đoán → Dụng cụ & cách
 *   đo → Quan sát → Rút ra → Chưa nói được gì. Ô đang diễn ra sáng lên theo giây của video (signaling);
 *   ô chưa tới khoá lại để không lộ đáp án trước khi clip tới đoạn đó (V8: chữ và clip không nói trùng nhau).
 * - Video tự dừng một lần ở câu Dự đoán; chọn xong mới chạy tiếp (đoán trước khi học). Không điểm, không
 *   xếp hạng: chỉ phản hồi tức thì (SDT — thưởng hữu hình làm giảm động lực nội tại).
 * - Bố cục: màn rộng = video bên trái (dính), phần tương tác bên phải; điện thoại = video dính trên đầu, thu theo
 *   chiều cao màn hình, dải bước + ô hiện tại nằm dưới.
 * - Câu Dự đoán bắt buộc: chạm video hay tua qua đều bị hỏi lại; chỉ có nút "Chưa muốn đoán, xem luôn" (tự chủ, SDT).
 * - Mốc giây lấy từ engine (scripts/video-thi-nghiem, `render.py <clip> --kich-ban`), nên không phải
 *   dựng lại mp4. Dữ liệu: content/thi-nghiem/video-khung/<id>.json.
 */

export type VideoKhungO = { khoa: string; giay: number; chu: string; kiem?: string };
export type VideoKhungDuDoan = {
  giay: number;
  cau_hoi: string;
  chon: string[];
  dung: number;
  giai_thich_dung: string;
  giai_thich_sai: string;
};
export type VideoKhungData = {
  id: string;
  ten: string;
  video: string;
  poster?: string;
  tong_giay: number;
  o: VideoKhungO[];
  dung_dua: VideoKhungDuDoan;
};

/** Mốc giây → "m:ss" để em biết ô này nằm ở đâu trong clip (bấm là tua tới). */
const mmss = (g: number) => `${Math.floor(g / 60)}:${String(Math.floor(g % 60)).padStart(2, "0")}`;

const NHAN: Record<string, string> = {
  gia_thuyet: "Giả thuyết",
  du_doan: "Dự đoán",
  dung_cu: "Dụng cụ & cách đo",
  quan_sat: "Quan sát",
  rut_ra: "Rút ra",
  chua_noi: "Chưa nói được gì",
};

export type VideoKhungEvent =
  | { loai: "dung_o_du_doan" }
  | { loai: "chon"; chon: number; dung: boolean }
  | { loai: "xem_lai_o"; khoa: string }
  | { loai: "bo_qua" };

/** Câu trả lời đã chọn theo id clip, sống ngoài component: bài vẽ lại HTML (KaTeX tải xong, bấm video YouTube khác)
 *  thì khung được gắn lại và vẫn nhớ em đã đoán, không bắt dừng hỏi lần nữa. */
const TRA_LOI = new Map<string, { chose: number | null; boQua: boolean }>();

export default function VideoThiNghiemKhung({
  data,
  onEvent,
  dinh = true,
}: {
  data: VideoKhungData;
  onEvent?: (e: VideoKhungEvent) => void;
  /** Video dính trên đầu màn hình khi cuộn. Trang bài có thanh tab dính sẵn nên ContentHtml truyền false. */
  dinh?: boolean;
}) {
  const saved = TRA_LOI.get(data.id);
  const videoRef = useRef<HTMLVideoElement>(null);
  const sectionRef = useRef<HTMLElement>(null);
  const cardRef = useRef<HTMLDivElement>(null); // ô hiện tại ở điện thoại (video cao gần hết màn hình nên câu hỏi nằm dưới)
  const askingRef = useRef(false); // đồng bộ với `asking` ngay lúc gọi (onPlay chạy trước khi React kịp dựng lại)
  const askedOnce = useRef(false);
  const doneRef = useRef(!!saved && (saved.chose !== null || saved.boQua)); // đã chọn hoặc chủ động bấm "xem luôn": từ đó mới hết bắt dừng và mở Giả thuyết
  const eventRef = useRef(onEvent); // trang gọi truyền hàm mới mỗi lần dựng: giữ ở ref để vòng rAF không bị huỷ liên tục
  useEffect(() => {
    eventRef.current = onEvent;
  }, [onEvent]);
  const [t, setT] = useState(0);
  const [reachedRaw, setReached] = useState(0); // chỉ số ô xa nhất đã tới: ô sau đó còn khoá
  const KEY_XONG = `khung-xong:${data.id}`;
  const [xong, setXong] = useState(() => {
    try {
      return localStorage.getItem(KEY_XONG) === "1";
    } catch {
      return false;
    }
  }); // đã xem hết clip (sau khi trả lời Dự đoán) một lần: mở cả sáu ô để ôn lại, nhớ theo id khung
  const reached = xong ? data.o.length - 1 : reachedRaw;
  const [asking, setAskingState] = useState(false);
  const setAsking = useCallback((b: boolean) => {
    askingRef.current = b;
    setAskingState(b);
  }, []);
  const [chose, setChose] = useState<number | null>(saved?.chose ?? null);
  const [boQua, setBoQua] = useState(saved?.boQua ?? false);

  const dd = data.dung_dua;
  const duDoanIdx = data.o.findIndex((o) => o.khoa === "du_doan");

  const curOf = useCallback(
    (sec: number) => {
      let c = 0;
      data.o.forEach((o, i) => {
        if (sec >= o.giay - 0.05) c = i;
      });
      return c;
    },
    [data.o],
  );

  // Dừng ở câu Dự đoán: thoát toàn màn hình (iOS/Android che mất thẻ câu hỏi), đưa focus vào nút chọn đầu tiên.
  const hoi = useCallback(
    (v: HTMLVideoElement) => {
      v.pause();
      const w = v as HTMLVideoElement & { webkitExitFullscreen?: () => void };
      if (document.fullscreenElement) void document.exitFullscreen().catch(() => {});
      else w.webkitExitFullscreen?.();
      setAsking(true);
      if (!askedOnce.current) {
        askedOnce.current = true;
        eventRef.current?.({ loai: "dung_o_du_doan" });
      }
    },
    [setAsking],
  );

  const check = useCallback(() => {
    const v = videoRef.current;
    if (!v) return;
    const now = v.currentTime;
    setT(now);
    // chưa trả lời thì các ô sau Dự đoán vẫn khoá, dù thanh tua đã kéo qua
    setReached((r) => Math.max(r, doneRef.current ? curOf(now) : Math.min(curOf(now), duDoanIdx)));
    if (now >= dd.giay - 0.05 && !v.seeking && !v.paused && !doneRef.current) hoi(v);
    if (doneRef.current && now >= data.tong_giay - 0.5) {
      setXong(true);
      try {
        localStorage.setItem(KEY_XONG, "1");
      } catch {}
    }
  }, [curOf, dd.giay, duDoanIdx, hoi, data.tong_giay, KEY_XONG]);

  // rAF chỉ chạy khi video đang phát; lúc dừng/tua cập nhật bằng sự kiện (tab ẩn thì timeupdate vẫn bắt kịp).
  const raf = useRef(0);
  useEffect(() => () => cancelAnimationFrame(raf.current), []);

  const onPlay = () => {
    const v = videoRef.current;
    if (askingRef.current && !doneRef.current) {
      v?.pause(); // chạm vào video hay bấm play gốc cũng không bỏ qua được câu hỏi
      return;
    }
    setAsking(false);
    document.querySelectorAll("video").forEach((o) => o !== videoRef.current && o.pause()); // một video phát một lúc
    cancelAnimationFrame(raf.current);
    const loop = () => {
      check();
      raf.current = requestAnimationFrame(loop);
    };
    raf.current = requestAnimationFrame(loop);
  };
  const onStop = () => {
    cancelAnimationFrame(raf.current);
    check();
  };

  // Tua qua câu Dự đoán khi chưa trả lời: đưa về sát câu hỏi và hỏi luôn; tua về trước nó thì thôi hỏi.
  const onSeeking = () => {
    const v = videoRef.current;
    if (!v) return;
    const now = v.currentTime;
    if (!doneRef.current && now >= dd.giay - 0.05) {
      v.currentTime = dd.giay - 0.1;
      hoi(v);
      return;
    }
    if (now < dd.giay - 0.3) setAsking(false);
  };

  // Điện thoại: video dính trên đầu màn hình, câu hỏi nằm ngay dưới; chỉ kéo nhẹ nếu thẻ còn nằm ngoài tầm mắt.
  // Hộp tĩnh trong HTML bài (label, <video>, "Nhìn vào") chỉ ẩn khi khung đã mount xong, nên chunk lỗi thì video vẫn còn.
  useLayoutEffect(() => {
    const box = sectionRef.current?.closest(".tl-box--khung");
    box?.classList.add("tl-khung-on");
    return () => box?.classList.remove("tl-khung-on");
  }, []);

  useEffect(() => {
    if (!asking) return;
    const card = cardRef.current;
    if (card && card.offsetParent !== null) card.scrollIntoView({ behavior: "instant", block: "nearest" });
    const nut = [...(sectionRef.current?.querySelectorAll<HTMLButtonElement>("button[data-chon]") ?? [])].find(
      (b) => b.offsetParent !== null && !b.disabled,
    );
    nut?.focus({ preventScroll: true });
  }, [asking]);

  const seekTo = (i: number) => {
    const v = videoRef.current;
    if (!v || i > reached) return;
    v.currentTime = data.o[i].giay + 0.05;
    setAsking(false);
    eventRef.current?.({ loai: "xem_lai_o", khoa: data.o[i].khoa });
    void v.play().catch(() => {});
  };

  const choose = (i: number) => {
    if (doneRef.current) return;
    doneRef.current = true;
    setChose(i);
    TRA_LOI.set(data.id, { chose: i, boQua: false });
    eventRef.current?.({ loai: "chon", chon: i, dung: i === dd.dung });
  };

  const resume = () => {
    setAsking(false);
    void videoRef.current?.play().catch(() => {});
  };

  const boQuaCau = () => {
    if (doneRef.current) return;
    doneRef.current = true;
    setBoQua(true);
    TRA_LOI.set(data.id, { chose: null, boQua: true });
    eventRef.current?.({ loai: "bo_qua" });
    resume();
  };

  // Giả thuyết nói thẳng quan hệ cần đoán nên chưa lộ: chỉ hiện sau khi em đã chọn (hoặc bấm xem luôn);
  // trước đó hiện câu hỏi trung tính `kiem`.
  const daQuaDuDoan = chose !== null || boQua;
  const an = (o: VideoKhungO) => o.khoa === "gia_thuyet" && !!o.kiem && !daQuaDuDoan;
  const nhan = (o: VideoKhungO) => (an(o) ? "Cần kiểm tra" : NHAN[o.khoa]);
  const chu = (o: VideoKhungO) => (an(o) ? o.kiem : o.chu);

  const cur = curOf(t);
  const shown = asking ? duDoanIdx : cur;

  const body = (i: number, big: boolean) => {
    const o = data.o[i];
    if (i === duDoanIdx && asking) {
      const dung = chose === dd.dung;
      return (
        <div role="group" aria-live="polite" aria-label="Câu dự đoán">
          <p className={big ? "text-[17px] leading-relaxed text-ink" : "text-[16px] leading-relaxed text-ink"}>
            {dd.cau_hoi}
          </p>
          <div className="mt-3 grid gap-2">
            {dd.chon.map((s, k) => {
              const picked = chose === k;
              return (
                <button
                  key={s}
                  type="button"
                  data-chon
                  disabled={chose !== null}
                  onClick={() => choose(k)}
                  className={
                    "min-h-12 rounded-xl border px-4 py-2 text-left text-[16px] font-semibold transition-colors " +
                    (picked
                      ? "border-primary bg-primary-soft text-ink"
                      : "border-line-strong bg-panel text-ink hover:bg-primary-soft disabled:opacity-60")
                  }
                >
                  {s}
                </button>
              );
            })}
          </div>
          {chose === null && (
            <button
              type="button"
              onClick={boQuaCau}
              className="mt-2 min-h-11 px-1 text-[14px] text-muted underline underline-offset-2 hover:text-ink"
            >
              Chưa muốn đoán, xem luôn
            </button>
          )}
          {chose !== null && (
            <div className="mt-3 rounded-xl bg-surface-2 p-3">
              <p className="flex items-start gap-2 text-[15px] leading-relaxed text-ink">
                {dung ? (
                  <Check className="mt-0.5 size-5 shrink-0 text-ok" aria-hidden />
                ) : (
                  <Target className="mt-0.5 size-5 shrink-0 text-warn" aria-hidden />
                )}
                <span>
                  <b>{dung ? "Đúng hướng. " : "Chưa khớp. "}</b>
                  {dung ? dd.giai_thich_dung : dd.giai_thich_sai}
                </span>
              </p>
              <button
                type="button"
                onClick={resume}
                className="mt-3 inline-flex min-h-12 items-center gap-2 rounded-xl bg-primary px-5 text-[16px] font-bold text-white hover:bg-primary-dark"
              >
                <Play className="size-4" aria-hidden /> Xem tiếp
              </button>
            </div>
          )}
        </div>
      );
    }
    return (
      <p
        className={
          "whitespace-pre-line " +
          (big ? "text-[17px] leading-relaxed text-ink" : "text-[15px] leading-relaxed text-muted")
        }
      >
        {chu(o)}
        {i === duDoanIdx && chose !== null && (
          <span className="mt-1 block text-[14px] font-semibold text-ink">Em đã chọn: {dd.chon[chose]}</span>
        )}
        {i === duDoanIdx && boQua && <span className="mt-1 block text-[14px] text-muted">Em chưa đoán.</span>}
      </p>
    );
  };

  return (
    <section
      ref={sectionRef}
      aria-label={`Video thí nghiệm: ${data.ten}`}
      className="rounded-2xl border border-line bg-panel p-4 sm:p-5"
    >
      <h3 className="font-display font-bold leading-snug text-ink" style={{ margin: "0 0 16px", fontSize: 18 }}>
        {data.ten}
      </h3>
      <div className="grid gap-5 lg:grid-cols-[auto_minmax(0,1fr)] lg:items-start lg:gap-6 xl:gap-8">
        {/* Phần tương tác (câu hỏi, sáu ô): bên phải ở màn rộng cho dễ bấm, dưới video ở điện thoại */}
        <div className="order-2">
          {/* Điện thoại: dải sáu chấm + MỘT ô hiện tại */}
          <div className="lg:hidden">
            <ol className="mb-3 flex gap-1.5" aria-label="Các bước thí nghiệm">
              {data.o.map((o, i) => (
                <li key={o.khoa} className="flex-1">
                  <button
                    type="button"
                    disabled={i > reached}
                    onClick={() => seekTo(i)}
                    aria-label={i > reached ? `${NHAN[o.khoa]} (chưa mở)` : NHAN[o.khoa]}
                    aria-current={i === shown ? "step" : undefined}
                    className={
                      "flex h-11 w-full items-center justify-center rounded-lg text-[14px] font-bold " +
                      (i === shown
                        ? "bg-primary text-white"
                        : i <= reached
                          ? "bg-primary-soft text-ink"
                          : "bg-surface-2 text-muted")
                    }
                  >
                    {i <= reached ? i + 1 : <Lock className="size-4" aria-hidden />}
                  </button>
                </li>
              ))}
            </ol>
            <div ref={cardRef} className="scroll-mb-24 rounded-xl border border-line-strong bg-primary-soft p-4">
              <p className="flex items-baseline gap-2 text-[15px] font-bold text-primary" style={{ marginBottom: 6 }}>
                <span>{nhan(data.o[shown])}</span>
                <span className="text-[13px] font-semibold text-muted">
                  {shown + 1}/{data.o.length} · {mmss(data.o[shown].giay)}
                </span>
              </p>
              {body(shown, true)}
            </div>
          </div>

          {/* Màn rộng: stepper dọc — một ray nối sáu bước, chỉ bước hiện tại mở nội dung (B3 nhóm bằng ray thay viền,
              C6 nhãn chữ thường, N4 không lặp "Xem lại": mốc giây ở phải là lời mời bấm tua tới) */}
          <ol className="hidden lg:block" aria-label="Các bước thí nghiệm">
            {data.o.map((o, i) => {
              const open = i <= reached;
              const on = i === shown;
              const last = i === data.o.length - 1;
              return (
                <li
                  key={o.khoa}
                  aria-current={on ? "step" : undefined}
                  className="relative"
                  style={{
                    paddingLeft: 40,
                  }} /* .tl-khung-host li đặt padding-left: 0 trong globals.css nên không dùng pl-10 */
                >
                  {/* ray nối: đã qua = màu nhấn nhạt, chưa tới = kẻ mờ */}
                  {!last && (
                    <span
                      aria-hidden
                      className={
                        "absolute left-[13px] top-8 bottom-0 w-0.5 " + (i < reached ? "bg-primary/40" : "bg-line")
                      }
                    />
                  )}
                  <span
                    aria-hidden
                    className={
                      "absolute left-0 top-1.5 grid size-7 place-items-center rounded-full text-[13px] font-bold " +
                      (on
                        ? "bg-primary text-white"
                        : open
                          ? "bg-primary-soft text-primary"
                          : "border border-line bg-panel text-muted")
                    }
                  >
                    {on ? i + 1 : open ? <Check className="size-4" strokeWidth={2.5} /> : <Lock className="size-3.5" />}
                  </span>
                  <button
                    type="button"
                    disabled={!open}
                    onClick={() => seekTo(i)}
                    className={
                      "-ml-2 flex min-h-11 w-[calc(100%+0.5rem)] items-center gap-3 rounded-lg px-2 text-left transition-colors " +
                      (open && !on ? "hover:bg-surface-2" : "") +
                      (open ? "" : " cursor-default")
                    }
                  >
                    <span
                      className={
                        "text-[16px] " +
                        (on ? "font-bold text-primary" : open ? "font-semibold text-ink" : "font-medium text-muted")
                      }
                    >
                      {nhan(o)}
                    </span>
                    <span
                      className={"ml-auto shrink-0 text-[13px] tabular-nums " + (on ? "text-primary" : "text-muted")}
                    >
                      {open ? mmss(o.giay) : `mở ở ${mmss(o.giay)}`}
                    </span>
                  </button>
                  {/* Chỉ ô hiện tại mở nội dung: cột phải luôn thấp hơn video, không phải cuộn mất video để đọc (V13) */}
                  {on && <div className="mb-3 mt-1 rounded-xl bg-primary-soft px-4 py-3">{body(i, true)}</div>}
                  {!on && <div className="h-1" />}
                </li>
              );
            })}
          </ol>
        </div>

        <div
          className={
            "order-1 mx-auto w-full self-start lg:mx-0 " +
            // Video dọc cao theo màn hình: điện thoại ≤ 50svh để ô câu hỏi bên dưới vẫn trong tầm mắt;
            // màn rộng bề rộng cố định (cột tương tác lấy phần còn lại), dính dưới thanh tab, cao vừa khung nhìn.
            "lg:w-[min(280px,calc((100svh_-_8rem)_*_9_/_16))] lg:max-w-none xl:w-[min(340px,calc((100svh_-_8rem)_*_9_/_16))] " +
            (dinh
              ? "sticky top-2 z-10 max-w-[min(340px,calc(62svh_*_9_/_16))] lg:top-4"
              : "max-w-[min(340px,calc(50svh_*_9_/_16))] lg:sticky lg:top-24")
          }
        >
          <video
            ref={videoRef}
            src={data.video}
            poster={data.poster ?? data.video.replace(/\.mp4$/, ".webp")}
            controls
            playsInline
            preload="none"
            onPlay={onPlay}
            onPause={onStop}
            onEnded={onStop}
            onSeeking={onSeeking}
            onSeeked={check}
            onTimeUpdate={check}
            className="aspect-[9/16] w-full rounded-xl bg-black object-contain shadow-lg"
          />
        </div>
      </div>
      <p className="mt-3 text-center text-[13px] text-muted lg:text-left">
        Video dựng lại từ số liệu mẫu, không phải quay thật.
      </p>
    </section>
  );
}
