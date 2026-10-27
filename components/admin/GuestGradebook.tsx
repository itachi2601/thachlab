"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Download } from "lucide-react";
import Button from "@/components/ui/Button";
import { getSupabase } from "@/services/supabase";
import { makeQrCode, QR_QUIET_ZONE as QUIET } from "@/lib/qr";
import { SITE_URL } from "@/lib/site";

/**
 * Bảng điểm cho đề làm bằng mã (/thi/?ma=…): tạo mã + QR cho một đề, xem điểm theo bảng (vd "CĐCK 24A"),
 * xuất CSV. Bảng điểm này tách khỏi exam_results (em làm không cần tài khoản).
 */

interface LinkRow {
  id: number;
  code: string;
  exam_id: number;
  gradebook: string;
  is_open: boolean;
  exams: { title: string } | null;
}
interface SessionRow {
  id: string;
  link_id: number;
  exam_id: number;
  gradebook: string;
  full_name: string;
  student_code: string;
  class_name: string;
  score: number | null;
  correct_count: number | null;
  question_count: number | null;
  started_at: string;
  submitted_at: string | null;
  duration_seconds: number | null;
}

const link = (code: string) => `${SITE_URL}/thi/?ma=${code}`;
const fmtTime = (iso: string | null) => (iso ? new Date(iso).toLocaleString("vi-VN", { timeZone: "Asia/Ho_Chi_Minh" }) : "—");
const num = (n: number | null) => (n === null ? "—" : Number(n).toLocaleString("vi-VN"));

function randomCode(): string {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  const bytes = new Uint8Array(6);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (b) => chars[b % chars.length]).join("");
}

function Qr({ text }: { text: string }) {
  const { d, count } = useMemo(() => makeQrCode(text), [text]);
  const box = count + QUIET * 2;
  return (
    <div className="inline-block rounded-xl bg-white p-2">
      <svg viewBox={`${-QUIET} ${-QUIET} ${box} ${box}`} width={160} height={160} role="img" aria-label={`Mã QR ${text}`}>
        <rect x={-QUIET} y={-QUIET} width={box} height={box} fill="#fff" />
        <path d={d} fill="#000" />
      </svg>
    </div>
  );
}

