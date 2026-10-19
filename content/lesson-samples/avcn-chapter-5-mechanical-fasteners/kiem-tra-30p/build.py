#!/usr/bin/env python3
"""Dựng bundle.json đề Kiểm tra 30 phút Chapter 5 (AVCN). Chạy: python3 build.py"""
import json, pathlib, random
HERE = pathlib.Path(__file__).resolve().parent
base = json.load(open(HERE.parent / "bundle.json"))
T = "AVCN C5: Mechanical Fasteners"
# (câu hỏi, [đúng, sai, sai, (sai)], giải thích) — đáp án đúng luôn ở vị trí 0, script xoay vị trí
MC = [
 # Part 1 · từ vựng
 ("A device used to hold two or more things together.", ["fastener","grade","washer","thread"], "<em>hold … together</em> (giữ … lại với nhau) → fastener, chốt nối."),
 ("A fastener with a thread that is turned into a surface.", ["screw","nail","pin","rivet"], "<em>a thread that is turned</em> (có ren, được vặn vào) → screw. Đinh (nail) thân trơn, không có ren."),
 ("A threaded fastener used with a nut to press pieces together.", ["bolt","nail","anchor","pin"], "<em>with a nut</em> (đi với đai ốc) → bolt."),
 ("The helical grooves on the outside of a bolt or screw.", ["thread","shank","nut","clamp"], "<em>grooves</em> (rãnh) quanh thân → thread, ren."),
 ("A bolt head with six sides, turned by a spanner.", ["hex head","socket head","rivet gun","hex key"], "<em>six sides</em> (sáu cạnh) + <em>spanner</em> → hex head, đầu lục giác."),
 ("A bolt head with a hexagonal hole in its top.", ["socket head","hex head","shop head","factory head"], "<em>hole in its top</em> (lỗ ở đỉnh) → socket head, vặn bằng chìa lục giác."),
 ("In the direction of clock hands; a nut is screwed on this way.", ["clockwise","anticlockwise","helical","metric"], "<em>clock hands</em> (kim đồng hồ) → clockwise."),
 ("A hollow rivet fitted with a rivet gun.", ["blind rivet","solid rivet","hex key","anchor"], "<em>hollow</em> (rỗng) + <em>rivet gun</em> → blind rivet."),
 ("Which word means \"vòng đệm, long đền\"?", ["washer","nut","anchor","clamp"], "Vòng đệm đặt giữa đai ốc và bề mặt → washer."),
 ("Which word means \"đinh tán\"?", ["rivet","nail","pin","bolt"], "Đinh tán là chốt nối vĩnh viễn → rivet. Nail là đinh đóng, bolt là bu lông."),
 # Part 2 · đọc lại Article 1–3
 ("Article 2. The threaded shaft allows a nut to be ______ onto the bolt.", ["screwed","welded","drilled","cut"], "Article 2: <em>to be screwed onto the bolt</em>."),
 ("Article 2. Nuts usually have a ______-hand thread.", ["right","left","flat","upper"], "Article 2: <em>Nuts usually have a right-hand thread</em>. Left-hand chỉ dùng <em>in some situations</em>."),
 ("Article 2. Nuts are unscrewed by turning them ______.", ["anticlockwise","clockwise","upward","outside"], "Article 2: <em>unscrewed by turning them anticlockwise</em>. Vặn vào là clockwise, tháo ra là ngược lại."),
 ("Article 2. Most bolts have heads with ______ perimeters.", ["hexagonal","helical","hollow","metric"], "Article 2: <em>heads with hexagonal perimeters</em>. Helical là kiểu của ren."),
 ("Article 3. A solid rivet has a head at one end, called the ______ head.", ["factory","shop","socket","blind"], "Article 3: <em>called the factory head</em>. Shop head là đầu thứ hai, tạo ra sau khi tán."),
 ("Article 3. The rivet is inserted through a pre-drilled ______.", ["hole","thread","grade","head"], "Article 3: <em>inserted through a pre-drilled hole</em>."),
 ("Article 3. Blind rivets are made from ______ tubes.", ["hollow","solid","heavy","flat"], "Article 3: <em>made from hollow tubes</em>. Solid rivet mới là loại đặc."),
 ("Article 1. Use an ______ for situations requiring extra support.", ["anchor","nail","pin","washer"], "Article 1: <em>Use an anchor for situations requiring extra support</em>. Trước chỗ trống là <em>an</em>."),
 # Part 3 · điền từ
 ("Nails are ______ for walls and wood surfaces.", ["ideal","hollow","clockwise","threaded"], "<em>ideal for</em> = rất hợp với. Hollow (rỗng), clockwise (theo chiều kim đồng hồ) không đi với <em>for</em> ở đây."),
 ("Wood screws are best for ______ wood surfaces.", ["solid","hollow","left-hand","blind"], "<em>solid wood</em> = gỗ đặc."),
 ("Article 1. Get the right washers and nuts to add strength and prevent damage to ______.", ["surfaces","shop heads","grades","clamps"], "Article 1: <em>prevent damage to surfaces</em> (tránh làm hỏng bề mặt)."),
 ("This store carries both UTS thread and ______ thread measurements.", ["metric","blind","socket","hollow"], "UTS là hệ inch, đi cặp với <em>metric</em> (hệ mét)."),
 ("Use ______ when pressing pieces together from both sides.", ["bolts","anchors","nails","pins"], "Bolt đi với nut: ép chi tiết lại từ hai phía."),
 # Part 4 · chọn bản dịch đúng
 ("Choose the correct translation: \"These allow a spanner to turn them.\"", ["Chúng giúp cờ lê vặn được chúng.","Cờ lê không thể vặn chúng.","Chúng được làm bằng cờ lê.","Cờ lê giúp chúng không bị gỉ."], "Mẫu <em>X allows Y to V</em> = X giúp / cho phép Y làm V."),
 ("Choose the correct translation: \"Rivets are permanent fasteners – they cannot be unscrewed.\"", ["Đinh tán là chốt nối vĩnh viễn, không thể vặn ra được.","Đinh tán là chốt nối tạm thời, vặn ra được.","Đinh tán là chốt nối rỗng, không có ren.","Đinh tán là dụng cụ để vặn đai ốc."], "<em>permanent</em> = vĩnh viễn; <em>cannot be unscrewed</em> = không thể vặn ra."),
 ("Choose the correct translation: \"Blind rivets are not suitable for high-strength joints.\"", ["Đinh tán rút không phù hợp cho mối ghép chịu lực cao.","Đinh tán rút rất phù hợp cho mối ghép chịu lực cao.","Đinh tán rút được lắp bằng kìm rút.","Đinh tán rút làm từ thanh đặc."], "<em>not suitable for</em> = không phù hợp với; <em>high-strength joints</em> = mối ghép chịu lực cao."),
]
qs = []
for i, (q, opts, why) in enumerate(MC):
    n = len(opts); k = random.Random(i + 7).randrange(n)           # vị trí đáp án đúng, xoay đều
    o = opts[1:]; o.insert(k, opts[0])
    qs.append({"type": "multiple_choice", "question": q, "options": o, "answer": k, "explanation": why,
               "topic": T, "form": "ly_thuyet", "difficulty": "de"})
