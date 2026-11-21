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

import { useMemo, useRef, useState, type PointerEvent, type ReactNode } from "react";
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

  const toMm = (e: PointerEvent<SVGSVGElement>) => {
    const r = ref.current!.getBoundingClientRect();
    return ((e.clientX - r.left) / r.width) * W - X0;
  };

  const main: ReactNode[] = [];
  for (let j = 0; j <= R; j++) {
    const h = j % 10 === 0 ? 13 : j % 5 === 0 ? 8 : 5;
    main.push(<line key={j} x1={x(j)} x2={x(j)} y1={50} y2={50 - h} />);
    if (j % 10 === 0)
      main.push(
        <text key={`t${j}`} x={x(j)} y={31} textAnchor="middle" fontSize={16} fill="currentColor" stroke="none">
          {j}
        </text>,
      );
  }
  const ver: ReactNode[] = [];
  for (let i = 0; i <= N; i++) {
    const xi = x(z + (i * len) / N);
    ver.push(<line key={i} x1={xi} x2={xi} y1={50} y2={50 + (i % DU_XICH[pH].nhanMoi === 0 ? 9 : 5)} />);
  }

  return (
    <svg
      ref={ref}
      viewBox={`0 0 ${W} 126`}
      className="block w-full select-none text-ink"
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
      {/* thước chính + hàm cố định */}
      <path
        d={`M${X0 - 16},12 H${X1 + 6} V50 H${X0} V118 H${X0 - 16} Z`}
        fill="var(--color-panel)"
        stroke="currentColor"
        strokeWidth={1.5}
      />
      <g stroke="currentColor" strokeWidth={1}>
        {main}
      </g>
      {/* vật được kẹp */}
      {z > 0.3 && (
        <rect x={X0} y={92} width={x(z) - X0} height={26} fill="var(--color-warn)" fillOpacity={0.18} stroke="var(--color-warn)" />
      )}
      {/* con trượt + hàm động */}
      <path
        d={`M${x(z)},50 H${x(z + len + 2)} V80 H${x(z) + 16} V118 H${x(z)} Z`}
        fill="var(--color-primary-soft)"
        stroke="var(--color-primary)"
        strokeWidth={1.5}
      />
      <g stroke="currentColor" strokeWidth={1}>
        {ver}
      </g>
      {/* khung kính lúp */}
      <rect
        x={x(c - wMm / 2)}
        y={6}
        width={wMm * S}
        height={82}
        fill="none"
        stroke="var(--color-primary)"
        strokeWidth={2}
        strokeDasharray="5 3"
        rx={3}
      />
      {xem && (
        <text x={x(z) + 22} y={110} fontSize={16} fill="var(--color-primary)">
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

  const main: ReactNode[] = [];
  const j0 = Math.max(0, Math.floor(c - (Rr - L) / ppm / 2) - 1);
  const j1 = Math.ceil(c + (Rr - L) / ppm / 2) + 1;
  for (let j = j0; j <= j1; j++) {
    const px = x(j);
    if (!inView(px)) continue;
    const hl = toTrung && j === n + k;
    const h = j % 10 === 0 ? 34 : j % 5 === 0 ? 26 : 17;
    main.push(
      <line
        key={j}
        x1={px}
        x2={px}
        y1={BY}
        y2={BY - h}
        stroke={hl ? "var(--color-ok)" : "currentColor"}
        strokeWidth={hl ? 3 : 1.4}
      />,
    );
    if ((ppm >= 40 || j % 5 === 0) && px > L + 12 && px < Rr - 12)
      main.push(
        <text key={`t${j}`} x={px} y={26} textAnchor="middle" fontSize={16} fontWeight={j % 5 === 0 ? 700 : 400} fill="currentColor">
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
        stroke={hl ? "var(--color-ok)" : zero ? "var(--color-primary)" : "currentColor"}
        strokeWidth={hl ? 3 : zero ? 2.4 : 1.4}
      />,
    );
    if (labeled && px > L + 8 && px < Rr - 8)
      ver.push(
        <text key={`v${i}`} x={px} y={BY + 44} textAnchor="middle" fontSize={16} fill={zero ? "var(--color-primary)" : "currentColor"}>
          {Math.round(i * pH * 0.1)}
        </text>,
      );
    if (hl)
      ver.push(
        <text key="trung" x={px} y={BY + 66} textAnchor="middle" fontSize={16} fontWeight={700} fill="var(--color-ok)">
          ✓ trùng
        </text>,
      );
  }

  const sx0 = Math.max(L, x(z - 0.6));
  const sx1 = Math.min(Rr, x(z + len + 1));
  return (
    <svg viewBox={`0 0 ${W} 146`} className="block w-full select-none text-ink" role="img" aria-label="Kính lúp: phóng to chỗ đọc du xích">
      <rect x={L} y={2} width={Rr - L} height={BY - 2} fill="var(--color-panel)" />
      {sx1 > sx0 && <rect x={sx0} y={BY} width={sx1 - sx0} height={72} fill="var(--color-primary-soft)" />}
      <line x1={L} x2={Rr} y1={BY} y2={BY} stroke="currentColor" strokeWidth={1} />
      {main}
      {ver}
      <rect x={L} y={2} width={Rr - L} height={142} fill="none" stroke="var(--color-line-strong)" rx={6} />
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
