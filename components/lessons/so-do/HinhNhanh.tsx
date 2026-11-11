import type { SoDoNhanh } from "@/features/lessons/so-do-tu-duy/types";

/**
 * Hình khoá của từng nhánh sơ đồ tư duy — mỗi nhánh MỘT hình gợi lại cả nhánh (mã hoá kép: Paivio 1986; H1, H3, H4).
 * Nét 2px `currentColor`, nền trong suốt (M5). Quy ước màu cả chương (thầy chốt 5/11/2026): B xanh · I cam · F đỏ;
 * nam châm N đỏ – S xanh như `bar_magnet` trong svg_lib.py; đường sức nét đứt, mũi chevron (AGENTS).
 */
const B = "#2563eb",
  I = "#ea580c",
  F = "#dc2626";

const chu = { fontSize: 12, fontWeight: 700, fontStyle: "italic" as const };

function TuTruong() {
  return (
    <>
      <g fill="none" stroke={B} strokeWidth={1.6} strokeDasharray="4 3">
        <path d="M30 27 C 8 2, 88 2, 66 27" />
        <path d="M30 37 C 8 62, 88 62, 66 37" />
      </g>
      <g fill="none" stroke={B} strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round">
        <polyline points="45,5 50,8.2 45,11.4" />
        <polyline points="45,52.6 50,55.8 45,59" />
      </g>
      <rect x={30} y={25} width={18} height={14} fill={F} />
      <rect x={48} y={25} width={18} height={14} fill={B} />
      <rect x={30} y={25} width={36} height={14} fill="none" stroke="#334155" strokeWidth={1} />
      <text x={39} y={36} textAnchor="middle" fontSize={11} fontWeight={700} fill="#fff">
        N
      </text>
      <text x={57} y={36} textAnchor="middle" fontSize={11} fontWeight={700} fill="#fff">
        S
      </text>
    </>
  );
}

function Mui({ x1, y1, x2, y2, mau }: { x1: number; y1: number; x2: number; y2: number; mau: string }) {
  const a = Math.atan2(y2 - y1, x2 - x1);
  // làm tròn 2 số lẻ: máy chủ và trình duyệt tính sin/cos lệch nhau ở số lẻ thứ 14 → lỗi hydration
  const p = (d: number) => `${(x2 - 7 * Math.cos(a + d)).toFixed(2)},${(y2 - 7 * Math.sin(a + d)).toFixed(2)}`;
  return (
    <g stroke={mau} strokeWidth={2.2} fill="none" strokeLinecap="round" strokeLinejoin="round">
      <line x1={x1} y1={y1} x2={x2} y2={y2} />
      <polyline points={`${p(0.45)} ${x2},${y2} ${p(-0.45)}`} />
    </g>
  );
}

function LucTu() {
  return (
    <>
      <Mui x1={40} y1={40} x2={84} y2={40} mau={B} />
      <Mui x1={40} y1={40} x2={18} y2={58} mau={I} />
      <Mui x1={40} y1={40} x2={40} y2={6} mau={F} />
      <path d="M40 33 h7 v7" fill="none" stroke="currentColor" strokeWidth={1} opacity={0.6} />
      <text x={86} y={34} textAnchor="end" fill={B} {...chu}>
        B
      </text>
      <text x={11} y={52} fill={I} {...chu}>
        I
      </text>
      <text x={47} y={14} fill={F} {...chu}>
        F
      </text>
    </>
  );
}

function CamUng() {
  return (
    <>
      <rect x={6} y={17} width={13} height={12} fill={B} />
      <rect x={19} y={17} width={13} height={12} fill={F} />
      <text x={12.5} y={26.5} textAnchor="middle" fontSize={10.5} fontWeight={700} fill="#fff">
        S
      </text>
      <text x={25.5} y={26.5} textAnchor="middle" fontSize={10.5} fontWeight={700} fill="#fff">
        N
      </text>
      <Mui x1={10} y1={9} x2={30} y2={9} mau="currentColor" />
      <g fill="none" stroke={I} strokeWidth={2}>
        {[50, 58, 66, 74].map((x) => (
          <ellipse key={x} cx={x} cy={23} rx={4.5} ry={13} />
        ))}
        <path d="M50 36 V52 H56 M74 36 V52 H68" />
      </g>
      <circle cx={62} cy={52} r={7} fill="none" stroke="currentColor" strokeWidth={1.6} />
      <line x1={62} y1={56} x2={66} y2={47.5} stroke={F} strokeWidth={1.8} strokeLinecap="round" />
    </>
  );
}

