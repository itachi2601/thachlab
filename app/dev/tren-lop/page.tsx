import type { Metadata } from "next";
import { BAN_CHIEU_TREN_LOP, linkBanChieu, linkGhiChuDay } from "@/features/lessons/tren-lop";

/**
 * BẢN CHIẾU TRÊN LỚP (tivi 50") — mục lục: https://thachlab.id.vn/dev/tren-lop
 * Mỗi bài là file HTML tĩnh trong public/dev/tren-lop/<slug>.html, sinh bằng
 * content/lesson-samples/<slug>/build_tren_lop.py (skill .claude/skills/ban-chieu-tren-lop).
 * Thêm bài mới: chạy build của bài đó rồi thêm một dòng vào features/lessons/tren-lop.ts.
 */
export const metadata: Metadata = { title: "Bản chiếu trên lớp", robots: { index: false, follow: false } };


export default function TrenLopDevPage() {
  return (
    <main className="min-h-screen bg-bg px-4 py-8 text-ink">
      <div className="mx-auto max-w-2xl">
        <h1 className="text-2xl font-bold">Bản chiếu trên lớp</h1>
        <p className="mt-2 text-muted">
          Mở trên máy nối tivi, bấm F11. Enter/→ sang màn, ← lùi; clip tự dừng ở mốc, Enter chạy tiếp.
        </p>
        <ul className="mt-6 space-y-3">
          {BAN_CHIEU_TREN_LOP.map((b) => (
            <li key={b.slug} className="rounded-xl border border-line p-4">
              <div className="font-semibold">{b.ten}</div>
              <div className="text-sm text-muted">{b.ghiChu}</div>
              <div className="mt-3 flex flex-wrap gap-3">
                <a className="rounded-lg bg-primary px-4 py-2 font-semibold text-white" href={linkBanChieu(b.slug)}>
                  Mở bản chiếu
                </a>
                <a className="rounded-lg border border-line px-4 py-2" href={linkGhiChuDay(b.slug)}>
                  Ghi chú dạy
                </a>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
