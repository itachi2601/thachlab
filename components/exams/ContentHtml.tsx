"use client";

import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { withQuestionTables } from "@/lib/question-table";
import imageDimensions from "@/features/lessons/image-dimensions.json";

const IMAGE_DIMENSIONS = imageDimensions as Record<string, number[]>;

/** Nút 🔊 bài Anh văn chuyên ngành: mp3 neural đang phát (nếu có), để bấm nút khác thì dừng cái cũ. */
let speakingAudio: HTMLAudioElement | null = null;

/** Đọc bằng giọng của trình duyệt (en-US, chậm 0.9) — dự phòng khi bài chưa có mp3 hoặc mp3 không tải được. */
function speakBrowser(text: string) {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "en-US";
  u.rate = 0.9;
  // Nhiều trình duyệt (Safari/iOS, Chrome Mac/Android) bỏ qua `lang` nếu không gán voice → đọc bằng giọng mặc định
  // của máy (tiếng Việt). Chọn giọng en tường minh, xếp hạng: ưu tiên Premium/Enhanced/Neural/Natural và các giọng
  // tự nhiên đã biết, tránh giọng nén/robot (Fred, Albert, Zarvox…); en-US hơn en-khác.
  const score = (v: SpeechSynthesisVoice) => {
    const lang = v.lang.replace("_", "-").toLowerCase();
    if (!lang.startsWith("en")) return -1;
    let s = lang === "en-us" ? 10 : 5;
    if (/premium|enhanced|neural|natural|online/i.test(v.name)) s += 30;
    if (/\b(samantha|ava|allison|evan|nicky|zoe|aria|jenny|guy|google us english)\b/i.test(v.name)) s += 20;
    if (/\b(fred|albert|zarvox|bad news|bahh|bells|boing|bubbles|cellos|deranged|good news|hysterical|junior|kathy|organ|princess|ralph|trinoids|whisper|superstar)\b/i.test(v.name)) s -= 40;
    if (v.localService === false) s += 5;
    return s;
  };
  const voice = window.speechSynthesis
    .getVoices()
    .filter((v) => score(v) >= 0)
    .sort((a, b) => score(b) - score(a))[0];
  if (voice) u.voice = voice;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(u);
}

/** Hình SVG có hoạt hình SMIL (`<animate>`): người dùng bật "giảm chuyển động" thì bỏ hoạt hình, hình đứng yên ở khung đầu. */
function withoutAnimationIfReduced(html: string): string {
  if (!html.includes("<animate")) return html;
  if (typeof window === "undefined" || !window.matchMedia?.("(prefers-reduced-motion: reduce)").matches) return html;
  return html
    .replace(/<animate(?:Transform)?\b[^>]*?(?:\/>|>\s*<\/animate(?:Transform)?>)/g, "")
    .replace(/<button[^>]*data-bt-run[^>]*>[\s\S]*?<\/button>/g, "");
}

/**
 * Ảnh tĩnh (hình vẽ, công thức quét) không có width/height trong HTML lưu —
 * trình duyệt không biết trước tỉ lệ nên chừa 0px chỗ rồi "nhảy" layout khi
 * ảnh tải xong, dễ thấy nhất khi đang cuộn trên điện thoại (chữ bị đè/lệch
 * trong khoảnh khắc ảnh vừa hiện). Gắn sẵn width/height thật (đọc lúc build,
 * xem scripts/gen-image-dimensions.mjs) để trình duyệt trừ chỗ đúng ngay từ đầu.
 * Ảnh trong bài học hầu hết nằm dưới màn hình đầu → gắn thêm decoding="async" cho
 * mọi ảnh, và loading="lazy" cho ảnh đã có width/height (ảnh chưa biết kích thước
 * mà lazy thì layout sẽ nhảy lúc cuộn tới, nên vẫn để tải sớm như cũ).
 */
