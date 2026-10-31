"use client";

import { useState } from "react";
import VideoThiNghiemKhung, {
  type VideoKhungData,
  type VideoKhungEvent,
} from "@/components/lessons/VideoThiNghiemKhung";
import c_tn_l10_co_nang_bao_toan_01 from "@/content/thi-nghiem/video-khung/tn-l10-co-nang-bao-toan-01.json";
import c_tn_l10_cong_suat_01 from "@/content/thi-nghiem/video-khung/tn-l10-cong-suat-01.json";
import c_tn_l10_dong_nang_the_nang_01 from "@/content/thi-nghiem/video-khung/tn-l10-dong-nang-the-nang-01.json";
import c_tn_l10_dongluong_01 from "@/content/thi-nghiem/video-khung/tn-l10-dongluong-01.json";
import c_tn_l10_dongluong_02 from "@/content/thi-nghiem/video-khung/tn-l10-dongluong-02.json";
import c_tn_l10_hieu_suat_01 from "@/content/thi-nghiem/video-khung/tn-l10-hieu-suat-01.json";
import c_tn_l10_thuchanhdl_03 from "@/content/thi-nghiem/video-khung/tn-l10-thuchanhdl-03.json";
import c_tn_l12_antoanpx_01 from "@/content/thi-nghiem/video-khung/tn-l12-antoanpx-01.json";
import c_tn_l12_apsuatdongnang_01 from "@/content/thi-nghiem/video-khung/tn-l12-apsuatdongnang-01.json";
import c_tn_l12_apsuatdongnang_02 from "@/content/thi-nghiem/video-khung/tn-l12-apsuatdongnang-02.json";
import c_tn_l12_boylecharles_01 from "@/content/thi-nghiem/video-khung/tn-l12-boylecharles-01.json";
import c_tn_l12_camungdt_01 from "@/content/thi-nghiem/video-khung/tn-l12-camungdt-01.json";
import c_tn_l12_camungdt_03 from "@/content/thi-nghiem/video-khung/tn-l12-camungdt-03.json";
import c_tn_l12_chuyenthe_01 from "@/content/thi-nghiem/video-khung/tn-l12-chuyenthe-01.json";
import c_tn_l12_dttruong_02 from "@/content/thi-nghiem/video-khung/tn-l12-dttruong-02.json";
import c_tn_l12_hatnhan_01 from "@/content/thi-nghiem/video-khung/tn-l12-hatnhan-01.json";
import c_tn_l12_hatnhan_02 from "@/content/thi-nghiem/video-khung/tn-l12-hatnhan-02.json";
import c_tn_l12_mayphatdien_01 from "@/content/thi-nghiem/video-khung/tn-l12-mayphatdien-01.json";
import c_tn_l12_mayphatdien_03 from "@/content/thi-nghiem/video-khung/tn-l12-mayphatdien-03.json";
import c_tn_l12_nllk_01 from "@/content/thi-nghiem/video-khung/tn-l12-nllk-01.json";
import c_tn_l12_phongxa_02 from "@/content/thi-nghiem/video-khung/tn-l12-phongxa-02.json";
import c_tn_l12_pttrangthai_02 from "@/content/thi-nghiem/video-khung/tn-l12-pttrangthai-02.json";
import c_tn_l12_thangnhietdo_01 from "@/content/thi-nghiem/video-khung/tn-l12-thangnhietdo-01.json";
import c_tn_l12_thangnhietdo_04 from "@/content/thi-nghiem/video-khung/tn-l12-thangnhietdo-04.json";
import c_tn_l12_thuchanh_02 from "@/content/thi-nghiem/video-khung/tn-l12-thuchanh-02.json";
import c_tn_l12_thuchanhtu_03 from "@/content/thi-nghiem/video-khung/tn-l12-thuchanhtu-03.json";
import c_tn_l12_thuchanhtu_04 from "@/content/thi-nghiem/video-khung/tn-l12-thuchanhtu-04.json";
import c_tn_l12_tutruong_04 from "@/content/thi-nghiem/video-khung/tn-l12-tutruong-04.json";
import c_tn_l12_udcamung_02 from "@/content/thi-nghiem/video-khung/tn-l12-udcamung-02.json";
import c_tn_l12_xoaychieu_03 from "@/content/thi-nghiem/video-khung/tn-l12-xoaychieu-03.json";

/**
 * XEM THỬ video thí nghiệm + khung sáu ô + dừng ở câu Dự đoán (bản thử 29/10/2026), 23 clip L12.
 * Mở http://localhost:3000/dev/video-tuong-tac. Chỉ có nghĩa ở máy dev; sự kiện chỉ in ra bảng bên dưới,
 * chưa ghi DB (muốn đo tỉ lệ dừng/chọn/xem lại thì nối onEvent vào bảng ghi sau khi thầy chốt).
 */
const CLIPS = [
  c_tn_l10_co_nang_bao_toan_01,
  c_tn_l10_cong_suat_01,
  c_tn_l10_dong_nang_the_nang_01,
  c_tn_l10_dongluong_01,
  c_tn_l10_dongluong_02,
  c_tn_l10_hieu_suat_01,
  c_tn_l10_thuchanhdl_03,
  c_tn_l12_antoanpx_01,
  c_tn_l12_apsuatdongnang_01,
  c_tn_l12_apsuatdongnang_02,
  c_tn_l12_boylecharles_01,
  c_tn_l12_camungdt_01,
  c_tn_l12_camungdt_03,
  c_tn_l12_chuyenthe_01,
  c_tn_l12_dttruong_02,
  c_tn_l12_hatnhan_01,
  c_tn_l12_hatnhan_02,
  c_tn_l12_mayphatdien_01,
  c_tn_l12_mayphatdien_03,
  c_tn_l12_nllk_01,
  c_tn_l12_phongxa_02,
  c_tn_l12_pttrangthai_02,
  c_tn_l12_thangnhietdo_01,
  c_tn_l12_thangnhietdo_04,
  c_tn_l12_thuchanh_02,
  c_tn_l12_thuchanhtu_03,
  c_tn_l12_thuchanhtu_04,
  c_tn_l12_tutruong_04,
  c_tn_l12_udcamung_02,
  c_tn_l12_xoaychieu_03,
] as VideoKhungData[];

export default function VideoTuongTacPreviewPage() {
  const [log, setLog] = useState<string[]>([]);
  const onEvent = (id: string) => (e: VideoKhungEvent) =>
    setLog((l) => [`${new Date().toLocaleTimeString("vi-VN")} · ${id} · ${JSON.stringify(e)}`, ...l].slice(0, 12));

  return (
    <main className="mx-auto max-w-5xl space-y-8 px-4 py-8">
      <header>
        <h1 className="font-display text-2xl font-bold text-ink">Video thí nghiệm bán tương tác — bản thử</h1>
        <p className="mt-1 text-[15px] text-muted">
          Khung sáu ô sáng theo giây của video; video tự dừng một lần ở câu Dự đoán. Thử tua qua câu Dự đoán, bấm ô đã
          mở để xem lại, và thu cửa sổ xuống 375px để xem dải bước trên điện thoại.
        </p>
      </header>
      {CLIPS.map((c) => (
        <VideoThiNghiemKhung key={c.id} data={c} onEvent={onEvent(c.id)} />
      ))}
      <section className="rounded-2xl border border-line bg-panel p-4">
        <h2 className="mb-2 text-[15px] font-bold text-ink">Sự kiện gần nhất</h2>
        <pre className="whitespace-pre-wrap text-[13px] text-muted">{log.length ? log.join("\n") : "Chưa có."}</pre>
      </section>
    </main>
  );
}
