"use client";

import { useEffect, useState } from "react";

/** Trình duyệt nhúng của Messenger, Zalo, Instagram, Line hay chặn đăng nhập và lưu phiên. */
export function isInAppBrowser(ua: string) {
  return /FBAN|FBAV|FB_IAB|Instagram|Messenger|\bZalo\b|ZaloTheme|Line\//i.test(ua);
}

/** Chỉ hiện khi đúng trình duyệt nhúng (N1, N3). Chữ 16px (C1). */
export default function InAppBrowserNotice() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    setShow(isInAppBrowser(navigator.userAgent));
  }, []);
  if (!show) return null;
  return (
    <p className="mb-4 rounded-xl border border-amber-400/40 bg-amber-500/10 px-4 py-3 text-base leading-relaxed text-amber-50">
      Trang đang mở trong Messenger hoặc Zalo. Em sao chép địa chỉ rồi dán vào Safari hoặc Chrome để đăng nhập được.
    </p>
  );
}
