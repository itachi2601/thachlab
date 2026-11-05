"use client";

/**
 * Cảnh `canh: {kieu: "ong"}` của họ `song_day` (5/11/2026, mẫu bài 15 L11 dạng 2): ống cộng hưởng đo tốc độ âm — ống
 * thẳng đứng, miệng hở ở trên, nguồn âm sát miệng, mặt nước hạ dần. Độ sâu d (cm) đo từ miệng ống xuống (d < 0 là trên
 * miệng). Đường bao sóng dừng (biên độ dao động của lớp khí) có nút ở mặt nước và bụng ở d = −e, vẽ đúng tỉ lệ theo `lam`
 * — nên khi nước ở l₂ thì đường bao tự có nút ở l₁ (l₂ − l₁ = λ/2). Bề ngang ống không theo tỉ lệ.
 * canh: { kieu: "ong", dai (cm, chiều dài ống), e (cm), nguon? (nhãn cạnh loa), nhan_dai? (nhãn bên phải đáy ống, vd "đáy 67 cm"),
 * hinh? (mục vẽ sẵn từ đầu, cùng kiểu mục lop — vd vạch l₁, l₂ đề cho) }
 * Mục lop: nuoc {l} (mặt nước; mục mới nhất thắng) · bao {l} (đường bao, nút ở l) · vach {l, ten} (nét đứt ngang ở độ sâu l,
 * nhãn bên trái; l > dai thì vạch nằm dưới đáy ống) · thuoc {tu, den, nhan, hang?} (ngoặc dọc bên phải; đoạn < 2 cm vẽ kiểu
 * kích thước nhỏ: hai vạch + mũi tên chỉ vào) · ghi {text}. `het: k` như chung. Dùng chung `lam` của `song_day` (cm);
 * A, x_max không dùng. Quy tắc: N8 + H3 (nhãn trên hình), H4 (nét đường bao khác nét nước), N5, B4 (không chạy).
 */

