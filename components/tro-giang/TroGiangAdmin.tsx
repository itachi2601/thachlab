"use client";

import { useState } from "react";
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
      <div className="flex gap-2">
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
