import AdminSidebar from "@/components/admin/AdminSidebar";
import RequireAuth from "@/components/auth/RequireAuth";

export default function ThptAdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <RequireAuth area="thpt">
      <div className="flex flex-col gap-6 lg:flex-row lg:items-start">
        <AdminSidebar area="thpt" />
        <div className="min-w-0 flex-1">{children}</div>
      </div>
    </RequireAuth>
  );
}
