import RequireAuth from "@/components/auth/RequireAuth";

export default function SharedAdminLayout({ children }: { children: React.ReactNode }) {
  return <RequireAuth restrictToAdmin>{children}</RequireAuth>;
}