TF = [
 ("Article 2. Mark each statement True or False.", [
   ("Bolts have threads on the outside of the shaft.", True),
   ("Nuts are usually unscrewed by turning them clockwise.", False),
   ("A hex key fits into a socket head.", True),
   ("Hexagonal heads allow a hex key to turn them.", False)],
  "Hex head dùng cờ lê (spanner); socket head mới dùng hex key. Nuts: vặn vào theo chiều kim đồng hồ, tháo ra ngược chiều."),
 ("Article 3. Mark each statement True or False.", [
   ("A solid rivet has a short, solid shaft of metal.", True),
   ("Blind rivets are fitted using a rivet gun.", True),
   ("Blind rivets are the best choice for high-strength joints.", False),
   ("The shop head is already on the rivet before it is inserted.", False)],
  "Shop head chỉ tạo ra sau khi tán (đầu ban đầu là factory head). Blind rivet không phù hợp mối ghép chịu lực cao."),
]
for q, st, why in TF:
    qs.append({"type": "true_false", "question": q, "statements": [{"text": t, "answer": a} for t, a in st],
               "explanation": why, "topic": T, "form": "ly_thuyet", "difficulty": "de"})
base["theory_html"] = ""; base["theory_title"] = ""; base["theory_subtitle"] = ""
base["worked_examples"] = []; base["raster_images"] = []
base["exam"] = {"title": "Kiểm tra 30 phút Chapter 5: Mechanical Fasteners", "topic": T, "difficulty": "de",
                "duration_minutes": 30, "subject_code": "avcn", "questions": qs}
json.dump(base, open(HERE / "bundle.json", "w"), ensure_ascii=False, indent=1)
print(len(qs), "câu;", sum(1 for q in qs if q["type"]=="multiple_choice"), "trắc nghiệm")
