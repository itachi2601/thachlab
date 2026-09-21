import RequireAuth from "@/components/auth/RequireAuth";

export default function ThptAdminLayout({ children }: { children: React.ReactNode }) {
  return <RequireAuth area="thpt">{children}</RequireAuth>;
}
