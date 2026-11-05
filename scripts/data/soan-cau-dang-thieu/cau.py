# Câu soạn mới cho các dạng LÝ THUYẾT/HIỆN TƯỢNG có dưới 3 câu chắc (docs/dang-thieu-cau.md, 05/11/2026).
# Soạn trực tiếp trong phiên (không gọi API ngoài). Chạy: python3 cau.py  → cau.json (đọc bởi kiem.mts, lap-trang-duyet.py, tao-sql.py)
import json, os

P = '<p class="text-base leading-relaxed my-2">'
def ps(lines): return "".join(P + l + "</p>" for l in lines)

DANG = {
 "2-1": (2, "Dạng 1 · Dễ · Gọi tên quá trình chuyển thể trong hiện tượng đời sống", 196, "Nóng chảy, đông đặc, hoá hơi, ngưng tụ"),
 "2-2": (2, "Dạng 2 · Dễ · Thể tích và hình dạng của chất rắn, lỏng, khí trong bình", 195, "Cấu trúc chất rắn, lỏng, khí theo mô hình động học phân tử"),
 "3-1": (3, "Dạng 1 · Dễ · Chiều truyền nhiệt năng và cân bằng nhiệt", 198, "Nhiệt độ và cân bằng nhiệt"),
 "6-1": (6, "Dạng 1 · Dễ · Đối chiếu phát biểu với thuyết động học phân tử (Brown, áp suất, nhiệt độ)", 204, "Nội dung thuyết động học phân tử"),
 "10-1": (10, "Dạng 1 · Dễ · Chiều từ trường và độ mạnh quanh thanh nam châm", 213, "Đường sức từ và từ phổ"),
 "10-2": (10, "Dạng 2 · Dễ · Chiều từ trường quanh dây thẳng (nắm tay phải)", 214, "Từ trường của nam châm và của dòng điện"),
 "127-1": (127, "Dạng 1 · Dễ · Điện trường xoáy: nguồn gây ra và dạng đường sức", 237, "Điện từ trường và sóng điện từ"),
 "15-2": (15, "Dạng 2 · Trung bình · Nhận ra đồng vị: cùng số prôtôn, khác số nơtron", 221, "Kí hiệu hạt nhân, số nuclôn, đồng vị"),
 "17-1": (17, "Dạng 1 · Dễ · Phân hạch, nhiệt hạch và hệ số nhân nơtron k", 71, "Phản ứng phân hạch, phản ứng nhiệt hạch"),
 "25-1": (25, "Dạng 1 · Dễ · Phân biệt dao động tắt dần, duy trì, cưỡng bức", 162, "Dao động tắt dần và nguyên nhân"),
 "28-1": (28, "Dạng 1 · Dễ · Phân biệt sóng ngang và sóng dọc", 166, "Phân biệt sóng ngang và sóng dọc"),
 "30-3": (30, "Dạng 3 · Trung bình · Chọn nhận định đúng về sóng điện từ", 168, "Đặc điểm và thang sóng điện từ"),
 "41-1": (41, "Dạng 1 · Dễ · Khái niệm: cách mắc ampe kế, chiều electron, dòng một chiều và dòng không đổi", 187, "Định nghĩa cường độ dòng điện và mật độ dòng"),
 "42-2": (42, "Dạng 2 · Dễ · Nhận biết đường đặc trưng của điện trở thuần và của điện trở nhiệt", 189, "Đường đặc trưng vôn – ampe"),
 "46-1": (46, "Dạng 1 · Dễ · Phân loại vi mô – vĩ mô và lĩnh vực ứng dụng của Vật lí", 103, "Đối tượng và phương pháp nghiên cứu Vật lí"),
 "46-3": (46, "Dạng 3 · Khó · Quy trình 5 bước: nhận ra giả thuyết, đọc số liệu và kết luận", 103, "Đối tượng và phương pháp nghiên cứu Vật lí"),
 "47-1": (47, "Dạng 1 · Dễ · Đọc nhãn thiết bị: DC, AC, Input, Output, cực + và −", 104, "Quy tắc an toàn trong phòng thực hành"),
 "47-2": (47, "Dạng 2 · Trung bình · Đọc kí hiệu cảnh báo qua hình dạng và màu, rồi biết phải làm gì", 104, "Quy tắc an toàn trong phòng thực hành"),
 "68-1": (68, "Dạng 1 · Dễ · Chuyển hoá và bảo toàn năng lượng: tính phần năng lượng còn lại", 133, "Định luật bảo toàn và chuyển hoá năng lượng"),
 "74-3": (74, "Dạng 3 · Trung bình · Phân biệt va chạm mềm và va chạm đàn hồi", 145, "Va chạm mềm, va chạm đàn hồi"),
 "76-1": (76, "Dạng 1 · Dễ · Nhận biết chuyển động tròn đều, vận tốc và độ dịch chuyển góc", 34, "Động học của chuyển động tròn đều"),
 "77-1": (77, "Dạng 1 · Dễ · Khái niệm: vận tốc đổi hướng nên có gia tốc hướng tâm", 35, "Lực hướng tâm và gia tốc hướng tâm"),
 "78-1": (78, "Dạng 1 · Dễ · Nhận biết biến dạng kéo, nén, đàn hồi, dẻo và giới hạn đàn hồi", 150, "Biến dạng kéo, nén và giới hạn đàn hồi"),
 "161-2": (161, "Dạng 2 · Dễ · Máy cơ đơn giản và định luật về công: ròng rọc cố định, đòn bẩy", 133, "Định luật bảo toàn và chuyển hoá năng lượng"),
 "150-2": (150, "Dạng 2 · Cơ bản · Tần số, độ cao, độ to: đọc đồ thị dao động hai âm, xếp hạ âm – siêu âm", 164, "Bước sóng, chu kì, tần số, tốc độ truyền sóng"),
 "152-1": (152, "Dạng 1 · Dễ · Điều kiện xuất hiện và chiều của dòng điện cảm ứng (định tính)", 95, "Điều kiện xuất hiện dòng điện cảm ứng"),
}
# số câu chắc đã có (docs/dang-thieu-cau.md) → cần soạn 4 - co
CO = {"6-1": 1, "15-2": 1, "17-1": 2, "46-1": 2, "74-3": 2, "150-2": 1}

C = []  # (key, kiểu, mức, đề, phương án/ý, đáp án, lời giải)
def mc(k, d, q, o, a, e): C.append(dict(k=k, t="multiple_choice", d=d, q=q, o=o, a=a, e=e))
def tf(k, d, q, s): C.append(dict(k=k, t="true_false", d=d, q=q, s=s))  # s = [(ý, đúng?, lời giải)]

# ---------- 2-1 Gọi tên quá trình chuyển thể ----------
mc("2-1", "de", "Sáng sớm, trên lá cây đọng những giọt sương. Sự hình thành giọt sương là quá trình nào?",
   ["Ngưng tụ.", "Bay hơi.", "Đông đặc.", "Nóng chảy."], 0,
   ["Gọi tên theo thể đầu và thể cuối của chính chất đó: hơi nước trong không khí (khí) gặp mặt lá lạnh về đêm thành giọt nước (lỏng).",
    "Khí → lỏng là ngưng tụ.", "Bay hơi là lỏng → khí, ngược chiều; đông đặc và nóng chảy đều có thể rắn, mà ở đây không có chất rắn nào.", "Chọn A."])
mc("2-1", "de", "Rót sáp nến đã nấu chảy vào khuôn rồi để nguội, thu được cây nến rắn. Quá trình chuyển thể của sáp và sự trao đổi nhiệt khi đó là",
   ["đông đặc, sáp nhận nhiệt.", "đông đặc, sáp toả nhiệt.", "nóng chảy, sáp toả nhiệt.", "ngưng tụ, sáp toả nhiệt."], 1,
   ["Sáp chuyển từ thể lỏng sang thể rắn nên đó là đông đặc.", "Đông đặc và ngưng tụ là hai quá trình chất toả nhiệt; nóng chảy và hoá hơi là hai quá trình chất nhận nhiệt.",
    "Phương án A sai chiều trao đổi nhiệt; C gọi nhầm rắn → lỏng; D là khí → lỏng, không đúng thể đầu.", "Chọn B."])
mc("2-1", "trung-binh", "Cho các hiện tượng: (1) quần áo ướt phơi nắng thì khô; (2) nước trong khay của ngăn đá tủ lạnh thành đá; (3) que kem lấy ra khỏi tủ một lúc thì chảy nước; (4) hơi nước từ nồi canh đọng thành giọt dưới nắp vung. Có bao nhiêu hiện tượng mà chất toả nhiệt?",
   ["$1$.", "$2$.", "$3$.", "$4$."], 1,
   ["Gọi tên từng hiện tượng: (1) bay hơi (lỏng → khí); (2) đông đặc (lỏng → rắn); (3) nóng chảy (rắn → lỏng); (4) ngưng tụ (khí → lỏng).",
    "Chất toả nhiệt khi đông đặc và ngưng tụ, tức hiện tượng (2) và (4): có $2$ hiện tượng.",
    "Không đúng $1$ vì bỏ sót (4) hoặc (2); không đúng $3$, $4$ vì bay hơi và nóng chảy là chất nhận nhiệt.", "Chọn B."])
tf("2-1", "trung-binh", "Đun nước trong ấm ở áp suất khí quyển. Khi nước sôi, thấy có “khói trắng” bay ra ở vòi ấm, cách miệng vòi một đoạn.",
   [("Nước sôi là sự hoá hơi xảy ra cả ở mặt thoáng và trong lòng chất lỏng.", True, "Sôi là hoá hơi xảy ra cả ở mặt thoáng và trong lòng chất lỏng, khác bay hơi chỉ ở mặt thoáng."),
    ("“Khói trắng” nhìn thấy ở vòi ấm chính là hơi nước.", False, "Hơi nước trong suốt, không nhìn thấy được; “khói trắng” là những giọt nước rất nhỏ do hơi nước ngưng tụ khi gặp không khí lạnh hơn, chứ không phải hơi nước."),
    ("Khi “khói trắng” hình thành, nước toả nhiệt ra không khí xung quanh.", True, "“Khói trắng” hình thành do ngưng tụ (khí → lỏng), mà ngưng tụ là quá trình chất toả nhiệt."),
    ("Trong suốt thời gian sôi, nước trong ấm vẫn nhận nhiệt và nhiệt độ của nước tăng dần.", False, "Nước vẫn nhận nhiệt nhưng nhiệt độ giữ không đổi ở nhiệt độ sôi (khoảng $100\\ ^\\circ\\text{C}$), nhiệt nhận được dùng để hoá hơi chứ không làm nóng thêm.")])

# ---------- 2-2 Thể tích và hình dạng trong bình ----------
mc("2-2", "de", "Thả một viên bi sắt có thể tích $2\\ \\text{cm}^3$ vào một bình thuỷ tinh rỗng dung tích $100\\ \\text{cm}^3$ rồi đậy kín. Trong bình, viên bi",
   ["chiếm $2\\ \\text{cm}^3$ và giữ nguyên hình dạng riêng của nó.", "chiếm $100\\ \\text{cm}^3$ và có hình dạng của bình.",
    "chiếm $2\\ \\text{cm}^3$ nhưng có hình dạng của phần đáy bình.", "chiếm $100\\ \\text{cm}^3$ nhưng giữ hình dạng riêng."], 0,
   ["Trong chất rắn, các hạt ở rất gần nhau và chỉ dao động quanh vị trí cân bằng cố định nên chất rắn có thể tích riêng và hình dạng riêng.",
    "Viên bi vẫn chiếm $2\\ \\text{cm}^3$ và vẫn tròn, không phụ thuộc bình.", "Phương án C là tính chất của chất lỏng; B, D gán cho chất rắn tính chất chiếm đầy bình của chất khí.", "Chọn A."])
mc("2-2", "de", "Rót $200\\ \\text{mL}$ nước từ một chai sang một cái bát rộng có dung tích $500\\ \\text{mL}$. Lượng nước trong bát",
   ["chiếm $500\\ \\text{mL}$ và có hình dạng của bát.", "chiếm $200\\ \\text{mL}$ và có hình dạng phần bát mà nó chứa đầy.",
    "chiếm $200\\ \\text{mL}$ và vẫn giữ hình dạng của chai.", "không có thể tích xác định vì đã đổi bình chứa."], 1,
   ["Trong chất lỏng, các hạt vẫn ở gần nhau nhưng vị trí cân bằng luôn thay đổi: chất lỏng có thể tích riêng nhưng không có hình dạng riêng.",
    "Nước vẫn là $200\\ \\text{mL}$ và lấy hình dạng phần dưới của bát.", "Phương án A gán cho nước tính chất của chất khí; C gán tính chất của chất rắn.", "Chọn B."])
