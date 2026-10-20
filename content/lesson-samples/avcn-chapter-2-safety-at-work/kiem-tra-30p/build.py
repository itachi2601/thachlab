#!/usr/bin/env python3
"""Dựng bundle.json đề Kiểm tra 30 phút Chapter 2 (AVCN). Chạy: python3 build.py"""
import json, pathlib, random
HERE = pathlib.Path(__file__).resolve().parent
base = json.load(open(HERE.parent / "bundle.json"))
T = "AVCN C2: Safety at Work"
# (câu hỏi, [đúng, sai, sai, (sai)], giải thích) — đáp án đúng luôn ở vị trí 0, script xoay vị trí
MC = [
 # Part 1 · từ vựng
 ("Protects the head from accidental injury.", ["safety helmet","safety goggles","ear protectors","protective mask"], "<em>the head</em> (đầu) → safety helmet, mũ bảo hộ."),
 ("Protect ears against noise.", ["ear protectors","safety goggles","safety helmet","safety gloves"], "<em>ears … noise</em> (tai, tiếng ồn) → ear protectors."),
 ("A safety sign which warns you of danger.", ["hazard sign","mandatory sign","prohibition sign","general safety sign"], "<em>warns you of danger</em> (cảnh báo nguy hiểm) → hazard sign."),
 ("A safety sign which tells you what you must not do.", ["prohibition sign","mandatory sign","hazard sign","fire safety sign"], "<em>must not</em> (không được) → prohibition sign, biển cấm. Mandatory là <em>must do</em>."),
 ("Protects the body against welding work.", ["protective apron","safety shoes","dorsal belt","knee pads"], "<em>the body … welding</em> → protective apron, tạp dề bảo hộ."),
 ("Avoids the worker falling.", ["safety harness","dorsal belt","knee pads","safety gloves"], "<em>falling</em> (rơi ngã) → safety harness, dây đai an toàn."),
 ("Protect knees on the ground while working.", ["knee pads","dorsal belt","safety shoes","safety gloves"], "<em>knees</em> (đầu gối) → knee pads."),
 ("Damage to one or more ligaments in a joint.", ["sprain","overexertion","apprentice","pit"], "<em>ligaments in a joint</em> (dây chằng ở khớp) → sprain, bong gân."),
 ("Too much use of physical or mental energy; hard work.", ["overexertion","sprain","apprentice","pit"], "<em>too much use of energy</em> → overexertion, gắng sức quá mức."),
 ("A space with limited entry that is not suitable for people.", ["confined areas","locker room","assembly point","fire brigade"], "<em>limited entry</em> (lối vào hạn chế) → confined areas, không gian hẹp, kín."),
 # Part 2 · đọc lại Article 1–2
 ("Article 1. Some shops that specialize in oil changes and lubrication use an arrangement commonly called a ______.", ["pit","apron","harness","locker"], "Article 1: <em>an arrangement commonly called a pit</em>."),
 ("Article 1. The mechanic then enters the pit to perform the ______.", ["work","risk","sign","apron"], "Article 1: <em>enters the pit to perform the work</em>."),
 ("Article 1. Pit areas are typically not well-______ and can be hot during summer months.", ["ventilated","injured","confined","drafty"], "Article 1: <em>not well-ventilated</em> (không thông gió tốt)."),
 ("Article 1. The rate of illnesses and injuries is ______ for mechanics than the national average rate.", ["higher","lower","equal","safer"], "Article 1: <em>is higher for mechanics than the national average rate</em>."),
 ("Article 1. Strains and sprains were also common and were typically caused by ______.", ["overexertion","noise","welding","fire"], "Article 1: <em>typically caused by overexertion</em>."),
 ("Article 1. Most automotive service technicians and mechanics work a standard ______ hour week.", ["40","30","50","60"], "Article 1: <em>a standard 40 hour week</em>."),
 ("Article 2. Dial ______ to call the fire brigade.", ["114","115","113","911"], "Article 2: <em>Dial 114 to call the fire brigade</em>."),
 ("Article 2. Leave by the nearest ______.", ["exit","pit","helmet","apron"], "Article 2: <em>Leave by the nearest exit</em>."),
 ("Article 2. Do not go back into the building until you have been told it is ______ to do so.", ["safe","hot","late","noisy"], "Article 2: <em>until you have been told it is safe to do so</em>."),
 # Part 3 · điền từ
 ("A ______ sign shows where fire equipment and fire alarms are.", ["fire safety","prohibition","hazard","mandatory"], "<em>fire equipment and fire alarms</em> → fire safety sign."),
 ("Wear a ______ to avoid inhaling dust, vapours and fumes.", ["protective mask","safety harness","knee pads","dorsal belt"], "<em>inhaling</em> (hít vào) bụi, khói → protective mask."),
 ("A room for changing clothes is called a ______ room.", ["locker","confined","sharp","greasy"], "<em>changing clothes</em> → locker room, phòng thay đồ có tủ cá nhân."),
 ("Work at height needs a safety ______ to avoid falling.", ["harness","helmet","apron","goggles"], "<em>avoid falling</em> → safety harness."),
 ("Lifting heavy parts is a ______ to your back, so wear a dorsal belt.", ["risk","apprentice","locker","pit"], "<em>a risk to your back</em> = nguy cơ cho lưng."),
 # Part 4 · chọn bản dịch đúng
 ("Choose the correct translation: \"However, some shops are drafty and noisy.\"", ["Tuy nhiên, một số xưởng có gió lùa và ồn.","Vì vậy, mọi xưởng đều yên tĩnh.","Tuy nhiên, một số xưởng rất sạch và sáng.","Hơn nữa, xưởng nào cũng nóng."], "<em>However</em> = tuy nhiên; <em>drafty and noisy</em> = có gió lùa và ồn."),
 ("Choose the correct translation: \"Do not stop to collect belongings.\"", ["Đừng dừng lại để lấy đồ đạc cá nhân.","Hãy dừng lại để lấy đồ đạc cá nhân.","Đừng quay lại tòa nhà.","Hãy gọi cứu hoả trước."], "<em>Do not</em> = đừng; <em>belongings</em> = đồ đạc cá nhân."),
 ("Choose the correct translation: \"Many employers provide uniforms, locker rooms, and shower facilities.\"", ["Nhiều chủ doanh nghiệp cung cấp đồng phục, phòng thay đồ và khu nhà tắm.","Nhiều thợ học việc mặc đồng phục và đi tắm.","Một số xưởng không có phòng thay đồ.","Chủ doanh nghiệp yêu cầu thợ tự mua đồng phục."], "<em>provide</em> = cung cấp; <em>locker rooms</em> = phòng thay đồ; <em>shower facilities</em> = khu nhà tắm."),
]
qs = []
for i, (q, opts, why) in enumerate(MC):
    n = len(opts); k = random.Random(i + 7).randrange(n)           # vị trí đáp án đúng, xoay đều
    o = opts[1:]; o.insert(k, opts[0])
    qs.append({"type": "multiple_choice", "question": q, "options": o, "answer": k, "explanation": why,
               "topic": T, "form": "ly_thuyet", "difficulty": "de"})
