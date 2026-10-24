"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { CONTACT } from "@/lib/contact";
import { supabaseConfigured } from "@/lib/supabase-env";
import { restRpc } from "@/lib/supabase-rest";

// Khối "Kết quả đo được" + "Đăng ký học thử" của /gioi-thieu (T1, GĐ 0 tuyển sinh riêng).
// Trang công khai, không có AuthProvider → chỉ dùng lib/supabase-rest (fetch thuần), không kéo supabase-js (QUY-TAC-THIET-KE-PHU-HUYNH P1, P4, P6, P10).
// Số liệu đọc 1 lần từ get_public_stats() (bảng cache tính hằng ngày) ở client — không round-trip lúc render và không đụng trang chủ.

interface PublicStats {
  computed_at?: string;
  active_students_by_grade?: { g10?: number; g11?: number; g12?: number };
  attempts_90d?: number;
  weekly_active_rate?: number | null;
  avg_improvement?: number | null;
}

const EVENINGS = [
  { v: "t2", l: "Thứ 2" },
  { v: "t3", l: "Thứ 3" },
  { v: "t4", l: "Thứ 4" },
  { v: "t5", l: "Thứ 5" },
  { v: "t6", l: "Thứ 6" },
  { v: "t7", l: "Thứ 7" },
  { v: "cn", l: "Chủ nhật" },
];

const ERRORS: Record<string, string> = {
  invalid_name: "Anh/chị nhập giúp họ tên (ít nhất 2 chữ).",
  invalid_phone: "Số điện thoại cần đủ 10 số, bắt đầu bằng 0.",
  invalid_grade: "Anh/chị chọn giúp khối lớp của con.",
  rate_limited: "Số này đã gửi nhiều lần hôm nay. Anh/chị gọi hoặc nhắn Zalo cho thầy giúp ạ.",
};

function errorText(e: unknown): string {
  const msg = e instanceof Error ? e.message : "";
  for (const k of Object.keys(ERRORS)) if (msg.includes(k)) return ERRORS[k];
  return "Chưa gửi được. Anh/chị thử lại hoặc nhắn Zalo cho thầy giúp ạ.";
}

function StatBox({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-2xl border border-line bg-panel p-5">
      <p className="font-display text-3xl font-bold tabular-nums text-ink">{value}</p>
      <p className="mt-1 text-base text-muted">{label}</p>
    </div>
  );
}

function Stats() {
  const [stats, setStats] = useState<PublicStats | null>(null);
  useEffect(() => {
    if (!supabaseConfigured) return;
    let alive = true;
    restRpc("get_public_stats", {})
      .then((r) => alive && setStats((r as PublicStats | null) ?? null))
      .catch(() => {});
    return () => {
      alive = false;
    };
  }, []);

  if (!stats) return null;
  const g = stats.active_students_by_grade ?? {};
  const total = (g.g10 ?? 0) + (g.g11 ?? 0) + (g.g12 ?? 0);
  const boxes: { value: string; label: string }[] = [];
  if (total > 0) boxes.push({ value: String(total), label: "em đang học đều trên ThachLab (lớp 10–12)" });
  if ((stats.attempts_90d ?? 0) > 0) boxes.push({ value: String(stats.attempts_90d), label: "bài kiểm tra, đề luyện đã nộp trong 90 ngày qua" });
  if (stats.weekly_active_rate != null) boxes.push({ value: `${stats.weekly_active_rate}%`, label: "số em làm bài ít nhất một lần trong tuần qua" });
  if (stats.avg_improvement != null && stats.avg_improvement > 0)
    boxes.push({ value: `+${String(stats.avg_improvement).replace(".", ",")}`, label: "điểm trung bình, bài gần nhất so với bài đầu tiên (thang 10)" });
  if (boxes.length === 0) return null;

  return (
    <div className="mt-8">
      <div className="grid gap-4 sm:grid-cols-2">
        {boxes.map((b) => (
          <StatBox key={b.label} {...b} />
        ))}
      </div>
      <p className="mt-3 text-[.9375rem] text-muted">
        Số liệu gộp từ các em đang học, không nêu tên, cập nhật mỗi ngày. Đây là con số đo được, không phải lời hứa về điểm.
      </p>
    </div>
  );
}

