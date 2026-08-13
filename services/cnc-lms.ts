export const CNC_PROGRESS = {
  turningQuizScore: 85,
  millingQuizScore: 82,
  turningOperationPassed: false,
  millingOperationPassed: false,
};

export const CNC_SETUP_CHECKLIST = [
  "Kiểm tra nguồn điện, khí nén, dầu bôi trơn và trạng thái nút dừng khẩn.",
  "Mở máy đúng trình tự và quan sát cảnh báo trên màn hình điều khiển.",
  "Di chuyển máy về chuẩn máy Reference point.",
  "Kiểm tra chiều quay trục chính và chế độ vận hành đang chọn.",
  "Gá phôi chắc chắn, đúng vị trí và bảo đảm không vướng hành trình dao.",
  "Gá dao đúng ổ dao, đúng chiều, đủ chiều dài kẹp dao an toàn.",
  "Cài đặt Geometry Offset cho dao theo phương X, Z hoặc các trục liên quan.",
  "Cài đặt Work shift / G54 theo chuẩn phôi.",
  "Chạy mô phỏng, Single Block hoặc Test không tải trước khi cắt thật.",
  "Ghi nhận lỗi, vệ sinh khu vực làm việc và thực hiện 5S cuối ca.",
];

export const CNC_GATE_QUIZ = [
  {
    id: "cnc-gate-1",
    question: "Trước khi mở máy CNC, thao tác nào bắt buộc phải kiểm tra đầu tiên?",
    options: [
      "Nguồn điện, khí nén, dầu bôi trơn và trạng thái nút dừng khẩn.",
      "Tốc độ cắt trong chương trình NC.",
      "Màu sắc của phôi sau gia công.",
      "Tên file chương trình trên máy tính cá nhân.",
    ],
    correctIndex: 0,
    explanation:
      "Nguồn, khí nén, bôi trơn và nút dừng khẩn là các điều kiện an toàn nền tảng trước khi vận hành.",
  },
  {
    id: "cnc-gate-2",
    question: "Khi vừa mở máy, vì sao phải đưa máy về chuẩn máy Reference point?",
    options: [
      "Để bộ điều khiển xác lập đúng tọa độ gốc máy trước khi thao tác tiếp.",
      "Để làm nóng phôi trước khi cắt.",
      "Để tự động sửa mọi lỗi trong chương trình NC.",
      "Để tăng tốc độ trục chính lên mức lớn nhất.",
    ],
    correctIndex: 0,
    explanation:
      "Reference point giúp máy biết vị trí chuẩn của các trục, tránh sai lệch tọa độ khi vận hành.",
  },
  {
    id: "cnc-gate-3",
    question: "Khi gá phôi, yêu cầu nào là quan trọng nhất trước khi chạy thử?",
    options: [
      "Phôi được kẹp chắc chắn, đúng vị trí và không cản trở hành trình dao.",
      "Phôi được đặt càng xa mâm cặp càng tốt.",
      "Phôi chưa cần siết chặt vì chỉ đang chạy mô phỏng.",
      "Phôi phải chạm trực tiếp vào mọi dao trong ổ dao.",
    ],
    correctIndex: 0,
    explanation:
      "Phôi lỏng hoặc đặt sai vị trí có thể gây văng phôi, gãy dao hoặc va chạm máy.",
  },
  {
    id: "cnc-gate-4",
    question: "Geometry Offset dùng để làm gì trong quá trình cài đặt dao?",
    options: [
      "Khai báo vị trí/kích thước dao để máy tính đúng đường chạy dao.",
      "Đổi màu hiển thị của chương trình NC.",
      "Lưu tên sinh viên thực hành.",
      "Tự động chọn vật liệu phôi.",
    ],
    correctIndex: 0,
    explanation:
      "Geometry Offset cho bộ điều khiển biết vị trí thực của mũi dao theo hệ tọa độ máy/phôi.",
  },
  {
    id: "cnc-gate-5",
    question: "Work shift hoặc G54 thường được dùng để xác lập điều gì?",
    options: [
      "Gốc tọa độ làm việc của phôi.",
      "Mật khẩu đăng nhập máy.",
      "Tốc độ quạt làm mát trong xưởng.",
      "Số lượng sinh viên trong nhóm.",
    ],
    correctIndex: 0,
    explanation:
      "G54/Work shift xác định gốc tọa độ gia công trên phôi để chương trình chạy đúng vị trí.",
  },
  {
    id: "cnc-gate-6",
    question: "Trước khi cắt thật, sinh viên bắt buộc phải thực hiện bước nào?",
    options: [
      "Mô phỏng, chạy thử không tải hoặc Single Block để kiểm tra va chạm.",
      "Bỏ qua mô phỏng nếu đã từng làm bài tương tự.",
      "Tăng Feed Override lên 100% ngay từ đầu.",
      "Tắt dung dịch làm mát và đứng sát vùng cắt.",
    ],
    correctIndex: 0,
    explanation:
      "Chạy thử giúp phát hiện sai tọa độ, sai dao, sai chiều chạy hoặc nguy cơ va chạm trước khi cắt thật.",
  },
  {
    id: "cnc-gate-7",
    question: "Nếu trong lúc chạy thử thấy dao đi sai hướng hoặc có nguy cơ va chạm, cần làm gì?",
    options: [
      "Dừng máy ngay bằng Stop/Emergency Stop theo tình huống và báo giảng viên.",
      "Đứng quan sát thêm đến khi dao chạm phôi.",
      "Tăng tốc độ chạy dao để chương trình kết thúc nhanh.",
      "Tự ý tháo phôi khi trục chính còn quay.",
    ],
    correctIndex: 0,
    explanation:
      "Khi có nguy cơ mất an toàn, ưu tiên dừng máy và báo giảng viên, không cố tiếp tục chương trình.",
  },
  {
    id: "cnc-gate-8",
    question: "Trong chế độ JOG/HANDLE, nguyên tắc thao tác an toàn là gì?",
    options: [
      "Di chuyển từng bước có kiểm soát, quan sát khoảng cách dao-phôi-mâm cặp.",
      "Giữ nút di chuyển liên tục mà không cần quan sát vùng máy.",
      "Chỉ nhìn màn hình, không cần nhìn vị trí dao thật.",
      "Cho phép nhiều người cùng bấm bảng điều khiển.",
    ],
    correctIndex: 0,
    explanation:
      "JOG/HANDLE là thao tác tay, nên phải di chuyển chậm, có kiểm soát và luôn quan sát vùng gia công.",
  },
  {
    id: "cnc-gate-9",
    question: "Khi tắt máy và kết thúc ca thực hành, việc nào thuộc quy trình bắt buộc?",
    options: [
      "Tắt máy đúng trình tự, vệ sinh công nghiệp và thực hiện 5S.",
      "Để phoi và dụng cụ lại cho nhóm sau tự xử lý.",
      "Tắt nguồn chính khi trục chính vẫn đang quay.",
      "Mang dao và đồ gá ra khỏi xưởng không cần báo giảng viên.",
    ],
    correctIndex: 0,
    explanation:
      "Kết thúc ca phải đưa máy về trạng thái an toàn, vệ sinh và sắp xếp đúng 5S.",
  },
  {
    id: "cnc-gate-10",
    question: "Điều kiện để được lên máy thực tập trong bài vận hành CNC là gì?",
    options: [
      "Hoàn thành checklist và trả lời đúng toàn bộ 10 câu hỏi chốt chặn.",
      "Chỉ cần xem tiêu đề video là đủ.",
      "Chỉ cần có mặt trong xưởng đúng giờ.",
      "Chỉ cần nộp file .NC, không cần kiểm tra an toàn.",
    ],
    correctIndex: 0,
    explanation:
      "Đây là bài kiểm tra chốt chặn an toàn, nên yêu cầu đúng 10/10 trước khi thực hành trực tiếp.",
  },
];

export const CNC_LESSON_4_TURN_QUIZ = [
  {
    id: "lesson-4-turn-q1",
    question: "Trước khi mở máy tiện CNC, nội dung nào phải được kiểm tra?",
    options: ["Tình trạng nguyên vẹn của máy, nguồn điện, nút dừng khẩn và ổ dao.", "Kết nối Internet của máy tính.", "Mở WinNC và kiểm tra chương trình cũ.", "Tra dầu mâm cặp trước khi cấp nguồn."],
    correctIndex: 0,
    explanation: "Phải kiểm tra tình trạng máy, nguồn điện, nút dừng khẩn và ổ dao trước khi cấp nguồn.",
  },
  {
    id: "lesson-4-turn-q2",
    question: "Trình tự mở máy tiện EMCO Turn 55/60 nào đúng?",
    options: ["Mở WinNC → mở máy tính → bật CB → mở khóa.", "Bật CB → mở khóa 0→1 → bật máy tính → xoay nút dừng khẩn theo chiều kim đồng hồ → mở WinNC Fanuc 21T.", "Nhấn dừng khẩn → bật CB → mở khóa → mở WinNC.", "Bật máy tính → mở WinNC → bật CB → chạy chương trình."],
    correctIndex: 1,
    explanation: "Trình tự đúng là bật CB, mở khóa, bật máy tính, nhả dừng khẩn rồi mở WinNC Fanuc 21T.",
  },
  {
    id: "lesson-4-turn-q3",
    question: "Muốn nhả nút dừng khẩn cấp trên máy tiện, cần thao tác thế nào?",
    options: ["Nhấn nút thêm một lần.", "Dùng khóa lục giác.", "Xoay nút theo chiều kim đồng hồ.", "Giữ nút trong 5 giây."],
    correctIndex: 2,
    explanation: "Nút dừng khẩn được nhả bằng cách xoay theo chiều kim đồng hồ.",
  },
  {
    id: "lesson-4-turn-q4",
    question: "Trình tự đưa máy tiện về điểm chuẩn Reference nào đúng?",
    options: ["Chọn JOG → Feed 100% → Reference.", "Chọn chế độ Reference → Feed 100% → thực hiện Reference.", "Nhập G28 trong MDI.", "Chọn EDIT rồi mở POS."],
    correctIndex: 1,
    explanation: "Chọn chế độ Reference, đặt Feed Override 100% và đưa máy về chuẩn.",
  },
  {
    id: "lesson-4-turn-q5",
    question: "Trong chế độ JOG, muốn di chuyển nhanh các trục cần dùng phím nào?",
    options: ["Phím hướng trục kết hợp phím Rapid có biểu tượng sóng.", "Các phím F1–F12.", "Các phím số.", "Shift kết hợp Handle."],
    correctIndex: 0,
    explanation: "Dùng phím hướng trục kết hợp phím Rapid để di chuyển nhanh có kiểm soát.",
  },
  {
    id: "lesson-4-turn-q6",
    question: "Khi gá dao tiện, cách kiểm tra chiều cao mũi dao phù hợp là gì?",
    options: ["Dùng căn lá.", "Căn mũi dao trùng với tâm ụ động.", "Để dao nhô dài nhất có thể.", "Gõ búa để chỉnh dao."],
    correctIndex: 1,
    explanation: "Mũi dao phải được căn trùng với tâm ụ động để bảo đảm đúng chiều cao tâm.",
  },
  {
    id: "lesson-4-turn-q7",
    question: "Trước khi cài đặt dữ liệu dao và phôi mới, thao tác nào phải thực hiện?",
    options: ["Khởi động lại máy.", "Chạy Dry Run ngay.", "Xóa dữ liệu Workshift X/Z và Geometry X/Z/R/T của dao cần cài.", "Nhấn RESET 5 lần."],
    correctIndex: 2,
    explanation: "Phải xóa dữ liệu Workshift và Geometry cũ để tránh kế thừa sai lệch từ bài trước.",
  },
  {
    id: "lesson-4-turn-q8",
    question: "Công thức xác định khoảng cách MW trong cài đặt Workshift máy tiện là gì?",
    options: ["MW = MA − AW.", "MW = MA × AW.", "MW = MA + AW.", "MW = MA ÷ AW."],
    correctIndex: 2,
    explanation: "Theo quy trình cài đặt, MW được xác định bằng MA + AW.",
  },
  {
    id: "lesson-4-turn-q9",
    question: "Khi nhập MA và AW vào Workshift, giá trị được nhập theo cách nào?",
    options: ["Nhập giá trị dương.", "Nhập −MA tại Shift value Z và −AW tại Measurement Z.", "Nhập cả hai bằng 0.", "Để máy tự động tính, không cần nhập."],
    correctIndex: 1,
    explanation: "Các giá trị được nhập theo dấu âm tại đúng trường Shift value Z và Measurement Z.",
  },
  {
    id: "lesson-4-turn-q10",
    question: "Khi dao cách mặt phôi khoảng 5 mm, cần điều chỉnh lượng chạy dao thế nào?",
    options: ["Giữ Feed Override 40%.", "Giảm dần từ 40% xuống 2% hoặc mức nhỏ nhất.", "Tăng lên 100%.", "Chuyển sang Handle nhanh."],
    correctIndex: 1,
    explanation: "Khi dao gần phôi phải giảm Feed Override xuống khoảng 2% để rà chạm an toàn.",
  },
  {
    id: "lesson-4-turn-q11",
    question: "Với dao chuẩn có Ztool1 = 0, tọa độ máy theo Z được nhập vào Workshift thế nào?",
    options: ["Nhập +Zmachine.", "Nhập −Zmachine vào Z Workshift.", "Nhập 0.", "Nhập chiều dài phôi."],
    correctIndex: 1,
    explanation: "Giá trị tọa độ máy của dao chuẩn được nhập với dấu âm vào Z Workshift.",
  },
  {
    id: "lesson-4-turn-q12",
    question: "Công thức xác định giá trị Z của các dao còn lại là gì?",
    options: ["Ztool = Zmachine − MW.", "Ztool = Zmachine + MW.", "Ztool = Zmachine × MW.", "Ztool = MW − Zmachine."],
    correctIndex: 0,
    explanation: "Giá trị dao còn lại được xác định theo công thức Ztool = Zmachine − MW.",
  },
  {
    id: "lesson-4-turn-q13",
    question: "Vì sao cần tiện thử một đoạn trụ ngắn khoảng 10 mm khi cài đặt dao?",
    options: ["Để kiểm tra rung động trục chính.", "Để tạo một bậc trên phôi.", "Để đo đường kính cắt thực tế bằng thước cặp.", "Để tăng độ cứng của phôi."],
    correctIndex: 2,
    explanation: "Đo đoạn trụ vừa tiện giúp xác định chính xác vị trí thực của mũi dao theo phương X.",
  },
  {
    id: "lesson-4-turn-q14",
    question: "Nếu đường kính tiện thử đo được là 23,8 mm, cần nhập dữ liệu nào?",
    options: ["Nhập 23.8 rồi INPUT.", "Nhập X23.8 rồi chọn MEASURE/F4.", "Nhập X−23.8.", "Nhập X0."],
    correctIndex: 1,
    explanation: "Nhập X23.8 và dùng chức năng MEASURE/F4 để bộ điều khiển xác lập bù dao.",
  },
  {
    id: "lesson-4-turn-q15",
    question: "Đoạn lệnh MDI nào phù hợp để kiểm tra dao số 2 sau khi cài đặt?",
    options: ["T0202; G00 X0 Z0; M30;", "T0202; M3 (M4) S800; G1 X27 Z0 F1; M5;", "G90 G54; G00 X0 Y0;", "T0202 M03 S1500; G00 X0 Z−50;"],
    correctIndex: 1,
    explanation: "Đoạn lệnh gọi dao, quay trục chính ở tốc độ phù hợp và tiến dao chậm để kiểm tra vị trí.",
  },
  {
    id: "lesson-4-turn-q16",
    question: "Nếu phát hiện nguy cơ va chạm trong khi vận hành, thao tác ưu tiên là gì?",
    options: ["Nhấn RESET.", "Nhấn FEED HOLD.", "Nhấn nút dừng khẩn cấp.", "Tắt nguồn máy tính."],
    correctIndex: 2,
    explanation: "Khi có nguy cơ va chạm phải dừng khẩn cấp ngay để bảo vệ người và máy.",
  },
  {
    id: "lesson-4-turn-q17",
    question: "Nếu toàn bộ kích thước X/Z đều sai sau khi cài đặt, nguyên nhân thường gặp nhất là gì?",
    options: ["Dung dịch làm mát không đủ.", "Rà chạm, đo hoặc nhập dữ liệu cài đặt sai.", "Tốc độ trục chính bị giảm.", "Sai cú pháp G01/G02."],
    correctIndex: 1,
    explanation: "Sai lệch đồng loạt thường xuất phát từ thao tác rà chạm, đo hoặc nhập dữ liệu gốc và dao.",
  },
  {
    id: "lesson-4-turn-q18",
    question: "Rà dao với lượng chạy dao quá lớn có thể gây hậu quả nào?",
    options: ["Lỏng cơ cấu kẹp dao.", "Mẻ hoặc gãy dao, hỏng phôi và tạo sai số cài đặt lớn.", "Quá tải trục chính ngay lập tức.", "Làm dịch chuyển điểm Reference của máy."],
    correctIndex: 1,
    explanation: "Rà dao nhanh dễ làm mẻ/gãy dao, hỏng phôi và khiến giá trị cài đặt sai lớn.",
  },
  {
    id: "lesson-4-turn-q19",
    question: "Theo nguyên tắc chốt chặn an toàn, điểm bài thực hành được tính khi nào?",
    options: ["Chỉ cần đạt phần an toàn rồi lấy điểm trung bình.", "Chỉ tính tổng điểm thực hành khi điểm kỹ thuật đạt từ 2,5/10 trở lên.", "Chỉ tính chất lượng sản phẩm.", "Luôn lấy trung bình, không có điểm chốt chặn."],
    correctIndex: 1,
    explanation: "Điểm kỹ thuật tối thiểu 2,5/10 là điều kiện chốt chặn trước khi tính tổng điểm thực hành.",
  },
  {
    id: "lesson-4-turn-q20",
    question: "Cuối ca thực hành máy tiện, công việc bảo dưỡng nào phải thực hiện?",
    options: ["Tháo toàn bộ ổ dao.", "Vệ sinh phoi và dầu, bôi trơn băng trượt, làm sạch khu vực làm việc.", "Xả toàn bộ dung dịch làm mát.", "Chỉ cần tắt nguồn máy."],
    correctIndex: 1,
    explanation: "Cuối ca phải vệ sinh, bôi trơn và thực hiện 5S tại khu vực máy.",
  },
];

