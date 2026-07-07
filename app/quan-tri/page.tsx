"use client";

import { useState } from "react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import PostsAdmin from "@/components/admin/PostsAdmin";
import ExamsAdmin from "@/components/admin/ExamsAdmin";
import ImportWord from "@/components/admin/ImportWord";
import ClassesAdmin from "@/components/admin/ClassesAdmin";
import ResultsAdmin from "@/components/admin/ResultsAdmin";
import MessagesAdmin from "@/components/admin/MessagesAdmin";

const TABS = [
  { id: "exams", label: "Đề kiểm tra" },
  { id: "import", label: "Import từ Word" },
  { id: "classes", label: "Lớp học" },
  { id: "results", label: "Bảng điểm" },
  { id: "posts", label: "Bài đăng" },
  { id: "messages", label: "Tin nhắn" },
] as const;

type TabId = (typeof TABS)[number]["id"];

export default function AdminPage() {
  const [tab, setTab] = useState<TabId>("exams");

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-5xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          Quản <span className="text-gradient">trị</span>
        </h1>
        <RequireAuth adminOnly>
          <div className="mt-8 flex flex-wrap gap-2">
            {TABS.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`rounded-full px-4 py-2 text-sm font-semibold transition-colors ${
                  tab === t.id
                    ? "bg-[#2563EB] text-white"
                    : "bg-white/5 text-slate-300 hover:bg-white/10"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
          <div className="mt-8">
            {tab === "exams" && <ExamsAdmin />}
            {tab === "import" && <ImportWord />}
            {tab === "classes" && <ClassesAdmin />}
            {tab === "results" && <ResultsAdmin />}
            {tab === "posts" && <PostsAdmin />}
            {tab === "messages" && <MessagesAdmin />}
          </div>
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
