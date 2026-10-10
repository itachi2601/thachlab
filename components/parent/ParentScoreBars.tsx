import { gradeBand, scoreText, shortDate } from "@/lib/parent-format";

/**
 * Biểu đồ cột các bài gần nhất cho phụ huynh. Khác biểu đồ đường của học sinh (P20):
 *  - số điểm in thẳng trên đầu cột (không phải đọc trục), chữ ≥15px;
 *  - không có trục, không có lưới — chỉ một vạch mốc 6,5 (và vạch mục tiêu nếu phụ huynh đặt);
 *  - cả chuỗi điểm cũng có trong aria-label, để không ai phải so sánh chiều cao cột bằng mắt.
 * Cột luôn có SỐ + màu xếp loại, màu không phải kênh duy nhất (P12).
 */
export interface BarPoint {
  score: number;
  at: string;
}

const PLOT_PX = 120;

export default function ParentScoreBars({ points, goal }: { points: BarPoint[]; goal?: number | null }) {
  const shown = points.slice(-6);
  if (shown.length < 2) return null;
  const summary = shown.map((p) => scoreText(p.score)).join(", ");
  const at = (v: number) => (v / 10) * PLOT_PX;

  return (
    <figure className="mt-4" role="img" aria-label={`Điểm các bài gần nhất, từ cũ đến mới: ${summary}`}>
      <div className="relative" style={{ height: PLOT_PX + 28 }}>
        <div className="absolute inset-x-0 bottom-0" style={{ height: PLOT_PX }}>
          <span
            className="pointer-events-none absolute inset-x-0 border-t border-dashed border-slate-400/60"
            style={{ bottom: at(6.5) }}
          />
          <span className="absolute right-0 text-[15px] text-muted" style={{ bottom: at(6.5) + 1 }}>
            6,5
          </span>
          {goal ? (
            <span
              className="pointer-events-none absolute inset-x-0 border-t-2 border-cyan-600"
              style={{ bottom: at(goal) }}
            />
          ) : null}
          <div className="absolute inset-0 flex items-end justify-around gap-1.5 pl-1 pr-9">
            {shown.map((p) => {
              const band = gradeBand(p.score);
              return (
                <div key={p.at} className="relative flex h-full w-full max-w-14 flex-col items-center justify-end">
                  <span
                    className="parent-num mb-1 text-lg font-bold text-ink"
                    style={{ position: "absolute", bottom: at(p.score) }}
                  >
                    {scoreText(p.score)}
                  </span>
                  <span className={`block w-full rounded-t-md ${band.bar}`} style={{ height: at(p.score) }} />
                </div>
              );
            })}
          </div>
        </div>
      </div>
      <div className="flex justify-around gap-1.5 pl-1 pr-9 pt-1.5">
        {shown.map((p) => (
          <span key={p.at} className="parent-num w-full max-w-14 whitespace-nowrap text-center text-[15px] text-muted">
            {shortDate(p.at)}
          </span>
        ))}
      </div>
      <figcaption className="mt-2 text-[15px] text-muted">
        Mỗi cột là một bài, từ cũ (trái) đến mới (phải). Vạch đứt là mốc 6,5 (bắt đầu mức Khá).
        {goal ? ` Vạch xanh liền là mục tiêu ${scoreText(goal)} do phụ huynh chọn.` : ""}
      </figcaption>
    </figure>
  );
}
