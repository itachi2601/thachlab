import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import CncEnrollmentGate from "@/components/lessons/CncEnrollmentGate";
import { CNC_COURSE_ITEMS } from "@/services/cnc-lms";

export const dynamicParams = false;

export function generateStaticParams() {
  return CNC_COURSE_ITEMS.filter((item) => item.id !== "intro").map((item) => ({ lessonId: item.id }));
}

export async function generateMetadata({ params }: { params: Promise<{ lessonId: string }> }): Promise<Metadata> {
  const { lessonId } = await params;
  const lesson = CNC_COURSE_ITEMS.find((item) => item.id === lessonId && item.id !== "intro");
  return { title: lesson ? `${lesson.shortTitle} — Gia công CNC` : "Bài học CNC" };
}

export default async function CncLessonPage({ params }: { params: Promise<{ lessonId: string }> }) {
  const { lessonId } = await params;
  if (!CNC_COURSE_ITEMS.some((item) => item.id === lessonId && item.id !== "intro")) notFound();
  return <><Navbar /><main className="cnc-page pt-[76px]"><CncEnrollmentGate lessonId={lessonId} /></main><Footer /></>;
}
