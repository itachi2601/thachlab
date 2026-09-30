"use client";

import { useCallback, useSyncExternalStore } from "react";
import Link from "next/link";
import { ArrowRight, X } from "lucide-react";

/**
 * Bảng chào mừng theo vai — chỉ dùng dữ liệu Account() đã có, không thêm round-trip Supabase.
 * Đóng rồi thì nhớ theo (tài khoản + tình huống) trong localStorage; đổi tình huống (vd. từ
 * "chờ duyệt" sang "đã vào lớp") thì bảng mới hiện lại đúng nội dung mới.
 */
export type WelcomeVariant =
  | "student_new"
  | "thpt_pick_class"
  | "thpt_pending"
  | "thpt_active"
  | "cttc_join"
  | "cttc_pending"
  | "cttc_active"
  | "instructor"
  | "admin"
  | "tro_giang"
  | "parent";

interface Tip { label: string; href: string }
interface Content { title: string; lead: string; primary: Tip; secondary?: Tip[]; tone: "blue" | "orange" | "emerald" | "cyan" }

const CONTENT: Record<WelcomeVariant, Content> = {
  student_new: {
    tone: "blue",
    title: "Chào mừng em đến ThachLab",
    lead: "Bắt đầu bằng việc chọn đúng luồng học bên dưới: THPT (chọn khối 9–12) hoặc CTTC (nhập mã khóa). Thầy duyệt xong là em vào học ngay.",
    primary: { label: "Xem các bài học mẫu", href: "/lop-hoc" },
  },
  thpt_pick_class: {
    tone: "blue",
    title: "Bước 1: chọn khối lớp của em",
    lead: "Gửi yêu cầu vào đúng khối lớp bên dưới. Giáo viên duyệt xong, em sẽ thấy bài học, đề kiểm tra và bảng xếp hạng của lớp.",
    primary: { label: "Xem trước nội dung các lớp", href: "/lop-hoc" },
  },
  thpt_pending: {
    tone: "blue",
    title: "Yêu cầu của em đang chờ duyệt",
    lead: "Trong lúc chờ, em có thể xem qua bài học để biết trước ThachLab học như thế nào. Bấm “Kiểm tra lại” để cập nhật khi thầy đã duyệt.",
    primary: { label: "Xem bài học", href: "/lop-hoc" },
  },
  thpt_active: {
    tone: "blue",
    title: "Hôm nay em học gì?",
    lead: "Mỗi ngày một ít: làm nhiệm vụ ngày để giữ chuỗi và tích RP, rồi ôn lại các bài đang “Cần luyện thêm”.",
    primary: { label: "Vào lớp học", href: "/lop-hoc" },
    secondary: [
      { label: "Xem bảng xếp hạng", href: "/lop-hoc/xep-hang" },
      { label: "Kết quả của em", href: "/lop-hoc/ket-qua" },
    ],
  },
  cttc_join: {
    tone: "orange",
    title: "Nhập mã khóa để vào lớp thực hành",
    lead: "Mã dạng CNC-XXXXXX hoặc TP-XXXXXX do giảng viên cung cấp. Gửi yêu cầu xong, chờ giảng viên duyệt.",
    primary: { label: "Xem học liệu", href: "/khoa-hoc" },
  },
  cttc_pending: {
    tone: "orange",
    title: "Yêu cầu vào khóa đang chờ duyệt",
    lead: "Giảng viên sẽ duyệt sớm. Trong lúc chờ, xem trước danh sách khóa học của ThachLab.",
    primary: { label: "Xem khóa học", href: "/khoa-hoc" },
  },
  cttc_active: {
    tone: "orange",
    title: "Chào em, vào buổi thực hành",
    lead: "Trước giờ máy: đọc lại bài, xem video thao tác, tự đánh giá theo rubric. Nhớ an toàn lao động trước khi vận hành.",
    primary: { label: "Vào khóa học", href: "/khoa-hoc" },
    secondary: [{ label: "Đổi mật khẩu", href: "/tai-khoan/doi-mat-khau" }],
  },
  instructor: {
    tone: "cyan",
    title: "Chào thầy/cô",
    lead: "Việc nên xem trước: học sinh cần phụ đạo, bài nộp chưa chấm, rồi mới đến đăng nội dung mới.",
    primary: { label: "Vào Dashboard giáo viên", href: "/dashboard-thpt" },
    secondary: [
      { label: "Đăng đề mới", href: "/quan-tri/dang-de" },
      { label: "Khu vực quản trị", href: "/quan-tri" },
    ],
  },
  admin: {
    tone: "cyan",
    title: "Tổng quan quản trị",
    lead: "Kiểm tra việc chờ xử lý: lời mời giáo viên chưa nhận, báo lỗi mới, ngân hàng câu hỏi nghi trùng. Dùng “Xem như học sinh” để kiểm giao diện từng vai.",
    primary: { label: "Vào Quản trị", href: "/quan-tri" },
    secondary: [
      { label: "Dashboard giáo viên", href: "/dashboard-thpt" },
      { label: "Báo lỗi của tôi", href: "/bao-loi-cua-toi" },
    ],
  },
  tro_giang: {
    tone: "cyan",
    title: "Chào bạn, trợ giảng",
    lead: "Xem việc được giao hôm nay, ghi chép buổi học và các mẫu, quy chế dành cho trợ giảng.",
    primary: { label: "Vào trang trợ giảng", href: "/tro-giang" },
  },
  parent: {
    tone: "emerald",
    title: "Kết quả học tập của con",
    lead: "Xem điểm, tiến độ và mức “Nắm vững” của con theo từng bài. Nếu chưa thấy dữ liệu, nhờ giáo viên chủ nhiệm liên kết tài khoản với con.",
    primary: { label: "Xem kết quả của con", href: "/phu-huynh" },
    secondary: [{ label: "Thông báo từ lớp", href: "/thong-bao" }],
  },
};

