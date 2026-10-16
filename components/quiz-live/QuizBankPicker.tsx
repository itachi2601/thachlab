"use client";

import { useEffect, useMemo, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtmlLazy";
import { useToast } from "@/components/ui/Toast";
import { bankToQuizQuestion, type QuizQuestion } from "@/features/quiz-live/text";
import { quizErrorText } from "@/features/quiz-live/types";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import { fetchQuestionTopics, type QuestionTopic } from "@/services/analytics";
import { searchBank, type BankHit } from "@/services/quiz-live";

const field = "rounded-xl border border-line-strong bg-panel px-3 py-2.5 text-sm text-ink focus:border-primary focus:outline-none";

const TIERS = ["de", "trung-binh", "kho"] as const;
const rank = (d: string) => {
  const i = TIERS.indexOf(d as (typeof TIERS)[number]);
  return i < 0 ? 1 : i;
};

/** Bốc ngẫu nhiên theo tỉ lệ ~40% dễ · 40% trung bình · 20% khó, thiếu mức nào thì bù từ mức gần nhất; xếp dễ → khó. */
async function rampPick(
  f: { grade: string; topicId: number | null; search: string; count: number },
  isUsable: (r: BankHit) => unknown,
): Promise<BankHit[]> {
  const pools = await Promise.all(
    TIERS.map((d) => searchBank({ ...f, difficulty: d, limit: f.count * 2, random: true }).then((rows) => rows.filter(isUsable))),
  );
  const quota = [Math.round(f.count * 0.4), 0, Math.round(f.count * 0.2)];
  quota[1] = f.count - quota[0] - quota[2];
  const out: BankHit[][] = pools.map((p, i) => p.slice(0, quota[i]));
  let missing = f.count - out.reduce((n, a) => n + a.length, 0);
  // Bù phần thiếu: ưu tiên trung bình, rồi dễ, cuối cùng mới tới khó.
  for (const i of [1, 0, 2]) {
    if (missing <= 0) break;
    const extra = pools[i].slice(out[i].length, out[i].length + missing);
    out[i] = out[i].concat(extra);
    missing -= extra.length;
  }
  return out.flat().sort((a, b) => rank(a.difficulty) - rank(b.difficulty));
}

/** Chọn câu trắc nghiệm từ ngân hàng. Bốc ngẫu nhiên N câu theo khối/chủ đề/mức độ, hoặc tự tick từng câu. */
export default function QuizBankPicker({
  defaultGrade,
  existingBankIds,
  onAdd,
  onClose,
}: {
  defaultGrade: string;
  existingBankIds: Set<number>;
  onAdd: (qs: QuizQuestion[]) => void;
  onClose: () => void;
}) {
  const toast = useToast();
  const [grade, setGrade] = useState(defaultGrade || "10");
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [topicId, setTopicId] = useState<number | null>(null);
  const [difficulty, setDifficulty] = useState("");
  const [search, setSearch] = useState("");
  const [countText, setCountText] = useState("10");
  const count = Math.max(1, Math.min(50, Math.floor(Number(countText)) || 1));
  const [ramp, setRamp] = useState(true);
  const [hits, setHits] = useState<BankHit[]>([]);
  const [picked, setPicked] = useState<Set<number>>(new Set());
  const [busy, setBusy] = useState(false);
  const [searched, setSearched] = useState(false);

  useEffect(() => {
    let off = false;
    fetchQuestionTopics(grade)
      .then((t) => !off && setTopics(t))
      .catch(() => !off && setTopics([]));
    return () => {
      off = true;
    };
  }, [grade]);

  // Bài (không có cha) kèm các yêu cầu cần đạt của bài đó ngay bên dưới.
  const topicOptions = useMemo(() => {
    const lessons = topics.filter((t) => t.parentId === null);
    return lessons.flatMap((l) => [
      { id: l.id, label: l.name },
      ...topics.filter((c) => c.parentId === l.id).map((c) => ({ id: c.id, label: `   – ${c.name}` })),
    ]);
  }, [topics]);

  async function run(random: boolean) {
    setBusy(true);
    try {
      const isUsable = (r: BankHit) => !existingBankIds.has(r.id) && bankToQuizQuestion(r.id, r.question);
      let usable: BankHit[];
      if (random && ramp && !difficulty) {
        usable = await rampPick({ grade, topicId, search, count }, isUsable);
      } else {
        const rows = await searchBank({ grade, topicId, difficulty, search, limit: random ? count : 60, random });
        usable = rows.filter(isUsable);
      }
      setHits(usable);
      setPicked(random ? new Set(usable.map((r) => r.id)) : new Set());
      setSearched(true);
    } catch (e) {
      toast("error", quizErrorText(e));
    } finally {
      setBusy(false);
    }
  }

  function confirm() {
    const qs = hits
      .filter((h) => picked.has(h.id))
      .map((h) => bankToQuizQuestion(h.id, h.question))
      .filter((q): q is QuizQuestion => q !== null);
    onAdd(qs);
    onClose();
  }

  return (
    <section className="space-y-4 rounded-2xl border border-line bg-surface-2 p-4">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-ink">Lấy câu từ ngân hàng</h3>
        <button onClick={onClose} className="min-h-10 px-3 text-sm text-ink hover:text-ink">Đóng</button>
      </div>
      <div className="grid gap-2 sm:grid-cols-2">
        <select aria-label="Khối" className={field} value={grade} onChange={(e) => { setGrade(e.target.value); setTopicId(null); }}>
          {["9", "10", "11", "12"].map((g) => <option key={g} value={g}>Lớp {g}</option>)}
        </select>
        <select aria-label="Chủ đề" className={field} value={topicId ?? ""} onChange={(e) => setTopicId(e.target.value ? Number(e.target.value) : null)}>
          <option value="">Mọi chủ đề</option>
          {topicOptions.map((o) => <option key={o.id} value={o.id}>{o.label}</option>)}
        </select>
        <select aria-label="Mức độ" className={field} value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
          <option value="">Mọi mức độ</option>
          {(["de", "trung-binh", "kho"] as const).map((d) => <option key={d} value={d}>{DIFFICULTY_LABELS[d]}</option>)}
        </select>
        <input aria-label="Tìm chữ trong câu" className={field} placeholder="Tìm chữ trong câu (không bắt buộc)" value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <label className="flex items-center gap-2 text-sm text-ink">
          Số câu
          <input type="number" min={1} max={50} className={`${field} w-20`} inputMode="numeric" value={countText} onChange={(e) => setCountText(e.target.value.replace(/\D/g, "").slice(0, 2))} onBlur={() => setCountText(String(count))} />
        </label>
        <label className="flex min-h-11 items-center gap-2 text-sm text-ink">
          <input type="checkbox" className="size-5" checked={ramp} onChange={(e) => setRamp(e.target.checked)} />
          Dễ → khó (ít câu khó)
        </label>
        <button disabled={busy} onClick={() => void run(true)} className="min-h-11 rounded-xl bg-primary px-4 text-sm font-bold text-white disabled:opacity-50">Bốc ngẫu nhiên</button>
        <button disabled={busy} onClick={() => void run(false)} className="min-h-11 rounded-xl border border-line px-4 text-sm text-ink disabled:opacity-50">Xem danh sách để tự chọn</button>
      </div>
      {searched && hits.length === 0 && <p className="text-sm text-muted">Không có câu trắc nghiệm phù hợp (hoặc đã thêm hết rồi).</p>}
      {hits.length > 0 && (
        <>
          <ul className="max-h-96 space-y-2 overflow-y-auto pr-1">
            {hits.map((h) => {
              const q = h.question as { question: string };
              return (
                <li key={h.id}>
                  <label className="flex cursor-pointer gap-3 rounded-xl border border-line bg-surface-2 p-3 text-sm text-ink">
                    <input
                      type="checkbox"
                      className="mt-1 size-5 shrink-0"
                      checked={picked.has(h.id)}
                      onChange={(e) => setPicked((p) => { const n = new Set(p); if (e.target.checked) n.add(h.id); else n.delete(h.id); return n; })}
                    />
                    <span className="min-w-0 flex-1">
                      <span className="line-clamp-3 block"><ContentHtml html={q.question} /></span>
                      <span className="mt-1 block text-xs text-muted">{h.topic_name || "chưa gắn chủ đề"}{h.difficulty ? ` · ${DIFFICULTY_LABELS[h.difficulty as keyof typeof DIFFICULTY_LABELS] ?? h.difficulty}` : ""}</span>
                    </span>
                  </label>
                </li>
              );
            })}
          </ul>
          <div className="flex items-center justify-between">
            <button onClick={() => setPicked(new Set(hits.map((h) => h.id)))} className="text-sm text-primary underline">Chọn tất cả</button>
            <button disabled={picked.size === 0} onClick={confirm} className="min-h-11 rounded-xl bg-primary px-5 font-bold text-white disabled:opacity-40">Thêm {picked.size} câu</button>
          </div>
        </>
      )}
    </section>
  );
}