mc("2-2", "trung-binh", "Một bình thép kín dung tích $5\\ \\text{L}$ đã hút hết không khí. Bơm vào bình một lượng khí oxygen mà trước khi bơm chiếm $0{,}5\\ \\text{L}$. Nhiệt độ không đổi. Trong bình, lượng khí oxygen đó",
   ["chiếm $0{,}5\\ \\text{L}$, nằm ở đáy bình.", "chiếm toàn bộ $5\\ \\text{L}$ và có hình dạng của bình.",
    "chiếm $0{,}5\\ \\text{L}$ nhưng có hình dạng của bình.", "chiếm $2{,}5\\ \\text{L}$ ở nửa dưới bình."], 1,
   ["Trong chất khí, các phân tử ở rất xa nhau, lực tương tác rất yếu và chúng chuyển động hỗn loạn về mọi phía.",
    "Vì vậy khí không có thể tích riêng, không có hình dạng riêng: nó chiếm toàn bộ $5\\ \\text{L}$ của bình.",
    "Không đúng A, C vì khí không giữ thể tích ban đầu; không đúng D vì phân tử khí không dồn về phía dưới.", "Chọn B."])
tf("2-2", "trung-binh", "Dùng mô hình động học phân tử để giải thích thể tích và hình dạng của chất rắn, chất lỏng, chất khí.",
   [("Chất rắn có thể tích và hình dạng riêng vì các hạt chỉ dao động quanh những vị trí cân bằng cố định.", True, "Các hạt trong chất rắn rất gần nhau, liên kết mạnh, dao động quanh vị trí cố định nên giữ được thể tích và hình dạng."),
    ("Chất lỏng có thể tích riêng nhưng không có hình dạng riêng vì vị trí cân bằng của các hạt luôn thay đổi.", True, "Hạt trong chất lỏng vẫn gần nhau (giữ thể tích) nhưng vị trí cân bằng luôn dịch chuyển nên chất lỏng lấy hình dạng của bình."),
    ("Chất khí có thể tích riêng, chỉ không có hình dạng riêng.", False, "Chất khí không có cả thể tích riêng lẫn hình dạng riêng, chứ không phải chỉ thiếu hình dạng riêng; nó chiếm toàn bộ bình chứa."),
    ("Rót một lượng dầu ăn từ chai nhỏ sang chai lớn thì thể tích dầu tăng lên bằng thể tích chai lớn.", False, "Dầu ăn là chất lỏng nên thể tích giữ nguyên, chỉ đổi hình dạng theo chai lớn.")])

# ---------- 3-1 Chiều truyền nhiệt năng ----------
mc("3-1", "de", "Thả một miếng đồng ở $80\\ ^\\circ\\text{C}$ vào cốc nước ở $20\\ ^\\circ\\text{C}$. Bỏ qua trao đổi nhiệt với môi trường. Nhiệt năng truyền",
   ["từ miếng đồng sang nước cho đến khi nhiệt độ hai vật bằng nhau.", "từ nước sang miếng đồng cho đến khi nhiệt độ hai vật bằng nhau.",
    "từ miếng đồng sang nước cho đến khi nhiệt năng của hai vật bằng nhau.", "từ nước sang miếng đồng vì nước có khối lượng lớn hơn."], 0,
   ["Nhiệt năng tự truyền từ vật có nhiệt độ cao hơn sang vật có nhiệt độ thấp hơn: từ đồng ($80\\ ^\\circ\\text{C}$) sang nước ($20\\ ^\\circ\\text{C}$).",
    "Sự truyền dừng khi hai vật cùng nhiệt độ (cân bằng nhiệt), không phải khi nhiệt năng bằng nhau như phương án C.",
    "Phương án B, D sai chiều; khối lượng không quyết định chiều truyền.", "Chọn A."])
mc("3-1", "de", "Hai vật tiếp xúc nhau đã ở trạng thái cân bằng nhiệt. Hai vật đó chắc chắn có cùng",
   ["nhiệt năng.", "nhiệt độ.", "khối lượng.", "nhiệt dung riêng."], 1,
   ["Cân bằng nhiệt là trạng thái hai vật có cùng nhiệt độ nên không còn truyền nhiệt năng cho nhau.",
    "Nhiệt năng, khối lượng, nhiệt dung riêng của hai vật vẫn có thể khác nhau.", "Chọn B."])
mc("3-1", "trung-binh", "Một hồ nước lớn ở $15\\ ^\\circ\\text{C}$ có nhiệt năng lớn hơn rất nhiều so với một ấm nhôm nhỏ đựng nước ở $90\\ ^\\circ\\text{C}$. Nhúng ấm (đậy kín) vào hồ. Phát biểu nào sau đây đúng?",
   ["Nhiệt năng truyền từ hồ sang ấm vì hồ có nhiệt năng lớn hơn.", "Nhiệt năng truyền từ ấm sang hồ vì ấm có nhiệt độ cao hơn.",
    "Không có sự truyền nhiệt năng vì hồ quá lớn so với ấm.", "Nhiệt năng truyền qua lại cho đến khi nhiệt năng của hồ và ấm bằng nhau."], 1,
   ["Chiều truyền nhiệt năng chỉ do nhiệt độ quyết định: từ ấm ($90\\ ^\\circ\\text{C}$) sang hồ ($15\\ ^\\circ\\text{C}$).",
    "Phương án A sai vì lấy lượng nhiệt năng làm căn cứ; C sai vì hai vật chênh nhiệt độ thì luôn truyền nhiệt; D sai vì điểm dừng là bằng nhiệt độ.", "Chọn B."])
tf("3-1", "trung-binh", "Ba vật A, B, C. Cho A tiếp xúc B thì thấy nhiệt năng truyền từ A sang B. Cho B tiếp xúc C (trước khi B chạm A) thì thấy B và C đã ở trạng thái cân bằng nhiệt. Bỏ qua trao đổi nhiệt với môi trường.",
   [("Lúc đầu nhiệt độ của A cao hơn nhiệt độ của B.", True, "Nhiệt năng truyền từ A sang B nên $t_A \\gt t_B$."),
    ("Lúc đầu B và C có cùng nhiệt độ.", True, "B và C ở cân bằng nhiệt nên $t_B = t_C$."),
    ("Nếu cho A tiếp xúc C thì nhiệt năng truyền từ C sang A.", False, "Vì $t_A \\gt t_B = t_C$ nên nhiệt năng truyền từ A sang C, chứ không phải từ C sang A."),
    ("Nếu B có khối lượng lớn hơn A nhiều lần thì nhiệt năng có thể truyền từ B sang A.", False, "Chiều truyền chỉ do nhiệt độ quyết định, không do khối lượng; vẫn truyền từ A sang B.")])

# ---------- 6-1 Thuyết động học phân tử (cần 3) ----------
mc("6-1", "de", "Quan sát qua kính hiển vi thấy các hạt phấn hoa lơ lửng trong nước chuyển động không ngừng theo những đường gấp khúc (chuyển động Brown). Hiện tượng này chứng tỏ",
   ["các phân tử nước chuyển động hỗn loạn, không ngừng và va chạm vào hạt phấn hoa.", "hạt phấn hoa tự sinh ra năng lượng để chuyển động.",
    "giữa các phân tử nước chỉ có lực đẩy, không có lực hút.", "các phân tử nước đứng yên, còn hạt phấn hoa trôi theo dòng nước."], 0,
   ["Hạt phấn hoa bị các phân tử nước va đập từ mọi phía; các va đập không cân bằng nên hạt bị đẩy lệch liên tục.",
    "Do đó chuyển động Brown là bằng chứng các phân tử nước chuyển động hỗn loạn, không ngừng.",
    "Phương án B, D trái với nguyên nhân va đập; C không liên quan tới chuyển động Brown.", "Chọn A."])
mc("6-1", "de", "Theo thuyết động học phân tử chất khí, áp suất của chất khí lên thành bình là do",
   ["trọng lượng của khối khí đè lên đáy bình.", "các phân tử khí va chạm vào thành bình.",
    "lực hút giữa các phân tử khí và thành bình.", "các phân tử khí đứng yên đẩy nhau ra xa."], 1,
   ["Mỗi phân tử khí va chạm vào thành bình tác dụng lên thành một lực; vô số va chạm đó gây ra áp suất của khí lên thành bình.",
    "Phương án A sai vì áp suất tác dụng lên mọi phía của thành bình, không chỉ đáy; D sai vì phân tử khí chuyển động không ngừng.", "Chọn B."])
mc("6-1", "trung-binh", "Cho các phát biểu về chất khí: (1) Chất khí gồm các phân tử có kích thước rất nhỏ so với khoảng cách giữa chúng. (2) Các phân tử khí chuyển động hỗn loạn, không ngừng; nhiệt độ càng cao thì chúng chuyển động càng nhanh. (3) Giữa hai va chạm, phân tử khí chuyển động theo đường cong do lực hút của các phân tử khác. (4) Các phân tử khí va chạm vào thành bình gây ra áp suất. Số phát biểu đúng là",
   ["$1$.", "$2$.", "$3$.", "$4$."], 2,
   ["(1), (2), (4) đúng theo thuyết động học phân tử chất khí.",
    "(3) sai: lực tương tác giữa các phân tử khí rất nhỏ (trừ lúc va chạm) nên giữa hai va chạm phân tử chuyển động thẳng đều.",
    "Vậy có $3$ phát biểu đúng.", "Chọn C."])

# ---------- 10-1 Từ trường quanh thanh nam châm ----------
mc("10-1", "de", "Ở bên ngoài một thanh nam châm thẳng, các đường sức từ",
   ["đi ra từ cực Bắc (N) và đi vào cực Nam (S).", "đi ra từ cực Nam (S) và đi vào cực Bắc (N).",
    "là những đường thẳng song song với thanh.", "là những đường cong hở, không khép kín."], 0,
   ["Đường sức từ là đường cong khép kín; bên ngoài nam châm đi ra từ cực N, đi vào cực S; bên trong nam châm đi từ S sang N.",
    "Phương án B ngược chiều; C, D sai hình dạng.", "Chọn A."])
mc("10-1", "de", "Một thanh nam châm thẳng nằm ngang. Đặt một kim nam châm nhỏ tại điểm P nằm trên đường thẳng chứa thanh, ở ngoài thanh, ngay cạnh cực Nam (S). Khi kim nằm cân bằng, cực Bắc của kim",
   ["hướng ra xa thanh nam châm.", "hướng về phía cực Nam (S) của thanh.", "vuông góc với thanh nam châm.", "có thể chỉ theo hướng bất kì."], 1,
   ["Đầu N của kim nhỏ nằm cân bằng chỉ theo chiều đường sức tại đó.",
    "Bên ngoài thanh, đường sức đi vào cực S; tại P đường sức hướng vào cực S, nên đầu N của kim hướng về cực S của thanh.",
    "Kiểm lại: cực N của kim và cực S của thanh khác tên nên hút nhau.", "Chọn B."])
mc("10-1", "trung-binh", "Trên hình ảnh đường sức từ của một thanh nam châm, điểm A ở gần một cực có các đường sức vẽ mau, điểm B ở xa thanh có các đường sức vẽ thưa. So sánh độ mạnh của từ trường tại A và tại B.",
   ["Tại A mạnh hơn tại B.", "Tại B mạnh hơn tại A.", "Tại A và tại B mạnh như nhau.", "Chưa so sánh được vì chưa biết chiều đường sức."], 0,
   ["Quy ước: nơi đường sức từ mau thì từ trường mạnh, nơi thưa thì từ trường yếu.",
    "Đường sức tại A mau hơn tại B nên từ trường tại A mạnh hơn.", "Phương án D sai vì độ mạnh đọc qua độ mau, không phụ thuộc chiều.", "Chọn A."])
tf("10-1", "trung-binh", "Một thanh nam châm thẳng nằm ngang, cực Bắc (N) ở bên phải, cực Nam (S) ở bên trái. Điểm M ở ngay phía trên chính giữa thanh, ngoài thanh.",
   [("Tại M, từ trường hướng từ trái sang phải.", False, "Bên ngoài thanh, đường sức đi từ cực N (bên phải) sang cực S (bên trái), nên tại M từ trường hướng sang trái, chứ không phải sang phải."),
    ("Bên trong thanh, đường sức từ đi từ cực S sang cực N, tức là hướng sang phải.", True, "Đường sức khép kín: bên trong nam châm đi từ S sang N, từ trái sang phải."),
    ("Đường sức từ là những đường có thật trong không gian quanh nam châm.", False, "Đường sức từ là đường vẽ quy ước để mô tả từ trường, chứ không phải đường có thật; mạt sắt chỉ cho hình ảnh của chúng (từ phổ)."),
    ("Qua mỗi điểm quanh thanh nam châm chỉ vẽ được một đường sức từ.", True, "Tại mỗi điểm từ trường chỉ có một hướng nên qua mỗi điểm chỉ có một đường sức.")])

