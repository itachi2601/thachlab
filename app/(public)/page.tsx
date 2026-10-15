import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import OpenClasses from "@/components/home/OpenClasses";
import ContentSearch from "@/components/home/ContentSearch";
import ForParents from "@/components/home/ForParents";
import { readHomeStats } from "@/components/home/home-stats.server";
import { PhysicsSimulationHero } from "@/components/home/PhysicsSimulationHero";
import { PhysicsPostRibbon } from "@/components/home/PhysicsPostRibbon";
import LearningPath from "@/components/home/LearningPath";
import HonorBoard from "@/components/home/HonorBoard";
import PwaInstallCard from "@/components/pwa/PwaInstallCard";
import { getPhysicsAroundPosts } from "@/lib/blog";
import { rotatePhysicsAround, vietnamDayIndex } from "@/lib/physics-around";
import HomeScreen from "@/components/home/HomeScreen";
import AdminHomeToday from "@/components/home/AdminHomeToday";

const PINNED_AROUND_SLUG = "vi-sao-van-dong-vien-xoay-nhanh-hon-khi-thu-tay";

export default function Home() {
  // Số chương/bài/mục đọc từ file tĩnh lúc build (xem home-stats.server.ts) — không gọi Supabase khi tải.
  const stats = readHomeStats();
  // Dải bài "Vật lý quanh ta" ngay dưới hero (không đè H1 — B2): xoay theo ngày. Trang chủ còn 6 khối; giới thiệu/cách học/lời nhắn ở /gioi-thieu (K1).
  const around = getPhysicsAroundPosts();
  // Thẻ của thầy (ảnh trượt băng) luôn đứng đầu dải; các thẻ còn lại xoay theo ngày.
  const pinned = around.find((post) => post.slug === PINNED_AROUND_SLUG);
  const rest = around.filter((post) => post !== pinned);
  const rotating = rest.length > 0 ? rotatePhysicsAround(rest, vietnamDayIndex() % rest.length, 4) : null;
  const ribbonPosts = rotating ? [...(pinned ? [pinned] : [rotating.featured]), ...(pinned ? [rotating.featured] : []), ...rotating.others].slice(0, 5) : pinned ? [pinned] : [];
  return (
    <>
      <Navbar />
      <main>
        <AdminHomeToday />
        {/* Máy tính: mỗi khối một màn (HomeScreen). Điện thoại giữ dòng chảy cũ. */}
        <HomeScreen first>
          <PhysicsSimulationHero />
          {ribbonPosts.length > 0 && (
            <a
              href="#vat-ly-quanh-ta"
              className="mx-auto mb-4 hidden min-h-11 items-center gap-1 text-sm font-medium text-muted hover:text-primary lg:inline-flex"
            >
              Vật lý quanh ta <span aria-hidden>↓</span>
            </a>
          )}
        </HomeScreen>
        {ribbonPosts.length > 0 && (
          <HomeScreen id="vat-ly-quanh-ta">
            <div className="bg-bg px-6 pt-4 lg:px-12 lg:py-8">
              <div className="mx-auto max-w-6xl">
                <PhysicsPostRibbon posts={ribbonPosts} label="Vật lý quanh ta" total={around.length} />
              </div>
            </div>
          </HomeScreen>
        )}
        {/* Thẻ cài app: điện thoại giữ chỗ cũ; máy tính dời xuống cuối trang để không chen giữa hai màn. */}
        <div className="bg-bg px-6 pt-4 lg:hidden">
          <PwaInstallCard guideFallback />
        </div>
        <HomeScreen>
          <OpenClasses stats={stats} />
          <ContentSearch />
        </HomeScreen>
        <HomeScreen className="bg-panel">
          <ForParents courses={stats?.courses ?? null} />
        </HomeScreen>
        <LearningPath />
        <HonorBoard />
        <div className="hidden bg-bg px-12 pb-8 lg:block">
          <div className="mx-auto max-w-6xl">
            <PwaInstallCard guideFallback />
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
