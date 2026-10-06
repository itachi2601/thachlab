"use client";

import { useEffect, useMemo, useState } from "react";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import type { SchoolClass } from "@/features/exams/types";
import { fetchClasses } from "@/services/classes";
import { fetchCoursesForClass, groupCoursesByPair, type ThptCourse } from "@/services/thpt-courses";
import {
  archiveFeePlan,
  ensureFeeMonth,
  fetchFeeLedger,
  fetchFeePlans,
  fetchFeeVisibility,
  recordFeePayment,
  setFeeVisibility,
  upsertFeePlan,
  waiveFeeCharge,
  type FeeCharge,
  type FeePlan,
  type FeeVisibility,
} from "@/services/tuition";
import { billingKeyOf, chargeState, formatVnd, monthStart, monthTitle, parseAmountVnd, todayVn } from "@/features/tuition/ledger";

const inputCls =
  "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

function errMsg(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

export default function TuitionLedgerAdmin() {
  const [visible, setVisible] = useState<FeeVisibility | null>(null);

  useEffect(() => {
    fetchFeeVisibility()
      .then(setVisible)
      .catch(() => setVisible({ staffVisible: false, familyVisible: false }));
  }, []);

  if (!visible?.staffVisible) return null;
  return <Ledger visibility={visible} onVisibility={setVisible} />;
}

function Ledger({
  visibility,
  onVisibility,
}: {
  visibility: FeeVisibility;
  onVisibility: (v: FeeVisibility) => void;
}) {
  const toast = useToast();
  const { profile } = useAuth();
  const isAdmin = profile?.role === "admin";
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [classId, setClassId] = useState<number | null>(null);
  const [courses, setCourses] = useState<ThptCourse[]>([]);
  const [plans, setPlans] = useState<FeePlan[]>([]);
  const [period, setPeriod] = useState(() => monthStart(new Date()).slice(0, 7));
  const [charges, setCharges] = useState<FeeCharge[]>([]);
  const [busy, setBusy] = useState(false);
  const [label, setLabel] = useState<string | null>(null);
  const [amount, setAmount] = useState("");
  const [dueDay, setDueDay] = useState("5");
  const [billingKey, setBillingKey] = useState<string | null>(null);

  useEffect(() => {
    fetchClasses()
      .then((rows) => {
        setClasses(rows);
        setClassId((cur) => cur ?? rows[0]?.id ?? null);
      })
      .catch((e) => toast("error", errMsg(e, "Chưa đọc được danh sách lớp")));
  }, [toast]);

  const groups = useMemo(() => {
    return groupCoursesByPair(courses).map((g) => {
      const first = g.courses[0];
      const key = billingKeyOf(first);
      return {
        key,
        label: g.pairKey ?? first.name,
        hint: g.courses.map((c) => c.name).join(" · "),
      };
    });
  }, [courses]);

  const activeKey = billingKey ?? groups[0]?.key ?? "";
  const activeLabel = label ?? groups.find((g) => g.key === activeKey)?.label ?? "";

  function reload(id: number, month: string) {
    return Promise.all([
      fetchCoursesForClass(id),
      fetchFeePlans(id),
      fetchFeeLedger(id, `${month}-01`),
    ]).then(([courseRows, planRows, ledger]) => {
      setCourses(courseRows);
      setPlans(planRows);
      setCharges(ledger);
    });
  }

  useEffect(() => {
    if (classId === null) return;
    let cancelled = false;
    Promise.all([
      fetchCoursesForClass(classId),
      fetchFeePlans(classId),
      fetchFeeLedger(classId, `${period}-01`),
    ])
      .then(([courseRows, planRows, ledger]) => {
        if (cancelled) return;
        setCourses(courseRows);
        setPlans(planRows);
        setCharges(ledger);
      })
      .catch((e) => {
        if (!cancelled) toast("error", errMsg(e, "Chưa đọc được sổ"));
      });
    return () => {
      cancelled = true;
    };
  }, [classId, period, toast]);

  async function savePlan() {
    if (classId === null || !activeKey) return;
    const amountVnd = parseAmountVnd(amount);
    const day = Number(dueDay);
    if (amountVnd === null) {
      toast("error", "Số tiền từ 1 đến 20.000.000 đồng");
      return;
    }
    if (!Number.isInteger(day) || day < 1 || day > 28) {
      toast("error", "Ngày hạn từ 1 đến 28");
      return;
    }
    setBusy(true);
    try {
      await upsertFeePlan({ classId, billingKey: activeKey, label: activeLabel.trim(), amountVnd, dueDay: day });
      toast("success", "Đã lưu mức thu");
      await reload(classId, period);
    } catch (e) {
      toast("error", errMsg(e, "Chưa lưu được mức thu"));
    } finally {
      setBusy(false);
    }
  }

  async function createMonth() {
    if (classId === null) return;
    setBusy(true);
    try {
      const n = await ensureFeeMonth(classId, `${period}-01`);
      toast("success", n > 0 ? `Đã thêm ${n} khoản` : "Tháng này đã có đủ khoản");
      setCharges(await fetchFeeLedger(classId, `${period}-01`));
    } catch (e) {
      toast("error", errMsg(e, "Chưa tạo được khoản"));
    } finally {
      setBusy(false);
    }
  }

  function changeMonth(next: string) {
    if (next) setPeriod(next);
  }

  async function toggleFamily(next: boolean) {
    setBusy(true);
    try {
      await setFeeVisibility(true, next);
      onVisibility({ staffVisible: true, familyVisible: next });
      toast("success", next ? "Phụ huynh thấy sổ tháng" : "Phụ huynh không còn thấy sổ tháng");
    } catch (e) {
      toast("error", errMsg(e, "Chưa đổi được"));
    } finally {
      setBusy(false);
    }
  }

  async function hideFromStaff() {
    setBusy(true);
    try {
      await setFeeVisibility(false, false);
      onVisibility({ staffVisible: false, familyVisible: false });
    } catch (e) {
      toast("error", errMsg(e, "Chưa ẩn được"));
      setBusy(false);
    }
  }

  return (
    <div className="admin-stack">
      <section className="admin-card">
        <h2 className="admin-h2">Sổ học phí theo tháng</h2>
        <p className="admin-lead">
          {visibility.familyVisible
            ? "Phụ huynh thấy các tháng đã tạo trên trang Phụ huynh. Học sinh không thấy sổ này."
            : "Phụ huynh và học sinh chưa thấy sổ này. Ô đóng học phí trên trang Phụ huynh vẫn như cũ."}
        </p>
        <div className="mt-4 flex flex-wrap items-end gap-3">
          <label className="text-sm text-slate-300">
            Khối
            <select
              className={`${inputCls} mt-1 block`}
              value={classId ?? ""}
              onChange={(e) => {
                setBillingKey(null);
                setLabel(null);
                setClassId(Number(e.target.value));
              }}
            >
              {classes.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </label>
          {isAdmin && (
            <label className="flex items-center gap-2 pb-2 text-sm text-slate-200">
              <input
                type="checkbox"
                checked={visibility.familyVisible}
                disabled={busy}
                onChange={(e) => void toggleFamily(e.target.checked)}
              />
              Phụ huynh thấy sổ tháng
            </label>
          )}
          {isAdmin && (
            <button type="button" className="admin-btn admin-btn--ghost" disabled={busy} onClick={() => void hideFromStaff()}>
              Ẩn sổ
            </button>
          )}
        </div>
      </section>

      <section className="admin-card">
        <h2 className="admin-h2">Mức thu</h2>
        <p className="admin-lead">Lớp hai buổi chỉ một mức. Khoản đã tạo giữ số tiền lúc tạo.</p>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <label className="text-sm text-slate-300">
            Lớp
            <select
              className={`${inputCls} mt-1 block w-full`}
              value={activeKey}
              onChange={(e) => {
                const g = groups.find((x) => x.key === e.target.value);
                setBillingKey(e.target.value);
                if (g) setLabel(g.label);
              }}
            >
              {groups.map((g) => (
                <option key={g.key} value={g.key}>{g.hint}</option>
              ))}
            </select>
          </label>
          <label className="text-sm text-slate-300">
            Tên trên sổ
            <input className={`${inputCls} mt-1 block w-full`} value={activeLabel} onChange={(e) => setLabel(e.target.value)} />
          </label>
          <label className="text-sm text-slate-300">
            Số tiền mỗi tháng
            <input className={`${inputCls} mt-1 block w-full`} inputMode="numeric" placeholder="800000" value={amount} onChange={(e) => setAmount(e.target.value)} />
          </label>
          <label className="text-sm text-slate-300">
            Hạn trong tháng
            <input className={`${inputCls} mt-1 block w-full`} inputMode="numeric" value={dueDay} onChange={(e) => setDueDay(e.target.value)} />
          </label>
        </div>
        <button type="button" className="admin-btn admin-btn--primary mt-4" disabled={busy || !activeKey} onClick={() => void savePlan()}>
          Lưu mức thu
        </button>
        <ul className="mt-4 space-y-2">
          {plans.map((p) => (
            <li key={p.id} className="flex flex-wrap items-center gap-3 rounded-xl border border-white/10 p-3">
              <span className={`admin-badge ${p.active ? "admin-badge--ok" : ""}`}>{p.active ? "Đang thu" : "Đã ngừng"}</span>
              <span className="min-w-0 flex-1">
                <b>{p.label}</b>
                <span className="admin-muted block">{formatVnd(p.amountVnd)} · hạn ngày {p.dueDay}</span>
              </span>
              {p.active && (
                <button
                  type="button"
                  className="admin-btn admin-btn--sm admin-btn--ghost"
                  disabled={busy}
                  onClick={() => {
                    setBusy(true);
                    archiveFeePlan(p.id)
                      .then(() => (classId !== null ? reload(classId, period) : undefined))
                      .then(() => toast("success", "Đã ngừng mức thu"))
                      .catch((e) => toast("error", errMsg(e, "Chưa ngừng được")))
                      .finally(() => setBusy(false));
                  }}
                >
                  Ngừng
                </button>
              )}
            </li>
          ))}
        </ul>
      </section>

      <section className="admin-card">
        <h2 className="admin-h2">{monthTitle(`${period}-01`)}</h2>
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <input className={inputCls} type="month" value={period} onChange={(e) => void changeMonth(e.target.value)} />
          <button type="button" className="admin-btn admin-btn--primary" disabled={busy} onClick={() => void createMonth()}>
            Tạo khoản của tháng này
          </button>
        </div>
        <p className="admin-muted mt-2">Đăng ký chưa gắn tài khoản không có dòng.</p>
        {charges.length === 0 ? (
          <p className="admin-empty mt-4">Chưa có khoản trong tháng này.</p>
        ) : (
          <ul className="mt-4 space-y-3">
            {charges.map((c) => (
              <ChargeRow
                key={c.chargeId}
                charge={c}
                busy={busy}
                onChanged={async () => {
                  if (classId !== null) setCharges(await fetchFeeLedger(classId, `${period}-01`));
                }}
                onBusy={setBusy}
              />
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

function ChargeRow({
  charge,
  busy,
  onChanged,
  onBusy,
}: {
  charge: FeeCharge;
  busy: boolean;
  onChanged: () => Promise<void>;
  onBusy: (v: boolean) => void;
}) {
  const toast = useToast();
  const state = chargeState(charge.amountVnd, charge.paidVnd, charge.waived);
  const [amount, setAmount] = useState("");
  const [method, setMethod] = useState<"center" | "transfer">("transfer");
  const [paidOn, setPaidOn] = useState(() => todayVn(new Date()));
  const [note, setNote] = useState("");
  const word = state === "paid" ? "Đủ" : state === "waived" ? "Miễn" : "Còn thiếu";

  async function pay() {
    const amountVnd = parseAmountVnd(amount);
    if (amountVnd === null) {
      toast("error", "Số tiền từ 1 đến 20.000.000 đồng");
      return;
    }
    onBusy(true);
    try {
      await recordFeePayment({ chargeId: charge.chargeId, amountVnd, method, paidOn, note });
      setAmount("");
      setNote("");
      toast("success", `Đã ghi ${formatVnd(amountVnd)}`);
      await onChanged();
    } catch (e) {
      toast("error", errMsg(e, "Chưa ghi được khoản đóng"));
    } finally {
      onBusy(false);
    }
  }

  async function waive(next: boolean) {
    onBusy(true);
    try {
      await waiveFeeCharge(charge.chargeId, next);
      toast("success", next ? "Đã miễn tháng này" : "Đã bỏ miễn");
      await onChanged();
    } catch (e) {
      toast("error", errMsg(e, "Chưa đổi được miễn"));
    } finally {
      onBusy(false);
    }
  }

  return (
    <li className="rounded-xl border border-white/10 p-3">
      <div className="flex flex-wrap items-center gap-3">
        <span className={`admin-badge ${state === "paid" ? "admin-badge--ok" : state === "open" ? "admin-badge--warn" : ""}`}>{word}</span>
        <span className="min-w-0 flex-1">
          <b>{charge.studentName}</b>
          <span className="admin-muted block">
            {charge.label} · đã ghi {formatVnd(charge.paidVnd)} / {formatVnd(charge.amountVnd)}
          </span>
        </span>
        <button type="button" className="admin-btn admin-btn--sm admin-btn--ghost" disabled={busy} onClick={() => void waive(!charge.waived)}>
          {charge.waived ? "Bỏ miễn" : "Miễn"}
        </button>
      </div>
      <div className="mt-3 grid gap-2 sm:grid-cols-4">
        <input className={inputCls} inputMode="numeric" placeholder="Số tiền" value={amount} onChange={(e) => setAmount(e.target.value)} aria-label="Số tiền ghi nhận" />
        <select className={inputCls} value={method} onChange={(e) => setMethod(e.target.value as "center" | "transfer")} aria-label="Hình thức">
          <option value="transfer">Chuyển khoản</option>
          <option value="center">Đóng tại trung tâm</option>
        </select>
        <input className={inputCls} type="date" value={paidOn} onChange={(e) => setPaidOn(e.target.value)} aria-label="Ngày đóng" />
        <input className={inputCls} placeholder="Ghi chú" value={note} onChange={(e) => setNote(e.target.value)} aria-label="Ghi chú" />
      </div>
      <button type="button" className="admin-btn admin-btn--sm admin-btn--primary mt-2" disabled={busy} onClick={() => void pay()}>
        Ghi nhận
      </button>
    </li>
  );
}
