// Lộ trình TẬP TẠI NHÀ cho học sinh lớp 10 trở lên (22/11/2026) — /suc-khoe/tai-nha.
// Đi theo con đường thầy Thạch đã đi: đi bộ công viên + nghe podcast → bài tay không → Tabata/HIIT
// → phòng gym với máy đi bộ, máy nhẹ → chương trình gym đầy đủ. Mỗi bậc có tiêu chí lên bậc rõ ràng.
//
// KHÔNG THU THẬP DỮ LIỆU: mọi câu trả lời, buổi đã tập, cảm nhận chỉ nằm ở localStorage của máy đang dùng
// (khoá "taiNha:<id tài khoản>" để máy dùng chung không lẫn người). Không gọi Supabase, không gửi đi đâu.
// Muốn đổi điều này phải sửa cả dòng cam kết trong components/suc-khoe/TapTaiNhaApp.tsx.
//
// Cơ sở: WHO 2020 (5–17 tuổi: trung bình 60′/ngày vận động vừa–mạnh, sức cơ–xương ≥3 ngày/tuần);
// AAP — Stricker, Faigenbaum, McCambridge 2020 (tập sức mạnh an toàn cho tuổi vị thành niên khi có hướng dẫn kỹ thuật,
// tăng tải từ từ); PAR-Q+ (câu hỏi sàng lọc sức khoẻ trước khi tập); "talk test" (nói được thành câu = mức vừa).
// Không mục tiêu cân nặng/vóc dáng, không xếp hạng, không chuỗi ngày (docs/QUY-TAC-THIET-KE.md G2, L3).

export type Move = { id: string; name: string; cue: string; /** bản không bật nhảy (nhà tầng, gối yếu) */ quiet?: string };

