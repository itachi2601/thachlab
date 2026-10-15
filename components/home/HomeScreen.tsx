/**
 * Một "màn" của trang chủ trên máy tính: cao đúng phần nhìn thấy dưới thanh menu (77px, fixed) và căn nội dung
 * vào giữa, để mỗi lần cuộn thấy trọn một phần (N1 một màn hình = một việc, B2 một điểm nổi bật/màn).
 * Chỉ áp từ lg; điện thoại giữ dòng chảy cũ. Không dùng scroll-snap (giật, kẹt cuộn khi phần cao hơn màn).
 */
export default function HomeScreen({
  id,
  first = false,
  className = "bg-bg",
  children,
}: {
  id?: string;
  /** Màn đầu nằm dưới thanh menu fixed nên tính cả chiều cao thanh menu. */
  first?: boolean;
  /** Nền của màn, trùng nền của khối bên trong để khoảng trống trên/dưới liền một mảng. */
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div
      id={id}
      className={`scroll-mt-[77px] lg:flex lg:flex-col lg:justify-center ${
        first ? "lg:min-h-svh" : "lg:min-h-[calc(100svh-77px)]"
      } ${className}`}
    >
      {children}
    </div>
  );
}
