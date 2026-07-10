"use client";

import { useState } from "react";
import type { ExamQuestion } from "@/features/exams/types";
import { parseExamLatex, type ExamParseResult } from "@/services/exam-latex-parser";
import { parseAzotaIframe, formatAzotaEmbed } from "@/services/azota-formatter";
import ExamEditor from "@/components/admin/ExamEditor";
import { useToast } from "@/components/ui/Toast";

const TYPE_COUNT_LABELS: Record<ExamQuestion["type"], string> = {
  multiple_choice: "trắc nghiệm",
  true_false: "đúng/sai",
  short_answer: "trả lời ngắn",
};

export default function ImportExam() {
  const toast = useToast();
  const [mode, setMode] = useState<"latex" | "azota">("latex");
  const [latexText, setLatexText] = useState("");
  const [result, setResult] = useState<ExamParseResult | null>(null);
  const [azotaEmbed, setAzotaEmbed] = useState<{ src: string; title: string } | null>(null);
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
      setResult(parsed);

      if (parsed.questions.length === 0) {
        toast("warning", "Không tìm thấy câu hỏi nào");
      } else {
        toast("success", `Đã parse ${parsed.questions.length} câu hỏi`);
      }
    } catch (err) {
      toast("error", `Lỗi parse: ${err instanceof Error ? err.message : err}`);
    } finally {
      setBusy(false);
    }
  }

  function handleParseAzota() {
    if (!latexText.trim()) {
      toast("error", "Vui lòng nhập iframe code từ AZOTA");
      return;
    }

    setBusy(true);
    try {
      const options = parseAzotaIframe(latexText);
      const embed = { src: options.src, title: options.title ?? "AZOTA Exercise" };
      setAzotaEmbed(embed);
      toast("success", `Đã nhận diện AZOTA: "${embed.title}"`);
    } catch (err) {
      toast("error", `Lỗi: ${err instanceof Error ? err.message : err}`);
    } finally {
      setBusy(false);
    }
  }

  // Show LaTeX preview
  if (editing && result && mode === "latex") {
    return (
      <ExamEditor
        exam={null}
        initialQuestions={result.questions}
        initialTitle={result.title}
        onDone={() => {
          setEditing(false);
          setResult(null);
          setLatexText("");
        }}
      />
    );
  }

  // Show AZOTA preview
  if (editing && azotaEmbed && mode === "azota") {
    return (
      <ExamEditor
        exam={null}
        initialTitle={azotaEmbed.title}
        initialAzotaEmbed={azotaEmbed}
        onDone={() => {
          setEditing(false);
          setAzotaEmbed(null);
          setLatexText("");
        }}
      />
    );
  }

  const inputCls =
    "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-[#3B82F6] focus:outline-none";

  return (
    <div className="space-y-6">
      {/* Mode Tabs */}
      <div className="flex gap-2 border-b border-white/10">
        <button
          onClick={() => {
            setMode("latex");
            setResult(null);
            setAzotaEmbed(null);
          }}
          className={`px-4 py-3 text-sm font-semibold transition-colors ${
            mode === "latex"
              ? "border-b-2 border-[#2563EB] text-white"
              : "text-slate-400 hover:text-slate-300"
          }`}
        >
          📐 LaTeX
        </button>
        <button
          onClick={() => {
            setMode("azota");
            setResult(null);
            setAzotaEmbed(null);
          }}
          className={`px-4 py-3 text-sm font-semibold transition-colors ${
            mode === "azota"
              ? "border-b-2 border-[#2563EB] text-white"
              : "text-slate-400 hover:text-slate-300"
          }`}
        >
          🔗 AZOTA
        </button>
      </div>

      {/* LaTeX Mode */}
      {mode === "latex" && (
        <div className="space-y-4">
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Paste LaTeX exam format
            </label>
            <textarea
              value={latexText}
              onChange={(e) => setLatexText(e.target.value)}
              placeholder={`\\section{Đề kiểm tra Vật lý 10}

\\question{Loại: multiple_choice}
Câu 1: Định luật II Newton phát biểu rằng?
A) F = ma
B) F = mv
C) F = m/a
D) F = a/m
\\answer{A}
\\explanation{Đây là định luật II Newton}

\\question{Loại: true_false}
Câu 2: Xác định đúng/sai
a) Lực là đại lượng vector - ĐÚNG
b) Lực có thể âm - SAI
c) Khối lượng không đổi - ĐÚNG
d) Gia tốc ngược chiều lực - SAI
\\answer{a, c}
\\explanation{Lực là vector, khối lượng không đổi trong cơ học cổ điển}

\\question{Loại: short_answer}
Câu 3: Tính gia tốc của vật khối lượng 2 kg dưới lực 10 N?
\\answer{5 m/s²}
\\explanation{a = F/m = 10/2 = 5 m/s²}`}
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

          {/* LaTeX Preview */}
          {result && (
            <div className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-6">
              <div>
                <p className="font-medium text-white">
                  <span className="text-[#22D3EE]">{result.title}</span>
                </p>
                <p className="mt-1 text-sm text-slate-400">
                  {result.questions.length} câu
                  {result.questions.length > 0 && (
                    <>
                      {" "}
                      <span className="text-xs">
                        (
                        {Object.entries(
                          result.questions.reduce(
                            (acc, q) => {
                              acc[q.type] = (acc[q.type] ?? 0) + 1;
                              return acc;
                            },
                            {} as Record<ExamQuestion["type"], number>,
                          ),
                        )
                          .map(
                            ([t, n]) =>
                              `${n} ${TYPE_COUNT_LABELS[t as ExamQuestion["type"]]}`,
                          )
                          .join(" · ")}
                        )
                      </span>
                    </>
                  )}
                </p>
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
                  className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#1D4ED8]"
                >
                  Xem trước &amp; chỉnh sửa →
                </button>
              )}
            </div>
          )}

          {/* Help */}
          <details className="text-xs text-slate-400">
            <summary className="cursor-pointer hover:text-slate-300">
              💡 Định dạng LaTeX
            </summary>
            <div className="mt-3 space-y-2 rounded-lg bg-white/5 p-3">
              <p className="font-semibold text-slate-300">Cấu trúc:</p>
              <ul className="space-y-1 pl-4 text-slate-400">
                <li>• <code className="text-slate-300">\section{'{'}Tên đề{'}'}</code> - Tiêu đề đề thi</li>
                <li>• <code className="text-slate-300">\question{'{'}Loại: multiple_choice{'}'}</code> - Bắt đầu câu hỏi</li>
                <li>• <code className="text-slate-300">A) B) C) D)</code> - 4 option (trắc nghiệm)</li>
                <li>• <code className="text-slate-300">a) b) c) d)</code> - 4 ý (đúng/sai)</li>
                <li>• <code className="text-slate-300">\answer{'{'}A{'}'}</code> hoặc <code className="text-slate-300">\answer{'{'}a,c{'}'}</code></li>
                <li>• <code className="text-slate-300">\explanation{'{'}Giải thích{'}'}</code></li>
              </ul>
              <p className="mt-2 font-semibold text-slate-300">Loại câu hỏi:</p>
              <ul className="space-y-1 pl-4 text-slate-400">
                <li>• <code className="text-slate-300">multiple_choice</code> hoặc <code className="text-slate-300">trắc nghiệm</code> hoặc <code className="text-slate-300">A/B/C/D</code></li>
                <li>• <code className="text-slate-300">true_false</code> hoặc <code className="text-slate-300">đúng/sai</code> hoặc <code className="text-slate-300">4 ý</code></li>
                <li>• <code className="text-slate-300">short_answer</code> - Trả lời ngắn (mặc định)</li>
              </ul>
            </div>
          </details>
        </div>
      )}

      {/* AZOTA Mode */}
      {mode === "azota" && (
        <div className="space-y-4">
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Paste iframe code từ AZOTA
            </label>
            <textarea
              value={latexText}
              onChange={(e) => setLatexText(e.target.value)}
              placeholder={`<iframe width="100%" height="900" src="https://azota.vn/de-thi/ezkjlr" title="[26-27] 12 KTTX tuần 1" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe>`}
              rows={6}
              className={`${inputCls} font-mono text-xs`}
            />
          </div>

          <button
            onClick={handleParseAzota}
            disabled={busy || !latexText.trim()}
            className={`w-full rounded-lg px-4 py-2.5 text-sm font-semibold transition-colors ${
              busy || !latexText.trim()
                ? "bg-slate-600/30 text-slate-500 cursor-not-allowed"
                : "bg-blue-600/30 text-blue-300 hover:bg-blue-600/50"
            }`}
          >
            {busy ? "Đang kiểm tra..." : "✓ Nhúng AZOTA"}
          </button>

          {/* AZOTA Preview */}
          {azotaEmbed && (
            <div className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-6">
              <div>
                <p className="font-medium text-white">
                  <span className="text-[#22D3EE]">{azotaEmbed.title}</span>
                </p>
                <p className="mt-1 text-sm text-slate-400">
                  📌 Link: <code className="text-xs text-slate-500">{azotaEmbed.src}</code>
                </p>
                <p className="mt-2 text-xs text-slate-500">
                  💡 Toàn bộ đề sẽ nhúng từ AZOTA. Học sinh làm trực tiếp trên AZOTA.
                </p>
              </div>

              <div className="max-h-96 overflow-y-auto rounded-lg border border-white/5 bg-white/5 p-3">
                <p className="mb-2 text-xs font-semibold text-slate-300">Preview:</p>
                <div dangerouslySetInnerHTML={{ __html: formatAzotaEmbed(azotaEmbed) }} />
              </div>

              <button
                onClick={() => setEditing(true)}
                className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#1D4ED8]"
              >
                Xem trước &amp; chỉnh sửa →
              </button>
            </div>
          )}

          {/* Help */}
          <details className="text-xs text-slate-400">
            <summary className="cursor-pointer hover:text-slate-300">
              💡 Cách lấy iframe từ AZOTA
            </summary>
            <div className="mt-3 space-y-2 rounded-lg bg-white/5 p-3">
              <ol className="space-y-1 pl-4 text-slate-400">
                <li>1. Vào <code className="text-slate-300">azota.vn</code> → Tìm bài tập/đề</li>
                <li>2. Click "Chia sẻ" hoặc "Nhúng" → Copy iframe code</li>
                <li>3. Dán vào field trên</li>
                <li>4. Click "✓ Nhúng AZOTA"</li>
              </ol>
            </div>
          </details>
        </div>
      )}
    </div>
  );
}
