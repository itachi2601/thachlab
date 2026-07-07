"use client";

import { useEffect, useState } from "react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import { getSupabase } from "@/services/supabase";

interface Message {
  id: number;
  created_at: string;
  subject: string;
  body: string;
  recipient_id: string | null;
  class_name: string | null;
}

function Inbox() {
  const { session } = useAuth();
  const [messages, setMessages] = useState<Message[] | null>(null);

  useEffect(() => {
    if (!session) return;
    getSupabase()
      .from("messages")
      .select("id, created_at, subject, body, recipient_id, class_name")
      .order("created_at", { ascending: false })
      .limit(100)
      .then(({ data }) => setMessages((data as Message[]) ?? []));
  }, [session]);

  if (!messages) return <p className="text-slate-400">Đang tải…</p>;
  if (messages.length === 0)
    return <p className="text-slate-400">Chưa có tin nhắn nào.</p>;

  return (
    <div className="space-y-4">
      {messages.map((m) => (
        <article
          key={m.id}
          className="rounded-2xl border border-white/10 bg-[#0B1020] p-5"
        >
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h2 className="font-semibold text-white">
              {m.subject || "(Không có tiêu đề)"}
            </h2>
            <span className="text-xs text-slate-500">
              {new Date(m.created_at).toLocaleString("vi-VN")} ·{" "}
              {m.recipient_id
                ? "Gửi riêng cho em"
                : m.class_name
                  ? `Lớp ${m.class_name}`
                  : "Toàn trường"}
            </span>
          </div>
          <p className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-slate-300">
            {m.body}
          </p>
        </article>
      ))}
    </div>
  );
}

export default function MessagesPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-3xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          Tin <span className="text-gradient">nhắn</span>
        </h1>
        <p className="mt-3 mb-10 text-slate-400">
          Thông báo từ thầy — gửi riêng cho em, cho lớp hoặc toàn trường.
        </p>
        <RequireAuth>
          <Inbox />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
