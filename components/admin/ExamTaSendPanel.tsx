"use client";

import { useEffect, useState } from "react";
import { Check, Copy, UserCheck } from "lucide-react";
import { fetchClasses } from "@/services/classes";
import { fetchTaPreviewClassIds, setTaPreviewClasses, taPreviewPath } from "@/services/exam-ta-preview";
import { SITE_URL } from "@/lib/site";
import { useToast } from "@/components/ui/Toast";
import type { SchoolClass } from "@/features/exams/types";

/**
 * Khối "Gửi trợ giảng xem trước" cạnh mã QR của đề (trang Đăng đề + Sửa đề).
 * Chọn lớp rồi bấm Gửi → đề hiện ở /tro-giang/xem-truoc cho trợ giảng làm thử từng câu (có đáp án
 * ngay), xong thì sang trang Chữa bài của lớp đó. Đề vẫn ẩn với học sinh — chỉ ghi bảng exam_ta_previews.
 */
export default function ExamTaSendPanel({ examId }: { examId: number }) {
  const toast = useToast();
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [picked, setPicked] = useState<number[]>([]);
  const [sent, setSent] = useState<number[]>([]);
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    let cancelled = false;
    Promise.all([fetchClasses(), fetchTaPreviewClassIds(examId)])
      .then(([list, ids]) => {
        if (cancelled) return;
        setClasses(list);
        setPicked(ids);
        setSent(ids);
      })
      .catch(() => !cancelled && toast("error", "Không tải được danh sách lớp đã gửi trợ giảng."));
    return () => {
      cancelled = true;
    };
  }, [examId, toast]);

  const dirty = picked.length !== sent.length || picked.some((id) => !sent.includes(id));
  const link = `${SITE_URL}${taPreviewPath(examId, sent[0])}`;

  async function save() {
    setBusy(true);
    try {
      await setTaPreviewClasses(examId, picked);
      setSent(picked);
      toast("success", picked.length ? "Đã gửi đề cho trợ giảng xem trước." : "Đã thu hồi đề khỏi trợ giảng.");
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không gửi được cho trợ giảng.");
    } finally {
      setBusy(false);
    }
  }

  async function copy() {
    try {
      await navigator.clipboard.writeText(link);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1500);
    } catch {
      toast("error", "Không chép được link — chọn và chép tay.");
    }
  }

  return (
    <section className="admin-card space-y-3" aria-label="Gửi trợ giảng xem trước">
      <p className="inline-flex items-center gap-1.5 text-sm font-semibold text-slate-200">
        <UserCheck size={15} /> Gửi trợ giảng xem trước
      </p>
      <p className="text-xs text-slate-400">
        Trợ giảng làm thử từng câu, đáp án hiện ngay sau mỗi câu, làm xong tự sang trang Chữa bài của lớp. Học sinh không thấy.
      </p>
      <div className="flex flex-wrap gap-2">
        {classes.map((c) => {
          const on = picked.includes(c.id);
          return (
            <button
              key={c.id}
              type="button"
              aria-pressed={on}
              onClick={() => setPicked((cur) => (on ? cur.filter((id) => id !== c.id) : [...cur, c.id]))}
              className={`min-h-11 rounded-lg px-3 text-sm font-semibold ${on ? "bg-primary text-white" : "bg-white/5 text-slate-300 hover:bg-white/10"}`}
            >
              {c.name}
            </button>
          );
        })}
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <button type="button" onClick={save} disabled={busy || !dirty} className="admin-btn admin-btn--primary disabled:opacity-40">
          {busy ? "Đang lưu…" : picked.length ? "Gửi trợ giảng" : "Thu hồi"}
        </button>
        {sent.length > 0 && (
          <button type="button" onClick={copy} className="admin-btn inline-flex items-center gap-1">
            {copied ? <Check size={14} /> : <Copy size={14} />} Chép link cho trợ giảng
          </button>
        )}
      </div>
    </section>
  );
}
