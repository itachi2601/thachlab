import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { PhysicsSimulationHero } from "@/components/home/PhysicsSimulationHero";
import Features from "@/components/home/Features";
import PhysicsEverywhere from "@/components/home/PhysicsEverywhere";
import LearningPath from "@/components/home/LearningPath";
import AboutFounder from "@/components/home/AboutFounder";
import Testimonials from "@/components/home/Testimonials";

export default function Home() {
  return (
    <>
      <Navbar />
      <main>
        <PhysicsSimulationHero />
        <PhysicsEverywhere />
        <LearningPath />
        <Features />
        <AboutFounder />
        <Testimonials />
      </main>
      <Footer />
    </>
  );
}
