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

const HINH: Record<SoDoNhanh["hinh"], () => React.ReactElement> = {
  tu_truong: TuTruong,
  luc_tu: LucTu,
  cam_ung: CamUng,
  xoay_chieu: XoayChieu,
  song_dien_tu: SongDienTu,
};

const MO_TA: Record<SoDoNhanh["hinh"], string> = {
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
