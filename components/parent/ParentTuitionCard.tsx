import { PAYMENT_STATUS_LABEL, type MyRegistration } from "@/services/thpt-courses";
import type { ThptCourse } from "@/services/thpt-courses-public";

/**
 * Học phí — với lớp học thêm, đây là câu hỏi hạng 2–3 của phụ huynh ("tôi đã đóng chưa, đóng bao nhiêu").
 * Chỉ ĐỌC trạng thái thầy đã ghi (thpt_registrations.payment_status), không có nút thanh toán.
 * Chưa đóng nói trung tính, kèm lối hỏi lại: có thể chỉ là thầy chưa kịp ghi.
 */
export default function ParentTuitionCard({
  registrations,
  courses,
}: {
  registrations: MyRegistration[];
  courses: ThptCourse[];
}) {
  const items = registrations.filter((r) => r.status === "active" || r.status === "catchup");
  if (items.length === 0) return null;
  const feeByCourse = new Map(courses.map((c) => [c.id, c.fee_note]));

  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-5">
      <h2 className="font-display text-lg font-semibold text-white">Học phí</h2>
      <ul className="mt-3 divide-y divide-white/10">
        {items.map((r) => {
          const paid = r.payment_status !== "unpaid";
          const fee = feeByCourse.get(r.course_id);
          return (
            <li key={r.id} className="py-3 first:pt-0 last:pb-0">
              <p className="font-semibold text-white">{r.courseName}</p>
              {fee ? <p className="parent-copy text-slate-400">{fee}</p> : null}
              <p className={`mt-1 font-semibold ${paid ? "text-emerald-300" : "text-amber-300"}`}>
                {paid ? PAYMENT_STATUS_LABEL[r.payment_status] : "Thầy chưa ghi nhận khoản đóng"}
              </p>
              {r.payment_note ? <p className="parent-copy text-slate-300">{r.payment_note}</p> : null}
              {!paid && (
                <p className="parent-copy text-slate-400">
                  Nếu phụ huynh đã đóng rồi, nhắn thầy qua Zalo để thầy cập nhật.
                </p>
              )}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
