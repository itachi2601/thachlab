export const CNC_PROGRESS = {
  turningQuizScore: 85,
  millingQuizScore: 82,
  operationPassedByInstructor: false,
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
    topics: [
      "Quá trình phát triển của máy tiện phay CNC.",
      "Cấu tạo chung của máy tiện phay CNC.",
      "Các bộ phận chính của máy tiện phay CNC.",
      "Đặc tính kỹ thuật của máy CNC Turn 55, 60 và Mill 55.",
      "Lắp đặt, bảo quản, bảo dưỡng máy tiện CNC.",
    ],
    activities: ["Bài tập nhóm: So sánh máy truyền thống và máy CNC."],
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
    id: "lesson-4",
    title: "Bài 4: Vận hành máy tiện phay CNC",
    shortTitle: "Vận hành & cài đặt",
    duration: "18 tiết",
    emphasis: "Trọng tâm cài đặt dao, phôi",
    topics: [
      "Kiểm tra máy trước khi hoạt động.",
      "Mở máy.",
      "Thao tác di chuyển máy về chuẩn máy.",
      "Thao tác cho trục chính quay.",
      "Di chuyển các trục X, Y, Z, Q ở chế độ JOG, HANDLE.",
      "Gá dao, gá phôi.",
      "Cài đặt dao, phôi.",
      "Cài đặt thông số phôi Work shift.",
      "Nhập chương trình gia công.",
      "Mô phỏng, chạy thử Test không tải / Single Block.",
      "Tắt máy đúng quy trình.",
      "Vệ sinh công nghiệp và 5S.",
    ],
    resources: ["Video clip giáo viên thị phạm quy trình mở máy và cài đặt dao phôi."],
    activities: [
      "Interactive Checklist: 10 bước cài đặt dao phôi để sinh viên tự kiểm tra chéo.",
      "Quiz 10-Minute Setup: 10 câu về trình tự và xử lý lỗi test dao phương X, Z.",
    ],
    flipped: true,
  },
  {
    id: "lesson-5",
    title: "Bài 5: Gia công tiện CNC",
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
    title: "Bài 6: Gia công phay CNC",
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