const TONE: Record<Content["tone"], string> = {
  blue: "border-blue-400/25 bg-blue-500/[.06]",
  orange: "border-orange-400/25 bg-orange-500/[.06]",
  emerald: "border-emerald-400/25 bg-emerald-500/[.06]",
  cyan: "border-cyan-400/25 bg-cyan-500/[.06]",
};

const EVENT = "thachlab-welcome-change";
const keyOf = (userId: string, variant: WelcomeVariant) => `thachlab_welcome_off_${userId}_${variant}`;

function subscribe(onChange: () => void) {
  window.addEventListener("storage", onChange);
  window.addEventListener(EVENT, onChange);
  return () => {
    window.removeEventListener("storage", onChange);
    window.removeEventListener(EVENT, onChange);
  };
}

function greeting(): string {
  const h = new Date().getHours();
  if (h < 11) return "Chào buổi sáng";
  if (h < 14) return "Chào buổi trưa";
  if (h < 18) return "Chào buổi chiều";
  return "Chào buổi tối";
}

export default function WelcomePanel({
  variant,
  userId,
  name,
}: {
  variant: WelcomeVariant;
  userId: string;
  name?: string | null;
}) {
  const key = keyOf(userId, variant);
  // Server/lần render đầu coi như đã đóng để không chớp hình rồi biến mất.
  const dismissed = useSyncExternalStore(
    subscribe,
    () => {
      try { return localStorage.getItem(key) === "1"; } catch { return false; }
    },
    () => true,
  );
  const dismiss = useCallback(() => {
    try { localStorage.setItem(key, "1"); } catch { /* không lưu được thì thôi, bảng vẫn đóng ở phiên này */ }
    window.dispatchEvent(new Event(EVENT));
  }, [key]);

  if (dismissed) return null;
  const c = CONTENT[variant];
  const firstName = name?.trim().split(/\s+/).pop();

  return (
    <aside role="region" aria-label="Chào mừng" className={`relative mb-6 rounded-3xl border p-6 pr-12 ${TONE[c.tone]}`}>
      <button
        type="button"
        onClick={dismiss}
        aria-label="Đóng bảng chào mừng"
        title="Không hiện lại"
        className="absolute right-4 top-4 rounded-full p-1.5 text-slate-400 hover:bg-white/10 hover:text-white"
      >
        <X size={16} />
      </button>
      {firstName && <p className="text-xs font-semibold text-slate-400">{greeting()}, {firstName}</p>}
      <h2 className="mt-1 font-display text-xl font-bold text-white">{c.title}</h2>
      <p className="mt-2 max-w-2xl text-sm leading-relaxed text-slate-300">{c.lead}</p>
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Link href={c.primary.href} className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white">
          {c.primary.label}
          <ArrowRight size={15} />
        </Link>
        {c.secondary?.map((t) => (
          <Link key={t.href} href={t.href} className="rounded-xl border border-white/15 px-4 py-2.5 text-sm font-semibold text-slate-200 hover:border-white/30">
            {t.label}
          </Link>
        ))}
      </div>
    </aside>
  );
}
