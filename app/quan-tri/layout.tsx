import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-7xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          Quản <span className="text-gradient">trị</span>
        </h1>
        <RequireAuth adminOnly>
          <div className="mt-8">{children}</div>
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
