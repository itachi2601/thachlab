"use client";

import { useEffect, useState } from "react";
import { Check, Info, Moon, Sun, TriangleAlert, X } from "lucide-react";

/**
 * XEM THỬ BẢNG MÀU — trang chỉ có nghĩa ở máy dev, mở http://localhost:3000/dev/giao-dien
 *
 * Vì sao có trang này: từ 11/10/2026 ThachLab lấy NỀN SÁNG (trắng) làm mặc định toàn site
 * (docs/QUY-TAC-THIET-KE.md M1 — đọc chữ sẫm trên nền sáng nhanh hơn ở mọi lứa tuổi). Bảng màu,
 * độ tương phản và "bộ dựng" cơ bản (thẻ, nút, ô nhập, trạng thái…) gom hết vào một chỗ để thầy
 * nhìn một lần là duyệt được, và để lần sau sửa màu thì sửa ở token `@theme` trong globals.css
 * rồi mở lại trang này kiểm — không phải đi soi từng trang.
 *
 * Trang này KHÔNG dùng màu hard-code: mọi thứ đọc từ token, nên đổi theme Sáng/Tối ở thanh trên
 * là thấy đúng cái người dùng thấy. Ba nhóm người xem (học sinh 14–18 / phụ huynh 45–60 / giáo
 * viên) dùng CÙNG hệ màu, chỉ khác số đo thị giác — bấm nút nhóm để xem khác nhau chỗ nào.
 */

type Theme = "light" | "dark";
type Audience = "student" | "parent" | "teacher";

const THEME_STORE = "thachlab-theme";

const TOKENS: { name: string; light: string; dark: string; note: string }[] = [
  { name: "--color-bg", light: "#f5f7fa", dark: "#05070b", note: "Nền trang. Không dùng trắng tinh để mặt thẻ nổi lên (M3)." },
  { name: "--color-panel", light: "#ffffff", dark: "#0b1020", note: "Mặt thẻ, navbar, thanh cố định." },
  { name: "--color-surface-2", light: "rgba(15,23,42,.05)", dark: "rgba(255,255,255,.05)", note: "Ô nhạt bên trong thẻ: khung hình, hàng bảng, nút phụ." },
  { name: "--color-ink", light: "#0f172a", dark: "#f1f5f9", note: "Chữ thân. 16,4:1 trên nền trang (M2 cần ≥4,5:1)." },
  { name: "--color-muted", light: "#475569", dark: "#94a3b8", note: "Chữ phụ, chú thích, mốc thời gian. 7,6:1 trên trắng." },
  { name: "--color-line", light: "rgba(15,23,42,.10)", dark: "rgba(255,255,255,.08)", note: "Viền hairline giữa các khối (B3: nhóm bằng khoảng cách, hạn chế viền)." },
  { name: "--color-line-strong", light: "#8b93a1", dark: "rgba(255,255,255,.16)", note: "Viền ô nhập, viền cần NHÌN RA — 3,2:1, đạt WCAG 1.4.11." },
  { name: "--color-primary", light: "#1d4ed8", dark: "#2563eb", note: "MÀU NHẤN DUY NHẤT cho thứ bấm được. Nền nút đặc + chữ trắng = 7,06:1." },
  { name: "--color-primary-soft", light: "#eef2ff", dark: "rgba(37,99,235,.18)", note: "Nền trạng thái \"đang chọn\": tab đang mở, chip lọc." },
  { name: "--color-ok", light: "#047857", dark: "#34d399", note: "Đúng / đạt. Luôn kèm icon hoặc chữ, không truyền nghĩa bằng màu (M4)." },
  { name: "--color-warn", light: "#b45309", dark: "#fbbf24", note: "Cần chú ý, sắp hết hạn." },
  { name: "--color-danger", light: "#b91c1c", dark: "#f87171", note: "Sai / lỗi / hành động phá huỷ (nộp bài sớm, xoá)." },
];

const AUDIENCES: Record<Audience, { label: string; wrap: string; note: string }> = {
  student: {
    label: "Học sinh 14–18",
    wrap: "",
    note: "Thân bài 16–18px, dòng 50–75 ký tự, đích chạm ≥44px. Một điểm nổi bật mỗi màn (B2). Phần thưởng/danh hiệu để cuối, không chen lúc đang học (L3).",
  },
  parent: {
    label: "Phụ huynh 45–60",
    wrap: "parent-page",
    note: "Nền hơi ngả ấm, chữ phụ nhắm 7:1 (AAA), đích chạm ≥48px, số to và thẳng cột (P1·P2·P4·P6). Nút A−/A+ ngay trong trang vì lão thị bắt đầu từ 40–45 tuổi (P5).",
  },
  teacher: {
    label: "Giáo viên / quản trị",
    wrap: "teacher-dashboard",
    note: "Cùng hệ màu nhưng nền trung tính hơn và cỡ chữ gốc 14px: người dùng là giáo viên trên laptop, màn hình nhiều bảng nên cần mật độ cao.",
  },
};

