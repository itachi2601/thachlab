"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { getSupabase } from "@/services/supabase";

type QType = "mcq" | "num" | "essay";
interface Q {
  n: number;
  type: QType;
  key: string | number;
  pts: number;
  topic?: string;
  unit?: string;
  tol?: number;
  text?: string; // đề bài (cần cho câu tự luận để AI chấm)
}
interface Test {
  id: number;
  title: string;
  kind: "pretest" | "custom";
  config: { questions: Q[] };
}
interface Score {
  got: number;
  by: "key" | "ai" | "manual";
  comment?: string;
}
interface Row {
  key: string; // khoá React cục bộ
  name: string;
  className: string;
  answers: Record<string, string>;
  manual: Record<string, Score>; // điểm tự luận (AI hoặc tay)
  saved: boolean;
}

const inputCls =
  "rounded-lg border border-white/10 bg-panel px-2 py-1.5 text-sm text-white focus:border-primary focus:outline-none";
const btnCls =
  "rounded-full border border-white/15 px-4 py-2 text-sm font-medium text-slate-200 hover:border-white/30 disabled:opacity-40";

function parseNum(s: string): number | null {
  const t = s.replace(/(\d)\s(?=\d{3}(\D|$))/g, "$1").replace(",", ".");
  const m = t.match(/-?\d+(\.\d+)?/);
  return m ? Number(m[0]) : null;
}

function autoScore(q: Q, ans: string): Score | null {
  if (q.type === "essay") return null;
  const a = (ans ?? "").trim();
  if (!a) return { got: 0, by: "key" };
  if (q.type === "mcq") return { got: a.toUpperCase() === String(q.key).toUpperCase() ? q.pts : 0, by: "key" };
  const v = parseNum(a);
  const k = Number(q.key);
  const ok = v !== null && Math.abs(v - k) <= Math.abs(k) * (q.tol ?? 0.01);
  return { got: ok ? q.pts : 0, by: "key" };
}

function scoreOf(q: Q, row: Row): Score | null {
  if (q.type === "essay") return row.manual[q.n] ?? null;
  return autoScore(q, row.answers[q.n] ?? "");
}

const round2 = (x: number) => Math.round(x * 100) / 100;

function totalOf(qs: Q[], row: Row) {
  return round2(qs.reduce((s, q) => s + (scoreOf(q, row)?.got ?? 0), 0));
}

