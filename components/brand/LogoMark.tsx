/**
 * Dấu ThạchLab — chén cầu (mặt cắt) kê trên nêm, dây qua ròng rọc treo quả cân.
 * Hình thầy phác 5/10/2026: cân bằng / mô-men / máy đơn, đúng câu "sống giữa phương trình và chuyển động".
 * Màu theo nền: mặc định mực sáng (nền tối). Theme sáng đổi mực, trừ data-surface="dark"
 * (footer marketing và sidebar quản trị luôn nền tối). Xem .logo-mark trong globals.css.
 */
export default function LogoMark({
  className = "h-8 w-auto",
  surface,
}: {
  className?: string;
  /** "dark" = mực sáng, không đổi theo theme. Bỏ trống = theo theme trang. */
  surface?: "dark";
}) {
  return (
    <svg
      className={`logo-mark ${className}`}
      data-surface={surface}
      viewBox="0 -2.03 136 79.03"
      fill="none"
      aria-hidden="true"
    >
      <path d="M 6 70 H 128" stroke="var(--mark-ink)" strokeWidth="2.75" strokeLinecap="round" />
      <g stroke="var(--mark-ink)" strokeWidth="1.5" strokeLinecap="round">
        <path d="M 16 70 l -3 5" />
        <path d="M 28 70 l -3 5" />
        <path d="M 40 70 l -3 5" />
        <path d="M 52 70 l -3 5" />
        <path d="M 64 70 l -3 5" />
        <path d="M 76 70 l -3 5" />
        <path d="M 88 70 l -3 5" />
        <path d="M 100 70 l -3 5" />
        <path d="M 112 70 l -3 5" />
        <path d="M 124 70 l -3 5" />
      </g>
      <path d="M 56 70 H 90 V 46 Z" fill="var(--mark-ink)" />
      <path
        d="M 8 40 A 35.94 35.94 0 1 0 78 24 Z"
        transform="translate(0 0.37)"
        fill="var(--mark-bowl)"
        stroke="var(--mark-line)"
        strokeWidth="2.6"
        strokeLinejoin="round"
      />
      <path d="M 78 24.37 L 108.33 3.12" stroke="var(--mark-ink)" strokeWidth="2.15" strokeLinecap="round" />
      <circle cx="112" cy="8.37" r="6.4" fill="var(--mark-bowl)" stroke="var(--mark-ink)" strokeWidth="2.15" />
      <circle cx="112" cy="8.37" r="1.55" fill="var(--mark-ink)" />
      <path d="M 112 14.77 V 22.77" stroke="var(--mark-ink)" strokeWidth="2.15" strokeLinecap="round" />
      <path
        d="M 106.8 22.77 h 10.4 a 1.5 1.5 0 0 1 1.5 1.5 v 8.6 a 1.5 1.5 0 0 1 -1.5 1.5 h -10.4 a 1.5 1.5 0 0 1 -1.5 -1.5 v -8.6 a 1.5 1.5 0 0 1 1.5 -1.5 z"
        fill="var(--mark-ink)"
      />
    </svg>
  );
}
