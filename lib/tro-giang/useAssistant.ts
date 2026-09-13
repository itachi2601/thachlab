"use client";

import { useEffect, useMemo, useState } from "react";
import { useAuth } from "@/components/auth/AuthProvider";
import { DEMO_QUERY_FLAG, demoAssistant, setTaDemoMode, useTaDemoMode } from "./demo";
import { getMyAssistant, type TaAssistant } from "./queries";

/**
 * Hồ sơ trợ giảng dùng cho mọi trang /tro-giang.
 * - assistant === undefined: đang tải
 * - assistant === null: tài khoản này chưa được đăng ký làm trợ giảng
 * - demo === true: giáo viên đang xem bản giả lập (xem lib/tro-giang/demo.ts)
 *
 * Chỉ role thật "admin" mới bật được chế độ giả lập — phòng cờ cũ còn sót trong
 * sessionStorage sau khi đổi tài khoản.
 */
export function useAssistantOrDemo(): { assistant: TaAssistant | null | undefined; demo: boolean } {
  const { session, realProfile, loading } = useAuth();
  const [demoFlag] = useTaDemoMode();
  const [fetched, setFetched] = useState<TaAssistant | null | undefined>(undefined);
  const fakeAssistant = useMemo(() => demoAssistant(), []);

  const isAdmin = realProfile?.role === "admin";
  const demo = demoFlag && isAdmin;

  // /tro-giang?gialap=1 — đường vào từ nút bên khu quản trị.
  useEffect(() => {
    if (loading || !isAdmin) return;
    const params = new URLSearchParams(window.location.search);
    if (params.get(DEMO_QUERY_FLAG) === "1") setTaDemoMode(true);
  }, [loading, isAdmin]);

  // Cờ còn sót lại ở tài khoản không phải admin — dọn luôn.
  useEffect(() => {
    if (!loading && demoFlag && realProfile && !isAdmin) setTaDemoMode(false);
  }, [loading, demoFlag, realProfile, isAdmin]);

  useEffect(() => {
    if (demo || !session) return;
    let cancelled = false;
    getMyAssistant(session.user.id)
      .then((a) => !cancelled && setFetched(a))
      .catch(() => !cancelled && setFetched(null));
    return () => {
      cancelled = true;
    };
  }, [demo, session]);

  return { assistant: demo ? fakeAssistant : fetched, demo };
}