export const MOVES: Move[] = [
  // khởi động / giãn cơ
  { id: "xoay_khop", name: "Xoay cổ, vai, hông, gối, cổ chân", cue: "Mỗi khớp 5 vòng mỗi chiều, chậm." },
  { id: "di_tai_cho", name: "Đi bộ nhanh tại chỗ, đánh tay", cue: "Nâng gối vừa phải, thở đều." },
  { id: "dang_tay_buoc", name: "Bước sang ngang dang tay", cue: "Bước trái–phải, tay dang lên ngang vai." },
  { id: "gian_dui_truoc", name: "Giãn đùi trước (mỗi bên)", cue: "Đứng vịn tường, kéo gót về mông, gối chỉ xuống đất." },
  { id: "gian_dui_sau", name: "Giãn đùi sau", cue: "Duỗi một chân ra trước, gập hông, lưng thẳng." },
  { id: "gian_nguc_vai", name: "Giãn ngực, vai", cue: "Đan tay sau lưng, ưỡn ngực nhẹ, thở chậm." },
  { id: "tho_cham", name: "Nằm thở chậm", cue: "Hít vào 4 giây, thở ra 6 giây." },
  // đi bộ / chạy
  { id: "di_bo", name: "Đi bộ", cue: "Mức vừa: vẫn nói được thành câu. Nghe podcast hay nhạc tuỳ em." },
  { id: "di_bo_nhanh", name: "Đi bộ nhanh", cue: "Thở nhanh hơn, nói được từng câu ngắn, không hát được." },
  { id: "chay_cham", name: "Chạy chậm", cue: "Chậm tới mức vẫn nói được vài chữ. Mệt thì đi bộ, không dừng hẳn." },
  // sức mạnh tay không
  { id: "squat", name: "Squat tay không", cue: "Đẩy hông ra sau, gối theo hướng mũi chân, gót không nhấc." },
  { id: "squat_ghe", name: "Ngồi xuống – đứng lên khỏi ghế", cue: "Chạm mông vào ghế rồi đứng lên, không thả phịch xuống." },
  { id: "hit_dat_ban", name: "Hít đất chống tay lên bàn", cue: "Thân thẳng từ đầu tới gót, ngực xuống gần mép bàn." },
  { id: "hit_dat_goi", name: "Hít đất chống gối", cue: "Thân thẳng từ đầu tới gối, khuỷu khép khoảng 45°." },
  { id: "hit_dat", name: "Hít đất", cue: "Siết bụng và mông, hạ chậm 2 giây." },
  { id: "keo_balo", name: "Cúi người kéo balo sách", cue: "Balo 3–5 kg, gập hông, lưng thẳng, kéo về bụng, siết bả vai." },
  { id: "sieu_nhan", name: "Nằm sấp nâng tay chân", cue: "Nâng vừa khỏi sàn, mắt nhìn sàn, không ngửa cổ." },
  { id: "nang_hong", name: "Nằm ngửa nâng hông", cue: "Gót gần mông, đẩy hông lên tới thân thẳng từ vai tới gối." },
  { id: "nang_hong_1", name: "Nâng hông một chân (đổi bên giữa hiệp)", cue: "Hông không lệch; khó quá thì về hai chân." },
  { id: "buoc_chung", name: "Bước chùng luân phiên", cue: "Gối sau gần chạm sàn, thân thẳng." },
  { id: "chung_ghe", name: "Chùng chân sau gác ghế (đổi bên giữa hiệp)", cue: "Mu bàn chân sau đặt lên ghế, hạ thẳng xuống." },
  { id: "buoc_bac", name: "Bước lên bậc cầu thang", cue: "Cả bàn chân đặt trên bậc, đứng thẳng hẳn rồi bước xuống." },
  { id: "ngoi_tuong", name: "Ngồi dựa tường", cue: "Đùi song song sàn, gối thẳng trên cổ chân." },
  { id: "plank", name: "Plank", cue: "Khuỷu dưới vai, thân thẳng; võng lưng thì nghỉ sớm." },
  { id: "plank_nghieng", name: "Plank nghiêng (đổi bên giữa hiệp)", cue: "Hông nâng cao; khó quá thì chống gối." },
  { id: "dead_bug", name: "Nằm ngửa duỗi tay chân đối bên", cue: "Lưng dưới luôn áp sàn, duỗi chậm." },
  { id: "nhon_got", name: "Nhón gót", cue: "Lên hết tầm, hạ chậm; vịn tường cho vững." },
  // tim mạch cường độ cao (HIIT / Tabata)
  { id: "nang_goi", name: "Chạy nâng cao gối tại chỗ", cue: "Gối lên ngang hông, tiếp đất nửa trước bàn chân.", quiet: "Nâng gối nhanh, không bật — luôn một chân trên sàn." },
  { id: "bat_nhay_dang", name: "Bật nhảy dang tay chân", cue: "Tiếp đất êm, gối hơi chùng.", quiet: "Bước sang ngang thay vì bật, tay vẫn dang lên." },
  { id: "leo_nui", name: "Leo núi tại chỗ", cue: "Tay thẳng dưới vai, hông thấp, kéo gối về ngực luân phiên.", quiet: "Leo núi chậm, đặt chân xuống nhẹ." },
  { id: "squat_bat", name: "Bật nhảy từ squat", cue: "Tiếp đất êm, gối chùng.", quiet: "Squat nhanh + nhón gót ở trên, không rời sàn." },
  { id: "truot_bang", name: "Bật sang ngang kiểu trượt băng", cue: "Tiếp đất một chân, gối chùng, giữ thăng bằng 1 nhịp.", quiet: "Bước dài sang ngang, chạm tay xuống gối." },
  { id: "burpee_buoc", name: "Burpee bước (không bật)", cue: "Chống tay, bước lùi hai chân ra plank, bước vào, đứng lên." },
  { id: "burpee", name: "Burpee", cue: "Chống tay, bật chân ra plank, bật vào, nhảy lên. Đúng động tác hơn nhanh.", quiet: "Burpee bước (không bật)." },
  { id: "dam_boc", name: "Đấm thẳng nhanh luân phiên", cue: "Đứng tấn, siết bụng, đấm không khoá khuỷu." },
  // phòng gym (bậc 6)
  { id: "may_di_bo", name: "Máy đi bộ (đi dốc)", cue: "Tốc độ 4–5,5 km/h, dốc 3–8%. Không vịn tay vịn suốt buổi." },
  { id: "xe_dap_tap", name: "Xe đạp tập", cue: "Yên ngang hông khi đứng; đạp đều, nói được thành câu." },
  { id: "may_ep_nguc", name: "Máy ép ngực", cue: "Tay cầm ngang giữa ngực, ép vai ra sau." },
  { id: "may_keo_xo", name: "Máy kéo xô", cue: "Kéo thanh về ngực trên, thả lên hết tầm." },
  { id: "may_dap_dui", name: "Máy đạp đùi", cue: "Không khoá gối khi duỗi; hạ tới gối khoảng 90°." },
  { id: "may_keo_cap", name: "Kéo cáp ngồi", cue: "Lưng thẳng, kéo về bụng, siết bả vai." },
  { id: "may_day_vai", name: "Máy đẩy vai", cue: "Đẩy lên trước mặt, không ưỡn lưng." },
];
export const moveById = (id: string) => MOVES.find((m) => m.id === id);

