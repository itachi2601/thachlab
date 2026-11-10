"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, Check, ChevronDown, Pencil } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { SESSION_TYPE_META, STATUS_META } from "@/lib/tro-giang/constants";
import { FLAG_INFO, flagSession, LEVEL_INFO, type SessionFlag } from "@/lib/tro-giang/co-bat-thuong";
import { formatHours } from "@/lib/tro-giang/format";
import { getPolicyMonth, getPolicySessions, type MonthPolicy } from "@/lib/tro-giang/policy";
import { approveSessions, fetchFlagContext, type TaSessionRow } from "@/lib/tro-giang/queries";
import { getSupabase } from "@/services/supabase";
import FlagLegend from "./FlagLegend";
import PolicyMonthSummary from "./PolicyMonthSummary";
import PolicyReviewForm from "./PolicyReviewForm";
import TaAppeals from "./TaAppeals";
import PolicySessionEditor from "./PolicySessionEditor";

interface Item {
  s: TaSessionRow;
  flags: SessionFlag[];
  passRatio: number | null | undefined;
}

type Filter = "all" | "flag" | "pending" | "lop" | "phudao";

const FILTERS: [Filter, string][] = [
  ["all", "Tất cả"],
  ["flag", "Có cờ"],
  ["pending", "Chờ duyệt"],
  ["lop", "Lên lớp"],
  ["phudao", "Phụ đạo"],
];

const ATTENDANCE: Record<string, string> = {
  on_time: "Đúng giờ",
  late: "Đi muộn",
  excused_absence: "Vắng có báo",
  unexcused_absence: "Vắng không báo",
};

const AUDIT_LABEL: Record<string, string> = {
  close_month: "Chốt và công bố tháng",
  save_review: "Lưu / điều chỉnh điểm",
  reopen_after_session_edit: "Mở lại tháng do sửa công",
  insert_session: "Ghi buổi",
  update_session: "Sửa / duyệt buổi",
};

const dayLabel = (iso: string) =>
  new Date(`${iso}T12:00:00`).toLocaleDateString("vi-VN", { weekday: "short", day: "2-digit", month: "2-digit" });
const hhmm = (t: string | null) => (t ? t.slice(0, 5) : "");

function FlagChip({ flag }: { flag: SessionFlag }) {
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-semibold ${
        flag.level === "red" ? "bg-red-500/20 text-red-300" : "bg-amber-500/15 text-amber-300"
      }`}
    >
      <AlertTriangle size={11} />
      {FLAG_INFO[flag.code]?.title ?? flag.text}
    </span>
  );
}

function Tick({ ok, label }: { ok: boolean; label: string }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs ${ok ? "bg-emerald-500/15 text-emerald-300" : "bg-white/10 text-slate-400 line-through"}`}>
      {label}
    </span>
  );
}

function Facts({ item }: { item: Item }) {
  const { s, passRatio } = item;
  const p = s.policy;
  return (
    <div className="space-y-2 text-sm text-slate-300">
      <p className="text-xs text-slate-400">
        {hhmm(s.start_time) && `${hhmm(s.start_time)}–${hhmm(s.end_time)} · `}
        {s.hours ? `${formatHours(s.hours)} giờ` : "chưa có giờ"}
      </p>
      {s.session_type === "lop" && p && (
        <>
          <p>
            {ATTENDANCE[p.attendance] ?? p.attendance} · {s.student_touches ?? 0}/12 lượt tiếp xúc
            {p.homework_missing ? ` · ${p.homework_missing} em chưa làm bài` : ""}
          </p>
          <div className="flex flex-wrap gap-1.5">
            <Tick ok={p.arrived_early} label="Đến sớm" />
            <Tick ok={p.homework_checked} label="Kiểm bài tập" />
            <Tick ok={p.walked_tables} label="Đi các bàn" />
            <Tick ok={p.reported_students} label="Báo em cần chú ý" />
          </div>
          {p.teaching_minutes > 0 && (
            <p>
              Chữa bài {p.teaching_minutes} phút{p.teaching_note ? `: ${p.teaching_note}` : ""}
            </p>
          )}
          {p.attention_note && <p>Em cần chú ý: {p.attention_note}</p>}
        </>
      )}
      {s.session_type === "phudao" && (
        <>
          <p className={passRatio === 0 ? "text-red-300" : passRatio == null ? "text-slate-400" : "text-emerald-300"}>
            {passRatio == null
              ? "Bài cuối buổi: chưa gắn chủ đề, không đối chiếu được"
              : passRatio === 0
                ? "Bài cuối buổi: chưa em nào đạt trong ngày"
                : `Bài cuối buổi: ${Math.round(passRatio * 100)}% cặp em–chủ đề đạt`}
          </p>
          <ul className="space-y-1">
            {s.phudao_students.map((name) => {
              const f = p?.followups?.find((x) => x.student === name);
              return (
                <li key={name} className="rounded-lg bg-white/5 px-3 py-2">
                  <b className="text-white">{name}</b>
                  {f?.lesson ? ` · ${f.lesson}` : ""}
                  {f?.difficulty ? <span className="block text-xs text-slate-400">{f.difficulty}</span> : null}
                </li>
              );
            })}
          </ul>
        </>
      )}
      {s.session_type === "chambai" && <p>{s.papers_graded ?? 0} bài đã chấm</p>}
      {s.note && <p className="text-xs text-slate-500">Ghi chú: {s.note}</p>}
    </div>
  );
}