function XoayChieu() {
  return (
    <>
      <g stroke="currentColor" strokeWidth={1.2} opacity={0.7}>
        <line x1={8} y1={34} x2={92} y2={34} />
        <line x1={8} y1={6} x2={8} y2={60} />
      </g>
      <path d="M8 34 Q 18 -6 28 34 T 48 34 T 68 34 T 88 34" fill="none" stroke={I} strokeWidth={2.2} />
      <g stroke="currentColor" strokeWidth={1} strokeDasharray="3 3" opacity={0.75}>
        <line x1={8} y1={14} x2={92} y2={14} />
        <line x1={8} y1={19.9} x2={92} y2={19.9} />
      </g>
      <text x={93} y={12} textAnchor="end" fontSize={11.5} fontWeight={700} fill="currentColor">
        I₀
      </text>
      <text x={93} y={30} textAnchor="end" fontSize={11.5} fontWeight={700} fill="currentColor">
        I
      </text>
    </>
  );
}

function SongDienTu() {
  return (
    <>
      <Mui x1={6} y1={34} x2={93} y2={34} mau="currentColor" />
      <path d="M10 34 Q 20 -4 30 34 T 50 34 T 70 34" fill="none" stroke={F} strokeWidth={2.2} />
      <path d="M10 34 Q 9 58 30 34 T 50 34 T 70 34" fill="none" stroke={B} strokeWidth={2.2} />
      <text x={24} y={11} fill={F} {...chu}>
        E
      </text>
      <text x={6} y={56} fill={B} {...chu}>
        B
      </text>
      <text x={84} y={28} fill="currentColor" {...chu}>
        c
      </text>
    </>
  );
}

/* ── Vật lí 10 · Chương 3 Động lực học. Màu lực theo build_figs.py của bài (bản đậm cho nền sáng):
   P đỏ · N xanh · lực kéo F cam · ma sát đỏ · gia tốc lục. ── */
const GIA_TOC = "#16a34a";

/** chữ có chỉ số dưới; chỉ số vẫn ≥ 10.5 để không dưới 13px ở hình 112px (H4) */
function ChiSo({ x, y, mau, chinh, duoi }: { x: number; y: number; mau: string; chinh: string; duoi: string }) {
  return (
    <text x={x} y={y} fill={mau} {...chu}>
      {chinh}
      <tspan fontSize={10.5} dy={3}>
        {duoi}
      </tspan>
    </text>
  );
}

function HopLuc() {
  return (
    <>
      <g stroke="currentColor" strokeWidth={1.2} strokeDasharray="3 3" opacity={0.7}>
        <line x1={56} y1={48} x2={76} y2={12} />
        <line x1={30} y1={12} x2={76} y2={12} />
      </g>
      <Mui x1={10} y1={48} x2={56} y2={48} mau={B} />
      <Mui x1={10} y1={48} x2={30} y2={12} mau={I} />
      <Mui x1={10} y1={48} x2={76} y2={12} mau={F} />
      <ChiSo x={28} y={60} mau={B} chinh="F" duoi="1" />
      <ChiSo x={3} y={24} mau={I} chinh="F" duoi="2" />
      <text x={80} y={30} fill={F} {...chu}>
        F
      </text>
    </>
  );
}

function Newton() {
  return (
    <>
      <line x1={4} y1={44} x2={92} y2={44} stroke="currentColor" strokeWidth={1.4} opacity={0.6} />
      <rect x={12} y={20} width={26} height={24} rx={2} fill="none" stroke="currentColor" strokeWidth={2} />
      <text x={25} y={37} textAnchor="middle" fill="currentColor" {...chu}>
        m
      </text>
      <Mui x1={38} y1={32} x2={74} y2={32} mau={I} />
      <text x={54} y={26} textAnchor="middle" fill={I} {...chu}>
        F
      </text>
      <Mui x1={12} y1={56} x2={50} y2={56} mau={GIA_TOC} />
      <text x={55} y={60} fill={GIA_TOC} {...chu}>
        a
      </text>
    </>
  );
}

function CacLuc() {
  return (
    <>
      <line x1={6} y1={40} x2={90} y2={40} stroke="currentColor" strokeWidth={1.4} opacity={0.6} />
      <rect x={38} y={24} width={20} height={16} fill="none" stroke="currentColor" strokeWidth={2} />
      <Mui x1={48} y1={32} x2={48} y2={5} mau={B} />
      <Mui x1={48} y1={32} x2={48} y2={61} mau={F} />
      <Mui x1={58} y1={30} x2={88} y2={30} mau={I} />
      <Mui x1={38} y1={37} x2={14} y2={37} mau={F} />
      <text x={53} y={13} fill={B} {...chu}>
        N
      </text>
      <text x={53} y={60} fill={F} {...chu}>
        P
      </text>
      <ChiSo x={10} y={30} mau={F} chinh="F" duoi="ms" />
    </>
  );
}

