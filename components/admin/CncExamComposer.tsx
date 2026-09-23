"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import ExamSection, { compressRasterInputs } from "@/components/admin/ExamSection";
import { useToast } from "@/components/ui/Toast";
import { canonicalizeQuestionTopics } from "@/features/exams/types";
import { CNC_QUIZ_BANKS, fetchCncExamBankMeta, fetchCncExamRow, type CncExamBankMeta } from "@/services/cnc-exam-bank";
import { applyMediaToBundle, bundleToRows, validateBundle, type LessonBundle } from "@/services/lesson-import";
import { removeLessonMedia, uploadLessonMedia } from "@/services/lesson-media";
import { getSupabase } from "@/services/supabase";

const selectCls =
  "w-full rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white focus:border-primary focus:outline-none";

export default function CncExamComposer() {
  const toast = useToast();
  const [bankKey, setBankKey] = useState<string>(CNC_QUIZ_BANKS[0]?.key ?? "");
  const [bankMeta, setBankMeta] = useState<CncExamBankMeta[]>([]);
  const [examId, setExamId] = useState<number | null>(null);
  const [examBundle, setExamBundle] = useState<LessonBundle | null>(null);
  const [busy, setBusy] = useState(false);
  const [log, setLog] = useState<string[]>([]);
  const [doneLink, setDoneLink] = useState<string | null>(null);

  useEffect(() => {
    fetchCncExamBankMeta().then(setBankMeta).catch(() => undefined);
  }, []);

  useEffect(() => {
    setExamId(null);
    fetchCncExamRow(bankKey)
      .then((row) => setExamId(row?.id ?? null))
      .catch(() => setExamId(null));
  }, [bankKey]);

  const bank = CNC_QUIZ_BANKS.find((b) => b.key === bankKey) ?? null;
  const meta = bankMeta.find((b) => b.key === bankKey) ?? null;
  const questions = examBundle?.exam.questions ?? [];
  const check = examBundle ? validateBundle(examBundle) : null;
  const canPublish = !!examBundle && !!check?.ok && questions.length > 0 && !busy && !!examBundle.exam.title.trim();

  async function publish() {
    if (!examBundle || !bank) return;
    setBusy(true);
    setDoneLink(null);
    const steps: string[] = [];
    const push = (s: string) => {
      steps.push(s);
      setLog([...steps]);
    };
    const supabase = getSupabase();
    let uploadedPaths: string[] = [];
    try {
      let resolved = examBundle;
      const rasters = examBundle.raster_images ?? [];
      if (rasters.length) {
        push(`Nén & tải ${rasters.length} ảnh…`);
        // Ngân hàng CNC không gắn với 1 bài số (lesson_id) — dùng 0 làm thư mục media dùng chung.
        const media = await uploadLessonMedia(supabase, 0, await compressRasterInputs(rasters));
        uploadedPaths = media.map((m) => m.storagePath);
        resolved = applyMediaToBundle(examBundle, media);
        push(`  ✓ đã tải ${media.length} ảnh`);
      }
      resolved = {
        ...resolved,
        exam: { ...resolved.exam, questions: canonicalizeQuestionTopics(resolved.exam.questions, []) },
      };
      const rows = bundleToRows(resolved, 0);

      push(`Ghi ngân hàng "${bank.label}" (${rows.exam.questions.length} câu)…`);
      const payload = {
        cnc_key: bank.key,
        title: rows.exam.title || bank.label,
        duration_minutes: rows.exam.duration_minutes,
        published: false,
        subject_code: "cnc",
        topic: rows.exam.topic,
        difficulty: rows.exam.difficulty,
        questions: rows.exam.questions,
      };
      const { error } = await supabase.from("exams").upsert(payload, { onConflict: "cnc_key" });
      if (error) throw new Error(`Ghi ngân hàng lỗi: ${error.message}`);

      push("Xong.");
      setDoneLink("/lop-hoc/cnc");
      toast("success", "Đã đăng đề.");
      fetchCncExamBankMeta().then(setBankMeta).catch(() => undefined);
      fetchCncExamRow(bankKey).then((row) => setExamId(row?.id ?? null)).catch(() => undefined);
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      push(`✕ ${msg}`);
      if (uploadedPaths.length) {
        await removeLessonMedia(supabase, uploadedPaths).catch(() => {});
        push("Đã gỡ ảnh vừa tải lên.");
      }
      toast("error", msg);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6">
      <header>
        <p className="admin-lead" style={{ marginTop: 0 }}>
          Dán đề từ Word hoặc thả file .docx — trang tách câu và đáp án ngay khi gõ, y như Azota. Chọn ngân hàng CNC rồi
          bấm Đăng.
        </p>
      </header>

      <ExamSection subjectCode="cnc" topicGroups={[]} catalogNames={[]} lessonPicked={!!bank} onChange={setExamBundle} />

      <section className="space-y-4 rounded-2xl border border-white/10 bg-white/5 p-4">
        <div className="flex items-center gap-2">
          <span className="admin-badge admin-badge--accent">3</span>
          <span className="text-sm font-semibold text-white">Cấu hình & đăng</span>
        </div>

        <label className="block text-xs font-semibold text-slate-400">
          Ngân hàng đề CNC
          <select value={bankKey} onChange={(e) => setBankKey(e.target.value)} className={`${selectCls} mt-1`}>
            {CNC_QUIZ_BANKS.map((b) => (
              <option key={b.key} value={b.key}>
                {b.label}
              </option>
            ))}
          </select>
        </label>

        {meta && (
          <p className="text-xs text-slate-400">
            Hiện có {meta.questionCount} câu{!examId && " · chưa có dữ liệu"}. Đăng đề mới sẽ thay toàn bộ ngân hàng
            này.
          </p>
        )}

        {check && !check.ok && (
          <ul className="space-y-1 rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-xs text-red-200">
            {check.errors.map((e, i) => (
              <li key={i}>• {e}</li>
            ))}
          </ul>
        )}

        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={publish}
            disabled={!canPublish}
            className="rounded-xl bg-primary px-5 py-2.5 text-sm font-bold text-white shadow-lg shadow-primary/20 hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {busy ? "Đang đăng…" : "Đăng đề"}
          </button>
          {doneLink && (
            <Link href={doneLink} target="_blank" className="text-sm font-semibold text-emerald-300 underline">
              Mở trang học CNC để kiểm tra →
            </Link>
          )}
        </div>

        {log.length > 0 && (
          <pre className="max-h-48 overflow-auto whitespace-pre-wrap rounded-xl bg-black/40 p-3 text-xs text-slate-300">
            {log.join("\n")}
          </pre>
        )}
      </section>
    </div>
  );
}
