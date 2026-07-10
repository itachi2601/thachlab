"use client";

import { useMemo, useState } from "react";
import {
  CNC_COURSE_ITEMS,
  CNC_GATE_QUIZ,
  CNC_PROGRESS,
  CNC_SETUP_CHECKLIST,
  type CncGateQuizQuestion,
  type CncCourseItem,
} from "@/services/cnc-lms";
import { useToast } from "@/components/ui/Toast";

type EditableCncItem = {
  id: string;
  title: string;
  shortTitle: string;
  duration: string;
  emphasis?: string;
  topics: string[];
  resources: string[];
  activities: string[];
  flipped?: boolean;
  assignment?: {
    title: string;
    requirement: string;
    accept: string;
  };
};

type EditableGateQuestion = {
  id: string;
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
};

function normalizeItem(item: CncCourseItem): EditableCncItem {
  return {
    id: item.id,
    title: item.title,
    shortTitle: item.shortTitle,
    duration: item.duration,
    emphasis: "emphasis" in item ? item.emphasis : "",
    topics: "topics" in item ? [...(item.topics ?? [])] : [],
    resources: "resources" in item ? [...(item.resources ?? [])] : [],
    activities: [...item.activities],
    flipped: "flipped" in item ? item.flipped : false,
    assignment:
      "assignment" in item && item.assignment
        ? { ...item.assignment }
        : undefined,
  };
}

function normalizeQuestion(question: CncGateQuizQuestion): EditableGateQuestion {
  return {
    id: question.id,
    question: question.question,
    options: [...question.options],
    correctIndex: question.correctIndex,
    explanation: question.explanation,
  };
}

