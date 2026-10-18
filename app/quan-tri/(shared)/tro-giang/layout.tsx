import TroGiangAdminNav from "@/components/tro-giang/TroGiangAdminNav";

export default function TroGiangAdminLayout({ children }: { children: React.ReactNode }) {
  return (
    // pb-28: chừa chỗ cho nút nổi "Xem thử như…" (admin-dock) để không đè ô nhập ở cuối trang.
    <div className="space-y-6 pb-28">
      <TroGiangAdminNav />
      {children}
    </div>
  );
}
