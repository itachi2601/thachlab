import { MessageCircle, Phone } from "lucide-react";
import { CONTACT } from "@/lib/contact";

/**
 * Lối liên hệ thầy, đặt ở đầu VÀ cuối trang phụ huynh (P10: phụ huynh 45–60 tuổi không đi tìm
 * nút liên hệ — họ gọi điện. Điện thoại là kênh chính, Zalo là kênh phụ, form/email là kênh cuối).
 *
 * variant "slim": một dòng, dùng ngay dưới tiêu đề trang.
 * variant "full": thẻ có tiêu đề + 2 nút to (≥48px), dùng ở cuối trang và ở trang khách.
 *
 * Số điện thoại hiển thị có khoảng trắng (0982 702 591) để đọc thành tiếng được khi mắt yếu;
 * href="tel:" vẫn dùng số trần.
 */
export function displayPhone(raw: string) {
  const digits = raw.replace(/\D/g, "");
  if (digits.length === 10) return `${digits.slice(0, 4)} ${digits.slice(4, 7)} ${digits.slice(7)}`;
  return raw;
}

export default function TeacherContact({
  variant = "full",
  className = "",
}: {
  variant?: "full" | "slim";
  className?: string;
}) {
  if (!CONTACT.phone && !CONTACT.zalo) return null;
  const phone = CONTACT.phone ? displayPhone(CONTACT.phone) : "";

  const zaloBtn =
    "inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-5 py-3 text-base font-semibold text-white hover:bg-primary-dark";
  const phoneBtn =
    "inline-flex items-center justify-center gap-2 rounded-xl border border-line px-5 py-3 text-base font-semibold text-ink hover:border-line-strong";

  if (variant === "slim") {
    return (
      <div
        className={`flex flex-wrap items-center gap-x-4 gap-y-1 rounded-2xl border border-line bg-panel px-5 py-3 text-ink ${className}`}
      >
        <span>Cần trao đổi với thầy về con?</span>
        {CONTACT.phone && (
          <a href={`tel:${CONTACT.phone}`} className="font-semibold text-primary underline-offset-2 hover:underline">
            Gọi {phone}
          </a>
        )}
        {CONTACT.zalo && (
          <a
            href={CONTACT.zalo}
            target="_blank"
            rel="noopener noreferrer"
            className="font-semibold text-primary underline-offset-2 hover:underline"
          >
            Nhắn Zalo
          </a>
        )}
      </div>
    );
  }

  return (
    <section className={`rounded-2xl border border-line bg-panel p-5 sm:p-6 ${className}`}>
      <h2 className="font-display text-lg font-bold text-ink">Cần trao đổi với thầy về con?</h2>
      <p className="parent-copy mt-1.5 text-muted">
        Thầy thường trả lời Zalo trong ngày. Nếu việc gấp (con ốm, xin nghỉ, đổi lịch học), phụ huynh gọi
        trực tiếp. Gõ chữ không tiện thì cứ gửi tin nhắn thoại Zalo cũng được.
      </p>
      <div className="mt-4 flex flex-wrap gap-3">
        {CONTACT.phone && (
          <a href={`tel:${CONTACT.phone}`} className={phoneBtn}>
            <Phone size={18} /> Gọi {phone}
          </a>
        )}
        {CONTACT.zalo && (
          <a href={CONTACT.zalo} target="_blank" rel="noopener noreferrer" className={zaloBtn}>
            <MessageCircle size={18} /> Nhắn Zalo cho thầy
          </a>
        )}
      </div>
      {(CONTACT.area || CONTACT.school) && (
        <p className="mt-3 text-muted">
          {[CONTACT.school, CONTACT.area].filter(Boolean).join(" · ")}
        </p>
      )}
    </section>
  );
}