# ---------- 10-2 Dây thẳng, nắm tay phải ----------
mc("10-2", "de", "Đường sức từ của dòng điện chạy trong một dây dẫn thẳng dài là",
   ["những đường thẳng song song với dây dẫn.", "những đường tròn đồng tâm nằm trong mặt phẳng vuông góc với dây, tâm nằm trên dây.",
    "những đường thẳng vuông góc với dây, hướng ra xa dây.", "những đường xoắn ốc quấn quanh dây dẫn."], 1,
   ["Từ phổ của dòng điện thẳng dài là các đường tròn đồng tâm, nằm trong mặt phẳng vuông góc với dây, tâm là giao điểm của dây với mặt phẳng đó.",
    "Chiều đường sức xác định bằng quy tắc nắm tay phải.", "Chọn B."])
mc("10-2", "trung-binh", "Một dây dẫn thẳng dài đặt vuông góc với mặt phẳng trang giấy, dòng điện trong dây hướng từ trang giấy ra phía người nhìn. Đặt một kim nam châm nhỏ tại điểm A trong mặt phẳng trang giấy, ở bên phải dây. Khi cân bằng, cực Bắc của kim chỉ",
   ["lên phía trên trang giấy.", "xuống phía dưới trang giấy.", "sang phải, ra xa dây.", "sang trái, về phía dây."], 0,
   ["Quy tắc nắm tay phải: ngón cái chỉ chiều dòng điện (ra phía người nhìn), các ngón khum lại chỉ chiều đường sức: đường sức là các đường tròn ngược chiều kim đồng hồ khi nhìn vào trang giấy.",
    "Tại điểm bên phải dây, tiếp tuyến của đường tròn ngược chiều kim đồng hồ hướng lên trên.",
    "Phương án C, D sai vì đường sức không hướng theo bán kính; B là kết quả khi dòng điện đi vào trang giấy.", "Chọn A."])
mc("10-2", "trung-binh", "Một dây dẫn thẳng dài đặt vuông góc với mặt phẳng trang giấy, dòng điện trong dây đi vào trang giấy (ra xa người nhìn). Điểm B trong mặt phẳng trang giấy, ở ngay phía trên dây. Từ trường tại B hướng",
   ["sang trái.", "sang phải.", "lên trên.", "xuống dưới."], 1,
   ["Ngón cái chỉ vào trang giấy thì các ngón khum lại theo chiều kim đồng hồ khi nhìn vào trang: đường sức là các đường tròn cùng chiều kim đồng hồ.",
    "Tại điểm ở phía trên tâm, tiếp tuyến của đường tròn cùng chiều kim đồng hồ hướng sang phải.",
    "Phương án A là kết quả khi dòng điện hướng ra phía người nhìn; C, D sai vì từ trường tại B vuông góc với bán kính nối dây với B.", "Chọn B."])
tf("10-2", "trung-binh", "Một dây dẫn thẳng dài có dòng điện không đổi chạy qua. Hai điểm $C_1$ và $C_2$ ở cùng một phía của dây, cách dây lần lượt $2\\ \\text{cm}$ và $6\\ \\text{cm}$.",
   [("Đảo chiều dòng điện thì chiều từ trường tại $C_1$ đổi ngược lại.", True, "Theo quy tắc nắm tay phải, đảo chiều ngón cái (dòng điện) thì chiều khum của các ngón (đường sức) đổi ngược."),
    ("Từ trường tại $C_2$ mạnh hơn tại $C_1$.", False, "Càng xa dây từ trường càng yếu; $C_2$ xa dây hơn nên từ trường tại $C_2$ yếu hơn, chứ không mạnh hơn."),
    ("Quy tắc nắm tay phải: ngón cái chỉ chiều dòng điện, các ngón tay khum lại chỉ chiều đường sức từ.", True, "Đây là cách dùng quy tắc nắm tay phải cho dòng điện thẳng."),
    ("Ngắt dòng điện, kim nam châm nhỏ đặt tại $C_1$ vẫn nằm dọc theo đường tròn quanh dây.", False, "Không còn dòng điện thì không còn từ trường của dây; kim quay về hướng Bắc – Nam theo từ trường Trái Đất, chứ không nằm dọc đường tròn quanh dây.")])

# ---------- 127-1 Điện trường xoáy ----------
mc("127-1", "de", "Điện trường xoáy được sinh ra bởi",
   ["các điện tích đứng yên.", "từ trường biến thiên theo thời gian.", "từ trường không đổi theo thời gian.", "dòng điện không đổi chạy trong dây dẫn."], 1,
   ["Theo Maxwell, từ trường biến thiên theo thời gian sinh ra điện trường xoáy.",
    "Phương án A sinh ra điện trường tĩnh; C và D chỉ có từ trường không đổi nên không sinh ra điện trường xoáy.", "Chọn B."])
mc("127-1", "de", "Đường sức của điện trường xoáy là",
   ["những đường cong kín bao quanh các đường sức từ.", "những đường đi ra từ điện tích dương và kết thúc ở điện tích âm.",
    "những đường thẳng song song, cách đều nhau.", "những đường cong hở, có điểm đầu và điểm cuối."], 0,
   ["Điện trường xoáy có đường sức là đường cong kín, bao quanh các đường sức của từ trường biến thiên.",
    "Phương án B là đường sức của điện trường tĩnh; C là điện trường đều giữa hai bản tụ.", "Chọn A."])
mc("127-1", "trung-binh", "Một vòng dây dẫn kín nối với điện kế nhạy đặt gần một nam châm. Trường hợp nào sau đây trong vòng dây có điện trường xoáy làm kim điện kế lệch?",
   ["Nam châm vĩnh cửu rất mạnh đặt yên cạnh vòng dây.", "Nam châm điện có dòng điện không đổi đặt yên cạnh vòng dây.",
    "Nam châm đang chuyển động lại gần vòng dây.", "Nam châm và vòng dây cùng đứng yên, vòng dây được nung nóng."], 2,
   ["Điện trường xoáy chỉ xuất hiện ở nơi từ trường biến thiên theo thời gian.",
    "Khi nam châm chuyển động lại gần, từ trường tại vòng dây tăng dần nên sinh ra điện trường xoáy, đẩy electron tự do tạo dòng điện.",
    "Phương án A, B: từ trường mạnh nhưng không đổi nên không sinh điện trường xoáy; D: nung nóng không làm từ trường biến thiên.", "Chọn C."])
tf("127-1", "trung-binh", "So sánh điện trường tĩnh và điện trường xoáy.",
   [("Điện trường tĩnh do điện tích đứng yên gây ra, đường sức không khép kín.", True, "Đường sức điện trường tĩnh đi ra từ điện tích dương, kết thúc ở điện tích âm (hoặc ở vô cực) nên không khép kín."),
    ("Điện trường xoáy chỉ xuất hiện khi trong vùng từ trường biến thiên có đặt một vòng dây dẫn kín.", False, "Điện trường xoáy xuất hiện ở mọi nơi có từ trường biến thiên, có hay không có dây dẫn; vòng dây kín chỉ giúp phát hiện nó qua dòng điện cảm ứng."),
    ("Từ trường càng mạnh (dù không đổi theo thời gian) thì điện trường xoáy sinh ra càng mạnh.", False, "Từ trường không đổi thì không sinh điện trường xoáy, dù mạnh đến đâu; chỉ từ trường biến thiên mới sinh ra nó."),
    ("Trong vòng dây kín, điện trường xoáy làm các electron tự do chuyển động có hướng, tạo thành dòng điện cảm ứng.", True, "Điện trường xoáy tác dụng lực điện lên electron tự do, làm chúng dịch chuyển có hướng theo vòng dây.")])

# ---------- 15-2 Đồng vị (cần 3) ----------
mc("15-2", "de", "Cặp hạt nhân nào sau đây là đồng vị của nhau?",
   ["$^{14}_{6}\\text{C}$ và $^{14}_{7}\\text{N}$.", "$^{16}_{8}\\text{O}$ và $^{17}_{8}\\text{O}$.", "$^{13}_{6}\\text{C}$ và $^{14}_{7}\\text{N}$.", "$^{3}_{1}\\text{H}$ và $^{3}_{2}\\text{He}$."], 1,
   ["Đồng vị là các hạt nhân cùng số prôtôn $Z$, khác số nơtron $N$.",
    "$^{16}_{8}\\text{O}$ và $^{17}_{8}\\text{O}$ cùng $Z=8$, số nơtron $N=A-Z$ lần lượt là $8$ và $9$: là đồng vị.",
    "Phương án A, D chỉ cùng số khối; C cùng số nơtron ($N=7$) nhưng khác $Z$: đều không phải đồng vị.", "Chọn B."])
mc("15-2", "trung-binh", "Cho năm hạt nhân: $^{1}_{1}\\text{H}$, $^{2}_{1}\\text{H}$, $^{3}_{1}\\text{H}$, $^{3}_{2}\\text{He}$, $^{4}_{2}\\text{He}$. Trong năm hạt nhân này có bao nhiêu cặp đồng vị?",
   ["$2$.", "$3$.", "$4$.", "$5$."], 2,
   ["Đồng vị phải cùng số prôtôn $Z$; xét từng nhóm cùng $Z$.",
    "Nhóm $Z=1$ có ba hạt nhân $^{1}_{1}\\text{H}$, $^{2}_{1}\\text{H}$, $^{3}_{1}\\text{H}$: ghép được $3$ cặp. Nhóm $Z=2$ có $^{3}_{2}\\text{He}$, $^{4}_{2}\\text{He}$: $1$ cặp.",
    "Tổng cộng $3+1=4$ cặp. Cặp $^{3}_{1}\\text{H}$ – $^{3}_{2}\\text{He}$ chỉ cùng số khối nên không tính.",
    "Không đúng $2$ vì chỉ đếm theo từng nguyên tố mà quên ghép cặp trong nhóm ba hạt nhân hiđrô; không đúng $5$ vì đã tính thêm cặp cùng số khối.", "Chọn C."])
tf("15-2", "trung-binh", "Xét hai hạt nhân $^{35}_{17}\\text{Cl}$ và $^{37}_{17}\\text{Cl}$.",
   [("Hai hạt nhân có cùng số prôtôn.", True, "Cả hai đều có $Z=17$."),
    ("Hạt nhân $^{37}_{17}\\text{Cl}$ có nhiều hơn hạt nhân $^{35}_{17}\\text{Cl}$ hai nơtron.", True, "$N=A-Z$: $37-17=20$ và $35-17=18$, chênh $2$ nơtron."),
    ("Hai nguyên tử clo này có tính chất hoá học khác nhau vì số khối khác nhau.", False, "Cùng $Z$ thì cùng số êlectron nên tính chất hoá học giống nhau, chứ không khác nhau."),
    ("$^{37}_{17}\\text{Cl}$ và $^{37}_{18}\\text{Ar}$ là đồng vị của nhau vì có cùng số khối.", False, "Hai hạt nhân khác số prôtôn ($17$ và $18$) nên không phải đồng vị; cùng số khối chưa đủ.")])

# ---------- 17-1 Phân hạch, nhiệt hạch, k (cần 2) ----------
mc("17-1", "trung-binh", "Trong một lò phản ứng hạt nhân, số nơtron đếm được ở hai thế hệ liên tiếp là $20\\,000$ và $19\\,800$. Hệ số nhân nơtron $k$ và tình trạng của lò là",
   ["$k=0{,}99$; phản ứng dây chuyền tắt dần, công suất lò giảm.", "$k=1{,}01$; phản ứng dây chuyền tăng nhanh, công suất lò tăng.",
    "$k=0{,}99$; phản ứng tự duy trì, công suất lò ổn định.", "$k=1$; phản ứng tự duy trì, công suất lò ổn định."], 0,
   ["Hệ số nhân là tỉ số số nơtron thế hệ sau so với thế hệ trước: $k=\\dfrac{N_{\\text{sau}}}{N_{\\text{trước}}}=\\dfrac{19\\,800}{20\\,000}=0{,}99$.",
    "Vì $k\\lt1$ nên phản ứng dây chuyền tắt dần, công suất lò giảm.",
    "Phương án B lấy nhầm tỉ số đảo ngược; C sai vì chỉ $k=1$ mới tự duy trì ổn định.", "Chọn A."])
