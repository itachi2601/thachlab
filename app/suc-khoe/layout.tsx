import AuthedShell from "@/components/auth/AuthedShell";

// Nhóm /suc-khoe cần đăng nhập thật: phải có AuthProvider ở trên (app/layout.tsx không còn bọc),
// nếu thiếu thì useAuth() rơi về "khách" và RequireAuth luôn hiện "Em cần đăng nhập…".
export default function Layout({ children }: { children: React.ReactNode }) {
  return <AuthedShell>{children}</AuthedShell>;
}
