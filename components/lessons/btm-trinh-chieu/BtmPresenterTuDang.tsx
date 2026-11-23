"use client";

import { useMemo } from "react";
import BtmPresenter from "./BtmPresenter";
import { chieuDuoc, tuDang } from "@/features/lessons/btm-trinh-chieu/tu-dang";
import type { LessonWorkedQuestion } from "@/features/lessons/types";

/** Chiếu các dạng của một mục Bài tập mẫu: dựng bản chiếu từ dữ liệu đã soạn (tu-dang.tsx), bỏ dạng không chia bước. */
export default function BtmPresenterTuDang({
  questions,
  start,
  title,
  lessonId,
  itemId,
  onClose,
}: {
  questions: LessonWorkedQuestion[];
  start: number;
  title?: string;
  lessonId?: number;
  itemId?: number;
  onClose: () => void;
}) {
  const { bais, batDau } = useMemo(() => {
    const dung = questions.map((q, i) => ({ q, i })).filter(({ q }) => chieuDuoc(q));
    return {
      bais: dung.map(({ q, i }) => tuDang(q, i)),
      batDau: Math.max(0, dung.findIndex(({ i }) => i === start)),
    };
  }, [questions, start]);
  if (!bais.length) return null;
  return <BtmPresenter bais={bais} start={batDau} title={title} lessonId={lessonId} itemId={itemId} onClose={onClose} />;
}
