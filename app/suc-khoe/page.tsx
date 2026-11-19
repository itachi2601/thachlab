"use client";
import dynamic from "next/dynamic";
import SucKhoeShell from "@/components/suc-khoe/SucKhoeShell";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

// Đường vào mục Sức khỏe — các mô-đun khai báo ở lib/suc-khoe/modules.ts.
const SucKhoeHub = dynamic(() => import("@/components/suc-khoe/SucKhoeHub"), { ssr: false });

export default function SucKhoePage() {
  return (
    <SucKhoeShell title="Sức khỏe">
      <LazyErrorBoundary>
        <SucKhoeHub />
      </LazyErrorBoundary>
    </SucKhoeShell>
  );
}
