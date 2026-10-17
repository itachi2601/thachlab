"use client";

/**
 * components/exams/QuestionSlideMotion.tsx
 *
 * Phần dùng framer-motion của <QuestionSlide> — chuyển câu trong lúc làm đề
 * (ExamRunner): câu mới trượt/mờ vào ngay khi đổi key, không có pha "thoát" chờ
 * (pha đó làm nội dung trễ so với số câu). Tách file để <QuestionSlide> nạp chậm (chunk riêng),
 * không nằm trong JS ban đầu của trang làm đề.
 */

import { motion, useReducedMotion } from "framer-motion";
import type { ReactNode } from "react";

export default function QuestionSlideMotion({
  children,
  slideKey,
}: {
  children: ReactNode;
  slideKey: number | string;
}) {
  const reduceMotion = useReducedMotion();

  // Không dùng AnimatePresence mode="wait": nó giữ câu cũ ~0,2 s rồi mới vào câu mới trong khi
  // ô "Câu N/M" đã đổi ngay → HS tưởng bấm hụt (N1/B). Đổi key = gỡ câu cũ ngay, câu mới mờ dần vào.
  return (
    <motion.div
      key={slideKey}
      initial={{ opacity: 0, x: reduceMotion ? 0 : 12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: reduceMotion ? 0 : 0.18, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
