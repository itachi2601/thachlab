# Dựng bundle chỉ-có-đề (đề KIỂM TRA, khác bộ Luyện tập) của AVCN Chapter 10 → kiem-tra-bundle.json
# Đăng: npx tsx scripts/upload-lesson.mts <file> --lesson <id Chapter 10> --target kiem_tra
import json, os
T = "AVCN C10: Maintenance"
def mc(q, opts, ans, why):
    assert len(opts) == 4 and 0 <= ans < 4
    return {"type": "multiple_choice", "question": q, "options": opts, "answer": ans, "explanation": why,
            "topic": T, "form": "ly_thuyet", "difficulty": "trung-binh"}
def tf(q, sts, why):
    return {"type": "true_false", "question": q, "statements": [{"text": t, "answer": a} for t, a in sts],
            "explanation": why, "topic": T, "form": "ly_thuyet", "difficulty": "trung-binh"}
Q = [
 mc("Any activity such as tests, adjustments, lubrication and repairs that keeps a unit able to do its job.", ["inspection", "replacement", "maintenance", "risk"], 2, "<em>tests, adjustments, lubrication, repairs</em> → maintenance (bảo dưỡng)."),
 mc("A part that supports a rotating shaft and reduces friction.", ["gasket", "belt", "casing", "bearing"], 3, "<em>supports a rotating shaft</em> → bearing (ổ bi, ổ trục)."),
 mc("The situation in which a machine stops working as it should.", ["failure", "schedule", "adjustment", "clearance"], 0, "<em>stops working</em> → failure (sự hỏng)."),
 mc("The action of fixing something that is broken or damaged.", ["replacement", "inspection", "repair", "lubrication"], 2, "<em>fixing … broken</em> → repair. Replacement là thay cái mới, không phải sửa."),
 mc("Gradual damage to a surface because two parts rub together.", ["corrosion", "leak", "crack", "wear"], 3, "<em>rub together</em> → wear (mòn). Corrosion là gỉ do hoá chất."),
 mc("A flat sheet of soft material fitted between two joined surfaces to make the joint tight.", ["belt", "roller", "gasket", "bearing"], 2, "<em>between two joined surfaces</em> → gasket (gioăng đệm)."),
 mc("A device that removes dirt from the oil.", ["motor oil", "oil filter", "belt", "gasket"], 1, "<em>removes dirt</em> → oil filter (bộ lọc dầu)."),
 mc("A ring fitted around a rotating shaft to keep oil inside and dirt out.", ["roller", "belt", "oil filter", "oil seal"], 3, "<em>ring around a shaft … keep oil inside</em> → oil seal (phớt chắn dầu)."),
 mc("A flexible tube that carries pressurised fluid.", ["hydraulic hose", "belt", "casing", "gasket"], 0, "<em>flexible tube … fluid</em> → hydraulic hose (ống mềm thuỷ lực)."),
 mc("A loop of flexible material that connects two pulleys and transmits motion.", ["roller", "casing", "belt", "crack"], 2, "<em>loop … connects two pulleys</em> → belt (dây đai)."),
 mc("A thin line on a surface where something has started to break.", ["leak", "crack", "wear", "corrosion"], 1, "<em>thin line … started to break</em> → crack (vết nứt). Leak là chỗ chất lỏng chảy ra."),
 mc("Liquid put into an engine to lubricate its moving parts.", ["oil filter", "oil seal", "hydraulic hose", "motor oil"], 3, "<em>liquid … lubricate</em> → motor oil (dầu nhớt động cơ)."),
 mc("Time worked in addition to normal working hours.", ["downtime", "overtime", "schedule", "inventory"], 1, "<em>in addition to normal hours</em> → overtime. Downtime là lúc máy ngừng, không phải giờ làm thêm."),
 mc("The list or stock of goods, such as spare parts, kept in a store.", ["inventory", "schedule", "overtime", "asset"], 0, "<em>stock of goods kept in a store</em> → inventory (hàng tồn kho)."),
 mc("The outer cover that protects the parts inside a machine.", ["belt", "roller", "asset", "casing"], 3, "<em>outer cover</em> → casing (vỏ máy)."),
 mc("Complete: \"Corrective maintenance is a technique that waits for equipment ______ before any maintenance action is taken.\"", ["reliability", "failure", "clearance", "schedule"], 1, "Corrective = chờ máy hỏng (<em>waits for … failure</em>) rồi mới sửa."),
 mc("Complete: \"Preventive maintenance gives improved ______ of equipment.\"", ["corrosion", "inventory", "downtime", "reliability"], 3, "Lợi ích của preventive: <em>improved reliability</em> (độ tin cậy cao hơn)."),
 mc("Complete: \"Preventive maintenance gives less unplanned ______ caused by equipment failure.\"", ["downtime", "injury", "overtime", "inventory"], 0, "Máy ngừng ngoài kế hoạch = <em>unplanned downtime</em>; preventive làm giảm nó."),
 mc("Complete: \"The fuel line ______, resulting in a major leak.\"", ["adjusted", "lubricated", "ruptured", "aligned"], 2, "Đường dẫn nhiên liệu bị vỡ (<em>ruptured</em>) nên mới rò rỉ lớn."),
 mc("Complete: \"We check the metal casing regularly for signs of ______.\"", ["tension", "schedule", "overtime", "corrosion"], 3, "Vỏ kim loại cần kiểm tra dấu hiệu gỉ sét: <em>corrosion</em>."),
 tf("Read Article 1 (corrective maintenance). Mark each statement True or False.", [
   ("Corrective maintenance is also called breakdown maintenance.", True),
   ("A plant using run-to-failure management spends money on maintenance every week.", False),
   ("High machine downtime is one of the expenses of corrective maintenance.", True),
   ("Corrective maintenance gives high production availability.", False)],
   "Run-to-failure: không tốn tiền bảo dưỡng cho tới khi máy hỏng; chi phí gồm downtime cao và <em>low</em> production availability."),
 tf("Read Article 2 (preventive maintenance). Mark each statement True or False.", [
   ("Preventive maintenance is routine maintenance of equipment and machinery.", True),
   ("Preventive maintenance leads to more unnecessary inspections.", False),
   ("Preventive maintenance helps prolong the life of equipment.", True),
   ("Preventive maintenance causes more expensive repairs after unexpected failures.", False)],
   "Preventive đem lại <em>less</em> unnecessary inspections và <em>fewer</em> expensive repairs; <em>prolonged life</em> là một lợi ích."),
 tf("Read Article 3 (Flight 236). Mark each statement True or False.", [
   ("An incorrect hydraulic pipe was fitted to the right-hand engine.", True),
   ("The pipe that was fitted was too small.", False),
   ("Flight 236 was flying from Toronto to Lisbon.", True),
   ("The problem was detected before the flight took off.", False)],
   "Ống bị lắp sai và <em>oversized</em> (quá lớn); lỗi <em>went undetected</em> tới đêm 24/8/2001."),
]
B = {"schema": "thachlab.lesson-bundle/v1",
 "target": {"class_name": "Anh văn chuyên ngành Cơ khí", "chapter_title": "Technical English for Mechanical Engineering", "lesson_title": "Chapter 10: Maintenance — Bảo dưỡng máy"},
 "theory_title": "Học", "theory_subtitle": "", "theory_html": "", "worked_examples": [],
 "exam": {"title": "Kiểm tra Chapter 10: Maintenance", "topic": T, "difficulty": "trung-binh", "duration_minutes": 25,
          "subject_code": "avcn", "new_topics": [T], "questions": Q},
 "raster_images": []}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kiem-tra-bundle.json")
json.dump(B, open(out, "w"), ensure_ascii=False, indent=1)
print(len(Q), "câu →", out)
