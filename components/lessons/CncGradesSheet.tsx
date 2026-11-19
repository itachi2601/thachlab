"use client";

// Bảng điểm học phần CNC của chính em: 2 điểm — Tiện, Phay (bảng cnc_grades, RLS chỉ cho đọc dòng của mình).
// Mở từ thông báo "Điểm thi tiện CNC". Một cột ≤680px, số to, lỗi loại trực tiếp ghi bằng chữ (không chỉ màu).
import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";
import { fetchMyCncGrades, type CncGrade, type CncGradeModule } from "@/services/cnc-grades";

const MODULES: { key: CncGradeModule; label: string }[] = [
  { key: "tien", label: "Điểm 1 · Tiện" },
  { key: "phay", label: "Điểm 2 · Phay" },
];
const LEVEL: Record<string, string> = { E: "Xuất sắc", G: "Khá", P: "Đạt", F: "Không đạt" };
const fmt = (x: number | null | undefined) => (x === null || x === undefined ? "–" : String(Math.round(x * 100) / 100).replace(".", ","));

function tone(g: CncGrade): "ok" | "warn" | "bad" {
  if (g.detail.violations?.length || g.total < 5) return "bad";
  return g.total >= 7 ? "ok" : "warn";
}

function GradeCard({ label, g }: { label: string; g: CncGrade | undefined }) {
  if (!g) {
    return (
      <section className="rounded-xl border p-4" style={{ borderColor: "var(--cnc-line)", background: "var(--cnc-surface)" }}>
        <h2 className="text-lg font-semibold" style={{ color: "var(--cnc-title)" }}>{label}</h2>
        <p className="mt-2 text-base" style={{ color: "var(--cnc-muted)" }}>Chưa có điểm. Khi giảng viên chấm xong, điểm sẽ hiện ở đây.</p>
      </section>
    );
  }
  const t = tone(g);
  const viol = g.detail.violations ?? [];
  const crit = g.detail.criteria ?? [];
  return (
    <section className="rounded-xl border p-4" style={{ borderColor: `var(--cnc-${t}-line)`, background: "var(--cnc-surface)" }}>
      <h2 className="text-lg font-semibold" style={{ color: "var(--cnc-title)" }}>{label}</h2>
      <p className="mt-1 flex flex-wrap items-baseline gap-x-3">
        <span className="text-4xl font-bold" style={{ color: `var(--cnc-${t})` }}>{fmt(g.total)}<span className="text-xl font-semibold">/10</span></span>
        <span className="text-lg font-semibold" style={{ color: `var(--cnc-${t})` }}>{g.grade ?? ""}</span>
      </p>
      <p className="mt-1 text-base" style={{ color: "var(--cnc-muted)" }}>
        I. Kỹ thuật {fmt(g.ky_thuat)}/7 · II. Thành phần {fmt(g.thanh_phan)}/3
        {g.ky_thuat !== null && g.ky_thuat < 3.5 ? " (kỹ thuật dưới 3,5 nên thành phần tính 0)" : ""}
      </p>
      <div className="mt-3 rounded-lg p-3 text-base" style={{ background: viol.length ? "var(--cnc-bad-soft)" : "var(--cnc-ok-soft)", color: viol.length ? "var(--cnc-bad)" : "var(--cnc-ok)" }}>
        <strong>Lỗi loại trực tiếp: </strong>
        {viol.length ? (
          <>
            <ul className="mt-1 list-disc pl-5">{viol.map((v) => <li key={v}>{v}</li>)}</ul>
            <span>Bài bị tính Không đạt.</span>
          </>
        ) : (
          "không vi phạm"
        )}
      </div>
      {crit.length > 0 && (
        <table className="mt-3 w-full border-collapse text-base" style={{ color: "var(--cnc-text)" }}>
          <thead>
            <tr style={{ color: "var(--cnc-muted)" }}>
              <th className="py-1 text-left font-medium">Tiêu chí</th>
              <th className="py-1 text-left font-medium">Mức</th>
              <th className="py-1 text-right font-medium">Điểm</th>
            </tr>
          </thead>
          <tbody>
            {crit.map((c) => (
              <tr key={c.name} className="border-t" style={{ borderColor: "var(--cnc-line)" }}>
                <td className="py-2 pr-2">{c.name}</td>
                <td className="py-2 pr-2">{c.level ? LEVEL[c.level] ?? c.level : "chưa chấm"}</td>
                <td className="py-2 text-right whitespace-nowrap">{fmt(c.points)}/{fmt(c.max)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}

export default function CncGradesSheet() {
  const { session, loading } = useAuth();
  const [grades, setGrades] = useState<CncGrade[] | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!session) return;
    let cancelled = false;
    fetchMyCncGrades(session.user.id)
      .then((r) => !cancelled && setGrades(r))
      .catch(() => !cancelled && setError(true));
    return () => {
      cancelled = true;
    };
  }, [session]);

  const here = typeof window === "undefined" ? "/lop-hoc/cnc/bang-diem/" : window.location.pathname + window.location.search;
  return (
    <div className="cnc-shell lesson-shell lesson-shell--cttc">
      <div className="mx-auto w-full max-w-[680px] px-4 py-6">
        <Link href="/lop-hoc/cnc" className="lesson-link min-h-[44px]">← Về lớp CNC</Link>
        <h1 className="mt-2 text-2xl font-bold" style={{ color: "var(--cnc-title)" }}>Bảng điểm CNC</h1>
        <p className="mt-1 text-base" style={{ color: "var(--cnc-muted)" }}>Học phần có 2 điểm: Tiện và Phay. Chỉ mình em xem được trang này.</p>
        <div className="mt-4 grid gap-4">
          {loading ? (
            <p style={{ color: "var(--cnc-muted)" }}>Đang tải…</p>
          ) : !session ? (
            <a className="lesson-btn" href={`/dang-nhap?next=${encodeURIComponent(here)}&lop=cnc`}>Đăng nhập để xem điểm</a>
          ) : error ? (
            <p style={{ color: "var(--cnc-bad)" }}>Chưa tải được điểm. Em tải lại trang giúp thầy nhé.</p>
          ) : grades === null ? (
            <p style={{ color: "var(--cnc-muted)" }}>Đang tải…</p>
          ) : (
            MODULES.map((m) => <GradeCard key={m.key} label={m.label} g={grades.find((x) => x.module === m.key)} />)
          )}
        </div>
      </div>
    </div>
  );
}
