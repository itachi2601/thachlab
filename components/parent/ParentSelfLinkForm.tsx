"use client";

import { useState } from "react";
import { CheckCircle2, Link2, MessageCircle, Send } from "lucide-react";
import { CONTACT } from "@/lib/contact";
import { claimParentByChildInfo, requestParentLinkReview, type SelfLinkResult } from "@/services/parent-links";

/**
 * Phụ huynh tự nối với con (thầy duyệt 15/10/2026) — khớp ĐỦ họ tên con + ngày sinh con + SĐT phụ huynh đã
 * khai lúc đăng ký học. Không dùng riêng tên + ngày sinh (bạn cùng lớp biết sinh nhật nhau) hay SĐT của con.
 * Lớp bảo vệ chính là THÔNG BÁO: nối xong, thầy và con đều nhận tin, người lạ nối được thì gỡ ngay.
 * Sai không nói sai ô nào (tránh dò từng ô); sai 5 lần/24 giờ thì khoá. Không khớp → gửi yêu cầu thầy duyệt.
 * Giao diện theo bộ P: ô nhập ≥48px, nhãn trên ô, ngày sinh 3 ô số (quen hơn lịch chọn ngày ở tuổi 45–60, P4/P8).
 */

const input =
  "mt-1 block w-full rounded-xl border border-line-strong bg-panel px-4 py-3 text-ink focus:border-primary focus:outline-none";

function toIsoDate(d: string, m: string, y: string): string | null {
  const dd = Number(d);
  const mm = Number(m);
  const yy = Number(y);
  if (!dd || !mm || !yy || yy < 1990 || yy > 2030 || mm > 12 || dd > 31) return null;
  const date = new Date(Date.UTC(yy, mm - 1, dd));
  if (date.getUTCMonth() !== mm - 1) return null;
  return `${yy}-${String(mm).padStart(2, "0")}-${String(dd).padStart(2, "0")}`;
}

