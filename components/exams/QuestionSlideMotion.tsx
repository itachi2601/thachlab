"use client";

/**
 * components/exams/QuestionSlideMotion.tsx
 *
 * Phần dùng framer-motion của <QuestionSlide> — chuyển câu trong lúc làm đề
 * (ExamRunner) trượt nhẹ + đổi mờ, câu cũ "thoát" trong khi câu mới "vào"
 * cùng lúc (AnimatePresence mode="wait"). Đây là animation có thoát (exit)
 * thật sự — không thay được bằng CSS transition thuần vì cần giữ node cũ
 * trong DOM một nhịp để chạy hiệu ứng thoát trước khi gỡ hẳn — nên vẫn giữ
 * framer-motion, nhưng tách file để <QuestionSlide> nạp chậm (chunk riêng),
 * không nằm trong JS ban đầu của trang làm đề.
 */

import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import type { ReactNode } from "react";

export default function QuestionSlideMotion({
  children,
  slideKey,
}: {
  children: ReactNode;
  slideKey: number | string;
}) {
  const reduceMotion = useReducedMotion();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={slideKey}
        initial={{ opacity: 0, x: reduceMotion ? 0 : 12 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: reduceMotion ? 0 : -12 }}
        transition={{ duration: reduceMotion ? 0 : 0.18, ease: "easeOut" }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