/** Một khối: lặp `rounds` vòng; mỗi vòng làm lần lượt `items`, mỗi bài `work` giây, nghỉ `rest` giây. */
export type Block = { label: string; items: string[]; work: number; rest: number; rounds: number; restRound?: number; note?: string; /** Tabata: giữ nguyên 8 lượt */ fixed?: boolean };
export type SessionType = "di-bo" | "suc-manh" | "hiit" | "gym";
export type Session = { key: string; title: string; type: SessionType; why: string; blocks: Block[]; /** khối tính phút theo thời gian em chọn (đi bộ) */ scaleWalk?: boolean };

export type Stage = {
  n: number;
  name: string;
  short: string;
  goal: string;
  minWeeks: number;
  /** thứ tự ưu tiên buổi khi em có N ngày/tuần: lấy N buổi đầu */
  order: string[];
  sessions: Session[];
  /** tự kiểm trước khi lên bậc — tất cả đều đạt */
  levelUp: string[];
  tips: string[];
};

const WALK = (min: number, item = "di_bo"): Block => ({ label: "Đi bộ", items: [item], work: min * 60, rest: 0, rounds: 1 });
/** đi nhanh xen đi thường: `fast` giây nhanh, `easy` giây thường */
const WALK_INT = (rounds: number, fast: number, easy: number, fastItem = "di_bo_nhanh", easyItem = "di_bo"): Block => ({
  label: "Đổi nhịp",
  items: [fastItem],
  work: fast,
  rest: easy,
  rounds,
  note: `Phần “nghỉ” là ${moveById(easyItem)?.name.toLowerCase()}, không đứng yên.`,
});

