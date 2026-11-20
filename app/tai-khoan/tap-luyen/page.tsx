"use client";
import { useEffect } from "react";

// Địa chỉ cũ (18/11/2026) → ứng dụng tập nay nằm trong mục Sức khỏe. Giữ trang này cho link/lịch tuần cũ.
export default function TapLuyenCu() {
  useEffect(() => {
    window.location.replace(`/suc-khoe/tap-luyen/${window.location.search}`);
  }, []);
  return <p className="p-8 text-center text-sm text-muted">Đang chuyển tới mục Sức khỏe…</p>;
}
