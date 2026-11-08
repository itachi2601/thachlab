/**
 * Bài mẫu CNC (tab "Bài mẫu" của Bài 2 tiện, Bài 3 phay): chương trình giải sẵn từng block, dễ → khó.
 * N6: ví dụ có lời giải đặt TRƯỚC Luyện tập/BTVN; block có `ask` bị che, sinh viên tự đoán rồi bấm mới hiện (fading).
 * Mã G theo bảng mã Win-NC32 (FANUC 21T/21M) của xưởng như bài lý thuyết: G71 = hệ mét, tiện thô G73, tiện tinh G72.
 * Hình: services/cnc-worked-examples-hinh.ts (sinh bởi scripts/cnc/ve-hinh-bai-mau.py) — số trên hình phải khớp số ở đây.
 * Không trùng đề BTVN (data/cnc/tien_bai345.json, phay_bai345.json).
 */

export type CncWorkedBlock = {
  /** Một block NC, ví dụ "N60 G01 Z-18 F0.15". */
  code: string;
  /** Một dòng giải thích. */
  note: string;
  /** Có câu hỏi → block bị che tới khi sinh viên bấm xem (fading N6). */
  ask?: string;
};

export type CncWorkedExample = {
  id: string;
  level: "Dễ" | "Vừa" | "Khó";
  title: string;
  /** Khoá hình trong CNC_WORKED_FIGURES. */
  figure: string;
  /** Đề bài: bản vẽ + yêu cầu, 1–2 câu. */
  task: string;
  params: [string, string][];
  blocks: CncWorkedBlock[];
  /** Chỗ hay sai (⚠), 1–3 ý. */
  pitfalls: string[];
};

const CODE_NOTE_TIEN =
  "Dòng đầu theo bảng mã Win-NC32 của xưởng: G71 là hệ mét. Tài liệu dùng bộ mã A (như BTVN) ghi G21 cho hệ mét.";
const CODE_NOTE_PHAY =
  "G71 là hệ mét theo bảng mã Win-NC32 của xưởng; tài liệu bộ mã A (như BTVN) ghi G21.";

