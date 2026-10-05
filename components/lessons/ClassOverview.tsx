"use client";

import Link from "next/link";
import type { RankStatus } from "@/features/rank/types";
import type { LinkedChild } from "@/services/parent-links";
import "./class-overview.css";

interface StatsProps {
  completedItems: number;
  totalItems: number;
  doneLessons: number;
  totalLessons: number;
  rank: RankStatus | null;
}

/** Dải số liệu đầu trang chương (A1): luôn lấy từ dữ liệu trang đã tải + 1 RPC rank, không query thêm. */
export function ClassStatsStrip({ completedItems, totalItems, doneLessons, totalLessons, rank }: StatsProps) {
  const percent = totalItems > 0 ? Math.round((completedItems / totalItems) * 100) : 0;
  const streak = rank?.daily?.streak ?? null;
  return (
    <div className="class-stats" role="list" aria-label="Tóm tắt tiến độ">
      <div className="class-stat" role="listitem">
        <b>{percent}%</b>
        <span>Tiến độ · {completedItems}/{totalItems} mục</span>
      </div>
      <div className="class-stat" role="listitem">
        <b>{doneLessons}/{totalLessons}</b>
        <span>Bài đã học xong</span>
      </div>
      {rank?.season && (
        <div className="class-stat" role="listitem">
          <b>{rank.rp} RP</b>
          <span>{rank.tier?.name ?? "Điểm rank mùa này"}</span>
        </div>
      )}
      {streak !== null && (
        <div className="class-stat" role="listitem">
          <b>{streak} ngày</b>
          <span>Chuỗi ngày học liên tiếp</span>
        </div>
      )}
    </div>
  );
}

interface ParentBandProps {
  childList: LinkedChild[];
  selectedId: string;
  onSelect: (studentId: string) => void;
}

/** Băng nhận diện phụ huynh (A4): nói rõ đang xem tiến độ của ai, chỉ xem, và lối sang trang kết quả đầy đủ. */
export function ParentBand({ childList, selectedId, onSelect }: ParentBandProps) {
  const selected = childList.find((c) => c.studentId === selectedId) ?? childList[0];
  return (
    <div className="class-parent-band" role="status">
      <p>
        Bạn đang xem tiến độ học của <b>{selected.fullName}</b>. Phụ huynh chỉ xem được tiến độ, không mở bài giảng.
      </p>
      {childList.length > 1 && (
        <label>
          <span className="sr-only">Chọn con</span>
          <select value={selected.studentId} onChange={(e) => onSelect(e.target.value)} aria-label="Chọn con">
            {childList.map((c) => (
              <option key={c.studentId} value={c.studentId}>{c.fullName}</option>
            ))}
          </select>
        </label>
      )}
      <Link href="/phu-huynh">Xem kết quả đầy đủ của con</Link>
    </div>
  );
}

/** Dải chấm theo mục của một bài (C1): mỗi chấm một mục, đặc = đã xong. */
export function ItemDots({ done }: { done: boolean[] }) {
  if (done.length === 0) return null;
  const shown = done.slice(0, 10);
  const doneCount = done.filter(Boolean).length;
  return (
    <span className="class-dots" role="img" aria-label={`${doneCount}/${done.length} mục đã xong`}>
      {shown.map((d, i) => (
        <i key={i} className={d ? "is-done" : ""} />
      ))}
    </span>
  );
}
