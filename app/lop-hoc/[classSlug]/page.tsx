import type { Metadata } from "next";
import ClassHubPage from "../page";
import { MANAGED_CLASSES } from "@/services/classes";

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
