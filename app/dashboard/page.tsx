"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { SkeletonGrid } from "@/components/ui/Skeleton";
import { useAuth } from "@/components/auth/AuthProvider";
import { getSupabase } from "@/services/supabase";
import { fetchMyClassIds } from "@/services/classes";
import {
  fetchPublishedExams,
  fetchPublishedPosts,
  visibleTo,
  type ExamMeta,
  type PostMeta,
} from "@/services/content";
import {
  fetchChapters,
  fetchLessons,
  fetchItemIdsByLessons,
  fetchMyProgress,
  fetchMyExamScores,
} from "@/services/lessons";
import type { Chapter, Lesson } from "@/features/lessons/types";
import { DIFFICULTY_LABELS } from "@/features/exams/types";

interface ResultRow {
  id: number;
  created_at: string;
  score: number;
  exams: { title: string } | null;
}

interface ChapterProgress {
  chapter: Chapter;
  done: number;
  total: number;
}

function Dashboard() {
  const { session, profile } = useAuth();
  const userId = session?.user.id;

  const [myClassIds, setMyClassIds] = useState<number[] | null>(null);
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<Lesson[] | null>(null);
  const [doneItemIds, setDoneItemIds] = useState<Set<number> | null>(null);
  const [itemsByLesson, setItemsByLesson] = useState<Map<number, number[]> | null>(null);
  const [scores, setScores] = useState<Map<number, number> | null>(null);
  const [exams, setExams] = useState<ExamMeta[] | null>(null);
  const [posts, setPosts] = useState<PostMeta[] | null>(null);
  const [recentResults, setRecentResults] = useState<ResultRow[] | null>(null);

  useEffect(() => {
    if (!userId) return;
    fetchMyClassIds(userId).then(setMyClassIds);
    fetchChapters().then(setChapters);
    fetchLessons().then(setLessons);
    fetchMyProgress(userId).then(setDoneItemIds);
    fetchMyExamScores(userId).then(setScores);
    fetchPublishedExams().then(setExams);
    fetchPublishedPosts().then(setPosts);
    getSupabase()
      .from("exam_results")
      .select("id, created_at, score, exams(title)")
      .eq("student_id", userId)
      .order("created_at", { ascending: false })
      .limit(5)
      .then(({ data }) => setRecentResults((data as unknown as ResultRow[]) ?? []));
  }, [userId]);

  useEffect(() => {
    if (!lessons) return;
    fetchItemIdsByLessons(lessons.map((l) => l.id)).then(setItemsByLesson);
  }, [lessons]);

  const visibleChapters = useMemo(
    () => (chapters ?? []).filter((c) => visibleTo(c.classIds, myClassIds)),
    [chapters, myClassIds],
  );

  const chapterProgress: ChapterProgress[] = useMemo(() => {
    if (!lessons || !itemsByLesson || !doneItemIds) return [];
    return visibleChapters.map((chapter) => {
      const chapterLessons = lessons.filter((l) => l.chapter_id === chapter.id);
      let done = 0;
      let total = 0;
      for (const l of chapterLessons) {
        const itemIds = itemsByLesson.get(l.id) ?? [];
        total += itemIds.length;
        done += itemIds.filter((id) => doneItemIds.has(id)).length;
      }
      return { chapter, done, total };
    });
  }, [visibleChapters, lessons, itemsByLesson, doneItemIds]);

  const overallDone = chapterProgress.reduce((s, c) => s + c.done, 0);
  const overallTotal = chapterProgress.reduce((s, c) => s + c.total, 0);
  const overallPct = overallTotal > 0 ? Math.round((overallDone / overallTotal) * 100) : 0;

  const avgScore = useMemo(() => {
    if (!scores || scores.size === 0) return null;
    const vals = [...scores.values()];
    return Math.round((vals.reduce((s, v) => s + v, 0) / vals.length) * 100) / 100;
  }, [scores]);

  const suggestedExams = useMemo(() => {
    if (!exams || !scores) return [];
    return exams
      .filter((e) => visibleTo(e.classIds, myClassIds))
      .filter((e) => !scores.has(e.id))
      .slice(0, 4);
  }, [exams, scores, myClassIds]);

  const suggestedPosts = useMemo(() => {
    if (!posts) return [];
    return posts.filter((p) => visibleTo(p.classIds, myClassIds)).slice(0, 3);
  }, [posts, myClassIds]);

  const loading = !chapters || !lessons || !itemsByLesson || !doneItemIds || !scores;

  if (loading) return <SkeletonGrid count={3} />;

  return (
    <div className="space-y-12">
      {/* ---- Lời chào ---- */}
      <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6">
        <p className="font-display text-xl font-semibold text-white">
          Chào {profile?.full_name || "em"} 👋
        </p>
        <p className="mt-1 text-sm text-slate-400">
          {profile?.class_name && `Lớp ${profile.class_name} · `}
          Đây là tổng quan tiến độ học tập của em.
        </p>
      </div>

      {/* ---- Thống kê nhanh ---- */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="glass rounded-2xl p-5">
          <p className="text-3xl font-bold text-white">{overallPct}%</p>
          <p className="mt-1 text-sm text-slate-400">Tiến độ học liệu</p>
        </div>
        <div className="glass rounded-2xl p-5">
          <p className="text-3xl font-bold text-white">
            {avgScore !== null ? avgScore.toLocaleString("vi-VN") : "—"}
          </p>
          <p className="mt-1 text-sm text-slate-400">Điểm trung bình</p>
        </div>
        <div className="glass rounded-2xl p-5">
          <p className="text-3xl font-bold text-white">{scores?.size ?? 0}</p>
          <p className="mt-1 text-sm text-slate-400">Đề đã làm</p>
        </div>
      </div>

      {/* ---- Tiến độ theo chương ---- */}
      <div>
        <h2 className="mb-4 font-display text-xl font-semibold text-white">
          Tiến độ theo chương
        </h2>
        {chapterProgress.length === 0 ? (
          <p className="text-sm text-slate-400">Chưa có chương trình học nào.</p>
        ) : (
          <div className="space-y-3">
            {chapterProgress.map(({ chapter, done, total }) => {
              const pct = total > 0 ? Math.round((done / total) * 100) : 0;
              return (
                <div
                  key={chapter.id}
                  className="rounded-2xl border border-white/10 bg-[#0B1020] p-4"
                >
                  <div className="flex items-center justify-between gap-4">
                    <p className="text-sm font-semibold text-white">{chapter.title}</p>
                    <span className="shrink-0 font-mono text-xs text-slate-400">
                      {done}/{total} mục
                    </span>
                  </div>
                  <div className="mt-2 h-2 overflow-hidden rounded-full bg-white/5">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-blue-500 to-cyan-400"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* ---- Đề gợi ý + Điểm gần đây ---- */}
      <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
        <div>
          <h2 className="mb-4 font-display text-xl font-semibold text-white">
            Đề gợi ý cho em
          </h2>
          {suggestedExams.length === 0 ? (
            <p className="text-sm text-slate-400">
              Em đã làm hết đề hiện có, tuyệt vời! 🎉
            </p>
          ) : (
            <div className="space-y-3">
              {suggestedExams.map((exam) => (
                <Link
                  key={exam.id}
                  href={`/kiem-tra/lam?id=${exam.id}`}
                  className="group flex items-center justify-between rounded-2xl border border-white/10 bg-[#0B1020] p-4 transition-colors hover:border-[#3B82F6]/50"
                >
                  <div>
                    <p className="text-sm font-semibold text-white group-hover:text-[#3B82F6]">
                      {exam.title}
                    </p>
                    <p className="mt-1 text-xs text-slate-400">
                      {exam.question_count} câu · {exam.duration_minutes} phút
                      {exam.difficulty && ` · ${DIFFICULTY_LABELS[exam.difficulty]}`}
                    </p>
                  </div>
                  <span className="text-slate-500 transition-transform group-hover:translate-x-1 group-hover:text-[#3B82F6]">
                    →
                  </span>
                </Link>
              ))}
            </div>
          )}
        </div>

        <div>
          <h2 className="mb-4 font-display text-xl font-semibold text-white">
            Điểm gần đây
          </h2>
          {!recentResults ? (
            <p className="text-sm text-slate-400">Đang tải…</p>
          ) : recentResults.length === 0 ? (
            <p className="text-sm text-slate-400">Em chưa làm bài kiểm tra nào.</p>
          ) : (
            <div className="overflow-hidden rounded-2xl border border-white/10">
              <table className="w-full text-left text-sm">
                <tbody className="divide-y divide-white/5 text-slate-300">
                  {recentResults.map((row) => (
                    <tr key={row.id}>
                      <td className="px-4 py-3">{row.exams?.title ?? "(Đề đã xóa)"}</td>
                      <td className="px-4 py-3 text-right font-mono font-semibold text-white">
                        {Number(row.score).toLocaleString("vi-VN")}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <Link
                href="/tai-khoan"
                className="block bg-white/5 px-4 py-2.5 text-center text-xs font-medium text-[#3B82F6] hover:bg-white/10"
              >
                Xem toàn bộ lịch sử →
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* ---- Bài viết liên quan ---- */}
      {suggestedPosts.length > 0 && (
        <div>
          <h2 className="mb-4 font-display text-xl font-semibold text-white">
            Bài viết dành cho em
          </h2>
          <div className="grid gap-5 sm:grid-cols-3">
            {suggestedPosts.map((p) => (
              <Link
                key={p.id}
                href={`/tin-tuc#post-${p.id}`}
                className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 transition-all hover:-translate-y-1 hover:border-[#3B82F6]/50"
              >
                <h3 className="font-display text-sm font-semibold text-white">{p.title}</h3>
                <p className="mt-2 line-clamp-2 text-xs text-slate-400">
                  {p.body || (p.video_url && "🎬 Video bài giảng")}
                </p>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function DashboardPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="mb-10 font-display text-3xl font-bold text-white sm:text-4xl">
          Dash<span className="text-gradient">board</span>
        </h1>
        <RequireAuth>
          <Dashboard />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
