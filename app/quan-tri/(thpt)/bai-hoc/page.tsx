import { Suspense } from "react";
import LessonsAdmin from "@/components/admin/LessonsAdmin";

export default function Page() {
  return (
    <Suspense fallback={null}>
      <LessonsAdmin />
    </Suspense>
  );
}
