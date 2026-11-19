"use client";

import { useLayoutEffect, useState, type RefObject } from "react";
import { createPortal } from "react-dom";
import { ChargeInFieldSimulationLazy, GasGraphsSimulationLazy } from "@/components/physics/SimulationsLazy";

/**
 * Gắn mô phỏng tự kéo (C1, C2 — content/thi-nghiem/de-xuat-bo-sung-2026-11-12.md mục C) vào hộp
 * `<div class="tl-box tl-note tl-mo-phong" data-mo-phong="<khoá>">` trong HTML bài. Cùng cách với KhungPortals:
 * HTML bài là chuỗi tĩnh nên mô phỏng được vẽ bằng portal vào `div.tl-mo-phong-host` thêm cuối hộp; chữ tĩnh trong
 * hộp là phương án dự phòng (code cũ, khoá lạ) và chỉ bị ẩn khi đã có host (class `tl-mo-phong-on`).
 * Khoá lạ → để nguyên hộp tĩnh. Khối JS mô phỏng tải chậm (SimulationsLazy: next/dynamic ssr:false + LazyErrorBoundary).
 */
const MO_PHONG = {
  "do-thi-khi": GasGraphsSimulationLazy,
  "dien-tich-tu-truong": ChargeInFieldSimulationLazy,
} as const;
type Khoa = keyof typeof MO_PHONG;

type Host = { host: HTMLElement; khoa: Khoa; key: string };

export default function MoPhongPortals({ rootRef, version }: { rootRef: RefObject<HTMLElement | null>; version: string }) {
  const [hosts, setHosts] = useState<Host[]>([]);

  useLayoutEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    const found: Host[] = [];
    root.querySelectorAll<HTMLElement>(".tl-mo-phong[data-mo-phong]").forEach((box, i) => {
      const khoa = box.dataset.moPhong ?? "";
      if (!(khoa in MO_PHONG)) return;
      let host = box.querySelector<HTMLElement>(":scope > .tl-mo-phong-host");
      if (!host) {
        host = document.createElement("div");
        host.className = "tl-mo-phong-host";
        box.appendChild(host);
      }
      box.classList.add("tl-mo-phong-on");
      found.push({ host, khoa: khoa as Khoa, key: `${khoa}-${i}` });
    });
    setHosts(found);
  }, [rootRef, version]);

  return (
    <>
      {hosts.map((h) => {
        const Sim = MO_PHONG[h.khoa];
        return createPortal(<Sim />, h.host, h.key);
      })}
    </>
  );
}
