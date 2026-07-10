"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { getSupabase, supabaseConfigured } from "@/services/supabase";
import { useToast } from "@/components/ui/Toast";
import { exportStudentToExcel } from "@/services/excel-export";

const inputCls = "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white focus:border-[#3B82F6] focus:outline-none placeholder:text-slate-600";

export default function RegisterPage() {
  const router = useRouter();
  const toast = useToast();
  const [step, setStep] = useState<"form" | "confirm">("form");
  const [busy, setBusy] = useState(false);

  // Form state
  const [fullName, setFullName] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [parentPhone, setParentPhone] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [gender, setGender] = useState("");
  const [studentId, setStudentId] = useState("");
  const [error, setError] = useState("");

  const validateForm = (): boolean => {
    setError("");

    if (!fullName.trim()) {
      setError("Vui lòng nhập họ và tên đầy đủ");
      return false;
    }

    if (!username.trim()) {
      setError("Vui lòng nhập username");
      return false;
    }

    const usernameRegex = /^(?=.*[a-zA-Z])[a-zA-Z0-9_.\-]+$/;
    if (!usernameRegex.test(username)) {
      setError("Username chỉ chứa chữ, số, gạch chân (_), gạch ngang (-), dấu chấm (.) và phải có ít nhất 1 chữ");
      return false;
    }

    if (!password.trim()) {
      setError("Vui lòng nhập mật khẩu");
      return false;
    }

    if (password.length < 6) {
      setError("Mật khẩu phải dài tối thiểu 6 ký tự");
      return false;
    }

    if (password !== confirmPassword) {
      setError("Mật khẩu xác nhận không khớp");
      return false;
    }

    if (email.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError("Email không hợp lệ");
      return false;
    }

    if (phone.trim() && !/^\d+$/.test(phone)) {
      setError("Số điện thoại chỉ chứa chữ số");
      return false;
    }

    if (parentPhone.trim() && !/^\d+$/.test(parentPhone)) {
      setError("Số điện thoại phụ huynh chỉ chứa chữ số");
      return false;
    }

    if (studentId.trim()) {
      const idNum = parseInt(studentId, 10);
      if (isNaN(idNum) || idNum <= 0 || studentId.length > 8) {
        setError("Số báo danh phải là số dương, tối đa 8 chữ số");
        return false;
      }
    }

    return true;
  };

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setStep("confirm");
  }

  async function handleConfirm() {
    setBusy(true);
    setError("");

    try {
      const { data: authData, error: authError } = await getSupabase().auth.signUp({
        email: email || `${username}@thachlab.local`,
        password,
        options: {
          data: {
            full_name: fullName,
            class_name: "",
          },
        },
      });

      if (authError) {
        setError(authError.message);
        setBusy(false);
        return;
      }

      if (!authData.user) {
        setError("Không thể tạo tài khoản");
        setBusy(false);
        return;
      }

      const { error: profileError } = await getSupabase()
        .from("profiles")
        .update({
          full_name: fullName,
        })
        .eq("id", authData.user.id);

      if (profileError) {
        console.error("Profile update error:", profileError);
      }

      const studentData = {
        stt: 1,
        fullName,
        username,
        phone: phone || "",
        parentPhone: parentPhone || "",
        email: email || "",
        birthDate: birthDate || "",
        gender: gender || "",
        studentId: studentId || "",
        password,
        class: "",
      };

      const excelFile = await exportStudentToExcel([studentData]);

      const url = window.URL.createObjectURL(excelFile);
      const a = document.createElement("a");
      a.href = url;
      a.download = `danh-sach-hoc-sinh-${Date.now()}.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast("success", "Đăng ký thành công! File Excel đã được tải xuống.");

      setTimeout(() => {
        router.push("/dang-nhap");
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Đăng ký thất bại");
      setBusy(false);
    }
  }

  if (!supabaseConfigured) {
    return (
      <>
        <Navbar />
        <main className="mx-auto min-h-screen w-full max-w-md px-6 pt-32 pb-20">
          <p className="text-slate-400">Hệ thống đang được cấu hình, vui lòng quay lại sau.</p>
        </main>
        <Footer />
      </>
    );
  }

  if (step === "confirm") {
    return (
      <>
        <Navbar />
        <main className="mx-auto min-h-screen w-full max-w-md px-6 pt-32 pb-20">
          <h1 className="font-display text-3xl font-bold text-white">
            Xác <span className="text-gradient">nhận</span>
          </h1>

          <div className="mt-8 space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-6">
            <p className="text-sm text-slate-300">
              <strong className="text-white">Họ và tên:</strong> {fullName}
            </p>
            <p className="text-sm text-slate-300">
              <strong className="text-white">Username:</strong> {username}
            </p>
            {email && (
              <p className="text-sm text-slate-300">
                <strong className="text-white">Email:</strong> {email}
              </p>
            )}
            {phone && (
              <p className="text-sm text-slate-300">
                <strong className="text-white">Số điện thoại:</strong> {phone}
              </p>
            )}

            <div className="mt-4 rounded-lg border border-amber-500/30 bg-amber-500/5 p-3">
              <p className="text-xs text-amber-300">
                ℹ️ Thông tin này sẽ được export ra file Excel để nhập vào AZOTA
              </p>
            </div>
          </div>

          <div className="mt-6 flex gap-3">
            <button
              onClick={() => setStep("form")}
              disabled={busy}
              className="flex-1 rounded-full border border-white/15 px-5 py-3 text-sm font-semibold text-slate-300 hover:border-white/30"
            >
              Quay lại sửa
            </button>
            <button
              onClick={handleConfirm}
              disabled={busy}
              className="flex-1 rounded-full bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white hover:bg-[#1D4ED8] disabled:opacity-50"
            >
              {busy ? "Đang xử lý…" : "Xác nhận & Download Excel"}
            </button>
          </div>

          {error && <p className="text-sm text-red-400">❌ {error}</p>}
        </main>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-md px-6 pt-32 pb-20">
        <h1 className="font-display text-3xl font-bold text-white">
          Đăng <span className="text-gradient">ký</span>
        </h1>

        <form onSubmit={handleSubmit} className="mt-8 space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Họ và tên <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Nguyễn Văn A"
              className={inputCls}
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Username <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value.toLowerCase())}
              placeholder="nguyen_van_a"
              className={inputCls}
            />
            <p className="mt-1 text-xs text-slate-500">Chỉ chứa chữ, số, gạch chân, gạch ngang, dấu chấm</p>
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Mật khẩu <span className="text-red-400">*</span>
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Tối thiểu 6 ký tự"
              className={inputCls}
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Xác nhận mật khẩu <span className="text-red-400">*</span>
            </label>
            <input
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Nhập lại mật khẩu"
              className={inputCls}
            />
          </div>

          <div className="mt-6 border-t border-white/10 pt-4">
            <p className="text-xs font-semibold text-slate-400 mb-4">Thông tin bổ sung (tùy chọn)</p>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="example@gmail.com"
                className={inputCls}
              />
            </div>

            <div className="mt-3">
              <label className="mb-1 block text-sm font-medium text-slate-300">Số điện thoại</label>
              <input
                type="text"
                value={phone}
                onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
                placeholder="0123456789"
                className={inputCls}
              />
            </div>

            <div className="mt-3">
              <label className="mb-1 block text-sm font-medium text-slate-300">Số điện thoại phụ huynh</label>
              <input
                type="text"
                value={parentPhone}
                onChange={(e) => setParentPhone(e.target.value.replace(/\D/g, ""))}
                placeholder="0123456789"
                className={inputCls}
              />
            </div>

            <div className="mt-3">
              <label className="mb-1 block text-sm font-medium text-slate-300">Ngày sinh</label>
              <input
                type="date"
                value={birthDate}
                onChange={(e) => setBirthDate(e.target.value)}
                className={inputCls}
              />
            </div>

            <div className="mt-3">
              <label className="mb-1 block text-sm font-medium text-slate-300">Giới tính</label>
              <select value={gender} onChange={(e) => setGender(e.target.value)} className={inputCls}>
                <option value="">-- Chọn --</option>
                <option value="1">Nam</option>
                <option value="0">Nữ</option>
              </select>
            </div>

            <div className="mt-3">
              <label className="mb-1 block text-sm font-medium text-slate-300">Số báo danh</label>
              <input
                type="text"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value.replace(/\D/g, ""))}
                placeholder="Số từ 1-99999999"
                className={inputCls}
              />
            </div>
          </div>

          {error && <p className="text-sm text-red-400">❌ {error}</p>}

          <button
            type="submit"
            disabled={busy}
            className="w-full rounded-full bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white hover:bg-[#1D4ED8] disabled:opacity-50"
          >
            {busy ? "Đang xử lý…" : "Tiếp tục"}
          </button>

          <p className="text-center text-sm text-slate-400">
            Đã có tài khoản?{" "}
            <Link href="/dang-nhap" className="text-[#3B82F6] hover:underline">
              Đăng nhập
            </Link>
          </p>
        </form>
      </main>
      <Footer />
    </>
  );
}
