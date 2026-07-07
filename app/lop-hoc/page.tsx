"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { SkeletonGrid } from "@/components/ui/Skeleton";
import type { SchoolClass } from "@/features/exams/types";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import { fetchClasses } from "@/services/classes";
import {
  fetchPublishedExams,
  fetchPublishedPosts,
  type ExamMeta,
  type PostMeta,
} from "@/services/content";
import { useAuth } from "@/components/auth/AuthProvider";
import { supabaseConfigured } from "@/services/supabase";

export default function ClassHubPage() {
  const { session } = useAuth();
  const [classes, setClasses] = useState<SchoolClass[] | null>(null);
  const [activeId, setActiveId] = useState<number | null>(null);
  const [exams, setExams] = useState<ExamMeta[] | null>(null);
  const [posts, setPosts] = useState<PostMeta[] | null>(null);

  useEffect(() => {
    if (!supabaseConfigured) return;
    fetchClasses().then((cs) => {
      setClasses(cs);
      if (cs.length > 0) setActiveId((prev) => prev ?? cs[0].id);
    });
    fetchPublishedPosts().then(setPosts);
  }, []);

  // đề thi yêu cầu đăng nhập (RLS) — chỉ tải khi có session
  useEffect(() => {
    if (!supabaseConfigured || !session) return;
    fetchPublishedExams().then(setExams);
  }, [session]);

  const active = classes?.find((c) => c.id === activeId);
  const classPosts = (posts ?? []).filter((p) =>
    p.classIds.includes(activeId ?? -1),
  );
  const classExams = (exams ?? []).filter((e) =>
    e.classIds.includes(activeId ?? -1),
  );

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          Lớp <span className="text-gradient">học</span>
        </h1>
        <p className="mt-3 mb-8 text-slate-400">
          Chọn lớp để xem bài viết, đề thi và tài liệu dành riêng cho lớp đó.
        </p>

        {!supabaseConfigured ? (
          <p className="text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : !classes ? (
          <SkeletonGrid count={3} />
        ) : classes.length === 0 ? (
          <p className="text-slate-400">Chưa có lớp nào.</p>
        ) : (
          <>
            <div className="flex flex-wrap gap-2">
              {classes.map((c) => (
                <button
                  key={c.id}
                  onClick={() => setActiveId(c.id)}
                  style={
                    activeId === c.id
                      ? { backgroundColor: c.color, color: "#fff" }
                      : undefined
                  }
                  className={`rounded-full px-4 py-2 text-sm font-semibold transition-colors ${
                    activeId === c.id
                      ? ""
                      : "bg-white/5 text-slate-300 hover:bg-white/10"
                  }`}
                >
                  {c.icon && `${c.icon} `}
                  {c.name}
                </button>
              ))}
            </div>

            {active && (
              <div className="mt-10 space-y-12">
                <section>
                  <h2 className="mb-4 font-display text-xl font-semibold text-white">
                    Đề thi lớp {active.name}
                  </h2>
                  {!session ? (
                    <p className="text-sm text-slate-400">
                      <Link
                        href="/dang-nhap"
                        className="text-[#3B82F6] hover:underline"
                      >
                        Đăng nhập
                      </Link>{" "}
                      để xem đề thi của lớp.
                    </p>
                  ) : !exams ? (
                    <SkeletonGrid count={3} />
                  ) : classExams.length === 0 ? (
                    <p className="text-sm text-slate-400">
                      Chưa có đề nào gán riêng cho lớp này.
                    </p>
                  ) : (
                    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                      {classExams.map((exam) => (
                        <Link
                          key={exam.id}
                          href={`/kiem-tra/lam?id=${exam.id}`}
                          className="group rounded-2xl border border-white/10 bg-[#0B1020] p-6 transition-all hover:-translate-y-1 hover:border-[#3B82F6]/50"
                        >
                          <h3 className="font-display font-semibold text-white group-hover:text-[#3B82F6]">
                            {exam.title}
                          </h3>
                          <p className="mt-2 text-sm text-slate-400">
                            {exam.question_count} câu · {exam.duration_minutes}{" "}
                            phút
                            {exam.difficulty &&
                              ` · ${DIFFICULTY_LABELS[exam.difficulty]}`}
                          </p>
                        </Link>
                      ))}
                    </div>
                  )}
                </section>

                <section>
                  <h2 className="mb-4 font-display text-xl font-semibold text-white">
                    Bài viết lớp {active.name}
                  </h2>
                  {!posts ? (
                    <SkeletonGrid count={3} />
                  ) : classPosts.length === 0 ? (
                    <p className="text-sm text-slate-400">
                      Chưa có bài viết nào gán riêng cho lớp này.
                    </p>
                  ) : (
                    <div className="grid gap-5 sm:grid-cols-2">
                      {classPosts.map((p) => (
                        <Link
                          key={p.id}
                          href={`/tin-tuc#post-${p.id}`}
                          className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 transition-all hover:-translate-y-1 hover:border-[#3B82F6]/50"
                        >
                          <h3 className="font-display font-semibold text-white">
                            {p.title}
                          </h3>
                          <p className="mt-2 line-clamp-2 text-sm text-slate-400">
                            {p.body || (p.video_url && "🎬 Video bài giảng")}
                          </p>
                        </Link>
                      ))}
                    </div>
                  )}
                </section>
              </div>
            )}
          </>
        )}
      </main>
      <Footer />
    </>
  );
}