function linesToList(value: string) {
  return value
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

function listToLines(value: string[]) {
  return value.join("\n");
}

export default function CncLmsAdmin() {
  const toast = useToast();
  const [items, setItems] = useState<EditableCncItem[]>(
    CNC_COURSE_ITEMS.map(normalizeItem),
  );
  const [activeId, setActiveId] = useState(items[0]?.id ?? "intro");
  const [checklist, setChecklist] = useState([...CNC_SETUP_CHECKLIST]);
  const [gateQuiz, setGateQuiz] = useState<EditableGateQuestion[]>(
    CNC_GATE_QUIZ.map(normalizeQuestion),
  );
  const [turningQuizScore, setTurningQuizScore] = useState(
    CNC_PROGRESS.turningQuizScore,
  );
  const [millingQuizScore, setMillingQuizScore] = useState(
    CNC_PROGRESS.millingQuizScore,
  );
  const [operationPassedByInstructor, setOperationPassedByInstructor] = useState(
    CNC_PROGRESS.operationPassedByInstructor,
  );

  const activeItem = items.find((item) => item.id === activeId) ?? items[0];
  const lesson4Unlocked = turningQuizScore >= 80 && millingQuizScore >= 80;
  const productionUnlocked = operationPassedByInstructor;

  const lockPreview = useMemo(
    () =>
      items.map((item) => {
        if (item.id === "lesson-4") {
          return {
            id: item.id,
            title: item.shortTitle,
            locked: !lesson4Unlocked,
            reason: "Quiz Bài 2 và Bài 3 cần đạt từ 80%.",
          };
        }
        if (item.id === "lesson-5" || item.id === "lesson-6") {
          return {
            id: item.id,
            title: item.shortTitle,
            locked: !productionUnlocked,
            reason: "Cần giảng viên đánh giá Đạt ở Bài 4.",
          };
        }
        return { id: item.id, title: item.shortTitle, locked: false, reason: "" };
      }),
    [items, lesson4Unlocked, productionUnlocked],
  );

  function updateActive(patch: Partial<EditableCncItem>) {
    setItems((current) =>
      current.map((item) =>
        item.id === activeItem.id ? { ...item, ...patch } : item,
      ),
    );
  }

  function updateAssignment(patch: Partial<NonNullable<EditableCncItem["assignment"]>>) {
    updateActive({
      assignment: {
        title: activeItem.assignment?.title ?? "",
        requirement: activeItem.assignment?.requirement ?? "",
        accept: activeItem.assignment?.accept ?? "",
        ...patch,
      },
    });
  }

  function exportConfig() {
    const payload = {
      progressRules: {
        lesson4: "Mở khi Quiz Bài 2 và Bài 3 đều >= 80%",
        lesson5And6: "Mở khi Bài 4 được giảng viên đánh giá Đạt",
      },
      previewProgress: {
        turningQuizScore,
        millingQuizScore,
        operationPassedByInstructor,
      },
      setupChecklist: checklist,
      gateQuiz,
      courseItems: items,
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "cnc-lms-config.json";
    link.click();
    URL.revokeObjectURL(url);
  }

  function updateGateQuestion(
    questionId: string,
    patch: Partial<EditableGateQuestion>,
  ) {
    setGateQuiz((current) =>
      current.map((question) =>
        question.id === questionId ? { ...question, ...patch } : question,
      ),
    );
  }

  if (!activeItem) {
    return <p className="text-sm text-slate-400">Chưa có nội dung LMS CNC.</p>;
  }

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <h2 className="font-display text-lg font-semibold text-white">
              Quản lý LMS Gia công CNC
            </h2>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
              Quản trị cấu trúc môn MĐ CNC, cây bài học, tài nguyên, hoạt động,
              khu nộp bài, checklist lớp học đảo ngược và rule khóa nội dung.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => toast("success", "Đã lưu bản nháp LMS CNC trên giao diện.")}
              className="rounded-full bg-[#2563EB] px-5 py-2 text-sm font-semibold text-white hover:bg-[#1D4ED8]"
            >
              Lưu bản nháp
            </button>
            <button
              type="button"
              onClick={exportConfig}
              className="rounded-full border border-white/15 px-5 py-2 text-sm font-semibold text-slate-200 hover:border-white/30"
            >
              Xuất JSON
            </button>
          </div>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
          <h3 className="font-display font-semibold text-white">Rule khóa</h3>
          <div className="mt-4 grid gap-3">
            <label className="text-sm text-slate-300">
              Điểm Quiz Bài 2
              <input
                type="number"
                min={0}
                max={100}
                value={turningQuizScore}
                onChange={(event) => setTurningQuizScore(Number(event.target.value))}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
            <label className="text-sm text-slate-300">
              Điểm Quiz Bài 3
              <input
                type="number"
                min={0}
                max={100}
                value={millingQuizScore}
                onChange={(event) => setMillingQuizScore(Number(event.target.value))}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
            <label className="flex items-center gap-3 rounded-xl bg-white/5 px-3 py-2 text-sm text-slate-300">
              <input
                type="checkbox"
                checked={operationPassedByInstructor}
                onChange={(event) =>
                  setOperationPassedByInstructor(event.target.checked)
                }
              />
              Bài 4 đã được giảng viên đánh giá Đạt
            </label>
          </div>
        </div>

        <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 lg:col-span-2">
          <h3 className="font-display font-semibold text-white">Xem trước khóa/mở</h3>
          <div className="mt-4 grid gap-2 sm:grid-cols-2">
            {lockPreview.map((item) => (
              <div
                key={item.id}
                className="rounded-xl border border-white/10 bg-white/5 px-4 py-3"
              >
                <div className="flex items-center justify-between gap-3">
                  <span className="text-sm font-semibold text-white">{item.title}</span>
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-bold ${
                      item.locked
                        ? "bg-amber-500/15 text-amber-200"
                        : "bg-emerald-500/15 text-emerald-200"
                    }`}
                  >
                    {item.locked ? "Khóa" : "Mở"}
                  </span>
                </div>
                {item.locked && (
                  <p className="mt-2 text-xs leading-5 text-slate-400">{item.reason}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="grid gap-5 lg:grid-cols-[280px_1fr]">
        <aside className="rounded-2xl border border-white/10 bg-[#0B1020] p-4">
          <p className="px-2 pb-3 text-xs font-bold tracking-wide text-slate-500 uppercase">
            Cây bài học
          </p>
          <div className="space-y-2">
            {items.map((item) => (
              <button
                key={item.id}
                type="button"
                onClick={() => setActiveId(item.id)}
                className={`w-full rounded-xl border px-3 py-3 text-left transition-colors ${
                  activeItem.id === item.id
                    ? "border-[#3B82F6]/70 bg-[#3B82F6]/15"
                    : "border-white/10 bg-white/5 hover:bg-white/10"
                }`}
              >
                <span className="block text-sm font-semibold text-white">
                  {item.shortTitle}
                </span>
                <span className="mt-1 block text-xs text-slate-400">{item.duration}</span>
              </button>
            ))}
          </div>
        </aside>

        <div className="space-y-5 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
          <div className="grid gap-4 md:grid-cols-2">
            <label className="text-sm text-slate-300">
              Tên hiển thị trong sidebar
              <input
                value={activeItem.shortTitle}
                onChange={(event) => updateActive({ shortTitle: event.target.value })}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
            <label className="text-sm text-slate-300">
              Thời lượng / nhãn
              <input
                value={activeItem.duration}
                onChange={(event) => updateActive({ duration: event.target.value })}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
          </div>

          <label className="block text-sm text-slate-300">
            Tiêu đề bài học
            <input
              value={activeItem.title}
              onChange={(event) => updateActive({ title: event.target.value })}
              className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
            />
          </label>

          <label className="block text-sm text-slate-300">
            Ghi chú trọng tâm
            <input
              value={activeItem.emphasis ?? ""}
              onChange={(event) => updateActive({ emphasis: event.target.value })}
              placeholder="Ví dụ: Trọng tâm cài đặt dao, phôi"
              className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white placeholder:text-slate-500"
            />
          </label>

          <div className="grid gap-4 lg:grid-cols-3">
            <label className="block text-sm text-slate-300">
              Đề mục
              <textarea
                value={listToLines(activeItem.topics)}
                onChange={(event) =>
                  updateActive({ topics: linesToList(event.target.value) })
                }
                rows={9}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
            <label className="block text-sm text-slate-300">
              Tài nguyên
              <textarea
                value={listToLines(activeItem.resources)}
                onChange={(event) =>
                  updateActive({ resources: linesToList(event.target.value) })
                }
                rows={9}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
            <label className="block text-sm text-slate-300">
              Hoạt động
              <textarea
                value={listToLines(activeItem.activities)}
                onChange={(event) =>
                  updateActive({ activities: linesToList(event.target.value) })
                }
                rows={9}
                className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-white"
              />
            </label>
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <label className="flex items-center gap-3 text-sm text-slate-300">
                <input
                  type="checkbox"
                  checked={Boolean(activeItem.flipped)}
                  onChange={(event) => updateActive({ flipped: event.target.checked })}
                />
                Có khu lớp học đảo ngược
              </label>
              <label className="mt-4 block text-sm text-slate-300">
                Checklist Bài 4
                <textarea
                  value={listToLines(checklist)}
                  onChange={(event) => setChecklist(linesToList(event.target.value))}
                  rows={8}
                  className="mt-1 w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white"
                />
              </label>
            </div>

            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <label className="flex items-center gap-3 text-sm text-slate-300">
                <input
                  type="checkbox"
                  checked={Boolean(activeItem.assignment)}
                  onChange={(event) =>
                    updateActive({
                      assignment: event.target.checked
                        ? {
                            title: "Nộp bài",
                            requirement: "Mô tả yêu cầu nộp bài.",
                            accept: ".NC",
                          }
                        : undefined,
                    })
                  }
                />
                Có khu vực nộp bài
              </label>
              {activeItem.assignment && (
                <div className="mt-4 space-y-3">
                  <input
                    value={activeItem.assignment.title}
                    onChange={(event) => updateAssignment({ title: event.target.value })}
                    placeholder="Tên bài nộp"
                    className="w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white placeholder:text-slate-500"
                  />
                  <textarea
                    value={activeItem.assignment.requirement}
                    onChange={(event) =>
                      updateAssignment({ requirement: event.target.value })
                    }
                    placeholder="Yêu cầu nộp bài"
                    rows={4}
                    className="w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white placeholder:text-slate-500"
                  />
                  <input
                    value={activeItem.assignment.accept}
                    onChange={(event) => updateAssignment({ accept: event.target.value })}
                    placeholder=".NC, ảnh mô phỏng 3D"
                    className="w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white placeholder:text-slate-500"
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h3 className="font-display text-lg font-semibold text-white">
              Bộ 10 câu Quiz chốt chặn
            </h3>
            <p className="mt-2 text-sm leading-6 text-slate-400">
              Đây là bài kiểm tra điều kiện trước khi sinh viên được lên máy.
              Logic đạt: đúng toàn bộ {gateQuiz.length}/{gateQuiz.length} câu.
            </p>
          </div>
          <span className="w-fit rounded-full bg-amber-500/15 px-3 py-1 text-xs font-bold text-amber-200">
            Bắt buộc đạt tuyệt đối
          </span>
        </div>

        <div className="mt-5 space-y-4">
          {gateQuiz.map((question, questionIndex) => (
            <div
              key={question.id}
              className="rounded-2xl border border-white/10 bg-white/5 p-4"
            >
              <div className="flex flex-col gap-3 lg:flex-row lg:items-start">
                <label className="flex-1 text-sm text-slate-300">
                  Câu {questionIndex + 1}
                  <textarea
                    value={question.question}
                    onChange={(event) =>
                      updateGateQuestion(question.id, {
                        question: event.target.value,
                      })
                    }
                    rows={2}
                    className="mt-1 w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white"
                  />
                </label>
                <label className="text-sm text-slate-300 lg:w-44">
                  Đáp án đúng
                  <select
                    value={question.correctIndex}
                    onChange={(event) =>
                      updateGateQuestion(question.id, {
                        correctIndex: Number(event.target.value),
                      })
                    }
                    className="mt-1 w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white"
                  >
                    {question.options.map((_, optionIndex) => (
                      <option key={optionIndex} value={optionIndex}>
                        Đáp án {optionIndex + 1}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <div className="mt-3 grid gap-3 md:grid-cols-2">
                {question.options.map((option, optionIndex) => (
                  <label key={optionIndex} className="text-sm text-slate-300">
                    Lựa chọn {optionIndex + 1}
                    <input
                      value={option}
                      onChange={(event) => {
                        const nextOptions = [...question.options];
                        nextOptions[optionIndex] = event.target.value;
                        updateGateQuestion(question.id, { options: nextOptions });
                      }}
                      className="mt-1 w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white"
                    />
                  </label>
                ))}
              </div>

              <label className="mt-3 block text-sm text-slate-300">
                Giải thích khi làm sai
                <textarea
                  value={question.explanation}
                  onChange={(event) =>
                    updateGateQuestion(question.id, {
                      explanation: event.target.value,
                    })
                  }
                  rows={2}
                  className="mt-1 w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-white"
                />
              </label>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
