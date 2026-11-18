import type { Metadata } from "next";

// Trang là client component nên tiêu đề đặt ở layout — tab/lịch sử trình duyệt phân biệt được với trang chủ.
export const metadata: Metadata = { title: "Bài đã làm & kết quả" };

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
