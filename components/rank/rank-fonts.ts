// Font riêng cho tên bậc huy hiệu rank — tách khỏi layout gốc (app/fonts.ts) vì chỉ
// TierName/TierLadder dùng. next/font preload theo route nơi nó được import, nên giờ
// chỉ các trang thật sự render component rank mới tải 2 họ này.
import { Cinzel, Playfair_Display } from "next/font/google";

export const cinzel = Cinzel({
  subsets: ["latin"],
  weight: "700",
  display: "swap",
  variable: "--font-cinzel",
});

export const playfair = Playfair_Display({
  subsets: ["vietnamese", "latin"],
  weight: ["600", "700"],
  display: "swap",
  variable: "--font-playfair",
});
