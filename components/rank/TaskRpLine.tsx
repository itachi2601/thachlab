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
  const requestKey = `${kind ?? ""}:${sourceId ?? ""}`;
  const [fetched, setFetched] = useState<{ key: string; text: string | null } | null>(null);

  useEffect(() => {
    if (staticText) return;
    if (kind == null || sourceId == null) return;
    let alive = true;
    fetchTaskRpMessage(kind, sourceId)
      .then((line) => {
        if (alive) setFetched({ key: requestKey, text: line });
      })
      .catch(() => {
        if (alive) setFetched({ key: requestKey, text: null });
      });
    return () => {
      alive = false;
    };
  }, [kind, sourceId, staticText, requestKey]);

  const text =
    staticText ??
    (kind == null || sourceId == null
      ? "Lượt này không tính RP."
      : fetched && fetched.key === requestKey
        ? fetched.text
        : null);

  if (!text) return null;
  return <p className="text-base leading-relaxed text-ink">{text}</p>;
}