function DongLucHoc() {
  // dốc từ (6,58) lên (90,14), góc ≈ 27,65°; toạ độ khối và trục tính sẵn (hằng số, không sin/cos lúc chạy)
  return (
    <>
      <path d="M6 58 H90 V14 Z" fill="none" stroke="currentColor" strokeWidth={1.4} opacity={0.6} />
      <path d="M20 58 A14 14 0 0 0 18.4 51.5" fill="none" stroke="currentColor" strokeWidth={1.2} />
      <rect
        x={34.5}
        y={23.46}
        width={18}
        height={14}
        fill="none"
        stroke="currentColor"
        strokeWidth={2}
        transform="rotate(-27.65 43.5 30.46)"
      />
      <Mui x1={43.5} y1={30.46} x2={72.2} y2={15.43} mau="currentColor" />
      <Mui x1={43.5} y1={30.46} x2={33.29} y2={10.97} mau="currentColor" />
      <text x={75} y={13} fill="currentColor" {...chu}>
        x
      </text>
      <text x={24} y={11} fill="currentColor" {...chu}>
        y
      </text>
      <text x={25} y={56} fontSize={11} fontStyle="italic" fill="currentColor">
        α
      </text>
    </>
  );
}

function Moment() {
  return (
    <>
      <line x1={10} y1={24} x2={86} y2={24} stroke="currentColor" strokeWidth={3} strokeLinecap="round" />
      <path d="M14 24 L8 34 H20 Z" fill="none" stroke="currentColor" strokeWidth={1.4} />
      <circle cx={14} cy={24} r={2.2} fill="currentColor" />
      <Mui x1={78} y1={24} x2={78} y2={50} mau={F} />
      <g stroke="currentColor" strokeWidth={1.2} opacity={0.75}>
        <line x1={14} y1={58} x2={78} y2={58} />
        <line x1={14} y1={54} x2={14} y2={62} />
        <line x1={78} y1={54} x2={78} y2={62} />
      </g>
      <text x={2} y={20} fill="currentColor" {...chu}>
        O
      </text>
      <text x={83} y={44} fill={F} {...chu}>
        F
      </text>
      <text x={46} y={54} textAnchor="middle" fill="currentColor" {...chu}>
        d
      </text>
    </>
  );
}

const HINH: Record<SoDoNhanh["hinh"], () => React.ReactElement> = {
  hop_luc: HopLuc,
  newton: Newton,
  cac_luc: CacLuc,
  dong_luc_hoc: DongLucHoc,
  moment: Moment,
  tu_truong: TuTruong,
  luc_tu: LucTu,
  cam_ung: CamUng,
  xoay_chieu: XoayChieu,
  song_dien_tu: SongDienTu,
};

const MO_TA: Record<SoDoNhanh["hinh"], string> = {
  hop_luc: "Hai lực F1, F2 chung gốc và hợp lực F là đường chéo hình bình hành",
  newton: "Vật khối lượng m chịu lực F, gia tốc a cùng hướng lực",
  cac_luc: "Vật trên sàn chịu trọng lực P, phản lực N, lực kéo và lực ma sát",
  dong_luc_hoc: "Vật trên mặt nghiêng góc α với trục x dọc dốc, trục y vuông góc dốc",
  moment: "Thanh quay quanh trục O, lực F cách trục một cánh tay đòn d",
  tu_truong: "Thanh nam châm và đường sức từ đi từ cực Bắc sang cực Nam",
  luc_tu: "Ba vectơ B, I, F vuông góc nhau từng đôi",
  cam_ung: "Nam châm tiến vào cuộn dây, kim điện kế lệch",
  xoay_chieu: "Đồ thị hình sin với giá trị cực đại và giá trị hiệu dụng",
  song_dien_tu: "Hai sóng E và B vuông góc nhau, cùng pha, truyền với tốc độ c",
};

export default function HinhNhanh({ hinh, className = "" }: { hinh: SoDoNhanh["hinh"]; className?: string }) {
  const H = HINH[hinh];
  return (
    <svg viewBox="0 0 96 64" className={className} role="img" aria-label={MO_TA[hinh]}>
      <H />
    </svg>
  );
}
