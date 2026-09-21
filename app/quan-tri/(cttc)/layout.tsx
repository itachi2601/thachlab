import RequireAuth from "@/components/auth/RequireAuth";

export default function CttcAdminLayout({ children }: { children: React.ReactNode }) {
  return <RequireAuth area="cttc">{children}</RequireAuth>;
}
