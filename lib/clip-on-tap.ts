// Clip "ôn nhanh 90 giây" trước buổi ôn theo chặng (chặng D, docs/KE-HOACH-MOTION-GRAPHIC.md, thí điểm L12 Ch.3).
// Kho: content/phu-dao/clip-on/<id>.json — `video` do scripts/tai-clip-len-storage.mts --kho-dir ghi khi tải lên bucket.
// Buổi ôn chưa lưu mã chương nên khớp theo chữ trong tên buổi/tên chặng (không đổi DB); chương khác thêm một dòng vào RULES.
import c01 from "@/content/phu-dao/clip-on/on-l12-ch3.json";

export type ClipOn = { id: string; nhan: string; nhinVao: string; mp4: string; poster: string; giay: number };

type Kho = {
  id: string;
  nhan: string;
  nhin_vao: string;
  video?: { mp4?: string; poster?: string; giay?: number };
};

const ALL = new Map<string, ClipOn>(
  ([c01] as Kho[]).flatMap((k) =>
    k.video?.mp4 && k.video.poster
      ? [[k.id, { id: k.id, nhan: k.nhan, nhinVao: k.nhin_vao, mp4: k.video.mp4, poster: k.video.poster, giay: k.video.giay ?? 90 }] as const]
      : [],
  ),
);

// "Từ trường" nhưng không phải "điện từ trường" (Ch.4 L12).
const RULES: { id: string; re: RegExp }[] = [
  { id: "on-l12-ch3", re: /(?<!điện )từ trường|đường sức từ|lực từ|cảm ứng từ|từ thông/i },
];

/** Clip ôn cho một buổi ôn: khớp tên buổi hoặc ≥ 2 tên chặng; không khớp thì không hiện gì. */
export function clipOnForSession(title: string, stageTitles: string[]): ClipOn | null {
  for (const r of RULES) {
    const clip = ALL.get(r.id);
    if (!clip) continue;
    if (r.re.test(title) || stageTitles.filter((t) => r.re.test(t)).length >= 2) return clip;
  }
  return null;
}
