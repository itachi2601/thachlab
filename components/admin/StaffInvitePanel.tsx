"use client";

import { useCallback, useEffect, useState } from "react";
import { Clock3, Check, Mail, X } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { displayClassesByGrade, fetchClasses } from "@/services/classes";
import {
  fetchStaffInvites,
  inviteStaff,
  revokeStaffInvite,
  type StaffInvite,
  type StaffInviteRole,
} from "@/services/staff-invites";
import type { SchoolClass } from "@/features/exams/types";

function errorMessage(error: unknown, fallback: string) {
  if (error instanceof Error) return error.message;
  return fallback;
}

const ROLES: { id: StaffInviteRole; label: string }[] = [
  { id: "instructor", label: "Giảng viên" },
  { id: "tro_giang", label: "Trợ giảng" },
];

export default function StaffInvitePanel() {
  const toast = useToast();
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [invites, setInvites] = useState<StaffInvite[] | null>(null);
  const [busy, setBusy] = useState(false);

  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState<StaffInviteRole>("instructor");
  const [adminArea, setAdminArea] = useState<"" | "thpt" | "cttc">("thpt");
  const [classId, setClassId] = useState<string>("");
  const [tier, setTier] = useState<"B1" | "B2" | "B3">("B1");

  const reload = useCallback(() => {
    fetchStaffInvites().then(setInvites).catch(() => setInvites([]));
  }, []);

  useEffect(() => {
    fetchClasses()
      .then((rows) => setClasses(displayClassesByGrade(rows)))
      .catch(() => setClasses([]));
    reload();
  }, [reload]);

  async function submit() {
    if (!email.trim() || !fullName.trim()) {
      toast("error", "Nhập đủ email và họ tên.");
      return;
    }
    setBusy(true);
    try {
      const result = await inviteStaff({
        email: email.trim(),
        fullName: fullName.trim(),
        role,
        adminArea: role === "instructor" && adminArea ? adminArea : null,
        classId: classId ? Number(classId) : null,
        tier: role === "tro_giang" ? tier : null,
      });
      toast(
        "success",
        result.status === "invited"
          ? "Đã gửi email mời đặt mật khẩu."
          : "Email này đã có tài khoản — đã cấp quyền và phân công ngay.",
      );
      setEmail("");
      setFullName("");
      reload();
    } catch (error) {
      toast(
        "error",
        errorMessage(error, "Chưa mời được — kiểm tra Edge Function invite-staff đã deploy chưa."),
      );
    } finally {
      setBusy(false);
    }
  }

  async function revoke(id: string) {
    setBusy(true);
    try {
      await revokeStaffInvite(id);
      toast("success", "Đã huỷ lời mời.");
      reload();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa huỷ được."));
    } finally {
      setBusy(false);
    }
  }

  const className = (id: number | null) =>
    id ? (classes.find((c) => c.id === id)?.name ?? `Lớp #${id}`) : null;

  return (
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
      <h3 className="flex items-center gap-2 font-semibold text-white">
        <Mail size={17} className="text-sky-300" />
        Mời người mới qua email
      </h3>
      <p className="mt-1 text-sm text-slate-400">
        Người chưa có tài khoản sẽ nhận email đặt mật khẩu; đăng nhập xong là có sẵn quyền và lớp được phân công.
      </p>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="email"
          placeholder="email@example.com"
          className="rounded-xl border border-white/10 bg-white/5 px-3 py-2.5 text-sm text-white placeholder:text-slate-500"
        />
        <input
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="Họ và tên"
          className="rounded-xl border border-white/10 bg-white/5 px-3 py-2.5 text-sm text-white placeholder:text-slate-500"
        />
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        {ROLES.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => setRole(item.id)}
            className={`rounded-xl px-4 py-2 text-sm font-bold transition ${
              role === item.id ? "bg-[#2563EB] text-white" : "bg-white/5 text-slate-300 hover:bg-white/10"
            }`}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className="mt-3 grid gap-3 sm:grid-cols-2">
        {role === "instructor" ? (
          <label className="text-sm text-slate-300">
            Khu vực quản trị
            <select
              value={adminArea}
              onChange={(e) => setAdminArea(e.target.value as "" | "thpt" | "cttc")}
              className="mt-1 w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2.5 text-sm text-white"
            >
              <option value="thpt">THPT</option>
              <option value="cttc">CTTC</option>
              <option value="">Không cấp khu vực</option>
            </select>
          </label>
        ) : (
          <label className="text-sm text-slate-300">
            Bậc trợ giảng
            <select
              value={tier}
              onChange={(e) => setTier(e.target.value as "B1" | "B2" | "B3")}
              className="mt-1 w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2.5 text-sm text-white"
            >
              <option value="B1">B1</option>
              <option value="B2">B2</option>
              <option value="B3">B3</option>
            </select>
          </label>
        )}

        <label className="text-sm text-slate-300">
          Lớp phụ trách {role === "instructor" ? "(không bắt buộc)" : ""}
          <select
            value={classId}
            onChange={(e) => setClassId(e.target.value)}
            className="mt-1 w-full rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2.5 text-sm text-white"
          >
            <option value="">Chưa gán lớp</option>
            {classes.map((schoolClass) => (
              <option key={schoolClass.id} value={schoolClass.id}>
                {schoolClass.name}
              </option>
            ))}
          </select>
        </label>
      </div>

      <button
        type="button"
        disabled={busy}
        onClick={submit}
        className="mt-4 inline-flex items-center gap-2 rounded-xl bg-[#2563EB] px-5 py-2.5 text-sm font-bold text-white disabled:opacity-40"
      >
        <Mail size={15} />
        Gửi lời mời
      </button>

      <div className="mt-5 border-t border-white/10 pt-4">
        <p className="text-xs font-bold uppercase tracking-wide text-slate-500">Lời mời gần đây</p>
        {invites === null ? (
          <p className="mt-2 text-sm text-slate-400">Đang tải…</p>
        ) : invites.length === 0 ? (
          <p className="mt-2 text-sm text-slate-400">Chưa mời ai qua email.</p>
        ) : (
          <div className="mt-2 space-y-2">
            {invites.map((invite) => (
              <article key={invite.id} className="flex items-center gap-3 rounded-xl border border-white/5 p-3">
                <span
                  className={`grid h-8 w-8 shrink-0 place-items-center rounded-full ${
                    invite.claimed_at ? "bg-emerald-500/15 text-emerald-300" : "bg-amber-500/15 text-amber-300"
                  }`}
                >
                  {invite.claimed_at ? <Check size={15} /> : <Clock3 size={15} />}
                </span>
                <div className="min-w-0 flex-1">
                  <strong className="block truncate text-sm text-white">
                    {invite.full_name || invite.email}
                  </strong>
                  <small className="text-slate-400">
                    {invite.email} · {invite.role === "instructor" ? "Giảng viên" : `Trợ giảng ${invite.tier ?? ""}`}
                    {className(invite.class_id) ? ` · ${className(invite.class_id)}` : ""}
                  </small>
                </div>
                <span className="shrink-0 text-xs font-semibold text-slate-400">
                  {invite.claimed_at ? "Đã nhận" : "Chờ nhận"}
                </span>
                {!invite.claimed_at && (
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => void revoke(invite.id)}
                    className="shrink-0 rounded-full bg-red-500/15 px-3 py-1.5 text-xs font-bold text-red-200 disabled:opacity-40"
                  >
                    <X size={13} />
                  </button>
                )}
              </article>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
