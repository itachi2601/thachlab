"use client";

import { useState } from "react";
import { usePoll } from "@/components/quiz-live/shared";
import { getReviewRoster, type MyStage, type RosterStudent } from "@/services/review-session";
import { Bar } from "./shared";

/** "Nguyễn Văn Minh Anh" → "Minh Anh": đủ nhận ra bạn, không dài trên điện thoại. */
function shortName(full: string): string {
  const w = full.trim().split(/\s+/);
  return w.slice(-2).join(" ");
}

function Group({ title, tone, list, empty }: { title: string; tone: "ok" | "doing" | "none"; list: RosterStudent[]; empty?: string }) {
  const mark = tone === "ok" ? "✓" : tone === "doing" ? "●" : "○";
  const cls = tone === "ok" ? "bg-surface-2 text-ok" : tone === "doing" ? "bg-primary-soft text-primary" : "bg-surface-2 text-muted";
  return (
    <div className="space-y-2">
      <h3 className="text-sm font-bold text-ink">{title} ({list.length})</h3>
      {list.length === 0 ? (
        empty ? <p className="text-sm text-muted">{empty}</p> : null
      ) : (
        <ul className="flex flex-wrap gap-2">
          {list.map((s) => (
            <li key={s.id} className={`inline-flex min-h-8 items-center gap-1 rounded-full px-3 py-1 text-sm ${cls} ${s.me ? "font-bold ring-2 ring-primary" : "font-medium"}`}>
              <span aria-hidden>{mark}</span>
              {s.me ? "Em" : shortName(s.name)}
              <span className="sr-only">{tone === "ok" ? " đã nộp" : tone === "doing" ? " đang làm" : " chưa làm"}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/**
 * Trang live của lớp: bạn nào đã nộp, đang làm, chưa làm từng ngày. Chỉ trạng thái, không điểm, không xếp hạng
 * (tuổi 14–18 nhạy địa vị bạn bè: người xem thấy việc làm, không thấy kết quả của nhau).
 */
export default function ClassRoster({ sessionId, stages, now }: { sessionId: number; stages: MyStage[]; now: string }) {
  const [students, setStudents] = useState<RosterStudent[] | null>(null);
  const nowMs = Date.parse(now);
  const opened = stages.map((s, i) => ({ s, i })).filter(({ s }) => !s.open_at || Date.parse(s.open_at) <= nowMs);
  const [pick, setPick] = useState<number | null>(null);
  const idx = pick ?? (opened.length ? opened[opened.length - 1].i : 0);

  usePoll(
    () => getReviewRoster(sessionId),
    () => 20000,
    (d) => setStudents(d?.students ?? []),
  );

  if (opened.length === 0) return null;
  const all = students ?? [];
  const done = all.filter((s) => s.st[idx] === "done");
  const doing = all.filter((s) => s.st[idx] === "doing");
  const none = all.filter((s) => s.st[idx] === "none");

  return (
    <section className="space-y-3 rounded-2xl border border-line bg-panel p-4" aria-label="Cả lớp đang làm bài">
      <div>
        <h2 className="text-base font-bold text-ink">Cả lớp hôm nay</h2>
        <p className="text-sm text-muted">Tự cập nhật mỗi 20 giây. Chỉ thấy bạn đã nộp hay chưa, không thấy điểm.</p>
      </div>
      {opened.length > 1 && (
        <div className="flex flex-wrap gap-2" role="tablist" aria-label="Chọn ngày">
          {opened.map(({ i }) => (
            <button
              key={i}
              type="button"
              role="tab"
              aria-selected={i === idx}
              onClick={() => setPick(i)}
              className={`min-h-11 rounded-full px-4 text-sm font-semibold ${i === idx ? "bg-primary text-white" : "border border-line-strong text-ink"}`}
            >
              Ngày {i + 1}
            </button>
          ))}
        </div>
      )}
      {students === null ? (
        <p className="text-sm text-muted">Đang tải…</p>
      ) : (
        <>
          <p className="font-semibold text-ink">
            {done.length}/{all.length} bạn đã nộp
          </p>
          <Bar value={done.length} max={all.length} tone="ok" />
          <Group title="Đã nộp" tone="ok" list={done} empty="Chưa có bạn nào nộp." />
          <Group title="Đang làm" tone="doing" list={doing} />
          <Group title="Chưa làm" tone="none" list={none} empty="Cả lớp đã nộp." />
        </>
      )}
    </section>
  );
}
