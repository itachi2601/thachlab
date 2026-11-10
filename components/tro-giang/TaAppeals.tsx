"use client";

import { useCallback, useEffect, useState } from "react";
import { useToast } from "@/components/ui/Toast";
import { fetchAppeals, resolveAppeal, submitAppeal, type TaAppeal } from "@/lib/tro-giang/queries";

const cls = "mt-1 w-full rounded-xl border border-white/15 bg-white/5 px-3 py-2.5 text-white";
const when = (iso: string) =>
  new Date(iso).toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit", timeZone: "Asia/Ho_Chi_Minh" });

/** Khiếu nại công tháng: trợ giảng gửi trong đợt xem lại (canSubmit), thầy trả lời (admin). */
export default function TaAppeals({ assistantId, month, canSubmit, admin }: { assistantId: string; month: string; canSubmit?: boolean; admin?: boolean }) {
  const toast = useToast();
  const [items, setItems] = useState<TaAppeal[] | null>(null);
  const [body, setBody] = useState("");
  const [replies, setReplies] = useState<Record<number, string>>({});
  const [busy, setBusy] = useState(false);

  const load = useCallback(() => {
    fetchAppeals(assistantId, month).then(setItems).catch(() => setItems([]));
  }, [assistantId, month]);
  useEffect(load, [load]);

  async function send() {
    if (!body.trim()) return;
    setBusy(true);
    try {
      await submitAppeal(month, body);
      setBody("");
      toast("success", "Đã gửi khiếu nại cho thầy.");
      load();
    } catch (e) {
      toast("error", (e as { message?: string })?.message ?? "Không gửi được");
    } finally {
      setBusy(false);
    }
  }

  async function resolve(id: number) {
    setBusy(true);
    try {
      await resolveAppeal(id, replies[id] ?? "");
      toast("success", "Đã trả lời, trợ giảng nhận thông báo.");
      load();
    } catch (e) {
      toast("error", (e as { message?: string })?.message ?? "Không lưu được");
    } finally {
      setBusy(false);
    }
  }

  if (!items || (!items.length && !canSubmit)) return null;
  return (
    <section className="space-y-3 rounded-2xl border border-white/10 p-4">
      <h3 className="font-semibold text-white">Khiếu nại công tháng {month.slice(5, 7)}/{month.slice(0, 4)}</h3>
      {items.map((a) => (
        <div key={a.id} className="rounded-xl bg-white/5 p-3 text-sm">
          <p className="whitespace-pre-line text-white">{a.body}</p>
          <p className="mt-1 text-xs text-slate-400">Gửi {when(a.created_at)}</p>
          {a.resolved_at ? (
            <p className="mt-2 text-emerald-300">Thầy: {a.reply ?? "Đã xem."}</p>
          ) : admin ? (
            <div className="mt-2 flex flex-col gap-2 sm:flex-row">
              <input className={cls} placeholder="Trả lời (tuỳ chọn)" value={replies[a.id] ?? ""} onChange={(e) => setReplies({ ...replies, [a.id]: e.target.value })} />
              <button type="button" disabled={busy} onClick={() => resolve(a.id)} className="min-h-11 shrink-0 rounded-xl bg-blue-600 px-4 text-sm font-semibold text-white disabled:opacity-50">
                Đã xử lý
              </button>
            </div>
          ) : (
            <p className="mt-2 text-amber-300">Chờ thầy xem</p>
          )}
        </div>
      ))}
      {canSubmit && (
        <div>
          <label className="block text-sm text-slate-300">
            Thắc mắc về công tháng này (buổi nào, sai chỗ nào)
            <textarea className={cls} rows={3} maxLength={2000} value={body} onChange={(e) => setBody(e.target.value)} />
          </label>
          <button type="button" disabled={busy || !body.trim()} onClick={send} className="mt-2 min-h-11 rounded-xl bg-blue-600 px-5 text-sm font-semibold text-white disabled:opacity-50">
            Gửi khiếu nại
          </button>
        </div>
      )}
    </section>
  );
}