export default function ParentSelfLinkForm({ onLinked }: { onLinked: () => void }) {
  const [name, setName] = useState("");
  const [day, setDay] = useState("");
  const [month, setMonth] = useState("");
  const [year, setYear] = useState("");
  const [phone, setPhone] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<SelfLinkResult | null>(null);
  const [requested, setRequested] = useState(false);

  const birth = toIsoDate(day, month, year);
  const phoneDigits = phone.replace(/\D/g, "");
  const ready = name.trim().split(/\s+/).length >= 2 && birth !== null && phoneDigits.length >= 9;

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!ready || !birth) return;
    setBusy(true);
    setError(null);
    try {
      const r = await claimParentByChildInfo(name, birth, phone);
      setResult(r);
      if (r.status === "linked" || r.status === "already") setTimeout(onLinked, 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Chưa kiểm tra được thông tin.");
    } finally {
      setBusy(false);
    }
  }

  async function sendRequest() {
    setBusy(true);
    setError(null);
    try {
      await requestParentLinkReview(name, birth ?? "", phone, note);
      setRequested(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Chưa gửi được yêu cầu.");
    } finally {
      setBusy(false);
    }
  }

  if (result && (result.status === "linked" || result.status === "already")) {
    return (
      <div className="rounded-2xl border border-ok/30 bg-ok/10 p-5 text-ink" role="status">
        <CheckCircle2 className="text-ok" size={28} aria-hidden />
        <p className="mt-2 font-display text-lg font-bold">
          Đã nối với {result.studentName ?? "con"}
          {result.className ? ` · lớp ${result.className}` : ""}.
        </p>
        <p className="mt-1">Đang mở kết quả học tập của con…</p>
      </div>
    );
  }

  if (requested) {
    return (
      <div className="rounded-2xl border border-primary/30 bg-primary/5 p-5 text-ink" role="status">
        <Send className="text-primary" size={24} aria-hidden />
        <p className="mt-2 font-display text-lg font-bold">Đã gửi yêu cầu cho thầy</p>
        <p className="mt-1">
          Thầy xem và xác nhận trong ngày. Khi xong, phụ huynh nhận thông báo ở biểu tượng chuông, rồi vào lại trang này là
          thấy kết quả của con.
        </p>
      </div>
    );
  }

  const failed = result?.status === "no_match" || result?.status === "locked";

  return (
    <form onSubmit={submit} className="rounded-2xl border border-line bg-panel p-5 text-left" noValidate>
      <div className="flex items-center gap-2">
        <Link2 size={22} className="text-primary" aria-hidden />
        <h2 className="font-display text-lg font-bold text-ink">Tự nối với con</h2>
      </div>
      <p className="parent-copy mt-2 text-muted">
        Điền đúng ba thông tin như lúc đăng ký học cho con. Nối xong, thầy và con đều nhận được thông báo.
      </p>

      {result?.status !== "locked" && (
        <div className="mt-4 space-y-4">
          <label className="block">
            <span className="font-semibold text-ink">Họ và tên của con</span>
            <input
              className={input}
              value={name}
              onChange={(e) => setName(e.target.value)}
              autoComplete="off"
              placeholder="Ví dụ: Nguyễn Minh An"
            />
          </label>

          <fieldset>
            <legend className="font-semibold text-ink">Ngày sinh của con</legend>
            <div className="mt-1 grid grid-cols-[1fr_1fr_1.4fr] gap-2">
              {(
                [
                  ["Ngày", day, setDay, 2],
                  ["Tháng", month, setMonth, 2],
                  ["Năm", year, setYear, 4],
                ] as const
              ).map(([label, value, set, max]) => (
                <label key={label} className="block">
                  <span className="text-[15px] text-muted">{label}</span>
                  <input
                    className={`${input} mt-0.5 text-center tabular-nums`}
                    inputMode="numeric"
                    maxLength={max}
                    value={value}
                    onChange={(e) => set(e.target.value.replace(/\D/g, ""))}
                    placeholder={label === "Năm" ? "2009" : label === "Ngày" ? "15" : "8"}
                  />
                </label>
              ))}
            </div>
          </fieldset>

          <label className="block">
            <span className="font-semibold text-ink">Số điện thoại của phụ huynh</span>
            <span className="block text-[15px] text-muted">Số đã ghi khi đăng ký học cho con</span>
            <input
              className={input}
              type="tel"
              inputMode="tel"
              autoComplete="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="09xx xxx xxx"
            />
          </label>

          <button
            type="submit"
            disabled={!ready || busy}
            className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-5 py-3 font-semibold text-white hover:bg-primary-dark disabled:opacity-50 sm:w-auto"
          >
            <Link2 size={18} /> {busy ? "Đang kiểm tra…" : "Nối với con"}
          </button>
        </div>
      )}

      {error && (
        <p className="mt-3 text-danger" role="alert">
          {error}
        </p>
      )}

      {failed && (
        <div className="mt-5 rounded-xl border border-warn/30 bg-warn/10 p-4 text-ink" role="alert">
          {result?.status === "locked" ? (
            <p>
              Thông tin chưa khớp 5 lần trong 24 giờ nên tạm khoá việc tự nối. Phụ huynh gửi yêu cầu để thầy xác nhận,
              hoặc nhắn Zalo cho thầy.
            </p>
          ) : (
            <p>
              Thông tin chưa khớp với hồ sơ đăng ký học. Phụ huynh xem lại cách viết họ tên, ngày sinh, và số điện
              thoại đã ghi khi đăng ký. Nếu vẫn chưa được, gửi yêu cầu để thầy xác nhận.
            </p>
          )}
          <label className="mt-3 block">
            <span className="text-[15px] text-muted">Lời nhắn cho thầy (không bắt buộc)</span>
            <input
              className={input}
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="Ví dụ: con học lớp 11 buổi tối thứ Ba"
            />
          </label>
          <div className="mt-3 flex flex-wrap gap-3">
            <button
              type="button"
              onClick={sendRequest}
              disabled={busy || name.trim() === "" || phoneDigits.length < 9}
              className="inline-flex items-center gap-2 rounded-xl bg-primary px-5 py-3 font-semibold text-white hover:bg-primary-dark disabled:opacity-50"
            >
              <Send size={18} /> Gửi yêu cầu cho thầy
            </button>
            {CONTACT.zalo && (
              <a
                href={CONTACT.zalo}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-xl border border-line px-5 py-3 font-semibold text-ink hover:border-line-strong"
              >
                <MessageCircle size={18} /> Nhắn Zalo
              </a>
            )}
          </div>
        </div>
      )}
    </form>
  );
}
