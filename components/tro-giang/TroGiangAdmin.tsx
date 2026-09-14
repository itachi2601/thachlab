"use client";

import { useState } from "react";
import Link from "next/link";
import { Drama } from "lucide-react";
import { setTaDemoMode } from "@/lib/tro-giang/demo";
import AdminMonthlyTable from "./AdminMonthlyTable";
import AdminSessionQueue from "./AdminSessionQueue";
import AdminTeamHours from "./AdminTeamHours";
import AdminVideoTab from "./AdminVideoTab";

const TABS = [
  { id: "buoi", label: "Buổi làm việc" },
  { id: "video", label: "Video TikTok" },
] as const;

type TabId = (typeof TABS)[number]["id"];

export default function TroGiangAdmin() {
  const [tab, setTab] = useState<TabId>("buoi");
  const [reloadKey, setReloadKey] = useState(0);

  return (
    <div className="space-y-6">
      <Link href="/tro-giang/quy-che" className="block rounded-xl border border-blue-400/25 bg-blue-500/5 p-3 text-sm text-blue-200">Quy chế mới từ 01/10/2026 · tháng 10 chưa giảm lương · xem chi tiết</Link>
      <div className="flex flex-wrap items-center gap-2">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setTab(t.id)}
            className={`rounded-xl px-4 py-2 text-sm font-bold transition ${
              tab === t.id ? "bg-[#2563EB] text-white" : "bg-white/5 text-slate-300 hover:bg-white/10"
            }`}
          >
            {t.label}
          </button>
        ))}

        {/* Mở giao diện trợ giảng với một hồ sơ giả lập — không đọc/ghi dữ liệu thật. */}
        <Link
          href="/tro-giang?gialap=1"
          onClick={() => setTaDemoMode(true)}
          className="ml-auto flex items-center gap-2 rounded-xl border border-fuchsia-400/30 bg-fuchsia-500/10 px-4 py-2 text-sm font-bold text-fuchsia-200 transition hover:border-fuchsia-400/60"
        >
          <Drama size={15} />
          Xem trước giao diện trợ giảng
        </Link>
      </div>

      {tab === "buoi" ? (
        <div className="space-y-8">
          <section>
            <h2 className="mb-3 font-display text-lg font-bold text-white">Hàng chờ duyệt</h2>
            <AdminSessionQueue onChanged={() => setReloadKey((k) => k + 1)} />
          </section>

          <section>
            <h2 className="mb-3 font-display text-lg font-bold text-white">Tổng hợp tháng</h2>
            <AdminMonthlyTable reloadKey={reloadKey} />
          </section>

          <section>
            <h2 className="mb-3 font-display text-lg font-bold text-white">Giờ của cả đội</h2>
            <AdminTeamHours reloadKey={reloadKey} />
          </section>
        </div>
      ) : (
        <AdminVideoTab reloadKey={reloadKey} />
      )}
    </div>
  );
}
