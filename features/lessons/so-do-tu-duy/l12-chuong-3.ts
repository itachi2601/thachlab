import type { SoDoChuong } from "@/features/lessons/so-do-tu-duy/types";

/**
 * Vật lí 12 — Chương 3. Từ trường (Bài 9–16; lesson id 10, 11, 12, 13, 14, 125, 126, 127).
 * Nội dung rút từ `content/lesson-samples/l12-*` (công thức, quy ước góc, cách phát biểu giữ đúng như bài đã soạn).
 * Mô phỏng: 3 PhET đang nhúng ở Bài 9, 12, 13; mô phỏng cân dòng điện (`.tl-sim`) ở Bài 11; hoạt hình sóng ở Bài 16.
 */
const bai = (id: number) => `/lop-hoc/bai/?id=${id}`;

export const L12_CHUONG_3: SoDoChuong = {
  lop: "Vật lí 12",
  chuong: "Chương 3 · Từ trường",
  tam: "Điện ⇄ Từ",
  mach: "Dòng điện sinh ra từ trường; từ trường biến thiên lại sinh ra dòng điện.",
  nhanh: [
    {
      id: "tu-truong",
      ten: "Từ trường",
      hinh: "tu_truong",
      bai: [{ so: 9, id: 10, ten: "Khái niệm từ trường" }],
      chot: "Quanh nam châm và dòng điện có từ trường.",
      ct: "\\vec{B}:\\ \\text{ra N, vào S}",
      yCon: [
        { tu: "Nguồn sinh ra", y: "Nam châm · dòng điện · Trái Đất." },
        { tu: "Đường sức từ", y: "Đường cong kín: ngoài nam châm ra cực Bắc, vào cực Nam. Chỗ mau thì từ trường mạnh." },
        { tu: "Kim la bàn", y: "Cực Bắc của kim chỉ chiều từ trường tại điểm đặt kim." },
        { tu: "Nắm tay phải", y: "Ngón cái theo chiều dòng điện, các ngón khum chỉ chiều đường sức." },
      ],
      bay: "Đường sức từ không có điểm đầu, điểm cuối và không cắt nhau.",
      moPhong: {
        kieu: "phet",
        ten: "PhET · Nam châm và la bàn",
        src: "https://phet.colorado.edu/sims/html/magnet-and-compass/latest/magnet-and-compass_all.html?locale=vi",
        nhiemVu: "Đoán trước: đặt la bàn sát cực Nam, kim chỉ vào hay ra? Kéo la bàn một vòng quanh nam châm để kiểm tra.",
      },
    },
    {
      id: "luc-tu",
      ten: "Lực từ · Cảm ứng từ",
      hinh: "luc_tu",
      bai: [
        { so: 10, id: 11, ten: "Lực từ. Cảm ứng từ" },
        { so: 11, id: 12, ten: "Thực hành đo cảm ứng từ" },
      ],
      chot: "Từ trường đẩy dây dẫn có dòng điện.",
      ct: "F = BIl\\sin\\alpha",
      noiTiep: "Đặt dây có dòng điện vào từ trường → dây chịu lực.",
      yCon: [
        { tu: "Góc α", y: "Góc giữa $\\vec{B}$ và chiều dòng điện. Dây song song đường sức thì không có lực." },
        { tu: "Bàn tay trái", y: "Đường sức xuyên lòng bàn tay, cổ tay → ngón tay theo dòng điện, ngón cái choãi 90° chỉ lực." },
        { tu: "Cảm ứng từ", y: "Đo độ mạnh của từ trường, đơn vị tesla (T).", ct: "B = \\dfrac{F}{Il\\sin\\alpha}" },
        { tu: "Đo bằng cân", y: "Số chỉ cân đổi Δm khi bật dòng điện.", ct: "B = \\dfrac{\\Delta m\\,g}{Il}" },
      ],
      bay: "Lực từ vuông góc với cả dây lẫn $\\vec{B}$, không nằm dọc theo đường sức.",
      moPhong: {
        kieu: "bai",
        ten: "Mô phỏng cân dòng điện · Bài 11",
        href: bai(12),
        nhiemVu: "Đoán trước: tăng dòng điện gấp đôi thì số chỉ cân đổi bao nhiêu? Bấm các mức dòng điện để kiểm tra.",
      },
    },
    {
      id: "cam-ung",
      ten: "Cảm ứng điện từ",
      hinh: "cam_ung",
      bai: [
        { so: 12, id: 13, ten: "Hiện tượng cảm ứng điện từ" },
        { so: 15, id: 126, ten: "Ứng dụng của cảm ứng điện từ" },
      ],
      chot: "Từ thông qua mạch kín đổi → có dòng điện.",
      ct: "|e_c| = N\\left|\\dfrac{\\Delta\\Phi}{\\Delta t}\\right|",
      noiTiep: "Chiều ngược lại: từ trường biến thiên sinh ra dòng điện.",
      yCon: [
        { tu: "Từ thông", y: "Đếm số đường sức xuyên qua mặt khung; α là góc giữa pháp tuyến và $\\vec{B}$. Đơn vị Wb.", ct: "\\Phi = BS\\cos\\alpha" },
        { tu: "Điều kiện", y: "Mạch kín và từ thông đang biến thiên. Đổi càng nhanh, dòng càng mạnh." },
        { tu: "Định luật Lenz", y: "Dòng cảm ứng có chiều chống lại sự biến thiên từ thông sinh ra nó." },
        { tu: "Ứng dụng", y: "Bếp từ · sạc không dây · dòng Foucault · đàn ghi ta điện." },
      ],
      bay: "Từ trường mạnh nhưng đứng yên thì không có dòng cảm ứng.",
      moPhong: {
        kieu: "phet",
        ten: "PhET · Định luật Faraday",
        src: "https://phet.colorado.edu/sims/html/faradays-law/latest/faradays-law_all.html?locale=vi",
        nhiemVu: "Đoán trước: đưa nam châm vào nhanh và vào chậm, lần nào kim lệch nhiều hơn? Rồi để nam châm nằm yên trong cuộn dây.",
      },
    },
    {
      id: "xoay-chieu",
      ten: "Dòng điện xoay chiều",
      hinh: "xoay_chieu",
      bai: [
        { so: 13, id: 14, ten: "Đại cương về dòng điện xoay chiều" },
        { so: 14, id: 125, ten: "Máy phát điện. Máy biến áp" },
      ],
      chot: "Khung dây quay đều → dòng điện đổi chiều đều đặn.",
      ct: "i = I_0\\cos(\\omega t + \\varphi_i)",
      noiTiep: "Cho khung dây quay đều trong từ trường → suất điện động xoay chiều.",
      yCon: [
        { tu: "Hiệu dụng", y: "Số ghi trên thiết bị (220 V) là giá trị hiệu dụng.", ct: "I = \\dfrac{I_0}{\\sqrt{2}},\\quad U = \\dfrac{U_0}{\\sqrt{2}}" },
        { tu: "Máy phát", y: "n: tốc độ quay (vòng/s), p: số cặp cực.", ct: "E_0 = NBS\\omega,\\quad f = np" },
        { tu: "Máy biến áp", y: "Đổi điện áp, không đổi tần số (máy lí tưởng).", ct: "\\dfrac{U_1}{U_2} = \\dfrac{N_1}{N_2} = \\dfrac{I_2}{I_1}" },
        { tu: "Truyền tải", y: "Tăng điện áp trước khi truyền để giảm hao phí.", ct: "\\Delta P = \\dfrac{RP^2}{U^2}" },
      ],
      bay: "Máy biến áp không chạy với dòng một chiều không đổi: từ thông trong lõi không biến thiên.",
      moPhong: {
        kieu: "phet",
        ten: "PhET · Máy phát điện",
        src: "https://phet.colorado.edu/sims/html/generator/latest/generator_all.html?locale=vi",
        nhiemVu: "Đoán trước: mở vòi nước mạnh hơn thì bóng đèn sáng hơn hay nháy nhanh hơn? Mở vòi để kiểm tra.",
      },
    },
    {
      id: "song-dien-tu",
      ten: "Sóng điện từ",
      hinh: "song_dien_tu",
      bai: [{ so: 16, id: 127, ten: "Điện từ trường. Sóng điện từ" }],
      chot: "Điện trường và từ trường sinh ra nhau, lan đi.",
      ct: "\\lambda = \\dfrac{c}{f}",
      noiTiep: "Điện trường và từ trường biến thiên nuôi nhau → tách khỏi dây dẫn, lan ra xa.",
      yCon: [
        { tu: "Sóng ngang", y: "$\\vec{E} \\perp \\vec{B}$, cả hai vuông góc phương truyền và luôn cùng pha." },
        { tu: "Chân không", y: "Truyền được không cần môi trường.", ct: "c = 3\\cdot 10^{8}\\ \\text{m/s}" },
        { tu: "Thang sóng", y: "Bước sóng giảm dần: vô tuyến → hồng ngoại → nhìn thấy → tử ngoại → tia X → tia gamma." },
        { tu: "Ứng dụng", y: "Phát thanh, wifi · điều khiển từ xa · diệt khuẩn · chụp X-quang." },
      ],
      bay: "$\\vec{E}$ và $\\vec{B}$ cùng pha, không lệch pha $\\pi/2$.",
      moPhong: {
        kieu: "bai",
        ten: "Hoạt hình sóng điện từ · Bài 16",
        href: bai(127),
        nhiemVu: "Nhìn vào: khi $\\vec{E}$ lớn nhất thì $\\vec{B}$ đang lớn nhất hay bằng 0?",
      },
    },
  ],
};