export default function PolicyPersonReview({ id, month }: { id: string; month: string }) {
  const toast = useToast();
  const [score, setScore] = useState<MonthPolicy | null>(null);
  const [items, setItems] = useState<Item[]>([]);
  const [audit, setAudit] = useState<{ id: number; action: string; created_at: string }[]>([]);
  const [error, setError] = useState("");
  const [revision, setRevision] = useState(0);
  const [openId, setOpenId] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [filter, setFilter] = useState<Filter>("all");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let active = true;
    (async () => {
      const [s, rows, history] = await Promise.all([
        getPolicyMonth(id, month),
        getPolicySessions(id, month),
        getSupabase().from("ta_policy_audit").select("id,action,created_at").eq("assistant_id", id).eq("month", month).order("created_at", { ascending: false }).limit(12),
      ]);
      const live = rows.filter((r) => r.status !== "rejected");
      const ctx = await fetchFlagContext(live).catch(() => ({ history: live, passRatios: new Map<string, number | null>() }));
      if (!active) return;
      setScore(s);
      setAudit(history.data ?? []);
      setItems(
        rows.map((r) => ({
          s: r,
          flags: r.status === "rejected" ? [] : flagSession(r, ctx.history, ctx.passRatios.get(r.id)),
          passRatio: ctx.passRatios.get(r.id),
        })),
      );
      setError("");
    })().catch((e) => {
      if (active) setError(e instanceof Error ? e.message : "Không tải được dữ liệu.");
    });
    return () => {
      active = false;
    };
  }, [id, month, revision]);

  const reload = useCallback(() => setRevision((r) => r + 1), []);

  const flagged = useMemo(() => items.filter((i) => i.flags.length > 0), [items]);
  const pending = items.filter((i) => i.s.status === "submitted").length;
  const shown = items.filter((i) =>
    filter === "all" ? true : filter === "flag" ? i.flags.length > 0 : filter === "pending" ? i.s.status === "submitted" : i.s.session_type === filter,
  );

  function openSession(sessionId: string, edit = false) {
    setFilter("all");
    setOpenId(sessionId);
    setEditingId(edit ? sessionId : null);
    requestAnimationFrame(() => document.getElementById(`buoi-${sessionId}`)?.scrollIntoView({ behavior: "smooth", block: "center" }));
  }

  async function approveOne(sessionId: string) {
    setBusy(true);
    try {
      await approveSessions([sessionId]);
      toast("success", "Đã duyệt buổi.");
      reload();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không duyệt được.");
    } finally {
      setBusy(false);
    }
  }

  const go = (anchor: string) => document.getElementById(anchor)?.scrollIntoView({ behavior: "smooth", block: "start" });

  if (error)
    return (
      <p role="alert" className="rounded-xl bg-red-500/10 p-4 text-red-200">
        {error}
        <button className="ml-3 underline" onClick={reload}>Thử lại</button>
      </p>
    );
  if (!score) return <p className="text-slate-400">Đang tải bảng tháng…</p>;

  const redCount = flagged.filter((i) => i.flags.some((f) => f.level === "red")).length;

  return (
    <div className="space-y-5">
      <div className="sticky top-0 z-10 -mx-1 space-y-2 border-b border-white/10 bg-panel/95 px-1 py-2 backdrop-blur">
        <div className="flex flex-wrap items-center gap-x-4 gap-y-1">
          <span className={`rounded-full px-3 py-1 text-xs font-semibold ${score.closed_at ? "bg-emerald-500/15 text-emerald-300" : "bg-amber-500/15 text-amber-200"}`}>
            {score.closed_at ? "Đã chốt" : "Tạm tính"}
          </span>
          <span className="text-sm text-slate-300">Điểm <b className="font-mono text-white">{score.total_score ?? "—"}</b>/100</span>
          <span className="text-sm text-slate-300">Tiền <b className="font-mono text-white">{score.total_pay === null ? "chờ đủ dữ liệu" : `${Math.round(score.total_pay).toLocaleString("vi-VN")} đ`}</b></span>
          {pending > 0 && <span className="text-sm text-amber-200">{pending} buổi chờ duyệt</span>}
        </div>
        <nav className="flex flex-wrap gap-2 text-sm" aria-label="Chuyển nhanh">
          {[
            ["can-xem", `Cần xem (${flagged.length})`],
            ["cac-buoi", `Các buổi (${items.length})`],
            ["diem-tien", "Điểm và tiền"],
            ["cham-chot", "Chấm và chốt"],
          ].map(([anchor, label]) => (
            <button key={anchor} type="button" onClick={() => go(anchor)} className="rounded-full border border-white/15 px-3 py-1.5 text-slate-200 hover:border-white/30">
              {label}
            </button>
          ))}
        </nav>
      </div>

      <section id="can-xem" className="scroll-mt-28 space-y-3">
        <h3 className="font-semibold text-white">Cần xem</h3>
        <FlagLegend defaultOpen={false} />
        {flagged.length === 0 ? (
          <p className="rounded-xl bg-emerald-500/10 p-4 text-sm text-emerald-200">
            Không có buổi nào bị gắn cờ trong tháng này.{pending > 0 ? ` Còn ${pending} buổi chờ duyệt, xem ở mục Các buổi.` : ""}
          </p>
        ) : (
          <>
            <p className="text-sm text-slate-300">
              {flagged.length} buổi có cờ{redCount ? `, trong đó ${redCount} buổi cờ đỏ cần xác minh trước khi chốt` : ""}. Bấm “Xem buổi” để nhảy tới đúng buổi.
            </p>
            <ul className="space-y-2">
              {[...flagged]
                .sort((a, b) => Number(b.flags.some((f) => f.level === "red")) - Number(a.flags.some((f) => f.level === "red")))
                .map((i) => (
                  <li key={i.s.id} className={`rounded-2xl border p-3 ${i.flags.some((f) => f.level === "red") ? "border-red-400/40 bg-red-500/5" : "border-amber-400/30 bg-amber-500/5"}`}>
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <b className="text-white">
                        {dayLabel(i.s.work_date)} · {SESSION_TYPE_META[i.s.session_type].label}
                        {i.s.class_label ? ` · ${i.s.class_label}` : ""}
                      </b>
                      <button type="button" onClick={() => openSession(i.s.id)} className="rounded-lg border border-white/20 px-3 py-1.5 text-sm text-white">
                        Xem buổi
                      </button>
                    </div>
                    <ul className="mt-2 space-y-2">
                      {i.flags.map((f) => (
                        <li key={f.code} className="text-sm">
                          <FlagChip flag={f} />
                          <p className="mt-1 text-slate-300">{f.text}.</p>
                          <p className="text-xs text-slate-400">Nên làm: {FLAG_INFO[f.code]?.todo}</p>
                        </li>
                      ))}
                    </ul>
                  </li>
                ))}
            </ul>
          </>
        )}
      </section>

      <section id="cac-buoi" className="scroll-mt-28 space-y-3">
        <h3 className="font-semibold text-white">Các buổi trong tháng</h3>
        <div className="flex flex-wrap gap-2" role="group" aria-label="Lọc buổi">
          {FILTERS.map(([key, label]) => (
            <button
              key={key}
              type="button"
              aria-pressed={filter === key}
              onClick={() => setFilter(key)}
              className={`rounded-full border px-3 py-1.5 text-sm ${filter === key ? "border-blue-400/60 bg-blue-500/20 text-blue-100" : "border-white/15 text-slate-300"}`}
            >
              {label}
            </button>
          ))}
        </div>
        {shown.length === 0 && <p className="rounded-xl border border-dashed border-white/10 p-4 text-center text-sm text-slate-500">Không có buổi nào khớp bộ lọc.</p>}
        <ul className="space-y-2">
          {shown.map((i) => {
            const { s } = i;
            const meta = SESSION_TYPE_META[s.session_type];
            const status = STATUS_META[s.status];
            const open = openId === s.id;
            return (
              <li key={s.id} id={`buoi-${s.id}`} className="scroll-mt-32 rounded-2xl border border-white/10 bg-white/5">
                <button
                  type="button"
                  aria-expanded={open}
                  onClick={() => {
                    setOpenId(open ? null : s.id);
                    if (open) setEditingId(null);
                  }}
                  className="flex w-full flex-wrap items-center gap-x-3 gap-y-1.5 p-3 text-left"
                >
                  <span className="min-w-[7rem] font-semibold text-white">{dayLabel(s.work_date)}</span>
                  <span className="text-sm text-slate-300">
                    {meta.label}
                    {s.class_label ? ` · ${s.class_label}` : ""}
                    {s.session_type === "phudao" ? ` · ${s.phudao_students.length} em` : ""}
                  </span>
                  <span className="text-xs text-slate-500">{s.hours ? `${formatHours(s.hours)} giờ` : ""}</span>
                  <span className={`rounded-full px-2 py-0.5 text-xs ${status.className}`}>{status.label}</span>
                  {i.flags.map((f) => (
                    <FlagChip key={f.code} flag={f} />
                  ))}
                  <ChevronDown size={16} className={`ml-auto text-slate-500 transition-transform ${open ? "rotate-180" : ""}`} />
                </button>
                {open && (
                  <div className="space-y-3 border-t border-white/10 p-3">
                    {i.flags.length > 0 && (
                      <ul className="space-y-1 text-xs text-slate-400">
                        {i.flags.map((f) => (
                          <li key={f.code}>
                            <b className={f.level === "red" ? "text-red-300" : "text-amber-300"}>{LEVEL_INFO[f.level].label}</b> · {f.text}. Nên làm: {FLAG_INFO[f.code]?.todo}
                          </li>
                        ))}
                      </ul>
                    )}
                    <Facts item={i} />
                    <div className="flex flex-wrap gap-2">
                      {s.status === "submitted" && (
                        <button type="button" disabled={busy} onClick={() => approveOne(s.id)} className="inline-flex items-center gap-1.5 rounded-xl bg-emerald-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40">
                          <Check size={14} /> Duyệt buổi này
                        </button>
                      )}
                      <button type="button" onClick={() => setEditingId(editingId === s.id ? null : s.id)} className="inline-flex items-center gap-1.5 rounded-xl border border-white/20 px-4 py-2 text-sm text-white">
                        <Pencil size={14} /> {editingId === s.id ? "Đóng phiếu sửa" : "Sửa công"}
                      </button>
                    </div>
                    {editingId === s.id && (
                      <PolicySessionEditor
                        key={s.id}
                        session={s}
                        onCancel={() => setEditingId(null)}
                        onSaved={() => {
                          setEditingId(null);
                          reload();
                        }}
                      />
                    )}
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      </section>

      <section id="diem-tien" className="scroll-mt-28 space-y-3">
        <h3 className="font-semibold text-white">Điểm và tiền</h3>
        <PolicyMonthSummary score={score} />
      </section>

      <section id="cham-chot" className="scroll-mt-28 space-y-4">
        <TaAppeals assistantId={id} month={month} admin />
        <PolicyReviewForm key={revision} score={score} onSaved={reload} />
      </section>

      {!!audit.length && (
        <details className="rounded-xl border border-white/10 p-3 text-sm text-slate-400">
          <summary>Nhật ký thay đổi gần đây</summary>
          <ul className="mt-2 space-y-1">
            {audit.map((a) => (
              <li key={a.id}>
                {new Date(a.created_at).toLocaleString("vi-VN")} · {AUDIT_LABEL[a.action] ?? a.action}
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}
