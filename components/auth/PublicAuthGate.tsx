"use client";

import { useEffect, useState, type ComponentType, type ReactNode } from "react";
import { hasStoredSupabaseSession } from "@/lib/supabase-env";

/**
 * Trang công khai không bọc AuthProvider sẵn (khách không tải supabase-js).
 * Nếu localStorage còn phiên thì mới nạp AuthProvider — Navbar hiện tên, admin thấy bảng việc hôm nay.
 */
export default function PublicAuthGate({ children }: { children: ReactNode }) {
  const [Provider, setProvider] = useState<ComponentType<{ children: ReactNode }> | null>(null);

  useEffect(() => {
    if (!hasStoredSupabaseSession()) return;
    let cancelled = false;
    import("@/components/auth/AuthProvider").then((mod) => {
      if (!cancelled) setProvider(() => mod.default);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  if (!Provider) return <>{children}</>;
  return <Provider>{children}</Provider>;
}
