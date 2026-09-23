/** Minh hoạ chung cho "chưa có gì ở đây" — khay trống + ngôi sao, thay cho một dòng chữ xám trần. */
function EmptyTrayIllustration() {
  return (
    <svg viewBox="0 0 120 100" className="h-24 w-28" role="presentation" aria-hidden="true">
      <defs>
        <linearGradient id="empty-tray" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#8b5cf6" />
          <stop offset="1" stopColor="#3b82f6" />
        </linearGradient>
      </defs>
      <ellipse cx="60" cy="86" rx="38" ry="6" fill="url(#empty-tray)" opacity="0.12" />
      <g stroke="url(#empty-tray)" strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20 52 34 22h52l14 30" />
        <path d="M20 52v20a6 6 0 0 0 6 6h68a6 6 0 0 0 6-6V52" />
        <path d="M20 52h24l4 8h24l4-8h24" />
      </g>
      <g stroke="url(#empty-tray)" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" fill="none">
        <path d="M90 18l2.4 5 5 2.4-5 2.4-2.4 5-2.4-5-5-2.4 5-2.4z" />
      </g>
    </svg>
  );
}

/** Trạng thái trống dùng chung — icon minh hoạ + lời nhắn, thay cho một dòng text xám đơn độc. */
export default function EmptyState({
  title,
  description,
  action,
  className = "",
}: {
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`flex flex-col items-center gap-3 rounded-2xl border border-dashed border-white/10 p-8 text-center ${className}`}
    >
      <EmptyTrayIllustration />
      <p className="font-semibold text-white">{title}</p>
      {description && <p className="max-w-xs text-sm text-slate-500">{description}</p>}
      {action}
    </div>
  );
}