const TIEN: CncWorkedExample[] = [
  {
    id: "tien-vd1",
    level: "Dễ",
    title: "Trục bậc hai lát cắt, vát mép",
    figure: "tien-vd1",
    task: "Phôi Ø32 đã khoả mặt đầu. Tiện bậc Ø26 dài 18 mm, vát 1×45° ở mép mặt đầu. Gốc W ở tâm mặt đầu phải.",
    params: [
      ["Dao", "T0101 – dao tiện ngoài"],
      ["Trục chính", "n = 1000 vòng/phút (G97)"],
      ["Chạy dao", "Lát 1 F0,15 · lát cuối F0,1 mm/vòng (G95)"],
      ["Chiều sâu cắt", "32 → 29 → 26: mỗi lát 1,5 mm mỗi bên"],
    ],
    blocks: [
      { code: "O0201 (VD1 TRUC BAC)", note: "Số chương trình, trong ngoặc là chú thích." },
      { code: "N10 G90 G71 G18 G95", note: `Toạ độ tuyệt đối, hệ mét, mặt phẳng XZ, F tính mm/vòng. ${CODE_NOTE_TIEN}` },
      { code: "N20 T0101", note: "Gọi dao số 1, bộ bù số 1." },
      { code: "N30 G97 S1000 M03", note: "Tốc độ trục chính cố định 1000 vòng/phút, quay thuận." },
      { code: "N40 M08", note: "Bật dung dịch trơn nguội." },
      { code: "N50 G00 X29 Z2", note: "Chạy nhanh tới Ø29, cách mặt đầu 2 mm, dao chưa chạm phôi." },
      { code: "N60 G01 Z-18 F0.15", note: "Lát thô 1: cắt dọc tới Z-18 (hết bậc)." },
      { code: "N70 X34", note: "Cắt lên vai bậc rồi ra ngoài phôi Ø32." },
      { code: "N80 G00 Z2", note: "Lùi nhanh về trước mặt đầu: dao đang ở Ø34, ngoài phôi nên không va." },
      { code: "N90 X24", note: "Tới Ø24 = Ø26 − 2×1: điểm bắt đầu đường vát." },
      { code: "N100 G01 Z0 F0.1", note: "Cắt chạm mặt đầu tại Z0, F nhỏ hơn cho lát cuối." },
      {
        code: "N110 X26 Z-1",
        note: "Đường vát 45°: X tăng 2 (bán kính tăng 1) khi Z lùi 1.",
        ask: "Đường vát 1×45° kết thúc ở điểm nào? Viết block N110.",
      },
      { code: "N120 Z-18", note: "Lát cuối Ø26 tới vai bậc." },
      {
        code: "N130 X34",
        note: "Tiện mặt vai từ Ø26 lên, ra khỏi phôi Ø32.",
        ask: "Hết đoạn Ø26, dao phải rời bậc thế nào? Viết block N130.",
      },
      { code: "N140 G00 X100", note: "Rút dao theo X trước, ra xa phôi." },
      { code: "N150 Z100", note: "Rồi mới rút Z về điểm thay dao." },
      { code: "N160 M09", note: "Tắt dung dịch." },
      { code: "N170 M05", note: "Dừng trục chính." },
      { code: "N180 M30", note: "Kết thúc chương trình, quay về đầu." },
    ],
    pitfalls: [
      "X ghi theo đường kính: bậc Ø26 là X26, không phải X13.",
      "Rút dao bằng G00 X trước, Z sau. Rút chéo hoặc rút Z trước dễ quệt vào vai bậc.",
    ],
  },
  {
    id: "tien-vd2",
    level: "Vừa",
    title: "Lượt tinh có côn và cung R6",
    figure: "tien-vd2",
    task: "Phôi Ø40 đã tiện thô, chừa 0,5 mm. Viết lượt tiện tinh theo bản vẽ: côn Ø16→Ø24 dài 12, Ø24 tới Z-22, cung lõm R6 lên Ø36, Ø36 tới Z-40.",
    params: [
      ["Dao", "T0404 – dao tiện tinh"],
      ["Trục chính", "n = 1200 vòng/phút (G97)"],
      ["Chạy dao", "F0,1 mm/vòng (G95)"],
      ["Bù mũi dao", "G41 như chương trình mẫu của xưởng; huỷ G40 khi rút"],
    ],
    blocks: [
      { code: "O0202 (VD2 TIEN TINH CON CUNG)", note: "Số chương trình." },
      { code: "N10 G90 G71 G18 G95", note: "Tuyệt đối, hệ mét, mặt XZ, F mm/vòng." },
      { code: "N20 T0404", note: "Dao tinh số 4, bộ bù số 4 (có bán kính mũi dao)." },
      { code: "N30 G97 S1200 M03", note: "1200 vòng/phút, quay thuận." },
      { code: "N40 M08", note: "Bật dung dịch." },
      { code: "N50 G00 X44 Z2", note: "Điểm an toàn ngoài phôi Ø40, trước mặt đầu." },
      { code: "N60 G41 G00 X16 Z2", note: "Gọi bù bán kính mũi dao khi dao còn ngoài phôi, tới Ø16." },
      { code: "N70 G01 Z0 F0.1", note: "Cắt tới mặt đầu, điểm đầu côn (Ø16; Z0)." },
      {
        code: "N80 X24 Z-12",
        note: "Côn: Ø16 → Ø24 trên 12 mm (bán kính tăng 4, góc ≈ 18,4°).",
        ask: "Điểm cuối đoạn côn có X, Z bằng bao nhiêu? Viết block N80.",
      },
      { code: "N90 Z-22", note: "Trụ Ø24 tới Z-22, chỗ bắt đầu cung." },
      {
        code: "N100 G02 X36 Z-28 R6",
        note: "Cung lõm R6: Ø24 → Ø36 (bán kính tăng 6), Z lùi 6. Nhìn hình (X lên, Z sang phải) dao đi cùng chiều kim đồng hồ → G02.",
        ask: "Cung R6 lên Ø36 dùng G02 hay G03, điểm cuối ở đâu? Viết block N100.",
      },
      { code: "N110 G01 Z-40", note: "Trụ Ø36 tới Z-40." },
      { code: "N120 X44", note: "Tiện mặt vai lên, ra khỏi phôi Ø40." },
      { code: "N130 G40 G00 X100", note: "Huỷ bù trong block rời biên dạng, rút X trước." },
      { code: "N140 Z100", note: "Rút Z về điểm thay dao." },
      { code: "N150 M09", note: "Tắt dung dịch." },
      { code: "N160 M05", note: "Dừng trục chính." },
      { code: "N170 M30", note: "Kết thúc chương trình." },
    ],
    pitfalls: [
      "Cung ghi R là bán kính thật (R6), còn X vẫn là đường kính: Ø24 + 2×6 = Ø36.",
      "Gọi G41 khi dao còn ngoài phôi, huỷ G40 trong block rời biên dạng. Gọi ngay trên biên dạng thì mũi dao ăn lẹm.",
      "Xưởng dùng G41 cho tiện ngoài; nhiều máy FANUC khác dùng G42 cho cùng chuyển động. Theo máy và hướng dẫn của giảng viên.",
    ],
  },
  {
    id: "tien-vd3",
    level: "Khó",
    title: "Chu trình tiện thô G73 và tinh G72",
    figure: "tien-vd3",
    task: "Phôi Ø40. Tiện trục theo bản vẽ bằng chu trình: thô dao T0202 rồi tinh dao T0404 theo cùng một biên dạng N80–N170.",
    params: [
      ["Dao thô", "T0202 · n = 800 vòng/phút · F0,2 mm/vòng · sâu 1 mm mỗi lát"],
      ["Dao tinh", "T0404 · n = 1000 vòng/phút · F0,1 mm/vòng"],
      ["Lượng dư tinh", "U0,5 (theo đường kính) · W0,1"],
      ["Bộ mã A", "G73 → G71, G72 → G70, G71 (mét) → G21"],
    ],
    blocks: [
      { code: "O0203 (VD3 CHU TRINH THO TINH)", note: "Số chương trình." },
      { code: "N10 G90 G71 G18 G95", note: `Tuyệt đối, hệ mét, mặt XZ, F mm/vòng. ${CODE_NOTE_TIEN}` },
      { code: "N20 T0202", note: "Dao thô số 2." },
      { code: "N30 G97 S800 M03", note: "800 vòng/phút, quay thuận." },
      { code: "N40 M08", note: "Bật dung dịch." },
      { code: "N50 G00 X42 Z2", note: "Điểm bắt đầu chu trình: ngoài phôi Ø40, trước mặt đầu 2 mm." },
      { code: "N60 G73 U1 R0.5", note: "Dòng 1 chu trình thô: mỗi lát sâu 1 mm (bán kính), lùi dao 0,5 mm." },
      {
        code: "N70 G73 P80 Q170 U0.5 W0.1 F0.2",
        note: "Dòng 2: biên dạng từ N80 tới N170, chừa U0,5 (đường kính) và W0,1 cho lượt tinh, F thô 0,2.",
        ask: "Dòng 2 của chu trình thô: P, Q trỏ tới block nào? Viết block N70.",
      },
      { code: "N80 G00 X16", note: "Block đầu biên dạng: chỉ đi theo X, không kèm Z." },
      { code: "N90 G01 Z0 F0.1", note: "Tới mặt đầu; F0,1 chỉ dùng ở lượt tinh." },
      { code: "N100 X20 Z-2", note: "Vát 2×45°: Ø16 → Ø20, Z lùi 2." },
      { code: "N110 Z-15", note: "Trụ Ø20." },
      { code: "N120 X26", note: "Lên vai Ø26." },
      { code: "N130 X30 Z-25", note: "Côn Ø26 → Ø30 dài 10." },
      { code: "N140 Z-35", note: "Trụ Ø30." },
      { code: "N150 G02 X38 Z-39 R4", note: "Cung lõm R4 lên Ø38: bán kính tăng 4, Z lùi 4, cùng chiều kim đồng hồ." },
      { code: "N160 G01 Z-50", note: "Trụ Ø38 tới Z-50." },
      { code: "N170 X42", note: "Block cuối biên dạng: ra khỏi phôi Ø40." },
      { code: "N180 G00 X100", note: "Xong thô: rút X trước." },
      { code: "N190 Z100", note: "Rút Z về điểm thay dao." },
      { code: "N200 T0404", note: "Đổi dao tinh số 4." },
      { code: "N210 G97 S1000 M03", note: "Tốc độ tinh 1000 vòng/phút." },
      { code: "N220 G41 G00 X42 Z2", note: "Gọi bù mũi dao, về đúng điểm bắt đầu chu trình." },
      {
        code: "N230 G72 P80 Q170",
        note: "Chu trình tinh chạy lại N80–N170 đúng kích thước, F lấy từ N90 (0,1).",
        ask: "Dao tinh đã ở điểm bắt đầu. Block nào chạy lượt tinh? Viết N230.",
      },
      { code: "N240 G40 G00 X100", note: "Huỷ bù, rút X." },
      { code: "N250 Z100", note: "Rút Z." },
      { code: "N260 M09", note: "Tắt dung dịch." },
      { code: "N270 M05", note: "Dừng trục chính." },
      { code: "N280 M30", note: "Kết thúc chương trình." },
    ],
    pitfalls: [
      "Hai chữ U khác nghĩa: dòng 1 (U1) là chiều sâu mỗi lát theo bán kính; dòng 2 (U0.5) là lượng dư tinh theo đường kính.",
      "Biên dạng P–Q phải đi một chiều: X không giảm, Z không tăng. Block đầu (N80) chỉ đi theo X.",
      "Lượt tinh phải bắt đầu đúng điểm của chu trình thô (X42 Z2).",
    ],
  },
];