TF = [
 ("Article 1. Mark each statement True or False.", [
   ("Pit areas are usually well-ventilated.", False),
   ("Mechanics can seldom avoid handling greasy and dirty parts.", True),
   ("A technician may be assisted by an apprentice for heavy work.", True),
   ("Most mechanics work a standard 50 hour week.", False)],
  "Pit areas <em>typically not well-ventilated</em>; tuần làm việc chuẩn là 40 giờ."),
 ("Article 2. Mark each statement True or False.", [
   ("If you find a fire, you should first try to put it out yourself.", False),
   ("All staff should know where the alarm buttons are.", True),
   ("You should close all the doors when you leave.", True),
   ("You should stop to collect your belongings before leaving.", False)],
  "Bài viết: <em>do not try to put it out yourself</em>; <em>Do not stop to collect belongings</em>."),
]
for q, st, why in TF:
    qs.append({"type": "true_false", "question": q, "statements": [{"text": t, "answer": a} for t, a in st],
               "explanation": why, "topic": T, "form": "ly_thuyet", "difficulty": "de"})
# Đoạn Article chép nguyên văn giáo trình, gắn thẳng vào đề để SV không phải lật lại (split-attention, Mayer)
import re
_src = json.load(open(HERE.parent / "data" / "bai.json"))["bai_doc"]
ART = {n: " ".join(re.sub("<[^>]+>", "", c[0]) for c in _src[n - 1]["cau"]) for n in (1, 2)}
def with_article(q):
    m = re.match(r"Article (\d)\.\s*(.*)", q, re.S)
    if not m or int(m.group(1)) not in ART:
        return q
    n = int(m.group(1))
    return f'<blockquote><strong>Article {n}</strong><br>{ART[n]}</blockquote><p>{m.group(2)}</p>'
for q in qs:
    q["question"] = with_article(q["question"])
base["theory_html"] = ""; base["theory_title"] = ""; base["theory_subtitle"] = ""
base["worked_examples"] = []; base["raster_images"] = []
base["exam"] = {"title": "Kiểm tra 30 phút Chapter 2: Safety at Work", "topic": T, "difficulty": "de",
                "duration_minutes": 30, "subject_code": "avcn", "questions": qs}
json.dump(base, open(HERE / "bundle.json", "w"), ensure_ascii=False, indent=1)
print(len(qs), "câu;", sum(1 for q in qs if q["type"]=="multiple_choice"), "trắc nghiệm")
