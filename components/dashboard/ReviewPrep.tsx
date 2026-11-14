"use client";

/**
 * Bước 0 của bảng chữa bài: "Phân tích trước khi chữa".
 *  - Phần máy tính (hiện ngay, không tốn AI): điểm trung bình, chủ đề cần ôn xếp theo % đúng, lỗi hay gặp.
 *  - Phần AI (giáo viên bấm mới chạy): nhận xét chung, chủ đề cần ôn kèm lý do + cách ôn, chẩn đoán lỗi hiểu
 *    sai ở câu khó, thứ tự chữa gợi ý.
 * Chỉ giáo viên/trợ giảng thấy (trang chữa bài nằm sau RequireAuth khu THPT/trợ giảng).
 */
import { useMemo, useState } from "react";
import { ArrowRight, Loader2, RefreshCw, Sparkles, X } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtmlLazy";
import type { ExamReviewData } from "@/services/analytics";
import { buildAiPayload, computeReviewInsights, type TopicInsight } from "@/lib/review-analysis";
import { analyzeExamResults, type AiExamAnalysis } from "@/services/ai-exam-analysis";

const LEVEL_LABEL: Record<TopicInsight["level"], string> = { cao: "Cần ôn ngay", vua: "Nên ôn", thap: "Ổn" };

function escapeHtml(s: string) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
/** Chữ AI có thể chứa $…$ — đưa qua ContentHtml để KaTeX dựng công thức (đã escape HTML). */
function AiText({ text }: { text: string }) {
  return <ContentHtml html={escapeHtml(text)} />;
}

function bandOf(p: number | null) {
  if (p === null) return "mid";
  return p >= 75 ? "easy" : p >= 50 ? "mid" : "hard";
}

