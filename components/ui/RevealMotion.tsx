"use client";

/**
 * components/ui/RevealMotion.tsx
 *
 * Phần dùng framer-motion của <Reveal> — tách file để trang chủ không phải
 * tải framer-motion (~140 KB) trong JS ban đầu; Reveal.tsx nạp file này chậm.
 * Logic giữ nguyên: hiện dần + trượt lên khi cuộn tới (một lần), tôn trọng
 * prefers-reduced-motion.
 */

import { motion, useReducedMotion } from "framer-motion";
import type { ReactNode } from "react";

export default function RevealMotion({
  children,
  delay = 0,
  className,
}: {
  children: ReactNode;
  delay?: number;
  className?: string;
}) {
  const reduced = useReducedMotion();

  if (reduced) return <div className={className}>{children}</div>;

  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 28 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1], delay }}
    >
      {children}
    </motion.div>
  );
}
