#!/usr/bin/env python3
"""Dựng bundle-kiem-tra.json (đề kiểm tra Chapter 8 theo form đề cuối kỳ 'đề 2'). Chạy: python3 build_kiem_tra.py"""
import json, pathlib
A = "/assets/avcn/chapter-8"
TOPIC = "AVCN C8: Chipping Machining"
Q = []

def mc(part, q, opts, ans, why):
    Q.append({"type": "multiple_choice", "question": f"<b>{part}</b> · {q}", "options": opts, "answer": ans,
              "explanation": why, "topic": TOPIC, "form": "ly_thuyet", "difficulty": "de"})

def pic(src, alt):
    return f'<br><img src="{A}/{src}" alt="{alt}" width="400">'

P1 = "Part 1"
# ---- Part 1: 15 câu (3 điểm)
mc(P1, "The gap left by the blade along the line of the cut.", ["swarf", "kerf", "core", "chuck"], 1, "<em>gap … line of the cut</em> → kerf.")
mc(P1, "Which machine rotates the workpiece while a fixed tool cuts it?", ["Milling machine", "Grinder", "Lathe", "Drill"], 2, "Lathe quay phôi, dao đứng yên (Article 2).")
mc(P1, "Look at the picture. What machine is this?" + pic("lathe.webp", "machine"), ["a milling machine", "a lathe", "a drill press", "a band saw"], 1, "Mâm cặp bên trái + băng máy dài → lathe.")
mc(P1, "A liquid pumped onto the workpiece to keep it cool.", ["Swarf", "Kerf", "Cutting fluid", "Abrasive"], 2, "<em>liquid … keep cool</em> → cutting fluid (coolant).")
mc(P1, "Look at the picture. What tool is this?" + pic("hacksaw.webp", "tool"), ["hole saw", "band saw", "circular saw", "hacksaw"], 3, "Khung chữ C, lưỡi răng nhỏ → hacksaw.")
mc(P1, "What is the waste metal produced during machining called?", ["swarf", "coolant", "workpiece", "blade"], 0, "Waste = swarf hoặc chips.")
mc(P1, "Which technique is used to enlarge a hole that already exists?", ["Drilling", "Milling", "Grinding", "Boring"], 3, "<em>enlarging a hole</em> → boring; drilling là khoan lỗ mới.")
mc(P1, "Look at the picture. What is this?" + pic("hole-saw.webp", "tool"), ["a drill bit", "a hole saw", "an abrasive wheel", "a blade"], 1, "Hình trụ rỗng có răng → hole saw.")
mc(P1, "A machine that removes material across a surface using an abrasive wheel.", ["Grinder", "Lathe", "Drill", "Saw"], 0, "<em>abrasive wheel</em> → grinder.")
mc(P1, "The piece of material being machined.", ["machine tool", "workpiece", "kerf", "core"], 1, "<em>material being machined</em> → workpiece.")
mc(P1, "Look at the picture. What is the tool fitted to a drill?" + pic("drill-bit.webp", "tool"), ["a chuck", "a blade", "a drill bit", "a core"], 2, "Mũi xoắn lắp vào máy khoan → drill bit.")
mc(P1, "Which of the following is NOT a machining technique?", ["Turning", "Painting", "Grinding", "Milling"], 1, "Turning, milling, grinding là gia công cắt gọt; painting thì không.")
mc(P1, "When a workpiece is milled, how is it held on the machine?", ["It rotates quickly", "It moves along the bed", "It is held in a fixed position", "It is held in the hand"], 2, "Article 2: <em>held in a fixed position</em>.")
mc(P1, "Which part of a lathe contains the motor and the gearbox?", ["Headstock", "Tailstock", "Carriage", "Tool post"], 0, "Head = đầu máy, có động cơ và hộp số.")
mc(P1, "A thin, sharp piece of metal, usually with teeth, used for cutting.", ["bit", "blade", "chuck", "wheel"], 1, "<em>thin, sharp piece of metal</em> → blade.")

