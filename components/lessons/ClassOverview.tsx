"use client";

import Link from "next/link";
import type { LinkedChild } from "@/services/parent-links";
import "./class-overview.css";

/** Một dòng tiến độ cho phụ huynh. Học sinh thấy số của đúng bài đang học trên thẻ "Nên làm tiếp". */
export function ClassProgressLine({ completedItems, totalItems }: { completedItems: number; totalItems: number }) {
  if (totalItems <= 0) return null;
  return <p className="class-progress-line">{completedItems}/{totalItems} mục đã học</p>;
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
