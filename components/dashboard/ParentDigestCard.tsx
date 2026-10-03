"use client";

import { useState } from "react";
import { Copy, MessageCircle, Sparkles } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { fetchMyScoreHistory, fetchMyTopicGaps } from "@/services/analytics";
import { fetchAttendanceForParent } from "@/services/parent-view";
import { fetchStudentAccount } from "@/services/student-account";
import { buildParentDigest } from "@/lib/parent-digest";
import { displayPhone } from "@/components/parent/TeacherContact";
import { CONTACT } from "@/lib/contact";
import { SITE_URL } from "@/lib/site";

const DAY = 24 * 60 * 60 * 1000;

/**
 * Thẻ "Tin Zalo cho phụ huynh" trong hồ sơ học sinh: soạn sẵn bản nháp tóm tắt từ số liệu thật, thầy sửa
 * rồi chép / mở Zalo của phụ huynh. Mục đích: phụ huynh nhận được điều cần biết ngay trong Zalo mà không
 * phải đăng nhập. Chưa tự gửi (cần Zalo OA/ZNS có phí) — thầy bấm gửi.
 */
export default function ParentDigestCard({ studentId, studentName }: { studentId: string; studentName: string }) {
  const toast = useToast();
  const [text, setText] = useState("");
  const [zaloPhone, setZaloPhone] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function compose() {
    setBusy(true);
    try {
      const [points, gaps, rows, account] = await Promise.all([
        fetchMyScoreHistory(studentId),
        fetchMyTopicGaps(studentId).catch(() => []),
        fetchAttendanceForParent(studentId),
        fetchStudentAccount(studentId).catch(() => null),
      ]);
      const worst = [...gaps].filter((g) => g.wrong > 0).sort((a, b) => b.wrong - a.wrong)[0];
      const now = new Date().getTime();
      const recent = (rows ?? []).filter(
        (r) => r.status !== null && now - new Date(`${r.date}T00:00:00`).getTime() <= 30 * DAY,
      );
      const attended = recent.filter((r) => r.status === "present" || r.status === "late").length;
      setText(
        buildParentDigest({
          studentName,
          points,
          worstTopic: worst && worst.topic !== "Chưa gắn chủ đề" ? worst.topic : null,
          attendance: rows === null ? null : { attended, total: recent.length, absent: recent.filter((r) => r.status === "absent").length },
          phone: displayPhone(CONTACT.phone),
          siteUrl: SITE_URL,
        }),
      );
      setZaloPhone(account?.parent_phone?.replace(/\D/g, "") || null);
    } catch {
      toast("error", "Chưa soạn được tin — thử lại sau.");
    } finally {
      setBusy(false);
    }
  }

  async function copy() {
    try {
      await navigator.clipboard.writeText(text);
      toast("success", "Đã chép tin — dán vào Zalo.");
    } catch {
      toast("error", "Không chép được, hãy bôi đen và chép tay.");
    }
  }

  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-5">
      <h4 className="flex items-center gap-2 font-display text-lg font-bold text-white">
        <MessageCircle size={18} aria-hidden /> Tin Zalo cho phụ huynh
      </h4>
      <p className="mt-1 text-sm text-slate-400">
        Soạn sẵn từ điểm, điểm danh và phần còn sai của em. Thầy đọc lại, sửa nếu cần rồi gửi.
      </p>
      <button
        type="button"
        onClick={compose}
        disabled={busy}
        className="mt-3 inline-flex items-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark disabled:opacity-60"
      >
        <Sparkles size={16} aria-hidden /> {busy ? "Đang soạn…" : text ? "Soạn lại" : "Soạn tin tuần này"}
      </button>
      {text && (
        <>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={10}
            className="mt-3 w-full rounded-xl border border-white/10 bg-black/20 p-3 text-sm text-white focus:border-primary focus:outline-none"
            aria-label="Nội dung tin Zalo gửi phụ huynh"
          />
          <div className="mt-2 flex flex-wrap gap-2">
            <button
              type="button"
              onClick={copy}
              className="inline-flex items-center gap-2 rounded-xl border border-white/15 px-4 py-2.5 text-sm font-semibold text-slate-200 hover:border-white/30"
            >
              <Copy size={16} aria-hidden /> Sao chép
            </button>
            {zaloPhone ? (
              <a
                href={`https://zalo.me/${zaloPhone}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-xl border border-white/15 px-4 py-2.5 text-sm font-semibold text-cyan-300 hover:border-white/30"
              >
                <MessageCircle size={16} aria-hidden /> Mở Zalo {zaloPhone}
              </a>
            ) : (
              <span className="self-center text-sm text-slate-400">Chưa có SĐT phụ huynh trong hồ sơ em.</span>
            )}
          </div>
        </>
      )}
    </section>
  );
}
