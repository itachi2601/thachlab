"use client";

import { useEffect } from "react";

/**
 * Cuộn tới phần tử trùng `location.hash` sau khi khối được dựng ở client.
 * Dùng cho trang mà nội dung chỉ xuất hiện sau hydrate (vd. trang khách /phu-huynh nằm sau
 * RequireAuth): trình duyệt tự cuộn lúc tải trang thì phần tử chưa tồn tại nên không cuộn.
 * Không render gì; chỉ chạy một lần khi mount.
 */
export default function ScrollToHash() {
  useEffect(() => {
    const id = window.location.hash.slice(1);
    if (!id) return;
    const el = document.getElementById(decodeURIComponent(id));
    if (!el) return;
    const frame = requestAnimationFrame(() => el.scrollIntoView({ block: "start" }));
    return () => cancelAnimationFrame(frame);
  }, []);
  return null;
}
