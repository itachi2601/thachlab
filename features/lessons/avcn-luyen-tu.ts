// Mục "Luyện từ" của môn Anh văn chuyên ngành Cơ khí (lớp avcn): lượt ngắn ~11 câu, mỗi màn một câu, báo đúng/sai
// ngay, câu sai quay lại cuối lượt (thầy chốt 19/11/2026: 3 dạng từ vựng trước — chọn nghĩa, nghe chọn từ, ghép cặp;
// không tim/XP). Câu sinh trên máy học sinh từ public/assets/avcn/chapter-N/luyen-tu.json (scripts/avcn-luyen-tu.mjs).
// Quy tắc: N1/N5 (một màn một việc, lượt ngắn), L1 (phản hồi tức thì), L2 (tiến độ của lượt), L3 (không thưởng ngoài).

/** Bài AVCN Chapter n có id 167+n (docs/memory/project_thachlab_avcn.md). lesson id → số chương. */
export const AVCN_LUYEN_TU_LESSONS: Readonly<Record<number, number>> = Object.fromEntries(
  Array.from({ length: 10 }, (_, i) => [168 + i, i + 1]),
);

export function luyenTuUrl(chapter: number): string {
  return `/assets/avcn/chapter-${chapter}/luyen-tu.json`;
}

export type LtWord = { term: string; vi: string; ipa?: string; audio?: string };
export type LtData = { chapter: number; title: string; words: LtWord[]; them: { term: string; vi: string }[] };

/** nghia: thấy từ tiếng Anh → chọn nghĩa · tu: thấy nghĩa → chọn từ · nghe: nghe → chọn từ · ghep: ghép 5 cặp. */
export type LtItem =
  | { id: string; kind: "nghia" | "tu" | "nghe"; word: LtWord; options: string[]; answer: number; retry: number }
  | { id: string; kind: "ghep"; pairs: LtWord[]; rightOrder: number[]; retry: number };

export const ROUND_WORDS = 10;
export const MATCH_PAIRS = 5;
/** Một câu sai quay lại tối đa 2 lần trong lượt — tránh vòng lặp làm SV yếu nản (ngưỡng bỏ cuộc). */
export const MAX_RETRY = 2;

export const wordKey = (w: { term: string; vi: string }) => `${w.term}|${w.vi}`;

type Rng = () => number;

export function shuffle<T>(arr: readonly T[], rng: Rng = Math.random): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** Thống kê từng từ lưu trên máy (localStorage): đúng/sai/lần gặp cuối — để lượt sau ưu tiên từ hay sai. */
export type LtStats = Record<string, { ok: number; sai: number; at: number }>;

const statsKey = (chapter: number) => `avcn-luyen-tu:${chapter}`;

export function readStats(chapter: number): LtStats {
  try {
    const raw = window.localStorage.getItem(statsKey(chapter));
    const v = raw ? JSON.parse(raw) : null;
    return v && typeof v === "object" ? (v as LtStats) : {};
  } catch {
    return {};
  }
}

export function writeStats(chapter: number, stats: LtStats): void {
  try {
    window.localStorage.setItem(statsKey(chapter), JSON.stringify(stats));
  } catch {
    /* chế độ riêng tư / chặn lưu: lượt vẫn chạy, chỉ không nhớ từ hay sai */
  }
}

export function recordResult(stats: LtStats, w: LtWord, ok: boolean, now = Date.now()): LtStats {
  const k = wordKey(w);
  const cur = stats[k] ?? { ok: 0, sai: 0, at: 0 };
  return { ...stats, [k]: { ok: cur.ok + (ok ? 1 : 0), sai: cur.sai + (ok ? 0 : 1), at: now } };
}

/** Chọn từ cho lượt: tối đa 4 từ hay sai (sai > đúng), còn lại ưu tiên từ chưa gặp / gặp lâu nhất, xáo nhẹ. */
export function pickWords(words: LtWord[], stats: LtStats, n = ROUND_WORDS, rng: Rng = Math.random): LtWord[] {
  const weak = shuffle(
    words.filter((w) => {
      const s = stats[wordKey(w)];
      return s && s.sai > s.ok;
    }),
    rng,
  ).slice(0, 4);
  const weakSet = new Set(weak.map(wordKey));
  const rest = shuffle(
    words.filter((w) => !weakSet.has(wordKey(w))),
    rng,
  ).sort((a, b) => (stats[wordKey(a)]?.at ?? 0) - (stats[wordKey(b)]?.at ?? 0));
  return shuffle([...weak, ...rest.slice(0, Math.max(0, n - weak.length))], rng);
}

