// Dựng SVG đồ thị thí điểm bằng services/figure-spec.ts (toạ độ tính bằng mã, khớp vạch chia).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { renderFigureSpec, type FigureSpec } from "../../../services/figure-spec.ts";
const out = path.join(path.dirname(fileURLToPath(import.meta.url)), "svg");
const put = (id: number, s: FigureSpec) => fs.writeFileSync(path.join(out, `${id}.svg`), renderFigureSpec(s));

// 1531526: v–t của hai xe cắt nhau tại t1 (không số liệu: đề chỉ cho giao điểm)
put(1531526, {
  kind: "plot", xLabel: "t", yLabel: "v", xRange: [0, 10], yRange: [0, 10],
  xTicks: [{ v: 5, label: "t₁" }], yTicks: [],
  series: [
    { type: "polyline", points: [[0, 2], [10, 8]], label: "xe 1", color: "#2563eb" },
    { type: "polyline", points: [[0, 8], [10, 2]], label: "xe 2", color: "#dc2626" },
  ],
  guides: [{ x: 5 }],
});
