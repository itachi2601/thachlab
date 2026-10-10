"use client";

import { useEffect, useState } from "react";
import { fetchTaskRpMessage, type TaskRpKind } from "@/services/task-rp";

/** Một dòng RP trước khi bắt đầu (N1, C1). Không có mùa hoặc lỗi mạng thì ẩn (N3). Không huy hiệu, không màu thưởng (L3). */
export default function TaskRpLine({
  kind,
  sourceId,
  staticText,
}: {
  kind?: TaskRpKind;
  sourceId?: number | null;
  /** Việc không bao giờ cộng RP (luyện theo chủ đề, bài thoát phụ đạo). */
  staticText?: string;
}) {
  const [text, setText] = useState<string | null>(staticText ?? null);

  useEffect(() => {
    if (staticText) {
      setText(staticText);
      return;
    }
    if (kind == null || sourceId == null) {
      setText("Lượt này không tính RP.");
      return;
    }
    let alive = true;
    setText(null);
    fetchTaskRpMessage(kind, sourceId)
      .then((line) => {
        if (alive) setText(line);
      })
      .catch(() => {
        if (alive) setText(null);
      });
    return () => {
      alive = false;
    };
  }, [kind, sourceId, staticText]);

  if (!text) return null;
  return <p className="text-base leading-relaxed text-ink">{text}</p>;
}
