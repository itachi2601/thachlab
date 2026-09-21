import Link from "next/link";
import { ChevronRight, FileQuestion, FileText, GraduationCap, MonitorPlay, ShieldCheck, Video } from "lucide-react";
import { CNC_COURSE_ITEMS } from "@/services/cnc-lms";

const learningItems = CNC_COURSE_ITEMS.filter((item) => item.id !== "intro");

export default function CncLmsLessonIndex() {
  return (
    <div className="admin-stack" style={{ gap: 24 }}>
      <header>
        <p className="admin-eyebrow">Trung tâm nội dung CNC</p>
        <p className="admin-lead max-w-2xl">
          Mỗi bài học có một trang soạn riêng. Chọn bài bên dưới để quản lý nội dung, video, học liệu, bài nộp và ngân
          hàng câu hỏi.
        </p>
      </header>

      <section className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_272px] lg:items-start">
        <div className="admin-stack" style={{ gap: 8 }}>
          <div className="flex items-end justify-between gap-4">
            <h2 className="admin-h2">Danh sách bài học</h2>
            <span className="admin-muted">{learningItems.length} bài · 70 tiết</span>
          </div>
          {learningItems.map((item, index) => (
            <Link key={item.id} href={`/quan-tri/lms-cnc/${item.id}`} className="admin-action group">
              <span className="admin-action-icon" style={{ width: 42, height: 42, fontWeight: 800 }}>
                {String(index + 1).padStart(2, "0")}
              </span>
              <span className="min-w-0 flex-1">
                <b>{item.title.replace(/^Bài \d+: /, "")}</b>
                <span>
                  Bài {index + 1} · {item.duration}
                </span>
                <span className="mt-2 flex flex-wrap gap-x-4 gap-y-1">
                  <span className="inline-flex items-center gap-1">
                    <GraduationCap size={13} /> Chuẩn đầu ra
                  </span>
                  <span className="inline-flex items-center gap-1">
                    <Video size={13} /> Video
                  </span>
                  <span className="inline-flex items-center gap-1">
                    <FileText size={13} /> Học liệu
                  </span>
                  <span className="inline-flex items-center gap-1">
                    <FileQuestion size={13} /> Kiểm tra
                  </span>
                </span>
              </span>
              <ChevronRight size={17} className="mt-1 shrink-0 opacity-50 transition-transform group-hover:translate-x-0.5" />
            </Link>
          ))}
        </div>

        <aside className="admin-stack lg:sticky lg:top-24">
          <Link href="/quan-tri/lms-cnc/intro" className="admin-action" style={{ flexDirection: "column" }}>
            <span className="admin-action-icon">
              <MonitorPlay size={18} />
            </span>
            <span>
              <b>Trang giới thiệu học phần</b>
              <span>Chỉnh mô tả chung, tài nguyên nhập môn và hoạt động mở đầu.</span>
            </span>
          </Link>
          <div className="admin-card">
            <p className="admin-h3 flex items-center gap-2">
              <ShieldCheck size={16} /> Luồng mở khóa
            </p>
            <ol className="admin-muted mt-3 space-y-2.5 leading-5">
              <li>
                <b>1.</b> Bài 2 và 3 đạt từ 80%
              </li>
              <li>
                <b>2.</b> Mở bài vận hành tiện/phay
              </li>
              <li>
                <b>3.</b> Đạt vận hành để mở bài gia công
              </li>
            </ol>
          </div>
        </aside>
      </section>
    </div>
  );
}