function applyTheme(theme: Theme) {
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.setAttribute("content", theme === "dark" ? "#05070b" : "#f5f7fa");
}

export default function PalettePreviewPage() {
  const [theme, setTheme] = useState<Theme>("light");
  const [audience, setAudience] = useState<Audience>("student");

  useEffect(() => {
    // Cho phép mở thẳng một tổ hợp: /dev/giao-dien?theme=dark&aud=parent — tiện chụp màn hình
    // và tiện gửi link cho người khác xem đúng cái mình đang nói.
    const q = new URLSearchParams(location.search);
    const qTheme = q.get("theme");
    const qAud = q.get("aud");
    if (qAud === "student" || qAud === "parent" || qAud === "teacher") setAudience(qAud);
    let saved: Theme = "light";
    try {
      if (localStorage.getItem(THEME_STORE) === "dark") saved = "dark";
    } catch {}
    const next: Theme = qTheme === "dark" || qTheme === "light" ? qTheme : saved;
    setTheme(next);
    applyTheme(next);
    // Mở bằng ?theme=… thì ghi luôn vào localStorage: nhờ vậy chỉ cần mở một lần là các trang
    // khác trong cùng trình duyệt cũng theo theme đó (tiện chụp màn hình nền tối của trang thật).
    if (qTheme === "dark" || qTheme === "light") {
      try {
        localStorage.setItem(THEME_STORE, next);
      } catch {}
    }
  }, []);

  const aud = AUDIENCES[audience];

  return (
    <div className="min-h-screen bg-bg text-ink">
      {/* Thanh điều khiển của CHÍNH trang xem thử (không phải mẫu thiết kế) */}
      <div className="sticky top-0 z-20 border-b border-line bg-panel/95 backdrop-blur">
        <div className="mx-auto flex max-w-5xl flex-wrap items-center gap-3 px-4 py-3">
          <b className="text-sm">Bảng màu ThachLab</b>
          <span className="text-xs text-muted">nền sáng là mặc định · đo bằng npm run check:a11y</span>
          <div className="ml-auto flex items-center gap-2">
            <div className="flex overflow-hidden rounded-lg border border-line">
              {(Object.keys(AUDIENCES) as Audience[]).map((k) => (
                <button
                  key={k}
                  type="button"
                  onClick={() => setAudience(k)}
                  className={`min-h-11 px-3 text-xs font-semibold ${audience === k ? "bg-primary text-white" : "text-muted"}`}
                >
                  {AUDIENCES[k].label}
                </button>
              ))}
            </div>
            <button
              type="button"
              onClick={() => {
                const next: Theme = theme === "dark" ? "light" : "dark";
                setTheme(next);
                applyTheme(next);
                try {
                  localStorage.setItem(THEME_STORE, next);
                } catch {}
              }}
              className="inline-flex min-h-11 items-center gap-2 rounded-lg border border-line px-3 text-xs font-semibold"
            >
              {theme === "dark" ? <Sun size={15} /> : <Moon size={15} />}
              {theme === "dark" ? "Đang xem nền tối" : "Đang xem nền sáng"}
            </button>
          </div>
        </div>
      </div>

      <main className={`mx-auto max-w-5xl px-4 py-6 ${aud.wrap}`}>
        <h1 className="text-xl font-bold">Bảng màu &amp; bộ dựng cơ bản</h1>
        <p className="mt-1 max-w-2xl text-sm text-muted">{aud.note}</p>

        {/* 1. Token */}
        <section className="mt-6">
          <h2 className="text-base font-bold">1 · Token màu</h2>
          <div className="mt-3 overflow-hidden rounded-2xl border border-line bg-panel">
            <table className="w-full border-collapse text-left text-sm">
              <thead>
                <tr className="bg-surface-2 text-xs uppercase tracking-wide text-muted">
                  <th className="px-3 py-2">Mẫu</th>
                  <th className="px-3 py-2">Token</th>
                  <th className="px-3 py-2">Nền sáng</th>
                  <th className="px-3 py-2">Nền tối</th>
                  <th className="hidden px-3 py-2 sm:table-cell">Dùng ở đâu</th>
                </tr>
              </thead>
              <tbody>
                {TOKENS.map((t) => (
                  <tr key={t.name} className="border-t border-line align-top">
                    <td className="px-3 py-2">
                      <span className="block h-6 w-10 rounded border border-line" style={{ background: `var(${t.name})` }} />
                    </td>
                    <td className="whitespace-nowrap px-3 py-2 font-mono text-xs">{t.name}</td>
                    <td className="whitespace-nowrap px-3 py-2 font-mono text-xs">{t.light}</td>
                    <td className="whitespace-nowrap px-3 py-2 font-mono text-xs">{t.dark}</td>
                    <td className="hidden px-3 py-2 text-xs text-muted sm:table-cell">{t.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* 2. Nút */}
        <section className="mt-8">
          <h2 className="text-base font-bold">2 · Nút — mỗi màn chỉ MỘT nút nổi (B2)</h2>
          <div className="mt-3 flex flex-wrap items-center gap-3">
            <button type="button" className="min-h-11 rounded-xl bg-primary px-4 text-sm font-semibold text-white">Học tiếp</button>
            <button type="button" className="min-h-11 rounded-xl bg-primary-dark px-4 text-sm font-semibold text-white">Đang bấm</button>
            <button type="button" className="min-h-11 rounded-xl border border-line-strong px-4 text-sm font-semibold text-ink">Nút phụ (viền, không nền)</button>
            <button type="button" className="min-h-11 rounded-xl bg-surface-2 px-4 text-sm font-semibold text-ink">Nút nhạt</button>
            <button type="button" className="min-h-11 rounded-xl border border-danger px-4 text-sm font-semibold text-danger">Nộp bài sớm</button>
            <button type="button" disabled className="min-h-11 rounded-xl bg-surface-2 px-4 text-sm font-semibold text-muted">Không bấm được</button>
          </div>
        </section>

        {/* 3. Chữ & thẻ */}
        <section className="mt-8 grid gap-4 sm:grid-cols-2">
          <div className="rounded-2xl border border-line bg-panel p-4">
            <h3 className="text-base font-bold">Thẻ nội dung</h3>
            <p className="mt-2 text-sm leading-relaxed">
              Chữ thân trên mặt thẻ trắng. Tiếng Việt có dấu chồng tầng nên line-height phải ≥ 1,55 để dấu không chạm dòng trên (C1).
            </p>
            <p className="mt-2 text-xs text-muted">Dòng phụ, mốc thời gian, chú thích — 7,6:1 trên trắng.</p>
            <div className="mt-3 h-2 overflow-hidden rounded-full bg-surface-2">
              <div className="h-full w-[62%] rounded-full bg-primary" />
            </div>
            <p className="mt-1 text-xs text-muted">Tiến độ: một màu nhấn, không gradient, không quầng sáng (M3·M6).</p>
          </div>

          <div className="space-y-3">
            <div className="flex items-start gap-2 rounded-xl border border-line bg-panel p-3 text-sm">
              <Check size={17} className="mt-0.5 shrink-0 text-ok" aria-hidden />
              <span><b className="text-ok">Đúng.</b> Phản hồi nói vì sao đúng và việc làm tiếp (L1·L4).</span>
            </div>
            <div className="flex items-start gap-2 rounded-xl border border-line bg-panel p-3 text-sm">
              <X size={17} className="mt-0.5 shrink-0 text-danger" aria-hidden />
              <span><b className="text-danger">Chưa đúng.</b> Xem lại mục 2 rồi thử câu tương tự.</span>
            </div>
            <div className="flex items-start gap-2 rounded-xl border border-line bg-panel p-3 text-sm">
              <TriangleAlert size={17} className="mt-0.5 shrink-0 text-warn" aria-hidden />
              <span><b className="text-warn">Còn 5 phút.</b> Trạng thái luôn có chữ đi kèm, không chỉ màu (M4).</span>
            </div>
            <div className="flex items-start gap-2 rounded-xl border border-line bg-surface-2 p-3 text-sm">
              <Info size={17} className="mt-0.5 shrink-0 text-muted" aria-hidden />
              <span className="text-muted">Ghi chú trung tính: nền nhạt hơn thẻ, không viền đậm (B3).</span>
            </div>
          </div>
        </section>

        {/* 4. Ô nhập & điều hướng */}
        <section className="mt-8 grid gap-4 sm:grid-cols-2">
          <div className="rounded-2xl border border-line bg-panel p-4">
            <h3 className="text-base font-bold">Ô nhập</h3>
            <label className="mt-3 block text-xs font-semibold text-muted" htmlFor="pv-input">Đáp số</label>
            <input
              id="pv-input"
              inputMode="decimal"
              placeholder="Ví dụ: 2,5"
              className="mt-1 min-h-11 w-full rounded-xl border border-line-strong bg-panel px-3 text-base text-ink placeholder:text-muted"
            />
            <p className="mt-2 text-xs text-muted">Viền ô nhập đạt 3:1 (WCAG 1.4.11); trên điện thoại ô nhập phải ≥16px để iOS không tự phóng to.</p>
            <label className="mt-3 block text-xs font-semibold text-muted" htmlFor="pv-select">Chọn lớp</label>
            <select id="pv-select" className="mt-1 min-h-11 w-full rounded-xl border border-line-strong bg-panel px-3 text-base text-ink">
              <option>Lớp 12A1</option>
              <option>Lớp 11B2</option>
            </select>
          </div>

          <div className="rounded-2xl border border-line bg-panel p-4">
            <h3 className="text-base font-bold">Tab &amp; chip</h3>
            <div className="mt-3 flex flex-wrap gap-2">
              <span className="rounded-lg bg-primary-soft px-3 py-2 text-sm font-semibold text-primary">Lý thuyết</span>
              <span className="rounded-lg px-3 py-2 text-sm font-semibold text-muted">Luyện tập</span>
              <span className="rounded-lg px-3 py-2 text-sm font-semibold text-muted">Kiểm tra</span>
              <span className="rounded-lg px-3 py-2 text-sm font-semibold text-muted">Bài mẫu</span>
            </div>
            <p className="mt-2 text-xs text-muted">Tối đa 4 mục nhìn thấy cùng lúc (N2); tab phải lộ hết ở 360px (D4).</p>
            <div className="mt-3 flex flex-wrap gap-2">
              <span className="rounded-full bg-surface-2 px-3 py-1 text-xs font-semibold text-muted">Đã học</span>
              <span className="rounded-full bg-primary-soft px-3 py-1 text-xs font-semibold text-primary">Đang học</span>
              <span className="rounded-full bg-surface-2 px-3 py-1 text-xs font-semibold text-muted">Chưa mở</span>
            </div>
          </div>
        </section>

        {/* 5. Bảng dữ liệu + trạng thái rỗng */}
        <section className="mt-8">
          <h2 className="text-base font-bold">5 · Bảng dữ liệu (khu giáo viên dùng nhiều)</h2>
          <div className="mt-3 overflow-hidden rounded-2xl border border-line bg-panel">
            <table className="w-full border-collapse text-left text-sm">
              <thead>
                <tr className="bg-surface-2 text-xs uppercase tracking-wide text-muted">
                  <th className="px-3 py-2">Học sinh</th>
                  <th className="px-3 py-2">Điểm</th>
                  <th className="px-3 py-2">Trạng thái</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-line">
                  <td className="px-3 py-2">Nguyễn Văn A</td>
                  <td className="px-3 py-2 font-semibold tabular-nums">8,5</td>
                  <td className="px-3 py-2"><span className="text-ok">Giỏi</span></td>
                </tr>
                <tr className="border-t border-line">
                  <td className="px-3 py-2">Trần Thị B</td>
                  <td className="px-3 py-2 font-semibold tabular-nums">6,0</td>
                  <td className="px-3 py-2"><span className="text-warn">Cần cố gắng thêm</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="mt-2 text-xs text-muted">Xếp loại theo ngưỡng quen thuộc (P15), số căn cột bằng tabular-nums (P6).</p>
        </section>

        {/* 6. Ba nguyên tắc dễ vi phạm nhất */}
        <section className="mt-8 rounded-2xl border border-line bg-panel p-4">
          <h2 className="text-base font-bold">6 · Ba lỗi hay gặp khi thêm màu mới</h2>
          <ul className="mt-2 space-y-1.5 text-sm">
            <li><b>Gradient/quầng sáng trong vùng đọc</b> — M6 chỉ cho phép ở trang giới thiệu; trong bài học và lúc làm bài là nhiễu (G3).</li>
            <li><b>Thêm sắc độ bão hoà thứ ba</b> — M3: một màu nhấn cho việc bấm được, ba màu trạng thái, còn lại trung tính. Màu rực kéo chú ý tiền ý thức (G2).</li>
            <li><b>Chữ trắng trên nền trắng hoặc xám nhạt trên xám nhạt</b> — sau khi đổi theme, luôn kiểm lại bằng <code className="font-mono text-xs">npm run check:a11y</code> rồi mở lại trang này.</li>
          </ul>
        </section>

        <p className="mt-8 text-xs text-muted">
          Sửa màu: chỉ sửa khối <code className="font-mono">@theme</code> và <code className="font-mono">html[data-theme=&quot;dark&quot;]</code> trong
          <code className="font-mono"> app/globals.css</code>, đo lại bằng <code className="font-mono">npm run check:a11y</code>, rồi mở lại trang này.
        </p>
      </main>
    </div>
  );
}
