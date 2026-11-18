"use client";

import { useState } from "react";
import { Check, FileText, Play } from "lucide-react";
import { youTubeEmbed, youTubeThumb, type LessonItem } from "@/features/lessons/types";

/** Video YouTube: ảnh bìa, bấm thì nhúng player ngay tại chỗ. Xem xong tự bấm "Đánh dấu đã xem". */
export function VideoBlock({
  item,
  done,
  loggedIn,
  onDone,
  showMarkDone = true,
}: {
  item: LessonItem;
  done: boolean;
  loggedIn: boolean;
  onDone: () => void;
  showMarkDone?: boolean;
}) {
  const [playing, setPlaying] = useState(false);
  const embed = youTubeEmbed(item.video_url);
  const thumb = youTubeThumb(item.video_url);

  return (
    <div className="lesson-block">
      <div className="lesson-block-head">
        <p className="lesson-block-title">{item.title}</p>
        {item.subtitle && <p className="lesson-block-sub">{item.subtitle}</p>}
      </div>
      {embed && (
        <div className="lesson-video">
          {playing ? (
            <iframe
              src={`${embed}?autoplay=1`}
              title={item.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          ) : (
            <button type="button" onClick={() => setPlaying(true)} aria-label={`Xem video ${item.title}`}>
              {thumb && (
                /* eslint-disable-next-line @next/next/no-img-element */
                <img src={thumb} alt="" loading="lazy" decoding="async" />
              )}
              <span>
                <Play size={22} fill="currentColor" />
              </span>
            </button>
          )}
        </div>
      )}
      <div className="lesson-block-foot">
        {item.pdf_url && (
          <a href={item.pdf_url} target="_blank" rel="noreferrer" className="lesson-link">
            <FileText size={15} /> Tài liệu PDF
          </a>
        )}
        {loggedIn && showMarkDone && (
          <button type="button" className={`lesson-done ${done ? "is-done" : ""}`} onClick={onDone} disabled={done}>
            <Check size={14} /> {done ? "Đã xem" : "Đánh dấu đã xem"}
          </button>
        )}
      </div>
    </div>
  );
}
