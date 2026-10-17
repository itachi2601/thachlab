import Link from "next/link";
import { nenKhtn9Href, nenKhtn9Of, tiepLop10Href, tiepLop10Of } from "@/features/hsg9/nen-khtn9";

/** "Ôn nền KHTN 9": nối bài HSG về các bài KHTN 9 cùng chủ đề (học lại nền trước khi vào phần nâng cao). */
export default function NenKhtn9({ lessonIds, compact = false }: { lessonIds: number[]; compact?: boolean }) {
  const items = [...new Map(lessonIds.flatMap(nenKhtn9Of).map((l) => [l.id, l])).values()];
  // "Học tiếp ở lớp 10" chỉ hiện ở trang bài (gập sẵn), không hiện ở thẻ Tuần này để khỏi quá tải.
  const tiep = compact ? [] : [...new Map(lessonIds.flatMap(tiepLop10Of).map((l) => [l.id, l])).values()];
  if (items.length === 0 && tiep.length === 0) return null;
  return (
    <div className={compact ? "mt-2" : "mb-4 rounded-xl border border-line bg-panel p-3"}>
      {items.length > 0 && (
        <>
          <p className="text-xs font-semibold uppercase tracking-wide text-muted">Ôn nền KHTN 9</p>
          <ul className="mt-1 space-y-0.5">
            {items.map((l) => (
              <li key={l.id}>
                <Link href={nenKhtn9Href(l.id)} className="lesson-link inline-flex min-h-11 items-center text-sm">
                  {l.title}
                </Link>
              </li>
            ))}
          </ul>
        </>
      )}
      {tiep.length > 0 && (
        <details className={items.length > 0 ? "mt-2 border-t border-line pt-2" : ""}>
          <summary className="flex min-h-11 cursor-pointer items-center text-xs font-semibold uppercase tracking-wide text-muted">
            Học tiếp ở lớp 10
          </summary>
          <ul className="mt-1 space-y-0.5">
            {tiep.map((l) => (
              <li key={l.id}>
                <Link href={tiepLop10Href(l.id)} className="lesson-link inline-flex min-h-11 items-center text-sm">
                  {l.title}
                </Link>
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}