export default function ReviewPrep({
  data,
  examId,
  classId,
  ai,
  onAi,
  onJump,
  onClose,
}: {
  data: ExamReviewData;
  examId: number;
  classId: number;
  ai: AiExamAnalysis | null;
  onAi: (a: AiExamAnalysis) => void;
  onJump: (questionIndex: number) => void;
  onClose: () => void;
}) {
  const insights = useMemo(() => computeReviewInsights(data), [data]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const hardCount = insights.questions.filter((q) => q.pct !== null && q.pct < 50).length;
  const order = ai?.reviewOrder.length ? ai.reviewOrder : insights.reviewOrder;

  async function runAi() {
    setLoading(true);
    setError("");
    try {
      onAi(await analyzeExamResults(examId, classId, buildAiPayload(data)));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Gọi AI phân tích lỗi.");
    } finally {
      setLoading(false);
    }
  }

  const QChip = ({ i }: { i: number }) => {
    const p = insights.questions[i]?.pct ?? null;
    return (
      <button
        type="button"
        className={`rp-qchip rp-${bandOf(p)}`}
        onClick={() => onJump(i)}
        title={p === null ? "Chưa có lượt làm" : `${p}% đúng`}
      >
        Câu {i + 1}
        {p !== null && <small>{p}%</small>}
      </button>
    );
  };

  return (
    <div className="rp-overlay" role="dialog" aria-modal="true" aria-label="Phân tích trước khi chữa">
      <div className="rp-panel">
        <div className="rp-head">
          <div>
            <span className="rb-eyebrow">Bước 1 · Phân tích trước khi chữa</span>
            <h2>{data.examTitle}</h2>
          </div>
          <button className="rb-btn rb-btn-icon" onClick={onClose} aria-label="Đóng phân tích">
            <X size={16} />
          </button>
        </div>

        <div className="rp-kpis">
          <div>
            <b>{insights.attempts}</b>
            <span>bài nộp</span>
          </div>
          <div>
            <b>{insights.avgPct === null ? "—" : `${insights.avgPct}%`}</b>
            <span>đúng trung bình</span>
          </div>
          <div>
            <b>{hardCount}</b>
            <span>câu dưới 50%</span>
          </div>
        </div>

        {insights.attempts === 0 ? (
          <p className="rp-muted">Lớp chưa có bài nộp nào — chưa có gì để phân tích.</p>
        ) : (
          <>
            <section className="rp-sec">
              <h3>Chủ đề theo tỉ lệ đúng</h3>
              <ul className="rp-topics">
                {insights.topics.map((t) => (
                  <li key={t.topic} className={`rp-topic rp-lv-${t.level}`}>
                    <div className="rp-topic-row">
                      <span className="rp-topic-name">{t.topic}</span>
                      <span className="rp-badge">{LEVEL_LABEL[t.level]}</span>
                      <span className="rp-topic-pct">{t.pct === null ? "—" : `${t.pct}%`}</span>
                    </div>
                    <span className="rp-bar">
                      <i style={{ width: `${t.pct ?? 0}%` }} />
                    </span>
                    <div className="rp-qchips">
                      {t.questionIndexes.map((i) => (
                        <QChip key={i} i={i} />
                      ))}
                    </div>
                  </li>
                ))}
              </ul>
            </section>

            <section className="rp-sec rp-ai">
              <div className="rp-ai-head">
                <h3>
                  <Sparkles size={16} /> AI gợi ý chủ đề cần ôn
                </h3>
                <button className="rb-btn" onClick={runAi} disabled={loading}>
                  {loading ? (
                    <>
                      <Loader2 size={16} className="animate-spin" /> Đang phân tích…
                    </>
                  ) : ai ? (
                    <>
                      <RefreshCw size={16} /> Phân tích lại
                    </>
                  ) : (
                    <>
                      <Sparkles size={16} /> Chạy AI phân tích
                    </>
                  )}
                </button>
              </div>
              {error && <p className="rp-error">{error}</p>}
              {!ai && !loading && !error && (
                <p className="rp-muted">
                  AI đọc tỉ lệ đúng, phương án nhiễu được chọn và đáp số sai hay gặp của cả lớp (không gửi tên học
                  sinh) để đoán chỗ các em hiểu sai và gợi ý nên ôn gì trước khi chữa. Mất khoảng 20–60 giây.
                </p>
              )}
              {ai && (
                <>
                  {ai.overview && (
                    <div className="rp-overview">
                      <AiText text={ai.overview} />
                    </div>
                  )}
                  <ol className="rp-ai-topics">
                    {ai.topics.map((t, k) => (
                      <li key={k} className={`rp-lv-${t.priority}`}>
                        <div className="rp-topic-row">
                          <span className="rp-topic-name">{t.topic}</span>
                          <span className="rp-badge">{LEVEL_LABEL[t.priority]}</span>
                        </div>
                        {t.reason && (
                          <div className="rp-reason">
                            <AiText text={t.reason} />
                          </div>
                        )}
                        {t.reviewTip && (
                          <div className="rp-tip">
                            <b>Ôn lại: </b>
                            <AiText text={t.reviewTip} />
                          </div>
                        )}
                        {t.questionIndexes.length > 0 && (
                          <div className="rp-qchips">
                            {t.questionIndexes.map((i) => (
                              <QChip key={i} i={i} />
                            ))}
                          </div>
                        )}
                      </li>
                    ))}
                  </ol>
                  {ai.questions.length > 0 && (
                    <>
                      <h4>Lỗi hiểu sai ở câu khó</h4>
                      <ul className="rp-notes">
                        {ai.questions.map((n) => (
                          <li key={n.index}>
                            <QChip i={n.index} />
                            <div>
                              <AiText text={n.misconception} />
                              {n.teachingTip && (
                                <div className="rp-tip">
                                  <b>Cách chữa: </b>
                                  <AiText text={n.teachingTip} />
                                </div>
                              )}
                            </div>
                          </li>
                        ))}
                      </ul>
                    </>
                  )}
                  <p className="rp-muted rp-small">Gợi ý của AI — thầy/cô đối chiếu trước khi dùng.</p>
                </>
              )}
            </section>

            {order.length > 0 && (
              <section className="rp-sec">
                <h3>Thứ tự chữa gợi ý {ai?.reviewOrder.length ? "(AI)" : "(sai nhiều trước)"}</h3>
                <div className="rp-qchips">
                  {order.map((i) => (
                    <QChip key={i} i={i} />
                  ))}
                </div>
              </section>
            )}
          </>
        )}

        <div className="rp-foot">
          <button className="rb-ctl rb-ctl-main" onClick={() => (order.length ? onJump(order[0]) : onClose())}>
            Bắt đầu chữa {order.length ? `từ Câu ${order[0] + 1}` : ""} <ArrowRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
