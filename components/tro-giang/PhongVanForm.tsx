"use client";

import { useCallback, useEffect, useState } from "react";
import {
  INTERVIEW_GROUPS,
  INTERVIEW_QUESTIONS,
  listInterviews,
  saveInterview,
  type InterviewGroup,
  type InterviewRow,
} from "@/lib/tro-giang/phong-van";

const FIELD = "w-full rounded-xl border border-white/15 bg-transparent px-3 py-3 text-base text-white";

function emptyForm() {
  return { code: "", grp: "" as InterviewGroup | "", answers: {} as Record<string, string>, barrier: "", wish: "" };
}

/** Trợ giảng hỏi trực tiếp từng em rồi ghi NGUYÊN VĂN câu em nói. Không ghi tên em — chỉ mã E1..E3. */
export default function PhongVanForm() {
  const [form, setForm] = useState(emptyForm);
  const [rows, setRows] = useState<InterviewRow[] | null>(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);

  const reload = useCallback(() => {
    listInterviews()
      .then(setRows)
      .catch(() => setRows([]));
  }, []);
  useEffect(reload, [reload]);

  const questions = INTERVIEW_QUESTIONS.filter((q) => !q.only || (form.grp && q.only.includes(form.grp)));
  const canSave = /^[A-Za-z][0-9]{1,2}$/.test(form.code.trim()) && form.grp !== "";

  async function submit() {
    if (!canSave || busy || form.grp === "") return;
    setBusy(true);
    setMsg(null);
    try {
      const answers: Record<string, string> = {};
      for (const q of questions) {
        const v = (form.answers[q.id] ?? "").trim();
        if (v) answers[q.id] = v;
      }
      await saveInterview({ code: form.code.trim(), grp: form.grp, answers, barrier: form.barrier.trim(), wish: form.wish.trim() });
      setMsg({ ok: true, text: `Đã lưu phiếu ${form.code.trim().toUpperCase()}.` });
      setForm(emptyForm());
      reload();
    } catch {
      setMsg({ ok: false, text: "Chưa lưu được. Kiểm tra mạng rồi bấm Lưu lại — nội dung vẫn còn trên màn hình." });
    } finally {
      setBusy(false);
    }
  }

  function edit(r: InterviewRow) {
    setForm({ code: r.code, grp: r.grp, answers: r.answers ?? {}, barrier: r.barrier ?? "", wish: r.wish ?? "" });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-white/10 p-4 text-sm text-slate-300">
        <p className="font-bold text-white">Trước khi hỏi</p>
        <ul className="mt-2 list-disc space-y-1 pl-5">
          <li>Hỏi riêng từng em, khoảng 10 phút, không có bạn bên cạnh.</li>
          <li>Nói: &quot;Em nói thật, chê cũng được, không bị trừ điểm.&quot; Dùng đúng từ em dùng (&quot;mở khoá&quot;).</li>
          <li>Ghi nguyên văn câu em nói, đừng diễn giải. Hỏi &quot;vì sao?&quot; tối đa 2 lần mỗi ý.</li>
          <li>Không hứa sẽ sửa. <b>Không ghi tên em</b> vào ô nào cả, chỉ dùng mã.</li>
        </ul>
      </section>

      <section className="space-y-4">
        <div>
          <label htmlFor="pv-code" className="mb-1 block text-sm font-bold text-white">Mã em (E1, E2, E3)</label>
          <input
            id="pv-code"
            value={form.code}
            maxLength={3}
            autoCapitalize="characters"
            onChange={(e) => setForm({ ...form, code: e.target.value })}
            className={FIELD}
            placeholder="E1"
          />
        </div>

        <fieldset>
          <legend className="mb-1 text-sm font-bold text-white">Em thuộc nhóm nào?</legend>
          <div className="space-y-2">
            {INTERVIEW_GROUPS.map((g) => (
              <label key={g.value} className="flex min-h-[44px] items-center gap-3 rounded-xl border border-white/15 px-3 py-2 text-sm text-slate-200">
                <input type="radio" name="pv-grp" checked={form.grp === g.value} onChange={() => setForm({ ...form, grp: g.value })} />
                {g.label}
              </label>
            ))}
          </div>
        </fieldset>

        {form.grp !== "" &&
          questions.map((q, i) => (
            <div key={q.id}>
              <label htmlFor={`pv-${q.id}`} className="mb-1 block text-sm font-bold text-white">
                {i + 1}. {q.text}
              </label>
              <textarea
                id={`pv-${q.id}`}
                rows={3}
                value={form.answers[q.id] ?? ""}
                onChange={(e) => setForm({ ...form, answers: { ...form.answers, [q.id]: e.target.value } })}
                className={FIELD}
                placeholder="Ghi nguyên văn câu em nói"
              />
            </div>
          ))}

        {form.grp !== "" && (
          <>
            <div>
              <label htmlFor="pv-barrier" className="mb-1 block text-sm font-bold text-white">Rào cản chính (nguyên văn câu em nói rõ nhất)</label>
              <textarea id="pv-barrier" rows={2} value={form.barrier} onChange={(e) => setForm({ ...form, barrier: e.target.value })} className={FIELD} />
            </div>
            <div>
              <label htmlFor="pv-wish" className="mb-1 block text-sm font-bold text-white">
                Nếu có cây đũa thần, em sửa đúng một thứ ở phần này của web là gì?
              </label>
              <textarea id="pv-wish" rows={2} value={form.wish} onChange={(e) => setForm({ ...form, wish: e.target.value })} className={FIELD} />
            </div>
          </>
        )}

        <button
          type="button"
          disabled={!canSave || busy}
          onClick={submit}
          className="w-full rounded-2xl bg-blue-600 py-4 text-base font-bold text-white disabled:opacity-40"
        >
          {busy ? "Đang lưu…" : "Lưu phiếu"}
        </button>
        {msg && (
          <p role="status" className={`text-sm ${msg.ok ? "text-emerald-300" : "text-amber-300"}`}>
            {msg.text}
          </p>
        )}
      </section>

      <section>
        <h2 className="mb-2 text-sm font-bold text-white">Phiếu đã ghi</h2>
        {rows === null ? (
          <p className="text-sm text-slate-400">Đang tải…</p>
        ) : rows.length === 0 ? (
          <p className="text-sm text-slate-400">Chưa có phiếu nào.</p>
        ) : (
          <ul className="space-y-2">
            {rows.map((r) => (
              <li key={r.id} className="rounded-xl border border-white/10 p-3 text-sm text-slate-300">
                <div className="flex items-center justify-between gap-2">
                  <span className="font-bold text-white">
                    {r.code} · {INTERVIEW_GROUPS.find((g) => g.value === r.grp)?.label ?? r.grp}
                  </span>
                  <button type="button" onClick={() => edit(r)} className="min-h-[44px] px-3 text-blue-300">
                    Sửa
                  </button>
                </div>
                <p className="mt-1 text-xs text-slate-500">Ghi bởi {r.by}</p>
                {r.barrier && <p className="mt-1">Rào cản: {r.barrier}</p>}
                {r.wish && <p className="mt-1">Muốn đổi: {r.wish}</p>}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
