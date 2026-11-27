import RequireAuth from "@/components/auth/RequireAuth";
import AbetOverview from "@/components/admin/AbetOverview";

// Dữ liệu ABET (MSSV + điểm của sinh viên nhiều lớp) chỉ admin xem — RLS abet_* cũng chỉ mở cho is_admin().
export default function Page() {
  return (
    <RequireAuth restrictToAdmin>
      <AbetOverview />
    </RequireAuth>
  );
}