function csvCell(v: string | number | null): string {
  const s = v === null ? "" : String(v);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

export default function GuestGradebook() {
  const [links, setLinks] = useState<LinkRow[]>([]);
  const [sessions, setSessions] = useState<SessionRow[]>([]);
  const [error, setError] = useState("");
  const [gradebook, setGradebook] = useState("");
  const [view, setView] = useState<"sv" | "luot">("sv");
  const [newExam, setNewExam] = useState("");
  const [newBook, setNewBook] = useState("CĐCK 24A");
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    const sb = getSupabase();
    const [l, s] = await Promise.all([
      sb.from("guest_exam_links").select("id, code, exam_id, gradebook, is_open, exams(title)").order("id", { ascending: false }),
      sb.from("guest_exam_sessions")
        .select("id, link_id, exam_id, gradebook, full_name, student_code, class_name, score, correct_count, question_count, started_at, submitted_at, duration_seconds")
        .order("started_at", { ascending: false })
        .limit(5000),
    ]);
    if (l.error || s.error) {
      setError((l.error ?? s.error)!.message);
      return;
    }
    setError("");
    setLinks((l.data ?? []) as unknown as LinkRow[]);
    setSessions((s.data ?? []) as SessionRow[]);
  }, []);
  useEffect(() => {
    void Promise.resolve().then(load);
  }, [load]);

  const books = useMemo(() => [...new Set([...links.map((x) => x.gradebook), ...sessions.map((x) => x.gradebook)])], [links, sessions]);
  const book = gradebook || books[0] || "";
  const rows = useMemo(() => sessions.filter((x) => x.gradebook === book), [sessions, book]);
  const done = useMemo(() => rows.filter((x) => x.submitted_at), [rows]);

  const perStudent = useMemo(() => {
    const m = new Map<string, { code: string; name: string; cls: string; n: number; last: SessionRow; best: number }>();
    for (const r of done) {
      const cur = m.get(r.student_code);
      const score = r.score ?? 0;
      if (!cur) m.set(r.student_code, { code: r.student_code, name: r.full_name, cls: r.class_name, n: 1, last: r, best: score });
      else {
        cur.n += 1;
        cur.best = Math.max(cur.best, score);
        if (r.submitted_at! > cur.last.submitted_at!) {
          cur.last = r;
          cur.name = r.full_name;
          cur.cls = r.class_name;
        }
      }
    }
    return [...m.values()].sort((a, b) => a.code.localeCompare(b.code));
  }, [done]);

  async function create() {
    const exam = Number(newExam);
    if (!exam || newBook.trim().length < 2) return;
    setBusy(true);
    const { error: e } = await getSupabase().from("guest_exam_links").insert({ code: randomCode(), exam_id: exam, gradebook: newBook.trim() });
    setBusy(false);
    if (e) setError(e.message);
    else {
      setNewExam("");
      void load();
    }
  }
  async function toggle(l: LinkRow) {
    const { error: e } = await getSupabase().from("guest_exam_links").update({ is_open: !l.is_open }).eq("id", l.id);
    if (e) setError(e.message);
    else void load();
  }
  function exportCsv() {
    const head = ["Bảng điểm", "MSSV", "Họ tên", "Lớp", "Đề", "Điểm", "Câu đúng", "Tổng câu", "Nộp lúc", "Thời gian làm (giây)"];
    const title = new Map(links.map((l) => [l.exam_id, l.exams?.title ?? `#${l.exam_id}`]));
    const lines = done.map((r) =>
      [r.gradebook, r.student_code, r.full_name, r.class_name, title.get(r.exam_id) ?? r.exam_id, r.score, r.correct_count, r.question_count, fmtTime(r.submitted_at), r.duration_seconds]
        .map(csvCell)
        .join(","),
    );
    const blob = new Blob(["﻿" + [head.map(csvCell).join(","), ...lines].join("\n")], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `bang-diem-${book.replace(/\s+/g, "-")}.csv`;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  const th = "px-3 py-2 text-left text-xs font-semibold uppercase text-muted";
  const td = "px-3 py-2 text-sm text-ink";
  return (
    <div className="mx-auto max-w-5xl space-y-8 p-4">
      <h1 className="text-xl font-bold text-ink">Đề làm bằng mã &amp; bảng điểm</h1>
      {error && <p role="alert" className="text-sm text-danger">{error}</p>}

      <section className="space-y-3">
        <h2 className="font-semibold text-ink">Tạo mã cho một đề</h2>
        <div className="flex flex-wrap items-end gap-3">
          <label className="text-sm text-muted">
            Mã đề trong hệ thống (số)
            <input className="mt-1 block min-h-11 w-40 rounded-xl border border-line-strong bg-surface px-3 text-ink" value={newExam} onChange={(e) => setNewExam(e.target.value.replace(/\D/g, ""))} inputMode="numeric" />
          </label>
          <label className="text-sm text-muted">
            Ghi điểm vào bảng
            <input className="mt-1 block min-h-11 w-48 rounded-xl border border-line-strong bg-surface px-3 text-ink" value={newBook} onChange={(e) => setNewBook(e.target.value)} />
          </label>
          <Button disabled={busy || !newExam} onClick={() => void create()}>Tạo mã</Button>
        </div>
        <ul className="space-y-3">
          {links.map((l) => (
            <li key={l.id} className="flex flex-wrap items-center gap-4 rounded-xl border border-line p-3">
              <Qr text={link(l.code)} />
              <div className="min-w-0 flex-1 text-sm">
                <p className="font-semibold text-ink">{l.exams?.title ?? `Đề #${l.exam_id}`}</p>
                <p className="text-muted">Bảng điểm: {l.gradebook} · Mã: <span className="font-mono text-ink">{l.code}</span> · {l.is_open ? "đang mở" : "đã đóng"}</p>
                <p className="break-all text-muted">{link(l.code)}</p>
              </div>
              <Button size="sm" variant="outline" onClick={() => void toggle(l)}>{l.is_open ? "Đóng mã" : "Mở lại"}</Button>
            </li>
          ))}
          {links.length === 0 && <li className="text-sm text-muted">Chưa có mã nào.</li>}
        </ul>
      </section>

      <section className="space-y-3">
        <div className="flex flex-wrap items-center gap-3">
          <h2 className="font-semibold text-ink">Bảng điểm</h2>
          <select className="min-h-11 rounded-xl border border-line-strong bg-surface px-3 text-ink" value={book} onChange={(e) => setGradebook(e.target.value)}>
            {books.map((b) => <option key={b}>{b}</option>)}
          </select>
          <Button size="sm" variant={view === "sv" ? "primary" : "outline"} onClick={() => setView("sv")}>Theo sinh viên</Button>
          <Button size="sm" variant={view === "luot" ? "primary" : "outline"} onClick={() => setView("luot")}>Từng lượt</Button>
          <Button size="sm" variant="outline" onClick={exportCsv} disabled={done.length === 0}><Download size={14} /> Xuất CSV</Button>
          <span className="text-sm text-muted">{perStudent.length} sinh viên · {done.length} lượt đã nộp · {rows.length - done.length} lượt chưa nộp</span>
        </div>
        <div className="overflow-x-auto rounded-xl border border-line">
          {view === "sv" ? (
            <table className="w-full min-w-[640px]">
              <thead className="bg-surface-2"><tr><th className={th}>MSSV</th><th className={th}>Họ tên</th><th className={th}>Lớp</th><th className={th}>Số lượt</th><th className={th}>Gần nhất</th><th className={th}>Cao nhất</th></tr></thead>
              <tbody>
                {perStudent.map((s) => (
                  <tr key={s.code} className="border-t border-line">
                    <td className={`${td} font-mono`}>{s.code}</td><td className={td}>{s.name}</td><td className={td}>{s.cls}</td>
                    <td className={td}>{s.n}</td><td className={td}>{num(s.last.score)}</td><td className={`${td} font-semibold`}>{num(s.best)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <table className="w-full min-w-[760px]">
              <thead className="bg-surface-2"><tr><th className={th}>MSSV</th><th className={th}>Họ tên</th><th className={th}>Lớp</th><th className={th}>Điểm</th><th className={th}>Đúng</th><th className={th}>Nộp lúc</th><th className={th}>Thời gian</th></tr></thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.id} className="border-t border-line">
                    <td className={`${td} font-mono`}>{r.student_code}</td><td className={td}>{r.full_name}</td><td className={td}>{r.class_name}</td>
                    <td className={`${td} font-semibold`}>{r.submitted_at ? num(r.score) : "chưa nộp"}</td>
                    <td className={td}>{r.submitted_at ? `${r.correct_count}/${r.question_count}` : "—"}</td>
                    <td className={td}>{fmtTime(r.submitted_at ?? r.started_at)}</td>
                    <td className={td}>{r.duration_seconds === null ? "—" : `${Math.floor(r.duration_seconds / 60)}ph ${r.duration_seconds % 60}s`}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
        <p className="text-xs text-muted">MSSV do sinh viên tự nhập nên chưa được xác thực: nên đối chiếu với danh sách lớp khi chốt điểm.</p>
      </section>
    </div>
  );
}