export const STAGES: Stage[] = [
  {
    n: 1,
    name: "Bậc 1 · Đi bộ và nghe",
    short: "Đi bộ",
    goal: "Tạo thói quen ra khỏi nhà và vận động đều. Chưa cần mệt — chỉ cần đi.",
    minWeeks: 2,
    order: ["b1_di", "b1_di_dai", "b1_di", "b1_di", "b1_di_dai"],
    sessions: [
      { key: "b1_di", title: "Đi bộ công viên", type: "di-bo", why: "Đi bộ mức vừa là cách nhẹ nhất để tim, phổi và chân quen vận động.", scaleWalk: true, blocks: [WALK(20)] },
      { key: "b1_di_dai", title: "Đi bộ dài + nghe một tập podcast", type: "di-bo", why: "Chọn một tập podcast dài 30–40 phút: đi tới khi hết tập.", scaleWalk: true, blocks: [WALK(30)] },
    ],
    levelUp: [
      "Đi bộ liền 30 phút mà không phải dừng nghỉ.",
      "Hai tuần gần nhất đi đủ số buổi đã chọn (thiếu nhiều nhất 1 buổi).",
      "Hôm sau không thấy đau chân, đau gối.",
    ],
    tips: [
      "Đi lúc mát (sáng sớm hoặc chiều tối), mang nước, giày có đế êm.",
      "Thử “talk test”: vừa đi vừa nói được thành câu là đúng mức.",
      "Không có công viên: sân trường, quanh khu nhà, hành lang chung cư đều được.",
    ],
  },
  {
    n: 2,
    name: "Bậc 2 · Đi nhanh và động tác nền",
    short: "Động tác nền",
    goal: "Đi bộ nhanh hơn và học 5 động tác gốc: ngồi xuống, đẩy, kéo, nâng hông, giữ thân.",
    minWeeks: 3,
    order: ["b2_nen", "b2_di", "b2_nen", "b2_di", "b2_di"],
    sessions: [
      { key: "b2_di", title: "Đi bộ đổi nhịp", type: "di-bo", why: "Xen 1 phút đi nhanh với 2 phút đi thường: tim quen với lúc gắng sức rồi hồi lại.", blocks: [WALK(5), WALK_INT(6, 60, 120), WALK(5)] },
      {
        key: "b2_nen",
        title: "5 động tác nền",
        type: "suc-manh",
        why: "Học đúng động tác khi còn dễ, để các bậc sau tăng độ khó mà không đau khớp.",
        blocks: [{ label: "Vòng động tác", items: ["squat_ghe", "hit_dat_ban", "keo_balo", "nang_hong", "plank"], work: 30, rest: 30, rounds: 2, restRound: 60 }],
      },
    ],
    levelUp: [
      "Squat tay không 15 lần đúng động tác (gót không nhấc, gối không chụm).",
      "Hít đất chống tay lên bàn 10 lần, thân thẳng.",
      "Plank 30 giây không võng lưng.",
      "Đi bộ nhanh liền 20 phút.",
    ],
    tips: [
      "Trong 30 giây làm, làm chậm và đúng; được bao nhiêu lần cũng được.",
      "Mỏi cơ 1–2 ngày sau buổi đầu là bình thường. Đau nhói ở khớp thì dừng bài đó.",
    ],
  },
  {
    n: 3,
    name: "Bậc 3 · Tay không toàn thân",
    short: "Tay không",
    goal: "Sức mạnh toàn thân bằng chính cân nặng cơ thể, cộng chạy chậm xen đi bộ.",
    minWeeks: 4,
    order: ["b3_toan_than", "b3_chay_di", "b3_chan_than", "b3_chay_di", "b3_toan_than"],
    sessions: [
      {
        key: "b3_toan_than",
        title: "Toàn thân",
        type: "suc-manh",
        why: "Mỗi vòng đủ đẩy – kéo – chân – thân giữa.",
        blocks: [{ label: "Vòng toàn thân", items: ["squat", "hit_dat_goi", "keo_balo", "buoc_chung", "sieu_nhan", "plank"], work: 40, rest: 20, rounds: 3, restRound: 60 }],
      },
      {
        key: "b3_chan_than",
        title: "Chân và thân giữa",
        type: "suc-manh",
        why: "Chân khoẻ và thân giữa vững giúp chạy, nhảy, chơi thể thao và ngồi học đỡ mỏi lưng.",
        blocks: [{ label: "Vòng chân – thân", items: ["buoc_bac", "nang_hong", "ngoi_tuong", "dead_bug", "plank_nghieng", "nhon_got"], work: 40, rest: 20, rounds: 3, restRound: 60 }],
      },
      { key: "b3_chay_di", title: "Chạy chậm xen đi bộ", type: "di-bo", why: "Bước đệm trước HIIT: tim quen với nhịp cao hơn trong thời gian ngắn.", blocks: [WALK(5), WALK_INT(8, 60, 90, "chay_cham", "di_bo"), WALK(5)] },
    ],
    levelUp: [
      "Hít đất chống gối 10 lần liền, thân thẳng.",
      "Bước chùng 10 lần mỗi chân, không mất thăng bằng.",
      "Plank 45 giây.",
      "Chạy chậm xen đi bộ đủ 8 lượt mà vẫn nói được vài chữ.",
    ],
    tips: [
      "Làm đủ 40 giây quá dễ → đổi sang bản khó hơn (hít đất chống gối → hít đất thường; squat → hạ chậm 3 giây).",
      "Các buổi sức mạnh cách nhau ít nhất 1 ngày.",
    ],
  },
  {
    n: 4,
    name: "Bậc 4 · Tabata và HIIT nhẹ",
    short: "HIIT nhẹ",
    goal: "Làm quen tập ngắt quãng cường độ cao: gắng sức ngắn, nghỉ ngắn, lặp lại.",
    minWeeks: 4,
    order: ["b4_hiit", "b4_suc_manh", "b4_vua", "b4_tabata", "b4_vua"],
    sessions: [
      {
        key: "b4_hiit",
        title: "HIIT 30/30",
        type: "hiit",
        why: "30 giây gắng sức, 30 giây nghỉ: đủ mạnh để tim khoẻ lên mà còn giữ được động tác đúng.",
        blocks: [{ label: "HIIT 30/30", items: ["nang_goi", "squat", "leo_nui", "hit_dat_goi", "bat_nhay_dang"], work: 30, rest: 30, rounds: 2, restRound: 90 }],
      },
      {
        key: "b4_tabata",
        title: "Kiểu Tabata 20/10",
        type: "hiit",
        why: "8 lượt × (20 giây gắng sức + 10 giây nghỉ) = 4 phút. Bản cho người mới: gắng sức mạnh nhưng giữ đúng động tác, không cần kiệt sức.",
        blocks: [
          { label: "Khối Tabata 1", items: ["nang_goi", "squat"], work: 20, rest: 10, rounds: 4, fixed: true },
          { label: "Nghỉ giữa khối", items: [], work: 0, rest: 90, rounds: 1 },
          { label: "Khối Tabata 2", items: ["leo_nui", "dam_boc"], work: 20, rest: 10, rounds: 4, fixed: true },
        ],
      },
      {
        key: "b4_suc_manh",
        title: "Sức mạnh tay không",
        type: "suc-manh",
        why: "Giữ sức cơ – xương ít nhất 3 lần/tuần cùng các buổi HIIT (WHO).",
        blocks: [{ label: "Vòng sức mạnh", items: ["hit_dat", "chung_ghe", "keo_balo", "nang_hong_1", "plank"], work: 40, rest: 20, rounds: 3, restRound: 60 }],
      },
      { key: "b4_vua", title: "Vận động vừa", type: "di-bo", why: "Ngày nhẹ giữa hai buổi mạnh: đi bộ nhanh, đạp xe, cầu lông, đá bóng với bạn.", scaleWalk: true, blocks: [WALK(30, "di_bo_nhanh")] },
    ],
    levelUp: [
      "Làm hết 2 khối Tabata mà động tác vẫn đúng tới lượt cuối.",
      "Hít đất thường 10 lần liền.",
      "Chạy chậm liền 20 phút.",
      "Sau buổi HIIT khoảng 2–3 phút là thở lại bình thường.",
    ],
    tips: [
      "Không xếp hai buổi HIIT vào hai ngày liền nhau.",
      "Nhà tầng hoặc gối yếu: bật chế độ “không bật nhảy” ở phần Hồ sơ.",
      "Chóng mặt, buồn nôn khi tập → giảm tốc độ, nghỉ lâu hơn; không cố cho hết lượt.",
    ],
  },
  {
    n: 5,
    name: "Bậc 5 · HIIT đầy đủ và tay không nâng cao",
    short: "HIIT đầy đủ",
    goal: "Tăng số khối Tabata, bài khó hơn, chạy liên tục. Đây là mức nhiều người tập ở nhà giữ lâu dài.",
    minWeeks: 6,
    order: ["b5_tabata", "b5_suc_manh", "b5_chay", "b5_hiit", "b5_suc_manh"],
    sessions: [
      {
        key: "b5_tabata",
        title: "Tabata 3 khối",
        type: "hiit",
        why: "Ba khối 4 phút, nghỉ 1 phút giữa khối.",
        blocks: [
          { label: "Khối 1", items: ["squat_bat", "hit_dat"], work: 20, rest: 10, rounds: 4, fixed: true },
          { label: "Nghỉ giữa khối", items: [], work: 0, rest: 60, rounds: 1 },
          { label: "Khối 2", items: ["truot_bang", "leo_nui"], work: 20, rest: 10, rounds: 4, fixed: true },
          { label: "Nghỉ giữa khối", items: [], work: 0, rest: 60, rounds: 1 },
          { label: "Khối 3", items: ["burpee", "nang_goi"], work: 20, rest: 10, rounds: 4, fixed: true },
        ],
      },
      {
        key: "b5_hiit",
        title: "HIIT 40/20",
        type: "hiit",
        why: "Gắng sức lâu hơn, nghỉ ngắn hơn bậc 4.",
        blocks: [{ label: "HIIT 40/20", items: ["burpee", "chung_ghe", "leo_nui", "hit_dat", "truot_bang", "plank"], work: 40, rest: 20, rounds: 3, restRound: 90 }],
      },
      {
        key: "b5_suc_manh",
        title: "Tay không nâng cao",
        type: "suc-manh",
        why: "Hạ chậm 3 giây mỗi lần để bài tay không vẫn đủ nặng.",
        blocks: [{ label: "Vòng nâng cao", items: ["hit_dat", "chung_ghe", "keo_balo", "nang_hong_1", "buoc_bac", "plank_nghieng"], work: 45, rest: 15, rounds: 3, restRound: 75, note: "Mỗi lần: hạ 3 giây, lên 1 giây." }],
      },
      { key: "b5_chay", title: "Chạy liên tục", type: "di-bo", why: "Sức bền nền cho mọi môn thể thao.", scaleWalk: true, blocks: [WALK(5), WALK(25, "chay_cham"), WALK(5)] },
    ],
    levelUp: [
      "Tập đều ít nhất 6 tuần ở bậc 5.",
      "Hít đất 20 lần liền, plank 60 giây.",
      "Muốn tập với máy và có điều kiện đến phòng gym (có người lớn hoặc huấn luyện viên chỉ kỹ thuật nếu em dưới 18 tuổi).",
    ],
    tips: ["Không đến được phòng gym thì cứ ở bậc này lâu dài — vẫn đủ khoẻ.", "Mỗi 6–8 tuần có một tuần nhẹ: bớt 1/3 số vòng."],
  },
  {
    n: 6,
    name: "Bậc 6 · Bước vào phòng gym",
    short: "Phòng gym",
    goal: "Làm quen máy đi bộ và máy tạ nhẹ. Học kỹ thuật trước, tạ nặng sau.",
    minWeeks: 4,
    order: ["b6_may", "b6_tim_mach", "b6_may", "b6_nha", "b6_tim_mach"],
    sessions: [
      { key: "b6_tim_mach", title: "Máy đi bộ / xe đạp tập", type: "gym", why: "Đi dốc trên máy là đi bộ công viên “nâng cấp” — quen thuộc nhất để bắt đầu ở phòng gym.", scaleWalk: true, blocks: [WALK(25, "may_di_bo")] },
      {
        key: "b6_may",
        title: "Máy tạ nhẹ",
        type: "gym",
        why: "Máy giữ đường đi của tạ nên dễ học đúng. Tạ nhẹ tới mức làm 15 lần vẫn còn sức làm thêm 3–4 lần.",
        blocks: [
          { label: "Khởi động máy", items: ["xe_dap_tap"], work: 300, rest: 0, rounds: 1 },
          { label: "Máy tạ — 12–15 lần mỗi hiệp", items: ["may_dap_dui", "may_ep_nguc", "may_keo_xo", "may_keo_cap", "may_day_vai"], work: 60, rest: 90, rounds: 2, note: "Ô thời gian chỉ để nhắc nhịp: làm 12–15 lần rồi nghỉ." },
        ],
      },
      { key: "b6_nha", title: "Buổi ở nhà (bậc 5)", type: "hiit", why: "Ngày không đến phòng gym: giữ một buổi HIIT ở nhà.", blocks: [{ label: "HIIT 40/20", items: ["hit_dat", "squat", "leo_nui", "keo_balo", "plank"], work: 40, rest: 20, rounds: 2, restRound: 90 }] },
    ],
    levelUp: [
      "Sau 4 tuần làm đúng kỹ thuật cả 5 máy, tăng lên 3 hiệp, rồi tăng tạ bước nhỏ nhất khi mọi hiệp đủ 15 lần.",
      "Lúc này em có thể nhờ huấn luyện viên lập chương trình gym chia buổi (thân trên / chân / toàn thân).",
    ],
    tips: [
      "Dưới 18 tuổi: đi cùng người lớn hoặc nhờ huấn luyện viên chỉ kỹ thuật buổi đầu (AAP 2020).",
      "Không thử mức tạ nặng nhất một lần; không dùng bột, thuốc tăng cơ khi chưa hỏi bác sĩ.",
      "Lau máy sau khi dùng, mang khăn và nước.",
    ],
  },
];
export const stageByN = (n: number) => STAGES.find((s) => s.n === n) ?? STAGES[0];

