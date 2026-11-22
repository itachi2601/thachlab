import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import MoPhongTheoSlug from "@/components/mo-phong/MoPhongTheoSlug";
import { MO_PHONG_TRANG } from "@/lib/mo-phong-trang";

// Trang riêng đã viết tay (vd giao-thoa-am) không đi qua đây.
const TRANG = MO_PHONG_TRANG.filter((m) => !m.rieng);

export const dynamicParams = false;

export function generateStaticParams() {
  return TRANG.map((m) => ({ slug: m.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const m = TRANG.find((x) => x.slug === slug);
  if (!m) return {};
  return { title: m.ten, description: m.mo_ta, alternates: { canonical: `/mo-phong/${m.slug}` } };
}

export default async function MoPhongSlugPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const m = TRANG.find((x) => x.slug === slug);
  if (!m) notFound();
  const hocTiep = m.lesson_id ? `/dang-nhap?next=${encodeURIComponent(`/lop-hoc/bai?id=${m.lesson_id}`)}` : "/dang-ky";
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-4xl px-4 pb-24 pt-28 lg:px-8">
        <p className="text-base">
          <Link href="/mo-phong" className="inline-flex min-h-12 items-center font-medium text-primary hover:underline">
            ← Thư viện mô phỏng
          </Link>
        </p>
        <h1 className="font-display text-2xl font-semibold text-ink sm:text-3xl">{m.ten}</h1>
        <p className="mt-2 text-lg leading-relaxed text-ink">{m.mo_ta}</p>
        {m.nhiem_vu && (
          <p className="mt-3 rounded-xl border border-line bg-panel p-4 text-lg leading-relaxed text-ink">
            <span className="font-semibold">Việc cần làm:</span> {m.nhiem_vu}
            {m.khoa_doan && <span className="mt-1 block text-muted">Chọn một đáp án dự đoán bên dưới để mở mô phỏng.</span>}
          </p>
        )}
        <div className="mt-6">
          <MoPhongTheoSlug slug={m.slug} />
        </div>
        <p className="mt-8 text-lg leading-relaxed text-ink">
          Mô phỏng này nằm trong một bài học có dự đoán trước và câu hỏi sau.{" "}
          <Link href={hocTiep} className="font-semibold text-primary underline-offset-4 hover:underline">
            {m.lesson_id ? "Học tiếp trong bài (cần đăng nhập)" : "Đăng ký để học cả bài"}
          </Link>
        </p>
      </main>
      <Footer />
    </>
  );
}