tf("17-1", "trung-binh", "Cho hai phản ứng hạt nhân: (1) ${}^{2}_{1}\\text{H}+{}^{2}_{1}\\text{H}\\to{}^{3}_{2}\\text{He}+{}^{1}_{0}\\text{n}$; (2) ${}^{1}_{0}\\text{n}+{}^{235}_{92}\\text{U}\\to{}^{140}_{54}\\text{Xe}+{}^{94}_{38}\\text{Sr}+2\\,{}^{1}_{0}\\text{n}$.",
   [("Phản ứng (1) là phản ứng nhiệt hạch.", True, "Hai hạt nhân rất nhẹ ($^{2}_{1}\\text{H}$) kết hợp thành hạt nhân nặng hơn ($^{3}_{2}\\text{He}$): nhiệt hạch."),
    ("Phản ứng (2) là phản ứng nhiệt hạch vì nó toả năng lượng.", False, "Hạt nhân rất nặng $^{235}_{92}\\text{U}$ hấp thụ nơtron rồi vỡ thành hai hạt nhân nhẹ hơn: đó là phân hạch, chứ không phải nhiệt hạch; cả hai loại đều toả năng lượng."),
    ("Phản ứng (2) chỉ xảy ra khi nhiên liệu được nung tới hàng chục triệu độ.", False, "Phân hạch $^{235}\\text{U}$ được kích thích bằng nơtron, không cần nhiệt độ rất cao; nhiệt độ hàng chục triệu độ là điều kiện của nhiệt hạch."),
    ("Trong lò phản ứng, người ta dùng thanh điều khiển hấp thụ bớt nơtron để giữ $k=1$.", True, "Thanh điều khiển (chứa chất hấp thụ nơtron) được đưa vào hay rút ra để giữ hệ số nhân $k=1$, công suất ổn định.")])

# ---------- 25-1 Tắt dần, duy trì, cưỡng bức ----------
mc("25-1", "de", "Con lắc của đồng hồ quả lắc được cấp năng lượng từ dây cót hoặc pin, mỗi chu kì bù đúng phần năng lượng đã mất. Dao động của con lắc là",
   ["dao động tắt dần.", "dao động duy trì.", "dao động cưỡng bức.", "dao động tự do không có lực cản."], 1,
   ["Dao động duy trì: năng lượng được bù đúng phần đã mất trong mỗi chu kì, biên độ không đổi, chu kì bằng chu kì riêng.",
    "Không phải cưỡng bức vì không có ngoại lực tuần hoàn tác dụng liên tục; không phải tắt dần vì biên độ không giảm.", "Chọn B."])
mc("25-1", "de", "Nguyên nhân làm cho dao động của con lắc tắt dần là",
   ["lực cản của môi trường.", "trọng lực tác dụng lên vật.", "lực đàn hồi của lò xo.", "ngoại lực tuần hoàn tác dụng lên vật."], 0,
   ["Lực cản (ma sát, sức cản không khí) làm cơ năng chuyển dần thành nhiệt năng, biên độ giảm dần.",
    "Trọng lực, lực đàn hồi là lực gây dao động; ngoại lực tuần hoàn gây dao động cưỡng bức.", "Chọn A."])
mc("25-1", "trung-binh", "Một con lắc có tần số dao động riêng $2\\ \\text{Hz}$ chịu tác dụng của một ngoại lực tuần hoàn có tần số $5\\ \\text{Hz}$. Khi đã ổn định, con lắc dao động",
   ["cưỡng bức với tần số $2\\ \\text{Hz}$.", "cưỡng bức với tần số $5\\ \\text{Hz}$.", "duy trì với tần số $2\\ \\text{Hz}$.", "tắt dần với tần số $3\\ \\text{Hz}$."], 1,
   ["Ngoại lực tuần hoàn tác dụng liên tục nên đây là dao động cưỡng bức.",
    "Khi ổn định, tần số dao động cưỡng bức bằng tần số của ngoại lực: $f=5\\ \\text{Hz}$, có thể khác tần số riêng.",
    "Phương án A, C lấy nhầm tần số riêng; D trừ hai tần số, không có cơ sở.", "Chọn B."])
tf("25-1", "trung-binh", "Xét các dao động tắt dần, dao động duy trì và dao động cưỡng bức.",
   [("Dao động duy trì có chu kì bằng chu kì dao động riêng của hệ.", True, "Năng lượng chỉ được bù đúng phần mất đi nên hệ vẫn dao động với chu kì riêng."),
    ("Dao động cưỡng bức khi đã ổn định có tần số bằng tần số dao động riêng của hệ.", False, "Tần số dao động cưỡng bức ổn định bằng tần số của ngoại lực, chứ không phải tần số riêng (chỉ trùng khi cộng hưởng)."),
    ("Biên độ của dao động tắt dần giảm dần theo thời gian.", True, "Lực cản làm cơ năng giảm nên biên độ giảm dần."),
    ("Trong dao động duy trì, năng lượng được cung cấp nhờ một ngoại lực tuần hoàn tác dụng liên tục lên vật.", False, "Dao động duy trì được bù năng lượng trong một phần của mỗi chu kì bằng cơ cấu của chính hệ; ngoại lực tuần hoàn tác dụng liên tục là đặc điểm của dao động cưỡng bức.")])

# ---------- 28-1 Sóng ngang, sóng dọc ----------
mc("28-1", "de", "Sóng dọc là sóng mà các phần tử môi trường dao động theo phương",
   ["vuông góc với phương truyền sóng.", "trùng với phương truyền sóng.", "luôn nằm ngang.", "luôn thẳng đứng."], 1,
   ["Gọi tên sóng bằng cách so phương dao động với phương truyền: trùng nhau là sóng dọc, vuông góc là sóng ngang.",
    "Phương án C, D sai vì tên sóng không phụ thuộc phương nằm ngang hay thẳng đứng.", "Chọn B."])
mc("28-1", "de", "Sóng âm truyền trong không khí là",
   ["sóng dọc.", "sóng ngang.", "sóng điện từ.", "vừa là sóng ngang vừa là sóng dọc."], 0,
   ["Trong lòng chất khí chỉ truyền được sóng dọc: các lớp không khí bị nén, giãn dọc theo phương truyền.",
    "Sóng ngang không truyền được trong lòng chất khí; sóng âm là sóng cơ, không phải sóng điện từ.", "Chọn A."])
mc("28-1", "trung-binh", "Một lò xo dài, mềm nằm trên mặt sàn ngang. Đẩy – kéo đầu lò xo qua lại dọc theo trục lò xo thì thấy các chỗ nén, giãn của các vòng lò xo lan dọc theo lò xo. Sóng trên lò xo là",
   ["sóng ngang, vì lò xo nằm ngang.", "sóng dọc, vì các vòng lò xo dao động dọc theo phương truyền sóng.",
    "sóng ngang, vì sóng lan truyền theo phương ngang.", "sóng dọc, vì lò xo là vật rắn."], 1,
   ["Phương truyền sóng: dọc theo trục lò xo. Phương dao động của các vòng: cũng dọc theo trục lò xo.",
    "Hai phương trùng nhau nên đây là sóng dọc.",
    "Phương án A, C dựa vào hướng của lò xo hay của phương truyền mà không so hai phương; D đúng tên sóng nhưng sai lí do (vật rắn truyền được cả sóng ngang).", "Chọn B."])
tf("28-1", "trung-binh", "Một người cầm đầu A của sợi dây dài căng ngang và rung đầu A lên – xuống theo phương thẳng đứng; dao động lan dọc theo dây.",
   [("Sóng trên dây là sóng ngang.", True, "Phần tử dây dao động thẳng đứng, sóng truyền nằm ngang dọc dây: hai phương vuông góc nên là sóng ngang."),
    ("Rung đầu A nhanh gấp đôi thì sóng trên dây trở thành sóng dọc.", False, "Tần số không quyết định loại sóng; phương dao động vẫn vuông góc phương truyền nên vẫn là sóng ngang."),
    ("Sóng ngang truyền được trong lòng chất khí.", False, "Sóng ngang chỉ truyền trong chất rắn và trên mặt chất lỏng, không truyền được trong lòng chất khí."),
    ("Sóng dọc truyền được trong chất rắn, chất lỏng và chất khí.", True, "Sóng dọc dựa vào sự nén, giãn của môi trường nên truyền được trong cả ba thể.")])

# ---------- 30-3 Nhận định về sóng điện từ ----------
mc("30-3", "trung-binh", "Phát biểu nào sau đây về sóng điện từ là đúng?",
   ["Sóng điện từ không truyền được trong chân không.", "Sóng điện từ là sóng ngang.",
    "Tại mỗi điểm, $\\vec E$ và $\\vec B$ dao động lệch pha nhau $\\dfrac{\\pi}{2}$.", "Tốc độ của sóng điện từ trong chân không phụ thuộc vào tần số."], 1,
   ["Tại mỗi điểm, $\\vec E$ và $\\vec B$ vuông góc với nhau và cùng vuông góc với phương truyền nên sóng điện từ là sóng ngang.",
    "Sai A vì sóng điện từ truyền được cả trong chân không; sai C vì $\\vec E$ và $\\vec B$ dao động cùng pha; sai D vì mọi sóng điện từ trong chân không có cùng tốc độ $c$.", "Chọn B."])
mc("30-3", "trung-binh", "Khi một sóng điện từ truyền từ không khí vào nước thì",
   ["tần số không đổi, bước sóng giảm.", "tần số giảm, bước sóng không đổi.", "tần số tăng, bước sóng tăng.", "tần số và bước sóng đều không đổi."], 0,
   ["Khi đổi môi trường, tần số do nguồn quyết định nên không đổi.",
    "Tốc độ truyền trong nước nhỏ hơn trong không khí; $\\lambda=\\dfrac{v}{f}$ nên bước sóng giảm.",
    "Phương án B, C cho tần số thay đổi; D bỏ qua sự thay đổi tốc độ truyền.", "Chọn A."])
mc("30-3", "trung-binh", "Phát biểu nào sau đây về sóng điện từ là SAI?",
   ["Sóng điện từ mang năng lượng.", "Sóng điện từ có thể phản xạ, khúc xạ, giao thoa.",
    "Trong chân không, tia X truyền nhanh hơn ánh sáng nhìn thấy.", "Sóng điện từ là điện từ trường lan truyền trong không gian."], 2,
   ["Trong chân không, mọi sóng điện từ (vô tuyến, ánh sáng, tia X…) có cùng tốc độ $c\\approx3\\cdot10^{8}\\ \\text{m/s}$, nên C sai.",
    "A, B, D là các tính chất đúng của sóng điện từ.", "Chọn C."])
tf("30-3", "trung-binh", "Xét các nhận định về sóng điện từ trong chân không.",
   [("Sóng vô tuyến, ánh sáng nhìn thấy và tia X đều là sóng điện từ.", True, "Chúng là các vùng khác nhau trên thang sóng điện từ, chỉ khác bước sóng."),
    ("Mọi sóng điện từ truyền với cùng tốc độ $3\\cdot10^{8}\\ \\text{m/s}$.", True, "Trong chân không, mọi sóng điện từ có tốc độ $c\\approx3\\cdot10^{8}\\ \\text{m/s}$."),
    ("Tại mỗi điểm, $\\vec E$ và $\\vec B$ dao động cùng phương.", False, "$\\vec E$ và $\\vec B$ luôn vuông góc với nhau, chứ không cùng phương."),
    ("Sóng điện từ có tần số $100\\ \\text{MHz}$ có bước sóng $30\\ \\text{m}$.", False, "$\\lambda=\\dfrac{c}{f}=\\dfrac{3\\cdot10^{8}}{100\\cdot10^{6}}=3\\ \\text{m}$, chứ không phải $30\\ \\text{m}$.")])

# ---------- 41-1 Ampe kế, chiều electron, dòng một chiều/không đổi ----------
mc("41-1", "de", "Để đo cường độ dòng điện chạy qua một bóng đèn, ampe kế phải được mắc",
   ["nối tiếp với bóng đèn.", "song song với bóng đèn.", "song song với nguồn điện.", "tuỳ ý, nối tiếp hay song song đều được."], 0,
   ["Ampe kế đo dòng điện chạy qua chính nó, nên dòng điện qua đèn phải đi qua ampe kế: mắc nối tiếp với đèn.",
    "Mắc song song (B, C) thì ampe kế không đo dòng qua đèn và có thể bị hỏng vì điện trở ampe kế rất nhỏ.", "Chọn A."])
mc("41-1", "de", "Trong một dây dẫn kim loại, chiều dòng điện quy ước",
   ["cùng chiều chuyển động có hướng của các electron tự do.", "ngược chiều chuyển động có hướng của các electron tự do.",
    "ở mạch ngoài luôn đi từ cực âm sang cực dương của nguồn.", "phụ thuộc vào vật liệu làm dây dẫn."], 1,
   ["Chiều dòng điện quy ước là chiều chuyển động của hạt mang điện dương; electron mang điện âm nên trôi ngược chiều dòng điện.",
    "Phương án C ngược: ở mạch ngoài dòng điện đi từ cực dương sang cực âm; D sai vì quy ước chung cho mọi dây dẫn.", "Chọn B."])
