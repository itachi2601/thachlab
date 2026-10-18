"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowRight, Bug, BookOpen, ClipboardList, Cpu, Database, GraduationCap, UserCheck, Wrench } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { AREA_ENTRY, AREA_ITEMS, SHARED_ITEMS, type AdminNavItem } from "@/components/admin/nav";
import { getSupabase, supabaseConfigured } from "@/services/supabase";
import { fetchAdminTodayBoard } from "@/services/admin-today";

type Counts = {
  lessons: number | null;
  exams: number | null;
  questions: number | null;
  students: number | null;
  results7d: number | null;
  brokenMachines: number | null;
};

const EMPTY_COUNTS: Counts = {
  lessons: null,
  exams: null,
  questions: null,
  students: null,
  results7d: null,
  brokenMachines: null,
};

// Các lối tắt hay dùng nhất, gom từ danh sách điều hướng để không phải khai báo hai lần.
const QUICK_HREFS = [
  "/quan-tri/dang-de",
  "/quan-tri/sua-de",
  "/quan-tri/bai-hoc",
  "/quan-tri/cnc-bai-hoc",
  "/quan-tri/tinh-trang-may",
  "/quan-tri/tin-nhan",
];

const ALL_NAV: AdminNavItem[] = [...AREA_ITEMS.thpt, ...AREA_ITEMS.cttc, ...SHARED_ITEMS];

export default function AdminOverviewPage() {
  const { profile, loading } = useAuth();
  const router = useRouter();
  const [counts, setCounts] = useState<Counts>(EMPTY_COUNTS);
  const [todo, setTodo] = useState<Awaited<ReturnType<typeof fetchAdminTodayBoard>> | null>(null);
  const restrictedArea = profile?.role === "instructor" ? profile.admin_area : null;

  // Giảng viên chỉ được phân công 1 khu vực thì vào thẳng khu đó, không thấy trang tổng quan.
  useEffect(() => {
    if (loading || !restrictedArea) return;
    router.replace(AREA_ENTRY[restrictedArea]);
  }, [loading, restrictedArea, router]);

  useEffect(() => {
    if (!supabaseConfigured || loading || restrictedArea) return;
    const since = new Date(Date.now() - 7 * 24 * 3600 * 1000).toISOString();
    const sb = getSupabase();
    // head + count: chỉ lấy số dòng, không kéo dữ liệu về.
    const head = { count: "exact" as const, head: true };
    let alive = true;
    Promise.all([
      sb.from("lessons").select("*", head),
      sb.from("exams").select("*", head),
      sb.from("question_bank").select("*", head),
      sb.from("profiles").select("*", head).eq("role", "student"),
      sb.from("exam_results").select("*", head).gte("created_at", since),
      sb.from("machines").select("*", head).eq("status", "broken"),
    ])
      .then((rows) => {
        if (!alive) return;
        const [lessons, exams, questions, students, results7d, brokenMachines] = rows.map((row) =>
          row.error ? null : row.count ?? 0,
        );
        setCounts({ lessons, exams, questions, students, results7d, brokenMachines });
      })
      .catch(() => undefined);
    fetchAdminTodayBoard()
      .then((board) => alive && setTodo(board))
      .catch(() => undefined);
    return () => {
      alive = false;
    };
  }, [loading, restrictedArea]);

  if (loading || restrictedArea) {
    return <p className="admin-muted">Đang chuyển hướng…</p>;
  }

  const quickItems = QUICK_HREFS.map((href) => ALL_NAV.find((item) => item.href === href)).filter(
    (item): item is AdminNavItem => !!item,
  );

  return (
    <div className="admin-stack" style={{ gap: 28 }}>
      <section>
        <p className="admin-eyebrow">Tổng quan</p>
        <h2 className="mt-1 text-xl font-bold">Chào {profile?.full_name?.split(" ").slice(-1)[0] ?? "thầy"} 👋</h2>
        <p className="admin-lead">Số liệu nhanh của hệ thống và các việc hay làm nhất.</p>
      </section>

      <section>
        <h3 className="admin-h2">Cần xử lý</h3>
        <div className="admin-grid mt-3" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))" }}>
          <Stat icon={Bug} label="Báo lỗi mới" value={todo?.newBugs ?? null} href="/quan-tri/bao-loi" tone="warn" />
          <Stat icon={UserCheck} label="Em chờ duyệt vào lớp" value={todo?.pendingJoins ?? null} href="/quan-tri/hoc-sinh?tab=pending" tone="warn" />
          <Stat icon={ClipboardList} label="Đăng ký khoá chờ duyệt" value={todo?.pendingEnrollments ?? null} href="/dashboard-thpt?tab=enrollment" tone="warn" />
          <Stat icon={UserCheck} label="Phiếu trợ giảng chờ duyệt" value={todo?.pendingTaSessions ?? null} href="/quan-tri/tro-giang" tone="warn" />
          <Stat icon={GraduationCap} label="Mục phụ đạo đang mở" value={todo?.openTutoring ?? null} href="/dashboard-thpt?tab=alerts" tone="warn" />
          <Stat icon={Wrench} label="Máy đang hư" value={counts.brokenMachines} href="/quan-tri/tinh-trang-may" tone="warn" />
        </div>
      </section>

      <section className="admin-grid" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(165px, 1fr))" }}>
        <Stat icon={BookOpen} label="Bài học" value={counts.lessons} href="/quan-tri/bai-hoc" />
        <Stat icon={ClipboardList} label="Đề kiểm tra" value={counts.exams} href="/quan-tri/sua-de" />
        <Stat icon={Database} label="Câu hỏi trong ngân hàng" value={counts.questions} href="/quan-tri/ngan-hang-cau-hoi" />
        <Stat icon={GraduationCap} label="Học sinh" value={counts.students} href="/quan-tri/hoc-sinh" />
        <Stat icon={ClipboardList} label="Bài nộp 7 ngày qua" value={counts.results7d} />
      </section>

      <section>
        <h3 className="admin-h2">Việc hay làm</h3>
        <div className="admin-grid mt-3">
          {quickItems.map((item) => {
            const Icon = item.icon;
            const cttc = AREA_ITEMS.cttc.some((c) => c.href === item.href);
            return (
              <Link key={item.href} href={item.href} className={`admin-action ${cttc ? "admin-action--cttc" : ""}`}>
                <span className="admin-action-icon">
                  <Icon size={18} />
                </span>
                <span className="min-w-0">
                  <b>
                    {item.label}
                    {/* Hai khu vực đều có mục "Bài học"/"Đăng đề" — gắn nhãn để khỏi bấm nhầm. */}
                    <em className="ml-1.5 inline-block rounded-full bg-black/5 px-2 py-0.5 align-middle text-[11px] font-semibold not-italic text-[color:var(--a-faint)]">
                      {cttc ? "CTTC" : "THPT – THCS"}
                    </em>
                  </b>
                  <span>{item.desc}</span>
                </span>
              </Link>
            );
          })}
        </div>
      </section>

      <section>
        <h3 className="admin-h2">Khu vực quản trị</h3>
        <div className="mt-3 grid gap-3 sm:grid-cols-2">
          <AreaCard
            href={AREA_ENTRY.thpt}
            icon={GraduationCap}
            title="THPT – THCS"
            desc="Bài học, đề kiểm tra, lớp học và bảng điểm Vật lý 9–12"
          />
          <AreaCard
            href={AREA_ENTRY.cttc}
            icon={Cpu}
            title="CTTC"
            desc="Nội dung học phần CNC, lớp học phần và tình trạng máy"
            cttc
          />
        </div>
      </section>
    </div>
  );
}

