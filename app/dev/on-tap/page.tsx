"use client";

import { useEffect, useState } from "react";
import { TheoryBlock } from "@/app/lop-hoc/bai/_parts/TheoryBlock";
import { flashTheorySection } from "@/app/lop-hoc/bai/_parts/lesson-nav";
import OnNamPhut, { cuonToiTieuMuc, type BoOnTap } from "@/components/lessons/OnNamPhut";
import type { LessonItem } from "@/features/lessons/types";

/**
 * XEM THỬ "Ôn 5 phút" (thử 25/11/2026, L11 bài 22–24): thẻ ôn ở trên, bài lý thuyết (bản đã rút bài toán mẫu)
 * ở dưới để nút "Ôn ngay" có chỗ cuộn tới. Mở http://localhost:3000/dev/on-tap?bai=22 (22 | 23 | 24).
 * Chỉ có nghĩa ở máy dev; không ghi RP/độ sâu đọc.
 */
type Nap = () => Promise<[{ default: unknown }, { default: { theory_html: string } }]>;
// Import tường minh từng file (không dùng template literal để bundler không gói cả 120 bundle.json).
const BAI: Record<string, Nap> = {
  "22": () =>
    Promise.all([
      import("@/content/on-tap/l11-cuong-do-dong-dien.json"),
      import("@/content/lesson-samples/l11-cuong-do-dong-dien/bundle.json"),
    ]),
  "23": () =>
    Promise.all([
      import("@/content/on-tap/l11-dien-tro-dinh-luat-ohm.json"),
      import("@/content/lesson-samples/l11-dien-tro-dinh-luat-ohm/bundle.json"),
    ]),
  "24": () =>
    Promise.all([
      import("@/content/on-tap/l11-nguon-dien.json"),
      import("@/content/lesson-samples/l11-nguon-dien/bundle.json"),
    ]),
};
const ITEM_ID = 999101;

export default function OnTapPreviewPage() {
  // null = chưa chọn: lần đầu lấy ?bai= trên URL (đọc trong effect để HTML tĩnh và lần hydrate khớp nhau).
  const [bai, setBai] = useState<string | null>(null);
  const [data, setData] = useState<{ bai: string; bo: BoOnTap; theory: string } | null>(null);

  useEffect(() => {
    const q = new URLSearchParams(window.location.search).get("bai");
    const k = bai ?? (q && BAI[q] ? q : "22");
    BAI[k]().then(([on, b]) => setData({ bai: k, bo: on.default as BoOnTap, theory: b.default.theory_html }));
  }, [bai]);
  const cur = data?.bai ?? bai;

  return (
    <main className="lesson-shell lesson-page" style={{ padding: "16px" }}>
      <nav style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        {Object.keys(BAI).map((k) => (
          <button
            key={k}
            type="button"
            onClick={() => {
              setData(null);
              setBai(k);
              window.history.replaceState(null, "", `?bai=${k}`);
            }}
            style={{ fontWeight: k === cur ? 700 : 400, minHeight: 44, padding: "0 12px" }}
          >
            Bài {k}
          </button>
        ))}
      </nav>
      {data ? (
        <>
          <OnNamPhut
            key={data.bai}
            bo={data.bo}
            theoryHtml={data.theory}
            theoryItemId={ITEM_ID}
            onOnNgay={(id, tieuMuc) => {
              flashTheorySection(id);
              cuonToiTieuMuc(id, tieuMuc);
            }}
          />
          <div style={{ marginTop: 24 }}>
            <TheoryBlock
              key={data.bai}
              item={{ id: ITEM_ID, title: "Lý thuyết", body_html: data.theory } as unknown as LessonItem}
              defaultOpen
              hideTitle
              done={false}
              loggedIn={false}
              onDone={() => {}}
              recordProgress={false}
            />
          </div>
        </>
      ) : (
        <p>Đang tải…</p>
      )}
    </main>
  );
}