const PHAY: CncWorkedExample[] = [
  {
    id: "phay-vd1",
    level: "Dễ",
    title: "Phay bệ biên ngoài có bù bán kính G41",
    figure: "phay-vd1",
    task: "Phôi nhôm 60×50×15 kẹp trên ê-tô. Phay biên ngoài thành bệ 50×40 bo 4 góc R5, cao 3 mm, một lượt. Gốc W ở tâm mặt trên phôi.",
    params: [
      ["Dao", "T01 – phay ngón Ø10, bù chiều dài H01, bù bán kính H11"],
      ["Trục chính", "S2500 vòng/phút, quay thuận M03"],
      ["Chạy dao", "Xuống dao F80 · cắt biên F250 mm/phút (G94)"],
      ["Cách phay", "Đi cùng chiều kim đồng hồ quanh chi tiết + G41 → phay thuận"],
    ],
    blocks: [
      { code: "O0301 (VD1 BIEN NGOAI)", note: "Số chương trình." },
      { code: "N10 G90 G71 G17 G94", note: `Tuyệt đối, hệ mét, mặt XY, F mm/phút. ${CODE_NOTE_PHAY}` },
      { code: "N20 G54", note: "Dùng gốc phôi W đã gá đặt ở ô G54." },
      { code: "N30 T01 M06", note: "Thay dao số 1; đưa trục Z về chỗ thay dao theo hướng dẫn xưởng." },
      { code: "N40 S2500 M03", note: "Trục chính 2500 vòng/phút, quay thuận." },
      { code: "N50 G43 H01 Z50", note: "Bù chiều dài dao ô H01, đưa dao lên cao Z50." },
      { code: "N60 M08", note: "Bật dung dịch." },
      { code: "N70 G00 X-40 Y-30", note: "Tới điểm ngoài phôi, góc dưới bên trái." },
      { code: "N80 Z5", note: "Hạ nhanh xuống cách mặt phôi 5 mm." },
      { code: "N90 G01 Z-3 F80", note: "Xuống sâu 3 mm ngoài phôi, chậm F80." },
      {
        code: "N100 G41 H11 X-25 Y-30 F250",
        note: "Gọi bù trái khi còn ngoài phôi, tới đường kéo dài cạnh trái. H11: ô chứa bán kính dao (máy EMCO ghi bằng H; tài liệu FANUC khác ghi D).",
      },
      { code: "N110 Y15", note: "Cạnh trái đi lên, dừng trước góc bo (20 − 5 = 15)." },
      { code: "N120 G02 X-20 Y20 R5", note: "Bo góc trên trái R5, cùng chiều kim đồng hồ." },
      { code: "N130 G01 X20", note: "Cạnh trên sang phải." },
      {
        code: "N140 G02 X25 Y15 R5",
        note: "Bo góc trên phải: từ (20; 20) tới (25; 15).",
        ask: "Bo góc trên phải R5: lệnh nào, điểm cuối ở đâu? Viết block N140.",
      },
      { code: "N150 G01 Y-15", note: "Cạnh phải đi xuống." },
      { code: "N160 G02 X20 Y-20 R5", note: "Bo góc dưới phải." },
      { code: "N170 G01 X-20", note: "Cạnh dưới sang trái." },
      { code: "N180 G02 X-25 Y-15 R5", note: "Bo góc dưới trái, khép kín biên dạng." },
      {
        code: "N190 G40 G01 X-40 Y-15",
        note: "Đưa dao rời biên dạng ra ngoài và huỷ bù trong cùng block.",
        ask: "Biên dạng đã khép kín. Block nào đưa dao ra và huỷ bù? Viết N190.",
      },
      { code: "N200 G00 Z50", note: "Rút dao lên cao." },
      { code: "N210 M09", note: "Tắt dung dịch." },
      { code: "N220 M05", note: "Dừng trục chính." },
      { code: "N230 M30", note: "Kết thúc chương trình." },
    ],
    pitfalls: [
      "Chương trình ghi toạ độ biên chi tiết (±25, ±20), không phải tâm dao: máy tự dời tâm dao ra 5 mm nhờ G41.",
      "Đi cùng chiều kim đồng hồ quanh biên ngoài thì dao nằm bên trái đường đi → G41. Đi ngược chiều thì G42.",
    ],
  },
  {
    id: "phay-vd2",
    level: "Vừa",
    title: "Khoan 4 lỗ bằng chu trình G81, G83",
    figure: "phay-vd2",
    task: "Tấm nhôm 80×60 dày 12, đã kê song song có khe hở dưới lỗ. Khoan 4 lỗ Ø8 xuyên, tâm cách mép 10 mm. Gốc W ở góc dưới trái mặt trên.",
    params: [
      ["Dao 2", "T02 – mũi khoan tâm · S2000 · F80 · sâu 3"],
      ["Dao 3", "T03 – mũi khoan Ø8 · S1500 · F100 · mỗi lát Q4"],
      ["Mặt phẳng R", "R2: cách mặt phôi 2 mm"],
      ["Chiều sâu lỗ", "Z-15: xuyên 12 mm + 3 mm cho mũi khoan thoát hết"],
    ],
    blocks: [
      { code: "O0302 (VD2 KHOAN 4 LO)", note: "Số chương trình." },
      { code: "N10 G90 G71 G17 G94", note: "Tuyệt đối, hệ mét, mặt XY, F mm/phút." },
      { code: "N20 G54", note: "Gốc phôi W." },
      { code: "N30 T02 M06", note: "Thay mũi khoan tâm (về chỗ thay dao theo hướng dẫn xưởng)." },
      { code: "N40 S2000 M03", note: "2000 vòng/phút, quay thuận." },
      { code: "N50 G43 H02 Z50", note: "Bù chiều dài dao 2, lên Z50: đây là mặt phẳng ban đầu." },
      { code: "N60 M08", note: "Bật dung dịch." },
      {
        code: "N70 G99 G81 X10 Y10 Z-3 R2 F80",
        note: "Khoan tâm lỗ 1: chạy nhanh tới (10; 10), xuống R2, khoan tới Z-3, rút về R (G99).",
      },
      { code: "N80 X70", note: "Chu trình còn hiệu lực: chỉ cần ghi toạ độ lỗ 2." },
      {
        code: "N90 Y50",
        note: "Lỗ 3 tại (70; 50): X giữ nguyên nên chỉ ghi Y.",
        ask: "Lỗ 3 nằm ở góc trên phải. Viết block N90 ngắn nhất.",
      },
      { code: "N100 G98 X10", note: "Lỗ cuối (10; 50): G98 rút về mặt phẳng ban đầu Z50." },
      { code: "N110 G80", note: "Huỷ chu trình khoan." },
      { code: "N120 M05", note: "Dừng trục chính trước khi thay dao." },
      { code: "N130 T03 M06", note: "Thay mũi khoan Ø8." },
      { code: "N140 S1500 M03", note: "1500 vòng/phút: mũi lớn hơn quay chậm hơn." },
      { code: "N150 G43 H03 Z50", note: "Bù chiều dài dao 3, lên Z50." },
      {
        code: "N160 G99 G83 X10 Y10 Z-15 R2 Q4 F100",
        note: "G83: mỗi lát 4 mm rồi rút lên thoát phoi, tới Z-15. Lỗ này nông, dùng G83 để tập; lỗ sâu trên 3 lần đường kính thì bắt buộc.",
        ask: "Khoan lỗ 1 bằng chu trình rút phoi, mỗi lát 4 mm. Viết block N160.",
      },
      { code: "N170 X70", note: "Lỗ 2." },
      { code: "N180 Y50", note: "Lỗ 3." },
      { code: "N190 G98 X10", note: "Lỗ 4, rút về Z50." },
      { code: "N200 G80", note: "Huỷ chu trình." },
      { code: "N210 M09", note: "Tắt dung dịch." },
      { code: "N220 M05", note: "Dừng trục chính." },
      { code: "N230 M30", note: "Kết thúc chương trình." },
    ],
    pitfalls: [
      "G99 chỉ dùng khi giữa các lỗ không có vấu kẹp cao hơn R2; lỗ cuối dùng G98 để rút lên cao.",
      "Quên G80 thì block di chuyển sau đó vẫn khoan thêm một lỗ.",
      "Lỗ xuyên phải khoan quá đáy (Z-15 với tấm 12) và phôi phải kê có khe hở bên dưới.",
    ],
  },
  {
    id: "phay-vd3",
    level: "Khó",
    title: "Phay hốc chữ nhật: biên trong, bù G41",
    figure: "phay-vd3",
    task: "Cùng tấm ở VD2. Phay hốc 30×20 bo góc R6, sâu 3 mm, tâm hốc (40; 30). Dao Ø10 đi một vòng biên trong là sạch cả hốc.",
    params: [
      ["Dao", "T01 – phay ngón Ø10 hai me, cắt được ở tâm"],
      ["Trục chính", "S2500 vòng/phút, M03"],
      ["Chạy dao", "Xuống dao F50 · cắt biên F200 mm/phút"],
      ["Cách phay", "Biên trong đi ngược chiều kim đồng hồ + G41 → phay thuận"],
    ],
    blocks: [
      { code: "O0303 (VD3 HOC CHU NHAT)", note: "Số chương trình." },
      { code: "N10 G90 G71 G17 G94", note: "Tuyệt đối, hệ mét, mặt XY, F mm/phút." },
      { code: "N20 G54", note: "Gốc phôi W ở góc dưới trái." },
      { code: "N30 T01 M06", note: "Thay dao phay ngón Ø10." },
      { code: "N40 S2500 M03", note: "2500 vòng/phút, quay thuận." },
      { code: "N50 G43 H01 Z50", note: "Bù chiều dài dao 1, lên Z50." },
      { code: "N60 M08", note: "Bật dung dịch." },
      { code: "N70 G00 X40 Y30", note: "Tới tâm hốc." },
      { code: "N80 Z2", note: "Hạ nhanh sát mặt phôi." },
      { code: "N90 G01 Z-3 F50", note: "Ăn thẳng xuống sâu 3 mm, chậm F50." },
      {
        code: "N100 G41 H11 Y20 F200",
        note: "Gọi bù trái, đi xuống giữa cạnh dưới hốc (40; 20). Tâm dao dừng ở Y25.",
        ask: "Dao ở tâm hốc. Block nào gọi bù và đưa dao ra cạnh dưới? Viết N100.",
      },
      { code: "N110 X49", note: "Cạnh dưới sang phải, dừng trước góc bo (55 − 6 = 49)." },
      {
        code: "N120 G03 X55 Y26 R6",
        note: "Góc dưới phải R6, ngược chiều kim đồng hồ.",
        ask: "Đi ngược chiều kim đồng hồ quanh hốc. Góc dưới phải viết thế nào? Viết N120.",
      },
      { code: "N130 G01 Y34", note: "Cạnh phải đi lên." },
      { code: "N140 G03 X49 Y40 R6", note: "Góc trên phải." },
      { code: "N150 G01 X31", note: "Cạnh trên sang trái." },
      { code: "N160 G03 X25 Y34 R6", note: "Góc trên trái." },
      { code: "N170 G01 Y26", note: "Cạnh trái đi xuống." },
      { code: "N180 G03 X31 Y20 R6", note: "Góc dưới trái." },
      { code: "N190 G01 X40", note: "Về giữa cạnh dưới, khép kín vòng." },
      { code: "N200 G40 G01 X40 Y30", note: "Huỷ bù, đưa dao về tâm hốc, rời thành hốc." },
      { code: "N210 G00 Z50", note: "Rút dao lên cao." },
      { code: "N220 M09", note: "Tắt dung dịch." },
      { code: "N230 M05", note: "Dừng trục chính." },
      { code: "N240 M30", note: "Kết thúc chương trình." },
    ],
    pitfalls: [
      "Bán kính góc hốc (R6) phải lớn hơn bán kính dao (R5). Bằng hoặc nhỏ hơn thì máy báo lỗi hoặc dao ăn lẹm góc.",
      "Hốc rộng 20 = 2 lần đường kính dao: một vòng biên trong vừa khít, hai dải cắt chạm nhau ở Y30. Dao mòn sẽ để lại gờ mảnh, nên thực tế chừa 0,2 rồi tinh hoặc thêm một lượt giữa. Hốc rộng hơn phải phay sạch phần giữa trước.",
      "Đi ngược chiều kim đồng hồ trong hốc thì dao nằm bên trái đường đi → G41 (phay thuận).",
    ],
  },
];

const BY_LESSON: Record<string, CncWorkedExample[]> = { "lesson-2": TIEN, "lesson-3": PHAY };

export function cncWorkedExamples(lessonId: string): CncWorkedExample[] {
  return BY_LESSON[lessonId] ?? [];
}

export function hasCncWorkedExamples(lessonId: string): boolean {
  return cncWorkedExamples(lessonId).length > 0;
}
