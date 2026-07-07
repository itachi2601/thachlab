"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import { getSupabase } from "@/services/supabase";

interface ResultRow {
  id: number;
  created_at: string;
  score: number;
  duration_seconds: number;
  exams: { title: string } | null;
}

function Account() {
  const router = useRouter();
  const { session, profile, signOut } = useAuth();
  const [results, setResults] = useState<ResultRow[] | null>(null);

  useEffect(() => {
    if (!session) return;
    getSupabase()
      .from("exam_results")
      .select("id, created_at, score, duration_seconds, exams(title)")
      .eq("student_id", session.user.id)
      .order("created_at", { ascending: false })
      .limit(50)
      .then(({ data }) => setResults((data as unknown as ResultRow[]) ?? []));
  }, [session]);

  return (
    <div className="space-y-8">
      <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="font-display text-xl font-semibold text-white">
              {profile?.full_name}
            </p>
            <p className="mt-1 text-sm text-slate-400">
              {profile?.class_name && `Lớp ${profile.class_name} · `}
              {session?.user.email}
              {profile?.role === "admin" && " · Quản trị viên"}
            </p>
          </div>
          <button
            onClick={async () => {
              await signOut();
              router.push("/");
            }}
            className="rounded-full border border-white/15 px-4 py-2 text-sm font-medium text-slate-300 hover:border-white/30 hover:text-white"
          >
            Đăng xuất
          </button>
        </div>
      </div>

      <div>
        <h2 className="mb-4 font-display text-xl font-semibold text-white">
          Lịch sử điểm
        </h2>
        {!results ? (
          <p className="text-slate-400">Đang tải…</p>
        ) : results.length === 0 ? (
          <p className="text-slate-400">Em chưa làm bài kiểm tra nào.</p>
        ) : (
          <div className="overflow-x-auto rounded-2xl border border-white/10">
            <table className="w-full min-w-105 text-left text-sm">
              <thead className="bg-white/5 text-slate-400">
                <tr>
                  <th className="px-4 py-3 font-medium">Đề</th>
                  <th className="px-4 py-3 font-medium">Ngày làm</th>
                  <th className="px-4 py-3 text-right font-medium">Điểm</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-slate-300">
                {results.map((row) => (
                  <tr key={row.id}>
                    <td className="px-4 py-3">
                      {row.exams?.title ?? "(Đề đã xóa)"}
                    </td>
                    <td className="px-4 py-3 text-slate-400">
                      {new Date(row.created_at).toLocaleString("vi-VN")}
                    </td>
                    <td className="px-4 py-3 text-right font-mono font-semibold text-white">
                      {Number(row.score).toLocaleString("vi-VN")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default function AccountPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-3xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="mb-10 font-display text-3xl font-bold text-white sm:text-4xl">
          Tài <span className="text-gradient">khoản</span>
        </h1>
        <RequireAuth>
          <Account />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