# ---- Part 2: đoạn đọc (chép từ Article 2, bỏ Turning/Drilling)
PASSAGE = ("<b>Milling</b> is cutting done by a milling machine, often using toothed cutting discs (wheels with teeth that have sharp edges). "
 "When a workpiece is milled, it is held in a fixed position on the machine, and is shaped by cutting tools which rotate while being moved over the surface of the workpiece. "
 "<b>Sawing</b> is cutting using a blade (a thin, sharp piece of metal), which usually has teeth, to remove a thickness of material slightly wider than the blade. "
 "The gap left by the blade, along the line of the cut, is called a kerf. Machines that use toothed blades include circular saws, band saws, and power hacksaws. "
 "A hacksaw has a blade with very small teeth, for cutting metal. Saws may also use abrasive wheels – thin, circular cutting wheels with tough, hard surfaces – often made of industrial diamond. "
 "<b>Grinding</b> is removing material across a surface area, using abrasive wheels. The machines used to grind material are called grinders.")
P2 = "Part 2"
DET = f'<details open><summary>📖 Passage</summary><p>{PASSAGE}</p></details>'
def p2(part, q, opts, ans, why):
    mc(part, q + "<br>" + DET, opts, ans, why)
def blank(n, q, opts, ans, why):
    p2(f"{P2} · 2.1 Fill in the blank ({n}/6)", q, opts, ans, why)
blank(1, "Milling is cutting done by a milling machine, often using toothed cutting ______.", ["discs", "oils", "tables", "locks"], 0, "Câu 1 của đoạn: <em>toothed cutting discs</em>.")
blank(2, "When a workpiece is milled, it is held in a ______ position on the machine.", ["moving", "fixed", "hollow", "round"], 1, "Câu 2: <em>held in a fixed position</em>.")
blank(3, "Sawing uses a ______ to remove a thickness of material slightly wider than itself.", ["bit", "core", "blade", "disc"], 2, "Câu 3: <em>using a blade</em>.")
blank(4, "The gap left by the blade, along the line of the cut, is called a ______.", ["kerf", "swarf", "chip", "bore"], 0, "Câu 4: <em>is called a kerf</em>.")
blank(5, "A hacksaw has a blade with very small ______, for cutting metal.", ["wheels", "holes", "teeth", "handles"], 2, "Câu 6: <em>very small teeth</em>.")
blank(6, "Grinding is removing material across a surface area, using ______ wheels.", ["rotating", "abrasive", "hollow", "fixed"], 1, "Câu cuối: <em>using abrasive wheels</em>.")

def tfset(n, sts, why):
    Q.append({"type": "true_false", "question": f"<b>{P2} · 2.2 Mark each statement True or False ({n}/2)</b><br>" + DET,
              "statements": [{"text": t, "answer": v} for t, v in sts], "explanation": why,
              "topic": TOPIC, "form": "ly_thuyet", "difficulty": "de"})
tfset(1, [("A milling machine holds the workpiece in a fixed position while the cutting tools rotate.", True),
          ("A kerf is the waste metal produced when a workpiece is cut.", False),
          ("Circular saws, band saws and power hacksaws all use toothed blades.", True),
          ("A hacksaw blade has very large teeth for cutting wood.", False)],
      "Milling: máy giữ phôi cố định, dao quay. Kerf là khe cắt (waste = swarf). Hacksaw: very small teeth, for cutting metal.")
tfset(2, [("Abrasive wheels used in sawing are often made of industrial diamond.", True),
          ("Grinding removes material using a lathe and a drill bit.", False),
          ("Sawing removes a thickness of material slightly wider than the blade.", True),
          ("In milling, the workpiece is rotated by a machine called a lathe.", False)],
      "Grinding dùng abrasive wheels (máy mài = grinder). Lathe dùng cho turning, không phải milling.")

def ask(n, q, opts, ans, why):
    p2(f"{P2} · 2.3 Choose the best answer ({n}/6)", q, opts, ans, why)
