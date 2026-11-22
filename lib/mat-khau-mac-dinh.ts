// Mật khẩu mặc định = mã số học sinh (import-roster / reset-password đặt như vậy): ai biết mã số là vào được.
// Nhận ra ngay lúc đăng nhập (mật khẩu vừa gõ trùng tên đăng nhập) → bắt đổi mật khẩu trước khi dùng tiếp.
// Không cần DB/round-trip: cờ chỉ nằm ở localStorage của máy vừa đăng nhập; máy khác đăng nhập bằng mã số
// cũng sẽ bị bắt đổi. Đây là lớp nhắc buộc phía client — chặn thật phải ở Auth (xem báo cáo vá bảo mật 22/11/2026).

export const CHANGE_PASSWORD_PATH = "/tai-khoan/doi-mat-khau";
const KEY = "thachlab.doi-mat-khau-bat-buoc.v1";

interface Flag {
  uid: string;
  login: string;
}

/** Tên đăng nhập dạng mã số (không phải email thật): bỏ đuôi @thachlab.local, chữ thường. */
function loginId(login: string): string {
  return login.trim().toLowerCase().replace(/@thachlab\.local$/, "");
}

/** Mật khẩu vừa đăng nhập thành công có trùng tên đăng nhập (mã số HS) không. */
export function isDefaultPassword(login: string, password: string): boolean {
  const id = loginId(login);
  return id !== "" && !id.includes("@") && password.trim().toLowerCase() === id;
}

export function markMustChangePassword(uid: string, login: string): void {
  try {
    localStorage.setItem(KEY, JSON.stringify({ uid, login: loginId(login) } satisfies Flag));
  } catch {
    /* không lưu được (chế độ riêng tư) thì thôi — lần đăng nhập sau sẽ nhắc lại */
  }
}

function readFlag(): Flag | null {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return null;
    const v = JSON.parse(raw) as Partial<Flag>;
    return typeof v.uid === "string" ? { uid: v.uid, login: typeof v.login === "string" ? v.login : "" } : null;
  } catch {
    return null;
  }
}

/** Tài khoản này đang phải đổi mật khẩu mặc định? Trả tên đăng nhập (mã số) để kiểm mật khẩu mới khác mã số. */
export function mustChangePassword(uid: string | null | undefined): { login: string } | null {
  if (!uid) return null;
  const f = readFlag();
  return f && f.uid === uid ? { login: f.login } : null;
}

export function clearMustChangePassword(): void {
  try {
    localStorage.removeItem(KEY);
  } catch {
    /* bỏ qua */
  }
}