export const CNC_LESSON_4_MILL_QUIZ = [
  {
    id: "lesson-4-mill-q1",
    question: "Điểm gốc tọa độ máy M (Machine Zero Point) trên máy phay CNC có đặc điểm gì?",
    options: ["Do người vận hành tự chọn trước mỗi ca gia công.", "Do nhà sản xuất xác lập cố định, người vận hành không thể thay đổi.", "Thay đổi theo từng loại phôi khác nhau.", "Chỉ tồn tại trên máy tiện, không có trên máy phay."],
    correctIndex: 1,
    explanation: "M là gốc tọa độ máy, cố định từ khi thiết kế và là nền tảng để xác định các điểm chuẩn khác như W, N, P.",
  },
  {
    id: "lesson-4-mill-q2",
    question: "Điểm chuẩn phôi W (Workpiece Zero Point) khác điểm M ở chỗ nào?",
    options: ["W cố định còn M thay đổi.", "W do người lập trình tự chọn dựa trên bản vẽ, có thể thay đổi linh hoạt.", "W chỉ dùng cho trục Z, không dùng cho X, Y.", "W và M luôn trùng nhau trên máy phay."],
    correctIndex: 1,
    explanation: "Người lập trình chọn W tùy theo bản vẽ, thường tại tâm mặt đầu hoặc góc phôi; trong khi M là điểm cố định.",
  },
  {
    id: "lesson-4-mill-q3",
    question: "Bản chất của việc cài đặt Offset trên máy CNC là gì?",
    options: ["Vẽ lại bản vẽ chi tiết trên máy tính.", "Khai báo cho bộ điều khiển biết khoảng cách vectơ từ gốc máy M đến gốc phôi W.", "Thay đổi tốc độ quay trục chính.", "Kiểm tra độ mòn của dao cắt."],
    correctIndex: 1,
    explanation: "Offset là phần phiên dịch giữa hệ tọa độ máy cố định và hệ tọa độ phôi do người lập trình chọn trong không gian X, Y, Z.",
  },
  {
    id: "lesson-4-mill-q4",
    question: "Giá trị lưu trong bảng Tool Length Offset (mã H) dùng để làm gì?",
    options: ["Hiệu chỉnh chiều dài thực tế giữa các dao khác nhau, đưa điểm cắt về đồng nhất với hệ tọa độ phôi.", "Xác định gốc tọa độ phôi W.", "Đo đường kính của dao phay.", "Cài đặt tốc độ trục chính cho từng dao."],
    correctIndex: 0,
    explanation: "Mỗi dao có chiều dài lắp khác nhau; bảng H giúp máy xác định vị trí mũi từng dao so với chuẩn trục chính.",
  },
  {
    id: "lesson-4-mill-q5",
    question: "Đầu dò cơ khí dùng để xác định biên phôi theo X, Y hoạt động dựa trên nguyên lý nào?",
    options: ["Phát tín hiệu laser đo khoảng cách.", "Hai phần trụ nối bằng lò xo, lệch tâm khi đầu dò quay và chạm vật cản.", "Cân trọng lượng phôi để suy ra kích thước.", "Đo nhiệt độ bề mặt phôi."],
    correctIndex: 1,
    explanation: "Khi đầu dò quay và mũi dò chạm biên phôi, lực chạm làm hai phần trụ lệch tâm, tạo tín hiệu xác định vị trí biên.",
  },
  {
    id: "lesson-4-mill-q6",
    question: "Khi gá phôi có kê thêm tấm kê (parallels), điều gì cần lưu ý khi xác lập gốc phôi G54 theo trục Z?",
    options: ["Không cần quan tâm, máy tự động bù trừ.", "Phải tính đến chiều cao của ê-tô và tấm kê vào giá trị gốc Z.", "Chỉ cần quan tâm khi phay lỗ, không cần khi phay mặt phẳng.", "Tấm kê chỉ ảnh hưởng trục X, không ảnh hưởng Z."],
    correctIndex: 1,
    explanation: "Chiều cao của ê-tô và tấm kê làm thay đổi vị trí mặt chuẩn theo trục Z, vì vậy phải được tính vào giá trị gốc phôi G54.",
  },
  {
    id: "lesson-4-mill-q7",
    question: "Vì sao nên dùng thiết bị Z-Setter thay vì ước lượng bằng cảm giác tay khi đo chiều dài dao?",
    options: ["Z-Setter giúp gia công nhanh hơn.", "Z-Setter đảm bảo tính đồng nhất và chính xác, không phụ thuộc cảm giác chủ quan của người vận hành.", "Z-Setter thay thế được bảng Tool Offset.", "Z-Setter chỉ cần dùng một lần cho mọi máy."],
    correctIndex: 1,
    explanation: "Z-Setter tạo chuẩn đo có thể lặp lại, giảm sai lệch giữa các lần đo và giữa những người vận hành khác nhau.",
  },
  {
    id: "lesson-4-mill-q8",
    question: "Khi đầu dò cơ khí lệch tâm đang tiến vào chạm biên phôi theo phương X, dấu hiệu nào cho biết đầu dò đã chạm đúng vị trí cần đọc giá trị X_M?",
    options: ["Đầu dò dừng quay hoàn toàn.", "Đèn báo trên máy chuyển sang màu đỏ.", "Hai phần trụ của đầu dò từ lệch tâm chuyển về đồng tâm (\"nhảy tâm\").", "Trục chính tự động nâng lên độ cao an toàn."],
    correctIndex: 2,
    explanation: "Khi hai phần trụ chuyển từ lệch tâm về đồng tâm (nhảy tâm), đầu dò đã chạm biên phôi và người vận hành đọc giá trị tọa độ máy X_M.",
  },
  {
    id: "lesson-4-mill-q9",
    question: "Nếu chi tiết gia công bị sai lệch kích thước ĐỀU theo phương X hoặc Y, nguyên nhân nhiều khả năng nhất là gì?",
    options: ["Trục chính quay sai chiều.", "Quên cộng/trừ bán kính dao (D/2) khi rà biên phôi.", "Tốc độ chạy dao F quá nhanh.", "Dao bị mòn lưỡi cắt."],
    correctIndex: 1,
    explanation: "Sai lệch đều một khoảng cố định là dấu hiệu đặc trưng của lỗi tính toán tọa độ khi rà biên, không phải lỗi ngẫu nhiên như mòn dao.",
  },
  {
    id: "lesson-4-mill-q10",
    question: "Sau khi đọc được giá trị tọa độ máy X_M tại thời điểm đầu dò nhảy tâm, công thức tính giá trị X_thực để nhập vào G54 là gì? (biết đường kính đầu dò D = 10mm)",
    options: ["X_thực = X_M.", "X_thực = X_M ± D/2.", "X_thực = X_M + D.", "X_thực = X_M − 2D."],
    correctIndex: 1,
    explanation: "Tọa độ cần nhập vào G54 phải bù bán kính đầu dò, tức D/2 = 5 mm, theo dấu phù hợp với phía biên phôi đang rà.",
  },
];

export const CNC_LESSON_1_QUIZ = [
  {
    id: "lesson-1-q1",
    question: "Sự khác biệt cơ bản nhất về mặt chức năng giữa hệ thống điều khiển số NC (Numerical Control) và CNC (Computer Numerical Control) là gì?",
    options: [
      "Máy NC sử dụng truyền động vô cấp, còn máy CNC thì không.",
      "Máy NC không có khả năng lưu trữ chương trình gia công trong bộ nhớ, còn máy CNC tích hợp máy vi tính cho phép đọc, biên sửa và lưu trữ chương trình trong bộ nhớ để tái sử dụng.",
      "Máy NC gia công chính xác hơn máy CNC nhờ sử dụng băng lỗ nhị phân.",
      "Máy NC chỉ dùng để gia công các chi tiết có đáy phẳng.",
    ],
    correctIndex: 1,
    explanation: "Máy NC không có chức năng lưu giữ chương trình. Hệ CNC tích hợp máy vi tính và lưu trữ chương trình gia công trong bộ nhớ.",
  },
  {
    id: "lesson-1-q2",
    question: "Vào năm nào Viện Công nghệ Massachusetts (MIT - Mỹ) đã chế tạo thành công máy phay đứng điều khiển số NC 3D đầu tiên trên thế giới?",
    options: ["Năm 1946", "Năm 1952", "Năm 1958", "Năm 1968"],
    correctIndex: 1,
    explanation: "Năm 1952, máy phay đứng điều khiển số NC 3D đầu tiên được MIT chế tạo thành công.",
  },
  {
    id: "lesson-1-q3",
    question: "Giải pháp thay đổi dụng cụ tự động ATC (Automatic Tool Change) được ra đời vào năm nào để nâng cao trình độ tự động hóa trong khâu gia công?",
    options: ["Năm 1952", "Năm 1965", "Năm 1968", "Năm 1976"],
    correctIndex: 1,
    explanation: "Giải pháp thay đổi dụng cụ tự động (ATC) được ứng dụng từ năm 1965.",
  },
  {
    id: "lesson-1-q4",
    question: "Cấu tạo chung của một máy công cụ CNC gồm mấy phần chính?",
    options: [
      "Gồm 2 phần chính: Phần điều khiển và phần chấp hành.",
      "Gồm 3 phần chính: Phần cơ khí, phần điện tử và phần mềm hệ thống.",
      "Gồm 4 phần chính: Phần tủ điện, phần động cơ, trục chính và bàn máy.",
      "Gồm 2 phần chính: Phần cứng máy vi tính và phần mềm WinNC.",
    ],
    correctIndex: 0,
    explanation: "Cấu tạo máy CNC gồm 2 phần chính: phần điều khiển và phần chấp hành.",
  },
  {
    id: "lesson-1-q5",
    question: "Thành phần nào dưới đây thuộc phần chấp hành của máy tiện phay CNC?",
    options: [
      "Bộ xử lý tín hiệu và cơ cấu nội suy.",
      "Cơ cấu đọc chương trình và bộ nhớ máy.",
      "Máy cắt kim loại trực tiếp cắt gọt và các cơ cấu phụ trợ như tay máy, ổ chứa dao, tưới nguội, hút phoi.",
      "Chương trình điều khiển gồm các câu lệnh chuẩn bị.",
    ],
    correctIndex: 2,
    explanation: "Phần chấp hành gồm máy cắt kim loại và các cơ cấu tự động hóa như tay máy, ổ chứa dao và các cơ cấu phụ trợ.",
  },
  {
    id: "lesson-1-q6",
    question: "Trong kết cấu hộp tốc độ của máy CNC, bộ phận nào thường được sử dụng để dễ dàng thay đổi tốc độ tự động và thực hiện truyền động vô cấp?",
    options: ["Ly hợp cơ khí dùng chêm đệm.", "Các bánh răng di trượt gạt bằng tay.", "Ly hợp điện từ.", "Động cơ bước kẹp đai truyền."],
    correctIndex: 2,
    explanation: "Hộp tốc độ có phạm vi điều chỉnh lớn và truyền động vô cấp thường sử dụng ly hợp điện từ.",
  },
  {
    id: "lesson-1-q7",
    question: "Để khử khe hở của các bộ truyền trong xích truyền động chạy dao của máy CNC, người ta thường sử dụng cơ cấu nào?",
    options: ["Cơ cấu bánh răng quay ngược.", "Cơ cấu vít me – đai ốc bi.", "Cơ cấu thanh răng – bánh răng thẳng.", "Cơ cấu tay đòn thủy lực."],
    correctIndex: 1,
    explanation: "Trục chạy dao dùng cơ cấu vít me – đai ốc bi để khử khe hở truyền động.",
  },
  {
    id: "lesson-1-q8",
    question: "Ổ tích dụng cụ trong máy phay CNC có các dụng cụ cắt được cắm dọc theo chiều dài của xích tải được phân loại là dạng nào?",
    options: ["Ổ tích dao dạng đĩa tròn.", "Ổ dao vòng đồng tâm.", "Ổ tích dao dạng băng xích.", "Đài dao xoay hình sao."],
    correctIndex: 2,
    explanation: "Nhiều dụng cụ cắt cắm dọc theo chiều dài xích thuộc loại ổ tích dao dạng băng xích.",
  },
  {
    id: "lesson-1-q9",
    question: "Điểm nào dưới đây là nhược điểm (hạn chế) của việc ứng dụng máy công cụ CNC tại xưởng sản xuất?",
    options: [
      "Năng suất cắt gọt và tính tự động hóa thấp.",
      "Không thể gia công được các chi tiết có biên dạng phức tạp.",
      "Giá thành đầu tư ban đầu cao, hệ điều hành cơ - điện phức tạp và yêu cầu bảo dưỡng máy định kỳ rất nghiêm ngặt.",
      "Độ bóng bề mặt và độ chính xác gia công kém hơn máy vạn năng.",
    ],
    correctIndex: 2,
    explanation: "Máy CNC có giá thành cao, hệ cơ - điện phức tạp và hiệu quả kinh tế thấp khi gia công các chi tiết đơn giản.",
  },
  {
    id: "lesson-1-q10",
    question: "Theo quy tắc bàn tay phải dùng để xác định hệ trục tọa độ trên máy CNC, trục Z luôn trùng với trục chính của máy và được biểu diễn bằng ngón tay nào?",
    options: ["Ngón tay cái.", "Ngón tay trỏ.", "Ngón tay giữa.", "Ngón tay áp út."],
    correctIndex: 2,
    explanation: "Ngón giữa của bàn tay phải tương ứng với hướng chiều trục Z, trùng phương trục chính.",
  },
  {
    id: "lesson-1-q11",
    question: "Đối với máy tiện CNC, chiều dương của trục Z được quy ước như thế nào?",
    options: ["Hướng đi vào trong mâm cặp.", "Hướng đi ra xa mâm cặp.", "Hướng song song với bàn dao ngang về phía người vận hành.", "Hướng từ trên trần máy thẳng đứng xuống mâm cặp."],
    correctIndex: 1,
    explanation: "Trên máy tiện, chiều dương trục Z hướng ra xa mâm cặp và chiều âm hướng vào mâm cặp.",
  },
  {
    id: "lesson-1-q12",
    question: "Trên máy tiện CNC 2D thông thường, trục tọa độ nào sau đây không tồn tại?",
    options: ["Trục Z.", "Trục X.", "Trục Y.", "Cả trục X và Z."],
    correctIndex: 2,
    explanation: "Máy tiện CNC thông thường chỉ gồm hai trục tịnh tiến X và Z, không có trục Y.",
  },
  {
    id: "lesson-1-q13",
    question: "Các chuyển động quay xung quanh các trục tịnh tiến cơ bản X, Y, Z trên máy CNC được ký hiệu tương ứng là gì?",
    options: ["U, V, W.", "P, Q, R.", "A, B, C.", "I, J, K."],
    correctIndex: 2,
    explanation: "Chuyển động quay tương ứng quanh X, Y, Z được ký hiệu lần lượt bằng A, B, C.",
  },
  {
    id: "lesson-1-q14",
    question: "Điểm gốc tọa độ của máy M (Machine Zero Point) được định nghĩa là gì?",
    options: [
      "Điểm gốc do người vận hành tự cài đặt tại mặt đầu của phôi gia công.",
      "Điểm gốc cố định do nhà sản xuất xác lập ngay từ khi thiết kế máy, không thể thay đổi.",
      "Điểm nằm cố định ở góc trên cùng bên trái của bàn máy phay.",
      "Điểm dừng nghỉ tạm thời của đài gá dao khi thay đổi dao cắt.",
    ],
    correctIndex: 1,
    explanation: "Điểm gốc tọa độ máy M do nhà sản xuất xác lập khi thiết kế máy và không thể thay đổi.",
  },
  {
    id: "lesson-1-q15",
    question: "Trên máy tiện CNC, điểm gốc tọa độ của máy M (Machine Zero Point) thường nằm ở vị trí nào?",
    options: ["Nằm ở tâm mặt đầu ngoài của phôi.", "Nằm ở ổ chứa dao rơvonve.", "Nằm ở bên trong mâm cặp, trên đường tâm trục chính.", "Nằm ở đỉnh nhọn cao nhất của ụ động."],
    correctIndex: 2,
    explanation: "Trên máy tiện, gốc tọa độ máy M nằm cố định ở bên trong mâm cặp, trên đường tâm trục chính.",
  },
  {
    id: "lesson-1-q16",
    question: "Đặc điểm của điểm chuẩn (Zero) của phôi W (Workpiece Zero Point) là gì?",
    options: [
      "Là điểm cố định do nhà sản xuất quy định sẵn, không thể dịch chuyển.",
      "Là điểm thay đổi, vị trí do người lập trình tự lựa chọn và xác định dựa vào bản vẽ gia công chi tiết.",
      "Là điểm chuẩn trùng khít hoàn toàn với điểm gốc của dao N tại vành trục chính.",
      "Là điểm nằm ở ranh giới hành trình xa nhất của đài gá dao.",
    ],
    correctIndex: 1,
    explanation: "Điểm chuẩn phôi W do người lập trình tự chọn gắn lên phôi và có thể thay đổi.",
  },
  {
    id: "lesson-1-q17",
    question: "Điểm chuẩn tham chiếu R (Reference Point) trên máy CNC có vai trò chính là gì?",
    options: [
      "Là điểm chuẩn để người lập trình bắt đầu gán tọa độ X0, Y0, Z0 cho chi tiết.",
      "Dùng làm mốc cố định giúp hệ thống điều khiển đo và hiệu chỉnh lại khoảng cách thực tế so với điểm gốc M, đặc biệt sau sự cố mất điện.",
      "Là điểm tỳ nằm ở mặt đầu của chấu kẹp mâm cặp.",
      "Là điểm đo chiều dài gá thực tế của từng dao cắt.",
    ],
    correctIndex: 1,
    explanation: "Điểm R giúp đưa hệ đo lường về trạng thái kiểm tra chuẩn xác sau khi xảy ra sự cố mất điện.",
  },
  {
    id: "lesson-1-q18",
    question: "Đối với máy phay CNC, điểm chuẩn dao N (Tool mount reference point) nằm ở vị trí nào?",
    options: ["Nằm tại vành trục chính máy phay.", "Nằm tại mặt phẳng tỳ gá của ê-tô bàn máy.", "Nằm tại tâm mặt phẳng của đài dao rơvonve máy tiện.", "Nằm tại đỉnh nhọn thực tế của mũi dụng cụ cắt."],
    correctIndex: 0,
    explanation: "Trên máy phay, điểm chuẩn gá dao N nằm tại vành trục chính.",
  },
  {
    id: "lesson-1-q19",
    question: "Theo tiêu chuẩn ISO R841, ba trục thẳng NC thứ hai song song bắt buộc với các trục cơ bản X, Y, Z được ký hiệu lần lượt là gì?",
    options: ["A, B, C.", "U, V, W.", "P, Q, R.", "D, E, F."],
    correctIndex: 1,
    explanation: "Ba trục thẳng tịnh tiến phụ song song với X, Y, Z được ký hiệu lần lượt là U, V, W.",
  },
  {
    id: "lesson-1-q20",
    question: "Dạng điều khiển đường viền nào cho phép dịch chuyển dụng cụ cắt đồng thời trên cả ba trục X, Y, Z để gia công các bề mặt lồi lõm phức tạp trong không gian 3D?",
    options: ["Điều khiển điểm - điểm.", "Điều khiển đoạn thẳng.", "Điều khiển 2½D.", "Điều khiển 3D."],
    correctIndex: 3,
    explanation: "Điều khiển đường viền 3D cho phép dịch chuyển đồng thời cả ba trục máy để tạo biên dạng cong.",
  },
];

