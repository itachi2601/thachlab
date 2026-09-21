import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, BookOpen, Cog, Factory, Sigma, Wrench, type LucideIcon } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";

export const metadata: Metadata = {
  title: "CTTC — Không gian học tập",
  description: "Gia công CNC, Tiện – Phay truyền thống và các học phần cơ khí dành cho sinh viên CTTC.",
};

type Course = { title: string; description: string; href?: string; icon: LucideIcon };

// Luồng CTTC tách riêng khỏi THPT: chỉ liệt kê học phần của trường, màu nhấn cam như thẻ "Sinh viên CTTC" ở trang chủ.
const COURSES: Course[] = [
  {
    title: "Gia công CNC",
    description: "Quy trình, thông số cắt, lập trình và vận hành gia công CNC.",
    href: "/lop-hoc/cnc",
    icon: Cog,
  },
  {
    title: "Tiện – Phay truyền thống",
    description: "Điểm danh, chọn máy và theo dõi 5S khi thực hành tại Xưởng C1.1.",
    href: "/lop-hoc/tien-phay",
    icon: Wrench,
  },
  {
    title: "Vật lý đại cương",
    description: "Nền tảng cơ học, nhiệt, điện từ và các mô hình vật lý ứng dụng.",
    icon: Sigma,
  },
  {
    title: "Công nghệ chế tạo máy",
    description: "Kiến thức về phôi, dụng cụ, nguyên công và tổ chức sản xuất cơ khí.",
    icon: Factory,
  },
  {
    title: "Anh văn chuyên ngành cơ khí",
    description: "Từ vựng, đọc hiểu tài liệu kỹ thuật và giao tiếp trong ngành cơ khí.",
    icon: BookOpen,
  },
];

export default function CttcHubPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full pt-[76px]">
        <div className="lesson-shell lesson-shell--cttc">
          <div className="lesson-main lesson-main--single">
            <header className="lesson-head">
              <p className="lesson-eyebrow">Sinh viên CTTC</p>
              <h1>
                Chọn học phần để <span className="text-gradient--warm">vào xưởng.</span>
              </h1>
              <p className="lesson-lead">
                Gia công CNC, Tiện – Phay truyền thống và các học phần cơ khí. Đăng nhập bằng tài khoản
                sinh viên để điểm danh, làm bài và theo dõi tiến độ.
              </p>
            </header>
            <div className="hub-grid">
              {COURSES.map((course) => {
                const Icon = course.icon;
                const body = (
                  <>
                    <span className="hub-tile">
                      <Icon size={22} />
                    </span>
                    <span className="hub-card-body">
                      <span className="hub-card-title">
                        {course.title}
                        {!course.href && <span className="hub-tag">Sắp mở</span>}
                      </span>
                      <span className="hub-card-desc">{course.description}</span>
                    </span>
                    <ArrowRight size={18} />
                  </>
                );
                return course.href ? (
                  <Link key={course.title} href={course.href} className="hub-card">
                    {body}
                  </Link>
                ) : (
                  <div key={course.title} className="hub-card is-soon" aria-disabled>
                    {body}
                  </div>
                );
              })}
            </div>
            <p className="hub-switch">
              Bạn là học sinh THPT · THCS?
              <Link href="/lop-hoc" className="lesson-link">
                Sang không gian THPT <ArrowRight size={14} />
              </Link>
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
