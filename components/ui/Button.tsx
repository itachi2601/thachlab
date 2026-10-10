"use client";

import { type ButtonHTMLAttributes, forwardRef } from "react";

type Variant = "primary" | "outline" | "ghost" | "danger";
type Size = "sm" | "md";

const VARIANT: Record<Variant, string> = {
  primary:
    "bg-primary text-white hover:bg-primary-dark disabled:hover:bg-primary",
  outline:
    "border border-line-strong text-ink hover:bg-surface-2 disabled:hover:bg-transparent",
  ghost: "text-ink hover:bg-surface-2 disabled:hover:bg-transparent",
  danger:
    "border border-danger text-danger hover:bg-surface-2 disabled:hover:bg-transparent",
};

const SIZE: Record<Size, string> = {
  sm: "min-h-11 px-3.5 py-1.5 text-xs",
  md: "min-h-11 px-5 py-2.5 text-sm",
};

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
}

/** Nút dùng chung — thay cho việc lặp lại class Tailwind ở mỗi nơi. */
const Button = forwardRef<HTMLButtonElement, Props>(function Button(
  { variant = "primary", size = "md", className = "", type = "button", ...rest },
  ref,
) {
  return (
    <button
      ref={ref}
      type={type}
      className={`inline-flex items-center justify-center gap-1.5 rounded-full font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-40 ${VARIANT[variant]} ${SIZE[size]} ${className}`}
      {...rest}
    />
  );
});

export default Button;
