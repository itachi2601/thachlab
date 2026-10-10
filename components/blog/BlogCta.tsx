import Link from "next/link";

/** Khối kêu gọi hành động ở cuối mỗi bài viết — điều hướng sang đăng ký / lớp học. */
export default function BlogCta() {
  return (
    <aside className="mt-14 overflow-hidden rounded-3xl border border-line bg-panel p-8 text-center">
      <p className="font-display text-xl font-bold text-ink sm:text-2xl">
        Sẵn sàng bắt đầu lộ trình của con?
      </p>
      <p className="mx-auto mt-3 max-w-lg text-sm leading-relaxed text-muted">
        Đăng ký học thử offline miễn phí, nhận lộ trình cá nhân hóa và tài khoản
        học online cùng thầy Thạch.
      </p>
      <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
        <Link
          href="/dang-ky"
          className="rounded-full bg-primary px-6 py-3 text-sm font-semibold text-white shadow-sm shadow-blue-900/30 transition-transform hover:-translate-y-0.5 hover:bg-primary-dark"
        >
          Đăng ký học thử miễn phí
        </Link>
        <Link
          href="/lop-hoc"
          className="rounded-full border border-line-strong px-6 py-3 text-sm font-semibold text-ink transition-colors hover:border-primary"
        >
          Xem chương trình học
        </Link>
      </div>
    </aside>
  );
}
