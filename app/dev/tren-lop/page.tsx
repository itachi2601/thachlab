import type { Metadata } from "next";

/**
 * BẢN CHIẾU TRÊN LỚP (tivi 50") — mục lục: https://thachlab.id.vn/dev/tren-lop
 * Mỗi bài là file HTML tĩnh trong public/dev/tren-lop/<slug>.html, sinh bằng
 * content/lesson-samples/<slug>/build_tren_lop.py (skill .claude/skills/ban-chieu-tren-lop).
 * Thêm bài mới: chạy build của bài đó rồi thêm một dòng vào BAI dưới đây.
 */
export const metadata: Metadata = { title: "Bản chiếu trên lớp", robots: { index: false, follow: false } };

const BAI: { slug: string; ten: string; ghiChu: string }[] = [
  { slug: "l11-dien-the", ten: "Vật lí 11 · Bài 20 · Điện thế", ghiChu: "22 màn · cuối tiết đề 1215 (QR)" },
];

export default function TrenLopDevPage() {
  return (
    <main className="min-h-screen bg-bg px-4 py-8 text-ink">
      <div className="mx-auto max-w-2xl">
        <h1 className="text-2xl font-bold">Bản chiếu trên lớp</h1>
        <p className="mt-2 text-muted">
          Mở trên máy nối tivi, bấm F11. Enter/→ sang màn, ← lùi; clip tự dừng ở mốc, Enter chạy tiếp.
        </p>
        <ul className="mt-6 space-y-3">
          {BAI.map((b) => (
            <li key={b.slug} className="rounded-xl border border-line p-4">
              <div className="font-semibold">{b.ten}</div>
              <div className="text-sm text-muted">{b.ghiChu}</div>
              <div className="mt-3 flex flex-wrap gap-3">
                <a className="rounded-lg bg-primary px-4 py-2 font-semibold text-white" href={`/dev/tren-lop/${b.slug}.html`}>
                  Mở bản chiếu
                </a>
                <a className="rounded-lg border border-line px-4 py-2" href={`/dev/tren-lop/${b.slug}-ghi-chu.html`}>
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
