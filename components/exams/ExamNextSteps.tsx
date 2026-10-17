import Link from "next/link";

interface Props {
  /** Có thì hiện "Làm lại đề này" (nơi gọi quyết định bằng shouldOfferRetry). */
  retryHref?: string;
  /** Có thì hiện "Ôn chủ đề này" — bài lý thuyết của chủ đề em sai. */
  reviewHref?: string;
}

const BASE = "inline-flex min-h-11 items-center justify-center rounded-xl px-4 text-sm font-semibold";
const OUTLINE = `${BASE} border border-line text-ink hover:border-primary hover:text-primary`;

/**
 * Hàng nút đi tiếp ở CUỐI phần xem lại bài làm — một lối thoát duy nhất, không lặp ở giữa trang (L5, D2/D3).
 * Nút chính (Về Hôm nay) đặt đầu, mỗi nút ≥ 44px, trên điện thoại xếp dọc.
 */
export default function ExamNextSteps({ retryHref, reviewHref }: Props) {
  return (
    <nav aria-label="Đi tiếp" className="mt-8 flex flex-col gap-2 border-t border-line pt-5 sm:flex-row sm:flex-wrap">
      <Link href="/tai-khoan" className={`${BASE} bg-primary text-white hover:bg-primary-dark`}>
        Về Hôm nay
      </Link>
      {reviewHref && (
        <Link href={reviewHref} className={OUTLINE}>
          Ôn chủ đề này
        </Link>
      )}
      <Link href="/lop-hoc" className={OUTLINE}>
        Về danh sách đề
      </Link>
      {retryHref && (
        // <a>: cùng đường dẫn /kiem-tra/lam nên cần tải lại trang.
        <a href={retryHref} className={OUTLINE}>
          Làm lại đề này
        </a>
      )}
      {retryHref && <p className="text-[13px] text-muted sm:basis-full">Làm lại không cộng thêm RP bài này.</p>}
    </nav>
  );
}