import { C_MAX, C_MIN, Chevron, Label, dangHien, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { SongDayCanh, SongDayLop } from "@/features/lessons/types";

type Props = { lam: number; canh: Extract<SongDayCanh, { kieu: "ong" }>; lop?: SongDayLop[][]; layer: number };

const XC = 9.2, R = 1.25, HTUBE = 7.2; // tâm ống, nửa bề ngang ống, chiều cao phần vẽ (đơn vị hình)

export default function OngCongHuong({ lam, canh, lop, layer: L }: Props) {
  const items = [...(canh.hinh ?? []).filter((it) => it.het == null || L < it.het), ...dangHien(lop, L)];
  const ghi = ghiMoiNhat(lop, L);
  const all = [...(canh.hinh ?? []), ...(lop ?? []).flat()];
  const dMax = Math.max(canh.dai, ...all.map((it) => (it.loai === "vach" || it.loai === "nuoc" || it.loai === "bao" ? it.l : 0))) + 1.5;
  const k = HTUBE / dMax;
  const Y0 = 2.7;
  const Y = (d: number) => Y0 + d * k;
  const yDay = Y(canh.dai);
  const ghiY = Y(dMax) + 1.0;
  const bot = ghiY + 2 * 1.3 + 0.3;

  const nuoc = [...items].reverse().find((it) => it.loai === "nuoc") as Extract<SongDayLop, { loai: "nuoc" }> | undefined;
  const bao = [...items].reverse().find((it) => it.loai === "bao") as Extract<SongDayLop, { loai: "bao" }> | undefined;
  const baoPath = (s: number) => {
    if (!bao) return "";
    const n = 90, d0 = -canh.e, pts: string[] = [];
    for (let i = 0; i <= n; i++) {
      const d = d0 + ((bao.l - d0) * i) / n;
      const a = (R - 0.25) * Math.abs(Math.sin((2 * Math.PI * (bao.l - d)) / lam));
      pts.push(`${(XC + s * a).toFixed(3)} ${Y(d).toFixed(3)}`);
    }
    return "M" + pts.join(" L");
  };
  const xr = XC + R + 0.75;

  return (
    <svg viewBox={`0 0 20 ${bot}`} className="cc-fig" role="img" aria-label={`Ống cộng hưởng dài ${canh.dai} cm`}>
      {/* nguồn âm (loa) sát miệng ống */}
      <g>
        <rect x={XC - 0.45} y={Y0 - 2.35} width={0.9} height={0.5} fill="none" stroke="currentColor" strokeWidth={0.09} />
        <path d={`M${XC - 0.45} ${Y0 - 1.85} L${XC - 1} ${Y0 - 1.1} H${XC + 1} L${XC + 0.45} ${Y0 - 1.85}`} fill="none" stroke="currentColor" strokeWidth={0.09} strokeLinejoin="round" />
        {canh.nguon && (
          <Label x={XC + 1.4} y={Y0 - 1.35} a="start" size={1}>
            {canh.nguon}
          </Label>
        )}
      </g>
      {/* nước */}
      {nuoc && nuoc.l < canh.dai && (
        <g className="cc-in">
          <rect x={XC - R} y={Y(nuoc.l)} width={2 * R} height={yDay - Y(nuoc.l)} fill={C_MIN} fillOpacity={0.16} />
          <line x1={XC - R} y1={Y(nuoc.l)} x2={XC + R} y2={Y(nuoc.l)} stroke={C_MIN} strokeWidth={0.12} />
        </g>
      )}
      {/* thành ống: miệng hở, đáy kín */}
      <path d={`M${XC - R} ${Y0} V${yDay} H${XC + R} V${Y0}`} fill="none" stroke="currentColor" strokeWidth={0.13} strokeLinejoin="round" />
      {canh.nhan_dai && (
        <Label x={XC + R + 0.5} y={yDay + 0.35} a="start" size={0.95}>
          {canh.nhan_dai}
        </Label>
      )}
      {bao && (
        <g key={`b${bao.l}`} className="cc-in">
          <path d={baoPath(1)} fill="none" stroke={C_MAX} strokeWidth={0.1} />
          <path d={baoPath(-1)} fill="none" stroke={C_MAX} strokeWidth={0.1} />
        </g>
      )}
      {items.map((it, i) => {
        if (it.loai === "vach") {
          const y = Y(it.l);
          return (
            <g key={i} className="cc-in">
              <line x1={XC - R - 1.2} y1={y} x2={XC + R + 0.3} y2={y} stroke={C_MIN} strokeWidth={0.07} strokeDasharray="0.3 0.2" />
              <Label x={XC - R - 1.4} y={y + 0.38} a="end" size={1} fill={C_MIN}>
                {it.ten}
              </Label>
            </g>
          );
        }
        if (it.loai === "thuoc") {
          const x = xr + (it.hang ?? 0) * 1.2, y1 = Y(it.tu), y2 = Y(it.den), nho = Math.abs(y2 - y1) < 0.6;
          return (
            <g key={i} className="cc-in" color={C_MAX}>
              {nho ? (
                <>
                  <path d={`M${x - 0.35} ${y1} H${x + 0.35} M${x - 0.35} ${y2} H${x + 0.35}`} stroke="currentColor" strokeWidth={0.08} />
                  <line x1={x} y1={y1 - 0.75} x2={x} y2={y1} stroke="currentColor" strokeWidth={0.08} />
                  <Chevron x={x} y={y1} ang={Math.PI / 2} color="currentColor" w={0.08} len={0.28} />
                  <line x1={x} y1={y2 + 0.75} x2={x} y2={y2} stroke="currentColor" strokeWidth={0.08} />
                  <Chevron x={x} y={y2} ang={-Math.PI / 2} color="currentColor" w={0.08} len={0.28} />
                </>
              ) : (
                <path d={`M${x - 0.3} ${y1} H${x} V${y2} H${x - 0.3}`} stroke="currentColor" strokeWidth={0.1} fill="none" />
              )}
              <Label x={x + 0.45} y={(y1 + y2) / 2 + 0.38} a="start" size={1} fill={C_MAX}>
                {it.nhan}
              </Label>
            </g>
          );
        }
        return null;
      })}
      {ghi.map((t, i) => (
        <Label key={`${L}-${i}`} x={10} y={ghiY + 1 + i * 1.3} size={1}>
          {t}
        </Label>
      ))}
    </svg>
  );
}