export const WARMUP: Block = { label: "Khởi động", items: ["xoay_khop", "di_tai_cho", "dang_tay_buoc"], work: 60, rest: 0, rounds: 1 };
export const COOLDOWN: Block = { label: "Giãn cơ", items: ["gian_dui_truoc", "gian_dui_sau", "gian_nguc_vai", "tho_cham"], work: 40, rest: 0, rounds: 1 };

// ---------------------------------------------------------------------------------------------
// Hồ sơ cá nhân — CHỈ lưu trên máy (localStorage).
export type Profile = {
  grade: "10" | "11" | "12" | "sv";
  activity: 0 | 1 | 2 | 3; // ngồi nhiều | đi bộ/đạp xe đi học | thể thao 1–2 buổi | tập đều ≥3 buổi
  walk: 0 | 1 | 2 | 3; // đi bộ nhanh liền: <10′ | 10–20′ | 20–30′ | >30′
  push: 0 | 1 | 2 | 3; // hít đất: chưa | chống bàn/gối | thường 1–9 | thường ≥10
  minutes: 20 | 30 | 45;
  days: 2 | 3 | 4 | 5;
  quiet: boolean; // không bật nhảy
  podcast: boolean; // thích nghe khi đi bộ
  withFriend: boolean;
  goals: string[];
  health: string[]; // cờ sàng lọc (PAR-Q+)
  doctorOk: boolean;
};

