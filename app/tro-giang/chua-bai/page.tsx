"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { Tv } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import NotRegistered from "@/components/tro-giang/NotRegistered";
import ReviewBoard from "@/components/dashboard/ReviewBoard";
import { useAssistantOrDemo } from "@/lib/tro-giang/useAssistant";
import { fetchMyAssistantClasses, type TaAssistantClass } from "@/lib/tro-giang/queries";
import { fetchClassStudentIds } from "@/services/classes";
import { fetchClassExamResults } from "@/services/class-results";
import { fetchExamReviewData, type ExamReviewData } from "@/services/analytics";

function Picker() {
  const router = useRouter();
  const [classes, setClasses] = useState<TaAssistantClass[] | null>(null);
  const [classId, setClassId] = useState<number | null>(null);
  const [exams, setExams] = useState<{ id: number; title: string }[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchMyAssistantClasses()
      .then((list) => {
        setClasses(list);
        setClassId((cur) => cur ?? list[0]?.class_id ?? null);
      })
      .catch(() => setError("Không tải được danh sách lớp."));
  }, []);

  useEffect(() => {
    if (!classId) return;
    let cancelled = false;
    setExams(null);
    fetchClassStudentIds(classId)
      .then((ids) => fetchClassExamResults(ids))
      .then((rows) => {
        if (cancelled) return;
        const map = new Map<number, string>();
        rows.forEach((r) => map.set(r.exam_id, r.exams?.title ?? `Đề #${r.exam_id}`));
        setExams([...map.entries()].map(([id, title]) => ({ id, title })));
      })
      .catch(() => !cancelled && setError("Không tải được các đề của lớp."));
    return () => {
      cancelled = true;
    };
  }, [classId]);

  if (error) return <p className="text-red-400">{error}</p>;
  if (!classes) return <p className="text-slate-400">Đang tải…</p>;

  return (
    <div className="space-y-5">
      <Link href="/tro-giang" className="text-sm text-blue-300 underline">
        ← Trang trợ giảng
      </Link>
      <h1 className="text-xl font-bold text-white">Chữa bài</h1>
      <p className="text-sm text-slate-400">
        Chọn lớp và đề để xem đáp án, lời giải và tỉ lệ làm đúng từng câu — hỗ trợ thầy chữa bài.
      </p>
      <select
        aria-label="Chọn lớp"
        value={classId ?? ""}
        onChange={(e) => setClassId(Number(e.target.value))}
        className="w-full rounded-xl border border-white/15 bg-panel px-3 py-3 text-white"
      >
        {classes.map((c) => (
          <option key={c.class_id} value={c.class_id}>
            {c.name}
          </option>
        ))}
      </select>
      {exams === null ? (
        <p className="text-slate-400">Đang tải đề…</p>
      ) : exams.length === 0 ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">
          Lớp này chưa có lượt làm bài kiểm tra nào.
        </p>
      ) : (
        <ul className="space-y-2">
          {exams.map((e) => (
            <li key={e.id}>
              <button
                onClick={() => router.push(`/tro-giang/chua-bai?exam=${e.id}&class=${classId}`)}
                className="flex min-h-12 w-full items-center gap-3 rounded-2xl border border-white/10 bg-panel px-4 py-3 text-left text-white"
              >
                <Tv size={18} className="shrink-0 text-blue-300" />
                <span className="flex-1">{e.title}</span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function Board({ examId, classId }: { examId: number; classId: number }) {
  const [data, setData] = useState<ExamReviewData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    fetchClassStudentIds(classId)
      .then((ids) => fetchExamReviewData(examId, ids))
      .then((r) => !cancelled && setData(r))
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Không tải được dữ liệu chữa bài.");
      });
    return () => {
      cancelled = true;
    };
  }, [examId, classId]);

  if (error) return <p className="p-10 text-center text-red-400">{error}</p>;
  if (!data) return <p className="p-10 text-center text-slate-400">Đang tải đề…</p>;
  if (data.questions.length === 0)
    return <p className="p-10 text-center text-slate-400">Đề này chưa có câu hỏi.</p>;
  return <ReviewBoard data={data} examId={examId} classId={classId} canCreateHomework={false} />;
}

function Loader() {
  const { assistant } = useAssistantOrDemo();
  const params = useSearchParams();
  const examId = Number(params.get("exam"));
  const classId = Number(params.get("class"));
  const ready = assistant !== undefined && assistant !== null;

  // Bảng chữa bài chiếm trọn màn hình, không bọc Navbar/Footer.
  if (ready && examId && classId) return <Board examId={examId} classId={classId} />;

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-lg px-5 pt-28 pb-16">
        {assistant === undefined ? (
          <p className="text-slate-400">Đang tải…</p>
        ) : assistant === null ? (
          <NotRegistered />
        ) : (
          <Picker />
        )}
      </main>
      <Footer variant="app" />
    </>
  );
}

export default function TroGiangChuaBaiPage() {
  return (
    <RequireAuth>
      <Suspense fallback={<p className="p-10 text-center text-slate-400">Đang tải…</p>}>
        <Loader />
      </Suspense>
    </RequireAuth>
  );
}
