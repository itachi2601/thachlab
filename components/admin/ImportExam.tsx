"use client";

import { useState } from "react";
import type { MultipleChoiceQuestion } from "@/features/exams/types";
import { parseExamLatex } from "@/services/exam-latex-parser";
import ExamEditor from "@/components/admin/ExamEditor";
import { useToast } from "@/components/ui/Toast";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

export default function ImportExam({
  cncBank,
  onDone,
}: {
  cncBank: { key: string; label: string }; // ngân hàng câu hỏi CNC sẽ bị thay thế toàn bộ bằng nội dung import
  onDone: () => void;
}) {
  const toast = useToast();
  const [latexText, setLatexText] = useState("");
  const [result, setResult] = useState<{ title: string; questions: MultipleChoiceQuestion[]; warnings: string[] } | null>(null);
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);

  function handleParseLatex() {
    if (!latexText.trim()) {
      toast("error", "Vui lòng nhập LaTeX content");
      return;
    }

    setBusy(true);
    try {
      const parsed = parseExamLatex(latexText);
      const questions = parsed.questions.filter((q): q is MultipleChoiceQuestion => q.type === "multiple_choice");
      const dropped = parsed.questions.length - questions.length;
      const warnings = dropped > 0
        ? [...parsed.warnings, `Đã bỏ qua ${dropped} câu không phải trắc nghiệm (ngân hàng CNC chỉ nhận trắc nghiệm 1 đáp án).`]
        : parsed.warnings;
      setResult({ title: parsed.title, questions, warnings });

      if (questions.length === 0) {
        toast("warning", "Không tìm thấy câu hỏi trắc nghiệm nào");
      } else {
        toast("success", `Đã parse ${questions.length} câu hỏi`);
      }
    } catch (err) {
      toast("error", `Lỗi parse: ${err instanceof Error ? err.message : err}`);
    } finally {
      setBusy(false);
    }
  }

  if (editing && result) {
    return (
      <ExamEditor
        exam={null}
        initialQuestions={result.questions}
        initialTitle={result.title}
        cncBank={cncBank}
        onDone={() => {
          setEditing(false);
          setResult(null);
          setLatexText("");
          onDone();
        }}
      />
    );
  }

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-orange-400/20 bg-orange-500/5 p-4">
        <p className="text-xs font-bold uppercase tracking-wide text-orange-300">Cập nhật ngân hàng câu hỏi CNC</p>
        <p className="mt-1 text-lg font-bold text-white">{cncBank.label}</p>
        <p className="mt-1 text-xs text-slate-400">Toàn bộ câu hỏi parse được từ LaTeX bên dưới sẽ thay thế ngân hàng này sau khi bạn xác nhận lưu ở bước tiếp theo.</p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Paste LaTeX câu hỏi trắc nghiệm
          </label>
          <textarea
            value={latexText}
            onChange={(e) => setLatexText(e.target.value)}
            placeholder={`\\section{Tên ngân hàng câu hỏi}

\\question{Loại: multiple_choice}
Câu 1: Định luật II Newton phát biểu rằng?
A) F = ma
B) F = mv
C) F = m/a
D) F = a/m
\\answer{A}
\\explanation{Đây là định luật II Newton}`}
            rows={12}
            className={`${inputCls} font-mono text-xs`}
          />
        </div>

        <button
          onClick={handleParseLatex}
          disabled={busy || !latexText.trim()}
          className={`w-full rounded-lg px-4 py-2.5 text-sm font-semibold transition-colors ${
            busy || !latexText.trim()
              ? "bg-slate-600/30 text-slate-500 cursor-not-allowed"
              : "bg-emerald-600/30 text-emerald-300 hover:bg-emerald-600/50"
          }`}
        >
          {busy ? "Đang parse..." : "✓ Parse LaTeX"}
        </button>

        {result && (
          <div className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-6">
            <div>
              <p className="font-medium text-white">
                <span className="text-cyan">{result.title}</span>
              </p>
              <p className="mt-1 text-sm text-slate-400">{result.questions.length} câu trắc nghiệm</p>
            </div>

            {result.warnings.length > 0 && (
              <ul className="space-y-1 rounded-lg border border-amber-500/30 bg-amber-500/5 p-3 text-sm text-amber-300">
                {result.warnings.map((w, i) => (
                  <li key={i}>⚠️ {w}</li>
                ))}
              </ul>
            )}

            {result.questions.length > 0 && (
              <button
                onClick={() => setEditing(true)}
                className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark"
              >
                Xem trước &amp; chỉnh sửa →
              </button>
            )}
          </div>
        )}

        <details className="text-xs text-slate-400">
          <summary className="cursor-pointer hover:text-slate-300">💡 Định dạng LaTeX</summary>
          <div className="mt-3 space-y-2 rounded-lg bg-white/5 p-3">
            <p className="font-semibold text-slate-300">Cấu trúc:</p>
            <ul className="space-y-1 pl-4 text-slate-400">
              <li>• <code className="text-slate-300">\section{'{'}Tên ngân hàng{'}'}</code> - Tiêu đề (không bắt buộc, có thể sửa lại ở bước sau)</li>
              <li>• <code className="text-slate-300">\question{'{'}Loại: multiple_choice{'}'}</code> - Bắt đầu 1 câu hỏi</li>
              <li>• <code className="text-slate-300">A) B) C) D)</code> - 4 đáp án</li>
              <li>• <code className="text-slate-300">\answer{'{'}A{'}'}</code> - Đáp án đúng</li>
              <li>• <code className="text-slate-300">\explanation{'{'}Giải thích{'}'}</code></li>
            </ul>
          </div>
        </details>
      </div>
    </div>
  );
}
