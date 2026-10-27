import GuestGradebook from "@/components/admin/GuestGradebook";

/** Không có trong menu: /quan-tri/bang-diem-ma — tạo mã + QR cho đề làm không cần tài khoản, xem bảng điểm theo lớp. */
export default function Page() {
  return <GuestGradebook />;
}
