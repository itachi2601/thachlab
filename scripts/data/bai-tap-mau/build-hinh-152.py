"""Bài tập mẫu Chuyên đề 08 "Cảm ứng điện từ và dòng điện xoay chiều" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 152.
Dàn ý chung: content/hsg9/cd08-cam-ung-dien-tu/nguon.md (số liệu mới tự đặt, không chép ví dụ docx).
Ba phần soạn song song, mỗi phần một module (mỗi module xuất DANG, BUILD, ANALYSIS, SOLS, STEPS, kiem_so):
  btm152_d123.py — Dạng 1–3 · btm152_d456.py — Dạng 4–6 · btm152_tl.py — tu_luan() (bài tự luận dễ → khó).
Module chưa có thì bỏ qua (để từng phần chạy thử được riêng).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-152.py   (idempotent; không ghi DB)"""
import importlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import write, inject

# Chạy thử riêng một phần (tránh hai agent ghi đè nhau): BTM152_ONLY=btm152_d456 BTM152_OUT=/tmp/x.json
ONLY = os.environ.get("BTM152_ONLY", "")
J = os.environ.get("BTM152_OUT") or os.path.join(HERE, "152.json")
DANG, BUILD, ANALYSIS, SOLS, STEPS = [], [], [], [], []
for name in ("btm152_d123", "btm152_d456"):
    if ONLY and name != ONLY:
        continue
    try:
        m = importlib.import_module(name)
    except ModuleNotFoundError as e:
        if e.name != name:
            raise
        print("bỏ qua", name, "(chưa có)")
        continue
    m.kiem_so()
    DANG += m.DANG; BUILD += m.BUILD; ANALYSIS += m.ANALYSIS; SOLS += m.SOLS; STEPS += m.STEPS
try:
    if ONLY and ONLY != "btm152_tl":
        raise ModuleNotFoundError(name="btm152_tl")
    import btm152_tl
    TU_LUAN = btm152_tl.tu_luan()
    if hasattr(btm152_tl, "kiem_so"):
        btm152_tl.kiem_so()
except ModuleNotFoundError as e:
    if e.name != "btm152_tl":
        raise
    TU_LUAN = None

assert len(DANG) == len(BUILD) == len(ANALYSIS) == len(SOLS) == len(STEPS)
assert DANG or ONLY == "btm152_tl", "không có dạng nào"
write(J, 152, "Chuyên đề 08. Cảm ứng điện từ và dòng điện xoay chiều", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-17"
REVIEW = os.path.join(HERE, "review-152.json")   # phiên chính ghi sau kiểm chéo
d["review"] = json.load(open(REVIEW)) if os.path.exists(REVIEW) else {"checked": False, "notes": "chờ kiểm chéo"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("ghi", J, len(d["dang_bai"]), "dạng")
