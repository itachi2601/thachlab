"use client";
import dynamic from "next/dynamic";
import SucKhoeShell from "@/components/suc-khoe/SucKhoeShell";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

// Dinh dưỡng: năng lượng mục tiêu (Mifflin–St Jeor) + nhật ký ăn theo ngày + chỉnh theo xu hướng cân.
const DinhDuongApp = dynamic(() => import("@/components/suc-khoe/DinhDuongApp"), { ssr: false });

export default function DinhDuongPage() {
  return (
    <SucKhoeShell title="Dinh dưỡng" back={{ href: "/suc-khoe", label: "Về Sức khỏe" }}>
      <LazyErrorBoundary>
        <DinhDuongApp />
      </LazyErrorBoundary>
    </SucKhoeShell>
  );
}
