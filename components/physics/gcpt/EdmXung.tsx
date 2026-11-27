"use client";

/**
 * GCPT Bài 2 (EDM chìm) — mô phỏng thông số xung Ip, Ton, Toff.
 * Mô hình: điện áp khe khi phóng ≈ 25 V nên năng lượng một xung E = U·Ip·Ton; tần số xung f = 1/(Ton + Toff).
 * Thể tích bóc mỗi xung xem như tỉ lệ với E, nên tốc độ bóc ∝ E·f (giảm mạnh khi xung nghỉ quá ngắn → hồ quang).
 * Độ nhám, lớp tái đúc ∝ E^(1/3) (kích thước miệng hố tỉ lệ căn bậc ba thể tích) — hệ số chọn để khớp khoảng
 * "dưới 1 µm đến hơn chục µm" của bài; chỉ là ước lượng tham khảo, không phải bảng công nghệ của máy nào.
 */

import { useState } from "react";
import { vn } from "../PredictGate";
import { CanhBao, GhiChuMoHinh, KhungMoPhong, O, ThanhMuc, TruotSo, nutPhu } from "./chung";

const U_KHE = 25; // V
const TON = [2, 5, 10, 20, 50, 100, 200, 400]; // µs
const TOFF = [2, 5, 10, 20, 50, 100, 200, 400];

const E_MAX = U_KHE * 50 * 400 * 1e-3; // mJ

const DOAN = {
  question:
    "Máy EDM đang chạy Ip = 20 A, Ton = 50 µs, Toff = 50 µs. Giữ nguyên Ip và Toff, tăng Ton lên 200 µs. Điều gì xảy ra?",
  options: [
    { text: "Bóc nhanh hơn và bề mặt mịn hơn.", why: "Xung dài hơn thì mỗi tia lửa mang nhiều năng lượng hơn: hố to hơn, bề mặt nhám hơn chứ không mịn hơn." },
    {
      text: "Bóc nhanh hơn nhưng bề mặt nhám hơn, lớp tái đúc dày hơn.",
      correct: true,
      why: "Năng lượng một xung E = U·Ip·Ton tăng 4 lần: mỗi hố to và sâu hơn. Bóc nhanh hơn, đổi lại Ra và lớp tái đúc tăng.",
    },
    { text: "Bóc chậm hơn vì số xung mỗi giây giảm.", why: "Số xung giảm (chu kì dài hơn) nhưng năng lượng mỗi xung tăng nhiều hơn, nên tổng vẫn bóc nhanh hơn." },
    { text: "Không đổi, vì chỉ dòng Ip mới quyết định tốc độ bóc.", why: "Ton cũng nằm trong năng lượng xung E = U·Ip·Ton, nên đổi Ton là đổi kết quả." },
  ],
  hint: "Kéo Ton để tự kiểm; xem hố trên bề mặt và hai thanh mức.",
};

function viTriGan(arr: number[], v: number) {
  return arr.reduce((b, x, i) => (Math.abs(x - v) < Math.abs(arr[b] - v) ? i : b), 0);
}

