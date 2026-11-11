"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import SoDoTuDuy from "@/components/lessons/so-do/SoDoTuDuy";
import { napSoDoChuong } from "@/features/lessons/so-do-tu-duy";
import type { SoDoChuong } from "@/features/lessons/so-do-tu-duy/types";

/**
 * Sơ đồ tư duy của một chương — mở từ dòng "Sơ đồ tư duy chương" ở cuối chương trên trang lớp.
 * `/lop-hoc/so-do/?chuong=<chapters.id>&lop=<slug lớp>`. Nội dung tĩnh trong bundle, không gọi Supabase.
 */
function NoiDung() {
  const q = useSearchParams();
  const chuong = Number(q.get("chuong"));
  const lop = q.get("lop");
  const [data, setData] = useState<SoDoChuong | null | undefined>(undefined);

  useEffect(() => {
    let con = true;
    napSoDoChuong(chuong).then((d) => con && setData(d));
    return () => {
      con = false;
    };
  }, [chuong]);

  const veLop = lop && /^[a-z0-9-]+$/.test(lop) ? `/lop-hoc/${lop}/?chapter=${chuong}` : "/lop-hoc/";

  return (
    <>
      <div className="mx-auto w-full max-w-6xl px-4 pt-20 sm:px-5 sm:pt-24">
        <Link
          prefetch={false}
          href={veLop}
          className="inline-flex min-h-11 items-center gap-1.5 text-[15px] font-semibold text-muted hover:text-ink"
        >
          <ArrowLeft size={16} aria-hidden /> Về danh sách bài
        </Link>
      </div>
      {data === undefined ? (
        <p className="mx-auto max-w-6xl px-4 py-10 text-[15px] text-muted sm:px-5">Đang mở sơ đồ…</p>
      ) : data === null ? (
        <p className="mx-auto max-w-6xl px-4 py-10 text-[15px] text-muted sm:px-5">Chương này chưa có sơ đồ tư duy.</p>
      ) : (
        <SoDoTuDuy data={data} />
      )}
    </>
  );
}

export default function SoDoChuongPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-bg pb-16">
        <Suspense fallback={null}>
          <NoiDung />
        </Suspense>
      </main>
      <Footer variant="app" />
    </>
  );
}
