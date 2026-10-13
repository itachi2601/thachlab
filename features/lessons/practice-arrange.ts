import { pickRandom, type Difficulty } from "@/features/exams/types";

/**
 * Bốc + xếp câu cho MỌI chỗ tự luyện / bốc ngẫu nhiên (một nguồn duy nhất, đừng chép lại).
 *
 * Nguyên tắc (docs/LUYEN-DUNG-CHO-YEU.md): HS trung bình–yếu cần tỉ lệ đúng ~70–80% để còn muốn làm tiếp
 * (Wilson 2019; Vygotsky ZPD), câu đầu phải làm được (Bandura – thành công sớm; goal-gradient), đỉnh khó nằm
 * gần cuối rồi kết bằng câu vừa sức (peak–end, Kahneman 1993), không dồn ≥3 câu khó liền nhau.
 * Bốc ngẫu nhiên thuần cho 1 em yếu ~1/3 câu khó liên tiếp ở vị trí bất kỳ → chuỗi sai → bỏ giữa chừng.
 */
export type AbilityBand = "weak" | "mid" | "strong";

/** Tỉ lệ [dễ, trung bình, khó]; kỳ vọng đúng ≈ 0,75 với em yếu, ≈ 0,7 với em khá. */
export const MIX_BY_BAND: Record<AbilityBand, [number, number, number]> = {
  weak: [0.5, 0.4, 0.1],
  mid: [0.3, 0.5, 0.2],
  strong: [0.2, 0.5, 0.3],
};

type Diff<T> = (item: T) => Difficulty | undefined;

const defaultDiff = <T,>(item: T): Difficulty | undefined => (item as { question?: { difficulty?: Difficulty } }).question?.difficulty;

/** Câu chưa gắn mức xếp như trung bình. */
function tierOf<T>(item: T, diff: Diff<T>): 0 | 1 | 2 {
  const d = diff(item);
  return d === "de" ? 0 : d === "kho" ? 2 : 1;
}

/** Bốc `n` câu theo mix; thiếu tầng nào thì mượn tầng gần nhất (hoà → tầng dễ hơn). `prefer` đưa câu ưu tiên (chưa gặp, đến hạn ôn) lên trước trong tầng. */
export function pickByMix<T>(
  items: T[],
  n: number,
  band: AbilityBand,
  opts: { diff?: Diff<T>; prefer?: (item: T) => boolean } = {},
): T[] {
  const diff = opts.diff ?? defaultDiff;
  const total = Math.min(n, items.length);
  if (total <= 0) return [];
  const tiers: T[][] = [[], [], []];
  for (const it of items) tiers[tierOf(it, diff)].push(it);
  const ordered = tiers.map((t) =>
    opts.prefer ? [...pickRandom(t.filter(opts.prefer), t.length), ...pickRandom(t.filter((x) => !opts.prefer!(x)), t.length)] : pickRandom(t, t.length),
  );
  const mix = MIX_BY_BAND[band];
  const quota = mix.map((p) => Math.floor(p * total));
  // Chia phần dư (do làm tròn xuống) cho tầng có tỉ lệ lẻ lớn nhất.
  const order = [0, 1, 2].sort((a, b) => mix[b] * total - quota[b] - (mix[a] * total - quota[a]));
  for (let left = total - quota.reduce((a, b) => a + b, 0), i = 0; left > 0; left -= 1, i += 1) quota[order[i % 3]] += 1;
  const out: T[][] = [[], [], []];
  const used = [0, 0, 0];
  for (let t = 0; t < 3; t += 1) {
    const take = Math.min(quota[t], ordered[t].length);
    out[t] = ordered[t].slice(0, take);
    used[t] = take;
  }
  let short = total - used.reduce((a, b) => a + b, 0);
  // Thiếu: mượn tầng gần nhất còn câu (ưu tiên tầng trung bình/dễ hơn để không đẩy em yếu vào câu khó).
  const borrowOrder: Record<number, number[]> = { 0: [1, 2], 1: [0, 2], 2: [1, 0] };
  for (let t = 0; t < 3 && short > 0; t += 1) {
    for (const b of borrowOrder[t]) {
      if (short <= 0) break;
      const spare = ordered[b].slice(used[b], used[b] + short);
      out[b].push(...spare);
      used[b] += spare.length;
      short -= spare.length;
    }
  }
  return out.flat();
}

/**
 * Xếp thứ tự một bộ câu đã chọn: 2 câu dễ mở đầu (1 nếu bộ < 6), thang tăng dần, đỉnh khó sát cuối,
 * câu cuối là câu vừa sức; không có ≥3 câu khó liền. Bộ < 4 câu: chỉ xếp dễ → khó.
 */
export function arrangeForMotivation<T>(items: T[], diff: Diff<T> = defaultDiff): T[] {
  const n = items.length;
  const shuffled = pickRandom(items, n);
  const rank = (x: T) => tierOf(x, diff);
  const asc = [...shuffled].sort((a, b) => rank(a) - rank(b));
  if (n < 4) return asc;
  const opener = Math.min(n >= 6 ? 2 : 1, asc.filter((x) => rank(x) === 0).length);
  const head = asc.slice(0, opener);
  const rest = asc.slice(opener);
  // Câu kết: ưu tiên dễ, không thì trung bình; không lấy câu khó trừ khi chỉ còn câu khó.
  let endIdx = rest.findIndex((x) => rank(x) === 0);
  if (endIdx < 0) endIdx = rest.findIndex((x) => rank(x) === 1);
  if (endIdx < 0) endIdx = 0;
  const [tail] = rest.splice(endIdx, 1);
  // Giữa: câu nhẹ tăng dần, câu khó chèn rải về phía cuối (đỉnh ~70% bộ), không dồn thành chuỗi.
  const lights = rest.filter((x) => rank(x) < 2);
  const hards = rest.filter((x) => rank(x) === 2);
  const middle: T[] = [];
  let li = 0;
  hards.forEach((h, k) => {
    const cut = Math.floor(lights.length * Math.sqrt((k + 1) / (hards.length + 1)));
    while (li < cut) middle.push(lights[li++]);
    middle.push(h);
  });
  while (li < lights.length) middle.push(lights[li++]);
  return [...head, ...middle, tail];
}

/** Bốc theo năng lực rồi xếp: điểm vào duy nhất cho chỗ "bốc ngẫu nhiên N câu". */
export function pickAndArrange<T>(
  items: T[],
  n: number,
  band: AbilityBand,
  opts: { diff?: Diff<T>; prefer?: (item: T) => boolean } = {},
): T[] {
  return arrangeForMotivation(pickByMix(items, n, band, opts), opts.diff);
}

/** Mức thang của PracticeSession → nhóm năng lực (Dễ = em đang ở bậc đầu → "weak"). */
export function bandFromLadder(level: "de" | "trung-binh" | "kho"): AbilityBand {
  return level === "de" ? "weak" : level === "trung-binh" ? "mid" : "strong";
}

/** Dùng cho test/kiểm: đếm tầng dễ/TB/khó. */
export function tierCounts<T>(items: T[], diff: Diff<T> = defaultDiff): [number, number, number] {
  const c: [number, number, number] = [0, 0, 0];
  for (const it of items) c[tierOf(it, diff)] += 1;
  return c;
}
