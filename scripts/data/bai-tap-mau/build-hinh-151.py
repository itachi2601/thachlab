"""Bài tập mẫu Chuyên đề 06 "Khúc xạ ánh sáng, phản xạ toàn phần, lăng kính và tán sắc" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 151.
Dàn ý chung: content/hsg9/cd06-khuc-xa-phan-xa-toan-phan/nguon.md (số liệu mới tự đặt, không chép ví dụ docx).
Ba phần soạn song song, mỗi phần một module (mỗi module xuất DANG, BUILD, ANALYSIS, SOLS, STEPS, kiem_so):
  btm151_d123.py — Dạng 1–3 · btm151_d456.py — Dạng 4–7 · btm151_tl.py — tu_luan() (bài tự luận dễ → khó).
Module chưa có thì bỏ qua (để từng phần chạy thử được riêng).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-151.py   (idempotent; không ghi DB)"""
import importlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import write, inject

# Chạy thử riêng một phần (tránh hai agent ghi đè nhau): BTM151_ONLY=btm151_d456 BTM151_OUT=/tmp/x.json
ONLY = os.environ.get("BTM151_ONLY", "")
J = os.environ.get("BTM151_OUT") or os.path.join(HERE, "151.json")
DANG, BUILD, ANALYSIS, SOLS, STEPS = [], [], [], [], []
for name in ("btm151_d123", "btm151_d456"):
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
    if ONLY and ONLY != "btm151_tl":
        raise ModuleNotFoundError(name="btm151_tl")
    import btm151_tl
    TU_LUAN = btm151_tl.tu_luan()
    if hasattr(btm151_tl, "kiem_so"):
        btm151_tl.kiem_so()
except ModuleNotFoundError as e:
    if e.name != "btm151_tl":
        raise
    TU_LUAN = None

assert len(DANG) == len(BUILD) == len(ANALYSIS) == len(SOLS) == len(STEPS) > 0
write(J, 151, "Chuyên đề 06. Khúc xạ ánh sáng, phản xạ toàn phần, lăng kính và tán sắc", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-17"
REVIEW = os.path.join(HERE, "review-151.json")   # phiên chính ghi sau kiểm chéo
d["review"] = json.load(open(REVIEW)) if os.path.exists(REVIEW) else {"checked": False, "notes": "chờ kiểm chéo"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("ghi", J, len(d["dang_bai"]), "dạng")
