"use client";

import "katex/dist/katex.min.css";
import BtmPresenter from "@/components/lessons/btm-trinh-chieu/BtmPresenter";
import { HinhOngThuyNgan, MAU_ONG_THUY_NGAN } from "@/features/lessons/btm-trinh-chieu/mau-ong-thuy-ngan";

/**
 * XEM THỬ TRÌNH CHIẾU BÀI TẬP MẪU (17/11/2026) — http://localhost:3000/dev/btm-trinh-chieu
 * Phím: → / Space / PageDown tiếp · ← lùi · 1–5 nhảy bước · F toàn màn · B nền bảng xanh · Home về đầu.
 * Chưa gắn vào trang bài học; thầy duyệt mẫu rồi mới quyết chỗ đặt nút và trường dữ liệu.
 */
export default function BtmTrinhChieuDevPage() {
  return <BtmPresenter bai={MAU_ONG_THUY_NGAN} hinh={(lop) => <HinhOngThuyNgan lop={lop} />} />;
}
