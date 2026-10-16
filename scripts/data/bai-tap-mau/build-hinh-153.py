"""Bài tập mẫu Chuyên đề 12 "Nhiệt học nâng cao: cân bằng nhiệt và chuyển thể" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 153.
Dàn ý chung: content/hsg9/cd12-nhiet-hoc/nguon.md (số liệu mới tự đặt, không chép ví dụ docx).
Ba phần soạn song song, mỗi phần một module (mỗi module xuất DANG, BUILD, ANALYSIS, SOLS, STEPS, kiem_so):
  btm153_d123.py — Dạng 1–3 · btm153_d456.py — Dạng 4–6 · btm153_tl.py — tu_luan() (bài tự luận dễ → khó).
Module chưa có thì bỏ qua (để từng phần chạy thử được riêng).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-153.py   (idempotent; không ghi DB)"""
import importlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import write, inject

# Chạy thử riêng một phần (tránh hai agent ghi đè nhau): BTM153_ONLY=btm153_d456 BTM153_OUT=/tmp/x.json
ONLY = os.environ.get("BTM153_ONLY", "")
J = os.environ.get("BTM153_OUT") or os.path.join(HERE, "153.json")
DANG, BUILD, ANALYSIS, SOLS, STEPS = [], [], [], [], []
for name in ("btm153_d123", "btm153_d456"):
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
    if ONLY and ONLY != "btm153_tl":
        raise ModuleNotFoundError(name="btm153_tl")
    import btm153_tl
    TU_LUAN = btm153_tl.tu_luan()
    if hasattr(btm153_tl, "kiem_so"):
        btm153_tl.kiem_so()
except ModuleNotFoundError as e:
    if e.name != "btm153_tl":
        raise
    TU_LUAN = None

assert len(DANG) == len(BUILD) == len(ANALYSIS) == len(SOLS) == len(STEPS) > 0
write(J, 153, "Chuyên đề 12. Nhiệt học nâng cao: cân bằng nhiệt và chuyển thể", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-16"
REVIEW = os.path.join(HERE, "review-153.json")   # phiên chính ghi sau kiểm chéo
d["review"] = json.load(open(REVIEW)) if os.path.exists(REVIEW) else {"checked": False, "notes": "chờ kiểm chéo"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("ghi", J, len(d["dang_bai"]), "dạng")
