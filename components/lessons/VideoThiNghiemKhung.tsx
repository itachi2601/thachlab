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
 * - Câu chốt (tuỳ chọn, `cau_chot`): dừng lần hai ở khung THỬ NGHĨ của cảnh Chốt, cùng khối A–D với câu Dự đoán; chọn xong
 *   mới hiện đáp án + giải thích của lựa chọn đó (L1). Sự kiện `*_cau_chot` qua `onEvent`.
 * - Việc 6: mỗi lượt xem gom ở máy khách (`VideoKhungLuot`), gửi qua `onLuot` khi xem hết / ẩn tab / rời trang
 *   (KhungPortals → services/clip-views → RPC log_clip_view). Không gọi gì lúc tải trang.
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
/** Câu chốt (việc 2, thầy chốt 19/11/2026): video dừng lần hai ở khung "THỬ NGHĨ" của cảnh Chốt, trước khi clip hiện
 *  Gợi ý. Chọn A–D, chấm tự động; giải thích riêng cho TỪNG lựa chọn (L1), không điểm/xếp hạng (L3, K6).
 *  `giay` = đúng lúc dừng (câu hỏi trong clip đã hiện đủ), không trừ DUNG_SOM. Kiểm bằng `xuat-khung.py --kiem`. */
export type VideoKhungCauChot = {
  giay: number;
  cau_hoi: string;
  chon: string[]; // đúng 4, có sẵn nhãn "A. " … "D. " (E1)
  dung: number;
  giai_thich: string[]; // cùng thứ tự với `chon`
};
export type VideoKhungData = {
  id: string;
  ten: string;
  video: string;
  poster?: string;
  tong_giay: number;
  o: VideoKhungO[];
  dung_dua: VideoKhungDuDoan;
  cau_chot?: VideoKhungCauChot; // clip chưa có thì chạy như cũ (chỉ dừng ở Dự đoán)
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
  | { loai: "bo_qua" }
  // Câu chốt (việc 6 sẽ gom các sự kiện này, ghi DB một lần khi xem xong/rời trang)
  | { loai: "dung_o_cau_chot" }
  | { loai: "chon_cau_chot"; chon: number; dung: boolean }
  | { loai: "bo_qua_cau_chot" }
  // Lượt xem mới bắt đầu (lần phát đầu): trang gọi chuẩn bị token ghi lượt (services/clip-views) — không lúc tải trang
  | { loai: "bat_dau_luot" };

/** Một lượt xem (việc 6): gom ở máy khách, gửi qua `onLuot` khi xem hết / ẩn tab / rời trang. Cùng `luotId` gửi lại
 *  là ảnh chụp mới của cùng lượt (máy chủ upsert). Khoá camelCase = payload RPC `log_clip_view`. */
export type VideoKhungLuot = {
  luotId: string;
  tnId: string;
  banClip: string; // tên file mp4: phân biệt clip cũ và clip dựng lại (việc 4)
  coCauChot: boolean;
  duDoan: number | null;
  duDoanBoQua: boolean;
  duDoanDung: boolean | null;
  chot: number | null;
  chotBoQua: boolean;
  chotDung: boolean | null;
  soXemLai: number;
  xemHet: boolean;
  giayMax: number;
  batDau: string;
};

const uuid = () => {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") return crypto.randomUUID();
  const b = crypto.getRandomValues(new Uint8Array(16));
  b[6] = (b[6] & 0x0f) | 0x40;
  b[8] = (b[8] & 0x3f) | 0x80;
  const h = [...b].map((x) => x.toString(16).padStart(2, "0")).join("");
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
};

type Hoi = "du_doan" | "cau_chot" | null;

/** Câu trả lời đã chọn theo id clip, sống ngoài component: bài vẽ lại HTML (KaTeX tải xong, bấm video YouTube khác)
 *  thì khung được gắn lại và vẫn nhớ em đã đoán, không bắt dừng hỏi lần nữa. */
/** Dừng sớm hơn mốc cuối cảnh Dự đoán (giây): hình còn là hình của câu hỏi, không trôi sang cảnh kế (K7). */
const DUNG_SOM = 0.5;

const TRA_LOI = new Map<
  string,
  { chose: number | null; boQua: boolean; chotChose?: number | null; chotBoQua?: boolean }
>();

/** Khối câu hỏi + 4 lựa chọn dùng chung cho câu Dự đoán và câu chốt (cùng nhãn A–D, cùng cỡ nút 48px, cùng cách
 *  cuộn ở effect trên qua `data-hoi`/`data-chon`). Câu chốt (hienDapAn) đánh dấu thêm lựa chọn đúng sau khi chọn. */
function KhoiChon(p: {
  nhanNhom: string;
  cauHoi: string;
  chon: string[];
  daChon: number | null;
  dungIdx: number;
  onChon: (k: number) => void;
  onBoQua: () => void;
  chuBoQua: string;
  giaiThich: (k: number) => string;
  hienDapAn?: boolean;
  onXemTiep: () => void;
}) {
  const dung = p.daChon === p.dungIdx;
  return (
    <div role="group" aria-live="polite" aria-label={p.nhanNhom} data-hoi>
      <p className="text-[17px] leading-relaxed text-ink">{p.cauHoi}</p>
      <div className="mt-3 grid gap-2">
        {p.chon.map((s, k) => {
          const picked = p.daChon === k;
          const laDung = !!p.hienDapAn && p.daChon !== null && k === p.dungIdx;
          return (
            <button
              key={s}
              type="button"
              data-chon
              disabled={p.daChon !== null}
              onClick={() => p.onChon(k)}
              aria-label={laDung ? `${s} (đáp án)` : undefined}
              className={
                "flex min-h-12 items-center gap-2 rounded-xl border px-4 py-2 text-left text-[16px] font-semibold transition-colors " +
                (laDung
                  ? "border-ok bg-panel text-ink"
                  : picked
                    ? "border-primary bg-primary-soft text-ink"
                    : "border-line-strong bg-panel text-ink hover:bg-primary-soft disabled:opacity-60")
              }
            >
              <span className="flex-1">{s}</span>
              {laDung && <Check className="size-5 shrink-0 text-ok" aria-hidden />}
              {p.hienDapAn && picked && !laDung && <Target className="size-5 shrink-0 text-warn" aria-hidden />}
            </button>
          );
        })}
      </div>
      {p.daChon === null && (
        <button
          type="button"
          onClick={p.onBoQua}
          className="mt-2 min-h-11 px-1 text-[14px] text-muted underline underline-offset-2 hover:text-ink"
        >
          {p.chuBoQua}
        </button>
      )}
      {p.daChon !== null && (
        <div className="mt-3 rounded-xl bg-surface-2 p-3">
          <p className="flex items-start gap-2 text-[15px] leading-relaxed text-ink">
            {dung ? (
              <Check className="mt-0.5 size-5 shrink-0 text-ok" aria-hidden />
            ) : (
              <Target className="mt-0.5 size-5 shrink-0 text-warn" aria-hidden />
            )}
            <span>
              <b>{dung ? "Đúng hướng. " : "Chưa khớp. "}</b>
              {p.giaiThich(p.daChon)}
            </span>
          </p>
          <button
            type="button"
            onClick={p.onXemTiep}
            className="mt-3 inline-flex min-h-12 items-center gap-2 rounded-xl bg-primary px-5 text-[16px] font-bold text-white hover:bg-primary-dark"
          >
            <Play className="size-4" aria-hidden /> Xem tiếp
          </button>
        </div>
      )}
    </div>
  );
}

export default function VideoThiNghiemKhung({
  data,
  onEvent,
  onLuot,
  dinh = true,
}: {
  data: VideoKhungData;
  onEvent?: (e: VideoKhungEvent) => void;
  /** Nhận lượt xem đã gom để ghi DB (việc 6). Trang /dev không truyền thì không gom gì. */
  onLuot?: (l: VideoKhungLuot) => void;
  /** Video dính trên đầu màn hình khi cuộn. Trang bài có thanh tab dính sẵn nên ContentHtml truyền false. */
  dinh?: boolean;
}) {
  const saved = TRA_LOI.get(data.id);
  const videoRef = useRef<HTMLVideoElement>(null);
  const sectionRef = useRef<HTMLElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null); // khối bọc video (dính, thu nhỏ lúc dừng ở điện thoại)
  const cardRef = useRef<HTMLDivElement>(null); // ô hiện tại ở điện thoại (video cao gần hết màn hình nên câu hỏi nằm dưới)
  const askingRef = useRef<Hoi>(null); // đồng bộ với `asking` ngay lúc gọi (onPlay chạy trước khi React kịp dựng lại)
  const askedOnce = useRef(false);
  const chotAskedOnce = useRef(false);
  const doneRef = useRef(!!saved && (saved.chose !== null || saved.boQua)); // đã chọn hoặc chủ động bấm "xem luôn": từ đó mới hết bắt dừng và mở Giả thuyết
  const chotDoneRef = useRef(!!saved && (saved.chotChose != null || !!saved.chotBoQua)); // câu chốt: đã chọn hoặc bỏ qua
  const eventRef = useRef(onEvent); // trang gọi truyền hàm mới mỗi lần dựng: giữ ở ref để vòng rAF không bị huỷ liên tục
  const luotRef = useRef(onLuot);
  useEffect(() => {
    eventRef.current = onEvent;
    luotRef.current = onLuot;
  }, [onEvent, onLuot]);
  // Lượt xem đang mở + cờ "có thay đổi chưa gửi". Mở ở lần phát đầu, đóng (gửi rồi bỏ) khi xem hết.
  const luot = useRef<VideoKhungLuot | null>(null);
  const luotBan = useRef(false);
  const guiLuot = useCallback(() => {
    if (!luot.current || !luotBan.current) return;
    luotBan.current = false;
    luotRef.current?.({ ...luot.current });
  }, []);
  const suaLuot = (f: (l: VideoKhungLuot) => void) => {
    if (!luot.current) return;
    f(luot.current);
    luotBan.current = true;
  };
  // Rời trang / ẩn tab (điện thoại khoá màn hình, chuyển app) / gỡ khung: gửi ảnh chụp lượt hiện tại.
  useEffect(() => {
    const an = () => {
      if (document.visibilityState === "hidden") guiLuot();
    };
    document.addEventListener("visibilitychange", an);
    window.addEventListener("pagehide", guiLuot);
    return () => {
      document.removeEventListener("visibilitychange", an);
      window.removeEventListener("pagehide", guiLuot);
      guiLuot();
    };
  }, [guiLuot]);
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
  const [asking, setAskingState] = useState<Hoi>(null);
  const setAsking = useCallback((b: Hoi) => {
    askingRef.current = b;
    setAskingState(b);
  }, []);
  const [chose, setChose] = useState<number | null>(saved?.chose ?? null);
  const [boQua, setBoQua] = useState(saved?.boQua ?? false);
  const [chotChose, setChotChose] = useState<number | null>(saved?.chotChose ?? null);

  const dd = data.dung_dua;
  const mocDung = dd.giay - DUNG_SOM;
  // Dữ liệu câu chốt sai dạng (gõ tay vào HTML bài) thì bỏ qua cả câu, clip chạy như cũ thay vì hỏng khung.
  const cc =
    data.cau_chot &&
    data.cau_chot.chon?.length === 4 &&
    data.cau_chot.giai_thich?.length === 4 &&
    data.cau_chot.dung >= 0 &&
    data.cau_chot.dung < 4 &&
    data.cau_chot.giay > dd.giay
      ? data.cau_chot
      : undefined;
  const mocChot = cc ? cc.giay : Infinity; // câu chốt: dừng đúng mốc (câu hỏi trong clip đã hiện đủ, Gợi ý chưa hiện)
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

  // Mở lượt xem ở lần phát đầu — hoặc khi tua qua điểm dừng trước khi bấm phát (hoi() chạy trước onPlay).
  const moLuot = useCallback(() => {
    if (luot.current || !luotRef.current) return;
    luot.current = {
      luotId: uuid(),
      tnId: data.id,
      banClip: (data.video.split("/").pop() ?? "").split("?")[0].toLowerCase(),
      coCauChot: !!cc,
      duDoan: null,
      duDoanBoQua: false,
      duDoanDung: null,
      chot: null,
      chotBoQua: false,
      chotDung: null,
      soXemLai: 0,
      xemHet: false,
      giayMax: 0,
      batDau: new Date().toISOString(),
    };
    luotBan.current = true;
    eventRef.current?.({ loai: "bat_dau_luot" });
  }, [data.id, data.video, cc]);

  // Dừng ở câu Dự đoán: thoát toàn màn hình (iOS/Android che mất thẻ câu hỏi), đưa focus vào nút chọn đầu tiên.
  const hoi = useCallback(
    (v: HTMLVideoElement, loai: "du_doan" | "cau_chot" = "du_doan") => {
      v.pause();
      moLuot();
      const w = v as HTMLVideoElement & { webkitExitFullscreen?: () => void };
      if (document.fullscreenElement) void document.exitFullscreen().catch(() => {});
      else w.webkitExitFullscreen?.();
      setAsking(loai);
      const once = loai === "du_doan" ? askedOnce : chotAskedOnce;
      if (!once.current) {
        once.current = true;
        eventRef.current?.({ loai: loai === "du_doan" ? "dung_o_du_doan" : "dung_o_cau_chot" });
      }
    },
    [setAsking, moLuot],
  );

  const check = useCallback(() => {
    const v = videoRef.current;
    if (!v) return;
    const now = v.currentTime;
    setT(now);
    if (luot.current && now > luot.current.giayMax + 0.5) suaLuot((l) => (l.giayMax = Math.round(now * 10) / 10));
    // chưa trả lời thì các ô sau Dự đoán vẫn khoá, dù thanh tua đã kéo qua
    setReached((r) => Math.max(r, doneRef.current ? curOf(now) : Math.min(curOf(now), duDoanIdx)));
    if (now >= mocDung && !v.seeking && !v.paused && !doneRef.current) hoi(v);
    else if (now >= mocChot && !v.seeking && !v.paused && doneRef.current && !chotDoneRef.current) hoi(v, "cau_chot");
    if (doneRef.current && now >= data.tong_giay - 0.5) {
      if (luot.current) {
        suaLuot((l) => {
          l.xemHet = true;
          l.giayMax = Math.max(l.giayMax, Math.round(now * 10) / 10);
        });
        guiLuot();
        luot.current = null; // phát lại từ đầu là lượt mới
      }
      setXong(true);
      try {
        localStorage.setItem(KEY_XONG, "1");
      } catch {}
    }
  }, [curOf, mocDung, mocChot, duDoanIdx, hoi, data.tong_giay, KEY_XONG, guiLuot]);

  // rAF chỉ chạy khi video đang phát; lúc dừng/tua cập nhật bằng sự kiện (tab ẩn thì timeupdate vẫn bắt kịp).
  const raf = useRef(0);
  useEffect(() => () => cancelAnimationFrame(raf.current), []);

  const onPlay = () => {
    const v = videoRef.current;
    const dangHoi =
      (askingRef.current === "du_doan" && !doneRef.current) ||
      (askingRef.current === "cau_chot" && !chotDoneRef.current);
    if (dangHoi) {
      v?.pause(); // chạm vào video hay bấm play gốc cũng không bỏ qua được câu hỏi
      return;
    }
    setAsking(null);
    moLuot();
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
    if (!doneRef.current && now >= mocDung) {
      v.currentTime = Math.max(0, mocDung - 0.05);
      hoi(v);
      return;
    }
    // Câu chốt cũng vậy: tua qua khi chưa trả lời thì đưa về đúng mốc và hỏi.
    if (doneRef.current && !chotDoneRef.current && now >= mocChot) {
      v.currentTime = Math.max(0, mocChot - 0.05);
      hoi(v, "cau_chot");
      return;
    }
    if (now < mocDung - 0.25 || (askingRef.current === "cau_chot" && now < mocChot - 0.25)) setAsking(null);
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
    const sec = sectionRef.current;
    const wrap = wrapRef.current;
    const grp = sec?.querySelector<HTMLElement>("[data-hoi]");
    const hep = !window.matchMedia("(min-width: 1024px)").matches;
    if (hep && wrap && grp && grp.offsetParent !== null) {
      // Điện thoại: video thu còn 36svh (đã đổi bằng class), vẫn dính; cuộn để câu hỏi nằm NGAY DƯỚI đáy video,
      // không bị video đè và không phải cuộn thêm (N8). Trong trang bài (dinh=false) video dính dưới thanh tab đầu bài.
      const tab = document.querySelector<HTMLElement>(".lesson-tabs");
      const topV =
        !dinh && tab && getComputedStyle(tab).position === "sticky" ? tab.getBoundingClientRect().bottom + 8 : 8;
      wrap.style.setProperty("--kd-top", `${topV}px`);
      wrap.style.removeProperty("--kd-h");
      const dat = grp.getBoundingClientRect().top - (topV + wrap.offsetHeight + 8);
      if (Math.abs(dat) > 1) window.scrollBy({ top: dat, behavior: "instant" });
      // Câu hỏi dài + lựa chọn xuống dòng có thể tràn xuống thanh điều hướng dưới: thu thêm video (sàn 26svh)
      // đúng phần tràn, rồi dán lại câu hỏi vào đáy video.
      const nav = document.querySelector<HTMLElement>(".mobile-tabbar");
      const day =
        (nav && getComputedStyle(nav).display !== "none" ? nav.getBoundingClientRect().top : window.innerHeight) - 4;
      const tran = grp.getBoundingClientRect().bottom - day;
      if (tran > 0) {
        const h = Math.max(wrap.offsetHeight - tran, window.innerHeight * 0.26);
        wrap.style.setProperty("--kd-h", `${Math.round(h)}px`);
        const dat2 = grp.getBoundingClientRect().top - (topV + wrap.offsetHeight + 8);
        if (Math.abs(dat2) > 1) window.scrollBy({ top: dat2, behavior: "instant" });
      }
    }
    const nut = [...(sec?.querySelectorAll<HTMLButtonElement>("button[data-chon]") ?? [])].find(
      (b) => b.offsetParent !== null && !b.disabled,
    );
    nut?.focus({ preventScroll: true });
  }, [asking, dinh]);

  const seekTo = (i: number) => {
    const v = videoRef.current;
    if (!v || i > reached) return;
    v.currentTime = data.o[i].giay + 0.05;
    setAsking(null);
    eventRef.current?.({ loai: "xem_lai_o", khoa: data.o[i].khoa });
    suaLuot((l) => (l.soXemLai += 1));
    void v.play().catch(() => {});
  };

  const choose = (i: number) => {
    if (doneRef.current) return;
    doneRef.current = true;
    setChose(i);
    TRA_LOI.set(data.id, { ...TRA_LOI.get(data.id), chose: i, boQua: false });
    eventRef.current?.({ loai: "chon", chon: i, dung: i === dd.dung });
    suaLuot((l) => {
      l.duDoan = i;
      l.duDoanDung = i === dd.dung;
    });
  };

  const resume = () => {
    setAsking(null);
    void videoRef.current?.play().catch(() => {});
  };

  const boQuaCau = () => {
    if (doneRef.current) return;
    doneRef.current = true;
    setBoQua(true);
    TRA_LOI.set(data.id, { ...TRA_LOI.get(data.id), chose: null, boQua: true });
    eventRef.current?.({ loai: "bo_qua" });
    suaLuot((l) => (l.duDoanBoQua = true));
    resume();
  };

  const chooseChot = (i: number) => {
    if (!cc || chotDoneRef.current) return;
    chotDoneRef.current = true;
    setChotChose(i);
    TRA_LOI.set(data.id, { chose, boQua, ...TRA_LOI.get(data.id), chotChose: i, chotBoQua: false });
    eventRef.current?.({ loai: "chon_cau_chot", chon: i, dung: i === cc.dung });
    suaLuot((l) => {
      l.chot = i;
      l.chotDung = i === cc.dung;
    });
  };

  const boQuaChot = () => {
    if (chotDoneRef.current) return;
    chotDoneRef.current = true;
    TRA_LOI.set(data.id, { chose, boQua, ...TRA_LOI.get(data.id), chotChose: null, chotBoQua: true });
    eventRef.current?.({ loai: "bo_qua_cau_chot" });
    suaLuot((l) => (l.chotBoQua = true));
    resume();
  };

  // Giả thuyết nói thẳng quan hệ cần đoán nên chưa lộ: chỉ hiện sau khi em đã chọn (hoặc bấm xem luôn);
  // trước đó hiện câu hỏi trung tính `kiem`.
  const daQuaDuDoan = chose !== null || boQua;
  const an = (o: VideoKhungO) => o.khoa === "gia_thuyet" && !!o.kiem && !daQuaDuDoan;
  const nhan = (o: VideoKhungO) =>
    asking === "cau_chot" && o === data.o[curOf(t)] ? "Câu chốt" : an(o) ? "Câu hỏi của thí nghiệm" : NHAN[o.khoa];
  const chu = (o: VideoKhungO) => (an(o) ? o.kiem : o.chu);

  const cur = curOf(t);
  const shown = asking === "du_doan" ? duDoanIdx : cur;
  // Chưa bấm phát: "Cần kiểm tra · 1/6 · 0:00" + 5 ổ khoá không nói phải làm gì → một câu chỉ dẫn (HS học thử 26/11, N1, L4).
  const chuaXem = t === 0 && reached === 0 && asking === null && chose === null && !boQua;
  const chiDan = (
    <p className="text-[15px] leading-snug text-ink" style={{ margin: "0 0 10px" }}>
      Bấm ▶ xem video. Video tự dừng ở câu dự đoán để em đoán trước; các ô 🔒 mở dần khi video chạy tới.
    </p>
  );

  const body = (i: number, big: boolean) => {
    const o = data.o[i];
    if (i === duDoanIdx && asking === "du_doan") {
      return (
        <KhoiChon
          nhanNhom={"Câu dự đoán"}
          cauHoi={dd.cau_hoi}
          chon={dd.chon}
          daChon={chose}
          dungIdx={dd.dung}
          onChon={(k) => choose(k)}
          onBoQua={() => boQuaCau()}
          chuBoQua={"Chưa muốn đoán, xem luôn"}
          giaiThich={(k) => (k === dd.dung ? dd.giai_thich_dung : dd.giai_thich_sai)}
          onXemTiep={resume}
        />
      );
    }
    if (cc && asking === "cau_chot" && i === shown) {
      return (
        <KhoiChon
          nhanNhom={"Câu chốt"}
          cauHoi={cc.cau_hoi}
          chon={cc.chon}
          daChon={chotChose}
          dungIdx={cc.dung}
          onChon={(k) => chooseChot(k)}
          onBoQua={() => boQuaChot()}
          chuBoQua={"Chưa muốn trả lời, xem tiếp"}
          giaiThich={(k) => cc.giai_thich[k] ?? ""}
          hienDapAn={true}
          onXemTiep={resume}
        />
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
          {chuaXem && chiDan}
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
                {!chuaXem && (
                  <span className="text-[13px] font-semibold text-muted">
                    {shown + 1}/{data.o.length} · {mmss(data.o[shown].giay)}
                  </span>
                )}
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
          ref={wrapRef}
          className={
            "order-1 mx-auto w-full self-start lg:mx-0 " +
            // Video dọc cao theo màn hình: điện thoại ≤ 50svh để ô câu hỏi bên dưới vẫn trong tầm mắt;
            // màn rộng bề rộng cố định (cột tương tác lấy phần còn lại), dính dưới thanh tab, cao vừa khung nhìn.
            "lg:w-[min(280px,calc((100svh_-_8rem)_*_9_/_16))] lg:max-w-none xl:w-[min(340px,calc((100svh_-_8rem)_*_9_/_16))] " +
            (asking
              ? // Lúc dừng ở câu hỏi: video thu còn 36svh nhưng VẪN dính để câu hỏi + 4 lựa chọn nằm trọn dưới video
                "sticky top-[var(--kd-top,0.5rem)] z-10 max-w-[min(340px,calc(var(--kd-h,36svh)_*_9_/_16))] " +
                (dinh ? "lg:top-4" : "lg:top-24")
              : dinh
                ? "sticky top-2 z-10 max-w-[min(340px,calc(62svh_*_9_/_16))] lg:top-4"
                : "max-w-[min(340px,calc(50svh_*_9_/_16))] lg:sticky lg:top-24")
          }
        >
          <video
            ref={videoRef}
            src={data.video}
            poster={data.poster ?? data.video.replace(/\.mp4$/, ".webp")}
            controls={!asking} // lúc dừng ẩn thanh điều khiển gốc để không đè phụ đề; chọn xong/“xem luôn” thì hiện lại
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
