import AuthedShell from "@/components/auth/AuthedShell";

export default function Layout({ children }: { children: React.ReactNode }) {
  return <AuthedShell>{children}</AuthedShell>;
}