export const GOALS = [
  { key: "ben", label: "Bền hơn khi chạy, leo cầu thang" },
  { key: "khoe", label: "Khoẻ hơn, làm được bài khó hơn" },
  { key: "ngu", label: "Ngủ ngon, bớt căng thẳng mùa thi" },
  { key: "the-thao", label: "Chơi thể thao tốt hơn" },
  { key: "gym", label: "Chuẩn bị để tập phòng gym" },
];

/** Câu hỏi sàng lọc, rút gọn từ PAR-Q+ cho học sinh. Chọn bất kỳ ô nào → hỏi bác sĩ trước khi qua bậc 2. */
export const HEALTH_FLAGS = [
  { key: "tim", label: "Bác sĩ từng nói em có vấn đề về tim hoặc huyết áp" },
  { key: "dau-nguc", label: "Đau tức ngực, chóng mặt hoặc ngất khi gắng sức" },
  { key: "hen", label: "Hen suyễn, khó thở khi chạy" },
  { key: "khop", label: "Đang đau hoặc chấn thương xương, khớp" },
  { key: "khac", label: "Bác sĩ dặn hạn chế vận động vì lý do khác" },
];

export const DEFAULT_PROFILE: Profile = {
  grade: "10", activity: 0, walk: 1, push: 1, minutes: 30, days: 3, quiet: false, podcast: true, withFriend: false, goals: [], health: [], doctorOk: false,
};