function withImageDimensions(html: string): string {
  if (!html.includes("<img")) return html;
  return html.replace(/<img\b([^>]*)>/g, (tag, attrs: string) => {
    const decoding = /\bdecoding=/.test(attrs) ? "" : ' decoding="async"';
    const lazy = /\bloading=/.test(attrs) ? "" : ' loading="lazy"';
    if (/\bwidth=/.test(attrs)) {
      // Có width mà thiếu height (ảnh AVCN, ảnh dán tay): lazy sẽ để ảnh cao 0px rồi bung ra lúc cuộn tới, kéo theo
      // cả trang giật khi cuộn/chuyển câu. Không biết tỉ lệ thì tải sớm (ảnh nhỏ, đã nén ≤150 KB).
      if (!/\bheight=/.test(attrs)) return `<img${attrs}${/\bloading=/.test(attrs) ? "" : ' loading="eager"'}${decoding}>`;
      return `<img${attrs}${lazy}${decoding}>`;
    }
    const src = attrs.match(/\bsrc="([^"]+)"/)?.[1];
    const dims = src ? IMAGE_DIMENSIONS[src] : undefined;
    if (!dims) return decoding ? `<img${attrs}${decoding}>` : tag;
    return `<img${attrs} width="${dims[0]}" height="${dims[1]}"${lazy}${decoding}>`;
  });
}

/**
 * Video thí nghiệm trong bài lý thuyết được soạn dưới dạng
 * `<div class="tl-video"><iframe src="https://www.youtube-nocookie.com/embed/ID?rel=0">…`.
 * Nhúng thẳng thì mỗi video kéo theo ~1 MB JS của YouTube ngay khi cuộn tới (bài Giao thoa
 * có 4 video), trong khi phần lớn học sinh không bấm xem. Ở đây đổi thành **ảnh bìa + nút
 * phát**, chỉ nhúng player khi bấm — cùng cách với `VideoBlock` ở `app/lop-hoc/bai/page.tsx`.
 * Ảnh bìa lấy từ i.ytimg.com (có width/height nên không nhảy layout), nút là `<button>` thật
 * nên bấm được cả bằng bàn phím. Video không phải YouTube thì để nguyên iframe.
 */
const TL_VIDEO_RE = /<div class="tl-video">\s*<iframe\b([^>]*)>\s*<\/iframe>\s*<\/div>/g;

function escapeAttr(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

export function withVideoFacades(html: string): string {
  if (!html.includes("tl-video")) return html;
  let slot = 0;
  return html.replace(TL_VIDEO_RE, (match, attrs: string) => {
    const src = /\bsrc="([^"]+)"/.exec(attrs)?.[1] ?? "";
    const id = /youtube-nocookie\.com\/embed\/([\w-]{11})/.exec(src)?.[1];
    if (!id) return match;
    const query = src.includes("?") ? src.slice(src.indexOf("?")) : "";
    const title = escapeAttr((/\btitle="([^"]*)"/.exec(attrs)?.[1] ?? "video thí nghiệm").trim());
    const start = Number(/[?&]start=(\d+)/.exec(query)?.[1] ?? NaN);
    const end = Number(/[?&]end=(\d+)/.exec(query)?.[1] ?? NaN);
    const dur = Number.isFinite(start) && Number.isFinite(end) && end > start ? `${end - start} giây` : "";
    return (
      `<div class="tl-video tl-video--facade">` +
      `<button type="button" class="tl-video-play" data-yt-slot="${slot++}" data-yt-id="${id}"` +
      ` data-yt-query="${escapeAttr(query)}" data-yt-title="${title}" aria-label="Phát video: ${title}">` +
      `<img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy" decoding="async">` +
      `<span class="tl-video-play-icon" aria-hidden="true">▶</span>` +
      (dur ? `<span class="tl-video-play-time">${dur}</span>` : "") +
      `<span class="tl-video-play-title">${title}</span>` +
      `</button></div>`
    );
  });
}

