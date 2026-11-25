"use client";

import { useEffect, useState } from "react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import OnNamPhut, { type BoOnTap, type TheOn } from "@/components/lessons/OnNamPhut";
import { BO_ON_TAP } from "@/content/on-tap";
import { getSupabase } from "@/services/supabase";

/**
 * Ôn thẻ đến hạn (thử 25/11/2026): lịch giãn cách 1 → 3 → 7 → 21 → 60 ngày theo TỪNG thẻ (bảng on_tap_the,
 * RPC on_tap_den_han / on_tap_ghi). Thẻ của nhiều bài được TRỘN xen kẽ (interleaving) — tối đa 8 thẻ một lượt
 * (N5). Không điểm, không RP (L3). Chưa gắn link ở trang chủ: muốn hiện số thẻ đến hạn ở "/" phải gộp vào RPC
 * trang chủ, không thêm round-trip.
 */
type Row = { slug: string; the_id: string; tong_den_han: number };

function tronXenKe(nhom: TheOn[][]): TheOn[] {
  const out: TheOn[] = [];
  for (let i = 0; nhom.some((g) => i < g.length); i++) for (const g of nhom) if (i < g.length) out.push(g[i]);
  return out;
}

function OnTheDenHan() {
  const [bo, setBo] = useState<BoOnTap | null>(null);
  const [trong, setTrong] = useState(false);
  const [loi, setLoi] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      const { data, error } = await getSupabase().rpc("on_tap_den_han", { p_limit: 8 });
      if (error) return setLoi("Chưa tải được lịch ôn. Em thử lại sau ít phút.");
      const rows = (data ?? []) as Row[];
      const slugs = [...new Set(rows.map((r) => r.slug))].filter((s) => BO_ON_TAP[s]);
      const bos = await Promise.all(slugs.map((s) => BO_ON_TAP[s]()));
      const nhom = bos.map((b) => {
        const can = new Set(rows.filter((r) => r.slug === b.slug).map((r) => r.the_id));
        const ten = b.lesson_title.replace(/^Bài\s+(\d+)\..*$/, "Bài $1");
        return b.the.filter((t) => can.has(t.id)).map((t) => ({ ...t, slug: b.slug, bai: ten }));
      });
      const the = tronXenKe(nhom);
      if (the.length === 0) return setTrong(true);
      setBo({
        slug: "tron",
        lesson_title: `${the.length} thẻ đến hạn · ${nhom.filter((g) => g.length).length} bài`,
        the,
      });
    })();
  }, []);

  if (loi) return <p>{loi}</p>;
  if (trong)
    return (
      <section>
        <h1 style={{ fontSize: "1.3rem", fontWeight: 700 }}>Hôm nay chưa có thẻ đến hạn</h1>
        <p style={{ marginTop: 8 }}>Học xong bài nào thì làm “Ôn 5 phút” của bài đó — thẻ sẽ hẹn em quay lại đúng lúc sắp quên.</p>
      </section>
    );
  if (!bo) return <p>Đang tải thẻ…</p>;
  return <OnNamPhut bo={bo} tron />;
}

export default function OnThePage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-xl px-4 pt-24 pb-24 sm:px-5 sm:pt-28">
        <RequireAuth>
          <OnTheDenHan />
        </RequireAuth>
      </main>
      <Footer variant="app" />
    </>
  );
}
