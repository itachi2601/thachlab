"""Bài tập mẫu Chuyên đề 15 "Âm thanh" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 150.
Dàn ý chung: content/hsg9/cd15-am-thanh/nguon.md (chuyên đề mới, không có docx nguồn).
Ba phần soạn song song, mỗi phần một module (mỗi module xuất DANG, BUILD, ANALYSIS, SOLS, STEPS, kiem_so):
  btm150_d123.py — Dạng 1–3 · btm150_d456.py — Dạng 4–6 · btm150_tl.py — tu_luan() (bài tự luận dễ → khó).
Module chưa có thì bỏ qua (để từng phần chạy thử được riêng).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-150.py   (idempotent; không ghi DB)"""
import importlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import write, inject

# Chạy thử riêng một phần (tránh hai agent ghi đè nhau): BTM150_ONLY=btm150_d456 BTM150_OUT=/tmp/x.json
ONLY = os.environ.get("BTM150_ONLY", "")
J = os.environ.get("BTM150_OUT") or os.path.join(HERE, "150.json")
DANG, BUILD, ANALYSIS, SOLS, STEPS = [], [], [], [], []
for name in ("btm150_d123", "btm150_d456"):
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
    if ONLY and ONLY != "btm150_tl":
        raise ModuleNotFoundError(name="btm150_tl")
    import btm150_tl
    TU_LUAN = btm150_tl.tu_luan()
    if hasattr(btm150_tl, "kiem_so"):
        btm150_tl.kiem_so()
except ModuleNotFoundError as e:
    if e.name != "btm150_tl":
        raise
    TU_LUAN = None

assert len(DANG) == len(BUILD) == len(ANALYSIS) == len(SOLS) == len(STEPS) > 0
write(J, 150, "Chuyên đề 15. Âm thanh: sóng âm, độ cao, độ to, phản xạ âm", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-16"
REVIEW = os.path.join(HERE, "review-150.json")   # phiên chính ghi sau kiểm chéo
d["review"] = json.load(open(REVIEW)) if os.path.exists(REVIEW) else {"checked": False, "notes": "chờ kiểm chéo"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("ghi", J, len(d["dang_bai"]), "dạng")
