"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";
import { fetchWrongTopicStats, type TopicStats } from "@/services/analytics";

interface Props {
  onTopicSelect?: (topic: string) => void;
}

export default function WrongTopicsTable({ onTopicSelect }: Props) {
  const { session } = useAuth();
  const [stats, setStats] = useState<TopicStats[] | null>(null);
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);

  useEffect(() => {
    if (!session?.user.id) return;
    fetchWrongTopicStats(session.user.id).then(setStats);
  }, [session?.user.id]);

  if (!stats) {
    return (
      <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-center">
        <p className="text-sm text-slate-400">Đang tải…</p>
      </div>
    );
  }

  if (stats.length === 0) {
    return (
      <div className="space-y-4">
        <div className="rounded-2xl border border-amber-500/30 bg-amber-500/5 p-6">
          <p className="text-lg font-semibold text-amber-300">
            Chờ dữ liệu phân tích 🔄
          </p>
          <p className="mt-2 text-sm text-slate-400">
            Tính năng này sẽ hiển thị các chủ đề em hay sai sau khi thầy/cô nhập chi tiết kết quả từng câu hỏi.
          </p>
          <p className="mt-3 text-xs text-slate-500">
            📚 Thầy/cô có thể tham khảo hướng dẫn trong file{" "}
            <code className="text-slate-400">docs/ANALYTICS-SETUP.md</code>
          </p>
        </div>
        <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/5 p-6 text-center">
          <p className="text-lg font-semibold text-emerald-300">
            Tuyệt vời! 🎉
          </p>
          <p className="mt-2 text-sm text-slate-400">
            Em chưa có câu sai nào, hoặc chưa có dữ liệu phân tích chi tiết.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <p className="text-sm text-slate-400">
        Dưới đây là các chủ đề em hay sai. Click để xem chi tiết và ôn tập lại.
      </p>
      <div className="overflow-x-auto rounded-2xl border border-white/10">
        <table className="w-full text-left text-sm">
          <thead className="bg-white/5 text-slate-400">
            <tr>
              <th className="px-4 py-3 font-medium">Chủ đề kiến thức</th>
              <th className="px-4 py-3 text-center font-medium">Tổng câu</th>
              <th className="px-4 py-3 text-center font-medium">Câu sai</th>
              <th className="px-4 py-3 text-center font-medium">% Sai</th>
              <th className="px-4 py-3 text-center font-medium">Hành động</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {stats.map((stat) => (
              <tr
                key={stat.topic}
                className="hover:bg-white/5 transition-colors"
              >
                <td className="px-4 py-3 font-medium text-white">
                  {stat.topic}
                </td>
                <td className="px-4 py-3 text-center text-slate-400">
                  {stat.total}
                </td>
                <td className="px-4 py-3 text-center">
                  <span className="font-semibold text-red-400">{stat.wrong}</span>
                </td>
                <td className="px-4 py-3 text-center">
                  <div className="flex items-center justify-center gap-2">
                    <div className="w-16 h-1.5 bg-white/10 rounded-full overflow-hidden">
                      <div
                        className={`h-full transition-all ${
                          stat.percentage >= 50
                            ? "bg-red-500"
                            : stat.percentage >= 30
                            ? "bg-amber-500"
                            : "bg-blue-500"
                        }`}
                        style={{ width: `${stat.percentage}%` }}
                      />
                    </div>
                    <span
                      className={`font-mono font-semibold w-10 text-right ${
                        stat.percentage >= 50
                          ? "text-red-400"
                          : stat.percentage >= 30
                          ? "text-amber-400"
                          : "text-blue-400"
                      }`}
                    >
                      {stat.percentage}%
                    </span>
                  </div>
                </td>
                <td className="px-4 py-3 text-center">
                  <button
                    onClick={() => {
                      setSelectedTopic(stat.topic);
                      onTopicSelect?.(stat.topic);
                    }}
                    className="inline-block rounded-full bg-blue-500/20 px-3 py-1.5 text-xs font-semibold text-blue-300 hover:bg-blue-500/30 transition-colors"
                  >
                    Ôn tập →
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {selectedTopic && (
        <div className="mt-4 p-4 rounded-2xl border border-blue-500/30 bg-blue-500/5">
          <p className="text-sm text-slate-300">
            💡 Chủ đề "<strong>{selectedTopic}</strong>" được chọn để ôn tập.
            Các bài ôn tập sẽ được cung cấp sớm.
          </p>
        </div>
      )}
    </div>
  );
}