const CNC_LESSON_2_QUIZ_LEGACY = [
  {
    id: "lesson-2-q1",
    question: "Tên của một chương trình gia công tiện CNC tiêu chuẩn trên hệ điều hành Fanuc 21T bắt buộc phải bắt đầu bằng ký tự nào và theo sau là bao nhiêu chữ số?",
    options: ["Bắt đầu bằng chữ N và theo sau là 4 chữ số.", "Bắt đầu bằng chữ G và theo sau là 3 chữ số.", "Bắt đầu bằng chữ O và theo sau là 4 chữ số.", "Bắt đầu bằng chữ M và theo sau là 2 chữ số."],
    correctIndex: 2,
    explanation: "Tên chương trình gồm chữ O và bốn chữ số, ví dụ: O1601.",
  },
  {
    id: "lesson-2-q2",
    question: "Trong khối lệnh tổng quát của chương trình tiện CNC (Block), ký tự nào được quy ước dùng để kết thúc một câu lệnh?",
    options: ["Dấu hai chấm (:).", "Dấu chấm phẩy (;).", "Dấu gạch chéo (/).", "Dấu ngoặc đơn (()."],
    correctIndex: 1,
    explanation: "Khối lệnh thường bắt đầu bằng N… và kết thúc bởi dấu chấm phẩy (;).",
  },
  {
    id: "lesson-2-q3",
    question: "Để lập trình di chuyển dao đến điểm đích được xác định bằng giá trị khoảng cách tuyệt đối so với điểm chuẩn phôi (W), ta sử dụng mã lệnh G nào?",
    options: ["G90", "G91", "G92", "G53"],
    correctIndex: 0,
    explanation: "G90 là lệnh tọa độ tuyệt đối, dao di chuyển đến điểm chỉ thị so với điểm chuẩn.",
  },
  {
    id: "lesson-2-q4",
    question: "Khi sử dụng phương pháp lập trình tọa độ tương đối (G91) trên máy tiện CNC, các trục tọa độ tịnh tiến X và Z được thay thế tương ứng bằng các địa chỉ nào?",
    options: ["I và K", "U và W", "A và C", "P và Q"],
    correctIndex: 1,
    explanation: "Trên máy tiện, tọa độ tương đối sử dụng U và W thay cho X và Z.",
  },
  {
    id: "lesson-2-q5",
    question: "Nguyên công tiện CNC có chuyển động cắt gọt chủ yếu trên mặt phẳng ZX. Lệnh nào dùng để chọn mặt phẳng làm việc ZX trong chương trình tiện?",
    options: ["G17", "G18", "G19", "G28"],
    correctIndex: 1,
    explanation: "G18 chọn mặt phẳng làm việc ZX (hoặc XOZ) dùng cho máy tiện.",
  },
  {
    id: "lesson-2-q6",
    question: "Để khai báo đơn vị đo lường sử dụng trong chương trình gia công là hệ mét (Metric), người lập trình sử dụng mã lệnh nào?",
    options: ["G70", "G71", "G20", "G95"],
    correctIndex: 1,
    explanation: "Theo hệ Fanuc 21T trong giáo trình, G71 thiết lập đơn vị đo hệ mét (Metric units).",
  },
  {
    id: "lesson-2-q7",
    question: "Lượng chạy dao (Feedrate) trong gia công tiện CNC thường được tính theo đơn vị mm/vòng. Mã lệnh nào dùng để thiết lập chế độ lượng chạy dao này?",
    options: ["G94", "G95", "G96", "G97"],
    correctIndex: 1,
    explanation: "G95 thiết lập lượng tiến dao hoặc tốc độ chạy dao vòng, đơn vị mm/vòng trong gia công tiện.",
  },
  {
    id: "lesson-2-q8",
    question: "Mã lệnh G00 trong lập trình tiện CNC có công dụng chính là gì?",
    options: ["Chạy dao theo đường thẳng với tốc độ cắt định sẵn.", "Di chuyển dao nhanh không cắt gọt để định vị dụng cụ cắt.", "Nội suy cung tròn theo chiều kim đồng hồ.", "Rút dao an toàn về gốc tọa độ máy."],
    correctIndex: 1,
    explanation: "G00 dùng để chạy dao nhanh không cắt gọt.",
  },
  {
    id: "lesson-2-q9",
    question: "Trong câu lệnh N15 G01 X25 Z-30 F0.2; khi gia công bằng đơn vị mét và lượng chạy dao vòng, thông số F0.2 có ý nghĩa kỹ thuật là gì?",
    options: ["Chiều sâu cắt là 0,2 mm.", "Tốc độ quay trục chính là 0,2 vòng/phút.", "Lượng chạy dao là 0,2 mm/vòng.", "Thời gian dừng dao ở cuối hành trình là 0,2 giây."],
    correctIndex: 2,
    explanation: "G01 nội suy đường thẳng; F là tốc độ chạy dao, đơn vị mm/vòng khi dùng G95.",
  },
  {
    id: "lesson-2-q10",
    question: "Điểm khác biệt quan trọng nhất giữa mã lệnh G02 và G03 khi thực hiện tiện biên dạng cong là gì?",
    options: ["G02 dùng để tiện côn, G03 dùng để tiện rãnh.", "G02 nội suy cung tròn cùng chiều kim đồng hồ, G03 nội suy cung tròn ngược chiều kim đồng hồ.", "G02 yêu cầu nhập bán kính R, G03 yêu cầu nhập tọa độ tâm I, K.", "G02 di chuyển dao nhanh, G03 di chuyển dao cắt gọt có tải."],
    correctIndex: 1,
    explanation: "G02 nội suy cùng chiều kim đồng hồ, còn G03 nội suy ngược chiều kim đồng hồ.",
  },
  {
    id: "lesson-2-q11",
    question: "Trong chu trình tiện thô dọc trục G73: N50 G73 U1... R...; tham số U1 được định nghĩa là gì?",
    options: ["Lượng dư chừa lại để gia công tinh theo phương X.", "Khoảng cách rút dao lên sau mỗi lát cắt.", "Chiều sâu của một lớp cắt theo phương X.", "Lượng dư chừa lại để gia công tinh theo phương Z."],
    correctIndex: 2,
    explanation: "U1 là chiều sâu một lớp cắt theo phương X trong chu trình G73.",
  },
  {
    id: "lesson-2-q12",
    question: "Trong chu trình tiện thô dọc trục G73: N50 G73 U1... R...; tham số R được định nghĩa là gì?",
    options: ["Bán kính của cung tròn cần bo góc.", "Khoảng cách rút dao ra khi di chuyển dao về, với điều kiện R ≤ U1.", "Tốc độ quay tối đa của trục chính.", "Số hiệu của dao tiện thô."],
    correctIndex: 1,
    explanation: "R là khoảng cách rút dao ra khi di chuyển dao về và không lớn hơn U1.",
  },
  {
    id: "lesson-2-q13",
    question: "Ở khối lệnh thứ hai của chu trình tiện thô dọc trục G73: N55 G73 P60 Q70 U2... W...; các tham số U2 và W có ý nghĩa gì?",
    options: ["U2 là chiều sâu cắt phương X, W là chiều sâu cắt phương Z.", "U2 là lượng dư gia công tinh theo phương X, W là lượng dư gia công tinh theo phương Z.", "U2 là số câu lệnh bắt đầu, W là số câu lệnh kết thúc biên dạng.", "U2 và W là tọa độ điểm cực của chu trình."],
    correctIndex: 1,
    explanation: "U2 là lượng dư gia công tinh theo phương X, W là lượng dư gia công tinh theo phương Z.",
  },
  {
    id: "lesson-2-q14",
    question: "Sau khi thực hiện chu trình tiện thô dọc trục G73, để gọi chu trình tiện tinh dọc trục nhằm cắt sạch lượng dư theo đúng biên dạng đã lập trình, ta dùng mã lệnh nào?",
    options: ["G70", "G71", "G72", "G73"],
    correctIndex: 2,
    explanation: "Theo hệ Fanuc 21T trong giáo trình, G72 là chu trình tiện tinh dọc trục.",
  },
  {
    id: "lesson-2-q15",
    question: "Công dụng của chu trình G77 trong lập trình tiện hệ Fanuc 21T là gì?",
    options: ["Tiện các bề mặt côn phức tạp.", "Cắt ren trục bậc bước lớn.", "Tiện cắt rãnh hoặc cắt đứt chi tiết theo phương X.", "Khoan lỗ sâu tịnh tiến trục Z."],
    correctIndex: 2,
    explanation: "G77 là chu trình cắt rãnh theo phương X, dùng để tiện rãnh hoặc cắt đứt.",
  },
  {
    id: "lesson-2-q16",
    question: "Trong chu trình tiện ren bước lớn G78: N... G78 P1... Q1... R1...; nhóm 6 số sau địa chỉ P1 (ví dụ P020060) được chia làm 3 cặp số thể hiện các thông số nào?",
    options: ["Số lần cắt tinh, trị số Chamfer (vát mép đầu ren) và góc biên dạng ren (Profile).", "Chiều sâu cắt ren, bước ren và lượng rút dao an toàn.", "Tốc độ trục chính, lượng tiến dao và số lần cắt thô.", "Đường kính đỉnh ren, đường kính chân ren và chiều dài đoạn ren."],
    correctIndex: 0,
    explanation: "Hai số đầu là số lần cắt tinh, hai số tiếp là trị số Chamfer và hai số cuối là góc Profile ren.",
  },
  {
    id: "lesson-2-q17",
    question: "Sự khác biệt cơ bản về tính năng giữa hai mã dừng chương trình M02 và M30 là gì?",
    options: ["M02 dừng trục chính quay, M30 chỉ dừng tưới nguội.", "M02 kết thúc chương trình tại dòng lệnh đó; M30 kết thúc chương trình và tự động đưa con trỏ trở lại đầu chương trình.", "M02 dùng cho chương trình con, M30 dùng cho chương trình chính.", "M02 tắt nguồn máy hoàn toàn, M30 giữ máy ở chế độ chờ."],
    correctIndex: 1,
    explanation: "M30 kết thúc chương trình và tự động đưa con trỏ về vị trí đầu chương trình để có thể lặp lại.",
  },
  {
    id: "lesson-2-q18",
    question: "Lệnh nào được sử dụng để gọi chương trình con (Subprogram) và kết thúc chương trình con để trở về chương trình chính?",
    options: ["Gọi bằng M03, kết thúc bằng M05.", "Gọi bằng M08, kết thúc bằng M09.", "Gọi bằng M98, kết thúc bằng M99.", "Gọi bằng M06, kết thúc bằng M30."],
    correctIndex: 2,
    explanation: "M98 dùng để gọi chương trình con, M99 dùng để kết thúc chương trình con.",
  },
  {
    id: "lesson-2-q19",
    question: "Lệnh nào dùng để thiết lập giới hạn tốc độ quay lớn nhất của trục chính nhằm bảo đảm an toàn ly tâm khi tiện phôi có đường kính thay đổi lớn?",
    options: ["G96", "G97", "G50 (hoặc G92 tùy hệ trục)", "G95"],
    correctIndex: 2,
    explanation: "G50 (hoặc G92) dùng để giới hạn tốc độ quay lớn nhất của trục chính.",
  },
  {
    id: "lesson-2-q20",
    question: "Khi mô phỏng trên WinNC32 hệ Fanuc 21T, để khai báo kích thước phôi ảo (Workpiece) cho mô phỏng 3D sau khi bấm F12 và F11, ta chọn phím mềm nào?",
    options: ["[TOOLS] (F3)", "[WORKP] (F4)", "[SIMUL] (F5)", "[W.SHFT] (F5)"],
    correctIndex: 1,
    explanation: "Chọn kích thước phôi mô phỏng WORKP bằng phím F4 trên bàn phím đồ họa.",
  },
];