/** 3 phương án nhiễu + đáp án, xáo. Không lấy phương án trùng chữ đáp án, cũng không lấy nghĩa của từ cùng chữ
 *  (vd. "drill" = máy khoan và "drill" = khoan: hỏi nghĩa của một cái thì cái kia không được là phương án). */
function buildOptions(
  correct: string,
  pool: string[],
  fallback: string[],
  banned: Set<string>,
  rng: Rng,
): { options: string[]; answer: number } {
  const norm = (s: string) => s.toLowerCase().trim();
  const seen = new Set([norm(correct), ...[...banned].map(norm)]);
  const distract: string[] = [];
  // Ưu tiên phương án từ chính của chương (cùng độ khó); thiếu mới lấy từ bổ sung (`fallback`).
  for (const p of [...shuffle(pool, rng), ...shuffle(fallback, rng)]) {
    if (distract.length >= 3) break;
    if (seen.has(norm(p))) continue;
    seen.add(norm(p));
    distract.push(p);
  }
  const options = shuffle([correct, ...distract], rng);
  return { options, answer: options.indexOf(correct) };
}

export function makeChoiceItem(
  kind: "nghia" | "tu" | "nghe",
  word: LtWord,
  data: LtData,
  rng: Rng = Math.random,
): LtItem {
  const all = [...data.words, ...data.them];
  if (kind === "nghia") {
    const twins = all.filter((w) => w.term.toLowerCase() === word.term.toLowerCase() && w.vi !== word.vi).map((w) => w.vi);
    const { options, answer } = buildOptions(
      word.vi,
      data.words.map((w) => w.vi),
      data.them.map((w) => w.vi),
      new Set(twins),
      rng,
    );
    return { id: `${kind}:${wordKey(word)}`, kind, word, options, answer, retry: 0 };
  }
  const sameVi = all.filter((w) => w.vi === word.vi && w.term !== word.term).map((w) => w.term);
  const { options, answer } = buildOptions(
    word.term,
    data.words.map((w) => w.term),
    data.them.map((w) => w.term),
    new Set(sameVi),
    rng,
  );
  return { id: `${kind}:${wordKey(word)}`, kind, word, options, answer, retry: 0 };
}

/** Một lượt: 4 câu chọn nghĩa, 3 câu thấy nghĩa chọn từ, 3 câu nghe chọn từ, 1 lượt ghép 5 cặp ở giữa.
 *  Các từ không trùng chữ trong cùng một lượt ghép (ghép "drill" với hai nghĩa là mơ hồ). */
export function buildRound(data: LtData, stats: LtStats, rng: Rng = Math.random): LtItem[] {
  const words = pickWords(data.words, stats, ROUND_WORDS, rng);
  const kinds: ("nghia" | "tu" | "nghe")[] = ["nghia", "nghia", "nghia", "nghia", "tu", "tu", "tu", "nghe", "nghe", "nghe"];
  const choice = words.map((w, i) => makeChoiceItem(kinds[i % kinds.length], w, data, rng));
  const seenTerms = new Set<string>();
  const pairs: LtWord[] = [];
  for (const w of shuffle(words, rng)) {
    const t = w.term.toLowerCase();
    if (seenTerms.has(t) || pairs.some((p) => p.vi === w.vi)) continue;
    seenTerms.add(t);
    pairs.push(w);
    if (pairs.length >= MATCH_PAIRS) break;
  }
  // Xếp: dễ trước (chọn nghĩa), ghép ở giữa, nghe sau cùng — từ đã gặp ở đầu lượt quay lại dưới dạng khó hơn.
  const order = { nghia: 0, tu: 1, nghe: 2 } as const;
  const sorted = choice.slice().sort((a, b) => order[a.kind as keyof typeof order] - order[b.kind as keyof typeof order]);
  const items: LtItem[] = sorted;
  if (pairs.length >= 3) {
    const ghep: LtItem = {
      id: "ghep",
      kind: "ghep",
      pairs,
      rightOrder: shuffle(
        pairs.map((_, i) => i),
        rng,
      ),
      retry: 0,
    };
    items.splice(Math.min(6, items.length), 0, ghep);
  }
  return items;
}

/** Câu sai quay lại cuối hàng đợi (xáo phương án lại để không nhớ vị trí), tối đa MAX_RETRY lần. */
export function requeue(queue: LtItem[], item: LtItem, rng: Rng = Math.random): LtItem[] {
  if (item.kind === "ghep" || item.retry >= MAX_RETRY) return queue;
  const correct = item.options[item.answer];
  const options = shuffle(item.options, rng);
  return [...queue, { ...item, options, answer: options.indexOf(correct), retry: item.retry + 1 }];
}
