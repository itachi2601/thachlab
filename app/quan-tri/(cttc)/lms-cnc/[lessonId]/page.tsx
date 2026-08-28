import { notFound } from "next/navigation";
import CncLmsAdmin from "@/components/admin/CncLmsAdmin";
import { CNC_COURSE_ITEMS } from "@/services/cnc-lms";

export const dynamicParams = false;

export function generateStaticParams() {
  return CNC_COURSE_ITEMS.map((item) => ({ lessonId: item.id }));
}

export default async function CncAdminLessonPage({ params }: { params: Promise<{ lessonId: string }> }) {
  const { lessonId } = await params;
  if (!CNC_COURSE_ITEMS.some((item) => item.id === lessonId)) notFound();
  return <CncLmsAdmin initialLessonId={lessonId} />;
}
