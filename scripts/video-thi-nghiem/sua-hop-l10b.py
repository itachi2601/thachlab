# Cổng mới L10b (thầy duyệt 27/11 "sửa cả hộp"): sửa tối thiểu hộp exp lộ đáp án Dự đoán/chốt clip mới — ghi theory.src.html, theory.html, bundle.json.
import json, sys
E = [
 ("l10-thuc-hanh-dong-luong",
  "bảng dưới (số liệu minh hoạ tính từ mô hình): tốc độ thật ở chỗ va chạm lớn hơn số đọc ở cổng 1.",
  "bảng dưới (số liệu minh hoạ tính từ mô hình): so tốc độ thật ở chỗ va chạm với số đọc ở cổng 1."),
 ("l10-thuc-hanh-dong-luong",
  "<strong>Rút ra:</strong> $p$ tính từ số đọc ở cổng 1 nhỏ hơn động lượng thật lúc va chạm, nên $p'$ đo được lớn hơn $p$ đo được. Chỉ nghiêng vài milimét đã lệch vài phần trăm, cỡ độ lệch $\\delta$ ở trên: phải chỉnh ngang trước khi đo.",
  "<strong>Rút ra:</strong> $p$ tính từ số đọc ở cổng 1 lệch thế nào so với động lượng thật lúc va chạm, kéo theo $p'$ đo được so với $p$ đo được ra sao? Vì sao phải chỉnh băng ngang trước khi đo?"),
 ("l10-dong-luong",
  "<strong>Quan sát:</strong> $v_2$ luôn âm và nhỏ hơn $v_1$ về độ lớn. Xung lượng tăng theo tốc độ đẩy.",
  "<strong>Quan sát:</strong> so dấu và độ lớn của $v_2$ với $v_1$; xung lượng thay đổi thế nào khi đẩy mạnh dần (video bên dưới)."),
 ("l10-dong-luong",
  "đặt một khúc gỗ. Lặp lại với bi $100\\ \\text{g}$.",
  "đặt một khúc gỗ (nặng hơn bi nhiều). Lặp lại với bi $100\\ \\text{g}$."),
 ("l10-co-nang-bao-toan",
  "<strong>Quan sát:</strong> $v$ đo được rất gần $\\sqrt{2gh}$, nhưng lần nào cũng thấp hơn một chút.",
  "<strong>Quan sát:</strong> đọc $v$ ở từng độ cao thả (video bên dưới), rồi so với $\\sqrt{2gh}$."),
 ("l10-dong-nang-the-nang",
  "<strong>Quan sát:</strong> tốc độ qua cổng gấp đôi thì quãng trượt dài gần gấp bốn.",
  "<strong>Quan sát:</strong> so quãng trượt khi tốc độ qua cổng tăng dần (video bên dưới)."),
 ("l10-dong-nang-the-nang",
  "đúng bằng phần động năng mất đi, nên $s$ tỉ lệ với $v^2$.",
  "đúng bằng phần động năng mất đi. Từ đó $s$ phụ thuộc $v$ thế nào?"),
 ("l10-hieu-suat",
  "<strong>Quan sát:</strong> vỏ động cơ ấm hơn chân đế rõ rệt; còn nghe tiếng ù nhẹ.",
  "<strong>Quan sát:</strong> so độ ấm của vỏ động cơ với chân đế; lắng nghe khi quạt chạy."),
 ("l10-hieu-suat",
  "Việc cần là nâng xe lên cao $h$, nên có ích luôn là $W_{ci} = mgh = 0{,}80\\ \\text{J}$.",
  "Việc cần là nâng xe lên cao $h$: đó là công có ích $W_{ci} = mgh$."),
 ("l10-hieu-suat",
  "<strong>Quan sát:</strong> $W_{tp}$ lớn hơn $0{,}80\\ \\text{J}$ ở cả bốn góc.",
  "<strong>Quan sát:</strong> so $W_{tp}$ với $W_{ci}$ ở từng góc (video bên dưới)."),
]
# Đợt 2 (kiem-code hop-kiem-v1, 27/11): chạy với --dot2.
E2 = [
 ("l10-nang-luong-cong-co-hoc", "Cột năng lượng nào đổi lúc bóng chạm sàn?", "Cột năng lượng nào đổi, và đổi vào lúc nào?"),
 ("l10-cong-suat", "<strong>Quan sát:</strong> thời gian giảm dần; leo nhanh thì mệt hơn.", "<strong>Quan sát:</strong> so thời gian bốn lần leo (video bên dưới)."),
 ("l10-cong-suat", "<strong>Rút ra:</strong> công nâng người luôn bằng nhau; leo nhanh hơn thì công suất lớn hơn.", "<strong>Rút ra:</strong> công nâng người ở bốn lần so với nhau thế nào? Công suất phụ thuộc vào những đại lượng nào?"),
 ("l10-hieu-suat", "<strong>Rút ra:</strong> điện năng nhận vào không thành hết cơ năng của cánh quạt; một phần thành nhiệt và âm: đó là $W_{hp}$.", "<strong>Rút ra:</strong> điện năng nhận vào có thành hết cơ năng của cánh quạt không? Phần còn lại đi đâu? Phần đó là $W_{hp}$."),
 ("l10-thuc-hanh-dong-luong", "lệch thế nào so với động lượng thật lúc va chạm, kéo theo $p'$ đo được so với $p$ đo được ra sao?", "lệch thế nào so với động lượng thật lúc va chạm? Vì thế $p'$ đo được so với $p$ đo được ra sao?"),
 ("l10-bao-toan-dong-luong", "Sau va chạm, hai xe đổi vận tốc cho nhau hay không?", "Sau va chạm, so vận tốc mỗi xe với vận tốc trước đó."),
 ("l10-dong-luong", "<strong>Quan sát:</strong> thả cao hơn (bi tới nhanh hơn) hoặc bi nặng hơn thì khúc gỗ bị đẩy đi xa hơn.", "<strong>Quan sát:</strong> so quãng khúc gỗ bị đẩy đi giữa các lần thả (video bên dưới)."),
]
if "--dot2" in sys.argv: E = E2
ap = "--apply" in sys.argv; loi = 0
for bai, cu, moi in E:
    for f, a, b in [("theory.src.html", cu, moi), ("theory.html", cu, moi), ("bundle.json", json.dumps(cu, ensure_ascii=False)[1:-1], json.dumps(moi, ensure_ascii=False)[1:-1])]:
        p = f"content/lesson-samples/{bai}/{f}"; s = open(p, encoding="utf-8").read(); n = s.count(a)
        if n != 1: print(f"LOI {p}: {n} lần — {cu[:50]}"); loi += 1; continue
        if ap: open(p, "w", encoding="utf-8").write(s.replace(a, b))
print("LOI", loi, "| apply" if ap else "| dry-run")
