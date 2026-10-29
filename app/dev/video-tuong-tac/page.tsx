"use client";

import { useState } from "react";
import VideoThiNghiemKhung, {
  type VideoKhungData,
  type VideoKhungEvent,
} from "@/components/lessons/VideoThiNghiemKhung";
import boyle from "@/content/thi-nghiem/video-khung/tn-l12-boylecharles-01.json";
import chuyenthe from "@/content/thi-nghiem/video-khung/tn-l12-chuyenthe-01.json";
import camungdt from "@/content/thi-nghiem/video-khung/tn-l12-camungdt-01.json";

/**
 * XEM THỬ video thí nghiệm + khung sáu ô + dừng ở câu Dự đoán (bản thử 29/10/2026).
 * Mở http://localhost:3000/dev/video-tuong-tac. Chỉ có nghĩa ở máy dev; sự kiện chỉ in ra bảng bên dưới,
 * chưa ghi DB (muốn đo tỉ lệ dừng/chọn/xem lại thì nối onEvent vào bảng ghi sau khi thầy chốt).
 */
const CLIPS = [boyle, chuyenthe, camungdt] as VideoKhungData[];

export default function VideoTuongTacPreviewPage() {
  const [log, setLog] = useState<string[]>([]);
  const onEvent = (id: string) => (e: VideoKhungEvent) =>
    setLog((l) => [`${new Date().toLocaleTimeString("vi-VN")} · ${id} · ${JSON.stringify(e)}`, ...l].slice(0, 12));

  return (
    <main className="mx-auto max-w-5xl space-y-8 px-4 py-8">
      <header>
        <h1 className="font-display text-2xl font-bold text-ink">Video thí nghiệm bán tương tác — bản thử</h1>
        <p className="mt-1 text-[15px] text-muted">
          Khung sáu ô sáng theo giây của video; video tự dừng một lần ở câu Dự đoán. Thử tua qua câu Dự đoán, bấm ô đã
          mở để xem lại, và thu cửa sổ xuống 375px để xem dải bước trên điện thoại.
        </p>
      </header>
      {CLIPS.map((c) => (
        <VideoThiNghiemKhung key={c.id} data={c} onEvent={onEvent(c.id)} />
      ))}
      <section className="rounded-2xl border border-line bg-panel p-4">
        <h2 className="mb-2 text-[15px] font-bold text-ink">Sự kiện gần nhất</h2>
        <pre className="whitespace-pre-wrap text-[13px] text-muted">{log.length ? log.join("\n") : "Chưa có."}</pre>
      </section>
    </main>
  );
}