ask(1, "What does milling use to cut the workpiece?", ["Toothed cutting discs", "A rotating workpiece", "A liquid", "An industrial diamond"], 0, "<em>often using toothed cutting discs</em>.")
ask(2, "What is sawing?", ["Making new holes with a bit", "Cutting with a toothed blade", "Cutting with a rotating workpiece", "Removing a core of material"], 1, "<em>Sawing is cutting using a blade</em>, usually with teeth.")
ask(3, "What is a kerf?", ["A kind of saw", "A very hard wheel", "The gap left by the blade", "The material cut away as chips"], 2, "<em>The gap left by the blade</em>.")
ask(4, "Which machines use toothed blades?", ["Circular saws, band saws and power hacksaws", "Grinders and milling machines", "Lathes and drills", "Hole saws and grinders"], 0, "Câu 5 của đoạn.")
ask(5, "What is a hacksaw used for?", ["Grinding wheels", "Cutting metal with small teeth", "Cutting thick wood", "Making large holes"], 1, "<em>very small teeth, for cutting metal</em>.")
ask(6, "What are the abrasive wheels used in sawing often made of?", ["Soft steel", "Wood", "Industrial diamond", "Plastic"], 2, "<em>often made of industrial diamond</em>.")

# ---- Part 3: bản vẽ (1,5 điểm)
P3 = "Part 3 · Look at the technical drawing."
DR = f'<br><img src="{A}/shaft-drawing.svg" alt="Technical drawing of a stepped shaft" width="440">'
mc(P3, "What is the diameter of the smaller step of the shaft?" + DR, ["Ø20 mm", "Ø12 mm", "Ø25 mm", "Ø40 mm"], 1, "Đường kính nhỏ ghi <em>Ø12</em>.")
mc(P3, "What tolerance is applied to the Ø20 diameter?" + DR, ["±0.2 mm", "±0.1 mm", "±0.02 mm", "±1.6 mm"], 2, "Ghi <em>Ø20 ±0.02</em>; 1.6 là độ nhám Ra.")
mc(P3, "What is the length of the smaller step (Ø12)?" + DR, ["65 mm", "25 mm", "40 mm", "12 mm"], 1, "Bậc Ø12 dài <em>25</em>; 40 là bậc lớn, 65 là tổng chiều dài.")

# ---- Part 4: dịch (chọn bản dịch đúng)
P4 = "Part 4 · Choose the best Vietnamese translation."
mc(P4, "Machining is the use of machines to cut pieces of material (called workpieces) and shape them into components.",
   ["Gia công cắt gọt là dùng máy để cắt các mảnh vật liệu (gọi là phôi) và tạo hình chúng thành các chi tiết.",
    "Gia công cắt gọt là dùng tay để cắt các chi tiết và tạo hình chúng thành phôi.",
    "Máy gia công là các phôi được cắt thành những mảnh vật liệu nhỏ hơn.",
    "Phôi là công cụ dùng để cắt máy và tạo hình các chi tiết."], 0, "workpieces = phôi; components = chi tiết; machines = máy.")
mc(P4, "During machining, a liquid called cutting fluid may be pumped onto the workpiece to act as a coolant, keeping the workpiece cool.",
   ["Trong khi gia công, dung dịch cắt gọt được dùng để làm sạch phoi ra khỏi máy.",
    "Trong khi gia công, một chất lỏng gọi là dung dịch cắt gọt có thể được bơm lên phôi để làm chất làm mát, giữ cho phôi nguội.",
    "Khi phôi nguội, người ta bơm dung dịch cắt gọt vào máy để tăng tốc độ cắt.",
    "Chất làm mát là phôi được bơm lên máy trong lúc gia công."], 1, "cutting fluid = dung dịch cắt gọt; coolant = chất làm mát; pumped = được bơm.")

bundle = {"schema": "thachlab.lesson-bundle/v1",
 "target": {"class_name": "Anh văn chuyên ngành Cơ khí", "chapter_title": "Technical English for Mechanical Engineering",
            "lesson_title": "Chapter 8: Chipping Machining — Gia công cắt gọt"},
 "exam": {"title": "Kiểm tra Chapter 8: Chipping Machining", "topic": TOPIC, "difficulty": "de", "duration_minutes": 40,
          "subject_code": "avcn", "questions": Q, "new_topics": [TOPIC]},
 "theory_html": "", "worked_examples": [], "raster_images": []}
out = pathlib.Path(__file__).with_name("bundle-kiem-tra.json")
out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(Q), "câu →", out.name)