export const CNC_LESSON_2_QUIZ = [
  {id:"lesson-2-basic-q1",question:"Trong khối lệnh tổng quát N_ G_ X_ Y_ Z_ M_ S_ F_ T_ ;, ký tự N dùng để khai báo thông tin nào?",options:["Lệnh tốc độ trục chính","Số thứ tự câu lệnh","Lệnh chọn dụng cụ cắt","Lệnh bước tiến dao"],correctIndex:1,explanation:"N là số thứ tự của câu lệnh (số block) trong chương trình CNC."},
  {id:"lesson-2-basic-q2",question:"Ký tự nào sau đây biểu thị lệnh bước tiến dao (Feed) trong chương trình tiện CNC?",options:["S","T","F","M"],correctIndex:2,explanation:"F là địa chỉ khai báo lượng hoặc tốc độ chạy dao."},
  {id:"lesson-2-basic-q3",question:"Ký tự ; đặt ở cuối mỗi khối lệnh trong chương trình CNC có ý nghĩa gì?",options:["Bắt đầu khối lệnh","Khai báo bán kính dao","Ký tự kết thúc câu lệnh","Bỏ qua câu lệnh"],correctIndex:2,explanation:"Dấu chấm phẩy đánh dấu kết thúc một câu lệnh CNC."},
  {id:"lesson-2-basic-q4",question:"Cặp mã lệnh nào được dùng để khai báo đơn vị đo trong hệ tọa độ gia công?",options:["G94 và G95","G70 và G71","G17 và G18","G41 và G42"],correctIndex:1,explanation:"Theo hệ lệnh của tài liệu, G70 và G71 dùng để chọn hệ inch và hệ mét."},
  {id:"lesson-2-basic-q5",question:"Mã lệnh G71 dùng để khai báo đơn vị đo theo hệ nào?",options:["Hệ inch","Hệ mét","Hệ độ (Degree)","Hệ radian"],correctIndex:1,explanation:"G71 khai báo đơn vị theo hệ mét trong hệ điều khiển được sử dụng ở bài học."},
  {id:"lesson-2-basic-q6",question:"Mã lệnh G95 được ứng dụng trong gia công tiện có ý nghĩa là gì?",options:["Chọn lượng chạy dao theo mm/phút","Chọn lượng chạy dao theo mm/vòng","Chọn tốc độ trục chính theo vòng/phút","Khai báo đơn vị đo hệ mét"],correctIndex:1,explanation:"G95 chọn chế độ lượng chạy dao theo mỗi vòng quay của trục chính."},
  {id:"lesson-2-basic-q7",question:"Mã lệnh nào dùng cho chuyển động chạy dao nhanh không cắt gọt?",options:["G01","G00","G02","G03"],correctIndex:1,explanation:"G00 dùng để định vị nhanh, không thực hiện cắt gọt."},
  {id:"lesson-2-basic-q8",question:"Trong cấu trúc lệnh G00 X(U)... Z(W)...;, hai ký tự U và W biểu thị tọa độ điểm đến theo giá trị nào?",options:["Tọa độ tuyệt đối","Tọa độ tương đối","Tọa độ cực","Bán kính cung tròn"],correctIndex:1,explanation:"U và W biểu thị lượng dịch chuyển tương đối theo trục X và Z."},
  {id:"lesson-2-basic-q9",question:"Mã lệnh G01 thực hiện chức năng gì trong quá trình gia công?",options:["Chạy dao nhanh không cắt gọt","Nội suy cung tròn cùng chiều kim đồng hồ","Nội suy theo đường thẳng","Xóa bù trừ bán kính dao"],correctIndex:2,explanation:"G01 thực hiện nội suy tuyến tính với lượng chạy dao F."},
  {id:"lesson-2-basic-q10",question:"Để tiện mặt đầu, tiện trụ thẳng hoặc tiện côn, người ta thường áp dụng lệnh nào?",options:["G00","G01","G02","G73"],correctIndex:1,explanation:"Các chuyển động tiện thẳng và tiện côn cơ bản thường dùng nội suy đường thẳng G01."},
  {id:"lesson-2-basic-q11",question:"Mã lệnh G02 có công dụng nào sau đây?",options:["Nội suy cung tròn theo cùng chiều kim đồng hồ","Nội suy cung tròn theo ngược chiều kim đồng hồ","Nội suy theo đường thẳng","Chạy dao nhanh"],correctIndex:0,explanation:"G02 là nội suy cung tròn theo chiều kim đồng hồ."},
  {id:"lesson-2-basic-q12",question:"Khi muốn gia công một khối lồi bằng lệnh nội suy cung tròn ngược chiều kim đồng hồ, mã lệnh cần chọn là:",options:["G01","G02","G03","G72"],correctIndex:2,explanation:"G03 là nội suy cung tròn ngược chiều kim đồng hồ."},
  {id:"lesson-2-basic-q13",question:"Trong lệnh nội suy cung tròn (G02/G03), ký tự R đại diện cho tham số nào?",options:["Tốc độ quay trục chính","Khoảng cách rút dao","Bán kính cung tròn","Lượng dư gia công"],correctIndex:2,explanation:"R khai báo bán kính của cung tròn cần nội suy."},
  {id:"lesson-2-basic-q14",question:"Tham số I và K trong lệnh nội suy cung tròn (G02/G03) là tọa độ tương đối của tâm quay theo hai phương nào?",options:["I theo phương Z, K theo phương X","I theo phương X, K theo phương Z","I theo phương Y, K theo phương Z","I và K đều theo phương X"],correctIndex:1,explanation:"Trên mặt phẳng tiện XZ, I là độ lệch tâm theo X và K là độ lệch tâm theo Z."},
  {id:"lesson-2-basic-q15",question:"Mã lệnh nào được sử dụng để xóa chức năng bù trừ bán kính dao?",options:["G40","G41","G42","G70"],correctIndex:0,explanation:"G40 hủy chức năng bù bán kính dao."},
  {id:"lesson-2-basic-q16",question:"Để kích hoạt chế độ bù trừ bán kính dao bên phải, ta dùng mã lệnh nào?",options:["G40","G41","G42","G73"],correctIndex:2,explanation:"G42 kích hoạt bù bán kính dao bên phải quỹ đạo lập trình."},
  {id:"lesson-2-basic-q17",question:"Mã lệnh G73 trong lập trình tiện CNC có công dụng là gì?",options:["Chu trình tiện tinh dọc trục","Chu trình tiện thô dọc trục","Chu trình tiện rãnh","Lệnh chạy dao nhanh"],correctIndex:1,explanation:"Theo cấu trúc chu trình trong tài liệu, G73 là chu trình tiện thô dọc trục."},
  {id:"lesson-2-basic-q18",question:"Trong cấu trúc chu trình G73 P... Q... U2... W...;, tham số U2 và W lần lượt là:",options:["Tọa độ điểm bắt đầu và kết thúc","Chiều sâu cắt thô và khoảng cách rút dao","Lượng dư gia công tinh theo phương X và phương Z","Bước tiến dao thô và bước tiến dao tinh"],correctIndex:2,explanation:"U2 và W là lượng dư để lại cho gia công tinh theo phương X và Z."},
  {id:"lesson-2-basic-q19",question:"Mã lệnh được dùng để thực hiện chu trình tiện tinh dọc trục là:",options:["G01","G71","G72","G73"],correctIndex:2,explanation:"Theo hệ chu trình trong tài liệu, G72 thực hiện chu trình tiện tinh dọc trục."},
  {id:"lesson-2-basic-q20",question:"Trong các lệnh chu trình gia công (G73, G72), tham số P và Q có ý nghĩa gì?",options:["P là tốc độ trục chính, Q là lượng chạy dao","P là số thứ tự câu lệnh bắt đầu, Q là số thứ tự câu lệnh kết thúc biên dạng","P là bán kính dao, Q là lượng dư gia công","P là chiều sâu cắt, Q là khoảng cách lùi dao"],correctIndex:1,explanation:"P và Q xác định số thứ tự block bắt đầu và kết thúc của biên dạng gia công."},
];

void CNC_LESSON_2_QUIZ_LEGACY;

export const CNC_LESSON_3_QUIZ = [
  {
    id: "lesson-3-q1",
    question: "Tên chương trình phay CNC tiêu chuẩn trên hệ điều hành Fanuc 21M bắt đầu bằng ký tự nào?",
    options: ["Bắt đầu bằng chữ N và theo sau là 4 chữ số.", "Bắt đầu bằng chữ G và theo sau là 3 chữ số.", "Bắt đầu bằng chữ O và theo sau là 4 chữ số.", "Bắt đầu bằng chữ M và theo sau là 2 chữ số."],
    correctIndex: 2,
    explanation: "Tên chương trình gồm chữ O và bốn chữ số, ví dụ: O1601.",
  },
  {
    id: "lesson-3-q2",
    question: "Nguyên công phay CNC cơ bản thường được tiến hành trên mặt phẳng nào và mã lệnh nào dùng để lựa chọn mặt phẳng đó?",
    options: ["Mặt phẳng XY (XOY); sử dụng lệnh G17.", "Mặt phẳng ZX (XOZ); sử dụng lệnh G18.", "Mặt phẳng YZ (YOZ); sử dụng lệnh G19.", "Mặt phẳng tự do; sử dụng lệnh G54."],
    correctIndex: 0,
    explanation: "G17 chọn mặt phẳng làm việc XY (mặt phẳng XOY) sử dụng cho máy phay.",
  },
  {
    id: "lesson-3-q3",
    question: "Trong chương trình phay CNC, đơn vị tốc độ tiến dao (Feedrate) thường được lập trình bằng đơn vị nào và mã lệnh nào dùng để thiết lập đơn vị đó?",
    options: ["mm/vòng; sử dụng lệnh G95.", "mm/phút; sử dụng lệnh G94.", "inch/vòng; sử dụng lệnh G97.", "m/phút; sử dụng lệnh G96."],
    correctIndex: 1,
    explanation: "G94 thiết lập lượng chạy dao theo đơn vị mm/phút, đặc trưng trong gia công phay.",
  },
  {
    id: "lesson-3-q4",
    question: "Khi muốn lập trình di chuyển dao đến điểm đích được xác định bằng giá trị khoảng cách tuyệt đối so với điểm gốc phôi (W), ta sử dụng mã lệnh nào?",
    options: ["G90", "G91", "G92", "G53"],
    correctIndex: 0,
    explanation: "G90 là lệnh tọa độ tuyệt đối, dao di chuyển đến điểm xác định so với điểm gốc chuẩn.",
  },
  {
    id: "lesson-3-q5",
    question: "Trong hệ tọa độ tương đối (G91) trên máy phay CNC, dao di chuyển đến vị trí mới dựa trên cơ sở nào?",
    options: ["Khoảng cách so với điểm gốc máy M.", "Khoảng cách so với điểm gốc phôi W.", "Khoảng cách từ vị trí hiện tại của dao trước khi thực hiện câu lệnh.", "Khoảng cách so với điểm chuẩn dao N."],
    correctIndex: 2,
    explanation: "G91 là hệ tọa độ tương đối, dao tịnh tiến một khoảng so với điểm hiện hành trước đó.",
  },
  {
    id: "lesson-3-q6",
    question: "Mã lệnh G00 trên máy phay CNC được định nghĩa là gì?",
    options: ["Chạy dao theo đường thẳng với tốc độ tiến dao định sẵn.", "Di chuyển dao nhanh không cắt gọt để định vị dụng cụ cắt.", "Di chuyển dao tịnh tiến về chuẩn tham chiếu.", "Bù trừ bán kính mũi dao cắt."],
    correctIndex: 1,
    explanation: "G00 là lệnh di chuyển nhanh không cắt gọt, dùng để định vị dao.",
  },
  {
    id: "lesson-3-q7",
    question: "Khối lệnh N10 G01 X25 Y-25 F100; trên máy phay CNC có ý nghĩa kỹ thuật gì?",
    options: ["Định vị nhanh dao đến điểm tọa độ X25 Y-25.", "Nội suy đường thẳng đến điểm X25 Y-25 với tốc độ tiến dao 100 mm/phút.", "Nội suy đường thẳng đến điểm X25 Y-25 với tốc độ tiến dao 100 mm/vòng.", "Di chuyển dao nội suy cung tròn với lượng tiến dao 100 mm/phút."],
    correctIndex: 1,
    explanation: "G01 nội suy đường thẳng có cắt gọt; F là tốc độ chạy dao, đơn vị mm/phút khi dùng G94.",
  },
  {
    id: "lesson-3-q8",
    question: "Khi sử dụng lệnh nội suy đường thẳng G01 để bo góc hoặc vát góc trên mặt phẳng gia công, tham số nào được dùng để bo tròn một cung có bán kính quy định?",
    options: ["Địa chỉ C.", "Địa chỉ R.", "Địa chỉ I.", "Địa chỉ K."],
    correctIndex: 1,
    explanation: "Khi dùng G01 để bo cung, cấu trúc lệnh nhập thêm địa chỉ R.",
  },
  {
    id: "lesson-3-q9",
    question: "Điểm khác biệt quan trọng nhất giữa mã lệnh G02 và G03 khi phay biên dạng cong là gì?",
    options: ["G02 nội suy ngược chiều kim đồng hồ, G03 cùng chiều kim đồng hồ.", "G02 nội suy cùng chiều kim đồng hồ, G03 ngược chiều kim đồng hồ.", "G02 yêu cầu bán kính R, G03 yêu cầu tọa độ tâm I, J.", "G02 dùng trên mặt phẳng XY, G03 dùng trên mặt phẳng YZ."],
    correctIndex: 1,
    explanation: "G02 nội suy cùng chiều kim đồng hồ, còn G03 nội suy ngược chiều kim đồng hồ.",
  },
  {
    id: "lesson-3-q10",
    question: "Trong câu lệnh phay cung tròn sử dụng tọa độ tâm tương đối, hai địa chỉ I và J biểu diễn khoảng cách hình học nào?",
    options: ["Khoảng cách từ tâm cung tròn đến điểm gốc phôi W.", "Khoảng cách từ vị trí bắt đầu của cung tròn đến tâm cung tròn theo hai phương X và Y tương ứng.", "Khoảng cách từ tâm cung tròn đến vị trí kết thúc của cung tròn.", "Bán kính của cung tròn cần nội suy."],
    correctIndex: 1,
    explanation: "I và J là tọa độ tương đối của tâm cung tròn so với điểm bắt đầu theo trục X và Y.",
  },
  {
    id: "lesson-3-q11",
    question: "Để tránh sai số gia công do đường kính dụng cụ cắt gây ra khi phay biên dạng (Profile), người ta sử dụng các lệnh bù trừ bán kính dao nào?",
    options: ["G43 và G44.", "G41 và G42.", "G54 và G55.", "G90 và G91."],
    correctIndex: 1,
    explanation: "Lệnh bù bán kính để dịch quỹ đạo tâm dao gồm G41 bên trái và G42 bên phải.",
  },
  {
    id: "lesson-3-q12",
    question: "Khi dao phay di chuyển ở phía bên trái của đường biên chi tiết theo chiều tiến dao, ta sử dụng lệnh bù bán kính nào?",
    options: ["G40", "G41", "G42", "G43"],
    correctIndex: 1,
    explanation: "G41 bù bán kính dao trái, nghĩa là dao nằm bên trái đường biên theo chiều chuyển động.",
  },
  {
    id: "lesson-3-q13",
    question: "Lệnh nào được sử dụng để hủy bỏ hiệu chỉnh bù trừ bán kính dao sau khi đã phay xong biên dạng?",
    options: ["G40", "G49", "G80", "G53"],
    correctIndex: 0,
    explanation: "G40 hủy bỏ hiệu chỉnh bù trừ bán kính dao.",
  },
  {
    id: "lesson-3-q14",
    question: "Để hiệu chỉnh bù trừ chiều dài dao theo chiều dương (+), ta sử dụng mã lệnh G nào đi kèm với địa chỉ H?",
    options: ["G41 H_", "G42 H_", "G43 H_", "G44 H_"],
    correctIndex: 2,
    explanation: "G43 hiệu chỉnh chiều dài dao theo chiều dương, kết hợp với số hiệu hiệu chỉnh H.",
  },
  {
    id: "lesson-3-q15",
    question: "Lệnh nào được sử dụng để hủy bỏ hiệu chỉnh bù trừ chiều dài dụng cụ cắt?",
    options: ["G40", "G49", "G80", "G98"],
    correctIndex: 1,
    explanation: "G49 hủy bỏ hiệu chỉnh chiều dài dao.",
  },
  {
    id: "lesson-3-q16",
    question: "Mã lệnh M06 trong chương trình phay CNC hệ Fanuc 21M có chức năng gì?",
    options: ["Quay trục chính cùng chiều kim đồng hồ.", "Dừng trục chính không điều kiện.", "Thay dụng cụ cắt (thay dao tự động).", "Bật dung dịch tưới nguội."],
    correctIndex: 2,
    explanation: "M06 là chức năng phụ điều khiển thay dao tự động trên máy phay CNC.",
  },
  {
    id: "lesson-3-q17",
    question: "Để thiết lập hệ tọa độ gia công (gốc phôi W) trên máy phay CNC, người lập trình có thể lựa chọn 6 hệ tọa độ làm việc chuẩn nào?",
    options: ["G50 đến G55", "G52 đến G57", "G54 đến G59", "G90 đến G95"],
    correctIndex: 2,
    explanation: "Sáu hệ tọa độ làm việc chuẩn được chọn bằng các mã G54 đến G59.",
  },
  {
    id: "lesson-3-q18",
    question: "Lệnh G80 trong lập trình phay CNC được dùng để làm gì?",
    options: ["Kết thúc và hủy bỏ toàn bộ chu trình gia công lỗ.", "Hủy bỏ bù trừ bán kính dụng cụ cắt.", "Khởi động chu trình taro ren.", "Trả dụng cụ cắt về chuẩn tham chiếu máy."],
    correctIndex: 0,
    explanation: "G80 hủy bỏ toàn bộ chu trình gia công lỗ đã gọi trước đó.",
  },
  {
    id: "lesson-3-q19",
    question: "Trong chu trình khoan lỗ sâu bước G83: G83 G99 G90 G00 X50 Y50 Z-98 I-22 J3 F100; hai tham số I và J được định nghĩa lần lượt là gì?",
    options: ["I là bán kính hốc tròn, J là chiều sâu một lớp cắt.", "I là giá trị mỗi bước khoan theo phương trục chính, J là số bước khoan thực hiện.", "I là lượng dư gia công thô, J là lượng dư gia công tinh.", "I là khoảng cách an toàn, J là thời gian dừng ở đáy lỗ."],
    correctIndex: 1,
    explanation: "Trong chu trình G83 phay Fanuc, I định nghĩa trị số bước khoan và J định nghĩa số lần thực hiện bước khoan.",
  },
  {
    id: "lesson-3-q20",
    question: "Khi mô phỏng chương trình phay CNC trên WinNC32 hệ Fanuc 21M, để chạy mô phỏng kiểm tra chương trình (SIMULATION), ta nhấn phím mềm nào?",
    options: ["[TOOLS] (F3)", "[WORKP] (F4)", "[SIMUL] (F6)", "[3DVIEW] (F3)"],
    correctIndex: 2,
    explanation: "Ở chế độ phay WinNC 21M, phím đồ họa SIMUL để chạy mô phỏng là F6.",
  },
];

