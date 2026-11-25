"use client";

/**
 * components/physics/do-luong/DongHoDaNang.tsx — đồng hồ đo điện đa năng hiện số (Gói A, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 3).
 * Gắn vào L10 Bài 2 (lesson 47) và L11 Thực hành đo suất điện động (lesson 45) qua MoPhongPortals khoá "dong-ho-da-nang".
 * Tự dựng, không lấy gì từ trang khác.
 *
 * Học sinh vặn núm (V⎓, V~, A⎓, Ω), chọn thang, cắm que đỏ (10A, mA, VΩ; que đen luôn ở COM), chọn mắc song song / nối tiếp,
 * rồi bấm "Chạm que". Đặt sai thì đồng hồ phản ứng như máy thật: quá thang hiện "1", chập mạch qua lỗ mA đứt cầu chì,
 * thang Ω trên mạch có điện bị cảnh báo; số học trong cham.ts (doDongHo).
 * Xem cách đọc (N6): bốn bước đặt máy cho từng tình huống + nút "Đặt đúng cho em xem". Luyện: tình huống ngẫu nhiên, chỉ lần
 * chạm que ĐẦU TIÊN được tính, đúng 5 lần liên tiếp là xong (L1, L2, L3, L4). Quy tắc UI: N2 (≤ 4 nút mỗi hàng), D2, C1/H4,
 * M1/M7, M4 (✓/✗/⚠ kèm chữ), B4.
 */

import { useId, useState } from "react";
import { ChonCheDo, DAT_LIEN_TIEP, HangChon, phuBtn, useTienDo, type CheDo } from "./chung";
import {
  SO_MAU_DH,
  TEN_DL,
  THANG_DH,
  cauHinhDung,
  doDongHo,
  manHinhDH,
  taoNhiemVuDH,
  type CachMac,
  type CauHinhDH,
  type DaiLuongDH,
  type KetQuaDo,
  type LoCam,
  type NhiemVuDH,
} from "./cham";

const DL_ITEMS: { value: DaiLuongDH; text: string }[] = (["DCV", "ACV", "DCA", "OHM"] as const).map((v) => ({
  value: v,
  text: TEN_DL[v],
}));
const LO_ITEMS: { value: LoCam; text: string }[] = [
  { value: "10A", text: "10A" },
  { value: "mA", text: "mA" },
  { value: "VΩ", text: "VΩ" },
];
const MAC_ITEMS: { value: CachMac; text: string }[] = [
  { value: "song-song", text: "Song song" },
  { value: "noi-tiep", text: "Nối tiếp" },
];
const KHOA = "cach-do";

/* ---------------- Hình đồng hồ ---------------- */

/*
 * Máy vẽ như "ảnh" vật thật (cùng cách với ThuocKep): màu CỐ ĐỊNH, không currentColor, giữ nguyên ở chế độ tối.
 * Vỏ nhựa cam bọc cao su, mặt máy xám đen, màn LCD xám xanh số 7 đoạn, núm xoay có mũi chỉ, vòng thang in quanh núm,
 * hàng lỗ cắm 10A · mA · COM · VΩ, hai que đo đỏ/đen có dây. Không ghi tên hãng.
 * Tương phản chữ (tự tính): trắng #f3f4f6 / vàng #fde047 trên mặt #2b3036 ≥ 11:1; chữ đen #111a12 trên LCD #b6c2a2 ≈ 10:1;
 * chữ trắng trên nhãn đỏ #b91c1c ≈ 6,4:1. Cỡ chữ nhỏ nhất 15 đơn vị viewBox (≈ 13,2 px khi SVG rộng 317 px, bề rộng thật ở màn 375 px).
 */
const W_VB = 360;
const H_VB = 342;
/** Tâm núm xoay. */
const NX = 130;
const NY = 194;
/** Góc giữa (độ, tính từ phía trên theo chiều kim đồng hồ) của từng vùng thang trên vòng in quanh núm. */
const GOC_VUNG: Record<DaiLuongDH, number> = { DCV: -45, ACV: 45, DCA: 135, OHM: 225 };
const NUA_VUNG = 30;
const JACK_Y = 288;
const JACK: { lo: LoCam | "COM"; x: number }[] = [
  { lo: "10A", x: 50 },
  { lo: "mA", x: 100 },
  { lo: "COM", x: 160 },
  { lo: "VΩ", x: 210 },
];
const QUE_DO_X = 332;
const QUE_DEN_X = 290;

