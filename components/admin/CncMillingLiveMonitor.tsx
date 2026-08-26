"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Activity, Medal, Radio, RotateCcw, Send, Trophy, Users } from "lucide-react";
import {
  fetchAllCncMillingQuizAttempts,
  resetAllCncMillingQuizAttempts,
  subscribeToCncMillingQuizAttempts,
  unsubscribeFromCncMillingQuizAttempts,
  type CncMillingQuizAttempt,
} from "@/services/cnc-milling-quiz-attempts";

const statCards = [
  { id: "players", label: "Người tham gia", icon: Users, color: "from-[#7C3AED] to-[#5B21B6]" },
  { id: "online", label: "Đang làm bài", icon: Activity, color: "from-[#2563EB] to-primary-dark" },
  { id: "submitted", label: "Đã nộp bài", icon: Send, color: "from-[#F59E0B] to-[#D97706]" },
  { id: "passed", label: "Đã vượt qua", icon: Trophy, color: "from-[#10B981] to-[#059669]" },
] as const;

export default function CncMillingLiveMonitor() {
  const [attempts, setAttempts] = useState<CncMillingQuizAttempt[]>([]);
  const [loading, setLoading] = useState(true);
  const [ready, setReady] = useState(true);
  const [now, setNow] = useState(() => Date.now());
  const [resetting, setResetting] = useState(false);
  const [resetError, setResetError] = useState("");

  const refresh = useCallback(async () => {
    try {
      setAttempts(await fetchAllCncMillingQuizAttempts());
      setReady(true);
      setNow(Date.now());
    } catch {
      setReady(false);
    } finally {
      setLoading(false);
    }
  }, []);

  const resetResults = useCallback(async () => {
    if (attempts.length === 0 || !window.confirm(
      `Xóa toàn bộ kết quả của ${attempts.length} học sinh? Thao tác này không thể hoàn tác.`,
    )) return;

    setResetting(true);
    setResetError("");
    try {
      await resetAllCncMillingQuizAttempts();
      setAttempts([]);
      await refresh();
    } catch {
      setResetError("Không thể reset kết quả. Hãy kiểm tra quyền xóa trên Supabase và thử lại.");
    } finally {
      setResetting(false);
    }
  }, [attempts.length, refresh]);

  useEffect(() => {
    void refresh();
    const channel = subscribeToCncMillingQuizAttempts(() => void refresh());
    const timer = window.setInterval(() => setNow(Date.now()), 10_000);
    return () => {
      window.clearInterval(timer);
      void unsubscribeFromCncMillingQuizAttempts(channel);
    };
  }, [refresh]);

  const isOnline = useCallback((attempt: CncMillingQuizAttempt) =>
    now - new Date(attempt.last_activity_at).getTime() < 120_000, [now]);
  const leaderboard = useMemo(() => [...attempts].sort((left, right) =>
    right.score - left.score || right.answered_count - left.answered_count ||
    new Date(left.last_activity_at).getTime() - new Date(right.last_activity_at).getTime(),
  ), [attempts]);
  const onlineCount = attempts.filter(isOnline).length;
  const submittedCount = attempts.filter((attempt) => attempt.status !== "in_progress").length;
  const passedCount = attempts.filter((attempt) => attempt.status === "passed").length;
  const statValues = { players: attempts.length, online: onlineCount, submitted: submittedCount, passed: passedCount };

  return <div className="cnc-live-game">
    <section className="cnc-live-hero">
      <div>
        <span><Radio size={15} /> PHÒNG THI ĐANG TRỰC TIẾP</span>
        <h2>Vận hành máy phay CNC</h2>
        <p>Học sinh chỉ cần nhập họ tên trong bài kiểm tra. Màn hình tự cập nhật khi các em chọn đáp án hoặc nộp bài.</p>
      </div>
      <div className="cnc-live-actions">
        <div className="cnc-live-pulse"><i /><strong>LIVE</strong><small>Cập nhật realtime</small></div>
        <button type="button" className="cnc-live-reset" disabled={attempts.length === 0 || resetting} onClick={resetResults}>
          <RotateCcw size={16} /> {resetting ? "Đang reset…" : "Reset kết quả"}
        </button>
      </div>
    </section>

    <section className="cnc-live-stats">
      {statCards.map(({ id, label, icon: Icon, color }) => <article key={id} className={`bg-gradient-to-br ${color}`}>
        <Icon size={28} />
        <strong>{statValues[id]}</strong>
        <span>{label}</span>
      </article>)}
    </section>

    {!ready && !loading && <div className="cnc-live-warning">Khu vực thi trực tiếp chưa sẵn sàng. Cần cập nhật cấu hình Supabase cho chế độ tham gia không đăng nhập.</div>}
    {resetError && <div className="cnc-live-warning">{resetError}</div>}

    <div className="cnc-live-grid">
      <section className="cnc-live-leaderboard">
        <header><div><Trophy size={22} /><span><strong>Bảng xếp hạng trực tiếp</strong><small>{attempts.length} học sinh tham gia</small></span></div><b>Điểm</b></header>
        <div>
          {loading ? <p className="cnc-live-empty">Đang kết nối phòng thi…</p> : leaderboard.length === 0 ? <p className="cnc-live-empty">Chưa có học sinh vào làm bài.</p> : leaderboard.map((attempt, index) => {
            const online = isOnline(attempt);
            const progress = Math.round((attempt.answered_count / attempt.total_questions) * 100);
            const name = attempt.participant_name || attempt.profiles?.full_name || "Học sinh";
            const classLabel = attempt.class_name || attempt.profiles?.class_name || "Chưa nhập lớp";
            return <article key={attempt.id} className={index < 3 ? `rank-${index + 1}` : ""}>
              <span className="cnc-live-rank">{index < 3 ? <Medal size={22} /> : index + 1}</span>
              <span className="cnc-live-avatar">{name.trim().charAt(0).toUpperCase()}</span>
              <div className="cnc-live-player">
                <strong>{name}</strong>
                <small>{classLabel} · {attempt.answered_count}/{attempt.total_questions} câu</small>
                <i><b style={{ width: `${progress}%` }} /></i>
              </div>
              <span className={`cnc-live-status ${attempt.status}`}><i />{attempt.status === "passed" ? "Đã đạt" : attempt.status === "failed" ? "Chưa đạt" : online ? "Đang làm" : "Tạm dừng"}</span>
              <strong className="cnc-live-score">{attempt.score}<small>/{attempt.total_questions}</small></strong>
            </article>;
          })}
        </div>
      </section>
    </div>
  </div>;
}