export default function EdmXung() {
  const [ip, setIp] = useState(20);
  const [iTon, setITon] = useState(viTriGan(TON, 50));
  const [iToff, setIToff] = useState(viTriGan(TOFF, 50));

  const ton = TON[iTon];
  const toff = TOFF[iToff];
  const E = U_KHE * ip * ton * 1e-3; // mJ
  const f = 1e6 / (ton + toff); // Hz
  const duty = ton / (ton + toff);
  // Ổn định: xung nghỉ quá ngắn so với xung phóng → mạt không kịp thoát.
  const onDinh = duty <= 0.7 ? 1 : duty <= 0.85 ? 0.75 : 0.35;
  const bocTuongDoi = (E * f * onDinh) / (E_MAX * (1e6 / (400 + 400)) * 2.2);
  const ra = 2.0 * Math.cbrt(E); // µm
  const taiDuc = 2.5 * Math.cbrt(E); // µm

  const datMau = (ten: "tho" | "tinh") => {
    if (ten === "tho") {
      setIp(40);
      setITon(viTriGan(TON, 200));
      setIToff(viTriGan(TOFF, 100));
    } else {
      setIp(3);
      setITon(viTriGan(TON, 5));
      setIToff(viTriGan(TOFF, 10));
    }
  };

  /* ---- Đồ thị dòng điện theo thời gian: luôn vẽ 3 chu kì ---- */
  const W = 320;
  const H = 120;
  const chuKi = ton + toff;
  const kx = (W - 40) / (3 * chuKi);
  const hI = 10 + (ip / 50) * 70;
  const xung = [0, 1, 2].map((k) => {
    const x0 = 30 + k * chuKi * kx;
    return <rect key={k} x={x0} y={H - 22 - hI} width={Math.max(1.5, ton * kx)} height={hI} fill="var(--color-primary)" opacity={0.85} />;
  });

  /* ---- Mặt phôi với các hố: bán kính ∝ E^(1/3) ---- */
  const r = 3 + 22 * Math.cbrt(E / E_MAX);
  const ho = [];
  for (let x = 20 + r; x < W - 10 - r; x += r * 1.7) {
    ho.push(<ellipse key={x} cx={x} cy={44} rx={r} ry={r * 0.55} fill="var(--color-panel)" stroke="var(--color-ink)" strokeWidth={1.2} />);
  }

  return (
    <KhungMoPhong ten="EDM: chỉnh xung Ip, Ton, Toff" doan={DOAN}>
      <div className="grid gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        <div className="min-w-0 space-y-2">
          <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Dòng phóng điện theo thời gian">
            <line x1={30} y1={H - 22} x2={W - 6} y2={H - 22} stroke="var(--color-ink)" strokeWidth={1.5} />
            <line x1={30} y1={H - 22} x2={30} y2={8} stroke="var(--color-ink)" strokeWidth={1.5} />
            <text x={W - 8} y={H - 6} textAnchor="end" fontSize={12} fill="var(--color-muted)">t</text>
            <text x={4} y={18} fontSize={12} fill="var(--color-muted)">i</text>
            {xung}
            <text x={30 + (ton * kx) / 2} y={H - 8} textAnchor="middle" fontSize={11} fill="var(--color-primary)">Ton</text>
            <text x={30 + (ton + toff / 2) * kx} y={H - 8} textAnchor="middle" fontSize={11} fill="var(--color-muted)">Toff</text>
            <text x={36 + ton * kx} y={H - 26 - hI + 10} fontSize={11} fill="var(--color-ink)">Ip = {ip} A</text>
          </svg>
          <svg viewBox={`0 0 ${W} 80`} className="w-full" role="img" aria-label="Mặt phôi sau phóng điện, kích thước hố theo năng lượng xung">
            <rect x={10} y={44} width={W - 20} height={32} fill="var(--color-surface-2)" stroke="var(--color-line-strong)" />
            {ho}
            <rect x={10} y={10} width={W - 20} height={34} fill="var(--color-panel)" />
            <text x={14} y={24} fontSize={11} fill="var(--color-muted)">mặt phôi nhìn cắt ngang — mỗi hố là một xung</text>
          </svg>
          <div className="flex gap-2">
            <button type="button" className={nutPhu + " flex-1"} onClick={() => datMau("tho")}>
              Chế độ thô
            </button>
            <button type="button" className={nutPhu + " flex-1"} onClick={() => datMau("tinh")}>
              Chế độ tinh
            </button>
          </div>
        </div>

        <div className="min-w-0 space-y-3">
          <TruotSo nhan="Dòng đỉnh Ip" giaTri={ip} hien={`${ip} A`} min={1} max={50} step={1} onChange={setIp} />
          <TruotSo nhan="Xung phóng Ton" giaTri={iTon} hien={`${ton} µs`} min={0} max={TON.length - 1} step={1} onChange={setITon} />
          <TruotSo nhan="Xung nghỉ Toff" giaTri={iToff} hien={`${toff} µs`} min={0} max={TOFF.length - 1} step={1} onChange={setIToff} />
          <dl className="grid grid-cols-2 gap-2">
            <O nhan="Năng lượng 1 xung E = U·Ip·Ton" so={`${E < 1 ? vn(E, 3) : vn(E, 1)} mJ`} phu="U khe ≈ 25 V" />
            <O nhan="Số xung mỗi giây" so={f >= 1000 ? `${vn(f / 1000, 1)} nghìn` : vn(f, 0)} phu={`Ton/(Ton+Toff) = ${Math.round(duty * 100)}%`} />
            <O nhan="Độ nhám Ra (ước lượng)" so={`≈ ${vn(ra, 1)} µm`} />
            <O nhan="Lớp tái đúc (ước lượng)" so={`≈ ${vn(taiDuc, 0)} µm`} />
          </dl>
          <ThanhMuc nhan="Tốc độ bóc (tương đối)" muc={bocTuongDoi} chu={bocTuongDoi > 0.5 ? "nhanh" : bocTuongDoi > 0.15 ? "vừa" : "chậm"} />
          <ThanhMuc nhan="Độ nhám bề mặt (tương đối)" muc={ra / 16} chu={ra < 1.5 ? "mịn" : ra < 6 ? "vừa" : "nhám"} mau="var(--color-warn)" />
          {duty > 0.85 ? (
            <CanhBao loai="danger">Xung nghỉ quá ngắn: mạt không kịp thoát, dễ hồ quang, cháy xước phôi. Tăng Toff.</CanhBao>
          ) : duty > 0.7 ? (
            <CanhBao loai="warn">Xung nghỉ hơi ngắn: phóng điện kém ổn định khi hốc sâu, nên tăng Toff hoặc tăng xả rửa.</CanhBao>
          ) : (
            <CanhBao loai="ok">Xung nghỉ đủ để điện môi phục hồi và cuốn mạt.</CanhBao>
          )}
        </div>
      </div>
      <GhiChuMoHinh>
        Mô hình đơn giản hoá: E = U·Ip·Ton; thể tích một hố ∝ E nên Ra và lớp tái đúc ∝ ∛E. Số Ra, lớp tái đúc chỉ là ước
        lượng tham khảo để thấy xu hướng; bảng công nghệ thật tra theo máy, cặp vật liệu điện cực – phôi.
      </GhiChuMoHinh>
    </KhungMoPhong>
  );
}
