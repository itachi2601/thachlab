type Tone = "success" | "error" | "warning" | "info" | "violet" | "neutral";

const TONE: Record<Tone, string> = {
  success: "bg-emerald-500/15 text-emerald-300",
  error: "bg-red-500/15 text-red-300",
  warning: "bg-amber-500/15 text-amber-300",
  info: "bg-primary/15 text-primary",
  violet: "bg-violet-500/15 text-violet-300",
  neutral: "bg-slate-500/20 text-slate-400",
};

/** Nhãn tròn nhỏ dùng chung cho trạng thái (đúng/sai/bỏ qua/…). */
export default function Badge({
  tone = "neutral",
  children,
  className = "",
}: {
  tone?: Tone;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <span
      className={`inline-block rounded-full px-2.5 py-1 text-xs font-semibold ${TONE[tone]} ${className}`}
    >
      {children}
    </span>
  );
}
