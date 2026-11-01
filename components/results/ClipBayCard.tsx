import type { ClipBay } from "@/lib/clip-bay";

/**
 * Clip "bẫy hay sai" trong thẻ mục phụ đạo. V5: chỉ ảnh bìa + nút phát của trình duyệt (`preload="none"`, không JS, không
 * gợi ý video khác — V9/G2). Không RP, không đếm "đã xem" (SDT; KE-HOACH-MOTION-GRAPHIC mục 1). Clip 9:16 → khung hẹp
 * ≤ 200 px để thẻ không dài quá màn 375 px; dòng "Nhìn vào" giữ lại vì clip trôi qua là mất (V8, Leahy & Sweller 2011).
 */
export function ClipBayCard({ clip }: { clip: ClipBay }) {
  return (
    <figure className="mt-3 flex flex-col gap-3 rounded-xl border border-line bg-surface-2 p-3 sm:flex-row sm:items-start">
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
        <p className="text-[13px] font-bold uppercase tracking-wide text-muted">🎬 Vì sao hay sai · {clip.giay} giây</p>
        <p className="mt-1 font-semibold text-ink">{clip.nhan}</p>
        <p className="mt-2 text-muted">
          <strong className="text-ink">Nhìn vào:</strong> {clip.nhinVao}
        </p>
        <p className="mt-2 text-[13px] text-muted">Tới câu hỏi, tự chọn trước khi thanh đếm chạy hết.</p>
      </figcaption>
    </figure>
  );
}
