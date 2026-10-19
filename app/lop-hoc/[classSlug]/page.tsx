import type { Metadata } from "next";
import ClassHubPage from "../page";
import { MANAGED_CLASSES, AVCN_CLASS_SLUG, CASIO_CLASS_SLUG } from "@/services/classes";

export const dynamicParams = false;

export function generateStaticParams() {
  return MANAGED_CLASSES.map((schoolClass) => ({ classSlug: schoolClass.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ classSlug: string }>;
}): Promise<Metadata> {
  const { classSlug } = await params;
  const schoolClass = MANAGED_CLASSES.find((item) => item.slug === classSlug);
  const className = schoolClass?.name === "KHTN 9" ? "KHTN 9" : `Lớp ${schoolClass?.name ?? "học"}`;

  // AVCN là học phần CTTC, không phải "Lớp …" của khối THPT.
  if (classSlug === AVCN_CLASS_SLUG) {
    return {
      title: "Anh văn chuyên ngành Cơ khí — CTTC",
      description: "Từ vựng, đọc hiểu tài liệu kỹ thuật và luyện đề cuối kỳ Anh văn chuyên ngành Cơ khí cho sinh viên CTTC.",
    };
  }

  if (classSlug === CASIO_CLASS_SLUG) {
    return {
      title: "Giải Vật lí trên máy tính cầm tay — Casio fx-580VN X",
      description: "Kỹ thuật bấm máy Casio fx-580VN X và bài luyện theo chuyên đề cho kỳ thi Giải Vật lí trên máy tính cầm tay.",
    };
  }

  return {
    title: `${className} — Không gian học tập`,
    description: `Bài giảng, bài tập và đề kiểm tra dành cho ${className}.`,
  };
}

export default async function SecondaryClassPage({
  params,
}: {
  params: Promise<{ classSlug: string }>;
}) {
  const { classSlug } = await params;
  return <ClassHubPage classSlug={classSlug} />;
}
