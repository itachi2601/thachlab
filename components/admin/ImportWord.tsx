"use client";

import { useState } from "react";
import type { ExamQuestion } from "@/features/exams/types";
import { parseWordHtml, type ParseResult } from "@/features/exams/wordImport";
import ExamEditor from "@/components/admin/ExamEditor";
import { getSupabase } from "@/services/supabase";
import { useToast } from "@/components/ui/Toast";

const TYPE_COUNT_LABELS: Record<ExamQuestion["type"], string> = {
  multiple_choice: "trắc nghiệm",
  true_false: "đúng/sai",
  short_answer: "trả lời ngắn",
};

export default function ImportWord() {
  const toast = useToast();
  const [busy, setBusy] = useState(false);
  const [fileName, setFileName] = useState("");
  const [result, setResult] = useState<ParseResult | null>(null);
  const [editing, setEditing] = useState(false);

  async function handleFile(file: File) {
    setBusy(true);
    setResult(null);
    setEditing(false);
    setFileName(file.name);
    try {
      const mammoth = (await import("mammoth")).default;
      const supabase = getSupabase();
      const stamp = Date.now();
      let imgIndex = 0;

      const { value: html, messages } = await mammoth.convertToHtml(
        { arrayBuffer: await file.arrayBuffer() },
        {
          convertImage: mammoth.images.imgElement(async (image) => {
            const b64 = await image.readAsBase64String();
            const contentType = image.contentType || "image/png";
            const ext = contentType.split("/")[1]?.split("+")[0] || "png";
            // WMF/EMF (MathType cũ) trình duyệt không hiển thị được
            if (ext === "x-wmf" || ext === "x-emf" || ext === "wmf" || ext === "emf") {
              return { src: "", alt: "[công thức MathType — cần Claude xử lý trên máy]" };
            }
            const path = `word-import/${stamp}-${imgIndex++}.${ext}`;
            const bytes = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
            const { error } = await supabase.storage
              .from("exam-images")
              .upload(path, bytes.buffer, { contentType });
            if (error) return { src: "" };
            const { data } = supabase.storage
              .from("exam-images")
              .getPublicUrl(path);
            return { src: data.publicUrl, alt: "" };
          }),
        },
      );

      const parsed = parseWordHtml(html);
      const mammothWarnings = messages
        .filter(
          (m) =>
            m.type === "warning" &&
            !m.message.includes("Unrecognised paragraph style"),
        )
        .slice(0, 3)
        .map((m) => `Word: ${m.message}`);
      // cảnh báo nếu file chứa equation OLE (mammoth bỏ qua)
      if (html.includes("MathType — cần Claude")) {
        parsed.warnings.unshift(
          "Đề chứa công thức MathType (ảnh WMF) — trình duyệt không đọc được. Hãy thả file vào Downloads và nhờ Claude nhập trên máy.",
        );
      }
      setResult({
        questions: parsed.questions,
        warnings: [...parsed.warnings, ...mammothWarnings],
      });
      if (parsed.questions.length > 0)
        toast("success", `Đã đọc ${parsed.questions.length} câu từ ${file.name}`);
    } catch (err) {
      toast("error", `Không đọc được file: ${err instanceof Error ? err.message : err}`);
    } finally {
      setBusy(false);
    }
  }

  if (editing && result) {
    return (
      <ExamEditor
        exam={null}
        initialQuestions={result.questions}
        onDone={() => {
          setEditing(false);
          setResult(null);
          setFileName("");
        }}
      />
    );
  }

  const counts = (result?.questions ?? []).reduce(
    (acc, q) => {
      acc[q.type] = (acc[q.type] ?? 0) + 1;
      return acc;
    },
    {} as Record<ExamQuestion["type"], number>,
  );

  return (
    <div className="space-y-6">
      <label
        className={`flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-white/15 bg-[#0B1020] px-6 py-12 text-center transition-colors hover:border-[#3B82F6]/60 ${
          busy ? "pointer-events-none opacity-60" : ""
        }`}
      >
        <input
          type="file"
          accept=".docx"
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) handleFile(f);
            e.target.value = "";
          }}
        />
        <span className="text-3xl">📄</span>
        <span className="mt-3 font-display text-lg font-semibold text-white">
          {busy ? "Đang đọc đề…" : "Chọn file Word (.docx)"}
        </span>
        <span className="mt-2 max-w-md text-sm text-slate-400">
          Hệ thống nhận diện 3 dạng câu hỏi: trắc nghiệm A/B/C/D (&ldquo;Đáp án:
          A&rdquo; hoặc đánh dấu *), đúng/sai 4 ý a-d, và trả lời ngắn. Ảnh trong
          đề tự động tải lên hệ thống.
        </span>
      </label>

      {result && (
        <div className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-6">
          <p className="font-medium text-white">
            {fileName}:{" "}
            <span className="text-[#22D3EE]">
              {result.questions.length} câu
            </span>{" "}
            <span className="text-sm text-slate-400">
              (
              {Object.entries(counts)
                .map(([t, n]) => `${n} ${TYPE_COUNT_LABELS[t as ExamQuestion["type"]]}`)
                .join(" · ") || "không có"}
              )
            </span>
          </p>

          {result.warnings.length > 0 && (
            <ul className="space-y-1 rounded-xl border border-amber-500/30 bg-amber-500/5 p-3 text-sm text-amber-300">
              {result.warnings.map((w, i) => (
                <li key={i}>⚠ {w}</li>
              ))}
            </ul>
          )}

          {result.questions.length > 0 && (
            <button
              onClick={() => setEditing(true)}
              className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#1D4ED8]"
            >
              Xem trước &amp; chỉnh sửa →
            </button>
          )}
        </div>
      )}
    </div>
  );
}
