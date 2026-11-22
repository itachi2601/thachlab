"use client";
import dynamic from "next/dynamic";
import SucKhoeShell from "@/components/suc-khoe/SucKhoeShell";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

// Lộ trình tập tại nhà 6 bậc (đi bộ → tay không → Tabata/HIIT → phòng gym). Chỉ lưu trên máy, không gửi máy chủ.
const TapTaiNhaApp = dynamic(() => import("@/components/suc-khoe/TapTaiNhaApp"), { ssr: false });

export default function TapTaiNhaPage() {
  return (
    <SucKhoeShell title="Tập tại nhà" back={{ href: "/suc-khoe", label: "Về Sức khỏe" }}>
      <LazyErrorBoundary>
        <TapTaiNhaApp />
      </LazyErrorBoundary>
    </SucKhoeShell>
  );
}
