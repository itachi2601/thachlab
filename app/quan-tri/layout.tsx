import AdminShell from "@/components/admin/AdminShell";
import RequireAuth from "@/components/auth/RequireAuth";
import AuthedShell from "@/components/auth/AuthedShell";

// AuthProvider trước đây nằm ở app/layout.tsx (gốc, áp dụng mọi trang) — giờ mỗi nhóm
// route tự thêm, /quan-tri thêm ở đây vì RequireAuth (bên trong AdminShell) cần useAuth().
export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthedShell>
      <AdminShell>
        <RequireAuth adminOnly>{children}</RequireAuth>
      </AdminShell>
    </AuthedShell>
  );
}
