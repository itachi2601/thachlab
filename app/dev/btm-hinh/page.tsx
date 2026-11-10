"use client";

import { useEffect, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import { Hinh } from "@/components/lessons/cong-cu/GiaiCungHinh";
import { apDong } from "@/components/lessons/cong-cu/Dong";
import type { LessonWorkedQuestion } from "@/features/lessons/types";

/**
 * Bảng soát hình "một dạng — một hình" (5/11/2026) — chỉ ở máy dev. Mỗi dạng có `cong_cu`: hình dưới đề (lớp 0), hình sau
 * từng bước (lớp 1..n), và 3 khung của mỗi `dong` (đầu · giữa · gần cuối). Khối #kiem liệt kê chữ tràn khung hình / hai chữ
 * đè nhau, để agent đọc bằng Chrome headless `--dump-dom` rồi mới chụp `--screenshot`.
 *   npx tsx scripts/publish-bai-tap-mau.mts --lesson 10 --xem-thu   → public/xem-thu/btm-10.json
 *   http://localhost:3000/dev/btm-hinh?f=btm-10[&d=3]   (d = chỉ một dạng, 1-based)
 */
export default function BtmHinhPage() {
  const [qs, setQs] = useState<LessonWorkedQuestion[] | null>(null);
  const [kiem, setKiem] = useState("…");
  const [only, setOnly] = useState<number | null>(null);
  useEffect(() => {
    const sp = new URLSearchParams(location.search);
    const f = sp.get("f");
    const d = Number(sp.get("d"));
    fetch(`/xem-thu/${f && /^[\w-]+$/.test(f) ? f : "btm"}.json`, { cache: "no-store" })
      .then((r) => r.json())
      .then((j) => {
        if (d) setOnly(d);
        setQs(j.questions);
      });
  }, []);
  useEffect(() => {
    if (!qs) return;
    const t = setTimeout(() => {
      const out: string[] = [];
      document.querySelectorAll<HTMLElement>("[data-khung]").forEach((box) => {
        const svg = box.querySelector("svg");
        if (!svg) return;
        const vb = svg.getBoundingClientRect();
        const rs = [...svg.querySelectorAll("text")]
          .map((t) => ({ t: t.textContent ?? "", r: t.getBoundingClientRect() }))
          .filter((x) => x.t.trim() && x.r.width > 0);
        for (const x of rs)
          if (x.r.left < vb.left - 1 || x.r.right > vb.right + 1 || x.r.top < vb.top - 1 || x.r.bottom > vb.bottom + 1)
            out.push(`TRAN ${box.dataset.khung}: "${x.t}"`);
        for (let i = 0; i < rs.length; i++)
          for (let j = i + 1; j < rs.length; j++) {
            const a = rs[i].r,
              b = rs[j].r;
            const w = Math.min(a.right, b.right) - Math.max(a.left, b.left),
              h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
            if (w > 2 && h > 2) out.push(`DE ${box.dataset.khung}: "${rs[i].t}" × "${rs[j].t}"`);
          }
      });
      setKiem(out.length ? out.join("\n") : "SACH");
    }, 1500);
    return () => clearTimeout(t);
  }, [qs, only]);
  return (
    <main className="lesson-shell lesson-page" style={{ padding: 12 }}>
      <pre id="kiem" style={{ whiteSpace: "pre-wrap", fontSize: 12 }}>
        {kiem}
      </pre>
      {qs?.map((q, k) =>
        !q.cong_cu || (only && only !== k + 1) ? null : (
          <section key={k} style={{ marginBottom: 28, "--cc-halo": "var(--color-panel)" } as React.CSSProperties}>
            <h2 style={{ fontWeight: 700, margin: "8px 0" }}>{q.label}</h2>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, 360px)", gap: 12 }}>
              <Khung ten={`D${k + 1} đề`} sub="dưới đề (lớp 0)">
                <Hinh tool={q.cong_cu} layer={0} step={0} />
              </Khung>
              {(q.buoc ?? []).map((b, i) => (
                <Khung key={i} ten={`D${k + 1} b${i + 1}`} sub={`sau bước ${i + 1}: ${b.tieu_de}`}>
                  <Hinh tool={q.cong_cu!} layer={i + 1} step={i} />
                </Khung>
              ))}
              {(q.cong_cu.dong ?? []).flatMap((d, j) =>
                [0, 0.5, 0.97].map((t) => (
                  <Khung key={`${j}-${t}`} ten={`D${k + 1} dong${j + 1} t${t}`} sub={`${d.nut} · ${d.buoc ? `bước ${d.buoc}` : "dưới đề"} · t=${t}`}>
                    <Hinh tool={apDong(q.cong_cu!, d, t)} layer={d.buoc ? d.buoc - 1 : 0} step={d.buoc ? d.buoc - 1 : 0} />
                  </Khung>
                )),
              )}
            </div>
          </section>
        ),
      )}
    </main>
  );
}

function Khung({ ten, sub, children }: { ten: string; sub: string; children: React.ReactNode }) {
  return (
    <div data-khung={ten} style={{ width: 360, border: "1px solid var(--color-line)", borderRadius: 8, padding: 6, background: "var(--color-panel)" }}>
      <div style={{ fontSize: 11, color: "var(--color-muted)" }}>
        <b>{ten}</b> · <ContentHtml html={sub} className="inline" />
      </div>
      <div style={{ height: 230 }} className="[&_.cc-fig]:!h-[230px]">
        {children}
      </div>
    </div>
  );
}
