"""Đóng gói theory.html + 12 câu Luyện tập thành bundle.json (schema thachlab.lesson-bundle/v1).
Chạy từ thư mục này: python3 build_figs.py && python3 build_bundle.py
Cơ cấu như đề Bộ: Phần I trắc nghiệm (8), Phần II đúng/sai (2), Phần III trả lời ngắn (2).
"""
import json

T = "Từ trường ngoài SGK hay gặp trong đề thi"


def mc(q, opts, ans, exp, topic=T):
    return {"type": "multiple_choice", "form": "ly_thuyet", "topic": topic, "question": q, "options": opts, "answer": ans, "explanation": exp}


QUESTIONS = [
    mc("Một vòng dây tròn gồm $N$ vòng, bán kính $R$, có dòng điện $I$ chạy qua. Độ lớn cảm ứng từ tại tâm vòng dây là",
       ["$B = 2\\cdot10^{-7}\\dfrac{NI}{R}$.", "$B = 4\\pi\\cdot10^{-7}\\dfrac{NI}{R}$.", "$B = 2\\pi\\cdot10^{-7}\\dfrac{NI}{R}$.", "$B = 2\\pi\\cdot10^{-7}NIR$."],
       2, "Thẳng 2 – Tròn 2π – Ống 4π: tại tâm vòng tròn $B = 2\\pi\\cdot10^{-7}\\dfrac{NI}{R}$. Hệ số 2 là của dây thẳng, $4\\pi$ là của ống dây; $B$ tỉ lệ nghịch với $R$ chứ không tỉ lệ thuận."),
    mc("Ống dây dài 20 cm có 500 vòng, dòng điện 0,5 A chạy qua. Cảm ứng từ trong lòng ống xấp xỉ bằng",
       ["0,785 mT.", "1,57 mT.", "15,7 mT.", "0,157 mT."],
       1, "$B = 4\\pi\\cdot10^{-7}\\dfrac{N}{\\ell}I = 4\\pi\\cdot10^{-7}\\cdot\\dfrac{500}{0{,}2}\\cdot0{,}5 \\approx 1{,}57\\cdot10^{-3}$ T. Ra 0,785 mT là dùng hệ số $2\\pi$; ra 0,157 mT là để $\\ell = 2$ m."),
    mc("Hai dây dẫn thẳng dài song song có dòng điện chạy qua. Lực từ tác dụng lên mỗi mét dây",
       ["tỉ lệ thuận với khoảng cách giữa hai dây.", "tỉ lệ nghịch với khoảng cách giữa hai dây.", "tỉ lệ nghịch với bình phương khoảng cách.", "không phụ thuộc khoảng cách giữa hai dây."],
       1, "$F = 2\\cdot10^{-7}\\dfrac{I_1I_2}{r}\\ell$: tỉ lệ nghịch với $r$ (bậc một). Bình phương khoảng cách là của lực Coulomb giữa hai điện tích điểm — đừng lẫn."),
    mc("Một electron chuyển động tròn đều trong từ trường đều chỉ do tác dụng của lực từ. Phát biểu nào sau đây đúng?",
       ["Lực từ sinh công dương làm electron chuyển động nhanh dần.", "Lực từ cùng phương với vận tốc của electron.", "Động năng của electron không đổi.", "Gia tốc của electron bằng không."],
       2, "Lực từ luôn vuông góc vận tốc nên không sinh công, động năng không đổi. Gia tốc hướng tâm $a = v^2/R$ khác 0 vì hướng vận tốc liên tục đổi."),
    mc("Electron bay sang phải trong mặt phẳng hình vẽ, từ trường đều hướng vào trong mặt phẳng hình vẽ. Lực Lorentz tác dụng lên electron hướng",
       ["lên trên.", "xuống dưới.", "sang trái.", "ra ngoài mặt phẳng hình vẽ."],
       1, "Bàn tay trái: đường sức vào lòng bàn tay, cổ tay → ngón tay theo $\\vec v$ (sang phải), ngón cái chỉ lên — đó là chiều lực lên hạt <em>dương</em>. Electron mang điện âm nên lực ngược lại: hướng xuống."),
    mc("Proton ($m = 1{,}67\\cdot10^{-27}$ kg, $q = 1{,}6\\cdot10^{-19}$ C) bay với tốc độ $10^{6}$ m/s vuông góc với đường sức của từ trường đều $B = 0{,}5$ T. Bán kính quỹ đạo xấp xỉ bằng",
       ["2,09 cm.", "4,18 cm.", "1,04 cm.", "20,9 cm."],
       0, "$R = \\dfrac{mv}{|q|B} = \\dfrac{1{,}67\\cdot10^{-27}\\cdot10^{6}}{1{,}6\\cdot10^{-19}\\cdot0{,}5} \\approx 2{,}09\\cdot10^{-2}$ m. Ra 4,18 cm là tính đường kính $2R$."),
    mc("Electron ($m_e = 9{,}1\\cdot10^{-31}$ kg) chuyển động tròn đều trong từ trường đều $B = 0{,}01$ T. Chu kì chuyển động xấp xỉ bằng",
       ["$1{,}8\\cdot10^{-9}$ s.", "$3{,}6\\cdot10^{-9}$ s.", "$5{,}7\\cdot10^{-10}$ s.", "Không tính được vì thiếu tốc độ."],
       1, "$T = \\dfrac{2\\pi m}{|q|B} = \\dfrac{2\\pi\\cdot9{,}1\\cdot10^{-31}}{1{,}6\\cdot10^{-19}\\cdot0{,}01} \\approx 3{,}57\\cdot10^{-9}$ s. Chu kì không phụ thuộc tốc độ nên đề không cần cho $v$. Quên $2\\pi$ thì ra $5{,}7\\cdot10^{-10}$ s; dùng $\\pi$ thì ra $1{,}8\\cdot10^{-9}$ s."),
    mc("Thanh kim loại dài 50 cm chuyển động với tốc độ 2 m/s, vuông góc với đường sức của từ trường đều $B = 0{,}2$ T (thanh vuông góc vận tốc). Suất điện động cảm ứng trong thanh là",
       ["20 V.", "0,05 V.", "0,2 V.", "2 V."],
       2, "$e = Bv\\ell = 0{,}2\\cdot2\\cdot0{,}5 = 0{,}2$ V. Ra 20 V là để $\\ell = 50$; ra 0,05 V là chia cho $v$."),
    {"type": "true_false", "form": "bai_tap", "topic": T,
     "question": "Thanh kim loại MN dài 25 cm trượt đều sang phải với tốc độ 3 m/s trên hai thanh ray nằm ngang nối với điện trở $R = 0{,}3\\ \\Omega$, trong từ trường đều $B = 0{,}4$ T có đường sức vuông góc với mặt phẳng ray. Bỏ qua điện trở của thanh, ray và ma sát.",
     "statements": [
         {"text": "Suất điện động cảm ứng trong thanh bằng 0,3 V.", "answer": True},
         {"text": "Lực từ tác dụng lên thanh cùng chiều chuyển động của thanh.", "answer": False},
         {"text": "Cường độ dòng điện trong mạch bằng 1 A.", "answer": True},
         {"text": "Công suất toả nhiệt trên điện trở bằng 3 W.", "answer": False}],
     "explanation": "a) Đúng: $e = Bv\\ell = 0{,}4\\cdot3\\cdot0{,}25 = 0{,}3$ V.<br>b) Sai: theo định luật Lenz lực từ cản chuyển động, ngược chiều $\\vec v$.<br>c) Đúng: $I = e/R = 0{,}3/0{,}3 = 1$ A.<br>d) Sai: $P = I^2R = 1^2\\cdot0{,}3 = 0{,}3$ W (bằng công suất lực kéo $Fv = 0{,}1\\cdot3$)."},
    {"type": "true_false", "form": "ly_thuyet", "topic": T,
     "question": "Một proton bay vào từ trường đều với vận tốc vuông góc đường sức và chuyển động tròn đều chỉ dưới tác dụng của lực từ.",
     "statements": [
         {"text": "Tốc độ của proton không đổi trong suốt chuyển động.", "answer": True},
         {"text": "Lực từ tác dụng lên proton sinh công dương.", "answer": False},
         {"text": "Tăng độ lớn cảm ứng từ lên gấp đôi thì bán kính quỹ đạo giảm một nửa.", "answer": True},
         {"text": "Proton bay càng nhanh thì chu kì chuyển động càng lớn.", "answer": False}],
     "explanation": "a) Đúng: lực từ vuông góc vận tốc nên không đổi tốc độ.<br>b) Sai: lực vuông góc vận tốc nên công bằng 0.<br>c) Đúng: $R = \\dfrac{mv}{|q|B}$ tỉ lệ nghịch với $B$.<br>d) Sai: $T = \\dfrac{2\\pi m}{|q|B}$ không phụ thuộc $v$."},
    {"type": "short_answer", "form": "bai_tap", "topic": T,
     "question": "Dây dẫn thẳng dài mang dòng điện 8 A. Cảm ứng từ tại điểm cách dây 4 cm bằng $x\\cdot10^{-5}$ T. Tìm $x$.",
     "answer": "4", "explanation": "$B = 2\\cdot10^{-7}\\dfrac{I}{r} = 2\\cdot10^{-7}\\cdot\\dfrac{8}{0{,}04} = 4\\cdot10^{-5}$ T."},
    {"type": "short_answer", "form": "bai_tap", "topic": T,
     "question": "Electron ($m_e = 9{,}1\\cdot10^{-31}$ kg, $|e| = 1{,}6\\cdot10^{-19}$ C) bay với tốc độ $1{,}6\\cdot10^{6}$ m/s vuông góc với đường sức của từ trường đều $B = 2{,}5\\cdot10^{-3}$ T. Bán kính quỹ đạo bằng bao nhiêu milimét (làm tròn đến hàng phần mười)?",
     "answer": "3,6", "explanation": "$R = \\dfrac{m_ev}{|e|B} = \\dfrac{9{,}1\\cdot10^{-31}\\cdot1{,}6\\cdot10^{6}}{1{,}6\\cdot10^{-19}\\cdot2{,}5\\cdot10^{-3}} = 3{,}64\\cdot10^{-3}$ m $\\approx 3{,}6$ mm."},
]

bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "target": {"class_name": "Vật lí 12", "lesson_title": "Chủ đề thêm. Từ trường ngoài SGK hay gặp trong đề thi"},
    "theory_title": "Lý thuyết trọng tâm",
    "theory_subtitle": "Dòng điện thẳng, tròn, ống dây · hai dòng song song · lực Lorentz · thanh trượt",
    "theory_html": open("theory.html", encoding="utf8").read(),
    "worked_examples": [],
    "exam": {"title": "Luyện tập — Từ trường ngoài SGK hay gặp trong đề thi", "duration_minutes": 25, "questions": QUESTIONS},
    "raster_images": [],
}

with open("bundle.json", "w", encoding="utf8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("bundle.json:", len(QUESTIONS), "câu")
