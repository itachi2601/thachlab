import LogoMark from "@/components/brand/LogoMark";

/**
 * Khóa ngang: dấu + chữ ThạchLab.
 * Chữ "Lab" là màu nhấn duy nhất (M3). Trên nền sáng dùng xanh đậm để đạt ≥ 4,5:1 (M2).
 */
export default function Logo({
  surface,
  className = "",
  markClassName = "h-8 w-auto",
}: {
  surface?: "dark";
  className?: string;
  markClassName?: string;
}) {
  return (
    <span className={`logo-lockup inline-flex items-center gap-2 whitespace-nowrap ${className}`} data-surface={surface}>
      <LogoMark surface={surface} className={markClassName} />
      <span className="logo-name font-display text-lg font-semibold tracking-tight">
        Thạch<span className="logo-lab">Lab</span>
      </span>
    </span>
  );
}
