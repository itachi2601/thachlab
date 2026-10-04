import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import OpenClasses from "@/components/home/OpenClasses";
import TeachingSchedule from "@/components/home/TeachingSchedule";
import { readTeachingSchedule } from "@/components/home/teaching-schedule.server";
import ForParents from "@/components/home/ForParents";
import { readHomeStats } from "@/components/home/home-stats.server";
import { PhysicsSimulationHero } from "@/components/home/PhysicsSimulationHero";
import Features from "@/components/home/Features";
import PhysicsEverywhere from "@/components/home/PhysicsEverywhere";
import LearningPath from "@/components/home/LearningPath";
import HonorBoard from "@/components/home/HonorBoard";
import AboutFounder from "@/components/home/AboutFounder";
import Testimonials from "@/components/home/Testimonials";

export default function Home() {
  // Số chương/bài/mục đọc từ file tĩnh lúc build (xem home-stats.server.ts) — không gọi Supabase khi tải.
  const stats = readHomeStats();
  const schedule = readTeachingSchedule();
  return (
    <>
      <Navbar />
      <main>
        <OpenClasses stats={stats} />
        <TeachingSchedule courses={schedule} />
        <ForParents />
        <PhysicsSimulationHero />
        <Features />
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
