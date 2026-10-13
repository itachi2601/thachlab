import type { ReactNode } from "react";

const MAX: Record<"sm" | "md" | "lg", string> = {
  sm: "max-h-64",
  md: "max-h-96",
  lg: "max-h-[32rem]",
};

/**
 * Khung cuộn cho danh sách dài: chỉ hiện một phần, còn lại cuộn trong khung để
 * trang không dài vô tận và phần bên dưới (form sửa, chi tiết) không bị đẩy xuống cuối (N1).
 */
export default function ScrollBox({ size = "md", children, className = "" }: { size?: "sm" | "md" | "lg"; children: ReactNode; className?: string }) {
  return (
    <div tabIndex={0} className={`${MAX[size]} overflow-y-auto overscroll-contain pr-1 ${className}`}>
      {children}
    </div>
  );
}
