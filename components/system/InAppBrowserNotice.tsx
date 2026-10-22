"use client";

import { useSyncExternalStore } from "react";

/** Trình duyệt nhúng của Messenger, Zalo, Instagram, Line hay chặn đăng nhập và lưu phiên. */
export function isInAppBrowser(ua: string) {
  return /FBAN|FBAV|FB_IAB|Instagram|Messenger|\bZalo\b|ZaloTheme|Line\//i.test(ua);
}

const subscribe = () => () => {};
const getSnapshot = () => typeof navigator !== "undefined" && isInAppBrowser(navigator.userAgent);
const getServerSnapshot = () => false;

/** Chỉ hiện khi đúng trình duyệt nhúng (N1, N3). Chữ 16px (C1). */
export default function InAppBrowserNotice() {
  const show = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
  if (!show) return null;
  return (
    <p className="mb-4 rounded-xl border border-amber-400/40 bg-amber-500/10 px-4 py-3 text-base leading-relaxed text-amber-50">
      Trang đang mở trong Messenger hoặc Zalo. Em sao chép địa chỉ rồi dán vào Safari hoặc Chrome để đăng nhập được.
    </p>
  );
}
