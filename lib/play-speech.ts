// Phát âm bài Anh văn chuyên ngành (AVCN): mp3 neural dựng sẵn, dự phòng giọng trình duyệt.
// Dùng chung cho nút 🔊 trong bài (components/exams/ContentHtml.tsx) và mục Luyện từ (components/lessons/avcn/).

/** Nút 🔊 bài Anh văn chuyên ngành: mp3 neural đang phát (nếu có), để bấm nút khác thì dừng cái cũ. */
let speakingAudio: HTMLAudioElement | null = null;

/** Chuỗi vừa đọc, để `click` + `change` của cùng một lần bấm không đọc 2 lần. */
let lastSpoken = { text: "", at: 0 };

/** Đọc bằng giọng của trình duyệt (en-US, chậm 0.9) — dự phòng khi bài chưa có mp3 hoặc mp3 không tải được.
 *  `giong` = "nam" (lời nhân vật nam, vd. thợ cả) → xếp hạng giọng nam lên trước. */
export function speakBrowser(text: string, giong = "") {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "en-US";
  u.rate = 0.9;
  const nam = giong === "nam";
  // Nhiều trình duyệt (Safari/iOS, Chrome Mac/Android) bỏ qua `lang` nếu không gán voice → đọc bằng giọng mặc định
  // của máy (tiếng Việt). Chọn giọng en tường minh, xếp hạng: ưu tiên Premium/Enhanced/Neural/Natural và các giọng
  // tự nhiên đã biết, tránh giọng nén/robot (Fred, Albert, Zarvox…); en-US hơn en-khác. Bài AVCN có câu của nhân
  // vật nam (thợ cả) nên khi `nam` thì cộng điểm giọng nam, trừ điểm giọng nữ — máy nào cũng có ít nhất 1 giọng nam.
  const NAM = /\b(guy|andrew|brian|christopher|eric|roger|steffan|alex|daniel|james|ryan|mark|thomas|aaron|arthur)\b/i;
  const NU = /\b(aria|jenny|samantha|ava|allison|nicky|zoe|michelle|sonia|libby|emma|kathy|karen|moira|tessa|victoria)\b/i;
  const score = (v: SpeechSynthesisVoice) => {
    const lang = v.lang.replace("_", "-").toLowerCase();
    if (!lang.startsWith("en")) return -1;
    let s = lang === "en-us" ? 10 : 5;
    if (/premium|enhanced|neural|natural|online/i.test(v.name)) s += 30;
    if (/\b(samantha|ava|allison|evan|nicky|zoe|aria|jenny|guy|google us english)\b/i.test(v.name)) s += 20;
    if (nam) {
      if (NAM.test(v.name)) s += 25;
      if (NU.test(v.name)) s -= 25;
    }
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

/** Phát một chuỗi của bài AVCN: ưu tiên mp3 neural dựng sẵn (data-tl-audio), không có thì giọng trình duyệt.
 *  Mỗi lần chỉ một tiếng: dừng mp3 cũ và huỷ giọng máy đang đọc trước khi phát cái mới. */
export function playSpeech(text: string, audioUrl = "", giong = "") {
  if (!text) return;
  // Cùng một lần bấm có thể phát sinh cả `click` (do mình xử lý) và `change` (một số WebView): chỉ đọc một lần.
  const now = Date.now();
  if (text === lastSpoken.text && now - lastSpoken.at < 200) return;
  lastSpoken = { text, at: now };
  speakingAudio?.pause();
  speakingAudio = null;
  if (audioUrl) {
    // Bấm nút khác khi mp3 này chưa kịp phát → pause() làm play() bị huỷ (AbortError); khi đó KHÔNG rơi về giọng
    // trình duyệt, nếu không giọng máy đọc câu cũ song song với mp3 mới (2 giọng cùng lúc).
    window.speechSynthesis?.cancel();
    const a = new Audio(audioUrl);
    speakingAudio = a;
    a.play().catch((e: unknown) => {
      if (speakingAudio === a && (e as { name?: string })?.name !== "AbortError") speakBrowser(text, giong);
    });
    return;
  }
  speakBrowser(text, giong);
}
