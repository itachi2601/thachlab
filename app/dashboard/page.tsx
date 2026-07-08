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
      <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-[#1a2a4a] via-[#0B1020] to-[#0B1020] p-8">
        <div aria-hidden className="absolute right-0 top-0 -translate-y-1/2 translate-x-1/2 h-[400px] w-[400px] rounded-full bg-blue-500/10 blur-3xl" />
        <div className="relative">
          <p className="font-display text-3xl font-bold text-white">
            Chào {profile?.full_name || "em"} 👋
          </p>
          <p className="mt-2 text-base text-slate-300">
            {profile?.class_name && `🎓 Lớp ${profile.class_name}`}
          </p>
          <p className="mt-3 text-sm text-slate-400">
            Tiến độ học tập hôm nay • Cố lên!
          </p>
        </div>
      </div>

      {/* ---- Thống kê nhanh ---- */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-blue-500/20 to-blue-600/5 p-6 transition-all hover:-translate-y-1 hover:border-blue-400/50">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-400/0 to-blue-600/0 group-hover:from-blue-400/10 group-hover:to-blue-600/10 transition-all" />
          <div className="relative">
            <p className="text-4xl font-bold text-white">{overallPct}%</p>
            <p className="mt-2 text-sm text-blue-200">📚 Tiến độ học liệu</p>
          </div>
        </div>
        <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-purple-500/20 to-purple-600/5 p-6 transition-all hover:-translate-y-1 hover:border-purple-400/50">
          <div className="absolute inset-0 bg-gradient-to-br from-purple-400/0 to-purple-600/0 group-hover:from-purple-400/10 group-hover:to-purple-600/10 transition-all" />
          <div className="relative">
            <p className="text-4xl font-bold text-white">
              {avgScore !== null ? avgScore.toLocaleString("vi-VN") : "—"}
            </p>
            <p className="mt-2 text-sm text-purple-200">⭐ Điểm trung bình</p>
          </div>
        </div>
        <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-emerald-500/20 to-emerald-600/5 p-6 transition-all hover:-translate-y-1 hover:border-emerald-400/50">
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-400/0 to-emerald-600/0 group-hover:from-emerald-400/10 group-hover:to-emerald-600/10 transition-all" />
          <div className="relative">
            <p className="text-4xl font-bold text-white">{scores?.size ?? 0}</p>
            <p className="mt-2 text-sm text-emerald-200">✅ Đề đã làm</p>
          </div>
        </div>
      </div>

      {/* ---- Tiến độ theo chương ---- */}
      <div>
        <div className="mb-6 flex items-center gap-3">
          <h2 className="font-display text-2xl font-semibold text-white">
            📖 Lộ trình học
          </h2>
          {overallTotal > 0 && (
            <span className="inline-block rounded-full bg-blue-500/20 px-3 py-1 text-xs font-semibold text-blue-200">
              {overallDone}/{overallTotal} mục
            </span>
          )}
        </div>
        {chapterProgress.length === 0 ? (
          <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-center">
            <p className="text-sm text-slate-400">Chưa có chương trình học nào cho lớp em.</p>
            <p className="mt-2 text-xs text-slate-500">Hãy chọn lớp trong menu Lớp học nhé!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {chapterProgress.map(({ chapter, done, total }) => {
              const pct = total > 0 ? Math.round((done / total) * 100) : 0;
              const isComplete = pct === 100;
              return (
                <div
                  key={chapter.id}
                  className={`group rounded-2xl border transition-all ${
                    isComplete
                      ? "border-emerald-500/30 bg-emerald-500/5"
                      : "border-white/10 bg-[#0B1020] hover:border-blue-400/30"
                  } p-4`}
                >
                  <div className="flex items-center justify-between gap-4">
                    <p className="text-sm font-semibold text-white">{chapter.title}</p>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className={`font-mono text-xs ${isComplete ? "text-emerald-300" : "text-slate-400"}`}>
                        {done}/{total}
                      </span>
                      {isComplete && <span className="text-lg">🎉</span>}
                    </div>
                  </div>
                  <div className="mt-3 h-2.5 overflow-hidden rounded-full bg-white/5">
                    <div
                      className={`h-full rounded-full transition-all ${
                        isComplete
                          ? "bg-gradient-to-r from-emerald-500 to-teal-400"
                          : "bg-gradient-to-r from-blue-500 to-cyan-400"
                      }`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                  {pct > 0 && pct < 100 && (
                    <p className="mt-2 text-xs text-slate-500">
                      {pct}% xong • {total - done} mục còn lại
                    </p>
                  )}
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
            📝 Đề gợi ý cho em
          </h2>
          {suggestedExams.length === 0 ? (
            <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/5 p-6 text-center">
              <p className="text-lg font-semibold text-emerald-300">
                Em đã làm hết đề hiện có! 🎉
              </p>
              <p className="mt-2 text-sm text-slate-400">
                Rất tuyệt vời! Hãy tiếp tục học thêm kiến thức nhé.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {suggestedExams.map((exam) => (
                <Link
                  key={exam.id}
                  href={`/kiem-tra/lam?id=${exam.id}`}
                  className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-r from-[#0B1020] to-[#1a1f3a] p-4 transition-all hover:-translate-y-1 hover:border-amber-400/50"
                >
                  <div className="relative flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <p className="text-sm font-bold text-white group-hover:text-amber-300">
                        {exam.title}
                      </p>
                      <p className="mt-1.5 text-xs text-slate-400">
                        ⏱️ {exam.duration_minutes} phút · 📋 {exam.question_count} câu
                        {exam.difficulty && ` · 💪 ${DIFFICULTY_LABELS[exam.difficulty]}`}
                      </p>
                    </div>
                    <span className="mt-1 shrink-0 text-xl transition-transform group-hover:translate-x-1">
                      👉
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>

        <div>
          <h2 className="mb-4 font-display text-xl font-semibold text-white">
            ⚡ Điểm gần đây
          </h2>
          {!recentResults ? (
            <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-center">
              <p className="text-sm text-slate-400">Đang tải…</p>
            </div>
          ) : recentResults.length === 0 ? (
            <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-center">
              <p className="text-sm text-slate-400">Em chưa làm bài kiểm tra nào.</p>
              <p className="mt-2 text-xs text-slate-500">Hãy chọn một đề trong mục gợi ý để bắt đầu!</p>
            </div>
          ) : (
            <div className="overflow-hidden rounded-2xl border border-white/10">
              <div className="divide-y divide-white/5 bg-[#0B1020]">
                {recentResults.map((row) => {
                  const score = Number(row.score);
                  const isGood = score >= 7;
                  return (
                    <div
                      key={row.id}
                      className={`flex items-center justify-between px-5 py-4 transition-colors ${
                        isGood ? "hover:bg-emerald-500/5" : "hover:bg-blue-500/5"
                      }`}
                    >
                      <p className="text-sm font-medium text-white">
                        {row.exams?.title ?? "(Đề đã xóa)"}
                      </p>
                      <div className="flex items-center gap-2">
                        <span
                          className={`font-mono text-lg font-bold ${
                            isGood ? "text-emerald-400" : "text-blue-400"
                          }`}
                        >
                          {score.toLocaleString("vi-VN")}
                        </span>
                        <span className="text-base">{isGood ? "🌟" : "💪"}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
              <Link
                href="/tai-khoan"
                className="block bg-gradient-to-r from-blue-500/10 to-cyan-500/10 px-5 py-3 text-center text-xs font-semibold text-blue-300 hover:from-blue-500/20 hover:to-cyan-500/20 transition-colors"
              >
                Xem lịch sử đầy đủ →
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* ---- Bài viết liên quan ---- */}
      {suggestedPosts.length > 0 && (
        <div>
          <h2 className="mb-4 font-display text-xl font-semibold text-white">
            ✨ Bài viết dành cho em
          </h2>
          <div className="grid gap-4 sm:grid-cols-3">
            {suggestedPosts.map((p) => (
              <Link
                key={p.id}
                href={`/tin-tuc#post-${p.id}`}
                className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-[#1a1f3a] to-[#0B1020] p-5 transition-all hover:-translate-y-1 hover:border-pink-400/50"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-pink-500/0 to-purple-500/0 group-hover:from-pink-500/10 group-hover:to-purple-500/10 transition-all" />
                <div className="relative">
                  <h3 className="font-display text-sm font-bold text-white group-hover:text-pink-300 line-clamp-2">
                    {p.title}
                  </h3>
                  <p className="mt-2 line-clamp-2 text-xs text-slate-400">
                    {p.body || (p.video_url && "🎬 Video bài giảng")}
                  </p>
                  <div className="mt-3 flex items-center gap-1 text-xs text-pink-300 opacity-0 transition-opacity group-hover:opacity-100">
                    Đọc thêm →
                  </div>
                </div>
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
