"use client";

import { useCallback, useEffect, useState } from "react";
import { Check, Clock3, Copy, Link2, Trash2, UserPlus } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { SITE_URL } from "@/lib/site";
import {
  createParentLink,
  fetchParentLinksForStudent,
  removeParentLink,
  type ParentLink,
} from "@/services/parent-links";

function errorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

function inviteLink(code: string) {
  return `${SITE_URL}/loi-moi?ma=${code}`;
}

/**
 * Thẻ "Phụ huynh" trong hồ sơ một học sinh (dashboard THPT): tạo mã, chép link gửi Zalo,
 * thấy phụ huynh nào đã nối, gỡ khi cần. Mỗi mã dùng cho một phụ huynh; bố và mẹ cùng
 * xem thì tạo hai mã.
 */
export default function ParentLinkCard({ studentId, studentName }: { studentId: string; studentName: string }) {
  const toast = useToast();
  const [links, setLinks] = useState<ParentLink[] | null>(null);
  const [label, setLabel] = useState("");
  const [busy, setBusy] = useState(false);

  const reload = useCallback(() => {
    fetchParentLinksForStudent(studentId)
      .then(setLinks)
      .catch(() => setLinks([]));
  }, [studentId]);

  // Đổi học sinh -> hồ sơ truyền key={studentId} nên component dựng lại, state tự về đầu.
  useEffect(() => {
    reload();
  }, [reload]);

  async function copy(text: string, what: string) {
    try {
      await navigator.clipboard.writeText(text);
      toast("success", `Đã chép ${what}.`);
    } catch {
      toast("error", "Trình duyệt không cho chép tự động — bôi đen rồi chép tay nhé.");
    }
  }

  async function create() {
    setBusy(true);
    try {
      const link = await createParentLink(studentId, label);
      setLabel("");
      reload();
      await copy(inviteLink(link.code), "link cho phụ huynh");
    } catch (error) {
      toast("error", errorMessage(error, "Chưa tạo được mã phụ huynh."));
    } finally {
      setBusy(false);
    }
  }

  async function remove(link: ParentLink) {
    const question = link.claimed_at
      ? `Gỡ liên kết này? Phụ huynh sẽ không xem được kết quả của ${studentName} nữa.`
      : `Huỷ mã ${link.code}?`;
    if (!window.confirm(question)) return;
    try {
      await removeParentLink(link.id);
      reload();
      toast("success", link.claimed_at ? "Đã gỡ liên kết." : "Đã huỷ mã.");
    } catch (error) {
      toast("error", errorMessage(error, "Chưa gỡ được."));
    }
  }

  const claimed = (links ?? []).filter((l) => l.claimed_at);
  const pending = (links ?? []).filter((l) => !l.claimed_at);

  return (
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h4 className="font-display text-lg font-bold text-white">Phụ huynh</h4>
        <span className="text-xs text-slate-500">
          {claimed.length > 0 ? `${claimed.length} phụ huynh đang theo dõi` : "Chưa có phụ huynh nào nối"}
        </span>
      </div>
      <p className="mt-1 text-sm text-slate-400">
        Tạo mã, gửi link qua Zalo. Phụ huynh mở link, tạo tài khoản là xem được điểm, chủ đề còn yếu
        và tình hình phụ đạo của em — chỉ xem, không sửa được gì.
      </p>

      <div className="mt-4 flex flex-wrap gap-2">
        <input
          value={label}
          onChange={(e) => setLabel(e.target.value)}
          placeholder="Ghi nhớ (Mẹ / Bố / tên…) — không bắt buộc"
          className="min-w-0 flex-1 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none"
        />
        <button
          type="button"
          onClick={create}
          disabled={busy}
          className="inline-flex items-center gap-2 rounded-xl bg-[#2563EB] px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
        >
          <UserPlus size={15} /> {busy ? "Đang tạo…" : "Tạo mã & chép link"}
        </button>
      </div>

      {links === null ? (
        <p className="mt-4 text-sm text-slate-500">Đang tải…</p>
      ) : links.length === 0 ? null : (
        <ul className="mt-4 space-y-2">
          {[...claimed, ...pending].map((link) => (
            <li
              key={link.id}
              className="flex flex-wrap items-center gap-3 rounded-xl border border-white/10 bg-white/[.02] px-3 py-2.5 text-sm"
            >
              {link.claimed_at ? (
                <Check size={16} className="shrink-0 text-emerald-300" />
              ) : (
                <Clock3 size={16} className="shrink-0 text-amber-300" />
              )}
              <span className="min-w-0 flex-1">
                <span className="font-mono font-bold text-white">{link.code}</span>
                {link.label && <span className="ml-2 text-slate-300">{link.label}</span>}
                <small className="block text-slate-500">
                  {link.claimed_at
                    ? `Đã nối ${new Date(link.claimed_at).toLocaleDateString("vi-VN")}`
                    : `Chưa nhận · tạo ${new Date(link.created_at).toLocaleDateString("vi-VN")}`}
                </small>
              </span>
              {!link.claimed_at && (
                <>
                  <button
                    type="button"
                    onClick={() => copy(link.code, "mã")}
                    title="Chép mã"
                    className="rounded-lg border border-white/10 p-1.5 text-slate-300 hover:border-white/30"
                  >
                    <Copy size={14} />
                  </button>
                  <button
                    type="button"
                    onClick={() => copy(inviteLink(link.code), "link")}
                    title="Chép link"
                    className="rounded-lg border border-white/10 p-1.5 text-slate-300 hover:border-white/30"
                  >
                    <Link2 size={14} />
                  </button>
                </>
              )}
              <button
                type="button"
                onClick={() => remove(link)}
                title={link.claimed_at ? "Gỡ liên kết" : "Huỷ mã"}
                className="rounded-lg border border-red-500/30 p-1.5 text-red-300 hover:bg-red-500/10"
              >
                <Trash2 size={14} />
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
