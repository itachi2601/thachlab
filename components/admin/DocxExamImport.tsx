"use client";

import { useRef, useState } from "react";
import { FileText, Upload } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { docxTextToBundle } from "@/services/docx-exam-parser";
import { readDocx } from "@/services/docx-reader";
import type { LessonBundle } from "@/services/lesson-import";

/**
 * Thả một file đề .docx → dựng sẵn gói đề ngay trong trình duyệt.
 * Không gọi máy chủ, không cần trợ lý: đọc file, tách câu, lấy đáp án dấu *,
 * chuyển công thức Office Math sang $…$, gom ảnh nhúng.
 */
export default function DocxExamImport({
  fallbackTitle,
  subjectCode,
  onDraft,
}: {
  fallbackTitle: string;
  subjectCode: string;
  onDraft: (bundle: LessonBundle, notes: string[]) => void;
}) {
  const toast = useToast();
  const fileRef = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState(false);
  const [dragging, setDragging] = useState(false);
  const [info, setInfo] = useState<{
    fileName: string;
    questions: number;
    markers: number;
    images: number;
    omml: number;
    mathType: number;
    text: string;
  } | null>(null);

  async function handleFile(file: File) {
    if (!/\.docx$/i.test(file.name)) {
      toast("error", "Chỉ nhận file .docx (Word). File .doc cũ: mở Word → Save As → .docx.");
      return;
    }
    setBusy(true);
    try {
      const read = await readDocx(await file.arrayBuffer());
      const draft = docxTextToBundle(read.text, {
        subjectCode,
        images: read.images,
      });
      if (draft.bundle.exam.title === "Đề kiểm tra" && fallbackTitle.trim())
        draft.bundle.exam.title = fallbackTitle.trim();

      setInfo({
        fileName: file.name,
        questions: draft.bundle.exam.questions.length,
        markers: draft.markerCount,
        images: read.images.length,
        omml: read.ommlCount,
        mathType: read.mathTypeCount,
        text: read.text,
      });
      onDraft(draft.bundle, [...read.warnings, ...draft.notes]);

      if (draft.bundle.exam.questions.length === 0)
        toast("warning", "Không tách được câu nào — xem phần ghi chú bên dưới.");
      else toast("success", `Đã đọc ${draft.bundle.exam.questions.length} câu từ ${file.name}.`);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-3">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          const file = e.dataTransfer.files[0];
          if (file) void handleFile(file);
        }}
        onClick={() => fileRef.current?.click()}
        className={`cursor-pointer rounded-2xl border border-dashed p-6 text-center ${
          dragging ? "border-blue-400 bg-blue-500/10" : "border-white/15 hover:border-white/30"
        }`}
      >
        <Upload size={22} className="mx-auto text-slate-400" />
        <p className="mt-2 text-sm font-semibold text-slate-200">
          {busy ? "Đang đọc file…" : "Kéo file đề .docx vào đây, hoặc bấm để chọn"}
        </p>
        <p className="mt-1 text-xs text-slate-500">
          Đề kiểu Azota: “Câu 1.”, phương án A–D, đáp án đánh dấu <b>*</b>, dòng “Lời giải:”.
        </p>
        <input
          ref={fileRef}
          type="file"
          accept=".docx"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            e.target.value = "";
            if (file) void handleFile(file);
          }}
        />
      </div>

      {info && (
        <div className="rounded-xl border border-white/10 bg-black/20 p-3 text-xs text-slate-300">
          <p className="flex flex-wrap items-center gap-2">
            <FileText size={14} className="text-blue-300" />
            <b className="text-slate-200">{info.fileName}</b>
            <span>· {info.questions}/{info.markers} câu dựng được</span>
            <span>· {info.omml} công thức đọc được</span>
            {info.mathType > 0 && <span className="text-amber-300">· {info.mathType} công thức MathType chưa chuyển</span>}
            {info.images > 0 && <span>· {info.images} ảnh</span>}
          </p>
          <details className="mt-2">
            <summary className="cursor-pointer text-slate-400 hover:text-slate-200">
              Xem văn bản đọc được từ file
            </summary>
            <pre className="mt-2 max-h-64 overflow-auto whitespace-pre-wrap rounded-lg bg-black/40 p-2 text-[11px] text-slate-400">
              {info.text}
            </pre>
          </details>
        </div>
      )}

      <details className="text-xs text-slate-400">
        <summary className="cursor-pointer hover:text-slate-200">Chuẩn bị file Word thế nào cho đọc được hết</summary>
        <ol className="mt-2 list-decimal space-y-1 pl-5">
          <li>
            Công thức MathType: mở file trong Word → tab <b>MathType</b> → <b>Convert Equations</b> →
            chọn <b>Microsoft Office Math</b> → OK → lưu lại. (Công thức gõ bằng Word <b>Alt + =</b> thì
            không cần bước này.)
          </li>
          <li>
            Đáp án đúng: thêm dấu <b>*</b> ngay trước phương án đúng (<code>*B. 5 m/s</code>), hoặc
            viết dòng <code>Đáp án: B</code>. Câu đúng–sai: đánh <b>*</b> ở các ý Đúng.
          </li>
          <li>
            Số thứ tự câu phải là chữ trong bài (<code>Câu 1.</code>), không dùng đánh số tự động của Word.
          </li>
          <li>Hình vẽ nên là ảnh PNG/JPG; ảnh WMF/EMF web không hiện được.</li>
          <li>Có “PHẦN I / II / III” thì tự nhận đúng loại câu; không có thì coi là trắc nghiệm A–D.</li>
        </ol>
      </details>
    </div>
  );
}