export default function HsgGradingAdmin() {
  const [tests, setTests] = useState<Test[] | null>(null);
  const [testId, setTestId] = useState<number | null>(null);
  const [rows, setRows] = useState<Row[]>([]);
  const [busy, setBusy] = useState("");
  const [msg, setMsg] = useState("");
  const [provider, setProvider] = useState<"deepseek" | "haiku">("deepseek");
  const [creating, setCreating] = useState(false);

  const test = tests?.find((t) => t.id === testId) ?? null;
  const qs = useMemo(() => test?.config.questions ?? [], [test]);
  const mcqs = qs.filter((q) => q.type === "mcq");
  const others = qs.filter((q) => q.type !== "mcq");
  const maxTotal = round2(qs.reduce((s, q) => s + q.pts, 0));

  const loadTests = useCallback(async () => {
    const { data } = await getSupabase()
      .from("hsg_grade_tests")
      .select("id, title, kind, config")
      .eq("archived", false)
      .order("id");
    const list = (data as unknown as Test[]) ?? [];
    setTests(list);
    setTestId((cur) => cur ?? list[0]?.id ?? null);
  }, []);

  useEffect(() => {
    loadTests();
  }, [loadTests]);

  useEffect(() => {
    if (!testId) return;
    getSupabase()
      .from("hsg_grade_sheets")
      .select("id, student_name, class_name, answers, scores")
      .eq("test_id", testId)
      .order("created_at")
      .then(({ data }) => {
        type S = { id: number; student_name: string; class_name: string; answers: Record<string, string>; scores: Record<string, Score> };
        setRows(
          ((data as unknown as S[]) ?? []).map((s) => ({
            key: `db${s.id}`,
            name: s.student_name,
            className: s.class_name,
            answers: s.answers ?? {},
            manual: Object.fromEntries(Object.entries(s.scores ?? {}).filter(([, v]) => v.by !== "key")),
            saved: true,
          })),
        );
      });
  }, [testId]);

  function patch(key: string, fn: (r: Row) => Row) {
    setRows((rs) => rs.map((r) => (r.key === key ? { ...fn(r), saved: false } : r)));
  }

  function addRow() {
    const last = rows[rows.length - 1];
    setRows((rs) => [
      ...rs,
      { key: `n${Date.now()}`, name: "", className: last?.className ?? "", answers: {}, manual: {}, saved: false },
    ]);
  }

  // Gõ/dán cả chuỗi "CBADA…" → gán lần lượt cho các câu trắc nghiệm.
  function setMcqString(key: string, s: string) {
    const letters = s.replace(/[^A-Da-d]/g, "").toUpperCase().split("");
    patch(key, (r) => {
      const answers = { ...r.answers };
      mcqs.forEach((q, i) => {
        if (letters[i]) answers[q.n] = letters[i];
        else delete answers[q.n];
      });
      return { ...r, answers };
    });
  }
  const mcqString = (r: Row) => mcqs.map((q) => r.answers[q.n] ?? "·").join("");

  async function save() {
    if (!test) return;
    const valid = rows.filter((r) => r.name.trim());
    if (!valid.length) return setMsg("Chưa có học sinh nào có tên.");
    setBusy("save");
    const payload = valid.map((r) => ({
      test_id: test.id,
      student_name: r.name.trim(),
      class_name: r.className.trim(),
      answers: r.answers,
      scores: Object.fromEntries(
        qs.flatMap((q) => {
          const s = scoreOf(q, r);
          return s ? [[q.n, s]] : [];
        }),
      ),
      total: totalOf(qs, r),
      updated_at: new Date().toISOString(),
    }));
    const { error } = await getSupabase()
      .from("hsg_grade_sheets")
      .upsert(payload, { onConflict: "test_id,student_name,class_name" });
    setBusy("");
    if (error) return setMsg(`Lưu lỗi: ${error.message}`);
    setRows((rs) => rs.map((r) => ({ ...r, saved: r.name.trim() ? true : r.saved })));
    setMsg(`Đã lưu ${valid.length} bài.`);
  }

  async function aiGrade(onlyKey?: string) {
    if (!test) return;
    const essays = qs.filter((q) => q.type === "essay");
    if (!essays.length) return setMsg("Bài này không có câu tự luận.");
    setBusy("ai");
    setMsg("");
    let done = 0;
    let failed = "";
    for (const r of rows.filter((x) => (onlyKey ? x.key === onlyKey : x.name.trim()))) {
      const items = essays
        .filter((q) => (r.answers[q.n] ?? "").trim() && !(r.manual[q.n]?.by === "manual"))
        .map((q) => ({
          n: q.n,
          question: q.text ?? "",
          reference: String(q.key),
          max: q.pts,
          answer: r.answers[q.n],
        }));
      if (!items.length) continue;
      const { data, error } = await getSupabase().functions.invoke("hsg-ai-grade", { body: { provider, items } });
      if (error) {
        failed = error.message;
        break;
      }
      const results = (data as { results?: { n: number; got: number; comment: string }[] })?.results ?? [];
      setRows((rs) =>
        rs.map((x) =>
          x.key === r.key
            ? {
                ...x,
                saved: false,
                manual: {
                  ...x.manual,
                  ...Object.fromEntries(results.map((s) => [s.n, { got: s.got, by: "ai" as const, comment: s.comment }])),
                },
              }
            : x,
        ),
      );
      done++;
    }
    setBusy("");
    setMsg(failed ? `Chấm AI lỗi: ${failed}` : `AI đã chấm ${done} bài — xem lại rồi bấm Lưu.`);
  }

  // Điểm trung bình theo chủ đề (chẩn đoán lớp).
  const topicStats = useMemo(() => {
    const m = new Map<string, { got: number; max: number }>();
    for (const r of rows) {
      if (!r.name.trim()) continue;
      for (const q of qs) {
        const t = q.topic || "Chung";
        const cur = m.get(t) ?? { got: 0, max: 0 };
        cur.got += scoreOf(q, r)?.got ?? 0;
        cur.max += q.pts;
        m.set(t, cur);
      }
    }
    return [...m.entries()];
  }, [rows, qs]);

  if (!tests) return <p className="text-slate-400">Đang tải…</p>;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <select
          value={testId ?? ""}
          onChange={(e) => setTestId(Number(e.target.value))}
          className={`${inputCls} py-2`}
        >
          {tests.map((t) => (
            <option key={t.id} value={t.id}>
              {t.title}
            </option>
          ))}
        </select>
        <button className={btnCls} onClick={() => setCreating((v) => !v)}>
          {creating ? "Đóng" : "+ Bài chấm mới"}
        </button>
        {test && (
          <span className="text-sm text-slate-400">
            {qs.length} câu · tối đa {maxTotal} điểm
          </span>
        )}
      </div>

      {creating && (
        <NewTestForm
          onDone={async (id) => {
            setCreating(false);
            await loadTests();
            setTestId(id);
          }}
        />
      )}

      {test && (
        <>
          <p className="text-xs text-slate-400">
            Trắc nghiệm: gõ hoặc dán cả chuỗi chữ cái ({mcqs.length} câu, ví dụ CBADA…; ký tự khác chữ A–D bị bỏ qua).
            {others.some((q) => q.type === "num") && " Câu đáp số: ghi số (đơn vị tuỳ ý), sai số cho phép 1%."}
          </p>

          <div className="admin-table-wrap">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-slate-400">
                  <th className="p-2">Học sinh</th>
                  <th className="p-2">Lớp</th>
                  {mcqs.length > 0 && <th className="p-2">Trắc nghiệm (câu {mcqs[0].n}–{mcqs[mcqs.length - 1].n})</th>}
                  {others.map((q) => (
                    <th key={q.n} className="p-2">
                      Câu {q.n}
                      <span className="block text-xs font-normal">{q.type === "num" ? `đáp số${q.unit ? ` (${q.unit})` : ""}` : "tự luận"} · /{q.pts}</span>
                    </th>
                  ))}
                  <th className="p-2">Điểm</th>
                  <th className="p-2" />
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.key} className="border-t border-white/5 align-top">
                    <td className="p-2">
                      <input className={`${inputCls} w-36`} value={r.name} placeholder="Họ tên"
                        onChange={(e) => patch(r.key, (x) => ({ ...x, name: e.target.value }))} />
                    </td>
                    <td className="p-2">
                      <input className={`${inputCls} w-16`} value={r.className} placeholder="9A"
                        onChange={(e) => patch(r.key, (x) => ({ ...x, className: e.target.value }))} />
                    </td>
                    {mcqs.length > 0 && (
                      <td className="p-2">
                        <input
                          className={`${inputCls} w-64 font-mono tracking-wider`}
                          value={mcqString(r)}
                          placeholder={"·".repeat(mcqs.length)}
                          onFocus={(e) => e.currentTarget.select()}
                          onChange={(e) => setMcqString(r.key, e.target.value)}
                        />
                        <span className="mt-1 block text-xs text-slate-500">
                          Sai câu: {mcqs.filter((q) => (scoreOf(q, r)?.got ?? 0) === 0).map((q) => q.n).join(", ") || "—"}
                        </span>
                      </td>
                    )}
                    {others.map((q) => {
                      const s = scoreOf(q, r);
                      return (
                        <td key={q.n} className="p-2">
                          {q.type === "num" ? (
                            <input className={`${inputCls} w-24`} value={r.answers[q.n] ?? ""}
                              onChange={(e) => patch(r.key, (x) => ({ ...x, answers: { ...x.answers, [q.n]: e.target.value } }))} />
                          ) : (
                            <div className="space-y-1">
                              <textarea className={`${inputCls} h-16 w-56`} value={r.answers[q.n] ?? ""}
                                placeholder="Chép bài làm…"
                                onChange={(e) => patch(r.key, (x) => ({ ...x, answers: { ...x.answers, [q.n]: e.target.value } }))} />
                              <input type="number" step={0.25} min={0} max={q.pts} className={`${inputCls} w-20`}
                                value={s?.got ?? ""} placeholder="điểm"
                                onChange={(e) =>
                                  patch(r.key, (x) => ({
                                    ...x,
                                    manual: { ...x.manual, [q.n]: { got: Math.min(q.pts, Math.max(0, Number(e.target.value))), by: "manual" } },
                                  }))
                                }
                              />
                              {s?.by === "ai" && <span className="ml-1 text-xs text-sky-300" title={s.comment}>AI</span>}
                              {s?.comment && <p className="max-w-56 text-xs text-slate-400">{s.comment}</p>}
                            </div>
                          )}
                          {q.type === "num" && s && (
                            <span className={`ml-1 text-xs ${s.got > 0 ? "text-emerald-400" : "text-rose-400"}`}>{s.got > 0 ? "✓" : "✗"}</span>
                          )}
                        </td>
                      );
                    })}
                    <td className="p-2 text-base font-semibold text-white">
                      {totalOf(qs, r)}
                      <span className="block text-xs font-normal text-slate-500">{r.saved ? "đã lưu" : "chưa lưu"}</span>
                    </td>
                    <td className="p-2">
                      <button className="text-xs text-rose-300 hover:underline"
                        onClick={() => setRows((rs) => rs.filter((x) => x.key !== r.key))}>
                        Xoá dòng
                      </button>
                      {qs.some((q) => q.type === "essay") && (
                        <button className="mt-1 block text-xs text-sky-300 hover:underline" disabled={!!busy}
                          onClick={() => aiGrade(r.key)}>
                          Chấm AI
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button className={btnCls} onClick={addRow}>+ Thêm học sinh</button>
            {qs.some((q) => q.type === "essay") && (
              <>
                <select value={provider} onChange={(e) => setProvider(e.target.value as "deepseek" | "haiku")} className={`${inputCls} py-2`}>
                  <option value="deepseek">DeepSeek</option>
                  <option value="haiku">Claude Haiku</option>
                </select>
                <button className={btnCls} disabled={!!busy} onClick={() => aiGrade()}>
                  {busy === "ai" ? "Đang chấm…" : "Chấm AI tất cả tự luận"}
                </button>
              </>
            )}
            <button className="rounded-full bg-primary px-5 py-2 text-sm font-semibold text-white disabled:opacity-40" disabled={!!busy} onClick={save}>
              {busy === "save" ? "Đang lưu…" : "Lưu"}
            </button>
            {msg && <span className="text-sm text-slate-300">{msg}</span>}
          </div>

          {topicStats.length > 0 && (
            <div>
              <h2 className="mb-2 text-sm font-semibold text-white">Mức đạt theo chủ đề (cả lớp)</h2>
              <ul className="grid gap-2 sm:grid-cols-2">
                {topicStats.map(([t, v]) => {
                  const pct = v.max ? Math.round((v.got / v.max) * 100) : 0;
                  return (
                    <li key={t} className="rounded-xl border border-white/10 p-3 text-sm">
                      <div className="flex justify-between text-slate-200"><span>{t}</span><span>{pct}%</span></div>
                      <div className="mt-1 h-1.5 rounded bg-white/10"><div className="h-full rounded bg-primary" style={{ width: `${pct}%` }} /></div>
                    </li>
                  );
                })}
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  );
}

/** Tạo bài chấm mới: ô đáp án trắc nghiệm gõ một chuỗi, thêm câu đáp số / tự luận từng câu. */
function NewTestForm({ onDone }: { onDone: (id: number) => void }) {
  const [title, setTitle] = useState("");
  const [mcqKey, setMcqKey] = useState("");
  const [mcqPts, setMcqPts] = useState(0.5);
  const [extra, setExtra] = useState<{ type: "num" | "essay"; key: string; pts: number; text: string; unit: string }[]>([]);
  const [err, setErr] = useState("");

  async function create() {
    const letters = mcqKey.replace(/[^A-Da-d]/g, "").toUpperCase().split("");
    const questions: Q[] = letters.map((k, i) => ({ n: i + 1, type: "mcq", key: k, pts: mcqPts }));
    extra.forEach((e, i) =>
      questions.push({
        n: letters.length + i + 1,
        type: e.type,
        key: e.type === "num" ? Number(e.key.replace(",", ".")) : e.key,
        pts: e.pts,
        text: e.text || undefined,
        unit: e.unit || undefined,
        tol: e.type === "num" ? 0.01 : undefined,
      }),
    );
    if (!title.trim() || !questions.length) return setErr("Cần tên bài và ít nhất một câu.");
    if (extra.some((e) => !e.key.trim() || (e.type === "num" && !Number.isFinite(Number(e.key.replace(",", "."))))))
      return setErr("Câu đáp số cần đáp án là số; câu tự luận cần đáp án/biểu điểm.");
    const { data, error } = await getSupabase()
      .from("hsg_grade_tests")
      .insert({ title: title.trim(), kind: "custom", config: { questions } })
      .select("id")
      .single();
    if (error) return setErr(error.message);
    onDone((data as { id: number }).id);
  }

  return (
    <div className="space-y-3 rounded-xl border border-white/10 p-4">
      <input className={`${inputCls} w-full`} placeholder="Tên bài (vd: Kiểm tra CĐ13 – Chuyển động)" value={title} onChange={(e) => setTitle(e.target.value)} />
      <div className="flex flex-wrap items-center gap-2">
        <input className={`${inputCls} w-72 font-mono tracking-wider`} placeholder="Đáp án trắc nghiệm: CBADA…" value={mcqKey} onChange={(e) => setMcqKey(e.target.value)} />
        <label className="text-sm text-slate-300">điểm/câu <input type="number" step={0.05} className={`${inputCls} w-20`} value={mcqPts} onChange={(e) => setMcqPts(Number(e.target.value))} /></label>
      </div>
      {extra.map((e, i) => (
        <div key={i} className="flex flex-wrap items-start gap-2">
          <select className={inputCls} value={e.type} onChange={(ev) => setExtra((x) => x.map((y, j) => (j === i ? { ...y, type: ev.target.value as "num" | "essay" } : y)))}>
            <option value="num">Đáp số</option>
            <option value="essay">Tự luận (AI chấm)</option>
          </select>
          {e.type === "essay" && (
            <textarea className={`${inputCls} h-16 w-64`} placeholder="Đề bài" value={e.text} onChange={(ev) => setExtra((x) => x.map((y, j) => (j === i ? { ...y, text: ev.target.value } : y)))} />
          )}
          <textarea className={`${inputCls} h-16 w-64`} placeholder={e.type === "num" ? "Đáp số (số)" : "Đáp án + biểu điểm từng ý"} value={e.key} onChange={(ev) => setExtra((x) => x.map((y, j) => (j === i ? { ...y, key: ev.target.value } : y)))} />
          {e.type === "num" && <input className={`${inputCls} w-20`} placeholder="đơn vị" value={e.unit} onChange={(ev) => setExtra((x) => x.map((y, j) => (j === i ? { ...y, unit: ev.target.value } : y)))} />}
          <input type="number" step={0.25} className={`${inputCls} w-20`} value={e.pts} onChange={(ev) => setExtra((x) => x.map((y, j) => (j === i ? { ...y, pts: Number(ev.target.value) } : y)))} />
          <button className="text-xs text-rose-300" onClick={() => setExtra((x) => x.filter((_, j) => j !== i))}>Xoá</button>
        </div>
      ))}
      <div className="flex items-center gap-3">
        <button className={btnCls} onClick={() => setExtra((x) => [...x, { type: "num", key: "", pts: 0.5, text: "", unit: "" }])}>+ Câu đáp số / tự luận</button>
        <button className="rounded-full bg-primary px-5 py-2 text-sm font-semibold text-white" onClick={create}>Tạo bài</button>
        {err && <span className="text-sm text-rose-300">{err}</span>}
      </div>
    </div>
  );
}
