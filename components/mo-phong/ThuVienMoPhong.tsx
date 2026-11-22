"use client";

/**
 * Thư viện /mo-phong (Gói B). Dữ liệu tĩnh từ lib/data/thu-vien-mo-phong.json, không gọi DB.
 * Quy tắc: N2 (≤4 lựa chọn nhìn thấy mỗi vùng lọc), V2 (dòng "Nhìn vào:"), V5 (clip: ảnh bìa, chỉ nạp player khi bấm),
 * D2/P4 (đích chạm ≥48px), C1/P1 (thân 18px, nhãn phụ ≥15px), M1 (nền sáng), B4 (không tự chạy), B2 (một lời mời cuối trang).
 */
import { useMemo, useState } from "react";
import Link from "next/link";
import { ChevronDown, Play, Search } from "lucide-react";
import data from "@/lib/data/thu-vien-mo-phong.json";

type The = {
  id: string;
  loai: "mo_phong" | "clip" | "phet";
  ten: string;
  lop: number;
  chu_de: string;
  nhin_vao: string;
  href: string;
  nhan_loai: string;
  poster?: string;
  mp4?: string;
  youtube_id?: string;
  nguon?: string;
  bat_dau?: number;
  ket_thuc?: number;
};

const CHU_DE = data.chu_de as Record<string, string>;
const THE = data.the as The[];
const LOP = [9, 10, 11, 12];
const CHU_DE_KEYS = Object.keys(CHU_DE);
const BUOC = 24;

export function boDau(s: string) {
  return s
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/đ/g, "d")
    .replace(/Đ/g, "d")
    .toLowerCase()
    .replace(/\s+/g, " ")
    .trim();
}

const chipCls = (on: boolean) =>
  `inline-flex min-h-12 items-center rounded-full border px-5 text-base font-medium transition-colors ${
    on ? "border-primary bg-primary-soft text-primary" : "border-line-strong bg-panel text-ink hover:bg-surface-2"
  }`;

const NHAN_CLS: Record<string, string> = {
  mo_phong: "bg-primary-soft text-primary",
  clip: "bg-surface-2 text-ink",
  phet: "bg-surface-2 text-ink",
};

function ClipMedia({ the }: { the: The }) {
  const [phat, setPhat] = useState(false);
  const doc = the.mp4 ? "aspect-[9/16] max-h-[26rem]" : "aspect-video";
  if (phat) {
    if (the.mp4) {
      return (
        <video
          src={the.mp4}
          poster={the.poster}
          controls
          autoPlay
          playsInline
          className="mx-auto max-h-[26rem] w-full rounded-xl bg-surface-2 object-contain"
          aria-label={`Clip: ${the.ten}`}
        />
      );
    }
    const q = new URLSearchParams({ autoplay: "1", rel: "0", playsinline: "1" });
    if (the.bat_dau != null) q.set("start", String(the.bat_dau));
    if (the.ket_thuc != null) q.set("end", String(the.ket_thuc));
    return (
      <iframe
        title={`Clip: ${the.ten}`}
        src={`https://www.youtube-nocookie.com/embed/${the.youtube_id}?${q}`}
        allow="autoplay; encrypted-media; picture-in-picture"
        allowFullScreen
        className="aspect-video w-full rounded-xl bg-surface-2"
      />
    );
  }
  return (
    <button
      type="button"
      onClick={() => setPhat(true)}
      aria-label={`Phát clip: ${the.ten}`}
      className={`relative block w-full overflow-hidden rounded-xl bg-surface-2 ${the.mp4 ? "aspect-video" : doc}`}
    >
      {the.poster && (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={the.poster}
          alt=""
          loading="lazy"
          decoding="async"
          className={`h-full w-full ${the.mp4 ? "object-contain" : "object-cover"}`}
        />
      )}
      <span className="absolute inset-0 flex items-center justify-center">
        <span className="flex h-14 w-14 items-center justify-center rounded-full bg-panel text-primary shadow-md ring-1 ring-line">
          <Play aria-hidden className="h-6 w-6" fill="currentColor" />
        </span>
      </span>
    </button>
  );
}

function TheMoPhong({ the }: { the: The }) {
  const ngoai = the.href.startsWith("http");
  const lienKet =
    the.loai === "mo_phong"
      ? "Mở mô phỏng"
      : the.loai === "phet"
        ? "Mở mô phỏng PhET"
        : "Xem trong bài học (cần đăng nhập)";
  return (
    <li className="flex flex-col gap-3 rounded-2xl border border-line bg-panel p-4">
      {the.loai === "clip" && <ClipMedia the={the} />}
      <div className="flex flex-wrap items-center gap-2 text-[15px]">
        <span className={`rounded-full px-3 py-1 font-semibold ${NHAN_CLS[the.loai]}`}>{the.nhan_loai}</span>
        <span className="text-muted">
          Lớp {the.lop} · {CHU_DE[the.chu_de]}
        </span>
      </div>
      <h3 className="text-lg font-semibold leading-snug text-ink">{the.ten}</h3>
      <p className="text-[17px] leading-relaxed text-ink">
        <span className="font-semibold">Nhìn vào:</span> {the.nhin_vao}
      </p>
      <div className="mt-auto flex flex-col gap-1 pt-1">
        <Link
          href={the.href}
          prefetch={false}
          {...(ngoai ? { target: "_blank", rel: "noopener noreferrer" } : {})}
          className="inline-flex min-h-12 items-center text-base font-semibold text-primary underline-offset-4 hover:underline"
        >
          {lienKet} {ngoai ? "↗" : "→"}
        </Link>
        {the.nguon && <span className="text-[15px] text-muted">{the.nguon}</span>}
      </div>
    </li>
  );
}

