import type { SoDoChuong } from "@/features/lessons/so-do-tu-duy/types";

/**
 * Vật lí 10 — Chương 3. Động lực học (Bài 13–22; lesson id 58–67).
 * Nội dung rút từ `content/lesson-samples/l10-*` (công thức, kí hiệu $F_{\mathrm{mst}}$, $\vec F_{AB}$… giữ đúng như bài đã soạn).
 * Mô phỏng: PhET Cộng vectơ (Bài 22), PhET Chuyển động ném màn Lực cản (Bài 19); clip đồng xu – bìa – cốc (Bài 14).
 * Bài 20 và 21 không có mô phỏng nên nhánh 4, 5 không có `moPhong`.
 */
const bai = (id: number) => `/lop-hoc/bai/?id=${id}`;

export const L10_CHUONG_3: SoDoChuong = {
  lop: "Vật lí 10",
  chuong: "Chương 3 · Động lực học",
  // "Lực → Chuyển động" tràn nút trung tâm ở màn rộng (158px) → chọn 2 chữ
  tam: "Hợp lực",
  mach: "Hợp lực quyết định gia tốc; lực không qua trục quay thì làm vật quay.",
  nhanh: [
    {
      id: "hop-luc",
      ten: "Tổng hợp · Phân tích lực",
      hinh: "hop_luc",
      bai: [
        { so: 13, id: 58, ten: "Tổng hợp và phân tích lực. Cân bằng lực" },
        { so: 22, id: 67, ten: "Thực hành: Tổng hợp lực" },
      ],
      chot: "Nhiều lực thay bằng một hợp lực.",
      ct: "\\vec F = \\vec F_1 + \\vec F_2",
      yCon: [
        { tu: "Cùng phương", y: "Cùng chiều thì cộng, ngược chiều thì trừ.", ct: "F = F_1 + F_2,\\quad F = \\lvert F_1 - F_2 \\rvert" },
        {
          tu: "Hai lực đồng quy",
          y: "Hợp lực là đường chéo hình bình hành; α là góc giữa hai lực chung gốc.",
          ct: "F^2 = F_1^2 + F_2^2 + 2F_1F_2\\cos\\alpha",
        },
        { tu: "Phân tích lực", y: "Chiếu lực lên hai phương vuông góc; α là góc giữa lực và Ox.", ct: "F_x = F\\cos\\alpha,\\quad F_y = F\\sin\\alpha" },
        { tu: "Cân bằng chất điểm", y: "Đứng yên hoặc thẳng đều khi tổng các lực bằng không.", ct: "\\vec F_1 + \\vec F_2 + \\dots = \\vec 0" },
      ],
      bay: "Hợp lực không luôn bằng $F_1 + F_2$: nó đổi theo góc, có thể nhỏ hơn cả hai lực.",
      moPhong: {
        kieu: "phet",
        ten: "PhET · Cộng vectơ",
        src: "https://phet.colorado.edu/sims/html/vector-addition/latest/vector-addition_all.html?locale=vi",
        nhiemVu: "Đoán trước: hai lực vuông góc thì vectơ tổng có dài bằng tổng độ dài hai lực không? Kéo vector b đổi góc rồi đọc ô Độ dài.",
      },
    },
    {
      id: "newton",
      ten: "Ba định luật Newton",
      hinh: "newton",
      bai: [
        { so: 14, id: 59, ten: "Định luật 1 Newton" },
        { so: 15, id: 60, ten: "Định luật 2 Newton" },
        { so: 16, id: 61, ten: "Định luật 3 Newton" },
      ],
      chot: "Hợp lực làm đổi vận tốc; lực luôn đi theo cặp.",
      ct: "\\vec a = \\dfrac{\\vec F}{m}",
      noiTiep: "Hợp lực khác không → vật đổi vận tốc, có gia tốc.",
      yCon: [
        { tu: "Định luật 1", y: "Hợp lực bằng không thì vật giữ nguyên vận tốc, cả độ lớn lẫn hướng.", ct: "\\vec F_{\\mathrm{hl}} = \\vec 0 \\;\\Rightarrow\\; \\vec v = \\text{const}" },
        { tu: "Quán tính", y: "Vật có xu hướng giữ vận tốc; khối lượng càng lớn càng khó đổi vận tốc." },
        { tu: "Định luật 2", y: "Gia tốc cùng hướng hợp lực, tỉ lệ thuận với F, tỉ lệ nghịch với m.", ct: "\\vec F = m\\vec a" },
        { tu: "Định luật 3", y: "Cùng lúc, cùng loại, cùng độ lớn, ngược chiều, khác vật.", ct: "\\vec F_{AB} = -\\vec F_{BA}" },
      ],
      bay: "Lực và phản lực đặt vào hai vật khác nhau nên không triệt tiêu nhau.",
      moPhong: {
        kieu: "bai",
        ten: "Clip đồng xu – bìa – cốc · Bài 14",
        href: bai(59),
        nhiemVu: "Đoán trước: búng mạnh tấm bìa, đồng xu bay theo bìa hay rơi vào cốc? Xem clip để kiểm tra.",
      },
    },
    {
      id: "cac-luc",
      ten: "Các lực thường gặp",
      hinh: "cac_luc",
      bai: [
        { so: 17, id: 62, ten: "Trọng lực và lực căng" },
        { so: 18, id: 63, ten: "Lực ma sát" },
        { so: 19, id: 64, ten: "Lực cản và lực nâng" },
      ],
      chot: "Biết từng lực: phương, chiều, độ lớn.",
      ct: "P = mg",
      noiTiep: "Muốn dùng định luật 2 → phải biết từng lực tác dụng lên vật.",
      yCon: [
        { tu: "Trọng lực", y: "Thẳng đứng, hướng xuống, đặt ở trọng tâm. Khối lượng không đổi, trọng lượng đổi theo g." },
        { tu: "Lực căng", y: "Dọc theo dây, kéo vật về phía dây. Dây nhẹ không dãn: lực căng như nhau." },
        { tu: "Ma sát trượt", y: "Ngược chiều trượt; μ không có đơn vị, N là áp lực.", ct: "F_{\\mathrm{mst}} = \\mu N" },
        { tu: "Lực đẩy Archimedes", y: "Bằng trọng lượng chất lỏng bị chiếm chỗ; V là thể tích phần chìm.", ct: "F_A = \\rho g V" },
      ],
      bay: "Áp lực không luôn bằng $mg$: kéo chếch lên hay đặt trên mặt nghiêng thì khác.",
      moPhong: {
        kieu: "phet",
        ten: "PhET · Chuyển động ném (màn Lực cản)",
        src: "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html?locale=vi",
        nhiemVu: "Đoán trước: tích ô Sức cản không khí thì quỹ đạo ngắn hơn hay dài hơn? Bắn hai lần, có và không có sức cản, để so.",
      },
    },
    {
      id: "giai-bai-toan",
      ten: "Giải bài toán động lực học",
      hinh: "dong_luc_hoc",
      bai: [{ so: 20, id: 65, ten: "Một số ví dụ về cách giải các bài toán thuộc phần động lực học" }],
      chot: "Vẽ – Kể – Viết – Chiếu, rồi giải.",
      ct: "\\vec P + \\vec N + \\dots = m\\vec a",
      noiTiep: "Gộp đủ các lực vào định luật 2 → tính gia tốc, rồi chuyển động.",
      yCon: [
        { tu: "Bốn bước", y: "Vẽ hình · kể lực · viết định luật 2 dạng vectơ · chiếu lên Ox, Oy." },
        { tu: "Kéo xiên", y: "Oy cho áp lực N, Ox cho gia tốc.", ct: "N = mg - F\\sin\\alpha" },
        { tu: "Mặt nghiêng", y: "Đặt Ox dọc theo dốc rồi tách trọng lực thành hai thành phần.", ct: "a = g(\\sin\\alpha - \\mu\\cos\\alpha)" },
        { tu: "Hệ nối dây", y: "Tách từng vật: cùng độ lớn gia tốc, cùng lực căng.", ct: "T_1 = T_2 = T" },
      ],
      bay: "Kể thiếu hoặc thừa lực: chỉ kể lực do vật khác tác dụng, không có \"lực đà\".",
    },
    {
      id: "moment",
      ten: "Moment lực · Cân bằng vật rắn",
      hinh: "moment",
      bai: [{ so: 21, id: 66, ten: "Moment lực. Cân bằng của vật rắn" }],
      chot: "Lực không qua trục thì làm vật quay.",
      ct: "M = F\\cdot d",
      noiTiep: "Vật có kích thước, lực lệch khỏi trục → vật quay chứ không chỉ tịnh tiến.",
      yCon: [
        { tu: "Cánh tay đòn", y: "Khoảng cách từ trục quay tới giá của lực, đơn vị m." },
        { tu: "Quy tắc moment", y: "Tổng moment làm quay thuận kim bằng tổng moment làm quay ngược kim.", ct: "M_1 + M_2 + \\dots = M_1' + M_2' + \\dots" },
        { tu: "Cân bằng vật rắn", y: "Không tịnh tiến và không quay.", ct: "\\sum \\vec F = \\vec 0,\\quad \\sum M = 0" },
        { tu: "Ngẫu lực", y: "Hai lực song song, ngược chiều, bằng nhau; d là khoảng cách hai giá.", ct: "M = F\\cdot d" },
      ],
      bay: "Cánh tay đòn đo tới giá của lực, không phải tới điểm đặt lực.",
    },
  ],
};
