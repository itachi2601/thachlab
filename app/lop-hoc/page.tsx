"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { SkeletonGrid } from "@/components/ui/Skeleton";
import type { SchoolClass } from "@/features/exams/types";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import type { Chapter, Lesson } from "@/features/lessons/types";
import {
  classGrade,
  displayClassesByGrade,
  expandClassIdsByGrade,
  fetchClasses,
} from "@/services/classes";
import { fetchChapters, fetchLessons } from "@/services/lessons";
import {
  fetchPublishedExams,
  fetchPublishedPosts,
  visibleTo,
  type ExamMeta,
  type PostMeta,
} from "@/services/content";
import { useAuth } from "@/components/auth/AuthProvider";
import { supabaseConfigured } from "@/services/supabase";

const GRADE_IMAGES: Record<string, string> = {
  "9": "/images/learning-path/khtn-9.jpg",
  "10": "/images/learning-path/vat-ly-10.jpg",
  "11": "/images/learning-path/vat-ly-11.jpg",
  "12": "/images/learning-path/vat-ly-12.jpg",
};
const GRADE_LABELS: Record<string, string> = { "9": "KHTN 9" };
const GRADE_ORDER = ["9", "10", "11", "12"];
const KHTN9_SUBJECTS = [
  { label: "Vật lý", icon: "⚡" },
  { label: "Hóa học", icon: "🧪" },
  { label: "Sinh học", icon: "🧬" },
];
const CLASS_TABS = [
  { id: "secondary", label: "Lý thuyết" },
  { id: "university", label: "Thực hành" },
] as const;
const UNIVERSITY_CLASSES = [
  {
    title: "Vật lý đại cương",
    icon: "⚙️",
    description: "Nền tảng cơ học, nhiệt, điện từ và các mô hình vật lý ứng dụng.",
    href: "",
  },
  {
    title: "Gia công CNC",
    icon: "🛠️",
    description: "Quy trình, thông số cắt, lập trình và vận hành gia công CNC.",
    href: "/lop-hoc/cnc",
  },
  {
    title: "Tiện – Phay truyền thống",
    icon: "🔧",
    description: "Điểm danh, chọn máy và theo dõi 5S khi thực hành tại Xưởng C1.1.",
    href: "/lop-hoc/tien-phay",
  },
  {
    title: "Công nghệ chế tạo máy",
    icon: "🏭",
    description: "Kiến thức về phôi, dụng cụ, nguyên công và tổ chức sản xuất cơ khí.",
    href: "",
  },
  {
    title: "Anh văn chuyên ngành cơ khí",
    icon: "📘",
    description: "Từ vựng, đọc hiểu tài liệu kỹ thuật và giao tiếp trong ngành cơ khí.",
    href: "",
  },
];