export default function ThuVienMoPhong() {
  const [lop, setLop] = useState<number | null>(null);
  const [cd, setCd] = useState<string | null>(null);
  const [q, setQ] = useState("");
  const [them, setThem] = useState(false);
  const [hien, setHien] = useState(BUOC);

  const blob = useMemo(() => new Map(THE.map((t) => [t.id, boDau(`${t.ten} ${t.nhin_vao} ${CHU_DE[t.chu_de]}`)])), []);
  const kq = useMemo(() => {
    // Cụm từ đã bỏ dấu, khớp từ đầu từ (" con lac" ra "con lắc", không ra "cộng … lắc").
    const cum = " " + boDau(q);
    return THE.filter(
      (t) => (lop == null || t.lop === lop) && (cd == null || t.chu_de === cd) && (cum === " " || (" " + blob.get(t.id)!).includes(cum)),
    );
  }, [lop, cd, q, blob]);

  const coLoc = lop != null || cd != null || q.trim() !== "";
  const xoa = () => {
    setLop(null);
    setCd(null);
    setQ("");
    setHien(BUOC);
  };
  const doi = <T,>(set: (v: T | null) => void, cur: T | null, v: T) => {
    set(cur === v ? null : v);
    setHien(BUOC);
  };
  const cdHienSan = CHU_DE_KEYS.slice(0, 4);
  const cdThem = CHU_DE_KEYS.slice(4);
  const cdThemDangChon = cd != null && cdThem.includes(cd);

  return (
    <section aria-label="Thư viện mô phỏng">
      <div className="rounded-2xl border border-line bg-panel p-4">
        <label htmlFor="tim-mo-phong" className="mb-2 block text-base font-semibold text-ink">
          Tìm theo tên hoặc hiện tượng
        </label>
        <div className="relative">
          <Search aria-hidden className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted" />
          <input
            id="tim-mo-phong"
            type="search"
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setHien(BUOC);
            }}
            placeholder="ví dụ: con lắc, sóng dừng"
            autoComplete="off"
            className="min-h-12 w-full rounded-xl border border-line-strong bg-panel pl-12 pr-4 text-lg text-ink placeholder:text-slate-500"
          />
        </div>

        <fieldset className="mt-4">
          <legend className="mb-2 text-base font-semibold text-ink">Lớp</legend>
          <div className="flex flex-wrap gap-2">
            {LOP.map((l) => (
              <button key={l} type="button" aria-pressed={lop === l} onClick={() => doi(setLop, lop, l)} className={chipCls(lop === l)}>
                {l === 9 ? "KHTN 9" : `Lớp ${l}`}
              </button>
            ))}
          </div>
        </fieldset>

        <fieldset className="mt-4">
          <legend className="mb-2 text-base font-semibold text-ink">Chủ đề</legend>
          <div className="flex flex-wrap gap-2">
            {cdHienSan.map((k) => (
              <button key={k} type="button" aria-pressed={cd === k} onClick={() => doi(setCd, cd, k)} className={chipCls(cd === k)}>
                {CHU_DE[k]}
              </button>
            ))}
            {!them && !cdThemDangChon && (
              <button
                type="button"
                aria-expanded={false}
                onClick={() => setThem(true)}
                className="inline-flex min-h-12 items-center gap-1 rounded-full px-4 text-base font-medium text-primary hover:underline"
              >
                Chủ đề khác <ChevronDown aria-hidden className="h-4 w-4" />
              </button>
            )}
            {(them || cdThemDangChon) &&
              cdThem.map((k) => (
                <button key={k} type="button" aria-pressed={cd === k} onClick={() => doi(setCd, cd, k)} className={chipCls(cd === k)}>
                  {CHU_DE[k]}
                </button>
              ))}
          </div>
        </fieldset>

        <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1">
          <p className="text-base text-ink" role="status" aria-live="polite">
            <span className="font-semibold">{kq.length}</span> kết quả
          </p>
          {coLoc && (
            <button type="button" onClick={xoa} className="min-h-12 text-base font-medium text-primary underline-offset-4 hover:underline">
              Bỏ hết bộ lọc
            </button>
          )}
        </div>
      </div>

      {kq.length === 0 ? (
        <div className="mt-6 rounded-2xl border border-line bg-panel p-6 text-center">
          <p className="text-lg text-ink">Không có mục nào khớp. Thử bớt một bộ lọc, hoặc gõ ngắn hơn (ví dụ “song”, “dien”).</p>
          <button type="button" onClick={xoa} className="mt-3 min-h-12 rounded-xl bg-primary px-5 text-base font-semibold text-white">
            Bỏ hết bộ lọc
          </button>
        </div>
      ) : (
        <>
          <ul className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {kq.slice(0, hien).map((t) => (
              <TheMoPhong key={t.id} the={t} />
            ))}
          </ul>
          {hien < kq.length && (
            <div className="mt-6 text-center">
              <button
                type="button"
                onClick={() => setHien((h) => h + BUOC)}
                className="min-h-12 rounded-xl border border-line-strong bg-panel px-6 text-base font-semibold text-ink hover:bg-surface-2"
              >
                Xem thêm ({kq.length - hien} mục nữa)
              </button>
            </div>
          )}
        </>
      )}
    </section>
  );
}
