"use client";

import { useEffect, useState } from "react";
import { Check, Search, UserPlus, X } from "lucide-react";
import {
  fetchPendingParentLinkRequests,
  reviewParentLinkRequest,
  searchStudentsForLink,
  type LinkStudentOption,
  type ParentLinkRequest,
} from "@/services/parent-links";

/**
 * Yêu cầu "phụ huynh xin nối với con" chưa khớp tự động (request_parent_link_review) — hiện ở đầu
 * /dashboard-thpt, không có yêu cầu nào thì không render gì. Đã đoán được em (tên + ngày sinh) thì duyệt
 * một chạm; chưa đoán được thì tìm em theo tên rồi duyệt. RLS: giáo viên chỉ thấy yêu cầu của em mình dạy.
 */

function vnDate(iso: string | null) {
  if (!iso) return "—";
  const [y, m, d] = iso.slice(0, 10).split("-");
  return `${d}/${m}/${y}`;
}

function RequestRow({ req, onDone }: { req: ParentLinkRequest; onDone: () => void }) {
  const [picked, setPicked] = useState<LinkStudentOption | null>(null);
  const [query, setQuery] = useState(req.child_name);
  const [options, setOptions] = useState<LinkStudentOption[] | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const studentId = picked?.id ?? req.matched_student_id;
  const studentLabel = picked
    ? `${picked.full_name}${picked.class_name ? ` · ${picked.class_name}` : ""}`
    : req.matched
      ? `${req.matched.full_name ?? ""}${req.matched.class_name ? ` · ${req.matched.class_name}` : ""}`
      : null;

  async function search() {
    setError(null);
    try {
      setOptions(await searchStudentsForLink(query));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Chưa tìm được.");
    }
  }

  async function review(approve: boolean) {
    setBusy(true);
    setError(null);
    try {
      await reviewParentLinkRequest(req.id, approve ? studentId : req.matched_student_id, approve);
      onDone();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Chưa xử lý được.");
      setBusy(false);
    }
  }

  return (
    <li className="rounded-xl border border-line bg-surface-2 p-4">
      <p className="text-sm text-ink">
        <b>{req.parent?.full_name || "Phụ huynh"}</b> xin nối với <b>{req.child_name}</b> (sinh {vnDate(req.child_birth)})
      </p>
      <p className="mt-0.5 text-[13px] text-muted">
        SĐT khai: {req.parent_phone} · gửi {vnDate(req.created_at)}
        {req.note ? ` · “${req.note}”` : ""}
      </p>

      {studentLabel ? (
        <p className="mt-2 text-sm text-ink">
          Nối với: <b>{studentLabel}</b>
          {!picked && req.matched && <span className="text-muted"> (đoán theo tên + ngày sinh)</span>}
        </p>
      ) : (
        <p className="mt-2 text-sm text-warn">Chưa đoán được em nào — tìm em theo tên rồi chọn.</p>
      )}

      <div className="mt-2 flex flex-wrap gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="min-h-11 min-w-0 flex-1 rounded-lg border border-line bg-panel px-3 text-sm text-ink"
          aria-label="Tìm học sinh theo tên"
        />
        <button type="button" onClick={search} className="inline-flex min-h-11 items-center gap-1 rounded-lg border border-line px-3 text-sm text-ink">
          <Search size={14} /> Tìm em khác
        </button>
      </div>
      {options && (
        <ul className="mt-2 space-y-1">
          {options.length === 0 && <li className="text-[13px] text-muted">Không thấy em nào.</li>}
          {options.map((o) => (
            <li key={o.id}>
              <button
                type="button"
                onClick={() => setPicked(o)}
                className={`w-full rounded-lg border px-3 py-2 text-left text-sm ${picked?.id === o.id ? "border-primary text-ink" : "border-line text-ink"}`}
              >
                {o.full_name}
                <span className="text-muted">
                  {o.class_name ? ` · ${o.class_name}` : ""} · sinh {vnDate(o.birth_date)}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}

      <div className="mt-3 flex flex-wrap gap-2">
        <button
          type="button"
          disabled={busy || !studentId}
          onClick={() => review(true)}
          className="inline-flex min-h-11 items-center gap-1 rounded-lg bg-primary px-4 text-sm font-semibold text-white disabled:opacity-40"
        >
          <Check size={16} /> Duyệt nối
        </button>
        <button
          type="button"
          disabled={busy}
          onClick={() => review(false)}
          className="inline-flex min-h-11 items-center gap-1 rounded-lg border border-line px-4 text-sm text-ink disabled:opacity-40"
        >
          <X size={16} /> Từ chối
        </button>
      </div>
      {error && <p className="mt-2 text-[13px] text-danger">{error}</p>}
    </li>
  );
}

export default function ParentLinkRequestsPanel() {
  const [items, setItems] = useState<ParentLinkRequest[]>([]);
  const [reload, setReload] = useState(0);

  useEffect(() => {
    let cancelled = false;
    // Bảng chưa có (migration chưa chạy) hay lỗi quyền → im lặng, không chắn dashboard.
    fetchPendingParentLinkRequests()
      .then((rows) => !cancelled && setItems(rows))
      .catch(() => !cancelled && setItems([]));
    return () => {
      cancelled = true;
    };
  }, [reload]);

  if (items.length === 0) return null;
  return (
    <section className="rounded-2xl border border-primary/30 bg-panel p-4 sm:p-5">
      <div className="flex items-center gap-2">
        <UserPlus size={18} className="text-primary" />
        <h2 className="font-display font-semibold text-ink">Phụ huynh xin nối với con ({items.length})</h2>
      </div>
      <p className="mt-1 text-[13px] text-muted">
        Thông tin chưa khớp hồ sơ đăng ký nên chưa tự nối. Kiểm tên, ngày sinh, SĐT rồi duyệt — phụ huynh và em đều nhận thông báo.
      </p>
      <ul className="mt-3 space-y-3">
        {items.map((r) => (
          <RequestRow key={r.id} req={r} onDone={() => setReload((n) => n + 1)} />
        ))}
      </ul>
    </section>
  );
}