mc("41-1", "trung-binh", "Dòng điện không đổi là dòng điện",
   ["có chiều không thay đổi theo thời gian.", "có chiều và cường độ không thay đổi theo thời gian.",
    "có cường độ không đổi nhưng chiều có thể thay đổi.", "có cường độ tăng đều theo thời gian."], 1,
   ["Dòng không đổi: cả chiều và cường độ đều không đổi. Dòng một chiều: chỉ cần chiều không đổi.",
    "Phương án A là định nghĩa dòng một chiều, chưa đủ cho dòng không đổi.", "Chọn B."])
tf("41-1", "trung-binh", "Khi sạc, bộ sạc cấp cho pin điện thoại một dòng điện luôn đi vào cực dương của pin, nhưng cường độ thay đổi trong khoảng từ $1{,}0\\ \\text{A}$ đến $2{,}0\\ \\text{A}$.",
   [("Dòng điện sạc là dòng điện một chiều.", True, "Chiều dòng điện không đổi nên đó là dòng một chiều."),
    ("Dòng điện sạc là dòng điện không đổi.", False, "Cường độ thay đổi từ $1{,}0\\ \\text{A}$ đến $2{,}0\\ \\text{A}$ nên không phải dòng không đổi."),
    ("Mọi dòng điện không đổi đều là dòng điện một chiều.", True, "Dòng không đổi có chiều không đổi nên luôn là dòng một chiều; điều ngược lại không đúng."),
    ("Muốn đo cường độ dòng sạc, ta mắc ampe kế song song với pin.", False, "Ampe kế phải mắc nối tiếp với pin để dòng sạc chạy qua nó, chứ không mắc song song.")])

# ---------- 42-2 Đường đặc trưng ----------
mc("42-2", "de", "Ở nhiệt độ không đổi, đường đặc trưng vôn – ampe (đồ thị $I$ theo $U$) của một điện trở thuần là",
   ["đường thẳng đi qua gốc toạ độ.", "đường cong đi qua gốc toạ độ.", "đường thẳng song song với trục $U$.", "đường thẳng song song với trục $I$."], 0,
   ["Điện trở thuần có $R=\\dfrac{U}{I}$ không đổi nên $I=\\dfrac{U}{R}$ tỉ lệ thuận với $U$: đồ thị là đường thẳng qua gốc toạ độ.",
    "Đường cong (B) là của linh kiện có điện trở thay đổi như đèn sợi đốt, điện trở nhiệt.", "Chọn A."])
mc("42-2", "trung-binh", "Đặt vào một linh kiện các hiệu điện thế $2{,}0\\ \\text{V}$; $4{,}0\\ \\text{V}$; $6{,}0\\ \\text{V}$ thì đo được cường độ dòng điện tương ứng $4{,}0\\ \\text{mA}$; $8{,}0\\ \\text{mA}$; $12{,}0\\ \\text{mA}$. Linh kiện này",
   ["là điện trở thuần có $R=0{,}5\\ \\text{k}\\Omega$.", "là điện trở thuần có $R=2\\ \\text{k}\\Omega$.",
    "là điện trở nhiệt NTC vì $I$ tăng khi $U$ tăng.", "là đèn sợi đốt vì điện trở tăng khi $U$ tăng."], 0,
   ["Tính $U/I$ ở từng lần đo (V/mA = kΩ): $\\dfrac{2{,}0}{4{,}0}=\\dfrac{4{,}0}{8{,}0}=\\dfrac{6{,}0}{12{,}0}=0{,}5\\ \\text{k}\\Omega$.",
    "$U/I$ không đổi nên đây là điện trở thuần, đường đặc trưng là đường thẳng qua gốc.",
    "Sai B vì lấy $I/U$; sai C vì $I$ tăng theo $U$ chưa đủ để kết luận, phải xét $U/I$; sai D vì $U/I$ không tăng.", "Chọn A."])
mc("42-2", "trung-binh", "Một điện trở nhiệt NTC nóng lên khi hiệu điện thế đặt vào nó tăng. Vẽ đồ thị $I$ theo $U$ ($I$ trên trục tung, $U$ trên trục hoành). Đồ thị có dạng",
   ["đường thẳng đi qua gốc toạ độ.", "đường cong đi qua gốc, càng về sau càng dốc lên.",
    "đường cong đi qua gốc, càng về sau càng thoải.", "đường nằm ngang."], 1,
   ["NTC nóng lên thì điện trở giảm; $I=\\dfrac{U}{R}$ với $R$ giảm dần nên $I$ tăng nhanh hơn tỉ lệ thuận.",
    "Đồ thị cong, độ dốc tăng dần khi $U$ tăng.",
    "Sai A vì $R$ không đổi mới cho đường thẳng; C là dạng của linh kiện có điện trở tăng khi nóng (đèn sợi đốt).", "Chọn B."])
tf("42-2", "trung-binh", "Đo hai linh kiện X và Y. X: $U=1{,}0\\ \\text{V}$ thì $I=10\\ \\text{mA}$; $U=3{,}0\\ \\text{V}$ thì $I=30\\ \\text{mA}$; $U=5{,}0\\ \\text{V}$ thì $I=50\\ \\text{mA}$. Y: $U=1{,}0\\ \\text{V}$ thì $I=10\\ \\text{mA}$; $U=3{,}0\\ \\text{V}$ thì $I=40\\ \\text{mA}$; $U=5{,}0\\ \\text{V}$ thì $I=90\\ \\text{mA}$.",
   [("X là điện trở thuần có điện trở $100\\ \\Omega$.", True, "$\\dfrac{U}{I}=\\dfrac{1{,}0}{0{,}010}=\\dfrac{3{,}0}{0{,}030}=\\dfrac{5{,}0}{0{,}050}=100\\ \\Omega$, không đổi."),
    ("Điện trở của Y tăng khi hiệu điện thế tăng.", False, "$\\dfrac{U}{I}$ của Y lần lượt là $100\\ \\Omega$; $75\\ \\Omega$; khoảng $56\\ \\Omega$: điện trở giảm, chứ không tăng."),
    ("Y có thể là một điện trở nhiệt NTC.", True, "Điện trở của Y giảm khi $U$ tăng (linh kiện nóng lên), đúng đặc điểm của NTC."),
    ("Vì cường độ dòng điện qua Y tăng theo hiệu điện thế nên đường đặc trưng của Y là đường thẳng qua gốc.", False, "Đường thẳng qua gốc đòi hỏi $U/I$ không đổi; $U/I$ của Y thay đổi nên đường đặc trưng của Y là đường cong.")])

# ---------- 46-1 Vi mô – vĩ mô, lĩnh vực (cần 2) ----------
mc("46-1", "de", "Đối tượng nào sau đây thuộc cấp độ vi mô?",
   ["Trái Đất.", "Electron.", "Chiếc xe đạp.", "Quả bóng đá."], 1,
   ["Vi mô là những đối tượng mắt thường không nhìn thấy được như nguyên tử, phân tử, electron; vĩ mô là những đối tượng mắt thường nhìn thấy được.",
    "Trái Đất, xe đạp, quả bóng đều nhìn thấy được nên thuộc vĩ mô.", "Chọn B."])
mc("46-1", "de", "Ứng dụng nào sau đây của Vật lí thuộc lĩnh vực y tế?",
   ["Chụp X-quang để chẩn đoán gãy xương.", "Cáp quang truyền tín hiệu internet.", "Robot hàn trong dây chuyền lắp ráp ô tô.", "Hệ thống tưới nhỏ giọt tự động cho cây trồng."], 0,
   ["Chụp X-quang dùng tia X để chẩn đoán bệnh: lĩnh vực y tế.",
    "Cáp quang thuộc thông tin liên lạc; robot hàn thuộc công nghiệp; tưới nhỏ giọt thuộc nông nghiệp.", "Chọn A."])

# ---------- 46-3 Quy trình 5 bước ----------
mc("46-3", "trung-binh", "Lan thấy nước trong chai nhựa để trong ngăn đá bị đông làm chai phồng lên. Lan hỏi: “Vì sao chai lại phồng?” rồi đoán: “Có lẽ nước nở ra khi đông đặc.” Ngay sau đó Lan ghi vào vở: “Kết luận: nước nở ra khi đông đặc.” Lan đã bỏ qua bước nào của phương pháp thực nghiệm?",
   ["Kiểm tra giả thuyết.", "Quan sát.", "Đặt vấn đề.", "Đưa ra giả thuyết."], 0,
   ["Quy trình: quan sát → đặt vấn đề → đưa ra giả thuyết → kiểm tra giả thuyết → kết luận.",
    "Lan đã quan sát (chai phồng), đặt vấn đề (“Vì sao…?”), đưa ra giả thuyết (“Có lẽ…”), nhưng chưa làm thí nghiệm nào đã viết kết luận: thiếu bước kiểm tra giả thuyết.",
    "Một lời đoán chưa được kiểm tra thì chưa thể thành kết luận.", "Chọn A."])
mc("46-3", "trung-binh", "Nam thấy quả bóng bơm căng để ngoài nắng gắt thì bị nổ. Nam hỏi: “Vì sao bóng để ngoài nắng lại nổ?” rồi nói: “Có lẽ khi nóng lên, áp suất khí trong bóng tăng.” Câu nói sau của Nam thuộc bước nào của phương pháp thực nghiệm?",
   ["Quan sát.", "Đặt vấn đề.", "Đưa ra giả thuyết.", "Kết luận."], 2,
   ["Giả thuyết là lời đoán về nguyên nhân, chưa được kiểm tra.",
    "Câu “Có lẽ khi nóng lên, áp suất khí trong bóng tăng” là lời đoán nguyên nhân nên là giả thuyết.",
    "Việc thấy bóng nổ là quan sát; câu hỏi “Vì sao…?” là đặt vấn đề; chưa có thí nghiệm nên chưa thể là kết luận.", "Chọn C."])
mc("46-3", "kho", "Một nhóm đo thời gian rơi của hai viên bi khác khối lượng từ cùng một độ cao, mỗi bi đo $3$ lần, sai số mỗi lần đo $\\pm0{,}02\\ \\text{s}$. Bi nhẹ: $0{,}45\\ \\text{s}$; $0{,}46\\ \\text{s}$; $0{,}44\\ \\text{s}$. Bi nặng: $0{,}46\\ \\text{s}$; $0{,}44\\ \\text{s}$; $0{,}45\\ \\text{s}$. Kết luận nào phù hợp với số liệu?",
   ["Bi nặng rơi nhanh hơn bi nhẹ.", "Trong điều kiện thí nghiệm, thời gian rơi của hai bi như nhau trong phạm vi sai số.",
    "Bi nhẹ rơi nhanh hơn bi nặng.", "Không rút ra được kết luận nào vì các lần đo không giống nhau."], 1,
   ["Thời gian trung bình: bi nhẹ $\\dfrac{0{,}45+0{,}46+0{,}44}{3}=0{,}45\\ \\text{s}$; bi nặng $\\dfrac{0{,}46+0{,}44+0{,}45}{3}=0{,}45\\ \\text{s}$.",
    "Chênh lệch $0\\ \\text{s}$, nhỏ hơn sai số $0{,}02\\ \\text{s}$: không phát hiện được khác biệt nào vượt quá sai số giữa hai bi.",
    "Sai A, C vì kết luận ngược số liệu; sai D vì các lần đo dao động trong phạm vi sai số là bình thường.", "Chọn B."])
tf("46-3", "kho", "Minh thấy con lắc dây dài dao động chậm hơn con lắc dây ngắn. Minh nói: “Chu kì con lắc tăng khi chiều dài dây tăng.” Minh đo chu kì, mỗi dây $3$ lần, sai số mỗi lần $\\pm0{,}05\\ \\text{s}$. Dây $0{,}25\\ \\text{m}$: $1{,}00\\ \\text{s}$; $1{,}02\\ \\text{s}$; $0{,}98\\ \\text{s}$. Dây $1{,}00\\ \\text{m}$: $2{,}01\\ \\text{s}$; $1{,}99\\ \\text{s}$; $2{,}00\\ \\text{s}$.",
   [("Câu “Chu kì con lắc tăng khi chiều dài dây tăng” là giả thuyết của Minh.", True, "Đó là lời đoán, chưa được kiểm tra bằng thí nghiệm."),
    ("Chu kì trung bình của hai con lắc chênh nhau $1{,}00\\ \\text{s}$.", True, "Trung bình: $\\dfrac{1{,}00+1{,}02+0{,}98}{3}=1{,}00\\ \\text{s}$ và $\\dfrac{2{,}01+1{,}99+2{,}00}{3}=2{,}00\\ \\text{s}$, chênh $1{,}00\\ \\text{s}$."),
    ("Chênh lệch đó nhỏ hơn sai số nên chưa kết luận được.", False, "Chênh lệch $1{,}00\\ \\text{s}$ lớn hơn nhiều so với sai số $0{,}05\\ \\text{s}$, nên khác biệt là thật và giả thuyết được ủng hộ."),
    ("Từ số liệu có thể kết luận chu kì tỉ lệ thuận với chiều dài dây.", False, "Chiều dài tăng $4$ lần nhưng chu kì chỉ tăng $2$ lần, nên không tỉ lệ thuận; số liệu chỉ cho phép kết luận chu kì tăng khi chiều dài tăng.")])