export const CNC_MILL_COMMAND_TRANSLATION_QUIZ = [
  { id: "mill-translate-q1", question: "G01 X20 Y10 F150", options: ["Phay đường thẳng (nội suy tuyến tính) đến X20 Y10, tốc độ chạy dao F150", "Nội suy cung tròn đến X20 Y10, F150", "Chạy dao nhanh (không cắt gọt) đến X20 Y10", "Bù chiều dài dao đến X20 Y10"], correctIndex: 0, explanation: "G01 là nội suy tuyến tính có cắt gọt; X, Y là tọa độ đích và F150 là tốc độ chạy dao." },
  { id: "mill-translate-q2", question: "G00 X0 Y0 Z50", options: ["Phay thẳng có cắt gọt đến X0 Y0 Z50", "Di chuyển nhanh (không cắt gọt) dao đến vị trí X0 Y0 Z50", "Nội suy cung tròn đến X0 Y0 Z50", "Dừng chương trình tại X0 Y0 Z50"], correctIndex: 1, explanation: "G00 dùng để định vị nhanh, không thực hiện chuyển động cắt gọt." },
  { id: "mill-translate-q3", question: "G03 X40 Y40 R20 F180", options: ["Nội suy cung tròn thuận chiều kim đồng hồ đến X40 Y40, R20", "Phay đường thẳng đến X40 Y40, R20", "Nội suy cung tròn ngược chiều kim đồng hồ đến X40 Y40, bán kính 20, F180", "Chạy dao nhanh đến X40 Y40, bán kính 20"], correctIndex: 2, explanation: "G03 là nội suy cung tròn ngược chiều kim đồng hồ; R20 là bán kính và F180 là tốc độ chạy dao." },
  { id: "mill-translate-q4", question: "G54 G90 G00 X0 Y0", options: ["Gọi gốc tọa độ máy, hệ tọa độ tương đối, chạy nhanh về X0 Y0", "Gọi gốc tọa độ phôi G54, hệ tọa độ tuyệt đối, chạy nhanh về gốc X0 Y0", "Gọi bù chiều dài dao H01, chạy nhanh về X0 Y0", "Gọi gốc tọa độ phôi G55, hệ tọa độ tương đối, về X0 Y0"], correctIndex: 1, explanation: "G54 chọn gốc phôi, G90 chọn tọa độ tuyệt đối và G00 định vị nhanh đến X0 Y0." },
  { id: "mill-translate-q5", question: "G43 H01 Z50", options: ["Bù bán kính dao theo H01, di chuyển đến Z50", "Hủy bù chiều dài dao, di chuyển đến Z50", "Bù chiều dài dao theo số hiệu H01, di chuyển dao lên Z50", "Gọi gốc tọa độ phôi H01, lên Z50"], correctIndex: 2, explanation: "G43 kích hoạt bù chiều dài dao dương, H01 chọn ô hiệu chỉnh chiều dài số 01 và Z50 là vị trí đích." },
  { id: "mill-translate-q6", question: "G91 G01 X10", options: ["Chuyển sang hệ tọa độ tuyệt đối, di chuyển đến X10", "Chuyển sang hệ tọa độ tương đối (incremental), di chuyển thêm 10mm theo X", "Chạy dao nhanh thêm 10mm theo X", "Nội suy cung tròn thêm 10mm theo X"], correctIndex: 1, explanation: "G91 chọn tọa độ tương đối; G01 X10 làm dao nội suy thẳng thêm 10 mm theo chiều dương X." },
  { id: "mill-translate-q7", question: "M03 S1000", options: ["Trục chính quay ngược chiều kim đồng hồ, tốc độ 1000mm/phút", "Bật dung dịch làm mát, tốc độ 1000 vòng/phút", "Trục chính quay thuận chiều kim đồng hồ, tốc độ 1000 vòng/phút", "Dừng trục chính ở tốc độ 1000 vòng/phút"], correctIndex: 2, explanation: "M03 khởi động trục chính theo chiều kim đồng hồ; S1000 đặt tốc độ 1000 vòng/phút." },
  { id: "mill-translate-q8", question: "G00 G90 X30 Y30 Z5", options: ["Chạy dao cắt gọt (feed) đến X30 Y30 Z5", "Chạy dao nhanh, tuyệt đối, đến vị trí X30 Y30 Z5", "Nội suy cung tròn đến X30 Y30 Z5", "Chạy dao nhanh, tương đối, đến X30 Y30 Z5"], correctIndex: 1, explanation: "G00 là chạy nhanh và G90 xác định X30 Y30 Z5 theo hệ tọa độ tuyệt đối." },
  { id: "mill-translate-q9", question: "G02 X60 Y0 I20 J0", options: ["Nội suy cung tròn dùng bán kính R, không dùng tâm I J", "Phay đường thẳng đến X60 Y0, bỏ qua I J", "Nội suy cung tròn thuận chiều kim đồng hồ đến X60 Y0, tâm cung cách điểm đầu (I20, J0)", "Nội suy cung tròn ngược chiều kim đồng hồ đến X60 Y0, tâm (I20, J0)"], correctIndex: 2, explanation: "G02 nội suy cung tròn theo chiều kim đồng hồ; I và J mô tả độ lệch tâm cung so với điểm bắt đầu." },
  { id: "mill-translate-q10", question: "G28 G91 Z0", options: ["Về gốc phôi G54 theo trục Z", "Về điểm tham chiếu máy (Machine Zero Point) theo trục Z, hệ tương đối", "Bù chiều dài dao theo trục Z", "Chạy dao nhanh tuyệt đối theo trục Z về 0"], correctIndex: 1, explanation: "G28 đưa trục về điểm tham chiếu máy; G91 Z0 khai báo điểm trung gian theo hệ tương đối cho trục Z." },
  { id: "mill-translate-q11", question: "G01 Z-5 F80", options: ["Chạy dao nhanh lên Z-5", "Nội suy cung tròn xuống Z-5", "Phay ăn dao xuống theo trục Z, sâu -5mm, F80", "Dừng dao tạm thời tại Z-5"], correctIndex: 2, explanation: "G01 tạo chuyển động ăn dao tuyến tính đến Z-5 với tốc độ chạy dao F80." },
  { id: "mill-translate-q12", question: "M08 / M09", options: ["Bật/tắt trục chính (Spindle)", "Bật (M08) và tắt (M09) dung dịch làm mát (Coolant)", "Bật/tắt đèn báo máy", "Bật/tắt chế độ Single Block"], correctIndex: 1, explanation: "M08 bật và M09 tắt hệ thống dung dịch làm mát." },
  { id: "mill-translate-q13", question: "G17 G02 X20 Y0 R10", options: ["Chọn mặt phẳng nội suy XZ, cung tròn ngược chiều kim đồng hồ", "Chọn mặt phẳng nội suy YZ, cung tròn thuận chiều kim đồng hồ", "Chọn mặt phẳng nội suy XY, cung tròn thuận chiều kim đồng hồ đến X20 Y0, R10", "Chọn mặt phẳng nội suy XY, phay đường thẳng đến X20 Y0"], correctIndex: 2, explanation: "G17 chọn mặt phẳng XY; G02 nội suy cung tròn theo chiều kim đồng hồ đến X20 Y0 với bán kính R10." },
  { id: "mill-translate-q14", question: "G20 / G21", options: ["Chọn hệ tọa độ tuyệt đối (G20) hoặc tương đối (G21)", "Chọn đơn vị đo Inch (G20) hoặc Milimet (G21)", "Chọn mặt phẳng nội suy XY (G20) hoặc XZ (G21)", "Bật (G20) hoặc tắt (G21) bù bán kính dao"], correctIndex: 1, explanation: "G20 thiết lập đơn vị inch, còn G21 thiết lập đơn vị milimét." },
  { id: "mill-translate-q15", question: "T01 M06", options: ["Gọi Work Offset số 01", "Gọi bù chiều dài dao số 01", "Gọi dao số 01 và thực hiện lệnh thay dao (Tool Change)", "Gọi chương trình con số 01"], correctIndex: 2, explanation: "T01 chọn dao số 01 và M06 thực hiện chu trình thay dao." },
  { id: "mill-translate-q16", question: "G04 X2.0", options: ["Di chuyển dao nhanh đến X2.0", "Dừng dao tạm thời (Dwell) trong 2 giây", "Phay đường thẳng đến X2.0 trong 2 giây", "Dừng chương trình 2 phút"], correctIndex: 1, explanation: "G04 là lệnh dừng tạm thời; trong cấu trúc của đề, X2.0 quy định thời gian dừng 2 giây." },
  { id: "mill-translate-q17", question: "G01 X50 Y50 Z-2 F100", options: ["Chỉ di chuyển theo Z, bỏ qua X và Y", "Nội suy cung tròn 3 trục đến (50, 50, -2)", "Chạy dao nhanh 3 trục đến (50, 50, -2)", "Phay nội suy thẳng đồng thời 3 trục X, Y, Z đến điểm (50, 50, -2), F100"], correctIndex: 3, explanation: "G01 nội suy tuyến tính đồng thời các trục được khai báo đến X50 Y50 Z-2 với tốc độ F100." },
  { id: "mill-translate-q18", question: "G40 G01 X30", options: ["Kích hoạt bù bán kính dao bên trái (G41)", "Hủy bù bán kính dao (Cutter Compensation Cancel), phay thẳng đến X30", "Kích hoạt bù bán kính dao bên phải (G42)", "Hủy bù chiều dài dao, phay thẳng đến X30"], correctIndex: 1, explanation: "G40 hủy bù bán kính dao, sau đó G01 thực hiện chuyển động thẳng đến X30." },
  { id: "mill-translate-q19", question: "M00 / M01", options: ["Kết thúc chương trình và quay về đầu (M30)", "Dừng trục chính và tắt coolant", "Dừng chương trình bắt buộc (M00) hoặc dừng tùy chọn (M01 - Optional Stop)", "Gọi chương trình con M00/M01"], correctIndex: 2, explanation: "M00 luôn dừng chương trình; M01 chỉ dừng khi chức năng Optional Stop được bật." },
  { id: "mill-translate-q20", question: "G92 X0 Y0 Z0 (thiết lập G54 tương đương)", options: ["Về điểm tham chiếu máy (Machine Zero Point)", "Thiết lập/gán giá trị tọa độ hiện tại của dao là gốc tọa độ phôi (Work Offset)", "Hủy toàn bộ Work Offset đang dùng", "Bù chiều dài dao về giá trị 0"], correctIndex: 1, explanation: "Trong ngữ cảnh câu hỏi, G92 gán tọa độ vị trí hiện tại thành X0 Y0 Z0 để thiết lập gốc làm việc." },
];

export const CNC_TURN_COMMAND_TRANSLATION_QUIZ = [
  {id:"turn-block-q1",question:"G00 X50 Z2",options:["Phay đường thẳng có cắt gọt đến X50 Z2","Chạy dao nhanh (không cắt gọt) đến vị trí X50 Z2","Nội suy cung tròn đến X50 Z2","Tiện ren đến X50 Z2"],correctIndex:1,explanation:"G00 là chuyển động định vị nhanh, không cắt gọt."},
  {id:"turn-block-q2",question:"G01 X30 Z-40 F0.2",options:["Tiện thẳng (nội suy tuyến tính) đến X30 Z-40, lượng chạy dao 0.2mm/vòng","Chạy dao nhanh đến X30 Z-40","Nội suy cung tròn đến X30 Z-40, F0.2","Tiện ren bước 0.2mm đến X30 Z-40"],correctIndex:0,explanation:"G01 nội suy tuyến tính đến X30 Z-40 với lượng chạy dao F0.2."},
  {id:"turn-block-q3",question:"G02 X40 Z-20 R10",options:["Nội suy cung tròn ngược chiều kim đồng hồ đến X40 Z-20, bán kính 10","Nội suy cung tròn thuận chiều kim đồng hồ đến X40 Z-20, bán kính 10","Tiện côn thẳng đến X40 Z-20, R10","Tiện rãnh tại X40 Z-20, sâu R10"],correctIndex:1,explanation:"G02 nội suy cung tròn thuận chiều kim đồng hồ, R10 là bán kính."},
  {id:"turn-block-q4",question:"G54 G90 G00 X100 Z100",options:["Gọi gốc tọa độ máy, hệ tương đối, chạy nhanh về X100 Z100","Gọi gốc tọa độ phôi G54, hệ tọa độ tuyệt đối, chạy nhanh về X100 Z100","Gọi bù dao T01, chạy nhanh về X100 Z100","Gọi gốc tọa độ phôi G55, hệ tương đối, về X100 Z100"],correctIndex:1,explanation:"G54 chọn gốc phôi, G90 chọn tọa độ tuyệt đối và G00 chạy nhanh."},
  {id:"turn-block-q5",question:"T0101",options:["Gọi dao số 01 và bù dao (offset) số 01","Gọi chương trình con số 01","Gọi gốc tọa độ phôi số 01","Gọi tốc độ trục chính số 01"],correctIndex:0,explanation:"Hai cặp số lần lượt chỉ số dao và số hiệu offset."},
  {id:"turn-block-q6",question:"G96 S150 M03",options:["Tốc độ trục chính không đổi vòng/phút S150, quay ngược chiều kim đồng hồ","Tốc độ cắt không đổi (Constant Surface Speed) 150 m/phút, trục chính quay thuận chiều kim đồng hồ","Tốc độ chạy dao không đổi F150, trục chính dừng","Giới hạn tốc độ trục chính tối đa 150 vòng/phút"],correctIndex:1,explanation:"G96 chọn tốc độ cắt không đổi, S150 đặt 150 m/phút và M03 quay thuận."},
  {id:"turn-block-q7",question:"G97 S1000 M03",options:["Tốc độ trục chính không đổi 1000 vòng/phút (constant RPM), quay thuận chiều kim đồng hồ","Tốc độ cắt không đổi 1000 m/phút, quay ngược chiều kim đồng hồ","Giới hạn tốc độ cắt tối đa 1000 m/phút","Chạy dao nhanh với tốc độ trục chính 1000"],correctIndex:0,explanation:"G97 chọn tốc độ vòng quay không đổi, S1000 và M03 quay thuận."},
  {id:"turn-block-q8",question:"G71 U2 R1",options:["Chu trình tiện tinh, chiều sâu cắt 2mm, lượng lùi dao 1mm","Chu trình tiện thô dọc trục (Rough Turning Cycle), chiều sâu cắt mỗi lát U2 (2mm/bán kính), lượng lùi dao R1","Chu trình tiện rãnh, chiều sâu 2mm, bán kính đáy rãnh 1mm","Chu trình tiện ren, bước ren 2mm, số lần cắt 1"],correctIndex:1,explanation:"G71 là chu trình tiện thô dọc trục; U và R đặt chiều sâu cắt và lượng lùi."},
  {id:"turn-block-q9",question:"G70 P10 Q20",options:["Chu trình tiện thô từ khối lệnh N10 đến N20","Chu trình tiện tinh (Finishing Cycle), thực hiện lại biên dạng từ khối lệnh N10 đến N20","Chu trình khoan lỗ từ N10 đến N20","Chu trình tiện ren từ N10 đến N20"],correctIndex:1,explanation:"G70 tiện tinh lại biên dạng được xác định từ block P đến Q."},
  {id:"turn-block-q10",question:"G28 U0 W0",options:["Về gốc tọa độ phôi G54 theo X, Z","Về điểm tham chiếu máy (Machine Zero Point) theo cả hai trục X (U0), Z (W0)","Chạy dao nhanh đến X0 Z0 theo hệ tuyệt đối","Tiện côn về vị trí gốc máy"],correctIndex:1,explanation:"G28 đưa các trục X và Z về điểm tham chiếu máy."},
  {id:"turn-block-q11",question:"G01 X-2 F0.1",options:["Tiện mặt đầu (Facing) vào tâm phôi đến đường kính X-2, F0.1","Chạy dao nhanh vào tâm phôi","Tiện ren vào tâm phôi","Tiện rãnh cắt đứt tại X-2"],correctIndex:0,explanation:"G01 chạy dao theo X vào qua tâm để tiện mặt đầu với F0.1."},
  {id:"turn-block-q12",question:"M08 / M09",options:["Bật/tắt trục chính (Spindle)","Bật (M08) và tắt (M09) dung dịch làm mát (Coolant)","Bật/tắt chế độ Single Block","Bật/tắt bù bán kính mũi dao"],correctIndex:1,explanation:"M08 bật và M09 tắt dung dịch làm mát."},
  {id:"turn-block-q13",question:"G96 G50 S2000",options:["Tốc độ cắt không đổi, giới hạn tốc độ trục chính tối đa (Max Spindle Speed) 2000 vòng/phút","Đặt gốc tọa độ phôi tại S2000","Tốc độ trục chính không đổi 2000 vòng/phút, không giới hạn","Tiện ren với bước 2000"],correctIndex:0,explanation:"G96 dùng tốc độ cắt không đổi và G50 S2000 giới hạn tốc độ trục chính."},
  {id:"turn-block-q14",question:"G32 X30 Z-40 F2.0",options:["Tiện thẳng thông thường đến X30 Z-40","Tiện ren (Thread Cutting) đơn giản đến X30 Z-40, bước ren F2.0","Chạy dao nhanh đến X30 Z-40","Chu trình tiện thô đến X30 Z-40"],correctIndex:1,explanation:"G32 cắt ren đến tọa độ đích, F2.0 là bước ren."},
  {id:"turn-block-q15",question:"G04 X2.0",options:["Di chuyển dao nhanh đến X2.0","Dừng dao tạm thời (Dwell) trong 2 giây","Tiện rãnh sâu 2.0mm","Dừng chương trình 2 phút"],correctIndex:1,explanation:"G04 là lệnh dừng tạm thời; X2.0 quy định thời gian 2 giây."},
  {id:"turn-block-q16",question:"G01 X50 Z-30 F0.15",options:["Tiện côn (taper) đồng thời hai trục X, Z đến điểm (50, -30), F0.15","Chỉ tiện theo Z, bỏ qua X","Chỉ tiện theo X, bỏ qua Z","Nội suy cung tròn đến (50, -30)"],correctIndex:0,explanation:"G01 nội suy đồng thời X và Z tạo đường côn đến điểm đích."},
  {id:"turn-block-q17",question:"G40 G01 X30",options:["Kích hoạt bù bán kính mũi dao bên trái (G41)","Hủy bù bán kính mũi dao (Tool Nose Radius Compensation Cancel), tiện thẳng đến X30","Kích hoạt bù bán kính mũi dao bên phải (G42)","Hủy bù chiều dài dao, tiện thẳng đến X30"],correctIndex:1,explanation:"G40 hủy bù bán kính mũi dao, G01 tiếp tục tiện thẳng đến X30."},
  {id:"turn-block-q18",question:"M00 / M01",options:["Kết thúc chương trình và quay về đầu (M30)","Dừng trục chính và tắt coolant","Dừng chương trình bắt buộc (M00) hoặc dừng tùy chọn (M01 - Optional Stop)","Gọi chương trình con M00/M01"],correctIndex:2,explanation:"M00 là dừng bắt buộc; M01 dừng khi Optional Stop được bật."},
  {id:"turn-block-q19",question:"G92 X40 Z-30 F2.0",options:["Chu trình tiện ren đơn giản (Simple Threading Cycle) đến X40 Z-30, bước ren F2.0","Thiết lập gốc tọa độ phôi tại X40 Z-30","Chu trình tiện thô đến X40 Z-30","Về điểm tham chiếu máy tại X40 Z-30"],correctIndex:0,explanation:"Trong ngữ cảnh tiện Fanuc của đề, G92 là chu trình tiện ren đơn giản với bước F2.0."},
  {id:"turn-block-q20",question:"G50 X100 Z150",options:["Chạy dao nhanh đến X100 Z150","Thiết lập/gán giá trị tọa độ hiện tại của dao là X100 Z150 (Coordinate System Setting)","Giới hạn tốc độ trục chính tại X100 Z150","Về điểm tham chiếu máy tại X100 Z150"],correctIndex:1,explanation:"G50 với địa chỉ X/Z gán tọa độ hiện tại cho hệ tọa độ."},
];

