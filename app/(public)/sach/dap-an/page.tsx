"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ContentHtml from "@/components/exams/ContentHtml";

/**
 * Đáp án & gợi ý đi kèm SÁCH IN (book/): quét mã QR cuối bài trong sách → /sach/dap-an/?bai=<lesson id>.
 * Dữ liệu là file tĩnh public/sach-data/dap-an-<id>.json do `book/build.py` sinh ra (cùng số thứ tự
 * với các ô "đáp án số n" in trong sách). Trang công khai, không cần đăng nhập, không gọi Supabase.
 */

type KeyItem = {
  n: number;
  kind: "quiz" | "selfq" | "fill" | "thuthach";
  tag: string;
  where?: string;
  letter?: string;
  q?: string;
  ok?: string;
  no?: string;
  body?: string;
};
type Formula = { n: number; tex: string; display: boolean };
type Worked = { n: number; label: string; title: string; solution: string };
type Answers = {
  lessonId: number;
  title: string;
  chapter: string;
  formulas: Formula[];
  items: KeyItem[];
  worked: Worked[];
};

const BODY = "text-sm leading-relaxed text-slate-300 [&_p]:mb-2";

function Badge({ n }: { n: number }) {
  return (
    <span className="inline-flex h-6 min-w-6 items-center justify-center rounded-md bg-white/10 px-1.5 text-xs font-bold text-white">
      {n}
    </span>
  );
}

function Section({ title, hint, children }: { title: string; hint?: string; children: React.ReactNode }) {
  return (
    <section className="mt-8">
      <h2 className="font-display text-xl font-semibold text-white">{title}</h2>
      {hint && <p className="mt-1 text-sm text-slate-400">{hint}</p>}
      <div className="mt-4 space-y-3">{children}</div>
    </section>
  );
}

function AnswersView({ id }: { id: string }) {
  const [data, setData] = useState<Answers | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    if (!/^\d+$/.test(id)) {
      setFailed(true);
      return;
    }
    let alive = true;
    fetch(`/sach-data/dap-an-${id}.json`)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((d: Answers) => alive && setData(d))
      .catch(() => alive && setFailed(true));
    return () => {
      alive = false;
    };
  }, [id]);

  if (failed) {
    return (
      <p className="mt-8 rounded-xl border border-white/10 bg-panel p-5 text-slate-300">
        Chưa có đáp án cho bài này. Kiểm tra lại mã QR trong sách hoặc mở bài trên{" "}
        <Link href="/lop-hoc/" className="text-primary hover:underline">
          trang lớp học
        </Link>
        .
      </p>
    );
  }
  if (!data) return <p className="mt-8 text-slate-400">Đang tải…</p>;

  const quizzes = data.items.filter((i) => i.kind === "quiz");
  const selfs = data.items.filter((i) => i.kind !== "quiz");

  return (
    <>
      <p className="text-xs font-semibold tracking-widest text-slate-500">{data.chapter}</p>
      <h1 className="mt-1 font-display text-3xl font-bold text-white sm:text-4xl">{data.title}</h1>
      <p className="mt-3 text-slate-400">
        Đáp án & gợi ý cho các ô trống và câu hỏi in trong sách. Làm xong trên giấy rồi hãy mở. Số thứ tự trùng với số in
        trong sách.
      </p>
      <Link
        href={`/lop-hoc/bai?id=${data.lessonId}`}
        className="mt-4 inline-block rounded-lg border border-white/15 px-4 py-2 text-sm text-white hover:bg-white/5"
      >
        Mở bài này để xem mô phỏng, luyện tập và giải đề →
      </Link>

      {data.formulas.length > 0 && (
        <Section title="Ô điền công thức" hint="Ô vuông nhỏ có số trong phần lý thuyết.">
          <div className="grid gap-3 sm:grid-cols-2">
            {data.formulas.map((f) => (
              <div key={f.n} className="flex items-center gap-3 rounded-xl border border-white/10 bg-panel p-4">
                <Badge n={f.n} />
                <ContentHtml html={f.display ? `$$${f.tex}$$` : `$${f.tex}$`} className="text-white" />
              </div>
            ))}
          </div>
        </Section>
      )}

      {quizzes.length > 0 && (
        <Section title="Câu trắc nghiệm" hint="Đáp án đúng và phân tích lỗi thường gặp.">
          {quizzes.map((k) => (
            <article key={k.n} className="rounded-xl border border-white/10 bg-panel p-4">
              <div className="flex items-center gap-3">
                <Badge n={k.n} />
                <span className="text-sm font-semibold text-white">
                  {k.tag} {k.where ? <span className="font-normal text-slate-500">· mục {k.where}</span> : null}
                </span>
                <span className="ml-auto inline-flex h-7 w-7 items-center justify-center rounded-full border border-emerald-400/60 text-sm font-bold text-emerald-300">
                  {k.letter}
                </span>
              </div>
              {k.ok && <ContentHtml html={k.ok} className={`mt-3 block ${BODY}`} />}
              {k.no && (
                <div className="mt-2 border-t border-white/10 pt-2">
                  <p className="text-xs font-semibold text-slate-400">Nếu em chọn sai</p>
                  <ContentHtml html={k.no} className={`mt-1 block ${BODY}`} />
                </div>
              )}
            </article>
          ))}
        </Section>
      )}

      {selfs.length > 0 && (
        <Section title="Câu tự hỏi, trả bài & thử thách" hint="Đối chiếu với câu em đã viết trong sách.">
          {selfs.map((k) => (
            <article key={k.n} className="rounded-xl border border-white/10 bg-panel p-4">
              <div className="flex items-center gap-3">
                <Badge n={k.n} />
                <span className="text-sm font-semibold text-white">
                  {k.tag} {k.where ? <span className="font-normal text-slate-500">· mục {k.where}</span> : null}
                </span>
              </div>
              {k.q && <ContentHtml html={k.q} className={`mt-2 block font-semibold ${BODY}`} />}
              {k.body && <ContentHtml html={k.body} className={`mt-2 block ${BODY}`} />}
            </article>
          ))}
        </Section>
      )}

      {data.worked.length > 0 && (
        <Section title="Lời giải bài tập mẫu" hint="Xem sau khi em đã tự điền bảng phân tích đề.">
          {data.worked.map((w) => (
            <details key={w.n} className="rounded-xl border border-white/10 bg-panel p-4">
              <summary className="cursor-pointer text-sm font-semibold text-white">
                {w.label} <span className="font-normal text-slate-400">· {w.title}</span>
              </summary>
              <ContentHtml html={w.solution} className={`mt-3 block ${BODY}`} />
            </details>
          ))}
        </Section>
      )}
    </>
  );
}

function Inner() {
  const id = useSearchParams().get("bai") ?? "";
  return <AnswersView id={id} />;
}

export default function BookAnswersPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-3xl px-6 pb-24 pt-28 lg:px-8">
        <Suspense fallback={<p className="text-slate-400">Đang tải…</p>}>
          <Inner />
        </Suspense>
      </main>
      <Footer />
    </>
  );
}