# ---------- 47-1 Nhãn thiết bị ----------
mc("47-1", "de", "Trên một thiết bị điện, kí hiệu “AC” hoặc dấu “$\\sim$” cho biết",
   ["dòng điện xoay chiều.", "dòng điện một chiều.", "cực dương của thiết bị.", "đầu ra của thiết bị."], 0,
   ["AC (dấu $\\sim$) là dòng điện xoay chiều; DC là dòng điện một chiều.",
    "Cực dương ghi “+”; đầu ra ghi “Output”.", "Chọn A."])
mc("47-1", "de", "Trên nhãn của một bộ nguồn, chữ “Output” chỉ",
   ["đầu vào, nơi bộ nguồn nhận điện từ lưới điện.", "đầu ra, nơi bộ nguồn cấp điện cho thiết bị.", "công tắc bật – tắt của bộ nguồn.", "cầu chì bảo vệ của bộ nguồn."], 1,
   ["Output là đầu ra, cấp điện cho thiết bị; Input là đầu vào, nhận điện.",
    "Phương án A là ý nghĩa của Input.", "Chọn B."])
mc("47-1", "trung-binh", "Một bộ nguồn có nhãn: Input: 100–240 V AC, 50/60 Hz; Output: 12 V DC, 1 A. Thiết bị nào sau đây phù hợp để nối vào đầu Output?",
   ["Bóng đèn ghi 220 V AC.", "Dải đèn LED ghi 12 V DC.", "Quạt mini ghi 12 V AC.", "Động cơ nhỏ ghi 24 V DC."], 1,
   ["Thiết bị phải khớp cả loại dòng và số vôn với đầu Output: một chiều (DC), $12\\ \\text{V}$.",
    "Dải LED 12 V DC khớp cả hai.",
    "Bóng đèn 220 V AC và quạt 12 V AC cần dòng xoay chiều; động cơ 24 V DC cần điện áp lớn hơn đầu Output cấp.", "Chọn B."])
tf("47-1", "de", "Một viên pin có hai đầu, một đầu ghi “+”, đầu kia ghi “−”. Dùng đồng hồ đo điện đa năng có dây đo màu đỏ để đo điện áp của pin.",
   [("Đầu ghi “+” là cực dương của pin.", True, "Kí hiệu “+” chỉ cực dương, “−” chỉ cực âm."),
    ("Dây đo màu đỏ của đồng hồ được nối với cực âm của pin.", False, "Dây đỏ là dây dương, nối với cực “+” của pin, chứ không nối với cực âm."),
    ("Khi đo điện áp của pin, phải chọn thang đo có kí hiệu DC trên đồng hồ.", True, "Pin cấp dòng điện một chiều nên dùng thang đo một chiều (DC)."),
    ("Ổ cắm điện trong nhà cấp dòng điện một chiều (DC).", False, "Lưới điện trong nhà cấp dòng điện xoay chiều (AC), chứ không phải một chiều.")])

# ---------- 47-2 Kí hiệu cảnh báo ----------
mc("47-2", "de", "Một kí hiệu hình tam giác nền vàng, bên trong vẽ tia sét màu đen. Kí hiệu này thuộc nhóm nào?",
   ["Cảnh báo (nguy hiểm về điện).", "Cấm.", "Bắt buộc phải làm.", "Bảo quản."], 0,
   ["Đọc hình dạng và màu trước: hình tam giác là nhóm cảnh báo.",
    "Hình tia sét bên trong cho biết nguy hiểm về điện.", "Nhóm cấm là hình tròn viền đỏ gạch chéo; nhóm bắt buộc là hình tròn nền xanh.", "Chọn A."])
mc("47-2", "de", "Một kí hiệu hình tròn viền đỏ có gạch chéo, bên trong vẽ ngọn lửa. Kí hiệu này có nghĩa là",
   ["cấm lửa, không được đốt lửa hay mang lửa vào.", "cảnh báo có chất dễ cháy.", "bắt buộc phải mang theo bình cứu hoả.", "nơi đặt bình cứu hoả."], 0,
   ["Hình tròn viền đỏ có gạch chéo là nhóm cấm: không được làm việc vẽ bên trong.",
    "Ngọn lửa bên trong nên kí hiệu là cấm lửa.", "Cảnh báo chất dễ cháy (B) là hình tam giác có ngọn lửa.", "Chọn A."])
mc("47-2", "trung-binh", "Trước cửa phòng thực hành có một kí hiệu hình tròn nền xanh, bên trong vẽ chiếc kính bảo hộ. Học sinh cần làm gì?",
   ["Đeo kính bảo hộ trước khi vào làm thí nghiệm.", "Không được đeo kính khi vào phòng.", "Cẩn thận vì trong phòng có kính vỡ.", "Chỉ đeo kính bảo hộ nếu thí nghiệm kéo dài."], 0,
   ["Hình tròn nền xanh là nhóm bắt buộc: phải làm điều được vẽ bên trong trước khi tiếp xúc.",
    "Bên trong là kính bảo hộ nên phải đeo kính bảo hộ trước khi làm thí nghiệm.",
    "Phương án B hiểu thành kí hiệu cấm; C hiểu thành kí hiệu cảnh báo; D bỏ qua tính bắt buộc.", "Chọn A."])
tf("47-2", "trung-binh", "Một tủ hoá chất dán ba kí hiệu: (1) tam giác nền vàng, bên trong có ngọn lửa; (2) hình tròn viền đỏ có gạch chéo, bên trong có bàn tay; (3) hình tròn nền xanh, bên trong có đôi găng tay.",
   [("Kí hiệu (1) cảnh báo trong tủ có chất dễ cháy.", True, "Tam giác là nhóm cảnh báo; ngọn lửa cho biết chất dễ cháy."),
    ("Kí hiệu (2) yêu cầu phải dùng tay chạm vào để kiểm tra.", False, "Hình tròn viền đỏ có gạch chéo là nhóm cấm: cấm chạm tay, chứ không phải yêu cầu chạm tay."),
    ("Kí hiệu (3) yêu cầu đeo găng tay trước khi lấy hoá chất.", True, "Hình tròn nền xanh là nhóm bắt buộc; bên trong là găng tay nên phải đeo găng tay."),
    ("Cả ba kí hiệu đều thuộc nhóm cảnh báo vì cùng dán trên tủ hoá chất.", False, "Nhóm được xác định bằng hình dạng và màu: (1) cảnh báo, (2) cấm, (3) bắt buộc, chứ không cùng một nhóm.")])

# ---------- 68-1 Chuyển hoá, bảo toàn năng lượng ----------
mc("68-1", "de", "Mỗi giây, một bóng đèn LED nhận $10\\ \\text{J}$ điện năng và phát ra $4\\ \\text{J}$ năng lượng ánh sáng; phần còn lại chuyển thành nhiệt năng. Mỗi giây có bao nhiêu điện năng chuyển thành nhiệt năng?",
   ["$6\\ \\text{J}$.", "$14\\ \\text{J}$.", "$4\\ \\text{J}$.", "$2{,}5\\ \\text{J}$."], 0,
   ["Theo định luật bảo toàn năng lượng, điện năng nhận vào bằng tổng năng lượng ánh sáng và nhiệt năng: $W_{\\text{nhiệt}}=W_{\\text{điện}}-W_{\\text{sáng}}=10-4=6\\ \\text{J}$.",
    "Sai B vì cộng thay vì trừ; sai D vì lấy $10:4$.", "Chọn A."])
mc("68-1", "de", "Khi quạt điện hoạt động, điện năng chủ yếu chuyển hoá thành",
   ["động năng của cánh quạt, một phần thành nhiệt năng và năng lượng âm thanh.", "hoá năng.", "quang năng.", "chỉ nhiệt năng."], 0,
   ["Quạt dùng điện năng để làm quay cánh (động năng); động cơ nóng lên và phát tiếng ồn là phần nhiệt năng, âm thanh.",
    "Quạt không tích hoá năng hay phát ánh sáng; D bỏ qua phần có ích là động năng.", "Chọn A."])
mc("68-1", "trung-binh", "Mỗi giây, pin của một ô tô đồ chơi cung cấp $5{,}0\\ \\text{J}$; bánh xe nhận $3{,}5\\ \\text{J}$ động năng có ích, phần còn lại toả ra dưới dạng nhiệt và âm thanh. Xe chạy liên tục $60\\ \\text{s}$. Phần năng lượng toả ra dưới dạng nhiệt và âm thanh trong thời gian đó là",
   ["$90\\ \\text{J}$.", "$210\\ \\text{J}$.", "$300\\ \\text{J}$.", "$1{,}5\\ \\text{J}$."], 0,
   ["Bảo toàn năng lượng: mỗi giây phần toả ra là $5{,}0-3{,}5=1{,}5\\ \\text{J}$.",
    "Trong $60\\ \\text{s}$: $W=1{,}5\\cdot60=90\\ \\text{J}$.",
    "Sai B vì đó là phần có ích $3{,}5\\cdot60$; sai C vì đó là toàn bộ năng lượng pin cấp; sai D vì chỉ tính cho $1\\ \\text{s}$.", "Chọn A."])
tf("68-1", "trung-binh", "Thả một quả bóng từ độ cao $h$ xuống sàn. Bóng nảy lên nhưng không trở lại được độ cao ban đầu. Chọn mốc thế năng tại sàn.",
   [("Khi bóng rơi, thế năng của bóng chuyển hoá dần thành động năng.", True, "Độ cao giảm, tốc độ tăng: thế năng chuyển thành động năng."),
    ("Bóng không trở lại độ cao cũ chứng tỏ một phần năng lượng đã mất đi hoàn toàn.", False, "Năng lượng không tự mất đi; phần thiếu hụt đã chuyển thành nhiệt năng và âm thanh truyền ra sàn, không khí."),
    ("Tổng năng lượng của bóng và môi trường xung quanh được bảo toàn.", True, "Theo định luật bảo toàn năng lượng, năng lượng chỉ chuyển hoá từ dạng này sang dạng khác."),
    ("Ban đầu bóng có thế năng $2{,}0\\ \\text{J}$, ở điểm cao nhất sau lần nảy đầu bóng có thế năng $1{,}6\\ \\text{J}$; phần năng lượng đã chuyển thành dạng khác là $0{,}4\\ \\text{J}$.", True, "Ở hai điểm cao nhất bóng có động năng bằng $0$, nên phần chuyển thành nhiệt và âm là $2{,}0-1{,}6=0{,}4\\ \\text{J}$.")])

# ---------- 74-3 Va chạm mềm / đàn hồi (cần 2) ----------
mc("74-3", "de", "Trong một va chạm mềm (hai vật dính vào nhau sau va chạm) của hệ kín, đại lượng nào được bảo toàn?",
   ["Động lượng của hệ được bảo toàn, động năng của hệ giảm.", "Cả động lượng và động năng của hệ đều được bảo toàn.",
    "Động lượng của hệ giảm, động năng của hệ được bảo toàn.", "Cả động lượng và động năng của hệ đều giảm."], 0,
   ["Với hệ kín, động lượng luôn bảo toàn trong mọi loại va chạm.",
    "Trong va chạm mềm, một phần động năng chuyển thành nhiệt năng và năng lượng biến dạng nên động năng của hệ giảm.",
    "Phương án B là va chạm đàn hồi; C, D sai vì động lượng của hệ kín không giảm.", "Chọn A."])
