import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import OpenClasses from "@/components/home/OpenClasses";
import ContentSearch from "@/components/home/ContentSearch";
import ForParents from "@/components/home/ForParents";
import { readHomeStats } from "@/components/home/home-stats.server";
import { PhysicsSimulationHero } from "@/components/home/PhysicsSimulationHero";
import Features from "@/components/home/Features";
import ExamSamples from "@/components/home/ExamSamples";
import PhysicsEverywhere from "@/components/home/PhysicsEverywhere";
import LearningPath from "@/components/home/LearningPath";
import HonorBoard from "@/components/home/HonorBoard";
import AboutFounder from "@/components/home/AboutFounder";
import PwaInstallCard from "@/components/pwa/PwaInstallCard";
import Testimonials from "@/components/home/Testimonials";

export default function Home() {
  // Số chương/bài/mục đọc từ file tĩnh lúc build (xem home-stats.server.ts) — không gọi Supabase khi tải.
  const stats = readHomeStats();
  return (
    <>
      <Navbar />
      <main>
        <PhysicsSimulationHero />
        <div className="bg-[#05070B] px-6 pt-4 lg:px-12">
          <div className="mx-auto max-w-6xl">
            <PwaInstallCard guideFallback />
          </div>
        </div>
        <OpenClasses stats={stats} />
        <ContentSearch />
        <ForParents courses={stats?.courses ?? null} />
        <Features />
        <ExamSamples />
        <PhysicsEverywhere />
        <LearningPath />
        <HonorBoard />
        <AboutFounder />
        <Testimonials />
      </main>
      <Footer />
    </>
  );
}
