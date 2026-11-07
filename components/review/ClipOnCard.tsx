import type { ClipOn } from "@/lib/clip-on-tap";

/**
 * Thẻ "Ôn nhanh 90 giây trước khi làm" ở buổi ôn theo chặng. V5: chỉ ảnh bìa + nút phát của trình duyệt (`preload="none"`,
 * không JS, không tự phát, không chặn nút vào làm chặng). Clip 9:16 → khung ≤ 200 px để thẻ không dài quá màn 375 px.
 * Không RP, không đếm "đã xem" (KE-HOACH-MOTION-GRAPHIC mục 1).
 */
export default function ClipOnCard({ clip }: { clip: ClipOn }) {
  return (
    <figure className="flex flex-col gap-3 rounded-2xl border border-line bg-panel p-4 sm:flex-row sm:items-start">
      <div className="relative mx-auto aspect-[9/16] w-full max-w-[200px] shrink-0 overflow-hidden rounded-lg bg-black sm:mx-0">
        <video
          src={clip.mp4}
          poster={clip.poster}
          controls
          preload="none"
          playsInline
          title={clip.nhan}
          className="absolute inset-0 h-full w-full object-contain"
        />
      </div>
      <figcaption className="min-w-0 text-sm">
        <p className="text-[13px] font-bold uppercase tracking-wide text-muted">🎬 Ôn nhanh · {clip.giay} giây</p>
        <p className="mt-1 text-base font-semibold text-ink">{clip.nhan}</p>
        <p className="mt-2 text-muted">{clip.nhinVao}</p>
        <p className="mt-2 text-[13px] text-muted">Xem hay không tuỳ em — vào làm chặng 1 bất cứ lúc nào.</p>
      </figcaption>
    </figure>
  );
}
