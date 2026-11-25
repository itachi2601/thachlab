"use client";

/**
 * components/physics/do-luong/ThuocKep.tsx — thước kẹp du xích tự kéo (Gói A, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 3).
 * Gắn vào L10 Bài 3 (lesson 48) qua MoPhongPortals khoá "thuoc-kep". Tự dựng, không lấy gì từ trang khác.
 *
 * Hình trên: toàn thước (thước chính + du xích + vật kẹp), khung xanh là chỗ kính lúp đang nhìn.
 * Hình dưới: kính lúp phóng to — vạch du xích lệch nhau 0,02 mm chỉ thấy được khi phóng to.
 * Xem cách đọc (N6): kéo hàm hoặc bấm ± theo bước bằng độ chính xác (kéo 0,02 mm bằng ngón tay là không thể — mục 2 kế hoạch),
 * ba bước đọc có số điền sẵn, vạch trùng tô màu kèm chữ "trùng" (M4, H3).
 * Luyện đọc: số ngẫu nhiên (có ca biên vạch 0 trùng, vạch kế cuối trùng), gõ số đọc, chấm ngay chỉ đúng chỗ sai (L1, L4),
 * đúng 5 lần liên tiếp là xong, lưu localStorage (L2, không điểm — L3).
 * Quy tắc UI: N2 (≤ 4 nút mỗi hàng), D2 (44 px), C1/H4 (chữ trong hình ≥ 13 px ở 360 px), M1/M7 (token nền sáng, tối tự đổi),
 * B4 (không gì tự chạy).
 */

import { useId, useMemo, useRef, useState, type PointerEvent, type ReactNode } from "react";
import { ChonCheDo, HangChon, LuyenDoc, phuBtn, soNguyenRaChuoi, useTienDo, type CheDo } from "./chung";
import { DU_XICH, chamThuocKep, ghiThuocKep, ngauNhienThuocKep, tachThuocKep, type LoaiDuXich } from "./cham";

const MAX_N = 30; // phần nguyên lớn nhất (mm) của số đọc
const W = 360;
const X0 = 24;
const X1 = 346;
/** Kính lúp: px/mm theo loại du xích (ở 70 px/mm, vạch kề vạch trùng lệch 1,4 px, vạch kề nữa 2,8 px — mắt thấy được độ đối xứng). */
const PPM: Record<LoaiDuXich, number> = { 10: 30, 5: 44, 2: 70 };

const LUA_CHON: { value: LoaiDuXich; text: string }[] = [
  { value: 10, text: "0,1" },
  { value: 5, text: "0,05" },
  { value: 2, text: "0,02" },
];

function kepZ(zH: number, pH: LoaiDuXich) {
  const max = MAX_N * 100 + (DU_XICH[pH].N - 1) * pH;
  return Math.max(0, Math.min(max, Math.round(zH / pH) * pH));
}

/* ---------------- Màu thép (cố định, không đổi theo sáng/tối: đây là "ảnh" dụng cụ thật — M5) ---------------- */

/** Mực khắc vạch, màu vạch 0 du xích, màu vạch trùng — cố định vì nằm trên nền thép sáng ở cả hai chế độ. */
const MUC = "#1b2026";
const XANH = "#1d4ed8";
const LUC = "#15803d";
/** Chữ đậm hơn nét để đạt ≥ 4,5:1 trên tấm du xích (kiem-code 25/11). */
const LUC_CHU = "#166534";
const XANH_CHU = "#1e40af";

