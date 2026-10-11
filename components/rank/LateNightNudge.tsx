"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/components/auth/auth-context";

const KEY = "thachlab-khuya-nhac";

/** Giờ Việt Nam (UTC+7) của thời điểm hiện tại, tính theo giờ + phút/60. */
function vnHour(d = new Date()) {
  return (d.getUTCHours() + 7 + d.getUTCMinutes() / 60) % 24;
}

/** Từ 23:00 đến 04:30 giờ Việt Nam. */
function isLate() {
  const h = vnHour();
  return h >= 23 || h < 4.5;
}

/** Ngày "đêm học" (trước 04:30 vẫn tính là đêm của hôm trước) để nhớ em đã bấm tắt. */
function nightId() {
  return new Date(Date.now() + 7 * 3600_000 - 5 * 3600_000).toISOString().slice(0, 10);
}

/**
 * Lời nhắc nghỉ ngơi cho học sinh học khuya. Chỉ là lời nhắn — KHÔNG đổi RP, chuỗi hay bất cứ điểm nào
 * (thầy chốt 11/10/2026: nhắc yêu thương, không phạt theo giờ).
 */
export default function LateNightNudge({ className = "" }: { className?: string }) {
  const { profile } = useAuth();
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (profile?.role !== "student" || !isLate()) return;
    try {
      if (sessionStorage.getItem(KEY) === nightId()) return;
    } catch {
      /* không có sessionStorage thì vẫn hiện */
    }
    setShow(true);
  }, [profile?.role]);

  if (!show) return null;

  return (
    <div
      role="note"
      className={`rounded-2xl border border-line bg-panel p-4 sm:p-5 ${className}`}
    >
      <p className="text-base font-semibold text-ink">Đã khuya rồi con ạ 🌙</p>
      <p className="mt-2 text-sm leading-relaxed text-muted">
        Thầy biết con đang rất cố gắng để hoàn thành bài tập. Nhưng con nhớ giữ gìn sức khoẻ để
        mai còn đi học nữa nhé.
      </p>
      <p className="mt-2 text-sm leading-relaxed text-muted">
        Con còn một chặng đường dài phía trước. Nghỉ ngơi và học tập hợp lý nhé con.
      </p>
      <button
        type="button"
        onClick={() => {
          setShow(false);
          try {
            sessionStorage.setItem(KEY, nightId());
          } catch {
            /* bỏ qua */
          }
        }}
        className="mt-3 min-h-11 rounded-xl border border-line px-4 text-sm font-semibold text-ink hover:border-line-strong"
      >
        Con biết rồi ạ
      </button>
    </div>
  );
}