const MAU = {
  vo: "#ea7a1a",
  voToi: "#b4560f",
  mat: "#2b3036",
  matVien: "#16191c",
  chu: "#f3f4f6",
  chuChon: "#fde047",
  lcdChu: "#111a12",
  doLo: "#d42020",
  do: "#c81e1e",
  den: "#1b1d20",
  denVien: "#8b939c",
};

/** Góc (độ) của vạch thang i trong vùng d. */
function gocThang(d: DaiLuongDH, i: number): number {
  const n = THANG_DH[d].length;
  return GOC_VUNG[d] - NUA_VUNG + ((i + 0.5) * 2 * NUA_VUNG) / n;
}
function diem(goc: number, r: number): [number, number] {
  const a = (goc * Math.PI) / 180;
  return [NX + r * Math.sin(a), NY - r * Math.cos(a)];
}

function MauDongHo({ id }: { id: string }) {
  return (
    <defs>
      <linearGradient id={`${id}-vo`} x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#f7a04a" />
        <stop offset="0.5" stopColor={MAU.vo} />
        <stop offset="1" stopColor={MAU.voToi} />
      </linearGradient>
      <linearGradient id={`${id}-mat`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#353b42" />
        <stop offset="1" stopColor={MAU.mat} />
      </linearGradient>
      <linearGradient id={`${id}-lcd`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#c3ceb0" />
        <stop offset="1" stopColor="#aebb99" />
      </linearGradient>
      <radialGradient id={`${id}-num`} cx="0.4" cy="0.35" r="0.75">
        <stop offset="0" stopColor="#4d545c" />
        <stop offset="1" stopColor="#1a1d21" />
      </radialGradient>
      <linearGradient id={`${id}-tay`} x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#5c636b" />
        <stop offset="0.5" stopColor="#3a4047" />
        <stop offset="1" stopColor="#24282d" />
      </linearGradient>
      <linearGradient id={`${id}-queDo`} x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#8f1414" />
        <stop offset="0.4" stopColor="#e23a3a" />
        <stop offset="1" stopColor="#9b1717" />
      </linearGradient>
      <linearGradient id={`${id}-queDen`} x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#0d0e10" />
        <stop offset="0.4" stopColor="#3b4046" />
        <stop offset="1" stopColor="#0d0e10" />
      </linearGradient>
      <linearGradient id={`${id}-kim`} x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#9aa3ab" />
        <stop offset="0.5" stopColor="#f1f3f5" />
        <stop offset="1" stopColor="#8a939b" />
      </linearGradient>
      <pattern id={`${id}-gai`} width="4" height="4" patternUnits="userSpaceOnUse">
        <rect width="4" height="4" fill={MAU.vo} />
        <rect width="4" height="1.6" fill={MAU.voToi} opacity="0.55" />
      </pattern>
    </defs>
  );
}

/* Màn 7 đoạn: 4 ô số (3½ chữ số), có bóng mờ các đoạn tắt như LCD thật. */
const DOAN: Record<string, string> = {
  "0": "abcdef",
  "1": "bc",
  "2": "abged",
  "3": "abgcd",
  "4": "fgbc",
  "5": "afgcd",
  "6": "afgedc",
  "7": "abc",
  "8": "abcdefg",
  "9": "abcdfg",
  "-": "g",
  "—": "g",
};
const SO_O = 4;
const O_X0 = 54;
const O_BUOC = 36;
const O_W = 25;
const O_H = 46;
const O_Y = 44;
const O_T = 5.5;
const NGHIENG = 0.1;

function ngang(x1: number, x2: number, y: number) {
  const h = O_T / 2;
  return `${x1},${y} ${x1 + h},${y - h} ${x2 - h},${y - h} ${x2},${y} ${x2 - h},${y + h} ${x1 + h},${y + h}`;
}
function doc(x: number, y1: number, y2: number) {
  const h = O_T / 2;
  return `${x},${y1} ${x + h},${y1 + h} ${x + h},${y2 - h} ${x},${y2} ${x - h},${y2 - h} ${x - h},${y1 + h}`;
}
function hinhDoan(x0: number): Record<string, string> {
  const g = 1.2;
  const y0 = O_Y;
  const ym = O_Y + O_H / 2;
  const y1 = O_Y + O_H;
  return {
    a: ngang(x0 + g, x0 + O_W - g, y0),
    g: ngang(x0 + g, x0 + O_W - g, ym),
    d: ngang(x0 + g, x0 + O_W - g, y1),
    f: doc(x0, y0 + g, ym - g),
    b: doc(x0 + O_W, y0 + g, ym - g),
    e: doc(x0, ym + g, y1 - g),
    c: doc(x0 + O_W, ym + g, y1 - g),
  };
}

type O = { doan: string; dp: boolean };
/** Tách chữ trên màn thành các ô 7 đoạn; null nếu có ký tự không vẽ được (khi đó in chữ thường). */
function tachO(man: string, quaThang: boolean): (O | null)[] | null {
  const ds: O[] = [];
  for (const k of man) {
    if (k === "." || k === ",") {
      if (ds.length === 0) ds.push({ doan: "", dp: false });
      ds[ds.length - 1].dp = true;
    } else if (k in DOAN) ds.push({ doan: DOAN[k], dp: false });
    else if (k !== " ") return null;
  }
  if (ds.length > SO_O) return null;
  const trong: null[] = Array(SO_O - ds.length).fill(null);
  return quaThang ? [...ds, ...trong] : [...trong, ...ds];
}

function ManLCD({ man, donVi, quaThang }: { man: string; donVi: string; quaThang: boolean }) {
  const o = tachO(man, quaThang);
  const skew = `matrix(1,0,${-NGHIENG},1,${NGHIENG * (O_Y + O_H)},0)`;
  return (
    <g>
      {o ? (
        <g transform={skew}>
          {Array.from({ length: SO_O }, (_, i) => {
            const x0 = O_X0 + i * O_BUOC;
            const hd = hinhDoan(x0);
            const cell = o[i];
            return (
              <g key={i}>
                {Object.entries(hd).map(([k, p]) => (
                  <polygon
                    key={k}
                    points={p}
                    fill={cell?.doan.includes(k) ? MAU.lcdChu : "#9eab8a"}
                    opacity={cell?.doan.includes(k) ? 1 : 0.45}
                  />
                ))}
                {i < SO_O - 1 && (
                  <rect
                    x={x0 + O_W + 3.5}
                    y={O_Y + O_H - 2.8}
                    width={5}
                    height={5}
                    fill={cell?.dp ? MAU.lcdChu : "#9eab8a"}
                    opacity={cell?.dp ? 1 : 0.45}
                  />
                )}
              </g>
            );
          })}
        </g>
      ) : (
        <text
          x={186}
          y={O_Y + O_H}
          textAnchor="end"
          fontSize={42}
          fontFamily="ui-monospace, monospace"
          fontWeight={700}
          fill={MAU.lcdChu}
        >
          {man}
        </text>
      )}
      <text x={222} y={O_Y + O_H} textAnchor="end" fontSize={18} fontWeight={700} fill={MAU.lcdChu}>
        {donVi}
      </text>
    </g>
  );
}

/** Que đo đứng ở bên phải máy: mũi kim loại, gờ chắn tay, cán, đuôi chống gập. */
function QueDo({ x, mau, id }: { x: number; mau: "do" | "den"; id: string }) {
  const fill = `url(#${id}-${mau === "do" ? "queDo" : "queDen"})`;
  const vien = mau === "do" ? "#6f0f0f" : MAU.denVien;
  return (
    <g>
      <rect x={x - 1.6} y={14} width={3.2} height={44} rx={1.4} fill={`url(#${id}-kim)`} />
      <path d={`M${x - 3},58 L${x + 3},58 L${x + 5},66 L${x - 5},66 Z`} fill={fill} stroke={vien} strokeWidth={0.8} />
      <rect x={x - 13} y={66} width={26} height={8} rx={3} fill={fill} stroke={vien} strokeWidth={0.8} />
      <rect x={x - 8} y={74} width={16} height={120} rx={6} fill={fill} stroke={vien} strokeWidth={0.8} />
      {[96, 104, 112, 120, 128].map((y) => (
        <line key={y} x1={x - 6} y1={y} x2={x + 6} y2={y} stroke={vien} strokeWidth={1} opacity={0.7} />
      ))}
      <path d={`M${x - 8},192 L${x + 8},192 L${x + 4},224 L${x - 4},224 Z`} fill={fill} stroke={vien} strokeWidth={0.8} />
    </g>
  );
}

function HinhDongHo({
  ch,
  man,
  donVi,
  chiDut,
  qua,
}: {
  ch: CauHinhDH;
  man: string;
  donVi: string;
  chiDut: boolean;
  qua?: boolean;
}) {
  const th = THANG_DH[ch.dl][ch.thang];
  const id = `dh${useId().replace(/[^a-zA-Z0-9]/g, "")}`;
  const gocNum = gocThang(ch.dl, ch.thang);
  // Quá thang: cờ từ kết quả chấm; khi chưa chạm que mà màn chờ "1" (thang Ω, mạch hở) thì mọi thang Ω đều có phần thập phân.
  const quaThang = qua ?? (man === "1" && th.decimals > 0);
  const loDo = JACK.find((j) => j.lo === ch.lo)!;
  const loDen = JACK.find((j) => j.lo === "COM")!;
  const day = (jx: number, qx: number) => `M${jx},${JACK_Y + 12} C${jx},${H_VB + 8} ${qx},${H_VB + 6} ${qx},224`;
  return (
    <svg
      viewBox={`0 0 ${W_VB} ${H_VB}`}
      className="mx-auto block w-full max-w-[420px] select-none"
      role="img"
      aria-label={`Đồng hồ đa năng: núm ${TEN_DL[ch.dl]} thang ${th.ten}, que đỏ lỗ ${ch.lo}. Màn hiện ${man} ${donVi}.`}
    >
      <MauDongHo id={id} />
      {/* vỏ nhựa cam bọc cao su */}
      <rect x={6} y={4} width={248} height={318} rx={26} fill={`url(#${id}-vo)`} stroke={MAU.voToi} strokeWidth={2} />
      <rect x={6} y={120} width={8} height={90} rx={3} fill={`url(#${id}-gai)`} />
      <rect x={246} y={120} width={8} height={90} rx={3} fill={`url(#${id}-gai)`} />
      {/* mặt máy */}
      <rect x={18} y={16} width={224} height={294} rx={14} fill={`url(#${id}-mat)`} stroke={MAU.matVien} strokeWidth={1.5} />
      {/* màn LCD trong khung */}
      <rect x={28} y={26} width={204} height={82} rx={8} fill="#121417" />
      <rect x={36} y={34} width={188} height={66} rx={4} fill={`url(#${id}-lcd)`} />
      <ManLCD man={man} donVi={donVi} quaThang={quaThang} />
      {chiDut ? (
        <g>
          <rect x={58} y={112} width={144} height={24} rx={6} fill="#b91c1c" />
          <text x={130} y={129} textAnchor="middle" fontSize={15} fontWeight={700} fill="#ffffff">
            ⚠ cầu chì đứt
          </text>
        </g>
      ) : (
        <text x={130} y={129} textAnchor="middle" fontSize={15} fontWeight={600} letterSpacing={0.8} fill={MAU.chu}>
          DIGITAL MULTIMETER
        </text>
      )}
      {/* vòng thang in quanh núm: mỗi vùng một đại lượng, mỗi vạch một thang */}
      <circle cx={NX} cy={NY} r={47} fill="none" stroke="#4a5058" strokeWidth={1} />
      {(Object.keys(GOC_VUNG) as DaiLuongDH[]).map((d) => {
        const chon = d === ch.dl;
        const [lx, ly] = diem(GOC_VUNG[d], 70);
        return (
          <g key={d}>
            {THANG_DH[d].map((_, i) => {
              const g = gocThang(d, i);
              const dangChon = chon && i === ch.thang;
              const [x1, y1] = diem(g, 40);
              const [x2, y2] = diem(g, dangChon ? 54 : 49);
              return (
                <line
                  key={i}
                  x1={x1}
                  y1={y1}
                  x2={x2}
                  y2={y2}
                  stroke={dangChon ? MAU.chuChon : MAU.chu}
                  strokeWidth={dangChon ? 3.5 : 2}
                  strokeLinecap="round"
                />
              );
            })}
            <text
              x={lx}
              y={ly + 6}
              textAnchor="middle"
              fontSize={chon ? 19 : 17}
              fontWeight={chon ? 800 : 600}
              fill={chon ? MAU.chuChon : MAU.chu}
            >
              {TEN_DL[d]}
            </text>
          </g>
        );
      })}
      {/* núm xoay: tay nắm có mũi chỉ trắng, xoay theo thang đang chọn */}
      <circle cx={NX} cy={NY} r={34} fill={`url(#${id}-num)`} stroke="#0e1012" strokeWidth={1.5} />
      <g
        className="motion-safe:transition-transform motion-safe:duration-300"
        style={{ transform: `rotate(${gocNum}deg)`, transformOrigin: `${NX}px ${NY}px` }}
      >
        <rect x={NX - 9} y={NY - 36} width={18} height={72} rx={8} fill={`url(#${id}-tay)`} stroke="#0e1012" />
        <path d={`M${NX},${NY - 35} L${NX + 5},${NY - 24} L${NX - 5},${NY - 24} Z`} fill="#ffffff" />
        <line x1={NX} y1={NY - 24} x2={NX} y2={NY - 10} stroke="#ffffff" strokeWidth={3} strokeLinecap="round" />
      </g>
      {/* hàng lỗ cắm */}
      {JACK.map((j) => {
        const den = j.lo === "COM";
        return (
          <g key={j.lo}>
            <text
              x={j.x}
              y={JACK_Y - 20}
              textAnchor="middle"
              fontSize={15}
              fontWeight={700}
              fill={j.lo === ch.lo || den ? MAU.chuChon : MAU.chu}
            >
              {j.lo}
            </text>
            <circle
              cx={j.x}
              cy={JACK_Y}
              r={12}
              fill={den ? MAU.den : MAU.doLo}
              stroke={den ? MAU.denVien : "#7a1010"}
              strokeWidth={1.2}
            />
            <circle cx={j.x} cy={JACK_Y} r={6.5} fill="#050607" stroke="#5a6068" strokeWidth={1} />
          </g>
        );
      })}
      {/* dây que: viền sáng để dây đen vẫn thấy ở chế độ tối */}
      <path d={day(loDen.x, QUE_DEN_X)} fill="none" stroke={MAU.denVien} strokeWidth={6.5} strokeLinecap="round" />
      <path d={day(loDen.x, QUE_DEN_X)} fill="none" stroke={MAU.den} strokeWidth={4} strokeLinecap="round" />
      <path d={day(loDo.x, QUE_DO_X)} fill="none" stroke="#7a1010" strokeWidth={6.5} strokeLinecap="round" />
      <path d={day(loDo.x, QUE_DO_X)} fill="none" stroke={MAU.do} strokeWidth={4} strokeLinecap="round" />
      {/* phích cắm trong lỗ */}
      {[
        { j: loDen, f: `url(#${id}-queDen)`, v: MAU.denVien },
        { j: loDo, f: `url(#${id}-queDo)`, v: "#6f0f0f" },
      ].map(({ j, f, v }) => (
        <g key={j.lo}>
          <rect x={j.x - 8} y={JACK_Y - 8} width={16} height={24} rx={5} fill={f} stroke={v} strokeWidth={1} />
        </g>
      ))}
      <QueDo x={QUE_DO_X} mau="do" id={id} />
      <QueDo x={QUE_DEN_X} mau="den" id={id} />
    </svg>
  );
}

/* ---------------- Component chính ---------------- */

function moiNhiemVuNgauNhien(cu?: NhiemVuDH): NhiemVuDH {
  for (let lan = 0; lan < 10; lan++) {
    const nv = taoNhiemVuDH(Math.floor(Math.random() * SO_MAU_DH));
    if (!cu || nv.de !== cu.de) return nv;
  }
  return taoNhiemVuDH(0);
}

const KY_HIEU: Record<KetQuaDo["loai"], { t: string; cls: string }> = {
  dung: { t: "✓ Đúng.", cls: "text-ok" },
  "chua-toi-uu": { t: "≈ Đo được, chưa tốt nhất.", cls: "text-warn" },
  sai: { t: "✗ Chưa đúng.", cls: "text-danger" },
  "nguy-hiem": { t: "⚠ Nguy hiểm.", cls: "text-danger" },
};

export default function DongHoDaNang() {
  const [cheDo, setCheDo] = useState<CheDo>("xem");
  const [iXem, setIXem] = useState(0);
  const [nvLuyen, setNvLuyen] = useState<NhiemVuDH>(() => taoNhiemVuDH(0));
  const [ch, setCh] = useState<CauHinhDH>({ dl: "DCV", thang: 3, lo: "VΩ", mac: "song-song" });
  const [kq, setKq] = useState<KetQuaDo | null>(null);
  const [chiDut, setChiDut] = useState(false);
  const [daTinh, setDaTinh] = useState(false);
  const { tienDo, ghi } = useTienDo("thachlab:do-luong:dong-ho-da-nang:v1");

  const xem = cheDo === "xem";
  const nv = xem ? taoNhiemVuDH(iXem, false) : nvLuyen;
  const th = THANG_DH[ch.dl][ch.thang];
  const td = tienDo[KHOA];

  const doiCh = (p: Partial<CauHinhDH>) => {
    setCh((c) => {
      const n = { ...c, ...p };
      if (p.dl && p.dl !== c.dl) n.thang = THANG_DH[p.dl].length - 1; // đổi đại lượng: về thang lớn nhất cho an toàn
      return n;
    });
    setKq(null);
  };

  const cham = (c: CauHinhDH = ch) => {
    const r = doDongHo(nv, c, chiDut);
    setKq(r);
    if (r.chiDut) setChiDut(true);
    if (!xem && !daTinh) {
      setDaTinh(true);
      ghi(KHOA, r.loai === "dung");
    }
  };

  const doiCheDo = (v: CheDo) => {
    setCheDo(v);
    setKq(null);
    setChiDut(false);
    if (v === "luyen") {
      setNvLuyen((cu) => moiNhiemVuNgauNhien(cu));
      setDaTinh(false);
    }
  };
  const cauMoi = () => {
    setNvLuyen((cu) => moiNhiemVuNgauNhien(cu));
    setKq(null);
    setChiDut(false);
    setDaTinh(false);
  };
  const doiTinhHuong = (d: number) => {
    setIXem((i) => (i + d + SO_MAU_DH) % SO_MAU_DH);
    setKq(null);
    setChiDut(false);
  };

  const dung = cauHinhDung(nv);
  const manCho = ch.dl === "OHM" ? "1" : manHinhDH(0, th);

  return (
    <section
      className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
      aria-label="Đồng hồ đo điện đa năng"
    >
      <h2 className="font-display text-lg font-semibold">Đồng hồ đa năng: đặt máy đúng trước khi đo</h2>
      <div className="mt-3">
        <ChonCheDo value={cheDo} onChange={doiCheDo} />
      </div>

      <div className="mt-3 rounded-xl border border-line bg-surface-2 p-3">
        {xem && (
          <div className="mb-2 flex items-center gap-2">
            <button type="button" className={phuBtn} aria-label="Tình huống trước" onClick={() => doiTinhHuong(-1)}>
              ◀
            </button>
            <p className="flex-1 text-center text-sm text-muted">
              Tình huống {iXem + 1}/{SO_MAU_DH}
            </p>
            <button type="button" className={phuBtn} aria-label="Tình huống sau" onClick={() => doiTinhHuong(1)}>
              ▶
            </button>
          </div>
        )}
        <p className="text-base font-medium">{nv.de}</p>
      </div>

      <div className="mt-3">
        <HinhDongHo ch={ch} man={kq ? kq.man : manCho} donVi={kq ? kq.donVi : th.donVi} chiDut={chiDut} qua={kq?.qua} />
      </div>

      <div className="mt-3 space-y-2">
        <HangChon labelTren label="Núm vặn" items={DL_ITEMS} value={ch.dl} onChange={(v) => doiCh({ dl: v })} />
        <HangChon labelTren
          label="Thang"
          items={THANG_DH[ch.dl].map((t, i) => ({ value: i, text: t.ten }))}
          value={ch.thang}
          onChange={(v) => doiCh({ thang: v })}
        />
        <HangChon labelTren label="Que đỏ cắm lỗ (que đen luôn ở COM)" items={LO_ITEMS} value={ch.lo} onChange={(v) => doiCh({ lo: v })} />
        <HangChon labelTren label="Cách mắc que" items={MAC_ITEMS} value={ch.mac} onChange={(v) => doiCh({ mac: v })} />
        <div className="flex gap-2">
          <button
            type="button"
            className="min-h-11 flex-1 rounded-lg bg-primary px-4 text-sm font-semibold text-white"
            onClick={() => cham()}
          >
            Chạm que, đọc số
          </button>
          {chiDut && (
            <button
              type="button"
              className={phuBtn}
              onClick={() => {
                setChiDut(false);
                setKq(null);
              }}
            >
              Thay cầu chì
            </button>
          )}
        </div>
      </div>

      {kq && (
        <p className="mt-3 text-base leading-relaxed" aria-live="polite">
          <span className={`font-semibold ${KY_HIEU[kq.loai].cls}`}>{KY_HIEU[kq.loai].t}</span> {kq.loi}
        </p>
      )}

      {xem ? (
        <div className="mt-3 space-y-2">
          <ol className="space-y-2 text-base leading-relaxed">
            <li className="rounded-lg bg-surface-2 px-3 py-2">
              1. <b>Núm:</b> chọn đại lượng cần đo → <b>{TEN_DL[dung.dl]}</b>
              {dung.dl === "DCV" ? " (một chiều)" : dung.dl === "ACV" ? " (xoay chiều)" : ""}.
            </li>
            <li className="rounded-lg bg-surface-2 px-3 py-2">
              2. <b>Thang:</b> nhỏ nhất mà vẫn lớn hơn giá trị ước lượng → <b>{THANG_DH[dung.dl][dung.thang].ten}</b>.
              Chưa ước lượng được thì bắt đầu từ thang lớn nhất rồi hạ dần.
            </li>
            <li className="rounded-lg bg-surface-2 px-3 py-2">
              3. <b>Que đỏ:</b> lỗ <b>{dung.lo}</b>
              {dung.lo === "VΩ"
                ? " (đo V và Ω)"
                : dung.lo === "mA"
                  ? " (dòng nhỏ hơn 200 mA)"
                  : " (dòng từ 200 mA trở lên)"}
              ; que đen ở COM.
            </li>
            <li className="rounded-lg bg-surface-2 px-3 py-2">
              4. <b>Mắc:</b>{" "}
              {dung.dl === "DCA" ? (
                <>
                  <b>nối tiếp</b>: ngắt mạch một chỗ rồi nối đồng hồ vào chỗ hở.
                </>
              ) : dung.dl === "OHM" ? (
                <>
                  <b>song song</b> hai đầu điện trở đã tháo khỏi mạch, không có điện.
                </>
              ) : (
                <>
                  <b>song song</b>: chạm hai que vào hai cực.
                </>
              )}
            </li>
          </ol>
          <button
            type="button"
            className={`${phuBtn} w-full`}
            onClick={() => {
              setCh(dung);
              setChiDut(false);
              cham(dung);
            }}
          >
            Đặt đúng cho em xem
          </button>
          <p className="text-sm text-muted">
            Thử đặt sai (thang quá nhỏ, que đỏ ở lỗ mA khi đo pin…) để xem đồng hồ phản ứng thế nào.
          </p>
        </div>
      ) : (
        <div className="mt-3 space-y-2">
          {kq && (
            <button
              type="button"
              className="min-h-11 w-full rounded-lg bg-primary px-4 text-sm font-semibold text-white"
              onClick={cauMoi}
            >
              Tình huống khác
            </button>
          )}
          <p className="text-sm text-muted">
            {td?.done ? (
              <span className="font-semibold text-ok">✓ Đã xong nhiệm vụ đặt đồng hồ.</span>
            ) : (
              <>
                Chỉ lần chạm que đầu tiên mỗi tình huống được tính. Đặt đúng liên tiếp{" "}
                {Math.min(td?.streak ?? 0, DAT_LIEN_TIEP)}/{DAT_LIEN_TIEP} lần là xong.
              </>
            )}
          </p>
        </div>
      )}
    </section>
  );
}