export default function ClassHubPage() {
  const { session } = useAuth();
  const [classes, setClasses] = useState<SchoolClass[] | null>(null);
  const [activeId, setActiveId] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<(typeof CLASS_TABS)[number]["id"]>(
    "secondary",
  );
  const [activeKhtn9Subject, setActiveKhtn9Subject] = useState("Vật lý");
  const [requestedChapterId, setRequestedChapterId] = useState<number | null>(null);
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<Lesson[] | null>(null);
  const [exams, setExams] = useState<ExamMeta[] | null>(null);
  const [posts, setPosts] = useState<PostMeta[] | null>(null);

  useEffect(() => {
    const requestedTab = new URLSearchParams(window.location.search).get("tab");
    if (requestedTab === "cttc") setActiveTab("university");
    const chapterParam = Number(new URLSearchParams(window.location.search).get("chapter"));
    if (chapterParam > 0) setRequestedChapterId(chapterParam);

    if (!supabaseConfigured) return;
    fetchClasses().then((cs) => {
      setClasses(cs);
      if (cs.length > 0) setActiveId((prev) => prev ?? cs[0].id);
    });
    fetchChapters().then(setChapters);
    fetchLessons().then(setLessons);
    fetchPublishedPosts().then(setPosts);
  }, []);

  // đề thi yêu cầu đăng nhập (RLS) — chỉ tải khi có session
  useEffect(() => {
    if (!supabaseConfigured || !session) return;
    fetchPublishedExams().then(setExams);
  }, [session]);

  const active = classes?.find((c) => c.id === activeId);
  const activeDisplayName =
    active && classGrade(active.name) === "9"
      ? `KHTN 9 - ${activeKhtn9Subject}`
      : active?.name;
  const displayClasses = classes ? displayClassesByGrade(classes) : [];
  const visibleClassIds =
    classes && activeId !== null ? expandClassIdsByGrade([activeId], classes) : null;
  const classChapters = (chapters ?? []).filter((ch) =>
    visibleTo(ch.classIds, visibleClassIds),
  );
  const classPosts = (posts ?? []).filter((p) =>
    visibleTo(p.classIds, visibleClassIds),
  );
  const classExams = (exams ?? []).filter((e) =>
    visibleTo(e.classIds, visibleClassIds),
  );

  useEffect(() => {
    if (!requestedChapterId || !classes || !chapters) return;
    const requestedChapter = chapters.find((chapter) => chapter.id === requestedChapterId);
    const targetClassId = requestedChapter?.classIds[0];
    if (targetClassId) {
      const targetClass = classes.find((item) => item.id === targetClassId);
      const representative = targetClass
        ? displayClassesByGrade(classes).find(
            (item) => classGrade(item.name) === classGrade(targetClass.name),
          )
        : undefined;
      setActiveId(representative?.id ?? targetClassId);
    }
  }, [chapters, classes, requestedChapterId]);

  useEffect(() => {
    if (!requestedChapterId || !lessons) return;
    const timer = window.setTimeout(() => {
      document
        .getElementById(`chapter-${requestedChapterId}`)
        ?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 80);
    return () => window.clearTimeout(timer);
  }, [activeId, lessons, requestedChapterId]);
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          Lớp <span className="text-gradient">học</span>
        </h1>
        <p className="mt-3 mb-8 text-slate-400">
          Chọn lớp để xem chương trình học, đề thi và tài liệu dành riêng cho
          lớp đó.
        </p>

        <div className="mb-6 inline-flex rounded-full border border-white/10 bg-white/5 p-1">
          {CLASS_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => {
                setActiveTab(tab.id);
                const url = tab.id === "university" ? "/lop-hoc?tab=cttc" : "/lop-hoc";
                window.history.replaceState(null, "", url);
              }}
              aria-pressed={activeTab === tab.id}
              className={`rounded-full px-5 py-2 text-sm font-semibold transition-colors ${
                activeTab === tab.id
                  ? "bg-primary text-white"
                  : "text-slate-300 hover:bg-white/10 hover:text-white"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {activeTab === "university" && (
          <section aria-labelledby="cttc-course-heading">
            <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
              <div>
                <h2 id="cttc-course-heading" className="font-display text-xl font-semibold text-white">
                  Chương trình thực hành (CTTC)
                </h2>
                <p className="mt-1 text-sm text-slate-400">
                  Chọn môn học để mở không gian học tập và theo dõi tiến độ.
                </p>
              </div>
              <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1.5 text-xs font-semibold text-emerald-300">
                {UNIVERSITY_CLASSES.filter((item) => item.href).length} môn đang hoạt động
              </span>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {UNIVERSITY_CLASSES.filter((universityClass) => universityClass.href).map((universityClass) => (
                <Link
                  key={universityClass.title}
                  href={universityClass.href}
                  className="group rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-left transition-all hover:-translate-y-1 hover:border-primary/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                >
                  <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/5 text-2xl">
                    {universityClass.icon}
                  </span>
                  <h3 className="mt-5 font-display text-lg font-bold text-white">
                    {universityClass.title}
                  </h3>
                  <p className="mt-3 min-h-18 text-sm leading-6 text-slate-400">
                    {universityClass.description}
                  </p>
                  <span className="mt-5 flex items-center justify-between border-t border-white/10 pt-4 text-sm font-semibold text-[#60A5FA]">
                    Mở môn học
                    <span aria-hidden="true">→</span>
                  </span>
                </Link>
              ))}
            </div>
          </section>
        )}

        {activeTab === "secondary" && (!supabaseConfigured ? (
          <p className="text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : !classes ? (
          <SkeletonGrid count={3} />
        ) : classes.length === 0 ? (
          <p className="text-slate-400">Chưa có lớp nào.</p>
        ) : (
          <>
              <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
                <div>
                  <h2 className="font-display text-xl font-semibold text-white">
                    Chương trình lý thuyết (THPT)
                  </h2>
                  <p className="mt-1 text-sm text-slate-400">
                    Chọn lớp hoặc môn học để xem chương trình và mở từng bài học.
                  </p>
                </div>
                {activeDisplayName && (
                  <span className="rounded-full border border-blue-400/20 bg-blue-400/10 px-3 py-1.5 text-xs font-semibold text-blue-300">
                    Đang chọn: {activeDisplayName}
                  </span>
                )}
              </div>

              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {GRADE_ORDER.map((grade) => {
                  const gradeClasses = displayClasses.filter(
                    (c) => classGrade(c.name) === grade,
                  );
                  if (gradeClasses.length === 0) return null;
                  return (
                    <div
                      key={grade}
                      className="overflow-hidden rounded-2xl border border-white/10 bg-[#0B1020]"
                    >
                      <img
                        src={GRADE_IMAGES[grade]}
                        alt={GRADE_LABELS[grade] ?? `Vật lý lớp ${grade}`}
                        className="aspect-[2/3] w-full object-cover"
                        loading="lazy"
                      />
                      <div className="flex flex-wrap gap-2 p-3">
                        {grade === "9"
                          ? KHTN9_SUBJECTS.map((subject) => {
                              const khtnClass = gradeClasses[0];
                              const selected =
                                activeId === khtnClass.id &&
                                activeKhtn9Subject === subject.label;
                              return (
                                <button
                                  key={subject.label}
                                  onClick={() => {
                                    setActiveId(khtnClass.id);
                                    setActiveKhtn9Subject(subject.label);
                                  }}
                                  style={
                                    selected
                                      ? { backgroundColor: khtnClass.color, color: "#fff" }
                                      : undefined
                                  }
                                  className={`rounded-full px-4 py-2 text-sm font-semibold transition-colors ${
                                    selected
                                      ? ""
                                      : "bg-white/5 text-slate-300 hover:bg-white/10"
                                  }`}
                                >
                                  {subject.icon} {subject.label}
                                </button>
                              );
                            })
                          : gradeClasses.map((c) => (
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
                    </div>
                  );
                })}
              </div>

            {active && (
              <div className="mt-10 space-y-12">
                <section>
                  <h2 className="mb-4 font-display text-xl font-semibold text-white">
                    Chương trình lớp {activeDisplayName}
                  </h2>
                  {!chapters || !lessons ? (
                    <SkeletonGrid count={2} />
                  ) : classChapters.length === 0 ? (
                    <p className="text-sm text-slate-400">
                      Chưa có chương trình học cho lớp này.
                    </p>
                  ) : (
                    <div className="space-y-6">
                      {classChapters.map((ch) => {
                        const chapterLessons = lessons.filter(
                          (l) => l.chapter_id === ch.id,
                        );
                        return (
                          <div
                            key={ch.id}
                            id={`chapter-${ch.id}`}
                            className="rounded-2xl border border-white/10 bg-[#080D1A] p-2"
                            style={{ scrollMarginTop: "104px" }}
                          >
                            <p className="px-4 pt-3 pb-2 text-sm font-bold tracking-wide text-slate-200 uppercase">
                              {ch.title}
                            </p>
                            <div className="space-y-1">
                              {chapterLessons.length === 0 && (
                                <p className="px-4 pb-3 text-sm text-slate-500">
                                  Chưa có bài học trong chương này.
                                </p>
                              )}
                              {chapterLessons.map((l) => (
                                <Link
                                  key={l.id}
                                  href={`/lop-hoc/bai?id=${l.id}`}
                                  className="group flex items-center gap-4 rounded-xl px-4 py-4 transition-colors hover:bg-white/5"
                                >
                                  <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#1D3461] text-lg">
                                    📖
                                  </span>
                                  <span className="min-w-0 flex-1">
                                    <span className="block truncate font-display text-sm font-bold tracking-wide text-white uppercase group-hover:text-primary">
                                      {l.title}
                                    </span>
                                    <span className="mt-0.5 block text-xs font-semibold tracking-wide text-[#60A5FA] uppercase">
                                      {l.itemCount} mục
                                    </span>
                                  </span>
                                  <span className="text-slate-500 transition-transform group-hover:translate-x-1 group-hover:text-primary">
                                    →
                                  </span>
                                </Link>
                              ))}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </section>

                {classExams.length > 0 && (
                  <section>
                    <h2 className="mb-4 font-display text-xl font-semibold text-white">
                      Đề thi lớp {activeDisplayName}
                    </h2>
                    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                      {classExams.map((exam) => (
                        <Link
                          key={exam.id}
                          href={`/kiem-tra/lam?id=${exam.id}`}
                          className="group rounded-2xl border border-white/10 bg-[#0B1020] p-6 transition-all hover:-translate-y-1 hover:border-primary/50"
                        >
                          <h3 className="font-display font-semibold text-white group-hover:text-primary">
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
                  </section>
                )}

                {!session && (
                  <p className="text-sm text-slate-400">
                    <Link
                      href="/dang-nhap"
                      className="text-primary hover:underline"
                    >
                      Đăng nhập
                    </Link>{" "}
                    để xem đề thi và lưu tiến độ học của em.
                  </p>
                )}

                {classPosts.length > 0 && (
                  <section>
                    <h2 className="mb-4 font-display text-xl font-semibold text-white">
                      Bài viết lớp {activeDisplayName}
                    </h2>
                    <div className="grid gap-5 sm:grid-cols-2">
                      {classPosts.map((p) => (
                        <Link
                          key={p.id}
                          href={`/tin-tuc#post-${p.id}`}
                          className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 transition-all hover:-translate-y-1 hover:border-primary/50"
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
                  </section>
                )}
              </div>
            )}
          </>
        ))}
      </main>
      <Footer />
    </>
  );
}
