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
import {
  CNC_COURSE_ITEMS,
  CNC_GATE_QUIZ,
  CNC_PROGRESS,
  CNC_SETUP_CHECKLIST,
} from "@/services/cnc-lms";
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
  { id: "secondary", label: "Trung học" },
  { id: "university", label: "Đại học" },
] as const;
const UNIVERSITY_CLASSES = [
  {
    title: "Vật lý đại cương",
    icon: "⚙️",
    description: "Nền tảng cơ học, nhiệt, điện từ và các mô hình vật lý ứng dụng.",
  },
  {
    title: "Gia công CNC",
    icon: "🛠️",
    description: "Quy trình, thông số cắt, lập trình và vận hành gia công CNC.",
  },
  {
    title: "Công nghệ chế tạo máy",
    icon: "🏭",
    description: "Kiến thức về phôi, dụng cụ, nguyên công và tổ chức sản xuất cơ khí.",
  },
  {
    title: "Anh văn chuyên ngành cơ khí",
    icon: "📘",
    description: "Từ vựng, đọc hiểu tài liệu kỹ thuật và giao tiếp trong ngành cơ khí.",
  },
];

export default function ClassHubPage() {
  const { session } = useAuth();
  const [classes, setClasses] = useState<SchoolClass[] | null>(null);
  const [activeId, setActiveId] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<(typeof CLASS_TABS)[number]["id"]>(
    "secondary",
  );
  const [activeUniversityClass, setActiveUniversityClass] = useState("Gia công CNC");
  const [activeCncItemId, setActiveCncItemId] = useState("intro");
  const [cncChecklist, setCncChecklist] = useState<Record<string, boolean>>({});
  const [cncGateAnswers, setCncGateAnswers] = useState<Record<string, number>>({});
  const [cncGateSubmitted, setCncGateSubmitted] = useState(false);
  const [activeKhtn9Subject, setActiveKhtn9Subject] = useState("Vật lý");
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<Lesson[] | null>(null);
  const [exams, setExams] = useState<ExamMeta[] | null>(null);
  const [posts, setPosts] = useState<PostMeta[] | null>(null);

  useEffect(() => {
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
  const cncProgrammingUnlocked =
    CNC_PROGRESS.turningQuizScore >= 80 && CNC_PROGRESS.millingQuizScore >= 80;
  const cncProductionUnlocked = CNC_PROGRESS.operationPassedByInstructor;
  const activeCncItem =
    CNC_COURSE_ITEMS.find((item) => item.id === activeCncItemId) ??
    CNC_COURSE_ITEMS[0];
  const checkedSetupSteps = CNC_SETUP_CHECKLIST.filter(
    (step) => cncChecklist[step],
  ).length;
  const cncGateScore = CNC_GATE_QUIZ.filter(
    (question) => cncGateAnswers[question.id] === question.correctIndex,
  ).length;
  const cncGatePassed = cncGateSubmitted && cncGateScore === CNC_GATE_QUIZ.length;
  const isCncItemLocked = (itemId: string) => {
    if (itemId === "lesson-4") return !cncProgrammingUnlocked;
    if (itemId === "lesson-5" || itemId === "lesson-6") return !cncProductionUnlocked;
    return false;
  };
  const cncLockReason = (itemId: string) => {
    if (itemId === "lesson-4") {
      return "Cần đạt >= 80% Quiz Bài 2 và Bài 3.";
    }
    if (itemId === "lesson-5" || itemId === "lesson-6") {
      return "Cần được giảng viên đánh giá Đạt ở Bài 4.";
    }
    return "";
  };

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

        {!supabaseConfigured ? (
          <p className="text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : !classes ? (
          <SkeletonGrid count={3} />
        ) : classes.length === 0 ? (
          <p className="text-slate-400">Chưa có lớp nào.</p>
        ) : (
          <>
            <div className="mb-6 inline-flex rounded-full border border-white/10 bg-white/5 p-1">
              {CLASS_TABS.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`rounded-full px-5 py-2 text-sm font-semibold transition-colors ${
                    activeTab === tab.id
                      ? "bg-[#3B82F6] text-white"
                      : "text-slate-300 hover:bg-white/10 hover:text-white"
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {activeTab === "secondary" ? (
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
            ) : (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {UNIVERSITY_CLASSES.map((universityClass) => (
                  <button
                    key={universityClass.title}
                    onClick={() => setActiveUniversityClass(universityClass.title)}
                    className={`rounded-2xl border bg-[#0B1020] p-5 text-left transition-all hover:-translate-y-1 hover:border-[#3B82F6]/50 ${
                      activeUniversityClass === universityClass.title
                        ? "border-[#3B82F6]/70"
                        : "border-white/10"
                    }`}
                  >
                    <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/5 text-2xl">
                      {universityClass.icon}
                    </span>
                    <h2 className="mt-5 font-display text-lg font-bold text-white">
                      {universityClass.title}
                    </h2>
                    <p className="mt-3 text-sm leading-6 text-slate-400">
                      {universityClass.description}
                    </p>
                  </button>
                ))}
              </div>
            )}

            {activeTab === "university" && activeUniversityClass === "Gia công CNC" && (
              <section className="mt-10 overflow-hidden rounded-2xl border border-white/10 bg-[#080D1A]">
                <div className="border-b border-white/10 p-6">
                  <p className="text-sm font-semibold tracking-wide text-[#60A5FA] uppercase">
                    MĐ CNC - Thực tập máy tiện phay điều khiển theo chương trình số
                  </p>
                  <div className="mt-3 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
                    <div>
                      <h2 className="font-display text-2xl font-bold text-white">
                        LMS môn Gia công CNC
                      </h2>
                      <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
                        Cấu trúc 70 tiết theo mô-đun, bài học, đề mục, tài nguyên
                        và hoạt động. Tiến độ thực hành được kiểm soát bằng điều
                        kiện quiz và đánh giá của giảng viên.
                      </p>
                    </div>
                    <div className="grid gap-2 text-xs font-semibold text-slate-300 sm:grid-cols-3 lg:min-w-[360px]">
                      <span className="rounded-xl bg-white/5 px-3 py-2">
                        Quiz tiện: {CNC_PROGRESS.turningQuizScore}%
                      </span>
                      <span className="rounded-xl bg-white/5 px-3 py-2">
                        Quiz phay: {CNC_PROGRESS.millingQuizScore}%
                      </span>
                      <span
                        className={`rounded-xl px-3 py-2 ${
                          cncProductionUnlocked
                            ? "bg-emerald-500/15 text-emerald-200"
                            : "bg-amber-500/15 text-amber-200"
                        }`}
                      >
                        Bài 4: {cncProductionUnlocked ? "Đạt" : "Chờ đánh giá"}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="grid lg:grid-cols-[300px_1fr]">
                  <aside className="border-b border-white/10 bg-[#050914] p-4 lg:border-r lg:border-b-0">
                    <p className="px-3 pb-3 text-xs font-bold tracking-wide text-slate-500 uppercase">
                      Cây nội dung môn học
                    </p>
                    <div className="space-y-2">
                      {CNC_COURSE_ITEMS.map((item) => {
                        const locked = isCncItemLocked(item.id);
                        const selected = activeCncItem.id === item.id;
                        return (
                          <button
                            key={item.id}
                            disabled={locked}
                            onClick={() => setActiveCncItemId(item.id)}
                            className={`w-full rounded-xl border px-3 py-3 text-left transition-colors ${
                              selected
                                ? "border-[#3B82F6]/70 bg-[#3B82F6]/15"
                                : "border-white/10 bg-white/5 hover:bg-white/10"
                            } ${locked ? "cursor-not-allowed opacity-55" : ""}`}
                          >
                            <span className="flex items-start justify-between gap-3">
                              <span>
                                <span className="block text-sm font-semibold text-white">
                                  {item.shortTitle}
                                </span>
                                <span className="mt-1 block text-xs text-slate-400">
                                  {item.duration}
                                </span>
                              </span>
                              <span className="text-xs text-slate-400">
                                {locked ? "Khóa" : "Mở"}
                              </span>
                            </span>
                            {locked && (
                              <span className="mt-2 block text-xs leading-5 text-amber-200">
                                {cncLockReason(item.id)}
                              </span>
                            )}
                          </button>
                        );
                      })}
                    </div>
                  </aside>

                  <div className="space-y-6 p-6">
                    <div>
                      <p className="text-sm font-semibold tracking-wide text-[#60A5FA] uppercase">
                        {activeCncItem.duration}
                      </p>
                      <h3 className="mt-2 font-display text-2xl font-bold text-white">
                        {activeCncItem.title}
                      </h3>
                      {"emphasis" in activeCncItem && activeCncItem.emphasis && (
                        <p className="mt-3 w-fit rounded-full bg-amber-500/15 px-3 py-1 text-xs font-bold text-amber-200">
                          {activeCncItem.emphasis}
                        </p>
                      )}
                    </div>

                    {"flipped" in activeCncItem && activeCncItem.flipped && (
                      <div className="rounded-2xl border border-[#3B82F6]/30 bg-[#3B82F6]/10 p-5">
                        <p className="text-sm font-bold tracking-wide text-[#BFDBFE] uppercase">
                          Chuẩn bị trước khi đến xưởng
                        </p>
                        <div className="mt-4 grid gap-4 xl:grid-cols-[1.1fr_1fr]">
                          <div className="flex min-h-56 items-center justify-center rounded-xl border border-white/10 bg-black/30 p-6 text-center">
                            <div>
                              <p className="font-display text-lg font-bold text-white">
                                Trình xem video thị phạm
                              </p>
                              <p className="mt-2 text-sm leading-6 text-slate-400">
                                Video quy trình mở máy, đưa về chuẩn máy, gá dao,
                                gá phôi và cài đặt offset trước khi chạy thử.
                              </p>
                              <button className="mt-4 rounded-full bg-[#3B82F6] px-5 py-2 text-sm font-bold text-white">
                                Xem video
                              </button>
                            </div>
                          </div>

                          <div className="rounded-xl border border-white/10 bg-[#050914] p-4">
                            <div className="flex items-center justify-between gap-3">
                              <p className="text-sm font-bold text-white">
                                Interactive Checklist
                              </p>
                              <span className="rounded-full bg-white/5 px-3 py-1 text-xs font-bold text-slate-300">
                                {checkedSetupSteps}/{CNC_SETUP_CHECKLIST.length}
                              </span>
                            </div>
                            <div className="mt-3 max-h-72 space-y-2 overflow-auto pr-1">
                              {CNC_SETUP_CHECKLIST.map((step) => (
                                <label
                                  key={step}
                                  className="flex gap-3 rounded-lg bg-white/5 px-3 py-2 text-sm leading-5 text-slate-300"
                                >
                                  <input
                                    type="checkbox"
                                    checked={Boolean(cncChecklist[step])}
                                    onChange={(event) =>
                                      setCncChecklist((current) => ({
                                        ...current,
                                        [step]: event.target.checked,
                                      }))
                                    }
                                    className="mt-1"
                                  />
                                  <span>{step}</span>
                                </label>
                              ))}
                            </div>
                          </div>
                        </div>

                        <div className="mt-5 rounded-xl border border-white/10 bg-[#050914] p-4">
                          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                            <div>
                              <p className="font-display text-lg font-bold text-white">
                                Quiz chốt chặn trước khi lên máy
                              </p>
                              <p className="mt-1 text-sm text-slate-400">
                                Sinh viên phải trả lời đúng toàn bộ 10/10 câu mới
                                được lên máy thực tập.
                              </p>
                            </div>
                            <span
                              className={`w-fit rounded-full px-3 py-1 text-xs font-bold ${
                                cncGatePassed
                                  ? "bg-emerald-500/15 text-emerald-200"
                                  : "bg-amber-500/15 text-amber-200"
                              }`}
                            >
                              {cncGateSubmitted
                                ? `${cncGateScore}/${CNC_GATE_QUIZ.length} câu đúng`
                                : "Chưa nộp"}
                            </span>
                          </div>

                          <div className="mt-4 space-y-4">
                            {CNC_GATE_QUIZ.map((question, questionIndex) => {
                              const selected = cncGateAnswers[question.id];
                              const answeredCorrectly =
                                selected === question.correctIndex;
                              return (
                                <div
                                  key={question.id}
                                  className="rounded-xl border border-white/10 bg-white/5 p-4"
                                >
                                  <p className="text-sm font-semibold leading-6 text-white">
                                    {questionIndex + 1}. {question.question}
                                  </p>
                                  <div className="mt-3 grid gap-2">
                                    {question.options.map((option, optionIndex) => (
                                      <label
                                        key={option}
                                        className={`flex gap-3 rounded-lg border px-3 py-2 text-sm leading-5 transition-colors ${
                                          selected === optionIndex
                                            ? "border-[#3B82F6]/70 bg-[#3B82F6]/15 text-white"
                                            : "border-white/10 bg-[#050914] text-slate-300"
                                        }`}
                                      >
                                        <input
                                          type="radio"
                                          name={question.id}
                                          checked={selected === optionIndex}
                                          onChange={() => {
                                            setCncGateSubmitted(false);
                                            setCncGateAnswers((current) => ({
                                              ...current,
                                              [question.id]: optionIndex,
                                            }));
                                          }}
                                          className="mt-1"
                                        />
                                        <span>{option}</span>
                                      </label>
                                    ))}
                                  </div>
                                  {cncGateSubmitted && !answeredCorrectly && (
                                    <p className="mt-3 rounded-lg bg-red-500/10 px-3 py-2 text-xs leading-5 text-red-200">
                                      Chưa đạt. Ôn lại: {question.explanation}
                                    </p>
                                  )}
                                </div>
                              );
                            })}
                          </div>

                          <button
                            type="button"
                            onClick={() => setCncGateSubmitted(true)}
                            className="mt-5 rounded-full bg-[#3B82F6] px-5 py-2 text-sm font-bold text-white hover:bg-[#2563EB]"
                          >
                            Nộp Quiz 10-Minute Setup
                          </button>
                          {cncGateSubmitted && (
                            <p
                              className={`mt-3 rounded-xl px-4 py-3 text-sm font-semibold ${
                                cncGatePassed
                                  ? "bg-emerald-500/15 text-emerald-200"
                                  : "bg-amber-500/15 text-amber-200"
                              }`}
                            >
                              {cncGatePassed
                                ? "Đạt chốt chặn: sinh viên đủ điều kiện lên máy thực tập."
                                : "Chưa đạt chốt chặn: phải đúng đủ 10/10 câu mới được lên máy."}
                            </p>
                          )}
                        </div>
                      </div>
                    )}

                    {"topics" in activeCncItem && activeCncItem.topics && (
                      <div>
                        <p className="text-sm font-bold tracking-wide text-slate-200 uppercase">
                          Đề mục bài học
                        </p>
                        <div className="mt-3 grid gap-2 md:grid-cols-2">
                          {activeCncItem.topics.map((topic) => (
                            <p
                              key={topic}
                              className="rounded-xl bg-white/5 px-4 py-3 text-sm leading-6 text-slate-300"
                            >
                              {topic}
                            </p>
                          ))}
                        </div>
                      </div>
                    )}

                    {"resources" in activeCncItem && activeCncItem.resources && (
                      <div>
                        <p className="text-sm font-bold tracking-wide text-slate-200 uppercase">
                          Tài nguyên
                        </p>
                        <div className="mt-3 grid gap-2 md:grid-cols-2">
                          {activeCncItem.resources.map((resource) => (
                            <p
                              key={resource}
                              className="rounded-xl border border-white/10 bg-[#0B1020] px-4 py-3 text-sm leading-6 text-slate-300"
                            >
                              {resource}
                            </p>
                          ))}
                        </div>
                      </div>
                    )}

                    <div>
                      <p className="text-sm font-bold tracking-wide text-slate-200 uppercase">
                        Hoạt động
                      </p>
                      <div className="mt-3 grid gap-2 md:grid-cols-2">
                        {activeCncItem.activities.map((activity) => (
                          <p
                            key={activity}
                            className="rounded-xl border border-[#3B82F6]/20 bg-[#3B82F6]/10 px-4 py-3 text-sm leading-6 text-slate-300"
                          >
                            {activity}
                          </p>
                        ))}
                      </div>
                    </div>

                    {"assignment" in activeCncItem && activeCncItem.assignment && (
                      <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
                        <p className="text-sm font-bold tracking-wide text-slate-200 uppercase">
                          Khu vực nộp bài
                        </p>
                        <h4 className="mt-3 font-display text-lg font-bold text-white">
                          {activeCncItem.assignment.title}
                        </h4>
                        <p className="mt-2 text-sm leading-6 text-slate-400">
                          {activeCncItem.assignment.requirement}
                        </p>
                        <div className="mt-4 rounded-xl border border-dashed border-white/20 bg-white/5 p-5 text-center">
                          <p className="text-sm font-semibold text-white">
                            Kéo thả file hoặc chọn file để nộp
                          </p>
                          <p className="mt-1 text-xs text-slate-400">
                            Định dạng yêu cầu: {activeCncItem.assignment.accept}
                          </p>
                          <button className="mt-4 rounded-full bg-[#3B82F6] px-5 py-2 text-sm font-bold text-white">
                            Chọn file
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </section>
            )}

            {activeTab === "secondary" && active && (
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
                            className="rounded-2xl border border-white/10 bg-[#080D1A] p-2"
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
                                    <span className="block truncate font-display text-sm font-bold tracking-wide text-white uppercase group-hover:text-[#3B82F6]">
                                      {l.title}
                                    </span>
                                    <span className="mt-0.5 block text-xs font-semibold tracking-wide text-[#60A5FA] uppercase">
                                      {l.itemCount} mục
                                    </span>
                                  </span>
                                  <span className="text-slate-500 transition-transform group-hover:translate-x-1 group-hover:text-[#3B82F6]">
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
                  </section>
                )}

                {!session && (
                  <p className="text-sm text-slate-400">
                    <Link
                      href="/dang-nhap"
                      className="text-[#3B82F6] hover:underline"
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
                  </section>
                )}
              </div>
            )}
          </>
        )}
      </main>
      <Footer />
    </>
  );
}
