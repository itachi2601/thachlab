"""Đóng gói theory.html + câu tự kiểm tra thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_figs.py && python3 build_bundle.py
Thứ tự phương án / chỉ số answer phải khớp quiz trong theory.src.html.
"""
import json

Q = []


def mc(question, options, answer, explanation):
    Q.append({"type": "multiple_choice", "question": question, "options": options,
              "answer": answer, "explanation": explanation})


mc("Khung dây diện tích 0,05 m² đặt trong từ trường đều B = 0,2 T. Pháp tuyến của khung hợp với B góc 60°. Từ thông qua khung là:",
   ["1,0×10⁻² Wb", "8,7×10⁻³ Wb", "0", "5,0×10⁻³ Wb"], 3,
   "Φ = BS cosα = 0,2·0,05·cos60° = 5×10⁻³ Wb.")
mc("Một vòng dây kín đứng yên trong từ trường đều rất mạnh, mặt vòng vuông góc với đường sức, B không đổi theo thời gian. Trong vòng dây:",
   ["Không có dòng điện cảm ứng, vì từ thông không biến thiên",
    "Có dòng điện cảm ứng lớn, vì từ thông lớn",
    "Có dòng điện cảm ứng, vì có từ trường mạnh",
    "Không có dòng điện cảm ứng, vì từ trường đều không tạo ra từ thông"], 0,
   "Điều kiện có dòng cảm ứng là từ thông biến thiên, không phải từ thông lớn.")
mc("Đưa cực Bắc của thanh nam châm lại gần một vòng dây kín (theo trục vòng dây). Theo định luật Lenz, đầu vòng dây gần nam châm trở thành:",
   ["cực Nam và hút nam châm vào", "không có cực nào, nên không có lực tác dụng lên nam châm",
    "cực Bắc và đẩy nam châm ra", "cực Bắc và hút nam châm vào"], 2,
   "Từ thông tăng nên vòng dây chống lại: tạo cực Bắc ở đầu gần, hai cực cùng tên đẩy nhau.")
mc("Kéo cực Nam của thanh nam châm ra xa một vòng dây kín (theo trục vòng dây). Đầu vòng dây gần nam châm trở thành:",
   ["cực Nam, đẩy nam châm ra xa", "cực Bắc, kéo nam châm lại gần",
    "cực Bắc, đẩy nam châm ra xa", "cực Nam, kéo nam châm lại gần"], 1,
   "Từ thông giảm nên vòng dây bù lại bằng cách kéo nam châm lại; hút nhau thì khác tên, nên đầu gần là cực Bắc.")
mc("Từ thông qua một mạch kín giảm đều từ 6 mWb về 0 trong 0,03 s. Độ lớn suất điện động cảm ứng trong mạch là:",
   ["0,2 V", "2 V", "0,02 V", "1,8×10⁻⁴ V"], 0,
   "|e_c| = 6×10⁻³/0,03 = 0,2 V. Phải đổi mWb ra Wb rồi chia cho Δt.")
mc("Khung dây kín có S = 200 cm², R = 0,5 Ω, mặt khung vuông góc với B. B tăng đều từ 0,1 T đến 0,5 T trong 0,1 s. Cường độ dòng cảm ứng trong khung là:",
   ["40 mA", "80 mA", "320 mA", "160 mA"], 3,
   "ΔΦ = 0,4·0,02 = 8×10⁻³ Wb; e_c = 8×10⁻³/0,1 = 0,08 V; i = 0,08/0,5 = 0,16 A = 160 mA.")

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Bài 12. Hiện tượng cảm ứng điện từ"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Từ chiếc đèn xe đạp không pin",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": {"title": "Luyện tập — Hiện tượng cảm ứng điện từ", "duration_minutes": 10, "questions": Q},
    "raster_images": [],
}
with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=1)
print("ok", len(bundle["theory_html"]), "bytes theory")