/** Gradient thép không gỉ (thân thước, du xích, hàm, đồng thau của vật kẹp). id duy nhất theo useId. */
function MauThep({ id }: { id: string }) {
  return (
    <defs>
      <linearGradient id={`${id}-than`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#f6f8fa" />
        <stop offset="0.42" stopColor="#dde2e7" />
        <stop offset="0.58" stopColor="#cbd2d8" />
        <stop offset="1" stopColor="#eef1f4" />
      </linearGradient>
      <linearGradient id={`${id}-tam`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#eaedf0" />
        <stop offset="1" stopColor="#c6cdd4" />
      </linearGradient>
      <linearGradient id={`${id}-ham`} x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#c3cad1" />
        <stop offset="0.5" stopColor="#eef1f4" />
        <stop offset="1" stopColor="#b7bfc7" />
      </linearGradient>
      <linearGradient id={`${id}-dong`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#f6dc98" />
        <stop offset="0.5" stopColor="#c9973a" />
        <stop offset="1" stopColor="#efcd7e" />
      </linearGradient>
      <pattern id={`${id}-khia`} width="3" height="4" patternUnits="userSpaceOnUse">
        <rect width="3" height="4" fill="#9aa4ad" />
        <rect width="1.4" height="4" fill="#5f6a74" />
      </pattern>
    </defs>
  );
}

const VIEN = "#7b8590";

/* ---------------- Hình toàn thước ---------------- */

function HinhToanThuoc({
  zH,
  pH,
  c,
  wMm,
  onPointMm,
  xem,
}: {
  zH: number;
  pH: LoaiDuXich;
  c: number;
  wMm: number;
  onPointMm: (mm: number, keo: boolean) => void;
  xem: boolean;
}) {
  const { N, len } = DU_XICH[pH];
  const R = MAX_N + len + 3;
  const S = (X1 - X0) / R;
  const x = (mm: number) => X0 + mm * S;
  const z = zH / 100;
  const ref = useRef<SVGSVGElement>(null);
  const down = useRef(false);
  const id = `tk${useId().replace(/[^a-zA-Z0-9]/g, "")}`;

  const toMm = (e: PointerEvent<SVGSVGElement>) => {
    const r = ref.current!.getBoundingClientRect();
    return ((e.clientX - r.left) / r.width) * W - X0;
  };

  // Thân thước: y 22–62; vạch thước chính khắc từ mép dưới thân lên; tấm du xích 62–84 ngay dưới.
  const T0 = 22;
  const BY = 62;
  const P1 = 84;
  const xa = x(z);
  const xb = x(z + len + 2);

  const main: ReactNode[] = [];
  for (let j = 0; j <= R; j++) {
    const h = j % 10 === 0 ? 12 : j % 5 === 0 ? 8 : 5;
    main.push(<line key={j} x1={x(j)} x2={x(j)} y1={BY} y2={BY - h} />);
    if (j % 10 === 0)
      main.push(
        <text key={`t${j}`} x={x(j)} y={T0 + 18} textAnchor="middle" fontSize={15} fill={MUC} stroke="none">
          {j}
        </text>,
      );
  }
  const ver: ReactNode[] = [];
  for (let i = 0; i <= N; i++) {
    const xi = x(z + (i * len) / N);
    ver.push(
      <line
        key={i}
        x1={xi}
        x2={xi}
        y1={BY}
        y2={BY + (i % DU_XICH[pH].nhanMoi === 0 ? 9 : 5)}
        stroke={i === 0 ? XANH : MUC}
        strokeWidth={i === 0 ? 1.8 : 1}
      />,
    );
  }

  return (
    <svg
      ref={ref}
      viewBox={`0 0 ${W} 150`}
      className="block w-full select-none"
      style={{ touchAction: "pan-y" }}
      role="img"
      aria-label={xem ? `Thước kẹp đang chỉ ${ghiThuocKep(zH, pH)} mm. Kéo hàm để đổi.` : "Thước kẹp. Chạm vào thước để dời kính lúp."}
      onPointerDown={(e) => {
        down.current = true;
        ref.current?.setPointerCapture(e.pointerId);
        onPointMm(toMm(e), false);
      }}
      onPointerMove={(e) => down.current && onPointMm(toMm(e), true)}
      onPointerUp={() => (down.current = false)}
      onPointerCancel={() => (down.current = false)}
    >
      <MauThep id={id} />
      {/* vật được kẹp: thanh đồng thau nhìn ngang */}
      {z > 0.3 && <rect x={X0} y={100} width={xa - X0} height={30} fill={`url(#${id}-dong)`} stroke="#9a6f22" strokeWidth={0.8} />}
      {/* hàm cố định: hàm đo ngoài (dưới) + mỏ đo trong (trên), mặt đo thẳng đứng ở x = X0 */}
      <path
        d={`M${X0},${BY} V136 L${X0 - 3},146 L${X0 - 8},142 L${X0 - 22},110 V${BY} Z`}
        fill={`url(#${id}-ham)`}
        stroke={VIEN}
        strokeWidth={1}
      />
      <path d={`M${X0},${T0} V4 L${X0 - 4},4 L${X0 - 16},${T0} Z`} fill={`url(#${id}-ham)`} stroke={VIEN} strokeWidth={1} />
      {/* thân thước (chạy ra khỏi mép phải hình) */}
      <rect x={X0 - 22} y={T0} width={W - X0 + 30} height={BY - T0} fill={`url(#${id}-than)`} stroke={VIEN} strokeWidth={1} />
      <line x1={X0 - 22} x2={W + 8} y1={BY - 1} y2={BY - 1} stroke="#ffffff" strokeOpacity={0.6} />
      <g stroke={MUC} strokeWidth={1}>
        {main}
      </g>
      {/* con trượt: dải trên thân + tấm du xích + hàm động + mỏ trên + vít hãm + núm khía */}
      <rect x={xa} y={T0 - 6} width={xb - xa} height={6} fill={`url(#${id}-tam)`} stroke={VIEN} strokeWidth={1} />
      <path d={`M${xa},${T0 - 6} V4 L${xa + 4},4 L${xa + 16},${T0 - 6} Z`} fill={`url(#${id}-ham)`} stroke={VIEN} strokeWidth={1} />
      <rect x={xa + (xb - xa) * 0.55 - 6} y={6} width={12} height={10} rx={1.5} fill={`url(#${id}-khia)`} stroke="#4b5560" />
      <path
        d={`M${xa},${BY} H${xb - 4} Q${xb},${BY} ${xb},${BY + 4} V${P1 - 4} Q${xb},${P1} ${xb - 4},${P1} H${xa + 22} V110 L${xa + 8},142 L${xa + 3},146 L${xa},136 Z`}
        fill={`url(#${id}-tam)`}
        stroke={VIEN}
        strokeWidth={1}
      />
      <line x1={xa} x2={xb - 4} y1={BY + 0.6} y2={BY + 0.6} stroke="#5f6a74" strokeOpacity={0.5} />
      <g>{ver}</g>
      <rect x={xa + 28} y={P1 - 3} width={24} height={13} rx={3} fill={`url(#${id}-khia)`} stroke="#4b5560" />
      {/* khung kính lúp */}
      <rect
        x={x(c - wMm / 2)}
        y={1}
        width={wMm * S}
        height={P1 + 4}
        fill="none"
        stroke={XANH}
        strokeWidth={2}
        strokeDasharray="5 3"
        rx={3}
      />
      {xem && (
        <text x={xa + 28} y={120} fontSize={15} fill="var(--color-primary)">
          ⇆ kéo hàm
        </text>
      )}
    </svg>
  );
}

/* ---------------- Kính lúp ---------------- */

function KinhLup({ zH, pH, c, toTrung }: { zH: number; pH: LoaiDuXich; c: number; toTrung: boolean }) {
  const { N, len, nhanMoi } = DU_XICH[pH];
  const ppm = PPM[pH];
  const L = 12;
  const Rr = 348;
  const x = (mm: number) => (L + Rr) / 2 + (mm - c) * ppm;
  const inView = (px: number) => px >= L - 1 && px <= Rr + 1;
  const z = zH / 100;
  const { n, k } = tachThuocKep(zH, pH);
  const BY = 72; // đường ranh giới thước chính / du xích
  const id = `kl${useId().replace(/[^a-zA-Z0-9]/g, "")}`;

  const main: ReactNode[] = [];
  const j0 = Math.max(0, Math.floor(c - (Rr - L) / ppm / 2) - 1);
  const j1 = Math.ceil(c + (Rr - L) / ppm / 2) + 1;
  for (let j = j0; j <= j1; j++) {
    const px = x(j);
    if (!inView(px)) continue;
    const hl = toTrung && j === n + k;
    const h = j % 10 === 0 ? 34 : j % 5 === 0 ? 26 : 17;
    main.push(<line key={j} x1={px} x2={px} y1={BY} y2={BY - h} stroke={hl ? LUC : MUC} strokeWidth={hl ? 3 : 1.4} />);
    if ((ppm >= 40 || j % 5 === 0) && px > L + 12 && px < Rr - 12)
      main.push(
        <text key={`t${j}`} x={px} y={26} textAnchor="middle" fontSize={16} fontWeight={j % 5 === 0 ? 700 : 400} fill={MUC}>
          {j}
        </text>,
      );
  }

  const ver: ReactNode[] = [];
  for (let i = 0; i <= N; i++) {
    const px = x(z + (i * len) / N);
    if (!inView(px)) continue;
    const labeled = i % nhanMoi === 0;
    const hl = toTrung && i === k;
    const zero = i === 0;
    ver.push(
      <line
        key={i}
        x1={px}
        x2={px}
        y1={BY}
        y2={BY + (labeled ? 26 : 17)}
        stroke={hl ? LUC : zero ? XANH : MUC}
        strokeWidth={hl ? 3 : zero ? 2.4 : 1.4}
      />,
    );
    if (labeled && px > L + 8 && px < Rr - 8)
      ver.push(
        <text key={`v${i}`} x={px} y={BY + 44} textAnchor="middle" fontSize={16} fill={zero ? XANH_CHU : MUC}>
          {Math.round(i * pH * 0.1)}
        </text>,
      );
    if (hl)
      ver.push(
        <text key="trung" x={px} y={BY + 66} textAnchor="middle" fontSize={16} fontWeight={700} fill={LUC_CHU}>
          ✓ trùng
        </text>,
      );
  }

  const sx0 = Math.max(L, x(z));
  const sx1 = Math.min(Rr, x(z + len + 1));
  return (
    <svg viewBox={`0 0 ${W} 148`} className="block w-full select-none" role="img" aria-label="Kính lúp: phóng to chỗ đọc du xích">
      <MauThep id={id} />
      <defs>
        <radialGradient id={`${id}-toi`} cx="0.5" cy="0.5" r="0.75">
          <stop offset="0.6" stopColor="#000" stopOpacity={0} />
          <stop offset="1" stopColor="#000" stopOpacity={0.16} />
        </radialGradient>
        <clipPath id={`${id}-o`}>
          <rect x={L} y={3} width={Rr - L} height={142} rx={10} />
        </clipPath>
      </defs>
      <g clipPath={`url(#${id}-o)`}>
        {/* nền sau thước (khe giữa các chi tiết) */}
        <rect x={L} y={3} width={Rr - L} height={142} fill="#8e979f" />
        {/* thân thước */}
        <rect x={L} y={3} width={Rr - L} height={BY - 3} fill={`url(#${id}-than)`} />
        {/* tấm du xích (chỉ trong khoảng con trượt) */}
        {sx1 > sx0 && <rect x={sx0 - 6} y={BY} width={sx1 - sx0 + 6} height={80} fill={`url(#${id}-tam)`} />}
        {sx1 > sx0 && <line x1={sx0 - 6} x2={sx1} y1={BY + 1} y2={BY + 1} stroke="#4b5560" strokeOpacity={0.55} strokeWidth={1.5} />}
        {main}
        {ver}
        <rect x={L} y={3} width={Rr - L} height={142} fill={`url(#${id}-toi)`} />
      </g>
      <rect x={L} y={3} width={Rr - L} height={142} fill="none" stroke="#3f4852" strokeWidth={3} rx={10} />
    </svg>
  );
}

/* ---------------- Component chính ---------------- */

export default function ThuocKep() {
  const [cheDo, setCheDo] = useState<CheDo>("xem");
  const [pH, setPH] = useState<LoaiDuXich>(2);
  const [zXem, setZXem] = useState(1234);
  const [zLuyen, setZLuyen] = useState(() => 0);
  const [daCham, setDaCham] = useState(false);
  const [nhin, setNhin] = useState<"trung" | "zero" | number>("trung");
  const { tienDo, ghi } = useTienDo("thachlab:do-luong:thuoc-kep:v1");

  const { N, len, ten } = DU_XICH[pH];
  const xem = cheDo === "xem";
  const zH = xem ? zXem : zLuyen;
  const z = zH / 100;
  const { n, k } = tachThuocKep(zH, pH);
  const wMm = (348 - 12) / PPM[pH];
  const R = MAX_N + len + 3;

  const tamRaw = nhin === "trung" ? z + (k * len) / N : nhin === "zero" ? z : nhin;
  const c = Math.max(wMm / 2 - 1, Math.min(R - wMm / 2 + 1, tamRaw));

  const cauMoi = (p: LoaiDuXich = pH) => {
    setZLuyen((cu) => ngauNhienThuocKep(p, MAX_N, cu));
    setDaCham(false);
    setNhin("zero");
  };

  const doiCheDo = (v: CheDo) => {
    setCheDo(v);
    if (v === "luyen") cauMoi();
    else setNhin("trung");
  };
  const doiLoai = (p: LoaiDuXich) => {
    setPH(p);
    setZXem((zz) => kepZ(zz, p));
    if (!xem) cauMoi(p);
  };

  const onPointMm = (mm: number) => {
    if (xem) {
      setZXem(kepZ(mm * 100, pH));
      setNhin("trung");
    } else setNhin(mm);
  };

  const cauKey = `${pH}-${zLuyen}`;
  const xH = k * pH;
  const phanLe = soNguyenRaChuoi(DU_XICH[pH].decimals === 1 ? xH / 10 : xH, DU_XICH[pH].decimals);
  const pStr = soNguyenRaChuoi(pH, 2).replace(/0$/, "");
  const doc = ghiThuocKep(zH, pH);

  const buoc = useMemo(
    () => [
      {
        key: "zero" as const,
        text: (
          <>
            <b>Phần nguyên:</b> vạch 0 du xích (màu xanh) nằm ngay sau vạch <b>{n} mm</b> của thước chính → {n} mm.
          </>
        ),
      },
      {
        key: "trung" as const,
        text: (
          <>
            <b>Phần lẻ:</b> vạch số <b>{k}</b> của du xích thẳng hàng với một vạch thước chính → {k} × {pStr} = {phanLe} mm.
            {k === 0 && " (Vạch 0 trùng thì vạch cuối cũng trùng — đừng đếm vạch cuối.)"}
          </>
        ),
      },
    ],
    [n, k, pStr, phanLe],
  );

  return (
    <section className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5" aria-label="Thước kẹp du xích">
      <h2 className="font-display text-lg font-semibold">Thước kẹp: đọc số trên du xích</h2>
      <div className="mt-3 space-y-2">
        <ChonCheDo value={cheDo} onChange={doiCheDo} />
        <HangChon label="Du xích (mm)" items={LUA_CHON} value={pH} onChange={doiLoai} />
      </div>

      <div className="mt-3">
        <HinhToanThuoc zH={zH} pH={pH} c={c} wMm={wMm} onPointMm={onPointMm} xem={xem} />
        <div className="mt-2">
          <KinhLup zH={zH} pH={pH} c={c} toTrung={xem || daCham} />
        </div>
        <div className="mt-2 flex items-center gap-2">
          <button type="button" className={phuBtn} aria-label="Dời kính lúp sang trái" onClick={() => setNhin(c - wMm / 2)}>
            ◀
          </button>
          <p className="flex-1 text-center text-sm text-muted">dời kính lúp</p>
          <button type="button" className={phuBtn} aria-label="Dời kính lúp sang phải" onClick={() => setNhin(c + wMm / 2)}>
            ▶
          </button>
        </div>
      </div>

      {xem ? (
        <div className="mt-3 space-y-2">
          <div className="flex gap-2">
            <button type="button" className={`${phuBtn} flex-1`} onClick={() => (setZXem((zz) => kepZ(zz - pH, pH)), setNhin("trung"))}>
              − {pStr} mm
            </button>
            <button type="button" className={`${phuBtn} flex-1`} onClick={() => (setZXem((zz) => kepZ(zz + pH, pH)), setNhin("trung"))}>
              + {pStr} mm
            </button>
          </div>
          <ol className="space-y-2 text-base leading-relaxed">
            {buoc.map((b, i) => (
              <li key={b.key}>
                <button
                  type="button"
                  onClick={() => setNhin(b.key)}
                  className={`w-full rounded-lg px-3 py-2 text-left ${nhin === b.key ? "bg-primary-soft" : "bg-surface-2"}`}
                >
                  {i + 1}. {b.text}
                </button>
              </li>
            ))}
            <li className="rounded-lg border border-line-strong px-3 py-2">
              3. <b>Số đọc:</b> L = {n} + {phanLe} = <b>{doc} mm</b>.
            </li>
          </ol>
          <p className="text-sm text-muted">
            Bấm bước 1 hoặc 2 để kính lúp nhảy tới chỗ cần nhìn. Đo một lần thì ghi L = ({doc} ± {pStr}) mm: du xích không ước được nửa
            vạch nên sai số dụng cụ lấy bằng độ chính xác {ten}.
          </p>
        </div>
      ) : (
        <div className="mt-3">
          <LuyenDoc
            cauKey={cauKey}
            donVi="mm"
            nhan={<>Thước kẹp (du xích {ten}) chỉ bao nhiêu?</>}
            cham={(raw) => chamThuocKep(raw, zLuyen, pH)}
            onDaCham={(kq) => {
              setDaCham(true);
              setNhin("trung");
              ghi(String(pH), kq.loai === "dung");
            }}
            onCauMoi={() => cauMoi()}
            tienDo={tienDo[String(pH)]}
            tenNhiemVu={`du xích ${ten}`}
          />
        </div>
      )}
    </section>
  );
}
