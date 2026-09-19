"use client";

import { useCallback, useEffect, useState } from "react";
import { Search, ShieldAlert } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { setInstructorAdminArea } from "@/services/course-instructors";
import {
  ROLE_LABEL,
  searchAccounts,
  setAccountRole,
  type AccountRole,
  type AdminAccount,
  type AssignableRole,
  type TaTier,
} from "@/services/account-roles";

const ROLE_CHOICES: AssignableRole[] = ["student", "tro_giang", "instructor"];
const TIERS: TaTier[] = ["B1", "B2", "B3"];

// Bỏ trống ô tìm kiếm mà vẫn xem được "ai đang là trợ giảng" — đó mới là câu hỏi hay gặp.
const FILTERS: { id: AccountRole | ""; label: string }[] = [
  { id: "tro_giang", label: "Trợ giảng" },
  { id: "instructor", label: "Giảng viên" },
  { id: "admin", label: "Quản trị" },
  { id: "", label: "Tất cả" },
];

function errorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

const chip = (on: boolean) =>
  `rounded-full border px-3 py-1.5 text-xs font-bold transition disabled:opacity-40 ${
    on ? "border-blue-400/50 bg-blue-500/15 text-blue-200" : "border-white/10 text-slate-400 hover:border-white/30"
  }`;

export default function AccountRolePanel({ onChanged }: { onChanged?: () => void }) {
  const toast = useToast();
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState<AccountRole | "">("tro_giang");
  const [rows, setRows] = useState<AdminAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState("");

  const load = useCallback(
    (q: string, role: AccountRole | "") => {
      setLoading(true);
      searchAccounts(q, role || null)
        .then(setRows)
        .catch((error: unknown) => {
          setRows([]);
          toast("error", errorMessage(error, "Không tìm được tài khoản."));
        })
        .finally(() => setLoading(false));
    },
    [toast],
  );

  useEffect(() => {
    const timer = window.setTimeout(() => load(query, filter), query.trim() ? 250 : 0);
    return () => clearTimeout(timer);
  }, [query, filter, load]);

  async function changeRole(account: AdminAccount, role: AssignableRole, tier?: TaTier) {
    setBusyId(account.id);
    try {
      await setAccountRole(account.id, role, tier ?? account.ta_tier ?? "B1");
      setRows((current) =>
        current.map((item) =>
          item.id === account.id
            ? {
                ...item,
                role,
                admin_area: role === "instructor" ? item.admin_area : null,
                ta_tier: role === "tro_giang" ? tier ?? item.ta_tier ?? "B1" : item.ta_tier,
                ta_active: role === "tro_giang",
              }
            : item,
        ),
      );
      onChanged?.();
      toast("success", `${account.full_name} giờ là ${ROLE_LABEL[role].toLowerCase()}.`);
    } catch (error) {
      toast("error", errorMessage(error, "Chưa đổi được vai trò."));
    } finally {
      setBusyId("");
    }
  }

  async function changeArea(account: AdminAccount, area: "thpt" | "cttc" | null) {
    setBusyId(account.id);
    try {
      await setInstructorAdminArea(account.id, area);
      setRows((current) => current.map((item) => (item.id === account.id ? { ...item, admin_area: area } : item)));
      toast("success", area ? `Đã cho vào khu vực ${area === "thpt" ? "THPT" : "CTTC"}.` : "Đã thu hồi quyền quản trị khu vực.");
    } catch (error) {
      toast("error", errorMessage(error, "Chưa đổi được khu vực quản trị."));
    } finally {
      setBusyId("");
    }
  }

  return (
    <section className="rounded-2xl border border-violet-400/15 bg-violet-500/5 p-5">
      <h3 className="font-semibold text-white">Vai trò tài khoản</h3>
      <p className="mt-1 text-xs text-slate-500">
        Một chỗ duy nhất để quyết định tài khoản nào là học sinh, trợ giảng hay giảng viên. Đặt làm trợ giảng là hồ sơ
        trong bảng lương được tạo/bật lại ngay; chuyển về học sinh thì hồ sơ đó ngừng hoạt động nhưng vẫn giữ lịch sử
        giờ công. Tài khoản quản trị chỉ đổi được bằng SQL.
      </p>

      <div className="mt-3 flex flex-wrap gap-2">
        {FILTERS.map((item) => (
          <button key={item.id || "all"} type="button" onClick={() => setFilter(item.id)} className={chip(filter === item.id)}>
            {item.label}
          </button>
        ))}
      </div>

      <div className="mt-3 flex items-center gap-2 rounded-xl border border-white/10 bg-black/15 px-3 py-2">
        <Search size={15} className="text-slate-500" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Tìm theo tên, email, lớp hoặc MSSV…"
          className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500"
        />
      </div>

      <div className="mt-3 space-y-2">
        {loading && <p className="text-sm text-slate-400">Đang tải…</p>}

        {!loading && rows.length === 0 && (
          <p className="text-sm text-slate-400">
            {query.trim() ? "Không có tài khoản nào khớp." : "Chưa có tài khoản nào ở nhóm này."}
          </p>
        )}

        {!loading &&
          rows.map((account) => (
            <article key={account.id} className="rounded-xl border border-white/5 bg-black/15 p-3">
              <div className="flex flex-wrap items-center gap-3">
                <div className="min-w-0 flex-1">
                  <strong className="block truncate text-sm text-white">{account.full_name || "(chưa có tên)"}</strong>
                  <small className="block truncate text-slate-400">
                    {account.email}
                    {account.class_name ? ` · ${account.class_name}` : ""}
                    {account.student_code ? ` · ${account.student_code}` : ""}
                  </small>
                </div>

                {account.role === "admin" ? (
                  <span className="inline-flex items-center gap-1.5 rounded-full border border-amber-400/30 bg-amber-500/10 px-3 py-1.5 text-xs font-bold text-amber-200">
                    <ShieldAlert size={13} />
                    Quản trị
                  </span>
                ) : (
                  <div className="flex flex-wrap gap-1">
                    {ROLE_CHOICES.map((role) => (
                      <button
                        key={role}
                        type="button"
                        disabled={busyId === account.id || account.role === role}
                        onClick={() => void changeRole(account, role)}
                        className={chip(account.role === role)}
                      >
                        {ROLE_LABEL[role]}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {account.role === "tro_giang" && (
                <div className="mt-2 flex items-center gap-2 border-t border-white/5 pt-2">
                  <span className="text-[11px] font-bold uppercase tracking-wide text-slate-500">Bậc</span>
                  {TIERS.map((tier) => (
                    <button
                      key={tier}
                      type="button"
                      disabled={busyId === account.id}
                      onClick={() => void changeRole(account, "tro_giang", tier)}
                      className={chip((account.ta_tier ?? "B1") === tier)}
                    >
                      {tier}
                    </button>
                  ))}
                </div>
              )}

              {account.role === "instructor" && (
                <div className="mt-2 flex flex-wrap items-center gap-2 border-t border-white/5 pt-2">
                  <span className="text-[11px] font-bold uppercase tracking-wide text-slate-500">Khu vực quản trị</span>
                  {([null, "thpt", "cttc"] as const).map((area) => (
                    <button
                      key={area ?? "none"}
                      type="button"
                      disabled={busyId === account.id}
                      onClick={() => void changeArea(account, area)}
                      className={chip(account.admin_area === area)}
                    >
                      {area === null ? "Không vào /quan-tri" : area === "thpt" ? "THPT" : "CTTC"}
                    </button>
                  ))}
                </div>
              )}
            </article>
          ))}
      </div>
    </section>
  );
}
