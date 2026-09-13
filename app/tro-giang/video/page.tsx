"use client";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import NotRegistered from "@/components/tro-giang/NotRegistered";
import TaDemoBanner from "@/components/tro-giang/TaDemoBanner";
import TroGiangVideo from "@/components/tro-giang/TroGiangVideo";
import { useAssistantOrDemo } from "@/lib/tro-giang/useAssistant";

function VideoLoader() {
  const { assistant, demo } = useAssistantOrDemo();

  if (assistant === undefined) return <p className="text-slate-400">Đang tải…</p>;
  if (assistant === null) return <NotRegistered />;
  return (
    <>
      <TroGiangVideo assistant={assistant} />
      {demo && <TaDemoBanner />}
    </>
  );
}

export default function TroGiangVideoPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-lg px-5 pt-28 pb-16">
        <RequireAuth>
          <VideoLoader />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
