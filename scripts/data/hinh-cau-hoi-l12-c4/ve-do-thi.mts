// Đồ thị cho câu chương 4 L12 (Vật lí hạt nhân) bằng services/figure-spec.ts. Chạy: npx tsx scripts/data/hinh-cau-hoi-l12-c4/ve-do-thi.mts
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { renderFigureSpec, type FigureSpec } from "../../../services/figure-spec.ts";
const out = path.join(path.dirname(fileURLToPath(import.meta.url)), "svg");
const put = (id: number, s: FigureSpec) => fs.writeFileSync(path.join(out, `${id}.svg`), renderFigureSpec(s));

// 1549418: N_X giảm, N_Y tăng, cắt nhau tại τ. Trục t không chia theo T (không lộ đáp án τ = T).
const tau = 1 / Math.LN2; // T = 1
put(1549418, {
  kind: "plot", xLabel: "t", yLabel: "N", xRange: [0, 4.2], yRange: [0, 1.15],
  xTicks: [{ v: 1, label: "τ" }], yTicks: [{ v: 1, label: "N₀" }],
  series: [
    { type: "exponential", y0: 1, tau, yInf: 0, domain: [0, 4], label: "X", color: "#2563eb" },
    { type: "exponential", y0: -1, tau, yInf: 1, domain: [0, 4], label: "Y", color: "#dc2626" },
  ],
  guides: [{ x: 1 }],
});

// 735961, 1550727, 1552351: năng lượng liên kết riêng theo A (số liệu chuẩn, MeV/nuclôn).
const bind: FigureSpec = {
  kind: "plot", xLabel: "A", yLabel: "Wlk/A (MeV/nuclôn)", xRange: [0, 250], yRange: [0, 10],
  xTicks: [50, 100, 150, 200].map((v) => ({ v })), yTicks: [2, 4, 6, 8].map((v) => ({ v })),
  series: [{
    type: "polyline", color: "#2563eb",
    points: [[2, 1.11], [3, 2.57], [4, 7.07], [6, 5.33], [7, 5.61], [9, 6.46], [12, 7.68], [16, 7.98], [20, 8.03], [24, 8.26],
      [28, 8.45], [40, 8.55], [56, 8.79], [62, 8.79], [84, 8.72], [120, 8.5], [150, 8.25], [208, 7.87], [238, 7.57]],
  }],
  points: [{ x: 2, y: 1.11, label: "H-2" }, { x: 56, y: 8.79, label: "Fe-56" }, { x: 235, y: 7.59, label: "U-235" }],
};
for (const id of [735961, 1550727, 1552351]) put(id, bind);
