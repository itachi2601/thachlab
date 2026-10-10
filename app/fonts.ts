// Font tự host qua next/font/google — thay cho @import Google Fonts trong globals.css
// (bỏ 1–2 handshake tới fonts.googleapis/gstatic trước FCP, không chặn render).
// Chỉ nạp đúng weight đang dùng thật để không tải thừa file woff2:
//   Be Vietnam Pro (font-display): 400 · 600 (font-semibold) · 700 (font-bold) · 800 (.hub-tile);
//     font-black/900 vẫn rơi về 800 như trước (trước đây cũng không nạp 900).
//   Inter (font-body): 400/500/600 — giữ đúng như cũ, font-bold trên chữ thân bài vẫn
//     hiển thị bằng 600 (không nạp 700 để giao diện không đổi).
//   JetBrains Mono (font-mono): dùng rải rác khắp nơi (trang chủ, đề, dashboard, admin)
//     nên nạp ở root, 1 weight 400, preload: false — chữ mono là chi tiết nhỏ, không cần
//     giành băng thông với CSS/font tiêu đề trước lúc vẽ trang (display: swap đã lo hiển thị tạm).
// Biến CSS được trỏ vào --font-display/--font-body/--font-mono trong @theme (globals.css).
// Cinzel + Playfair Display (tên bậc huy hiệu rank) đã chuyển sang components/rank/rank-fonts.ts —
//   chỉ trang có render component rank mới tải, trang chủ không còn dính.
import { Be_Vietnam_Pro, Inter, JetBrains_Mono, Tinos } from "next/font/google";

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
  preload: false,
  variable: "--font-jetbrains-mono",
});

// Tinos: serif cùng số đo với Times New Roman (metric-compatible) — chỉ dùng cho vùng ĐỀ (.exam-paper) để chữ
// ngắt dòng/ngắt trang như đề giấy. preload: false để không giành băng thông với font thân trang; chỉ tải khi
// trang có chữ dùng tới (font-display swap). Weight 400/700 (đậm cho "Câu n." và \textbf trong đề).
export const tinos = Tinos({
  subsets: ["vietnamese", "latin"],
  weight: ["400", "700"],
  display: "swap",
  preload: false,
  variable: "--font-tinos",
});

export const fontClassName = `${beVietnamPro.variable} ${inter.variable} ${jetbrainsMono.variable} ${tinos.variable}`;