/** Bậc gợi ý từ hồ sơ: không bao giờ bắt đầu cao hơn bậc 5 (bậc 6 phải đi qua tiêu chí bậc 5). */
export function suggestStage(p: Profile): { n: number; why: string } {
  if (p.health.length && !p.doctorOk) return { n: 1, why: "Em đã chọn một mục sức khoẻ cần lưu ý: bắt đầu bằng đi bộ và hỏi bác sĩ trước khi tập mạnh hơn." };
  const score = p.activity + p.walk + p.push; // 0..9
  if (p.walk === 0 || score <= 2) return { n: 1, why: "Bắt đầu từ đi bộ để cơ thể quen dần — thầy Thạch cũng bắt đầu như vậy." };
  if (score <= 4) return { n: 2, why: "Em đã đi bộ được khá lâu: thêm đi nhanh và học 5 động tác nền." };
  if (score <= 6) return { n: 3, why: "Em đã quen vận động: tập tay không toàn thân, chạy xen đi bộ." };
  if (p.push >= 3 && p.walk >= 3 && p.activity >= 2) return { n: 5, why: "Em đã tập đều và khá khoẻ: vào thẳng HIIT đầy đủ, theo dõi tiêu chí để lên phòng gym." };
  return { n: 4, why: "Em đã có nền tốt: bắt đầu làm quen Tabata và HIIT nhẹ." };
}

/** Bậc tối đa được phép theo sức khoẻ. */
export const maxStageFor = (p: Profile) => (p.health.length && !p.doctorOk ? 1 : p.health.includes("hen") || p.health.includes("khop") ? 3 : 6);

