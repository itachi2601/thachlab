import type { Metadata } from "next";
import ClassHubPage from "../page";
import { MANAGED_CLASSES, AVCN_CLASS_SLUG, CASIO_CLASS_SLUG, WORLDSKILLS_CLASS_SLUG, CNCTM_CLASS_SLUG, GCPT_CLASS_SLUG, CNCTM2_CLASS_SLUG } from "@/services/classes";

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

  if (classSlug === WORLDSKILLS_CLASS_SLUG) {
    return {
      title: "WorldSkills — Industrial Mechanics 2026 — CTTC",
      description: "Đề thi, thang điểm, phiếu tự chấm và thuật ngữ song ngữ Anh–Việt để huấn luyện sinh viên dự thi WorldSkills Skill 01 Industrial Mechanics.",
    };
  }

  if (classSlug === CNCTM_CLASS_SLUG) {
    return {
      title: "Công nghệ chế tạo máy 1 — CTTC",
      description: "Nguyên công, gá, bước, dạng sản xuất và các hình thức gia công cơ khí: bài lý thuyết tương tác có câu tự kiểm cho sinh viên Cơ khí.",
    };
  }

  if (classSlug === CNCTM2_CLASS_SLUG) {
    return {
      title: "Công nghệ chế tạo máy 2 — CTTC",
      description: "Quy trình công nghệ gia công chi tiết điển hình (trục, càng, bạc, hộp, bánh răng) và công nghệ lắp ráp: bài lý thuyết tương tác có câu tự kiểm cho sinh viên Cơ khí.",
    };
  }

  if (classSlug === GCPT_CLASS_SLUG) {
    return {
      title: "Gia công phi truyền thống — CTTC",
      description: "EDM, cắt dây, điện hoá, laser, tia nước, siêu âm, plasma, hoá học: nguyên lý, ưu nhược, ứng dụng và cách chọn công nghệ cho chi tiết.",
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
