"use client";

import { useState } from "react";
import { latexToHtml, validateLatexSyntax } from "@/services/latex-converter";
import { parseAzotaIframe, formatAzotaEmbed } from "@/services/azota-formatter";

interface Props {
  value: string;
  onChange: (html: string, latex?: string) => void;
  placeholder?: string;
}

export default function LaTexEditor({ value, onChange, placeholder }: Props) {
  const initialMode = value.includes("<") && value.includes(">") ? "html" : "latex";
  const [mode, setMode] = useState<"latex" | "azota" | "html">(initialMode);
  const [latexText, setLatexText] = useState(value);
  const [htmlPreview, setHtmlPreview] = useState("");
  const [errors, setErrors] = useState<string[]>([]);
  const [showPreview, setShowPreview] = useState(false);

  function handleLatexChange(text: string) {
    setLatexText(text);

    // Validate
    const validation = validateLatexSyntax(text);
    setErrors(validation.errors);

    // Convert to HTML for preview
    if (validation.valid) {
      const result = latexToHtml(text);
      setHtmlPreview(result.html);
    }
  }

  function handleConvert() {
    const validation = validateLatexSyntax(latexText);
    if (!validation.valid) {
      setErrors(validation.errors);
      return;
    }

    const result = latexToHtml(latexText);
    onChange(result.html, latexText);
    setMode("html");
  }

  function handleHtmlChange(text: string) {
    setLatexText(text);
    onChange(text, text); // Keep same value for HTML
  }

  function handleAzotaEmbed() {
    try {
      const options = parseAzotaIframe(latexText);
      const html = formatAzotaEmbed(options);
      onChange(html);
      setMode("html");
      setErrors([]);
    } catch (err) {
      setErrors([err instanceof Error ? err.message : "Lỗi không xác định"]);
    }
  }

  const inputCls =
    "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-[#3B82F6] focus:outline-none";

  return (
    <div className="space-y-3">
      {/* Mode Toggle */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setMode("latex")}
            className={`rounded-lg px-3 py-1.5 text-sm font-semibold transition-colors ${
              mode === "latex"
                ? "bg-[#2563EB] text-white"
                : "bg-white/5 text-slate-400 hover:bg-white/10"
            }`}
          >
            📐 LaTeX
          </button>
          <button
            onClick={() => setMode("azota")}
            className={`rounded-lg px-3 py-1.5 text-sm font-semibold transition-colors ${
              mode === "azota"
                ? "bg-[#2563EB] text-white"
                : "bg-white/5 text-slate-400 hover:bg-white/10"
            }`}
          >
            🔗 AZOTA
          </button>
          <button
            onClick={() => setMode("html")}
            className={`rounded-lg px-3 py-1.5 text-sm font-semibold transition-colors ${
              mode === "html"
                ? "bg-[#2563EB] text-white"
                : "bg-white/5 text-slate-400 hover:bg-white/10"
            }`}
          >
            ♯ HTML
          </button>
        </div>
        {mode === "latex" && (
          <button
            onClick={() => setShowPreview(!showPreview)}
            className="text-xs text-slate-400 hover:text-slate-200 transition-colors"
          >
            {showPreview ? "✓ Preview On" : "Preview Off"}
          </button>
        )}
      </div>

      {/* LaTeX Mode */}
      {mode === "latex" && (
        <div className="space-y-2">
          <textarea
            value={latexText}
            onChange={(e) => handleLatexChange(e.target.value)}
            placeholder={
              placeholder ||
              `Viết LaTeX content ở đây…

\\section{Tiêu đề chính}
Nội dung bài học…

\\subsection{Tiêu đề phụ}
Giải thích thêm…

\\textbf{In đậm} và $x^2 + y^2 = z^2$

\\begin{itemize}
\\item Điểm 1
\\item Điểm 2
\\end{itemize}`
            }
            rows={8}
            className={`${inputCls} w-full font-mono`}
          />

          {/* Errors */}
          {errors.length > 0 && (
            <div className="rounded-lg border border-red-500/30 bg-red-500/5 p-3">
              <p className="text-xs font-semibold text-red-300">❌ Lỗi cú pháp:</p>
              <ul className="mt-1 space-y-1">
                {errors.map((err, i) => (
                  <li key={i} className="text-xs text-red-200">
                    • {err}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Preview */}
          {showPreview && errors.length === 0 && htmlPreview && (
            <div className="rounded-lg border border-blue-500/30 bg-blue-500/5 p-4">
              <p className="mb-2 text-xs font-semibold text-blue-300">👁️ Preview:</p>
              <div
                className="prose prose-invert max-w-none text-sm text-slate-300"
                dangerouslySetInnerHTML={{ __html: htmlPreview }}
              />
            </div>
          )}

          {/* Convert Button */}
          <button
            onClick={handleConvert}
            disabled={errors.length > 0}
            className={`w-full rounded-lg px-4 py-2 text-sm font-semibold transition-colors ${
              errors.length > 0
                ? "bg-slate-600/30 text-slate-500 cursor-not-allowed"
                : "bg-emerald-600/30 text-emerald-300 hover:bg-emerald-600/50"
            }`}
          >
            {errors.length > 0 ? "❌ Sửa lỗi trước khi convert" : "✓ Convert → HTML"}
          </button>

          {/* Help */}
          <details className="text-xs text-slate-400">
            <summary className="cursor-pointer hover:text-slate-300">
              💡 Cú pháp LaTeX hỗ trợ
            </summary>
            <div className="mt-2 space-y-1 pl-3 text-slate-500">
              <p>
                <code className="text-slate-400">\section{'{'}Tiêu đề chính{'}'}</code> → H1
              </p>
              <p>
                <code className="text-slate-400">\subsection{'{'}Tiêu đề phụ{'}'}</code> → H2
              </p>
              <p>
                <code className="text-slate-400">$x^2$</code> hoặc{" "}
                <code className="text-slate-400">\(x^2\)</code> → Inline math
              </p>
              <p>
                <code className="text-slate-400">$$x^2$$</code> hoặc{" "}
                <code className="text-slate-400">\[x^2\]</code> → Display math
              </p>
              <p>
                <code className="text-slate-400">\textbf{'{'}đậm{'}'}</code>,{" "}
                <code className="text-slate-400">\textit{'{'}nghiêng{'}'}</code>
              </p>
              <p>
                <code className="text-slate-400">\begin{'{'}itemize{'}'} \item ... \end{'{'}itemize{'}'}</code>
              </p>
            </div>
          </details>
        </div>
      )}

      {/* AZOTA Mode */}
      {mode === "azota" && (
        <div className="space-y-2">
          <textarea
            value={latexText}
            onChange={(e) => setLatexText(e.target.value)}
            placeholder={`Dán iframe code từ AZOTA ở đây, ví dụ:

<iframe width="100%" height="900" src="https://azota.vn/de-thi/ezkjlr" title="[26-27] 12 KTTX tuần 1" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe>`}
            rows={6}
            className={`${inputCls} w-full font-mono text-xs`}
          />

          {/* Errors */}
          {errors.length > 0 && (
            <div className="rounded-lg border border-red-500/30 bg-red-500/5 p-3">
              <p className="text-xs font-semibold text-red-300">❌ Lỗi:</p>
              <ul className="mt-1 space-y-1">
                {errors.map((err, i) => (
                  <li key={i} className="text-xs text-red-200">
                    • {err}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Preview */}
          {!errors.length && latexText.includes("iframe") && (
            <div className="rounded-lg border border-blue-500/30 bg-blue-500/5 p-3">
              <p className="mb-2 text-xs font-semibold text-blue-300">👁️ Preview sau khi embed:</p>
              <div className="max-h-64 overflow-y-auto rounded bg-white/5 p-2">
                <div
                  dangerouslySetInnerHTML={{
                    __html: formatAzotaEmbed(parseAzotaIframe(latexText)),
                  }}
                />
              </div>
            </div>
          )}

          {/* Embed Button */}
          <button
            onClick={handleAzotaEmbed}
            disabled={!latexText.includes("iframe") || errors.length > 0}
            className={`w-full rounded-lg px-4 py-2 text-sm font-semibold transition-colors ${
              !latexText.includes("iframe") || errors.length > 0
                ? "bg-slate-600/30 text-slate-500 cursor-not-allowed"
                : "bg-blue-600/30 text-blue-300 hover:bg-blue-600/50"
            }`}
          >
            {errors.length > 0 ? "❌ Sửa lỗi trước" : "✓ Nhúng AZOTA"}
          </button>

          {/* Help */}
          <details className="text-xs text-slate-400">
            <summary className="cursor-pointer hover:text-slate-300">
              💡 Cách lấy iframe từ AZOTA
            </summary>
            <div className="mt-2 space-y-2 pl-3 text-slate-500">
              <p>1. Vào <code className="text-slate-400">azota.vn</code> → Tìm bài tập/đề</p>
              <p>2. Click &quot;Chia sẻ&quot; hoặc &quot;Nhúng&quot; → Copy iframe code</p>
              <p>3. Dán vào field trên</p>
              <p>4. Click &quot;✓ Nhúng AZOTA&quot;</p>
            </div>
          </details>
        </div>
      )}

      {/* HTML Mode */}
      {mode === "html" && (
        <textarea
          value={latexText}
          onChange={(e) => handleHtmlChange(e.target.value)}
          placeholder={placeholder || "Nội dung HTML + công thức math (dùng $...$ hoặc $$...$$ cho LaTeX math)"}
          rows={8}
          className={`${inputCls} w-full font-mono`}
        />
      )}
    </div>
  );
}