function Stat({
  icon: Icon,
  label,
  value,
  href,
  tone,
}: {
  icon: typeof BookOpen;
  label: string;
  value: number | null;
  href?: string;
  /** warn: ô "cần xử lý" — sáng lên khi > 0, mờ đi khi = 0. */
  tone?: "warn";
}) {
  const active = tone === "warn" && !!value;
  const body = (
    <>
      <p className="admin-stat-label">
        <Icon size={14} /> {label}
      </p>
      {value === null ? (
        <span className="mt-2 block h-[29px] w-16 animate-pulse rounded-md bg-white/10" aria-label="Đang tải" />
      ) : (
        <p className="admin-stat-value" style={active ? { color: "#fca5a5" } : undefined}>
          {value.toLocaleString("vi-VN")}
        </p>
      )}
    </>
  );
  const style = tone === "warn" && value === 0 ? { opacity: 0.6 } : undefined;
  return href ? (
    <Link href={href} className="admin-stat block transition-colors hover:border-white/25" style={style}>
      {body}
    </Link>
  ) : (
    <div className="admin-stat" style={style}>
      {body}
    </div>
  );
}

function AreaCard({
  href,
  icon: Icon,
  title,
  desc,
  cttc,
}: {
  href: string;
  icon: typeof BookOpen;
  title: string;
  desc: string;
  cttc?: boolean;
}) {
  return (
    <Link href={href} className={`admin-action ${cttc ? "admin-action--cttc" : ""}`} style={{ padding: "18px 18px" }}>
      <span className="admin-action-icon" style={{ width: 42, height: 42 }}>
        <Icon size={20} />
      </span>
      <span className="min-w-0 flex-1">
        <b style={{ fontSize: 15.5 }}>{title}</b>
        <span>{desc}</span>
      </span>
      <ArrowRight size={17} className="mt-1 shrink-0 opacity-50" />
    </Link>
  );
}
