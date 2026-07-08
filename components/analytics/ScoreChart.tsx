"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/components/auth/AuthProvider";
import { fetchScoreHistory, type ScorePoint } from "@/services/analytics";

export default function ScoreChart() {
  const { session } = useAuth();
  const [points, setPoints] = useState<ScorePoint[] | null>(null);

  useEffect(() => {
    if (!session?.user.id) return;
    fetchScoreHistory(session.user.id).then(setPoints);
  }, [session?.user.id]);

  if (!points) {
    return (
      <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-center">
        <p className="text-sm text-slate-400">Đang tải…</p>
      </div>
    );
  }

  if (points.length === 0) {
    return (
      <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-center">
        <p className="text-sm text-slate-400">Em chưa làm bài kiểm tra nào.</p>
      </div>
    );
  }

  // Tính min, max, avg
  const scores = points.map((p) => p.score);
  const minScore = Math.min(...scores);
  const maxScore = Math.max(...scores);
  const avgScore = Math.round((scores.reduce((a, b) => a + b, 0) / scores.length) * 100) / 100;

  // Tính chiều cao các bar (normalize to 0-100 scale)
  const chartHeight = 200;
  const barWidth = Math.max(30, Math.min(60, 400 / points.length));
  const chartWidth = points.length * (barWidth + 8) + 40;

  return (
    <div className="space-y-4">
      <div className="flex items-end justify-between">
        <div>
          <h3 className="font-display text-lg font-semibold text-white">
            Xu hướng điểm số
          </h3>
          <p className="mt-1 text-sm text-slate-400">
            Biểu đồ điểm qua {points.length} bài kiểm tra
          </p>
        </div>
        <div className="flex gap-6 text-sm">
          <div>
            <p className="text-slate-400">Cao nhất</p>
            <p className="text-lg font-bold text-emerald-400">
              {maxScore.toLocaleString("vi-VN")}
            </p>
          </div>
          <div>
            <p className="text-slate-400">Trung bình</p>
            <p className="text-lg font-bold text-blue-400">
              {avgScore.toLocaleString("vi-VN")}
            </p>
          </div>
          <div>
            <p className="text-slate-400">Thấp nhất</p>
            <p className="text-lg font-bold text-red-400">
              {minScore.toLocaleString("vi-VN")}
            </p>
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="overflow-x-auto rounded-2xl border border-white/10 bg-[#0B1020] p-6">
        <svg
          width={chartWidth}
          height={chartHeight + 60}
          className="min-w-full"
          viewBox={`0 0 ${chartWidth} ${chartHeight + 60}`}
        >
          {/* Y-axis labels */}
          <text x="25" y="20" fontSize="12" fill="#94a3b8" textAnchor="end">
            10
          </text>
          <text x="25" y={chartHeight / 2 + 5} fontSize="12" fill="#94a3b8" textAnchor="end">
            5
          </text>
          <text x="25" y={chartHeight + 10} fontSize="12" fill="#94a3b8" textAnchor="end">
            0
          </text>

          {/* Grid lines */}
          <line
            x1="30"
            y1="15"
            x2={chartWidth - 10}
            y2="15"
            stroke="#1e293b"
            strokeDasharray="4"
          />
          <line
            x1="30"
            y1={chartHeight / 2}
            x2={chartWidth - 10}
            y2={chartHeight / 2}
            stroke="#1e293b"
            strokeDasharray="4"
          />
          <line
            x1="30"
            y1={chartHeight + 5}
            x2={chartWidth - 10}
            y2={chartHeight + 5}
            stroke="#1e293b"
            strokeDasharray="4"
          />

          {/* Bars */}
          {points.map((point, i) => {
            const x = 40 + i * (barWidth + 8);
            const barHeight = (point.score / 10) * chartHeight;
            const y = chartHeight + 5 - barHeight;
            const isRecent = i === points.length - 1;

            return (
              <g key={i}>
                <rect
                  x={x}
                  y={y}
                  width={barWidth}
                  height={barHeight}
                  fill={
                    point.score >= 7
                      ? "#10b981"
                      : point.score >= 5
                      ? "#f59e0b"
                      : "#ef4444"
                  }
                  rx="4"
                  opacity={isRecent ? 1 : 0.8}
                  className="hover:opacity-100 transition-opacity cursor-help"
                >
                  <title>{`${point.examTitle}\n${point.score} điểm\n${point.date}`}</title>
                </rect>
                {/* Score label on top */}
                <text
                  x={x + barWidth / 2}
                  y={y - 5}
                  fontSize="12"
                  fontWeight="bold"
                  fill="white"
                  textAnchor="middle"
                >
                  {point.score.toLocaleString("vi-VN")}
                </text>
              </g>
            );
          })}

          {/* X-axis labels (dates) */}
          {points.map((point, i) => {
            if (i % Math.ceil(points.length / 5) === 0 || i === points.length - 1) {
              const x = 40 + i * (barWidth + 8) + barWidth / 2;
              return (
                <text
                  key={`date-${i}`}
                  x={x}
                  y={chartHeight + 25}
                  fontSize="11"
                  fill="#94a3b8"
                  textAnchor="middle"
                >
                  {point.date}
                </text>
              );
            }
          })}
        </svg>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-4 text-sm text-slate-400">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-emerald-500" />
          <span>≥ 7 điểm (Tốt)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-amber-500" />
          <span>5-7 điểm (Trung bình)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-red-500" />
          <span>{'< 5'} điểm (Cần cải thiện)</span>
        </div>
      </div>
    </div>
  );
}
