"use client";

import { useState } from "react";
import Link from "next/link";
import type { PhysicsCardData } from "@/lib/physics-card";

const LETTERS = ["A", "B", "C", "D"];

/**
 * Thẻ "Vật lý quanh ta": khung ảnh 16:9 (ảnh thật hoặc khung giữ chỗ) + nhãn tò mò + câu hook + câu đố chọn tại chỗ.
 * Quy tắc: M4 (đúng/sai kèm chữ), D2 (nút ≥ 44px), B4 (không chuyển động), E1 (nhãn A. B. C.), N1 (một câu đố/thẻ, không điểm, không xếp hạng).
 */
export function PhysicsCuriosityCard({
  card,
  isNew = false,
  compact = false,
  onOpen,
}: {
  card: PhysicsCardData;
  isNew?: boolean;
  /** Dải trang chủ: khung ảnh dẹt hơn (2:1) để thẻ không quá cao khi nằm trước các khối khác (B1). */
  compact?: boolean;
  onOpen?: (slug: string) => void;
}) {
  const [picked, setPicked] = useState<number | null>(null);
  // Dải trang chủ: câu đố gập lại sau nút "Đoán thử" để thẻ không cao cả màn hình; /blog mở sẵn.
  const [open, setOpen] = useState(!compact);
  const { quiz } = card;
  const answered = picked !== null;
  const correct = answered && quiz ? picked === quiz.answer : false;
  const credit = card.photoCredit;

  return (
    <article className="flex h-full flex-col overflow-hidden rounded-xl border border-line bg-panel">
      <div className={`relative shrink-0 bg-surface-2 ${compact ? "aspect-[2/1]" : "aspect-[16/9]"}`}>
        {card.photo ? (
          // Ảnh tĩnh (export), webp ≤150 KB do script kiểm; width/height giữ chỗ để không nhảy bố cục.
          <img
            src={card.photo}
            alt={card.photoAlt ?? ""}
            width={1200}
            height={675}
            loading="lazy"
            decoding="async"
            className="h-full w-full object-cover"
          />
        ) : (
          <div aria-hidden className="flex h-full w-full items-center justify-center bg-primary/10 font-display text-5xl font-bold text-primary/40">
            ?
          </div>
        )}
        <div className="absolute left-3 top-3 flex items-center gap-2">
          {card.badge ? (
            <span className="rounded-full border border-line bg-panel px-2.5 py-1 text-[13px] font-semibold text-ink">{card.badge}</span>
          ) : null}
          {isNew ? (
            <span className="rounded border border-primary/25 bg-panel px-1.5 py-0.5 font-mono text-[13px] font-bold uppercase tracking-wider text-primary">
              mới
            </span>
          ) : null}
        </div>
      </div>
      {card.photo && credit ? (
        <p className="px-4 pt-1.5 text-[13px] leading-snug text-muted">
          Ảnh:{" "}
          <a href={credit.sourceUrl} target="_blank" rel="noopener noreferrer" className="underline underline-offset-2">
            {credit.author}
          </a>
          {" · "}
          {credit.licenseUrl ? (
            <a href={credit.licenseUrl} target="_blank" rel="noopener noreferrer" className="underline underline-offset-2">
              {credit.license}
            </a>
          ) : (
            credit.license
          )}
        </p>
      ) : null}

      <div className="flex flex-1 flex-col gap-3 p-4">
        <div>
          <h3 className="font-display text-lg font-bold leading-snug text-ink">{card.title}</h3>
          {card.hook ? <p className={`mt-1.5 text-[15px] leading-relaxed text-muted ${compact ? "line-clamp-3" : ""}`}>{card.hook}</p> : null}
        </div>

        {quiz && !open ? (
          <button
            type="button"
            aria-expanded={false}
            onClick={() => setOpen(true)}
            className="flex min-h-11 w-full items-center justify-between rounded-lg border border-primary bg-bg px-3 py-2 text-left text-[15px] font-semibold text-primary"
          >
            Đoán thử 30 giây
            <span aria-hidden>↓</span>
          </button>
        ) : null}
        {quiz && open ? (
          <div role="group" aria-label="Câu đố nhanh" className="space-y-2">
            <p className="text-[15px] font-semibold leading-snug text-ink">{quiz.question}</p>
            <ul className="space-y-2">
              {quiz.options.map((option, index) => {
                const isRight = answered && index === quiz.answer;
                const isWrongPick = answered && index === picked && index !== quiz.answer;
                return (
                  <li key={option}>
                    <button
                      type="button"
                      disabled={answered}
                      onClick={() => setPicked(index)}
                      className={`flex min-h-11 w-full items-start gap-2 rounded-lg border px-3 py-2 text-left text-[15px] leading-snug transition-colors ${
                        isRight
                          ? "border-ok bg-surface-2 text-ink"
                          : isWrongPick
                            ? "border-danger bg-surface-2 text-ink"
                            : "border-line bg-bg text-ink enabled:hover:border-primary"
                      } ${answered && !isRight && !isWrongPick ? "opacity-70" : ""}`}
                    >
                      <span className="font-bold">{LETTERS[index]}.</span>
                      <span className="flex-1">{option}</span>
                      {isRight ? <span className="shrink-0 font-semibold text-ok">Đúng</span> : null}
                      {isWrongPick ? <span className="shrink-0 font-semibold text-danger">Chưa đúng</span> : null}
                    </button>
                  </li>
                );
              })}
            </ul>
            <div aria-live="polite">
              {answered ? (
                <p className="text-[15px] leading-relaxed text-ink">
                  <span className="font-semibold">{correct ? "Đúng rồi. " : `Đáp án là ${LETTERS[quiz.answer]}. `}</span>
                  {quiz.why}
                </p>
              ) : null}
            </div>
          </div>
        ) : null}

        <Link
          href={card.href}
          onClick={() => onOpen?.(card.slug)}
          className="mt-auto inline-flex min-h-11 items-center text-[15px] font-semibold text-primary underline-offset-4 hover:underline"
        >
          {answered ? "Xem vì sao →" : "Đọc bài →"}
          <span className="ml-2 text-[13px] font-normal text-muted">{card.readingMinutes} phút</span>
        </Link>
      </div>
    </article>
  );
}
