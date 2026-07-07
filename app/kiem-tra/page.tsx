"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { SkeletonGrid } from "@/components/ui/Skeleton";
import { useAuth } from "@/components/auth/AuthProvider";
import type { SchoolClass, Difficulty } from "@/features/exams/types";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import { fetchClasses, fetchMyClassIds } from "@/services/classes";
import {
  fetchPublishedExams,
  visibleTo,
  type ExamMeta,
} from "@/services/content";

const selectCls =
  "rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-sm text-white focus:border-[#3B82F6] focus:outline-none";

const PAGE_SIZE = 12;

function ExamList() {
  const { session, profile } = useAuth();
  const [exams, setExams] = useState<ExamMeta[] | null>(null);
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [myClassIds, setMyClassIds] = useState<number[] | null>(null);

  const [search, setSearch] = useState("");
  const [classFilter, setClassFilter] = useState<number | 0>(0);
  const [topicFilter, setTopicFilter] = useState("");
  const [diffFilter, setDiffFilter] = useState<Difficulty | "all">("all");
  const [durFilter, setDurFilter] = useState<"all" | "short" | "medium" | "long">("all");
  const [page, setPage] = useState(1);

  const isAdmin = profile?.role === "admin";

  useEffect(() => {
    if (!session) return;
    fetchPublishedExams().then(setExams);
    fetchClasses().then(setClasses);
    if (!isAdmin) fetchMyClassIds(session.user.id).then(setMyClassIds);
  }, [session, isAdmin]);

  const effectiveClassIds = isAdmin ? null : myClassIds;

  const topics = useMemo(
    () => [...new Set((exams ?? []).map((e) => e.topic).filter(Boolean))],
    [exams],
  );

  const filtered = useMemo(
    () =>
      (exams ?? []).filter((e) => {
        if (!visibleTo(e.classIds, effectiveClassIds)) return false;
        if (classFilter && !e.classIds.includes(classFilter)) return false;
        if (topicFilter && e.topic !== topicFilter) return false;
        if (diffFilter !== "all" && e.difficulty !== diffFilter) return false;
        if (durFilter === "short" && e.duration_minutes > 20) return false;
        if (
          durFilter === "medium" &&
          (e.duration_minutes <= 20 || e.duration_minutes > 50)
        )
          return false;
        if (durFilter === "long" && e.duration_minutes <= 50) return false;
        if (!e.title.toLowerCase().includes(search.toLowerCase())) return false;
        return true;
      }),
    [exams, effectiveClassIds, classFilter, topicFilter, diffFilter, durFilter, search],
  );

  const shown = filtered.slice(0, page * PAGE_SIZE);

  if (!exams) return <SkeletonGrid />;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center gap-3">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="🔍 Tìm đề…"
          className="min-w-48 flex-1 rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-white placeholder:text-slate-500 focus:border-[#3B82F6] focus:outline-none"
        />
        {(isAdmin || !session) && classes.length > 0 && (
          <select
            value={classFilter}
            onChange={(e) => setClassFilter(Number(e.target.value))}
            className={selectCls}
          >
            <option value={0}>Tất cả lớp</option>
            {classes.map((c) => (
              <option key={c.id} value={c.id}>
                Lớp {c.name}
              </option>
            ))}
          </select>
        )}
        {topics.length > 0 && (
          <select
            value={topicFilter}
            onChange={(e) => setTopicFilter(e.target.value)}
            className={selectCls}
          >
            <option value="">Mọi chủ đề</option>
            {topics.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        )}
        <select
          value={diffFilter}
          onChange={(e) => setDiffFilter(e.target.value as Difficulty | "all")}
          className={selectCls}
        >
          <option value="all">Mọi độ khó</option>
          <option value="de">Dễ</option>
          <option value="trung-binh">Trung bình</option>
          <option value="kho">Khó</option>
        </select>
        <select
          value={durFilter}
          onChange={(e) =>
            setDurFilter(e.target.value as typeof durFilter)
          }
          className={selectCls}
        >
          <option value="all">Mọi thời lượng</option>
          <option value="short">≤ 20 phút</option>
          <option value="medium">20–50 phút</option>
          <option value="long">&gt; 50 phút</option>
        </select>
      </div>

      {filtered.length === 0 ? (
        <p className="text-slate-400">Không có đề nào phù hợp bộ lọc.</p>
      ) : (
        <>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {shown.map((exam) => (
              <Link
                key={exam.id}
                href={`/kiem-tra/lam?id=${exam.id}`}
                className="group rounded-2xl border border-white/10 bg-[#0B1020] p-6 transition-all hover:-translate-y-1 hover:border-[#3B82F6]/50"
              >
                <h2 className="font-display text-lg font-semibold text-white group-hover:text-[#3B82F6]">
                  {exam.title}
                </h2>
                <p className="mt-3 text-sm text-slate-400">
                  {exam.question_count} câu · {exam.duration_minutes} phút
                  {exam.difficulty &&
                    ` · ${DIFFICULTY_LABELS[exam.difficulty]}`}
                </p>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {exam.topic && (
                    <span className="rounded-full bg-white/5 px-2.5 py-0.5 text-xs text-slate-400">
                      {exam.topic}
                    </span>
                  )}
                  {exam.classIds.map((id) => {
                    const c = classes.find((x) => x.id === id);
                    return c ? (
                      <span
                        key={id}
                        style={{ color: c.color }}
                        className="rounded-full bg-white/5 px-2.5 py-0.5 text-xs"
                      >
                        {c.name}
                      </span>
                    ) : null;
                  })}
                  {exam.classIds.length === 0 && (
                    <span className="rounded-full bg-white/5 px-2.5 py-0.5 text-xs text-slate-500">
                      Toàn trường
                    </span>
                  )}
                </div>
                <span className="mt-4 inline-block rounded-full bg-[#2563EB]/15 px-4 py-1.5 text-sm font-semibold text-[#3B82F6]">
                  Vào làm bài →
                </span>
              </Link>
            ))}
          </div>
          {shown.length < filtered.length && (
            <button
              onClick={() => setPage((p) => p + 1)}
              className="mx-auto block rounded-full border border-white/15 px-6 py-2.5 text-sm font-medium text-slate-200 hover:border-white/30"
            >
              Xem thêm ({filtered.length - shown.length} đề)
            </button>
          )}
        </>
      )}
    </div>
  );
}

export default function ExamListPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          Đề <span className="text-gradient">thi</span>
        </h1>
        <p className="mt-3 mb-10 max-w-2xl text-slate-400">
          Làm bài trắc nghiệm ngay trên web — nộp bài là có điểm liền, kèm lời
          giải chi tiết từng câu.
        </p>
        <RequireAuth>
          <ExamList />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