/** Đổi đúng nút phát của `slot` thành iframe player (chạy sau khi học sinh bấm). */
export function playVideo(html: string, slot: number, id: string, query: string, title: string): string {
  const re = new RegExp(`<button type="button" class="tl-video-play" data-yt-slot="${slot}"[\\s\\S]*?</button>`);
  const params = new URLSearchParams(query.startsWith("?") ? query.slice(1) : query);
  params.set("autoplay", "1");
  if (!params.has("rel")) params.set("rel", "0");
  const iframe =
    `<iframe src="https://www.youtube-nocookie.com/embed/${id}?${params.toString()}"` +
    ` title="${escapeAttr(title)}" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
  return html.replace(re, iframe);
}

/**
 * Dấu vết định dạng Word còn sót lại khi dán qua: dòng chấm dẫn của mục lục
 * ("I. TÓM TẮT.........."), ký tự thay thế khi font/encoding lỗi, và các
 * đoạn liệt kê gõ tay bằng "-"/"•" ở đầu dòng thay vì thẻ <ul><li> thật —
 * đánh dấu lại bằng data-bullet để CSS vẽ chấm đầu dòng thụt lề nhất quán.
 * Bảng dán từ Word có sẵn min-width cố định, tràn màn hình điện thoại nếu
 * để nguyên — bọc riêng một lớp cuộn ngang cho bảng, không đẩy tràn cả trang.
 */
/** Hộp "Đề bài" của bài toán mẫu trong lý thuyết mô phỏng một câu hỏi thi ⇒ nhận class `tl-box--de` để
 *  CSS đặt font đề thi thật (E4). Làm lúc hiển thị nên bài đã đăng không cần đăng lại. */
function withDeBaiBox(html: string): string {
  return html.replace(
    /<div class="(tl-box(?: [^"]*)?)"([^>]*)>(\s*<p class="tl-label">[^<]*Đề bài)/g,
    '<div class="$1 tl-box--de"$2>$3',
  );
}

function stripWordArtifacts(html: string): string {
  return html
    .replace(/[�￼]/g, "")
    .replace(/\.{4,}/g, "")
    .replace(/(<p\b[^>]*)>(\s*)[-•●▪][ \t ]+/g, '$1 data-bullet="1">')
    .replace(/<table\b/g, '<div class="table-scroll"><table')
    .replace(/<\/table>/g, "</table></div>");
}

// Nhận diện cả 3 kiểu đánh dấu công thức: "$…$"/"$$…$$" (Azota, phổ biến nhất
// trong dữ liệu hiện có) và "\(…\)"/"\[…\]" (một số nguồn dán vào theo chuẩn
// LaTeX gốc). Chỉ cần MỘT trong 3 ký hiệu xuất hiện là coi như "có thể có công
// thức" — quyết định có tải KaTeX (~290 KB) hay không dựa vào đây.
const MATH_MARKER = /\$|\\\(|\\\[/;
const MATH_PATTERN = /\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$|\\\(([\s\S]+?)\\\)|\\\[([\s\S]+?)\\\]/g;

function hasMath(html: string): boolean {
  return MATH_MARKER.test(html);
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/**
 * Trong lúc chờ KaTeX tải xong (hoặc nếu tải lỗi): hiện nguyên văn LaTeX bọc
 * trong <code> — học sinh vẫn đọc được ký hiệu thô ngay lập tức, không có
 * skeleton/khoảng trắng nên không nhảy layout khi công thức "biến hình" lúc
 * KaTeX tải xong (kích thước <code> và công thức render đã render gần giống
 * nhau về chiều cao dòng).
 */
function renderRawFallback(html: string): string {
  if (!hasMath(html)) return html;
  return html.replace(
    MATH_PATTERN,
    (match) => `<code class="exam-content-raw-tex">${escapeHtml(match)}</code>`,
  );
}

type KatexModule = typeof import("katex");

let katexPromise: Promise<KatexModule> | null = null;

function loadKatex(): Promise<KatexModule> {
  if (!katexPromise) {
    katexPromise = Promise.all([import("katex"), import("katex/dist/katex.min.css")]).then(
      ([mod]) => (("default" in mod ? mod.default : mod) as unknown as KatexModule),
    );
  }
  return katexPromise;
}

function renderWithKatex(html: string, katex: KatexModule): string {
  return html.replace(MATH_PATTERN, (match, display, inline, parenInline, bracketDisplay) => {
    const tex = display ?? inline ?? parenInline ?? bracketDisplay;
    const displayMode = display !== undefined || bracketDisplay !== undefined;
    try {
      // Dấu phẩy thập phân kiểu Việt (3,25): KaTeX coi là dấu câu và chèn khoảng trắng ("3, 25") → bọc {,}
      const fixed = tex.replace(/(\d),(?=\d)/g, "$1{,}");
      return katex.renderToString(fixed, { displayMode, throwOnError: false });
    } catch {
      return match; // giữ nguyên văn bản nếu LaTeX lỗi
    }
  });
}

/**
 * Render nội dung câu hỏi/bài học: HTML (ảnh công thức, hình vẽ) + LaTeX $...$.
 *
 * KaTeX (~290 KB) không còn nằm trong JS ban đầu của trang — chỉ `import()`
 * lúc component thực sự mount VÀ nội dung có dấu hiệu công thức ($, \(, \[).
 * Nội dung không có công thức thì không đụng tới KaTeX chút nào (không tải
 * chunk, không có CSS). Khi KaTeX tải xong, công thức được render thành chuỗi
 * HTML rồi đưa vào React (không biến đổi DOM sau khi mount) nên không bị mất
 * khi React re-render.
 */
/** Đáp án đã chọn theo nội dung HTML, sống ngoài component: nếu cha remount ContentHtml (đổi key, mở/đóng đoạn,
 *  tải lại dữ liệu bài) thì bản mới vẫn khôi phục được lựa chọn thay vì về "chưa chọn". Giữ tối đa 40 nội dung. */
const PICKS_BY_HTML = new Map<string, Record<string, string>>();

export default function ContentHtml({
  html,
  className = "",
}: {
  html: string;
  className?: string;
}) {
  const cleaned = useMemo(
    () => withoutAnimationIfReduced(withImageDimensions(withVideoFacades(withQuestionTables(withDeBaiBox(stripWordArtifacts(html)))))),
    [html],
  );
  const needsMath = useMemo(() => hasMath(cleaned), [cleaned]);

  // Video đang phát (theo `slot` trong `cleaned`). Giữ kèm `forHtml` để html đổi
  // thì tự rơi về facade, không cần setState "reset" trong effect.
  const [playing, setPlaying] = useState<
    { forHtml: string; slot: number; id: string; query: string; title: string } | null
  >(null);
  const active = playing && playing.forHtml === cleaned ? playing : null;

  // Chỉ giữ bản KaTeX đã render xong ỨNG VỚI đúng `cleaned` hiện tại (so khớp bằng
  // `forHtml`) — html đổi thì coi như chưa có, tự rơi về fallback thô bên dưới mà
  // không cần gọi setState đồng bộ trong effect để "reset" (tránh cascading renders).
  const [katexResult, setKatexResult] = useState<{ forHtml: string; rendered: string } | null>(
    null,
  );

  useEffect(() => {
    if (!needsMath) return; // không có công thức thì không đụng tới KaTeX chút nào
    let cancelled = false;
    loadKatex()
      .then((katex) => {
        if (!cancelled) setKatexResult({ forHtml: cleaned, rendered: renderWithKatex(cleaned, katex) });
      })
      .catch(() => {
        // Tải chunk lỗi (mất mạng, 404…) — giữ nguyên fallback văn bản thô, không kẹt trắng.
      });
    return () => {
      cancelled = true;
    };
  }, [cleaned, needsMath]);

  const rendered = !needsMath
    ? cleaned
    : katexResult && katexResult.forHtml === cleaned
      ? katexResult.rendered
      : renderRawFallback(cleaned);

  const renderedWithVideo = active
    ? playVideo(rendered, active.slot, active.id, active.query, active.title)
    : rendered;

  /** Bấm nút phát (uỷ quyền sự kiện): đổi đúng nút đó thành player, không tải player trước. */
  function handleClick(event: React.MouseEvent<HTMLSpanElement>) {
    if (!(event.target instanceof Element)) return;
    // Nút nghe 🔊 của bài Anh văn chuyên ngành: <button data-tl-speak="…"> — HTML lưu DB không chứa JS,
    // đọc bằng speechSynthesis của trình duyệt (en-US, chậm 0.9). Không lan ra <summary> bao ngoài.
    const speak = event.target.closest("button[data-tl-speak]");
    if (speak instanceof HTMLButtonElement) {
      event.preventDefault();
      event.stopPropagation();
      const text = speak.dataset.tlSpeak ?? "";
      const audioUrl = speak.dataset.tlAudio;
      if (!text) return;
      speakingAudio?.pause();
      speakingAudio = null;
      if (audioUrl) {
        // mp3 giọng neural dựng sẵn (Azure Aria); tải lỗi/không phát được thì rơi về giọng trình duyệt
        window.speechSynthesis?.cancel();
        const a = new Audio(audioUrl);
        speakingAudio = a;
        // Bấm nút khác khi mp3 này chưa kịp phát → pause() làm play() bị huỷ (AbortError); khi đó KHÔNG rơi về giọng
        // trình duyệt, nếu không giọng máy đọc câu cũ song song với mp3 mới (2 giọng cùng lúc).
        a.play().catch((e: unknown) => {
          if (speakingAudio === a && (e as { name?: string })?.name !== "AbortError") speakBrowser(text);
        });
        return;
      }
      speakBrowser(text);
      return;
    }
    // Mô phỏng SVG (SMIL begin="indefinite"): chạy MỘT lần mỗi lần bấm, không tự chạy khi đang đọc (B4).
    const run = event.target.closest("button[data-bt-run]");
    if (run instanceof HTMLButtonElement) {
      run.closest("figure")?.querySelectorAll("animate, animateTransform").forEach((a) => (a as SVGAnimationElement).beginElement?.());
      run.textContent = "↻ Chạy lại";
      return;
    }
    const button = event.target.closest("button.tl-video-play");
    if (!(button instanceof HTMLButtonElement)) return;
    const slot = Number(button.dataset.ytSlot);
    const id = button.dataset.ytId ?? "";
    if (!id || !Number.isFinite(slot)) return;
    setPlaying({
      forHtml: cleaned,
      slot,
      id,
      query: button.dataset.ytQuery ?? "",
      title: button.dataset.ytTitle ?? "video thí nghiệm",
    });
  }

  // Đáp án em đã chọn trong các câu tự chấm. innerHTML bị thay mỗi khi KaTeX tải xong hoặc
  // khi bấm phát video → radio mất dấu chọn, em thấy "bấm không ăn". Ghi nhớ rồi khôi phục.
  const rootRef = useRef<HTMLSpanElement>(null);
  const picks = useRef<{ forHtml: string; byKey: Record<string, string> }>({
    forHtml: cleaned,
    byKey: PICKS_BY_HTML.get(cleaned) ?? {},
  });

  function markAnswered(input: HTMLInputElement) {
    const quiz = input.closest<HTMLElement>(".tl-quiz");
    const label = input.nextElementSibling;
    if (!quiz || !input.checked || !(label instanceof HTMLElement)) return;
    // Dự phòng cho WebView cũ (Zalo/Facebook) chưa có :has() — CSS đọc data-answered.
    quiz.dataset.answered = label.classList.contains("tl-ok") ? "ok" : "no";
  }

  function handleChange(event: React.ChangeEvent<HTMLSpanElement>) {
    const input = event.target;
    if (!(input instanceof HTMLInputElement) || !input.id) return;
    if (input.type === "radio" && input.name) {
      picks.current.byKey[input.name] = input.id;
      markAnswered(input);
    } else if (input.type === "checkbox") {
      if (input.checked) picks.current.byKey[input.id] = input.id;
      else delete picks.current.byKey[input.id];
    }
  }

  useLayoutEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    if (picks.current.forHtml !== cleaned) picks.current = { forHtml: cleaned, byKey: PICKS_BY_HTML.get(cleaned) ?? {} };
    PICKS_BY_HTML.delete(cleaned);
    PICKS_BY_HTML.set(cleaned, picks.current.byKey);
    if (PICKS_BY_HTML.size > 40) PICKS_BY_HTML.delete(PICKS_BY_HTML.keys().next().value as string);
    for (const id of Object.values(picks.current.byKey)) {
      const el = root.querySelector(`[id="${id.replace(/"/g, "")}"]`);
      if (!(el instanceof HTMLInputElement) || el.checked) continue;
      el.checked = true;
      markAnswered(el);
    }
  }, [renderedWithVideo, cleaned]);

  return (
    <span
      ref={rootRef}
      className={`exam-content ${className}`}
      onClick={handleClick}
      onChange={handleChange}
      dangerouslySetInnerHTML={{ __html: renderedWithVideo }}
    />
  );
}
