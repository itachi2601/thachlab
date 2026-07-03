import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import Hero from "@/components/home/Hero";
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
        <Hero />
        <Features />
        <PhysicsEverywhere />
        <LearningPath />
        <AboutFounder />
        <Testimonials />
      </main>
      <Footer />
    </>
  );
}
