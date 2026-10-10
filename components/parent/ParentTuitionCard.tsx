"use client";

import { useEffect, useState } from "react";
import { parentFeeBlocks, parentMonthLine, type TuitionMonth } from "@/features/tuition/ledger";
import { PAYMENT_STATUS_LABEL, type MyRegistration } from "@/services/thpt-courses";
import type { ThptCourse } from "@/services/thpt-courses-public";
import { fetchFamilyTuition } from "@/services/tuition";

/**
 * Học phí — với lớp học thêm, đây là câu hỏi hạng 2–3 của phụ huynh ("tôi đã đóng chưa, đóng bao nhiêu").
 * Mặc định chỉ ĐỌC ô thầy đã ghi (thpt_registrations.payment_status), không có nút thanh toán (P23).
 * Sổ theo tháng nằm sau cờ family_visible. Cờ tắt hoặc hàm chưa có → mảng rỗng, thẻ giữ nguyên câu cũ.
 * Có khoản tháng thì nói bằng chữ, không chỉ bằng màu (P12). Chưa đóng nói trung tính, kèm lối hỏi lại.
 */
export default function ParentTuitionCard({
  registrations,
  courses,
}: {
  registrations: MyRegistration[];
  courses: ThptCourse[];
}) {
  const [months, setMonths] = useState<TuitionMonth[]>([]);
  const items = registrations.filter((r) => r.status === "active" || r.status === "catchup");
  const watch = items.map((r) => r.student_id ?? "").join("|");

  useEffect(() => {
    let cancelled = false;
    fetchFamilyTuition().then((rows) => {
      if (!cancelled) setMonths(rows);
    });
    return () => {
      cancelled = true;
    };
  }, [watch]);

  if (items.length === 0) return null;

  const blocks = parentFeeBlocks(
    items.map((r) => ({
      id: r.id,
      courseId: r.course_id,
      courseName: r.courseName,
      studentId: r.student_id,
      paymentStatus: r.payment_status,
      paymentNote: r.payment_note,
    })),
    courses.map((c) => ({
      id: c.id,
      name: c.name,
      feeNote: c.fee_note,
      pairKey: c.pairKey,
      pairSlot: c.pairSlot,
    })),
    months,
  );

  return (
    <section className="rounded-2xl border border-line bg-panel p-5">
      <h2 className="font-display text-lg font-semibold text-ink">Học phí</h2>
      <ul className="mt-3 divide-y divide-line">
        {blocks.map((block) => {
          const paid = block.paymentStatus !== "unpaid";
          return (
            <li key={block.key} className="py-3 first:pt-0 last:pb-0">
              <p className="font-semibold text-ink">{block.title}</p>
              {block.feeNote ? <p className="parent-copy text-muted">{block.feeNote}</p> : null}
              {block.months.length > 0 ? (
                <ul className="mt-1 space-y-1">
                  {block.months.map((m) => {
                    const line = parentMonthLine(m);
                    return (
                      <li
                        key={m.period}
                        className={`font-semibold ${line.tone === "paid" ? "text-ok" : line.tone === "waived" ? "text-ink" : "text-warn"}`}
                      >
                        {line.text}
                      </li>
                    );
                  })}
                </ul>
              ) : (
                <>
                  <p className={`mt-1 font-semibold ${paid ? "text-ok" : "text-warn"}`}>
                    {paid ? PAYMENT_STATUS_LABEL[block.paymentStatus] : "Thầy chưa ghi nhận khoản đóng"}
                  </p>
                  {block.paymentNote ? <p className="parent-copy text-ink">{block.paymentNote}</p> : null}
                  {!paid && (
                    <p className="parent-copy text-muted">
                      Nếu phụ huynh đã đóng rồi, nhắn thầy qua Zalo để thầy cập nhật.
                    </p>
                  )}
                </>
              )}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
