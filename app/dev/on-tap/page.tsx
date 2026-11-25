"use client";

import { useEffect, useMemo, useState } from "react";
import { TheoryBlock } from "@/app/lop-hoc/bai/_parts/TheoryBlock";
import { flashTheorySection } from "@/app/lop-hoc/bai/_parts/lesson-nav";
import OnNamPhut, { cuonToiTieuMuc, type BoOnTap } from "@/components/lessons/OnNamPhut";
import OnNamPhutGon from "@/components/lessons/OnNamPhutGon";
import { BO_ON_TAP } from "@/content/on-tap";
import { getSupabase, supabaseConfigured } from "@/services/supabase";
import type { LessonItem } from "@/features/lessons/types";

/**
 * XEM THỬ "Ôn 5 phút" cho MỌI bài có bộ thẻ (đọc từ content/on-tap/index.ts, file sinh tự động).
 * Mở http://localhost:3000/dev/on-tap?bai=<slug>  (ví dụ ?bai=l11-nguon-dien). Lý thuyết bên dưới lấy từ DB
 * (mục ly_thuyet của lesson_id) để nút "Ôn ngay" có chỗ cuộn tới; không tải được thì chỉ hiện thẻ.
 * Chỉ có nghĩa ở máy dev; không ghi RP/độ sâu đọc.
 */
const SLUGS = Object.keys(BO_ON_TAP);
const LOP = ["l10", "l11", "l12"];

export default function OnTapPreviewPage() {
  const [slug, setSlug] = useState<string | null>(null);
  const [data, setData] = useState<{ slug: string; bo: BoOnTap; theory?: string; itemId?: number } | null>(null);

  useEffect(() => {
    const q = new URLSearchParams(window.location.search).get("bai");
    const k = slug ?? (q && BO_ON_TAP[q] ? q : SLUGS[0]);
    let huy = false;
    void (async () => {
      const bo = await BO_ON_TAP[k]();
      let theory: string | undefined;
      let itemId: number | undefined;
      if (supabaseConfigured && bo.lesson_id) {
        const { data: it } = await getSupabase()
          .from("lesson_items")
          .select("id, body_html")
          .eq("lesson_id", bo.lesson_id)
          .eq("kind", "ly_thuyet")
          .order("sort_order")
          .limit(1)
          .maybeSingle();
        if (it) {
          theory = it.body_html ?? undefined;
          itemId = it.id;
        }
      }
      if (!huy) setData({ slug: k, bo, theory, itemId });
    })();
    return () => {
      huy = true;
    };
  }, [slug]);
  const cur = data?.slug ?? slug;
  const nhom = useMemo(() => LOP.map((l) => [l, SLUGS.filter((s) => s.startsWith(`${l}-`))] as const), []);

  return (
    <main className="lesson-shell lesson-page" style={{ padding: "16px" }}>
      <label style={{ display: "block", marginBottom: 12 }}>
        Bài ({SLUGS.length} bộ):{" "}
        <select
          value={cur ?? ""}
          onChange={(e) => {
            setData(null);
            setSlug(e.target.value);
            window.history.replaceState(null, "", `?bai=${e.target.value}`);
          }}
          style={{ minHeight: 44, maxWidth: "100%" }}
        >
          {nhom.map(([l, ss]) => (
            <optgroup key={l} label={l.toUpperCase()}>
              {ss.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
      </label>
      {data ? (
        <>
          {/* Thẻ thu gọn y như cuối mục Lý thuyết ở /lop-hoc/bai (bấm Bắt đầu mới nạp JSON). */}
          {!!data.bo.lesson_id && (
            <div style={{ marginBottom: 24 }}>
              <OnNamPhutGon key={`gon-${data.slug}`} lessonId={data.bo.lesson_id} theoryHtml={data.theory} theoryItemId={data.itemId ?? 999101} />
            </div>
          )}
          <OnNamPhut
            key={data.slug}
            bo={data.bo}
            theoryHtml={data.theory}
            theoryItemId={data.itemId}
            onOnNgay={(id, tieuMuc) => {
              flashTheorySection(id);
              cuonToiTieuMuc(id, tieuMuc);
            }}
          />
          {data.theory && data.itemId != null && (
            <div style={{ marginTop: 24 }}>
              <TheoryBlock
                key={data.slug}
                item={{ id: data.itemId, title: "Lý thuyết", body_html: data.theory } as unknown as LessonItem}
                defaultOpen
                hideTitle
                done={false}
                loggedIn={false}
                onDone={() => {}}
                recordProgress={false}
              />
            </div>
          )}
        </>
      ) : (
        <p>Đang tải…</p>
      )}
    </main>
  );
}
