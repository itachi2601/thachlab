"use client";

import { Suspense, useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ChevronLeft, Sparkles, Wrench } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import Button from "@/components/ui/Button";
import ExamResultSummary from "@/components/exams/ExamResultSummary";
import ExamReviewPager from "@/components/exams/ExamReviewPager";
import FixQuizModal from "@/components/rank/FixQuizModal";
import type { FixableTopic, RankStatus } from "@/features/rank/types";
import { fetchMyExamResultDetail, type MyExamAttemptDetail } from "@/services/analytics";
import { fetchFixableTopics, fetchMyRankStatus, fetchResultRpContext, type ResultRpContext } from "@/services/rank";
import { supabaseConfigured } from "@/services/supabase";

function AttemptDetail({ resultId, fromParent }: { resultId: number; fromParent: boolean }) {
  const [detail, setDetail] = useState<MyExamAttemptDetail | null | undefined>(undefined);
  const [rp, setRp] = useState<ResultRpContext | null | undefined>(undefined);
  const [topics, setTopics] = useState<FixableTopic[]>([]);
  const [fixing, setFixing] = useState<FixableTopic | null>(null);
  const [rankStatus, setRankStatus] = useState<RankStatus | null | undefined>(undefined);

  // Bài làm, trạng thái rank và chủ đề sửa sai không phụ thuộc nhau → tải song song ngay từ đầu;
  // chỉ RP của bài (cần examId + mùa) mới chờ.
  useEffect(() => {
    fetchMyExamResultDetail(resultId).then(setDetail).catch(() => setDetail(null));
    if (fromParent) return;
    fetchMyRankStatus().then(setRankStatus).catch(() => setRankStatus(null));
    fetchFixableTopics(resultId).then(setTopics).catch(() => setTopics([]));
  }, [resultId, fromParent]);

  const loadRp = useCallback(() => {
    if (!detail || fromParent || rankStatus === undefined) return;
    fetchResultRpContext(resultId, detail.examId, rankStatus).then(setRp).catch(() => setRp(null));
  }, [detail, resultId, fromParent, rankStatus]);

  useEffect(loadRp, [loadRp]);

  function reloadAfterFix() {
    loadRp();
    fetchFixableTopics(resultId).then(setTopics).catch(() => setTopics([]));
  }

  if (detail === undefined) {
    return <p className="mt-10 text-center text-sm text-slate-400">Đang tải bài làm…</p>;
  }
  if (detail === null) {
    return <p className="mt-10 text-center text-sm text-slate-500">Không tải được bài làm này.</p>;
  }

  const dateLabel = new Date(detail.createdAt).toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric" });
  const showFix = !fromParent && rp?.sourceEnabled && topics.length > 0;

  return (
    <>
      <div className="mb-4">
        <h1 className="font-display text-2xl font-bold text-white">{detail.examTitle}</h1>
        <p className="mt-1 text-sm text-slate-400">Làm ngày {dateLabel}</p>
      </div>

      <ExamResultSummary
        questions={detail.questions}
        responses={detail.responses}
        detailAnchor="xem-lai-tung-cau"
        meta={
          rp?.sourceEnabled ? (
            <span className="inline-flex items-center gap-1.5">
              <Sparkles size={14} className="text-amber-300" />
              Bài này: <b className="text-white">{rp.practiceRp}/{rp.maxRp} RP</b>
              {rp.fixRp > 0 && (
                <>
                  {" "}· sửa sai <b className="text-white">{rp.fixRp}/{rp.fixMaxRp} RP</b>
                </>
              )}
              {" · "}
              <Link href="/lop-hoc/xep-hang/" className="text-cyan-300 hover:underline">
                Xếp hạng
              </Link>
            </span>
          ) : rp === null || rp?.sourceEnabled === false ? (
            <span className="text-slate-500">{rp === null ? "Chưa mở mùa xếp hạng" : "Bài này không tính RP"}</span>
          ) : undefined
        }
      />

      {showFix && (
        <section className="mt-8 rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-4 sm:p-5">
          <div className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-cyan-500/15 text-cyan-300">
              <Wrench size={16} />
            </span>
            <h2 className="font-display text-lg font-semibold text-white">Sửa sai để nhận RP</h2>
            <span className="ml-auto text-xs text-slate-500">
              tối đa {rp!.fixMaxRp} RP · đã nhận {rp!.fixRp}
            </span>
          </div>
          <p className="mt-2 text-sm text-slate-400">
            Với mỗi chủ đề em sai, làm một bài ngắn gồm câu <em>khác</em> cùng chủ đề từ ngân hàng. Đạt từ 80% là chủ đề đó được tính đã sửa. Tối đa 3 lượt mỗi chủ đề.
          </p>
          <ul className="mt-3 space-y-2">
            {topics.map((t) => (
              <li key={t.topicId} className="flex flex-wrap items-center gap-3 rounded-xl border border-white/10 bg-panel px-3 py-2">
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm text-white">{t.name}</span>
                  <span className="text-xs text-slate-500">
                    sai {t.wrong}/{t.total} câu · đã dùng {t.attemptsDone}/3 lượt
                  </span>
                </span>
                {t.passed ? (
                  <span className="rounded-full bg-emerald-500/15 px-3 py-1 text-xs font-semibold text-emerald-300">Đã sửa</span>
                ) : t.attemptsDone >= 3 ? (
                  <span className="text-xs text-slate-500">Hết lượt</span>
                ) : (
                  <Button size="sm" onClick={() => setFixing(t)}>
                    Làm bài sửa sai
                  </Button>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      <h2 id="xem-lai-tung-cau" className="mt-10 mb-4 scroll-mt-24 font-display text-xl font-semibold text-white">
        Xem lại từng câu
      </h2>
      <p className="mb-4 text-sm text-slate-500">
        Bấm số câu ở bảng bên dưới để xem nhanh — bảng luôn ghim trên đầu khi em cuộn trang.
      </p>
      <ExamReviewPager questions={detail.questions} responses={detail.responses} />

      {fixing && (
        <FixQuizModal
          resultId={resultId}
          topic={fixing}
          onClose={() => setFixing(null)}
          onDone={reloadAfterFix}
        />
      )}
    </>
  );
}

function DetailLoader() {
  const searchParams = useSearchParams();
  const resultId = Number(searchParams.get("id"));
  // Phụ huynh mở từ /phu-huynh (link mang ?ph=1) — quay về đúng chỗ.
  const fromParent = searchParams.get("ph") === "1";

  if (!resultId || Number.isNaN(resultId)) {
    return <p className="mt-10 text-center text-sm text-slate-500">Không tìm thấy bài làm — thiếu mã bài làm trên đường dẫn.</p>;
  }

  return (
    <>
      <Link href={fromParent ? "/phu-huynh/" : "/lop-hoc/ket-qua/"} className="mb-6 inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-white">
        <ChevronLeft size={16} /> {fromParent ? "Về Kết quả của con" : "Về Kết quả học tập"}
      </Link>
      <RequireAuth>
        <AttemptDetail key={resultId} resultId={resultId} fromParent={fromParent} />
      </RequireAuth>
    </>
  );
}

export default function KetQuaChiTietPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full">
        <div className="mx-auto w-full max-w-3xl px-6 pb-20 pt-28">
          {!supabaseConfigured ? (
            <p className="text-center text-slate-400">Hệ thống đang được cấu hình.</p>
          ) : (
            <Suspense fallback={<p className="text-center text-sm text-slate-400">Đang tải…</p>}>
              <DetailLoader />
            </Suspense>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
