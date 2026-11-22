"use client";
import dynamic from "next/dynamic";
import SucKhoeShell from "@/components/suc-khoe/SucKhoeShell";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

// Ứng dụng tập gym kiểu Hevy (chương trình A/B/C ở lib/tap-luyen/chuong-trinh.ts). ?buoi=A|B|C, ?tab=so-do|lich-su|tien-bo
const TapLuyenApp = dynamic(() => import("@/components/tap-luyen/TapLuyenApp"), { ssr: false });

export default function TapLuyenPage() {
  return (
    <SucKhoeShell title="Tập luyện" back={{ href: "/suc-khoe", label: "Về Sức khỏe" }}>
      <LazyErrorBoundary>
        <TapLuyenApp />
      </LazyErrorBoundary>
    </SucKhoeShell>
  );
}
