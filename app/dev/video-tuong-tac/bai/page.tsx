"use client";

import { useEffect, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";

/**
 * XEM THỬ lý thuyết thật của 3 bài L12 có khung video tương tác, đi qua đúng ContentHtml như trang học sinh
 * (bài thật cần đăng nhập nên không mở được ở máy dev). Mở http://localhost:3000/dev/video-tuong-tac/bai?bai=boyle
 * (boyle | chuyen-the | cam-ung). HTML lấy từ content/lesson-samples/<slug>/bundle.json; chỉ có nghĩa ở máy dev.
 */
const BAI: Record<string, () => Promise<{ default: { theory_html: string } }>> = {
  boyle: () => import("@/content/lesson-samples/l12-boyle-charles/bundle.json"),
  "chuyen-the": () => import("@/content/lesson-samples/l12-su-chuyen-the/bundle.json"),
  "cam-ung": () => import("@/content/lesson-samples/l12-cam-ung-dien-tu/bundle.json"),
};

export default function BaiThatPreviewPage() {
  const [html, setHtml] = useState<string | null>(null);
  const [bai, setBai] = useState("boyle");
  useEffect(() => {
    const b = new URLSearchParams(location.search).get("bai") ?? "boyle";
    (BAI[b] ?? BAI.boyle)().then((m) => {
      setBai(b);
      setHtml(m.default.theory_html);
    });
  }, []);
  return (
    <main className="mx-auto max-w-3xl px-4 py-6">
      <p className="mb-4 text-[13px] text-muted">
        Xem thử bài: {bai} ·{" "}
        {Object.keys(BAI).map((k) => (
          <a key={k} href={`?bai=${k}`} className="mr-2 underline">
            {k}
          </a>
        ))}
      </p>
      {html ? <ContentHtml html={html} /> : <p>Đang tải…</p>}
    </main>
  );
}
