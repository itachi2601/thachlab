// Font tự host qua next/font/google — thay cho @import Google Fonts trong globals.css
// (bỏ 1–2 handshake tới fonts.googleapis/gstatic trước FCP, không chặn render).
// Chỉ nạp đúng weight đang dùng thật để không tải thừa file woff2:
//   Be Vietnam Pro (font-display): 400 · 600 (font-semibold) · 700 (font-bold) · 800 (.hub-tile);
//     font-black/900 vẫn rơi về 800 như trước (trước đây cũng không nạp 900).
//   Inter (font-body): 400/500/600 — giữ đúng như cũ, font-bold trên chữ thân bài vẫn
//     hiển thị bằng 600 (không nạp 700 để giao diện không đổi).
//   JetBrains Mono (font-mono): dùng rải rác khắp nơi (trang chủ, đề, dashboard, admin)
//     nên nạp ở root, 1 weight 400.
// Biến CSS được trỏ vào --font-display/--font-body/--font-mono trong @theme (globals.css).
//   Cinzel (--font-cinzel, 700) + Playfair Display (--font-playfair, 600/700): riêng cho tên bậc rank
//     (tên tiếng Anh lớn / tiếng Việt nhỏ) — khớp thiết kế huy chương.
import { Be_Vietnam_Pro, Cinzel, Inter, JetBrains_Mono, Playfair_Display } from "next/font/google";

export const beVietnamPro = Be_Vietnam_Pro({
  subsets: ["vietnamese", "latin"],
  weight: ["400", "600", "700", "800"],
  display: "swap",
  variable: "--font-be-vietnam",
});

export const inter = Inter({
  subsets: ["vietnamese", "latin"],
  weight: ["400", "500", "600"],
  display: "swap",
  variable: "--font-inter",
});

export const jetbrainsMono = JetBrains_Mono({
  subsets: ["vietnamese", "latin"],
  weight: "400",
  display: "swap",
  variable: "--font-jetbrains-mono",
});

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

export const fontClassName = `${beVietnamPro.variable} ${inter.variable} ${jetbrainsMono.variable} ${cinzel.variable} ${playfair.variable}`;
