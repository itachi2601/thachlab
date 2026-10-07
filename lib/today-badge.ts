"use client";

/**
 * Chấm đỏ "Hôm nay" trên thanh đáy học sinh: có việc cần làm hôm nay (bài giao chưa làm, bài kế, BTVN, phụ đạo).
 * ThptStudentHome đã tính sẵn "việc hôm nay" nên chỉ ghi lại kết quả ở đây — thanh đáy đọc, KHÔNG thêm truy vấn Supabase nào.
 * Lưu theo user + ngày trong localStorage để sang trang khác / tải lại vẫn còn chấm; sang ngày mới thì tự hết cho tới khi em mở trang Hôm nay.
 */
import { useSyncExternalStore } from "react";

const EVENT = "thachlab-today-badge";
const keyOf = (userId: string) => `thachlab-today-badge:${userId}`;
const today = () => new Date().toLocaleDateString("sv-SE"); // YYYY-MM-DD theo giờ máy

export function setTodayBadge(userId: string, on: boolean) {
  try {
    if (on) window.localStorage.setItem(keyOf(userId), today());
    else window.localStorage.removeItem(keyOf(userId));
  } catch {
    /* localStorage bị chặn — không có chấm, trang vẫn chạy */
  }
  window.dispatchEvent(new Event(EVENT));
}

function subscribe(onChange: () => void) {
  window.addEventListener(EVENT, onChange);
  window.addEventListener("storage", onChange);
  return () => {
    window.removeEventListener(EVENT, onChange);
    window.removeEventListener("storage", onChange);
  };
}

export function useTodayBadge(userId: string | null): boolean {
  return useSyncExternalStore(
    subscribe,
    () => {
      if (!userId) return false;
      try {
        return window.localStorage.getItem(keyOf(userId)) === today();
      } catch {
        return false;
      }
    },
    () => false,
  );
}
