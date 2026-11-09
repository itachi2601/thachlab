import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { BAI_DOC, nhanBai } from "@/lib/shcn/bai-doc";
import { readBaiDoc } from "@/lib/shcn/bai-doc-server";

// Bài đọc SHCN cho sinh viên lớp chủ nhiệm (bản .sv.md). Sinh viên vào từ thẻ tuần ở /tai-khoan
// → "Sinh hoạt lớp"; không có trang danh sách (N1/N2: mỗi tuần một bài, không phô 95 bài).
// Kịch bản giảng viên không bao giờ build ra đây.

export const dynamicParams = false;

export function generateStaticParams() {
  return BAI_DOC.map((item) => {
    const [hk, bai] = item.key.split("/");
    return { hk, bai };
  });
}

type Params = Promise<{ hk: string; bai: string }>;

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { hk, bai } = await params;
  const doc = readBaiDoc(hk, bai);
  return {
    title: { absolute: `${doc?.ten ?? "Sinh hoạt lớp"} | ThachLab` },
    description: doc?.muc_tieu,
    robots: { index: false, follow: false },
  };
}

export default async function BaiDocPage({ params }: { params: Params }) {
  const { hk, bai } = await params;
  const doc = readBaiDoc(hk, bai);
  if (!doc) notFound();

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-2xl px-4 pt-24 pb-20 sm:px-6">
        <nav aria-label="Breadcrumb" className="text-sm text-slate-500">
          <Link href="/tai-khoan" className="text-primary hover:underline">
            Sinh hoạt lớp
          </Link>
          <span className="mx-2">/</span>
          <span>
            HK{doc.hk} · {nhanBai(doc.bai)}
          </span>
        </nav>
        <article className="mt-3">
          <h1 className="font-display text-2xl font-bold leading-tight text-ink sm:text-3xl">{doc.ten}</h1>
          {doc.muc_tieu && <p className="mt-3 text-base text-slate-500">{doc.muc_tieu}</p>}
          <div className="blog-prose shcn-prose mt-6" dangerouslySetInnerHTML={{ __html: doc.html }} />
        </article>
      </main>
      <Footer />
    </>
  );
}
