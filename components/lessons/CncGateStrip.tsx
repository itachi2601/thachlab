"use client";

import { CheckCircle2, Circle, CircleDot, Hourglass, LockKeyhole } from "lucide-react";
import type { CncGateState, CncGateStatus, CncSectionKind } from "@/services/cnc-progress";

// Dải 5 cổng G1–G5 ở đầu trang khoá CNC (docs/CNC-FLIPPED-THIET-KE-LAI-2026-11-08.md mục 4.2).
// M4: trạng thái luôn có chữ + biểu tượng; D2: mỗi ô ≥44px; B2/L5: chỉ cổng tiếp theo được tô nổi + 1 dòng việc tiếp theo; B6: ≤15% màn 375px.
const STATUS: Record<CncGateStatus, { label: string; Icon: typeof Circle }> = {
  dat: { label: "Đạt", Icon: CheckCircle2 },
  cho_duyet: { label: "Chờ duyệt", Icon: Hourglass },
  dang_lam: { label: "", Icon: CircleDot },
  chua_lam: { label: "Chưa làm", Icon: Circle },
  khoa: { label: "Chưa mở", Icon: LockKeyhole },
};

const statusText = (state: CncGateState) => (state.status === "dang_lam" ? `${state.done}/${state.total}` : STATUS[state.status].label);

export default function CncGateStrip({ states, onOpen }: { states: CncGateState[]; onOpen: (lessonId: string, section: CncSectionKind) => void }) {
  const currentIndex = states.findIndex((state) => state.status !== "dat");
  const current = currentIndex >= 0 ? states[currentIndex] : null;
  const caption = !current
    ? "Đã đạt cả 5 cổng năng lực."
    : current.status === "cho_duyet"
      ? `${current.gate.id} ${current.gate.title}: đã làm đủ bài, chờ giảng viên duyệt tại xưởng.`
      : current.status === "khoa"
        ? `${current.gate.id} ${current.gate.title} chưa mở — giảng viên sẽ mở khi lớp tới bài này.`
        : `Tiếp theo: ${current.gate.id} ${current.gate.title} — còn ${current.total - current.done} bài.`;

  return (
    <nav className="cnc-gates" aria-label="Năm cổng năng lực">
      <ol>
        {states.map((state, index) => {
          const { Icon } = STATUS[state.status];
          // Cổng chưa mở: bấm thì đưa tới việc còn thiếu gần nhất ở cổng trước.
          const target = state.next ?? (state.status === "khoa" ? states.slice(0, index).reverse().find((item) => item.next)?.next ?? null : null);
          const text = statusText(state);
          return (
            <li key={state.gate.id}>
              <button
                type="button"
                className={`cnc-gate is-${state.status}`}
                aria-current={index === currentIndex ? "step" : undefined}
                aria-label={`${state.gate.id} ${state.gate.title}: ${state.status === "dang_lam" ? `đã đạt ${text} bài` : text}`}
                title={`${state.gate.id} ${state.gate.title}`}
                disabled={!target}
                onClick={() => target && onOpen(target.lessonId, target.section)}
              >
                <span className="cnc-gate-head">
                  <Icon size={14} aria-hidden="true" />
                  <b>{state.gate.id}</b>
                  <span className="cnc-gate-name">{state.gate.title}</span>
                </span>
                <small>{text}</small>
              </button>
            </li>
          );
        })}
      </ol>
      <p>{caption}</p>
    </nav>
  );
}