tf("74-3", "trung-binh", "Trên đường ray đệm khí, xe 1 khối lượng $0{,}20\\ \\text{kg}$ chạy với tốc độ $1{,}0\\ \\text{m/s}$ tới va vào xe 2 khối lượng $0{,}20\\ \\text{kg}$ đang đứng yên. Sau va chạm hai xe tách nhau: xe 1 đứng yên, xe 2 chạy theo chiều ban đầu của xe 1 với tốc độ $1{,}0\\ \\text{m/s}$.",
   [("Tổng động lượng của hệ được bảo toàn.", True, "$p_{\\text{trước}}=m_1v_1=0{,}20\\cdot1{,}0=0{,}20\\ \\text{kg·m/s}$; $p_{\\text{sau}}=m_2v_2'=0{,}20\\cdot1{,}0=0{,}20\\ \\text{kg·m/s}$."),
    ("Tổng động năng của hệ được bảo toàn.", True, "$W_{\\text{trước}}=\\dfrac12m_1v_1^2=\\dfrac12\\cdot0{,}20\\cdot1{,}0^2=0{,}10\\ \\text{J}$; $W_{\\text{sau}}=\\dfrac12\\cdot0{,}20\\cdot1{,}0^2=0{,}10\\ \\text{J}$."),
    ("Va chạm này là va chạm mềm.", False, "Hai xe tách nhau và động năng bảo toàn nên đây là va chạm đàn hồi, chứ không phải va chạm mềm."),
    ("Nếu hai xe dính vào nhau sau va chạm (cùng điều kiện đầu) thì động năng của hệ ngay sau va chạm là $0{,}05\\ \\text{J}$.", True, "Vận tốc chung $v=\\dfrac{m_1v_1}{m_1+m_2}=\\dfrac{0{,}20}{0{,}40}=0{,}5\\ \\text{m/s}$; $W=\\dfrac12\\cdot0{,}40\\cdot0{,}5^2=0{,}05\\ \\text{J}$.")])

# ---------- 76-1 Chuyển động tròn đều ----------
mc("76-1", "de", "Chuyển động tròn đều là chuyển động có",
   ["quỹ đạo là đường tròn và tốc độ không đổi.", "quỹ đạo là đường tròn và vectơ vận tốc không đổi.",
    "quỹ đạo là đường thẳng và tốc độ không đổi.", "quỹ đạo là đường tròn và tốc độ tăng đều."], 0,
   ["Chuyển động tròn đều có quỹ đạo tròn và tốc độ (độ lớn vận tốc) không đổi.",
    "Phương án B sai vì hướng của vectơ vận tốc thay đổi liên tục.", "Chọn A."])
mc("76-1", "de", "Trong chuyển động tròn đều, vectơ vận tốc của vật có",
   ["phương tiếp tuyến với quỹ đạo, chiều theo chiều chuyển động.", "phương trùng bán kính, chiều hướng vào tâm.",
    "phương trùng bán kính, chiều hướng ra xa tâm.", "hướng không đổi trong suốt chuyển động."], 0,
   ["Vectơ vận tốc tại mỗi điểm có phương tiếp tuyến với quỹ đạo, chiều theo chiều chuyển động, độ lớn bằng tốc độ.",
    "Phương án B là hướng của gia tốc hướng tâm; D sai vì hướng vận tốc đổi liên tục.", "Chọn A."])
mc("76-1", "trung-binh", "Một vật chuyển động tròn đều trên quỹ đạo bán kính $2{,}0\\ \\text{m}$ với tốc độ $0{,}50\\ \\text{m/s}$. Sau $8{,}0\\ \\text{s}$, độ dịch chuyển góc của vật là",
   ["$2{,}0\\ \\text{rad}$.", "$4{,}0\\ \\text{rad}$.", "$8{,}0\\ \\text{rad}$.", "$0{,}50\\ \\text{rad}$."], 0,
   ["Tốc độ không đổi nên cung đi được $s=vt=0{,}50\\cdot8{,}0=4{,}0\\ \\text{m}$.",
    "Độ dịch chuyển góc $\\theta=\\dfrac{s}{r}=\\dfrac{4{,}0}{2{,}0}=2{,}0\\ \\text{rad}$.",
    "Sai B vì lấy độ dài cung làm góc; sai C vì nhân $s$ với $r$.", "Chọn A."])
tf("76-1", "trung-binh", "Đầu kim giây của một đồng hồ chạy đúng chuyển động tròn đều, quay một vòng trong $60\\ \\text{s}$.",
   [("Tốc độ của đầu kim giây không đổi.", True, "Chuyển động tròn đều có tốc độ không đổi."),
    ("Vận tốc của đầu kim giây không đổi.", False, "Độ lớn vận tốc không đổi nhưng hướng (tiếp tuyến) đổi liên tục, nên vận tốc thay đổi."),
    ("Sau $15\\ \\text{s}$, độ dịch chuyển góc của kim giây là $\\dfrac{\\pi}{2}\\ \\text{rad}$.", True, "$15\\ \\text{s}$ là $\\dfrac14$ vòng: $\\theta=\\dfrac{2\\pi}{4}=\\dfrac{\\pi}{2}\\ \\text{rad}$."),
    ("Sau $60\\ \\text{s}$, độ dịch chuyển góc của kim giây là $\\pi\\ \\text{rad}$.", False, "$60\\ \\text{s}$ là một vòng: $\\theta=2\\pi\\ \\text{rad}$, chứ không phải $\\pi\\ \\text{rad}$.")])

# ---------- 77-1 Gia tốc hướng tâm ----------
mc("77-1", "de", "Vật chuyển động tròn đều có gia tốc vì",
   ["hướng của vectơ vận tốc thay đổi liên tục.", "độ lớn của vận tốc thay đổi liên tục.", "vật luôn chịu lực ma sát.", "quãng đường vật đi được tăng dần."], 0,
   ["Gia tốc đo sự thay đổi của vận tốc, cả độ lớn lẫn hướng.",
    "Trong chuyển động tròn đều độ lớn vận tốc không đổi nhưng hướng đổi liên tục, nên vật có gia tốc (gia tốc hướng tâm).", "Phương án B mâu thuẫn với tốc độ không đổi.", "Chọn A."])
mc("77-1", "de", "Gia tốc hướng tâm của vật chuyển động tròn đều có",
   ["phương trùng bán kính, chiều hướng vào tâm quỹ đạo.", "phương tiếp tuyến với quỹ đạo.", "phương trùng bán kính, chiều hướng ra xa tâm.", "cùng hướng với vectơ vận tốc."], 0,
   ["Gia tốc hướng tâm có gốc tại vật, phương trùng bán kính, chiều hướng vào tâm.",
    "Phương án B, D là hướng của vận tốc.", "Chọn A."])
mc("77-1", "trung-binh", "Một vật chuyển động tròn đều trên quỹ đạo bán kính $1{,}5\\ \\text{m}$ với tốc độ $3{,}0\\ \\text{m/s}$. Độ lớn gia tốc hướng tâm của vật là",
   ["$2{,}0\\ \\text{m/s}^2$.", "$4{,}5\\ \\text{m/s}^2$.", "$6{,}0\\ \\text{m/s}^2$.", "$13{,}5\\ \\text{m/s}^2$."], 2,
   ["Chuyển động tròn đều: $a_{\\text{ht}}=\\dfrac{v^2}{r}=\\dfrac{3{,}0^2}{1{,}5}=6{,}0\\ \\text{m/s}^2$.",
    "Sai A vì lấy $\\dfrac{v}{r}$; sai B vì lấy $v\\cdot r$; sai D vì lấy $v^2 r$.", "Chọn C."])
tf("77-1", "trung-binh", "Một vệ tinh chuyển động tròn đều quanh Trái Đất.",
   [("Độ lớn vận tốc của vệ tinh không đổi.", True, "Chuyển động tròn đều có tốc độ không đổi."),
    ("Vệ tinh không có gia tốc vì tốc độ của nó không đổi.", False, "Hướng vận tốc đổi liên tục nên vệ tinh có gia tốc hướng tâm, chứ không phải không có gia tốc."),
    ("Gia tốc của vệ tinh luôn hướng về tâm Trái Đất.", True, "Tâm quỹ đạo là tâm Trái Đất; gia tốc hướng tâm hướng vào tâm quỹ đạo."),
    ("Vectơ vận tốc của vệ tinh tại hai điểm ở hai đầu một đường kính quỹ đạo có cùng hướng.", False, "Tại hai đầu một đường kính, hai tiếp tuyến song song nhưng vận tốc ngược hướng nhau.")])

# ---------- 78-1 Biến dạng ----------
mc("78-1", "de", "Kéo giãn một lò xo rồi thôi tác dụng lực, lò xo trở về đúng chiều dài ban đầu. Biến dạng của lò xo là",
   ["biến dạng đàn hồi.", "biến dạng dẻo.", "biến dạng nén.", "không phải biến dạng."], 0,
   ["Thôi lực mà vật trở lại hình dạng, kích thước ban đầu là biến dạng đàn hồi.",
    "Biến dạng dẻo là khi thôi lực vật không trở lại như cũ; lò xo bị kéo dài ra là biến dạng kéo chứ không phải nén.", "Chọn A."])
mc("78-1", "de", "Một cột nhà chịu trọng lượng của mái nhà đè từ trên xuống. Cột nhà bị",
   ["biến dạng nén.", "biến dạng kéo.", "biến dạng dẻo.", "không biến dạng."], 0,
   ["Cặp lực tác dụng lên cột (mái đè xuống, nền đỡ lên) hướng vào trong cột, làm cột ngắn lại: biến dạng nén.",
    "Biến dạng kéo khi cặp lực hướng ra ngoài vật; dẻo chỉ xét sau khi thôi lực.", "Chọn A."])
mc("78-1", "trung-binh", "Một lò xo có chiều dài tự nhiên $15\\ \\text{cm}$. Lần lượt kéo lò xo bằng các lực $3\\ \\text{N}$; $6\\ \\text{N}$; $9\\ \\text{N}$ thì chiều dài khi có lực là $18\\ \\text{cm}$; $21\\ \\text{cm}$; $25\\ \\text{cm}$, còn chiều dài sau khi thôi lực là $15\\ \\text{cm}$; $15\\ \\text{cm}$; $16\\ \\text{cm}$. Kết luận nào đúng?",
   ["Ở lực $9\\ \\text{N}$ lò xo bị biến dạng dẻo; giới hạn đàn hồi nằm trong khoảng từ $6\\ \\text{N}$ đến $9\\ \\text{N}$.", "Ở lực $6\\ \\text{N}$ lò xo đã bị biến dạng dẻo.",
    "Giới hạn đàn hồi của lò xo đúng bằng $9\\ \\text{N}$.", "Lò xo bị biến dạng nén ở cả ba lần thử."], 0,
   ["Đàn hồi hay dẻo xét sau khi thôi lực, so với $l_0=15\\ \\text{cm}$: với $3\\ \\text{N}$ và $6\\ \\text{N}$ lò xo trở về $15\\ \\text{cm}$ (đàn hồi); với $9\\ \\text{N}$ còn $16\\ \\text{cm}$ (dẻo).",
    "Lực lớn nhất còn đàn hồi trong các lần thử là $6\\ \\text{N}$, ở $9\\ \\text{N}$ đã vượt giới hạn, nên giới hạn đàn hồi nằm trong khoảng $6\\ \\text{N}$ đến $9\\ \\text{N}$.",
    "Sai B vì ở $6\\ \\text{N}$ lò xo vẫn trở về $15\\ \\text{cm}$; sai C vì ở $9\\ \\text{N}$ đã dẻo; sai D vì lực kéo làm lò xo dài ra.", "Chọn A."])
tf("78-1", "de", "Uốn cong một đoạn dây đồng thành hình chiếc móc rồi thả tay ra, đoạn dây vẫn giữ nguyên hình chiếc móc.",
   [("Đoạn dây đồng đã bị biến dạng dẻo.", True, "Thôi lực mà dây không trở lại hình dạng ban đầu là biến dạng dẻo."),
    ("Lực uốn đã vượt quá giới hạn đàn hồi của đoạn dây.", True, "Vượt giới hạn đàn hồi thì biến dạng trở thành dẻo."),
    ("Biến dạng nén là biến dạng làm vật dài ra.", False, "Biến dạng nén làm vật ngắn lại; biến dạng làm vật dài ra là biến dạng kéo."),
    ("Vật biến dạng đàn hồi thì khi thôi lực sẽ trở lại hình dạng và kích thước ban đầu.", True, "Đây là định nghĩa biến dạng đàn hồi.")])

# ---------- 161-2 Ròng rọc cố định, đòn bẩy ----------
mc("161-2", "de", "Dùng một ròng rọc cố định kéo đều một vật có trọng lượng $400\\ \\text{N}$ lên cao. Bỏ qua ma sát và khối lượng dây, ròng rọc. Lực kéo và tác dụng của ròng rọc là",
   ["$F=400\\ \\text{N}$; ròng rọc chỉ làm đổi hướng của lực.", "$F=200\\ \\text{N}$; ròng rọc cho lợi hai lần về lực.",
    "$F=800\\ \\text{N}$; ròng rọc làm thiệt hai lần về lực.", "$F=400\\ \\text{N}$; ròng rọc cho lợi về đường đi."], 0,
   ["Ròng rọc cố định chỉ đổi hướng của lực: $F=P=400\\ \\text{N}$ và đường đi của dây bằng độ cao nâng vật.",
    "Phương án B là tác dụng của ròng rọc động; D sai vì không lợi về lực cũng không lợi về đường đi.", "Chọn A."])
