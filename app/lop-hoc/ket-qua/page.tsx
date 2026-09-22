"use client";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import StudentResultsDashboard from "@/components/results/StudentResultsDashboard";
import { supabaseConfigured } from "@/services/supabase";

function Dashboard() {
  const { session } = useAuth();
  if (!session) return null;
  return (
    <div className="px-6 pb-20 pt-28">
      <StudentResultsDashboard studentId={session.user.id} viewer="student" />
    </div>
  );
}

export default function KetQuaPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full">
        {!supabaseConfigured ? (
          <p className="pt-28 text-center text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : (
          <RequireAuth>
            <Dashboard />
          </RequireAuth>
        )}
      </main>
      <Footer />
    </>
  );
}
