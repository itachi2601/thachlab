"use client";

import dynamic from "next/dynamic";
import type { ComponentType } from "react";

/**
 * Danh bạ mô phỏng gắn vào bài học bằng <div data-sim="<id thí nghiệm>"> (xem content/thi-nghiem/).
 * Mỗi mô phỏng là một chunk riêng (next/dynamic, ssr:false) — chỉ tải khi bài có thẻ và thẻ gần vào màn
 * hình (SimPortals). id phải trùng tên file trong content/thi-nghiem/.
 */
export const SIMULATIONS: Record<string, ComponentType> = {
  "tn-l10-newton3-04": dynamic(() => import("./TwoBodyPushSim"), {
    ssr: false,
    loading: () => <p className="tl-sim__loading">Đang tải mô phỏng…</p>,
  }),
};