/** Chỉnh thời lượng buổi theo số phút em có. */
export function scaleSession(s: Session, minutes: Profile["minutes"]): Session {
  const f = minutes === 20 ? 0.67 : minutes === 45 ? 1.4 : 1;
  return {
    ...s,
    blocks: s.blocks.map((b) => {
      if (s.scaleWalk && b.items.length === 1 && b.rounds === 1 && b.work >= 600) return { ...b, work: Math.round((b.work * f) / 60) * 60 };
      if (!b.fixed && b.rounds >= 2) return { ...b, rounds: Math.max(1, Math.min(b.rounds + 2, Math.round(b.rounds * f))) };
      return b;
    }),
  };
}

export type Phase = { kind: "work" | "rest"; sec: number; label: string; move?: Move; next?: string; block: string };

/** Trải buổi thành các pha cho đồng hồ: khởi động → các khối → giãn cơ. */
export function phasesOf(s: Session, quiet: boolean): Phase[] {
  const out: Phase[] = [];
  const pick = (id: string): Move => {
    const m = moveById(id) ?? { id, name: id, cue: "" };
    return quiet && m.quiet ? { ...m, name: `${m.name} — bản không bật`, cue: m.quiet } : m;
  };
  const blocks = s.type === "gym" && s.blocks[0]?.items[0] === "may_di_bo" ? [...s.blocks, COOLDOWN] : [WARMUP, ...s.blocks, COOLDOWN];
  for (const b of blocks) {
    if (!b.items.length) {
      out.push({ kind: "rest", sec: b.rest, label: "Nghỉ", block: b.label });
      continue;
    }
    for (let r = 0; r < b.rounds; r++) {
      b.items.forEach((id, i) => {
        out.push({ kind: "work", sec: b.work, label: pick(id).name, move: pick(id), block: b.rounds > 1 ? `${b.label} · vòng ${r + 1}/${b.rounds}` : b.label });
        const last = i === b.items.length - 1;
        const restSec = last ? (r < b.rounds - 1 ? (b.restRound ?? b.rest) : 0) : b.rest;
        if (restSec > 0) out.push({ kind: "rest", sec: restSec, label: last ? "Nghỉ giữa vòng" : "Nghỉ", block: b.label });
      });
    }
  }
  for (let i = 0; i < out.length; i++) {
    const nx = out.slice(i + 1).find((p) => p.kind === "work");
    out[i].next = nx?.label;
  }
  return out;
}
export const totalMin = (ph: Phase[]) => Math.round(ph.reduce((a, p) => a + p.sec, 0) / 60);

// ---------------------------------------------------------------------------------------------
// Lưu trên máy
export type WeekLog = { week: string; done: string[]; feel?: "nhe" | "vua" | "met" };
export type LocalState = { v: 1; profile: Profile | null; stage: number; stageSince: string; weeks: WeekLog[] };
export const EMPTY_STATE: LocalState = { v: 1, profile: null, stage: 1, stageSince: "", weeks: [] };

const key = (uid: string) => `taiNha:${uid || "khach"}`;
export function loadLocal(uid: string): LocalState {
  try {
    const raw = localStorage.getItem(key(uid));
    if (!raw) return EMPTY_STATE;
    const s = JSON.parse(raw) as LocalState;
    return s?.v === 1 ? { ...EMPTY_STATE, ...s } : EMPTY_STATE;
  } catch {
    return EMPTY_STATE;
  }
}
export function saveLocal(uid: string, s: LocalState) {
  try {
    localStorage.setItem(key(uid), JSON.stringify({ ...s, weeks: s.weeks.slice(-12) }));
  } catch {
    /* chế độ ẩn danh / bộ nhớ đầy: vẫn dùng được trong lần mở này */
  }
}
export function clearLocal(uid: string) {
  try {
    localStorage.removeItem(key(uid));
  } catch {
    /* bỏ qua */
  }
}

/** Gợi ý theo 2 tuần gần nhất (không tính tuần đang dở). */
export function progressHint(s: LocalState, planned: number, thisWeek: string): "len" | "giu" | "nhe-lai" | null {
  const past = s.weeks.filter((w) => w.week < thisWeek && w.week >= s.stageSince).slice(-2);
  if (past.length < 2) return null;
  if (past.every((w) => w.feel === "met")) return "nhe-lai";
  const st = stageByN(s.stage);
  const weeksIn = s.weeks.filter((w) => w.week < thisWeek && w.week >= s.stageSince && w.done.length > 0).length;
  if (weeksIn >= st.minWeeks && past.every((w) => w.done.length >= planned - 1 && w.feel !== "met")) return "len";
  return "giu";
}
