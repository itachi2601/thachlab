"use client";

import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/components/auth/AuthProvider";
import { getSupabase } from "@/services/supabase";

interface Student {
  id: string;
  full_name: string;
  class_name: string;
}

interface SentMessage {
  id: number;
  created_at: string;
  subject: string;
  body: string;
  recipient_id: string | null;
  class_name: string | null;
  profiles: { full_name: string } | null;
}

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-[#3B82F6] focus:outline-none";

export default function MessagesAdmin() {
  const { session } = useAuth();
  const [students, setStudents] = useState<Student[]>([]);
  const [sent, setSent] = useState<SentMessage[]>([]);
  const [target, setTarget] = useState<string>("all"); // all | class:<name> | student:<id>
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [okMsg, setOkMsg] = useState("");

  const reload = useCallback(() => {
    getSupabase()
      .from("messages")
      .select(
        "id, created_at, subject, body, recipient_id, class_name, profiles!messages_recipient_id_fkey(full_name)",
      )
      .order("created_at", { ascending: false })
      .limit(50)
      .then(({ data }) => setSent((data as unknown as SentMessage[]) ?? []));
  }, []);

  useEffect(() => {
    getSupabase()
      .from("profiles")
      .select("id, full_name, class_name")
      .eq("role", "student")
      .order("class_name")
      .order("full_name")
      .then(({ data }) => setStudents((data as Student[]) ?? []));
    reload();
  }, [reload]);

  const classes = [...new Set(students.map((s) => s.class_name))].filter(
    Boolean,
  );

  async function send(e: React.FormEvent) {
    e.preventDefault();
    if (!session) return;
    setBusy(true);
    setError("");
    setOkMsg("");
    const payload: Record<string, unknown> = {
      sender_id: session.user.id,
      subject: subject.trim(),
      body: body.trim(),
      recipient_id: null,
      class_name: null,
    };
    if (target.startsWith("class:")) payload.class_name = target.slice(6);
    if (target.startsWith("student:")) payload.recipient_id = target.slice(8);
    const { error } = await getSupabase().from("messages").insert(payload);
    setBusy(false);
    if (error) {
      setError(error.message);
      return;
    }
    setSubject("");
    setBody("");
    setOkMsg("✓ Đã gửi tin nhắn.");
    reload();
  }

  return (
    <div className="space-y-8">
      <form
        onSubmit={send}
        className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-6"
      >
        <h2 className="font-display text-lg font-semibold text-white">
          Gửi tin nhắn
        </h2>
        <select
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          className="w-full rounded-xl border border-white/10 bg-[#0B1020] px-4 py-2.5 text-white focus:border-[#3B82F6] focus:outline-none"
        >
          <option value="all">📢 Toàn bộ học sinh</option>
          {classes.map((c) => (
            <option key={c} value={`class:${c}`}>
              🏫 Lớp {c}
            </option>
          ))}
          {students.map((s) => (
            <option key={s.id} value={`student:${s.id}`}>
              👤 {s.full_name} ({s.class_name})
            </option>
          ))}
        </select>
        <input
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          placeholder="Tiêu đề"
          className={inputCls}
        />
        <textarea
          required
          value={body}
          onChange={(e) => setBody(e.target.value)}
          placeholder="Nội dung tin nhắn"
          rows={4}
          className={inputCls}
        />
        {error && <p className="text-sm text-red-400">{error}</p>}
        {okMsg && <p className="text-sm text-emerald-400">{okMsg}</p>}
        <button
          type="submit"
          disabled={busy}
          className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#1D4ED8] disabled:opacity-50"
        >
          {busy ? "Đang gửi…" : "Gửi"}
        </button>
      </form>

      <div className="space-y-3">
        <h3 className="font-display text-lg font-semibold text-white">
          Đã gửi gần đây
        </h3>
        {sent.map((m) => (
          <div
            key={m.id}
            className="rounded-2xl border border-white/10 bg-[#0B1020] px-5 py-4"
          >
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <p className="font-medium text-white">
                {m.subject || "(Không tiêu đề)"}
              </p>
              <span className="text-xs text-slate-500">
                {new Date(m.created_at).toLocaleString("vi-VN")} →{" "}
                {m.recipient_id
                  ? (m.profiles?.full_name ?? "1 học sinh")
                  : m.class_name
                    ? `Lớp ${m.class_name}`
                    : "Tất cả"}
              </span>
            </div>
            <p className="mt-1 line-clamp-2 text-sm text-slate-400">{m.body}</p>
          </div>
        ))}
        {sent.length === 0 && (
          <p className="text-sm text-slate-400">Chưa gửi tin nhắn nào.</p>
        )}
      </div>
    </div>
  );
}