function TrialForm() {
  const [parentName, setParentName] = useState("");
  const [phone, setPhone] = useState("");
  const [grade, setGrade] = useState("");
  const [school, setSchool] = useState("");
  const [evenings, setEvenings] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  function toggle(v: string) {
    setEvenings((cur) => (cur.includes(v) ? cur.filter((x) => x !== v) : [...cur, v]));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (busy) return;
    setBusy(true);
    setError(null);
    try {
      let source = "web";
      try {
        const ref = new URLSearchParams(window.location.search).get("ref");
        if (ref) source = `ref:${ref}`.slice(0, 60);
      } catch {
        /* bỏ qua */
      }
      await restRpc("submit_trial_request", {
        p: { parent_name: parentName, phone, grade: Number(grade), school, preferred_evenings: evenings, source },
      });
      setDone(true);
    } catch (err) {
      setError(errorText(err));
    } finally {
      setBusy(false);
    }
  }

  if (done) {
    return (
      <div role="status" className="rounded-2xl border border-line bg-panel p-6">
        <p className="font-display text-2xl font-bold text-ink">Đã nhận đăng ký</p>
        <p className="mt-2 text-lg text-ink">Thầy sẽ gọi lại trong 24 giờ.</p>
        {CONTACT.zalo && (
          <a
            href={CONTACT.zalo}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-flex min-h-12 items-center rounded-xl border border-line px-5 text-lg font-semibold text-primary"
          >
            Nhắn Zalo cho thầy
          </a>
        )}
      </div>
    );
  }

  const field = "mt-1 block min-h-12 w-full rounded-xl border border-line bg-bg px-4 text-lg text-ink";
  return (
    <form onSubmit={submit} className="space-y-5 rounded-2xl border border-line bg-panel p-6">
      <label className="block text-lg font-medium text-ink">
        Họ tên phụ huynh
        <input className={field} value={parentName} onChange={(e) => setParentName(e.target.value)} required maxLength={80} autoComplete="name" />
      </label>
      <label className="block text-lg font-medium text-ink">
        Số điện thoại
        <input
          className={field}
          type="tel"
          inputMode="tel"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          required
          placeholder="0xxxxxxxxx"
          autoComplete="tel"
        />
      </label>
      <label className="block text-lg font-medium text-ink">
        Con học khối
        <select className={field} value={grade} onChange={(e) => setGrade(e.target.value)} required>
          <option value="">Chọn khối</option>
          <option value="9">Lớp 9 (ôn vào lớp 10)</option>
          <option value="10">Lớp 10</option>
          <option value="11">Lớp 11</option>
          <option value="12">Lớp 12</option>
        </select>
      </label>
      <label className="block text-lg font-medium text-ink">
        Trường của con <span className="font-normal text-muted">(không bắt buộc)</span>
        <input className={field} value={school} onChange={(e) => setSchool(e.target.value)} maxLength={120} />
      </label>
      <fieldset>
        <legend className="text-lg font-medium text-ink">
          Các tối con rảnh <span className="font-normal text-muted">(chọn nhiều tối)</span>
        </legend>
        <div className="mt-2 flex flex-wrap gap-2">
          {EVENINGS.map((d) => {
            const on = evenings.includes(d.v);
            return (
              <button
                key={d.v}
                type="button"
                aria-pressed={on}
                onClick={() => toggle(d.v)}
                className={`min-h-12 rounded-xl border px-4 text-lg font-medium ${on ? "border-primary bg-primary text-white" : "border-line bg-bg text-ink"}`}
              >
                {d.l}
              </button>
            );
          })}
        </div>
      </fieldset>
      {error && (
        <p role="alert" className="text-lg font-medium text-red-700">
          {error}
        </p>
      )}
      <button
        type="submit"
        disabled={busy}
        className="min-h-14 w-full rounded-xl bg-primary px-6 text-xl font-bold text-white disabled:opacity-60"
      >
        {busy ? "Đang gửi…" : "Đăng ký học thử 2 buổi miễn phí"}
      </button>
      <p className="text-[.9375rem] text-muted">
        Thầy chỉ dùng số điện thoại để gọi lại về buổi học thử, không chia sẻ cho nơi khác. Xem{" "}
        <Link href="/dieu-khoan" className="font-medium text-primary underline">
          điều khoản
        </Link>
        .
      </p>
    </form>
  );
}

export default function TrialSignup() {
  return (
    <section id="hoc-thu" className="parent-page border-t border-line py-16 lg:py-24">
      <div className="mx-auto max-w-3xl px-6 lg:px-8">
        <p className="font-mono text-xs uppercase tracking-widest text-primary">Kết quả đo được</p>
        <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">Con số thật, không lời hứa</h2>
        <p className="mt-4 text-lg leading-relaxed text-muted">
          Mỗi em được trợ giảng theo dõi từng bài trên ThachLab. Dưới đây là những gì đo được ở các lớp đang học.
        </p>
        <Stats />

        <h2 className="mt-14 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">Đăng ký học thử 2 buổi miễn phí</h2>
        <p className="mt-4 text-lg leading-relaxed text-muted">
          Con học thử hai buổi rồi anh/chị quyết định. Thầy gọi lại trong 24 giờ để hẹn tối phù hợp.
        </p>
        <div className="mt-6">
          <TrialForm />
        </div>

        <div className="mt-8 flex flex-wrap gap-3">
          {CONTACT.phone && (
            <a href={`tel:${CONTACT.phone}`} className="inline-flex min-h-12 items-center rounded-xl border border-line px-5 text-lg font-semibold text-ink">
              Gọi thầy {CONTACT.phone}
            </a>
          )}
          <Link href="/khoa-hoc" className="inline-flex min-h-12 items-center rounded-xl border border-line px-5 text-lg font-semibold text-primary">
            Xem các lớp đang mở
          </Link>
        </div>
      </div>
    </section>
  );
}
