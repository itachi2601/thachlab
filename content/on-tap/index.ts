import type { BoOnTap } from "@/components/lessons/OnNamPhut";

/**
 * Bộ thẻ "Ôn 5 phút" theo slug bài. Import tường minh từng file (không template literal) để bundler chỉ tách
 * đúng các JSON này thành chunk riêng. Thêm bài: chạy scripts/on-tap/rut-the-on.py rồi thêm một dòng ở đây.
 */
export const BO_ON_TAP: Record<string, () => Promise<BoOnTap>> = {
  "l11-cuong-do-dong-dien": () => import("./l11-cuong-do-dong-dien.json").then((m) => m.default as BoOnTap),
  "l11-dien-tro-dinh-luat-ohm": () => import("./l11-dien-tro-dinh-luat-ohm.json").then((m) => m.default as BoOnTap),
  "l11-nguon-dien": () => import("./l11-nguon-dien.json").then((m) => m.default as BoOnTap),
};