mc("161-2", "de", "Phát biểu nào sau đây là nội dung định luật về công?",
   ["Không một máy cơ đơn giản nào cho lợi về công; được lợi bao nhiêu lần về lực thì thiệt bấy nhiêu lần về đường đi.",
    "Máy cơ đơn giản cho lợi về công; được lợi bao nhiêu lần về lực thì lợi bấy nhiêu lần về đường đi.",
    "Máy cơ đơn giản cho lợi cả về lực lẫn về đường đi.", "Được lợi bao nhiêu lần về đường đi thì được lợi bấy nhiêu lần về công."], 0,
   ["Định luật về công: máy cơ đơn giản đổi lực lấy đường đi, nhưng công không đổi (bỏ qua ma sát).",
    "Các phương án còn lại đều cho rằng có thể lợi về công.", "Chọn A."])
mc("161-2", "trung-binh", "Một đòn bẩy có khoảng cách từ điểm tựa tới điểm treo vật là $0{,}25\\ \\text{m}$, tới điểm đặt lực là $1{,}0\\ \\text{m}$. Dùng đòn bẩy nâng vật có trọng lượng $800\\ \\text{N}$ lên cao $4\\ \\text{cm}$. Bỏ qua ma sát và khối lượng đòn bẩy. Lực tác dụng và quãng đường điểm đặt lực đi được là",
   ["$200\\ \\text{N}$ và $16\\ \\text{cm}$.", "$200\\ \\text{N}$ và $1\\ \\text{cm}$.", "$3200\\ \\text{N}$ và $1\\ \\text{cm}$.", "$800\\ \\text{N}$ và $4\\ \\text{cm}$."], 0,
   ["Điều kiện cân bằng đòn bẩy: $F\\,l_2=P\\,l_1$, nên $F=\\dfrac{P\\,l_1}{l_2}=\\dfrac{800\\cdot0{,}25}{1{,}0}=200\\ \\text{N}$.",
    "Lợi $4$ lần về lực thì thiệt $4$ lần về đường đi: $s=4\\cdot4=16\\ \\text{cm}$.",
    "Sai B vì cho cả lực lẫn đường đi cùng giảm (trái định luật về công); sai C vì đảo $l_1$, $l_2$.", "Chọn A."])
tf("161-2", "trung-binh", "Bỏ qua ma sát và khối lượng của dây, ròng rọc, đòn bẩy. Dùng ròng rọc cố định đưa một vật trọng lượng $300\\ \\text{N}$ lên cao $3\\ \\text{m}$. Dùng một đòn bẩy có khoảng cách từ điểm tựa tới vật $0{,}3\\ \\text{m}$, tới điểm đặt lực $0{,}9\\ \\text{m}$ để nâng một vật khác trọng lượng $300\\ \\text{N}$ lên cao $0{,}1\\ \\text{m}$.",
   [("Công của lực kéo khi dùng ròng rọc cố định là $900\\ \\text{J}$.", True, "Ròng rọc cố định: $F=P$, $s=h$ nên $A=P\\,h=300\\cdot3=900\\ \\text{J}$."),
    ("Lực tác dụng lên đòn bẩy là $100\\ \\text{N}$.", True, "$F=\\dfrac{P\\,l_1}{l_2}=\\dfrac{300\\cdot0{,}3}{0{,}9}=100\\ \\text{N}$."),
    ("Điểm đặt lực trên đòn bẩy dịch chuyển $0{,}1\\ \\text{m}$.", False, "Lợi $3$ lần về lực thì thiệt $3$ lần về đường đi: $s=3\\cdot0{,}1=0{,}3\\ \\text{m}$, chứ không phải $0{,}1\\ \\text{m}$."),
    ("Công của lực tác dụng lên đòn bẩy nhỏ hơn $3$ lần công nâng vật trực tiếp.", False, "$A=F\\,s=100\\cdot0{,}3=30\\ \\text{J}$, bằng công nâng trực tiếp $P\\,h=300\\cdot0{,}1=30\\ \\text{J}$: không máy nào cho lợi về công.")])

# ---------- 150-2 Tần số, độ cao, độ to (cần 3) ----------
mc("150-2", "de", "Một nguồn âm thực hiện $600$ dao động trong $2\\ \\text{s}$. Tần số của âm và khả năng nghe của tai người là",
   ["$300\\ \\text{Hz}$; tai người nghe được.", "$1200\\ \\text{Hz}$; tai người nghe được.", "$300\\ \\text{Hz}$; là hạ âm.", "$300\\ \\text{Hz}$; là siêu âm."], 0,
   ["Tần số là số dao động trong $1\\ \\text{s}$: $f=\\dfrac{N}{t}=\\dfrac{600}{2}=300\\ \\text{Hz}$.",
    "Tai người nghe được âm từ $20\\ \\text{Hz}$ đến $20\\,000\\ \\text{Hz}$ nên nghe được âm này.",
    "Sai B vì nhân thay vì chia; C, D sai vì $300\\ \\text{Hz}$ nằm trong ngưỡng nghe.", "Chọn A."])
mc("150-2", "trung-binh", "Trên màn hình dao động kí, cùng một thang đo cho hai âm: đồ thị âm A có một chu kì chiếm $4$ ô theo trục ngang, biên độ $2$ ô theo trục dọc; đồ thị âm B có một chu kì chiếm $2$ ô, biên độ $3$ ô. Phát biểu nào đúng?",
   ["Âm B cao hơn và to hơn âm A.", "Âm A cao hơn, âm B to hơn.", "Âm A cao hơn và to hơn âm B.", "Âm B cao hơn, âm A to hơn."], 0,
   ["Chu kì của B ($2$ ô) ngắn hơn của A ($4$ ô) nên tần số của B lớn hơn: âm B cao hơn.",
    "Biên độ của B ($3$ ô) lớn hơn của A ($2$ ô) nên âm B to hơn.",
    "Sai B, C vì nhầm chu kì dài là âm cao; sai D vì nhầm biên độ.", "Chọn A."])
tf("150-2", "trung-binh", "Biết tai người nghe được âm có tần số từ $20\\ \\text{Hz}$ đến $20\\,000\\ \\text{Hz}$. Voi có thể giao tiếp bằng âm tần số khoảng $15\\ \\text{Hz}$; máy siêu âm y tế dùng sóng tần số $2\\ \\text{MHz}$.",
   [("Âm tần số $15\\ \\text{Hz}$ của voi là hạ âm.", True, "$15\\ \\text{Hz}\\lt20\\ \\text{Hz}$ nên là hạ âm."),
    ("Tai người nghe được sóng âm do máy siêu âm $2\\ \\text{MHz}$ phát ra.", False, "$2\\ \\text{MHz}=2\\,000\\,000\\ \\text{Hz}\\gt20\\,000\\ \\text{Hz}$ nên là siêu âm, tai người không nghe được."),
    ("Một màng loa dao động $3000$ lần trong $0{,}1\\ \\text{s}$ phát ra siêu âm.", True, "$f=\\dfrac{N}{t}=\\dfrac{3000}{0{,}1}=30\\,000\\ \\text{Hz}\\gt20\\,000\\ \\text{Hz}$: siêu âm."),
    ("Gảy dây đàn mạnh hơn thì âm phát ra cao hơn.", False, "Gảy mạnh làm biên độ lớn hơn nên âm to hơn, chứ không cao hơn; độ cao do tần số quyết định.")])

# ---------- 152-1 Dòng điện cảm ứng (định tính) ----------
mc("152-1", "de", "Trong cuộn dây dẫn kín xuất hiện dòng điện cảm ứng khi",
   ["số đường sức từ xuyên qua tiết diện của cuộn dây biến thiên.", "đặt một nam châm mạnh nằm yên trong lòng cuộn dây.",
    "từ trường xuyên qua cuộn dây rất mạnh.", "cuộn dây được làm bằng đồng."], 0,
   ["Điều kiện xuất hiện dòng điện cảm ứng: cuộn dây kín và số đường sức từ xuyên qua tiết diện của nó biến thiên.",
    "Phương án B, C: số đường sức không đổi thì không có dòng cảm ứng, dù từ trường mạnh.", "Chọn A."])
mc("152-1", "de", "Một nam châm thẳng đặt gần một cuộn dây dẫn kín, trục nam châm trùng trục cuộn dây. Trường hợp nào sau đây KHÔNG xuất hiện dòng điện cảm ứng trong cuộn dây?",
   ["Đưa nam châm lại gần cuộn dây.", "Kéo nam châm ra xa cuộn dây.", "Để nam châm nằm yên trong lòng cuộn dây.", "Quay nam châm quanh một trục vuông góc với trục cuộn dây."], 2,
   ["Nam châm nằm yên thì số đường sức xuyên qua tiết diện cuộn dây không đổi, nên không có dòng cảm ứng.",
    "Đưa lại gần, kéo ra xa hay quay nam châm quanh trục vuông góc với trục cuộn dây đều làm số đường sức xuyên qua cuộn dây thay đổi.", "Chọn C."])
mc("152-1", "trung-binh", "Đưa cực Bắc (N) của một nam châm thẳng lại gần đầu A của một cuộn dây dẫn kín. Theo định luật Lenz, đầu A của cuộn dây trở thành cực gì, và nhìn từ phía nam châm vào đầu A thì dòng điện cảm ứng chạy theo chiều nào?",
   ["Cực Bắc; ngược chiều kim đồng hồ.", "Cực Nam; ngược chiều kim đồng hồ.", "Cực Bắc; cùng chiều kim đồng hồ.", "Cực Nam; cùng chiều kim đồng hồ."], 0,
   ["Định luật Lenz: dòng cảm ứng sinh ra từ trường chống lại sự tăng số đường sức, nên đầu A đẩy nam châm lại: A là cực Bắc (cùng tên với cực N đang tiến lại).",
    "Quy tắc nắm tay phải: nhìn vào một đầu ống dây thấy dòng điện ngược chiều kim đồng hồ thì đầu đó là cực Bắc.",
    "Sai B, D vì khi đó cuộn dây hút nam châm lại, làm số đường sức tăng thêm; C ứng với đầu A là cực Nam.", "Chọn A."])
tf("152-1", "trung-binh", "Một nam châm điện đặt yên cạnh một cuộn dây dẫn kín; nam châm điện nối với nguồn điện một chiều qua công tắc K.",
   [("Ngay khi đóng K, trong cuộn dây xuất hiện dòng điện cảm ứng trong thời gian ngắn.", True, "Lúc đóng K, dòng điện trong nam châm điện tăng từ $0$, từ trường tăng nên số đường sức qua cuộn dây biến thiên."),
    ("Khi K đã đóng lâu và dòng điện trong nam châm điện ổn định, trong cuộn dây vẫn có dòng điện cảm ứng.", False, "Dòng điện ổn định thì từ trường không đổi, số đường sức qua cuộn dây không biến thiên nên không có dòng cảm ứng."),
    ("Ngay khi ngắt K, trong cuộn dây xuất hiện dòng điện cảm ứng.", True, "Lúc ngắt K, từ trường của nam châm điện giảm về $0$ nên số đường sức qua cuộn dây biến thiên."),
    ("Nếu thay bằng một nam châm thẳng có cực Bắc hướng vào một đầu cuộn dây rồi kéo nam châm ra xa, thì đầu đó của cuộn dây trở thành cực Bắc.", False, "Kéo ra xa làm số đường sức giảm; theo định luật Lenz cuộn dây hút nam châm lại nên đầu đó là cực Nam, chứ không phải cực Bắc.")])


def build():
    out = []
    count = {}
    for i, c in enumerate(C):
        lid, label, tid, tname = DANG[c["k"]]
        count[c["k"]] = count.get(c["k"], 0) + 1
        q = {"type": c["t"], "form": "bai_tap", "topic": tname, "difficulty": c["d"], "difficultySource": "ai",
             "question": P + c["q"] + "</p>"}
        if c["t"] == "multiple_choice":
            q["options"] = c["o"]; q["answer"] = c["a"]; q["explanation"] = ps(c["e"])
        else:
            q["statements"] = [{"text": t, "answer": b} for t, b, _ in c["s"]]
            q["explanation"] = ps([f"{'abcd'[j]}) {'Đúng' if b else 'Sai'}. {x}" for j, (_, b, x) in enumerate(c["s"])])
        out.append({"stt": i + 1, "key": c["k"], "lesson_id": lid, "dang_label": label, "topic_id": tid, "topic_name": tname, "q": q})
    for k in DANG:
        need = 4 - CO.get(k, 0)
        if count.get(k, 0) < need: print("THIẾU", k, count.get(k, 0), "/", need)
    return out

if __name__ == "__main__":
    out = build()
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, "cau.json"), "w"), ensure_ascii=False, indent=1)
    print(len(out), "câu,", len({o["key"] for o in out}), "dạng")
