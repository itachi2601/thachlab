"use client";

/**
 * components/physics/PredictGate.tsx
 *
 * Bước "đoán trước rồi mới xem" dùng chung cho các mô phỏng tự kéo (C1, C2 — content/thi-nghiem/de-xuat-bo-sung-2026-11-12.md).
 * Câu dự đoán hỏi HIỆN TƯỢNG, kết quả bị khoá tới khi học sinh chọn (T2, V7 — docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md).
 * Nhãn A. B. C. D. như đề thật (E1), chữ câu hỏi dùng font đề (E4); phản hồi nói vì sao, không chỉ đúng/sai (L1, L4);
 * đúng/sai có chữ + ký hiệu, không chỉ màu (M4); nút phương án cao ≥ 44 px (D2). Không điểm, không huy hiệu (L3).
 */

export interface PredictOption {
  text: string;
  correct?: boolean;
  /** Vì sao phương án này đúng/sai — hiện sau khi chọn. */
  why: string;
}

export interface PredictGateProps {
  question: string;
  options: PredictOption[];
  choice: number | null;
  onChoose: (index: number) => void;
  /** Dòng gợi ý sau khi chọn (ví dụ "Kéo điểm (2) để tự kiểm."). */
  hint?: string;
}

const LETTERS = ["A", "B", "C", "D"];

export function PredictGate({ question, options, choice, onChoose, hint }: PredictGateProps) {
  const correctIndex = options.findIndex((o) => o.correct);

  if (choice === null) {
    return (
      <div className="rounded-xl border border-line-strong bg-panel p-3 sm:p-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-primary">Đoán trước rồi mới xem</p>
        <div className="exam-paper mt-1">
          <p className="exam-content text-ink">{question}</p>
          <div className="exam-content mt-2 grid gap-2">
            {options.map((o, i) => (
              <button
                key={i}
                type="button"
                onClick={() => onChoose(i)}
                className="flex min-h-11 w-full items-start gap-2 rounded-lg border border-line-strong bg-panel px-3 py-2 text-left text-ink transition hover:bg-primary-soft active:scale-[0.99]"
              >
                <span className="shrink-0 font-bold">{LETTERS[i]}.</span>
                <span>{o.text}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const chosen = options[choice];
  const right = choice === correctIndex;
  return (
    <div className="rounded-xl border border-line bg-surface-2 p-3 text-sm leading-relaxed text-ink">
      <p>
        <span className={right ? "font-semibold text-ok" : "font-semibold text-danger"}>
          {right ? "✓ Em đoán đúng" : "✗ Chưa đúng"}
        </span>{" "}
        — em chọn {LETTERS[choice]}. {chosen.text.replace(/\.$/, "")}
        {!right && correctIndex >= 0 && (
          <>
            ; đáp án {LETTERS[correctIndex]}. {options[correctIndex].text.replace(/\.$/, "")}
          </>
        )}
      </p>
      <p className="mt-1 text-muted">{right ? chosen.why : `${chosen.why} ${options[correctIndex]?.why ?? ""}`}</p>
      {hint && <p className="mt-1 text-muted">{hint}</p>}
    </div>
  );
}

/* ---------- Định dạng số kiểu Việt (dấu phẩy thập phân, dấu trừ thật, mũ chỉ số trên) ---------- */

const SUP: Record<string, string> = {
  "-": "⁻",
  "0": "⁰",
  "1": "¹",
  "2": "²",
  "3": "³",
  "4": "⁴",
  "5": "⁵",
  "6": "⁶",
  "7": "⁷",
  "8": "⁸",
  "9": "⁹",
};

/** 1.5 → "1,5"; −3 → "−3". */
export function vn(x: number, digits = 2): string {
  const s = x.toFixed(digits);
  return (s.startsWith("-") && Number(s) !== 0 ? "−" + s.slice(1) : s.replace("-", "")).replace(".", ",");
}

/** 6.52e-7 → "6,5·10⁻⁷". */
export function vnSci(x: number, digits = 1): string {
  if (x === 0 || !Number.isFinite(x)) return "0";
  let e = Math.floor(Math.log10(Math.abs(x)));
  let m = Number((x / 10 ** e).toFixed(digits));
  if (Math.abs(m) >= 10) {
    m /= 10;
    e += 1;
  }
  const exp = String(e)
    .split("")
    .map((c) => SUP[c] ?? c)
    .join("");
  return `${vn(m, digits)}·10${exp}`;
}