export const CNC_COURSE_ITEMS = [
  {
    id: "intro",
    title: "Phần mở đầu",
    shortTitle: "Thông tin chung",
    duration: "Quy định xưởng",
    resources: [
      "Đề cương chi tiết học phần MĐ CNC.",
      "Tiêu chí đánh giá và quy đổi điểm số.",
      "Hướng dẫn an toàn lao động và quy trình 5S.",
    ],
    activities: ["Đăng ký nhóm thực hành."],
  },
  {
    id: "lesson-1",
    title: "Bài 1: Giới thiệu chung về máy tiện phay CNC",
    shortTitle: "Giới thiệu CNC",
    duration: "2 tiết",
    overview: {
      lessonName: "BÀI 1: GIỚI THIỆU CHUNG VỀ MÁY TIỆN PHAY CNC",
      allocation: "2 tiết lý thuyết",
      purpose:
        "Cung cấp cho sinh viên những kiến thức cơ bản nhất về máy tiện và máy phay CNC.",
      outcome:
        "Sinh viên trình bày được các đặc tính kỹ thuật cơ bản của máy tiện và máy phay CNC, đáp ứng chuẩn đầu ra CĐR 1 của học phần.",
    },
    topics: [
      "Quá trình phát triển của máy tiện phay CNC — 0,25 tiết.",
      "Cấu tạo chung của máy tiện phay CNC — 0,5 tiết.",
      "Các bộ phận chính của máy tiện phay CNC — 0,5 tiết.",
      "Đặc tính kỹ thuật của máy CNC — 0,5 tiết; tập trung vào máy tiện CNC EMCO Turn 55, 60 và máy phay CNC EMCO Mill 55.",
      "Lắp đặt, bảo quản, bảo dưỡng máy tiện CNC — 0,25 tiết.",
    ],
    coreKnowledge: [
      {
        title: "Khái niệm về NC và CNC",
        content:
          "Phân biệt máy tự động NC, được điều khiển bằng chương trình ghi trên cơ cấu mang mã số, với máy CNC thế hệ mới tích hợp bộ vi xử lý, có khả năng nội suy phức tạp và lưu trữ chương trình.",
      },
      {
        title: "Đặc điểm của máy CNC",
        content:
          "Tìm hiểu các ưu điểm như tính tự động cao, linh hoạt khi thay đổi sản phẩm, tập trung nguyên công; đồng thời nhận biết các hạn chế như chi phí đầu tư ban đầu lớn và yêu cầu bảo dưỡng khắt khe.",
      },
      {
        title: "Hệ tọa độ",
        content:
          "Giới thiệu hệ tọa độ Đề-các vuông góc X, Y, Z xác định theo quy tắc bàn tay phải và hệ tọa độ cực biểu diễn theo bán kính và trị số góc.",
      },
      {
        title: "Các điểm chuẩn trên máy CNC",
        content:
          "Định nghĩa và xác định vị trí chuẩn máy (M), chuẩn phôi hoặc chi tiết (W), chuẩn tham chiếu (R), chuẩn gá dao (N) và điểm đỉnh mũi dao (P).",
      },
      {
        title: "Quy trình thực hiện gia công",
        content:
          "Thực hiện tuần tự từ nghiên cứu bản vẽ, lập quy trình công nghệ, thiết kế quỹ đạo cắt, lập trình NC đến kiểm tra mô phỏng và cài đặt máy.",
      },
    ],
    lessonContent: [
      {
        title: "1. Quá trình phát triển của máy CNC",
        paragraphs: [
          "Máy công cụ phát triển từ máy vạn năng lên máy NC. Khi máy NC được bổ sung cụm vi tính, bộ xử lý và phương pháp điều khiển theo đường biên, máy NC (Numerical Control) phát triển thành máy CNC (Computer Numerical Control).",
        ],
        bullets: [
          "Máy vạn năng: người vận hành trực tiếp điều khiển các chuyển động gia công.",
          "Máy NC: hoạt động theo chương trình điều khiển số đã được thiết lập.",
          "Máy CNC: sử dụng máy tính và bộ xử lý để điều khiển, lưu trữ và hiệu chỉnh chương trình linh hoạt.",
        ],
      },
      {
        title: "2. Cấu tạo chung của máy CNC",
        paragraphs: [
          "Máy CNC gồm hai phần chính: phần điều khiển và phần chấp hành. Hai phần trao đổi tín hiệu về chuyển động, vận tốc, vị trí và trạng thái lỗi trong suốt quá trình gia công.",
        ],
        bullets: [
          "Phần điều khiển: chương trình điều khiển, bàn phím, màn hình và các cơ cấu điều khiển bằng tay hoặc tự động.",
          "Phần chấp hành: máy cắt kim loại và các cơ cấu tự động hóa như tay máy, ổ chứa dao, hệ thống cấp phôi và hút phoi.",
          "Đầu vào là phôi và chương trình; đầu ra là chi tiết được gia công theo yêu cầu kỹ thuật.",
        ],
      },
      {
        title: "3. Các bộ phận chính của máy tiện và máy phay CNC",
        paragraphs: [
          "Phần chấp hành của máy tiện CNC và máy phay CNC có kết cấu khác nhau để phù hợp với chuyển động tạo hình đặc trưng của từng loại máy.",
        ],
        bullets: [
          "Máy tiện CNC: băng máy, trục chính, mâm dao, động cơ bàn dao ngang, động cơ xoay dao, động cơ bàn dao dọc, bộ truyền trục chính, bàn dao ngang và ụ động.",
          "Máy phay CNC: trục chính, ổ tích dao, cơ cấu thay dao, bảng điều khiển, bàn máy, động cơ dẫn động và đế máy.",
        ],
      },
      {
        title: "4. Đặc tính kỹ thuật của máy CNC",
        paragraphs: [
          "Máy tiện và máy phay CNC có khả năng tự động hóa và tập trung nguyên công cao, phù hợp với sản xuất chính xác và các biên dạng phức tạp.",
        ],
        bullets: [
          "Tự động hóa cao và giảm sự phụ thuộc vào thao tác trực tiếp của người vận hành.",
          "Linh hoạt khi thay đổi sản phẩm thông qua việc thay đổi chương trình.",
          "Tập trung nhiều nguyên công trên một lần gá đặt.",
          "Đảm bảo độ chính xác và chất lượng bề mặt cao.",
          "Gia công được các biên dạng phức tạp.",
          "Mang lại hiệu quả kinh tế và kỹ thuật khi tổ chức sản xuất phù hợp.",
        ],
      },
      {
        title: "5. Hệ trục tọa độ trên máy CNC",
        paragraphs: [
          "Vị trí và chuyển động trên máy CNC được mô tả chủ yếu bằng hệ tọa độ Đề-các X, Y, Z. Chiều dương của các trục được xác định theo quy tắc bàn tay phải và quy ước dụng cụ cắt chuyển động tương đối so với chi tiết.",
          "Máy CNC hiện đại cũng cho phép lập trình theo tọa độ cực, trong đó vị trí được xác định bằng bán kính và góc quay; cách biểu diễn này thuận tiện cho các chi tiết có vị trí phân bố theo vòng tròn.",
        ],
        bullets: [
          "Trục Z trùng với trục chính của máy.",
          "Máy tiện: chiều +Z hướng ra xa mâm cặp; trục X biểu diễn chuyển động theo phương đường kính; máy tiện cơ bản không có trục Y.",
          "Máy phay: các trục X, Y nằm trên mặt bàn máy; trục Z theo phương trục chính.",
          "Ví dụ tọa độ cực: P1 (R100, 30°), P2 (R100, 150°), P3 (R100, 270°).",
        ],
      },
      {
        title: "6. Các điểm chuẩn trên máy CNC",
        paragraphs: [
          "Để điều khiển quỹ đạo chạy dao, cần xác lập quan hệ tọa độ giữa máy, phôi và mũi dao. Máy tiện và máy phay CNC cùng sử dụng các điểm chuẩn M, W, R, N/T và P.",
        ],
        bullets: [
          "M — Machine zero point: điểm gốc tọa độ máy, do nhà sản xuất xác định và không thay đổi.",
          "W — Workpiece zero point: điểm gốc tọa độ chi tiết/phôi, thay đổi theo cách gá và yêu cầu lập trình.",
          "R — Reference point: điểm chuẩn tham chiếu, là vị trí chuẩn cố định để máy xác lập tọa độ.",
          "N/T — Tool reference point: điểm chuẩn dao, nằm tại vị trí chuẩn của ổ hoặc cơ cấu gá dao.",
          "P — Cutter point: điểm đỉnh mũi dao trực tiếp tạo hình bề mặt, thay đổi theo dụng cụ.",
        ],
      },
      {
        title: "7. Lắp đặt, bảo quản và bảo dưỡng máy CNC",
        paragraphs: [
          "Sinh viên phải bảo quản máy, phụ tùng và vật tư trong toàn bộ thời gian thực tập, đồng thời thực hiện đúng quy định vệ sinh và bảo dưỡng của xưởng.",
        ],
        bullets: [
          "Kiểm tra máy và phụ tùng thiết bị ngay khi được phân máy.",
          "Bảo quản vật tư, thiết bị trong suốt quá trình thực tập.",
          "Cuối ca thực hiện vệ sinh và tra dầu nhớt; cuối tuần tổng vệ sinh máy và xưởng.",
        ],
      },
      {
        title: "8. Bài tập củng cố",
        paragraphs: [
          "Hoàn thành các câu hỏi sau để hệ thống hóa kiến thức của Bài 1.",
        ],
        bullets: [
          "So sánh những điểm giống và khác nhau cơ bản giữa máy tiện vạn năng và máy tiện CNC.",
          "Trình bày và phân tích các điểm chuẩn trên máy tiện CNC.",
          "Xác định tọa độ các điểm P1–P7 trên biên dạng chi tiết tiện theo bản vẽ bài tập.",
        ],
      },
    ],
    teachingGuidance:
      "Sinh viên đã được học kiến thức cơ bản ở học phần Máy cắt kim loại và Điều khiển chương trình số. Giảng viên trình bày nhanh, khái quát phần lý thuyết để chuyển trọng tâm sang các nội dung thực hành tiếp theo.",
    assessment: {
      format:
        "Sinh viên thảo luận và viết bài thu hoạch theo nhóm tại nhà, nộp vào ngày hôm sau.",
      prompts: [
        "Trình bày các đặc tính kỹ thuật cơ bản của máy tiện CNC Turn 55 và máy phay CNC Mill 55.",
        "So sánh những điểm giống và khác nhau cơ bản giữa máy tiện, máy phay truyền thống tại xưởng trường với máy tiện CNC Turn 55 và máy phay CNC Mill 55.",
      ],
      grading: "Chấm như một bài tự luận theo thang điểm 10.",
    },
    activities: ["Thảo luận nhóm và hoàn thành bài thu hoạch Bài 1."],
  },
  {
    id: "lesson-2",
    title: "Bài 2: Lập trình tiện CNC với Win-NC32 / FANUC 21T",
    shortTitle: "Lập trình tiện",
    duration: "8 tiết",
    topics: [
      "Cài đặt các thông số cơ bản cho phần mềm điều khiển tiện CNC.",
      "Cấu trúc chương trình tiện CNC.",
      "Lệnh, câu lệnh tiện CNC.",
      "Chế độ cắt khi tiện CNC.",
      "Giới thiệu các lệnh hỗ trợ tiện CNC.",
      "Giới thiệu các lệnh cắt gọt cơ bản tiện CNC.",
      "Giới thiệu một số lệnh, chu trình tiện CNC cơ bản như G70, G71.",
      "Mô phỏng chương trình trên phần mềm WinNC 32.",
      "Xuất, nhập chương trình NC.",
    ],
    lessonContent: [
      {
        title: "1. Các điểm chuẩn trên máy tiện CNC",
        paragraphs: [
          "Việc lập trình và cài đặt máy tiện CNC dựa trên mối quan hệ giữa hệ tọa độ máy, hệ tọa độ phôi và vị trí thực của mũi dao.",
        ],
        bullets: [
          "M — Machine zero point: điểm gốc tọa độ máy, cố định và không thay đổi.",
          "W — Workpiece zero point: điểm gốc tọa độ chi tiết/phôi, thay đổi theo cách gá và yêu cầu lập trình.",
          "R — Reference point: điểm chuẩn tham chiếu của máy, không thay đổi.",
          "T/N — Tool reference point: điểm chuẩn dao, không thay đổi.",
          "P — Cutter point: điểm đỉnh mũi dao trực tiếp tạo hình, thay đổi theo dụng cụ.",
        ],
      },
      {
        title: "2. Cấu trúc chương trình tiện NC — FANUC 21T",
        paragraphs: [
          "Chương trình NC gồm chương trình chính và chương trình con. Các khối lệnh được thực hiện tuần tự; chương trình chính có thể gọi chương trình con để tổ chức các phần gia công lặp lại.",
          "Tên chương trình gồm chữ O và bốn chữ số, ví dụ O1601. Khối lệnh tổng quát có dạng N_G_X_Y_Z_M_S_F_T_; và kết thúc bằng dấu chấm phẩy.",
        ],
        bullets: [
          "N: số thứ tự câu lệnh; G: chức năng chuẩn bị.",
          "X, Y, Z: vị trí tọa độ; trên máy tiện chủ yếu sử dụng X và Z.",
          "M: lệnh phụ; S: tốc độ trục chính; F: lượng chạy dao; T: chọn dụng cụ cắt.",
          "G90 lập trình tọa độ tuyệt đối; G91 lập trình tọa độ tương đối so với điểm trước đó.",
        ],
      },
      {
        title: "3. Mặt phẳng, đơn vị và các lệnh dịch chuyển cơ bản",
        paragraphs: [
          "Hệ tọa độ gia công gồm ba trục X, Y, Z và các mặt phẳng XOY, XOZ, YOZ. Khi tiện, mặt phẳng làm việc chính là XOZ (G18).",
        ],
        bullets: [
          "G17/G18/G19: chọn lần lượt mặt phẳng XOY, XOZ và YOZ.",
          "G70: đơn vị inch; G71: đơn vị hệ mét.",
          "G94: lượng chạy dao mm/phút; G95: lượng chạy dao mm/vòng, thường dùng khi tiện.",
          "G00 X(U)… Z(W)…: chạy dao nhanh không cắt; X, Z là tọa độ tuyệt đối, U, W là tọa độ tương đối.",
          "G01 X(U)… Z(W)… F…: nội suy đường thẳng, dùng để tiện mặt đầu, trụ, côn, rãnh, khoan và doa; có thể dùng R để bo góc hoặc C để vát góc.",
          "G02/G03 X(U)… Z(W)… I… K… F… hoặc dùng R: nội suy cung tròn cùng/ngược chiều kim đồng hồ.",
        ],
      },
      {
        title: "4. Bù trừ bán kính mũi dao",
        paragraphs: [
          "Bù trừ bán kính mũi dao giúp đường tâm dao được hiệu chỉnh để biên dạng thực đạt đúng kích thước yêu cầu khi tiện ngoài, tiện trong và gia công cung tròn.",
        ],
        bullets: [
          "G40: hủy bù trừ bán kính dao.",
          "G41: bù trừ bán kính dao về bên trái quỹ đạo lập trình.",
          "G42: bù trừ bán kính dao về bên phải quỹ đạo lập trình.",
          "Phải chọn đúng G41/G42 theo hướng chạy dao và vị trí mũi dao; hủy bù bằng G40 trước khi rút dao.",
        ],
      },
      {
        title: "5. Các chu trình tiện cơ bản",
        paragraphs: [
          "Chu trình giúp rút gọn chương trình và tổ chức tự động các lượt cắt thô, cắt tinh, cắt rãnh và tiện ren.",
        ],
        bullets: [
          "G73: chu trình tiện thô dọc trục, bóc hết lượng dư theo biên dạng từ khối P đến Q; khai báo chiều sâu cắt U, khoảng rút dao R và lượng dư tinh U/W.",
          "G72 P… Q…: chu trình tiện tinh dọc trục theo biên dạng đã được xác định trong khối P–Q.",
          "G77: chu trình cắt rãnh theo phương X; khai báo điểm cuối X(U), Z(W), chiều sâu cắt P, bước dịch theo Z là Q và lượng dịch ngang R.",
          "G78: chu trình tiện ren ngoài, ren lỗ hoặc ren côn; khai báo số lần cắt tinh, góc ren, chiều sâu lát cắt nhỏ nhất, chiều sâu ren và bước ren F.",
          "Khi dùng G73, khối bắt đầu và kết thúc vùng biên dạng phải được tổ chức đúng, đồng thời bố trí G00 an toàn trước và sau chu trình.",
        ],
      },
      {
        title: "6. Chu trình khoan trên máy tiện",
        paragraphs: [
          "Các lệnh khoan quy định mặt phẳng lùi dao, chiều sâu, lượng ăn dao từng bước và thời gian dừng ở đáy lỗ.",
        ],
        bullets: [
          "G98: sau khi khoan, dao trở về mặt phẳng ban đầu.",
          "G99: sau khi khoan, dao trở về mặt phẳng tham chiếu R.",
          "G83 X(U)… Z(W)… R… Q… P… F… M… K…: chu trình khoan lỗ sâu; Q là chiều sâu mỗi lần cắt, P là thời gian dừng đáy lỗ và K là số lần lặp.",
          "G80: hủy chu trình khoan đang hoạt động.",
        ],
      },
      {
        title: "7. Mã lệnh M dùng trong chương trình tiện",
        paragraphs: [
          "Mã M điều khiển các chức năng phụ của máy, trục chính, dung dịch làm mát, mâm cặp, ụ động và luồng thực hiện chương trình.",
        ],
        bullets: [
          "M00 dừng vô điều kiện; M01 dừng có điều kiện; M30 kết thúc và trở về đầu chương trình.",
          "M03/M04/M05: quay thuận, quay nghịch và dừng trục chính; M06: thay dao.",
          "M08/M09: bật/tắt dung dịch tưới nguội; M71/M72: bật/tắt thổi phoi.",
          "M20/M21: lùi/đẩy nòng ụ động; M25/M26: mở/đóng chấu mâm cặp.",
          "M98 gọi chương trình con; M99 kết thúc chương trình con.",
        ],
      },
      {
        title: "8. Bài tập lập trình tiện",
        paragraphs: [
          "Bài tập 1 và 2 yêu cầu viết chương trình gia công hoàn chỉnh từ bản vẽ biên dạng, lựa chọn dao, chế độ cắt và kiểm tra quỹ đạo trên phần mềm mô phỏng.",
        ],
        bullets: [
          "Bài tập 1: tiện thô bằng dao T0202, n = 800 vòng/phút, F = 0,2 mm/vòng, chiều sâu cắt 1 mm; tiện tinh bằng dao T0404, n = 1000 vòng/phút, F = 0,1 mm/vòng, chiều sâu cắt 0,5 mm.",
          "Chương trình mẫu sử dụng G90, G71, G18, G95; tiện mặt đầu; chu trình G73; biên dạng G01; bù dao G41/G40; chu trình tiện tinh G72 và kết thúc M30.",
          "Bài tập 2: lập trình biên dạng có vát và hai cung chuyển tiếp bằng G02/G03; sử dụng cùng bộ thông số dao thô–dao tinh, lượng dư tinh U0.5/W0.5.",
          "Yêu cầu kiểm tra: đúng gốc W, đúng thứ tự dao, đúng chiều trục chính, không va chạm, mô phỏng đạt trước khi xuất file .NC.",
        ],
      },
    ],
    resources: ["Link tải phần mềm Win-NC32.", "Video lập trình mẫu."],
    activities: [
      "Assignment: Nộp file code tiện biên dạng .NC sau khi mô phỏng thành công.",
    ],
    assignment: {
      title: "Nộp file code tiện biên dạng",
      requirement:
        "Sinh viên tự khắc phục lỗi mô phỏng thành công trước khi nộp file .NC.",
      accept: ".NC",
    },
  },
  {
    id: "lesson-3",
    title: "Bài 3: Lập trình phay CNC với Win-NC32 / FANUC 21M",
    shortTitle: "Lập trình phay",
    duration: "8 tiết",
    topics: [
      "Cài đặt thông số cơ bản cho phần mềm điều khiển phay CNC.",
      "Cấu trúc chương trình phay.",
      "Lệnh, câu lệnh phay.",
      "Chế độ cắt khi phay CNC.",
      "Lệnh hỗ trợ phay CNC.",
      "Lệnh cắt gọt cơ bản.",
      "Chu trình phay cơ bản.",
      "Mô phỏng chương trình.",
      "Xuất nhập chương trình NC.",
    ],
    lessonContent: [
      {
        title: "1. Các điểm chuẩn trên máy phay CNC",
        paragraphs: [
          "Lập trình phay CNC yêu cầu xác định rõ hệ tọa độ máy, hệ tọa độ phôi và điểm chuẩn của từng dụng cụ trước khi tạo quỹ đạo cắt.",
        ],
        bullets: [
          "M — Machine zero point: gốc tọa độ máy, cố định.",
          "W — Workpiece zero point: gốc tọa độ phôi, thay đổi theo cách gá và chương trình.",
          "R — Reference point: điểm tham chiếu cố định của máy.",
          "T/N — Tool reference point: điểm chuẩn dao, không thay đổi.",
          "P — Cutter point: điểm đỉnh mũi dao thực hiện cắt gọt, thay đổi theo dụng cụ.",
        ],
      },
      {
        title: "2. Cấu trúc chương trình phay NC — FANUC 21M",
        paragraphs: [
          "Chương trình phay gồm chương trình chính và chương trình con, được thực hiện theo thứ tự các khối lệnh. Tên chương trình có dạng Oxxxx, ví dụ O1601.",
          "Khối lệnh tổng quát có dạng N_G_X_Y_Z_M_S_F_T_; và kết thúc bằng dấu chấm phẩy.",
        ],
        bullets: [
          "N: số thứ tự; G: chức năng chuẩn bị; X/Y/Z: tọa độ vị trí.",
          "M: chức năng phụ; S: tốc độ trục chính; F: tốc độ chạy dao; T: chọn dụng cụ.",
          "G90: lập trình tọa độ tuyệt đối so với chuẩn phôi; G91: lập trình lượng dịch chuyển tương đối so với điểm trước.",
          "Khi chuẩn W đặt tại tâm, phải xác định đúng dấu của X, Y và chiều sâu Z cho từng điểm biên dạng.",
        ],
      },
      {
        title: "3. Mặt phẳng, đơn vị và lệnh dịch chuyển",
        paragraphs: [
          "Máy phay sử dụng đầy đủ ba trục X, Y, Z. Việc chọn đúng mặt phẳng nội suy quyết định ý nghĩa của tọa độ cung tròn và hướng chuyển động.",
        ],
        bullets: [
          "G17/G18/G19: chọn mặt phẳng XOY, XOZ và YOZ; phay biên dạng thông dụng thường dùng G17.",
          "G70: đơn vị inch; G71: đơn vị hệ mét.",
          "G94: lượng chạy dao mm/phút, thường dùng khi phay; G95: lượng chạy dao mm/vòng.",
          "G00 X… Y… Z…: chạy dao nhanh không cắt.",
          "G01 X… Y… Z… F…: nội suy đường thẳng; có thể dùng R để bo góc hoặc C để vát góc.",
          "G02/G03 X… Y… Z… I… J… K… F… hoặc dùng R: nội suy cung tròn cùng/ngược chiều kim đồng hồ.",
        ],
      },
      {
        title: "4. Bù bán kính và bù chiều dài dao",
        paragraphs: [
          "Bù dao cho phép chương trình mô tả biên dạng chi tiết trong khi bộ điều khiển tự hiệu chỉnh theo kích thước và chiều dài thực của dụng cụ.",
        ],
        bullets: [
          "G40: hủy bù bán kính; G41/G42: bù bán kính dao trái/phải theo hướng chạy dao.",
          "G41, G42 đi kèm địa chỉ H để chọn ô dữ liệu bù bán kính, ví dụ G41 H2.",
          "G43: bù chiều dài dao theo hướng dương; G44: bù theo hướng âm; G49: hủy bù chiều dài.",
          "G43/G44 đi kèm H để chọn ô dữ liệu chiều dài dao, ví dụ G43 H12.",
          "Phải gọi bù tại vị trí tiếp cận an toàn và hủy bù trước khi kết thúc/rút dao khỏi biên dạng.",
        ],
      },
      {
        title: "5. Chu trình khoan G81, G83 và G73",
        paragraphs: [
          "Các chu trình khoan cố định giúp lập trình nhiều lỗ bằng cách khai báo một lần các thông số chiều sâu, mặt phẳng an toàn và lượng tiến dao.",
        ],
        bullets: [
          "G98: trở về mặt phẳng ban đầu; G99: trở về mặt phẳng tham chiếu R sau mỗi lỗ.",
          "G81 X… Y… Z… R… F…: khoan hết chiều sâu trong một lần tiến dao.",
          "G83 X… Y… Z… R… P… Q… F… K…: khoan lỗ sâu; Q là chiều sâu mỗi lát cắt, P là thời gian dừng đáy lỗ, K là số lần lặp.",
          "G73 X… Y… Z… R… P… Q… F…: chu trình khoan cao tốc, rút dao ngắn để bẻ và thoát phoi.",
          "X/Y xác định tâm lỗ; Z xác định chiều sâu; R là khoảng an toàn tính từ mặt phôi.",
        ],
      },
      {
        title: "6. Chu trình tarô và doa",
        paragraphs: [
          "Chu trình tarô và doa sử dụng cùng cấu trúc vị trí lỗ, chiều sâu và mặt phẳng an toàn nhưng khác phương thức chuyển động của trục chính và dụng cụ.",
        ],
        bullets: [
          "G84: tarô ren phải; G74: tarô ren trái; cấu trúc gồm X, Y, Z, R, P, F và K.",
          "Khi tarô, tốc độ tiến dao phải đồng bộ với tốc độ trục chính và bước ren.",
          "G89 X… Y… Z… R… P… F… K…: chu trình doa, có dừng P tại đáy lỗ trước khi rút dao.",
          "Kết thúc nhóm chu trình cố định phải hủy chu trình trước khi chuyển sang chuyển động khác.",
        ],
      },
      {
        title: "7. Mã lệnh M dùng trong chương trình phay",
        paragraphs: [
          "Mã M điều khiển trục chính, thay dao, làm mát, cơ cấu kẹp phôi, đầu phân độ và kết thúc chương trình.",
        ],
        bullets: [
          "M00 dừng vô điều kiện; M01 dừng có điều kiện; M30 kết thúc chương trình.",
          "M03/M04/M05: quay thuận, quay nghịch và dừng trục chính; M06: thay dao.",
          "M08/M09: bật/tắt dung dịch tưới nguội; M71/M72: bật/tắt thổi phoi.",
          "M10/M11: khóa/mở khóa đầu phân độ; M19: xác định vị trí dừng trục chính.",
          "M25/M26: mở ê-tô và siết ê-tô kẹp phôi.",
        ],
      },
      {
        title: "8. Bài tập lập trình phay",
        paragraphs: [
          "Bài tập yêu cầu phay biên dạng ngoài sâu 2 mm và khoan bốn lỗ sâu 6 mm theo bản vẽ, sử dụng hai dụng cụ và kiểm tra toàn bộ chương trình bằng mô phỏng.",
        ],
        bullets: [
          "Chương trình O0005 chọn G17, G90; gọi dao T02, bù chiều dài G43 H02, trục chính S1000 M03 và tiếp cận từ vị trí an toàn.",
          "Phay biên dạng dùng G01 kết hợp G02, bù bán kính G41 H12 và hủy bù bằng G40 sau khi hoàn thành đường bao.",
          "Khoan bốn lỗ dùng dao T04, bù chiều dài G43 H04 và chu trình G99 G73 với Z-6, R5, P1000, Q3, F100.",
          "Các tâm lỗ lần lượt tại X12 Y25, X25 Y38, X38 Y25 và X25 Y12; chương trình kết thúc bằng M30.",
          "Yêu cầu nộp file .NC và ảnh chụp mô phỏng 3D sau khi kiểm tra không còn va chạm hoặc lỗi quỹ đạo.",
        ],
      },
    ],
    activities: [
      "Assignment: Nộp bài tập lập trình phay biên dạng gồm file .NC và ảnh chụp mô phỏng 3D.",
    ],
    assignment: {
      title: "Nộp bài lập trình phay biên dạng",
      requirement: "Nộp file .NC kèm ảnh chụp mô phỏng 3D.",
      accept: ".NC, ảnh mô phỏng 3D",
    },
  },
  {
    id: "lesson-4-turn",
    title: "Bài 4: Vận hành và cài đặt máy tiện CNC EMCO TURN 55",
    shortTitle: "Vận hành máy tiện",
    duration: "9 tiết",
    emphasis: "Trọng tâm cài đặt dao tiện, mâm cặp và gốc phôi",
    topics: [
      "Kiểm tra máy trước khi hoạt động.",
      "Mở máy.",
      "Thao tác di chuyển máy về chuẩn máy.",
      "Thao tác cho trục chính quay.",
      "Di chuyển trục X, Z ở chế độ JOG, HANDLE.",
      "Gá dao tiện và gá phôi trên mâm cặp.",
      "Cài đặt Geometry Offset dao tiện theo X, Z.",
      "Cài đặt gốc phôi Work Shift.",
      "Nhập chương trình tiện CNC.",
      "Mô phỏng, chạy thử Test không tải / Single Block.",
      "Tắt máy đúng quy trình.",
      "Vệ sinh công nghiệp và 5S.",
    ],
    lessonContent: [
      {
        title: "1. Cấu tạo máy tiện CNC EMCO TURN 55",
        paragraphs: [
          "Máy tiện CNC gồm hai phần chính: phần điều khiển tiếp nhận chương trình và lệnh của người vận hành; phần chấp hành thực hiện các chuyển động cắt gọt để tạo thành chi tiết.",
        ],
        bullets: [
          "Phần điều khiển: tủ điều khiển, màn hình, bàn phím máy CNC, bàn phím máy tính và thùng CPU.",
          "Phần chấp hành: băng máy, trục chính, mâm dao, động cơ bàn dao ngang, động cơ xoay dao, động cơ bàn dao dọc, cơ cấu phân độ trục chính, động cơ trục chính, bàn dao ngang và ụ động.",
          "Dụng cụ, phụ kiện và thiết bị đo phải được đặt đúng vị trí trong tủ dụng cụ sau khi sử dụng.",
        ],
      },
      {
        title: "2. Kiểm tra máy trước khi cấp điện",
        paragraphs: [
          "Trước khi đóng điện, người vận hành phải quan sát toàn bộ máy và khu vực làm việc để phát hiện vật cản, hư hỏng hoặc trạng thái không an toàn.",
        ],
        bullets: [
          "Kiểm tra tủ điện, thân máy tiện CNC và khu vực băng máy.",
          "Kiểm tra mâm cặp, chấu cặp, ổ gá dao/mâm dao và ụ động.",
          "Kiểm tra nút dừng khẩn cấp, cửa che chắn và vùng hành trình dao.",
          "Kiểm tra màn hình, bàn phím CNC, bàn phím máy tính và thùng CPU.",
          "Bảo đảm không còn chìa khóa mâm cặp, dụng cụ hoặc vật lạ trong vùng quay.",
        ],
      },
      {
        title: "3. Mở máy, về chuẩn tham chiếu và di chuyển JOG",
        paragraphs: [
          "Máy chỉ được thao tác sau khi mở đúng trình tự và hoàn thành việc đưa các trục về chuẩn tham chiếu Reference.",
        ],
        bullets: [
          "Đóng CP của máy tiện CNC; nhấn Power của máy tính; mở phần mềm WinNC FANUC 21T.",
          "Chọn chế độ Reference, đặt phần trăm bước tiến phù hợp và nhấn phím Reference để đưa máy về chuẩn.",
          "Chuyển sang JOG; điều chỉnh phần trăm bước tiến; dùng +X, -X, +Z, -Z để di chuyển dao theo hai trục.",
          "Luôn quan sát khoảng cách giữa dao, phôi, mâm cặp và ụ động khi di chuyển bằng tay.",
        ],
      },
      {
        title: "4. Trục chính, mâm dao và thao tác MDI",
        paragraphs: [
          "Chế độ MDI được dùng để gọi dao, thay dao và ra lệnh quay trục chính trước khi thực hiện các thao tác cài đặt hoặc gia công bằng tay.",
        ],
        bullets: [
          "M03: trục chính quay cùng chiều kim đồng hồ; M04: quay ngược chiều kim đồng hồ; kiểm tra chiều quay trước khi tiếp cận phôi.",
          "Dùng phím quay dao để kiểm tra vị trí và số lượng dao trên mâm dao.",
          "Chọn MDI, mở Program MDI, nhập T0202 M6; và M3 S500; rồi chạy từng câu lệnh.",
          "Sau khi gọi đúng dao và xác nhận trục chính quay đúng chiều, chuyển sang JOG để thao tác X, Z bằng tay.",
        ],
      },
      {
        title: "5. Gá phôi và gá dao tiện",
        paragraphs: [
          "Phôi và dao phải được gá chắc chắn, đúng tâm và không gây cản trở hành trình máy trước khi cho trục chính quay.",
        ],
        bullets: [
          "Dùng chấu thuận để kẹp phôi nhỏ; dùng chấu ngược để kẹp phôi lớn; lựa chọn chiều dài nhô ra phù hợp.",
          "Mâm dao có thể gá tám dao, gồm dao tiện ngoài, dao cắt rãnh, dao tiện ren ngoài, dao tiện lỗ, dao ren lỗ và mũi khoan.",
          "Gá đúng chiều dao, siết chặt bằng lục giác và dùng căn chêm để canh tâm mũi dao.",
          "Quay thử mâm cặp ở tốc độ thấp và kiểm tra khoảng hở trước khi gia công.",
        ],
      },
      {
        title: "6. Bài tập vận hành tiện bằng tay",
        paragraphs: [
          "Sinh viên vận hành máy ở chế độ JOG/MDI, căn cứ tọa độ hiển thị để tiện chi tiết và đo kiểm sau gia công.",
        ],
        bullets: [
          "Vạt mặt đầu để đạt chiều dài 60 ± 0,1 mm.",
          "Tiện trụ đạt đường kính Ø18 ± 0,1 mm trên chiều dài 20 ± 0,1 mm.",
          "Theo dõi tọa độ X, Z trong suốt quá trình, sử dụng bước tiến nhỏ khi dao gần phôi.",
          "Đo kiểm chiều dài và đường kính bằng dụng cụ đo phù hợp; ghi nhận sai lệch và hiệu chỉnh thao tác.",
        ],
      },
      {
        title: "7. Điểm chuẩn và xóa dữ liệu cài đặt cũ",
        paragraphs: [
          "Trước khi cài đặt cho phôi và bộ dao mới, phải xác định đúng các điểm M, W, R, N/T, P và xóa các giá trị cũ để tránh dùng nhầm dữ liệu của lần gá trước.",
        ],
        bullets: [
          "M: gốc máy; W: gốc phôi; R: điểm tham chiếu; N/T: chuẩn dao; P: đỉnh mũi dao.",
          "Vào Offset Setting → Work Shift để xóa dữ liệu X, Z của phôi.",
          "Vào Offset Setting → Offset Geometry để xóa dữ liệu X, Z, R, T của dao.",
          "Chỉ xóa và nhập dữ liệu khi đã xác nhận đúng trang, đúng hàng dao và đúng đơn vị.",
        ],
      },
      {
        title: "8. Cài đặt gốc phôi W trên máy tiện",
        paragraphs: [
          "Cài đặt phôi là dịch hệ tọa độ từ gốc máy M sang gốc chi tiết W. Tài liệu hướng dẫn hai phương pháp xác lập giá trị Z của Work Shift.",
        ],
        bullets: [
          "Cách 1 — đo trực tiếp: xác định kích thước mâm cặp MA và khoảng cách từ mâm cặp đến mặt đầu phôi AW; nhập Zphôi = MW = MA + AW với đúng dấu tọa độ.",
          "Cách 2 — chạm dao: vào MDI cho phôi quay, chuyển JOG, đưa dao chạm nhẹ mặt đầu phôi theo Z.",
          "Nhấn POS để đọc Zmachine, đổi dấu theo quy ước rồi nhập vào giá trị Z của Shift Value.",
          "Sau khi nhập, rút dao về vị trí an toàn và kiểm tra lại gốc W trên màn hình Position.",
        ],
      },
      {
        title: "9. Cài đặt Geometry Offset dao theo Z và X",
        paragraphs: [
          "Mỗi dao phải được đo riêng để dịch từ điểm chuẩn dao N đến đỉnh mũi dao P. Ví dụ dùng dao số 2 và lưu dữ liệu tại hàng Geometry số 2.",
        ],
        bullets: [
          "Gọi dao trong MDI bằng T0202 M6; cho trục chính quay M3 hoặc M4 S500; sau đó chuyển JOG.",
          "Theo Z: cho dao chạm mặt đầu phôi, tại hàng 2 nhập Z0 và nhấn Measure; quan hệ Zdao2 = Zmachine2 − Zphôi.",
          "Theo X: cho dao chạm nhẹ đường kính đã biết của phôi, tại hàng 2 nhập giá trị X và nhấn Measure; quan hệ Xdao2 = Xmachine2 − Xphôi.",
          "Nhập đúng bán kính và hướng mũi dao nếu chương trình sử dụng bù bán kính mũi dao.",
        ],
      },
      {
        title: "10. Kiểm tra cài đặt trước khi chạy máy tiện",
        paragraphs: [
          "Sau khi cài đặt, phải kiểm tra ở chế độ MDI và chạy từng khối với bước tiến thấp; không chuyển sang gia công tự động nếu vị trí thực không trùng với tọa độ dự kiến.",
        ],
        bullets: [
          "Gọi đúng dao: T0202 M6; và quay trục chính M3 S500;.",
          "Tiếp cận thử: G0 X20 Z5; sau đó G1 X20 Z0 F0.2;.",
          "Quan sát khoảng cách dao–phôi–mâm cặp, tọa độ Position và chiều chuyển động của từng trục.",
          "Nếu có sai lệch hoặc nguy cơ va chạm, dừng ngay, rút dao và kiểm tra lại Work Shift/Geometry Offset.",
        ],
      },
    ],
    resources: ["Video giáo viên thị phạm quy trình mở máy tiện và cài đặt dao, phôi."],
    activities: [
      "Interactive Checklist: 10 bước cài đặt dao phôi để sinh viên tự kiểm tra chéo.",
      "Kiểm tra an toàn máy tiện: 10 câu về trình tự và xử lý lỗi test dao phương X, Z.",
    ],
    flipped: true,
  },
  {
    id: "lesson-4-mill",
    title: "Bài 5: Vận hành và cài đặt máy phay CNC EMCO MILL 55",
    shortTitle: "Vận hành máy phay",
    duration: "9 tiết",
    emphasis: "Trọng tâm cài đặt dao phay, ê-tô và gốc phôi G54",
    topics: [
      "Kiểm tra máy phay CNC trước khi hoạt động.",
      "Mở máy và đưa các trục về điểm chuẩn máy.",
      "Thao tác trục chính và thay dao an toàn.",
      "Di chuyển các trục X, Y, Z ở chế độ JOG, HANDLE.",
      "Gá ê-tô, gá phôi và kiểm tra vùng làm việc.",
      "Cài đặt chiều dài và bán kính dao phay.",
      "Cài đặt gốc phôi G54 theo X, Y, Z.",
      "Nhập chương trình phay CNC.",
      "Mô phỏng, chạy thử không tải và Single Block.",
      "Tắt máy, vệ sinh công nghiệp và thực hiện 5S.",
    ],
    lessonContent: [
      {
        title: "1. Cấu tạo máy phay CNC EMCO MILL 55",
        paragraphs: [
          "Máy phay CNC gồm phần điều khiển và phần chấp hành. Phần điều khiển xử lý chương trình; phần chấp hành tạo chuyển động tương đối giữa dao và phôi.",
        ],
        bullets: [
          "Phần điều khiển: tủ điều khiển, màn hình, bàn phím CNC, bàn phím máy tính và thùng CPU.",
          "Phần chấp hành: trục chính, ổ tích dao, cơ cấu thay dao, bảng điều khiển, bàn máy, động cơ dẫn động và đế máy.",
          "Dụng cụ, collet, thiết bị đo và phụ kiện phải được vệ sinh, kiểm đếm và đặt đúng vị trí trong tủ.",
        ],
      },
      {
        title: "2. Kiểm tra máy phay trước khi cấp điện",
        paragraphs: [
          "Trước khi mở máy, người vận hành phải quan sát khu vực làm việc và xác nhận các bộ phận ở trạng thái an toàn.",
        ],
        bullets: [
          "Kiểm tra nút dừng khẩn cấp, cửa bảo vệ và không gian hành trình các trục.",
          "Kiểm tra trục chính, ổ gá dao/ổ tích dao và cơ cấu thay dao.",
          "Kiểm tra ê-tô, bàn máy, phôi, đồ gá và vật cản trong vùng gia công.",
          "Kiểm tra màn hình, bàn phím CNC, bàn phím máy tính, chuột và thùng CPU.",
          "Bảo đảm dao được kẹp chắc, đúng chiều dài và không có người/vật trong vùng chuyển động.",
        ],
      },
      {
        title: "3. Mở máy, về Reference và di chuyển JOG",
        paragraphs: [
          "Máy phải được mở đúng trình tự và đưa về điểm tham chiếu trước khi gọi dao, cài đặt phôi hoặc chạy chương trình.",
        ],
        bullets: [
          "Đóng CP của máy; nhấn Power máy tính; mở phần mềm WinNC FANUC 21M.",
          "Chọn Reference, đặt phần trăm bước tiến phù hợp và nhấn phím Reference.",
          "Chuyển sang JOG; dùng +X, -X, +Y, -Y, +Z, -Z để di chuyển dao theo ba trục.",
          "Khi dao gần phôi, ê-tô hoặc đồng hồ đo, giảm bước tiến và thao tác từng bước có kiểm soát.",
        ],
      },
      {
        title: "4. Trục chính, thay dao và thao tác MDI",
        paragraphs: [
          "Chế độ MDI cho phép gọi dao, thay dao và chạy trục chính bằng từng câu lệnh để chuẩn bị cài đặt hoặc gia công bằng tay.",
        ],
        bullets: [
          "M03/M04 điều khiển trục chính quay thuận/nghịch; xác nhận đúng chiều quay của dụng cụ.",
          "Dùng nút tháo dao theo đúng quy trình, giữ chắc chuôi dao và tránh đứng dưới dụng cụ.",
          "Chọn MDI, mở Program MDI, nhập T02 M6; và M3 S500; rồi chạy câu lệnh.",
          "Sau khi gọi đúng dao, có thể chuyển sang JOG để di chuyển X, Y, Z bằng tay.",
        ],
      },
      {
        title: "5. Gá phôi và gá dao phay",
        paragraphs: [
          "Gá đặt phải bảo đảm định vị đúng, kẹp chặt và tạo khoảng hở an toàn cho dao, trục chính và ê-tô trong toàn bộ hành trình.",
        ],
        bullets: [
          "Vệ sinh ê-tô và phôi; định vị phôi đủ sáu bậc tự do; siết ê-tô chắc chắn.",
          "Ổ dao có tám vị trí, có thể gá dao phay mặt đầu, dao phay ngón, mũi khoan và mũi tarô.",
          "Chọn đúng collet/chấu kẹp, kiểm tra chiều dài nhô dao và siết đúng lực.",
          "Kiểm tra đường kính, chiều dài dao và nguy cơ va chạm khi thay dao tự động.",
        ],
      },
      {
        title: "6. Bài tập vận hành phay bằng tay",
        paragraphs: [
          "Sinh viên vận hành máy để phay mặt phẳng theo tọa độ, sau đó đo kiểm kích thước và chất lượng bề mặt.",
        ],
        bullets: [
          "Phay mặt đầu đạt kích thước 60 ± 0,1 mm.",
          "Bề mặt sau phay đạt yêu cầu nhám Rz20.",
          "Theo dõi tọa độ X, Y, Z và điều chỉnh bước tiến phù hợp khi dao vào/ra phôi.",
          "Đo kiểm sản phẩm, đối chiếu bản vẽ và ghi nhận nguyên nhân sai lệch nếu chưa đạt.",
        ],
      },
      {
        title: "7. Điểm chuẩn và xóa dữ liệu cài đặt cũ",
        paragraphs: [
          "Trước khi thiết lập bộ dao và phôi mới, phải xác định các điểm M, W, R, N, P và xóa giá trị cũ để tránh sai lệch hệ tọa độ.",
        ],
        bullets: [
          "M: gốc máy; W: gốc phôi; R: điểm tham chiếu; N: chuẩn dao; P: đỉnh mũi dao.",
          "Vào Offset Setting → Work Shift/Work Coordinates để xóa thông số X, Y, Z của phôi.",
          "Vào Offset Setting → Offset để xóa thông số chiều dài và bán kính dao.",
          "Xác nhận đúng hàng dao và hệ tọa độ phôi trước khi nhập số liệu mới.",
        ],
      },
      {
        title: "8. Cài đặt chiều dài và bán kính dao số 2",
        paragraphs: [
          "Tài liệu sử dụng đồng hồ chuẩn cao 50 mm để đo chiều dài dao. Gốc Z tạm thời được thiết lập theo chiều cao đồng hồ trước khi chạm dao.",
        ],
        bullets: [
          "Nhập Zphôi = ZMA + ZAW1 = 50 + 0 = 50 vào Work Shift.",
          "Trong MDI gọi T2 M6; nhấn POS để theo dõi tọa độ Machine; chuyển JOG và đưa dao vào tâm đồng hồ.",
          "Giảm bước tiến, cho dao chạm nhẹ mặt trên đồng hồ; tính Zdao2 = Zmachine2 − Zphôi.",
          "Nhập bù chiều dài dao số 2 tại hàng 2 và nhập bù bán kính Rdao2 tại hàng 12.",
          "Rút dao và đưa máy về Reference sau khi hoàn tất.",
        ],
      },
      {
        title: "9. Cài đặt chiều dài và bán kính dao số 4",
        paragraphs: [
          "Dao số 4 được đo độc lập theo cùng phương pháp để bảo đảm mỗi dụng cụ có giá trị chiều dài và bán kính riêng.",
        ],
        bullets: [
          "Trong MDI gọi T4 M6; theo dõi tọa độ Machine trên màn hình POS.",
          "Chuyển JOG, đưa dao vào tâm đồng hồ, giảm bước tiến và chạm nhẹ mặt đồng hồ.",
          "Tính Zdao4 = Zmachine4 − Zphôi.",
          "Nhập chiều dài dao tại hàng 4 và bán kính Rdao4 tại hàng 14; sau đó rút dao và về Reference.",
        ],
      },
      {
        title: "10. Cài đặt gốc phôi theo Z, X và Y",
        paragraphs: [
          "Gốc phôi W được xác lập lần lượt theo ba phương. Khi dò cạnh X/Y bằng dao, phải cộng bán kính dao để chuyển từ tâm dao về bề mặt chuẩn của phôi.",
        ],
        bullets: [
          "Theo Z: nhập Zphôi = ZMA + ZAW1; ví dụ máy MILL 55 có ZMA = 28 mm và chiều cao phôi ZAW1 = 50 mm.",
          "Theo X: gọi T02 M6; M3 S800; chuyển JOG, chạm cạnh trái phôi và tính Xphôi = Xmachine + Rdao.",
          "Theo Y: chạm cạnh trước phôi, giảm bước tiến và tính Yphôi = Ymachine + Rdao.",
          "Nhập Xphôi, Yphôi, Zphôi vào Work Shift/Work Coordinates và đưa máy về Reference.",
        ],
      },
      {
        title: "11. Kiểm tra cài đặt trước khi chạy máy phay",
        paragraphs: [
          "Sau khi cài đặt, phải kiểm tra từng dao tại gốc phôi trong MDI với bù chiều dài tương ứng và tốc độ tiến dao thấp.",
        ],
        bullets: [
          "Dao số 2: T02 M6; M3 S500; G43 H2; G0 X0 Y0 Z50; G1 Z0 F200;.",
          "Dao số 4: T04 M6; M3 S500; G43 H4; G0 X0 Y0 Z50; G1 Z0 F200;.",
          "Theo dõi Position, kiểm tra đúng dao, đúng H, đúng chiều trục chính và đúng gốc X0 Y0 Z0.",
          "Nếu dao không đến đúng vị trí hoặc có nguy cơ va chạm, dừng máy và kiểm tra lại Work Shift, chiều dài và bán kính dao.",
        ],
      },
    ],
    resources: ["Video giáo viên thị phạm quy trình mở máy phay và cài đặt dao, phôi."],
    activities: [
      "Interactive Checklist: quy trình cài đặt dao phay, ê-tô và gốc phôi G54.",
      "Kiểm tra an toàn máy phay: 10 câu trước khi được phép vận hành.",
    ],
    flipped: true,
  },
  {
    id: "lesson-5",
    title: "Bài 6: Gia công tiện CNC",
    shortTitle: "Gia công tiện",
    duration: "17 tiết",
    topics: [
      "Tiện mặt đầu.",
      "Tiện trụ ngắn, bậc, bo cung vạt cạnh.",
      "Tiện côn, ren.",
      "Bài tập tổng hợp.",
    ],
    resources: ["Tài liệu: Bản vẽ phôi."],
    activities: ["Diễn đàn thảo luận khắc phục lỗi sai hỏng bề mặt/kích thước."],
  },
  {
    id: "lesson-6",
    title: "Bài 7: Gia công phay CNC",
    shortTitle: "Gia công phay",
    duration: "17 tiết",
    topics: [
      "Phay mặt phẳng.",
      "Phay bậc, cong, cung.",
      "Phay theo biên dạng profile.",
      "Khoan lỗ, Tarô.",
      "Bài tập tổng hợp.",
    ],
    activities: ["Rubric trực quan: Bảng tiêu chí chấm điểm bài thực hành phay tổng hợp."],
  },
];

export type CncCourseItem = (typeof CNC_COURSE_ITEMS)[number];
export type CncGateQuizQuestion = (typeof CNC_GATE_QUIZ)[number];
