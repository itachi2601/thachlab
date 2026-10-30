"use client";

import { useLayoutEffect, useState, type RefObject } from "react";
import { createPortal } from "react-dom";
import VideoKhungLazy from "@/components/lessons/VideoKhungLazy";
import { logClipChoice } from "@/services/learning-events";
import type { VideoKhungData, VideoKhungEvent } from "@/components/lessons/VideoThiNghiemKhung";

/**
 * Gắn khung video tương tác vào các hộp `<div class="tl-box tl-box--video tl-box--khung" data-khung='{json}'>`
 * trong HTML bài (chen-video-thi-nghiem.mts ghi). HTML bài là chuỗi tĩnh nên khung được vẽ bằng portal vào một
 * `div.tl-khung-host` thêm cuối hộp; hộp tĩnh (label, <video>, "Nhìn vào") vẫn là phương án dự phòng và chỉ bị
 * ẩn khi khung mount xong. `version` đổi (HTML bị ghi lại sau KaTeX…) thì tìm lại hộp: câu em đã chọn được
 * nhớ theo id clip nên không bị hỏi lại.
 */
type Host = { host: HTMLElement; data: VideoKhungData };

const NGUON = /^https:\/\/jgvbdbpvjdntdgzthumv\.supabase\.co\/storage\/v1\/object\/public\/lesson-clips\//;

export default function KhungPortals({
  rootRef,
  version,
}: {
  rootRef: RefObject<HTMLElement | null>;
  version: string;
}) {
  const [hosts, setHosts] = useState<Host[]>([]);

  useLayoutEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    const found: Host[] = [];
    root.querySelectorAll<HTMLElement>(".tl-box--khung[data-khung]").forEach((box) => {
      let data: VideoKhungData;
      try {
        data = JSON.parse(box.dataset.khung ?? "");
      } catch {
        return;
      }
      if (!data?.id || !data.video || !Array.isArray(data.o) || !data.dung_dua) return;
      if (!NGUON.test(data.video) || (data.poster && !NGUON.test(data.poster))) return; // chỉ nhận clip từ kho lesson-clips
      let host = box.querySelector<HTMLElement>(":scope > .tl-khung-host");
      if (!host) {
        host = document.createElement("div");
        host.className = "tl-khung-host";
        box.appendChild(host);
      }
      found.push({ host, data });
    });
    setHosts(found);
  }, [rootRef, version]);

  // Chỉ học sinh trong bài (InlineLessonAccordion đặt data-lesson-id): ghi lựa chọn Dự đoán vào lô sự kiện chung.
  const ghi = (tnId: string, e: VideoKhungEvent) => {
    if (e.loai !== "chon" && e.loai !== "bo_qua") return;
    const lessonId = Number(rootRef.current?.closest<HTMLElement>("[data-lesson-id]")?.dataset.lessonId);
    if (!Number.isFinite(lessonId) || lessonId <= 0) return;
    logClipChoice({
      lessonId,
      tnId,
      choice: e.loai === "chon" ? e.chon : null,
      correct: e.loai === "chon" ? e.dung : null,
    });
  };

  return (
    <>
      {hosts.map((h) =>
        createPortal(<VideoKhungLazy data={h.data} dinh={false} onEvent={(e) => ghi(h.data.id, e)} />, h.host, h.data.id),
      )}
    </>
  );
}
