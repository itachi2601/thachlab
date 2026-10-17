"""Bài tập mẫu Chuyên đề 09 "Năng lượng với cuộc sống: vòng năng lượng Trái Đất, nhiên liệu và năng lượng tái tạo" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 163.
Dàn ý chung: content/hsg9/cd09-nang-luong-cuoc-song/nguon.md (+ tinh.py) (số liệu mới tự đặt, không chép ví dụ docx).
Ba phần soạn song song, mỗi phần một module (mỗi module xuất DANG, BUILD, ANALYSIS, SOLS, STEPS, kiem_so):
  btm163_d123.py — Dạng 1–3 · btm163_d456.py — Dạng 4 trở đi · btm163_tl.py — tu_luan() (bài tự luận dễ → khó).
Module chưa có thì bỏ qua (để từng phần chạy thử được riêng).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-163.py   (idempotent; không ghi DB)"""
import importlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import write, inject

# Chạy thử riêng một phần (tránh hai agent ghi đè nhau): BTM163_ONLY=btm163_d456 BTM163_OUT=/tmp/x.json
ONLY = os.environ.get("BTM163_ONLY", "")
J = os.environ.get("BTM163_OUT") or os.path.join(HERE, "163.json")
DANG, BUILD, ANALYSIS, SOLS, STEPS = [], [], [], [], []
for name in ("btm163_d123", "btm163_d456"):
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
    if ONLY and ONLY != "btm163_tl":
        raise ModuleNotFoundError(name="btm163_tl")
    import btm163_tl
    TU_LUAN = btm163_tl.tu_luan()
    if hasattr(btm163_tl, "kiem_so"):
        btm163_tl.kiem_so()
except ModuleNotFoundError as e:
    if e.name != "btm163_tl":
        raise
    TU_LUAN = None

assert len(DANG) == len(BUILD) == len(ANALYSIS) == len(SOLS) == len(STEPS) > 0
write(J, 163, "Chuyên đề 09. Năng lượng với cuộc sống: vòng năng lượng Trái Đất, nhiên liệu và năng lượng tái tạo", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-17"
REVIEW = os.path.join(HERE, "review-163.json")   # phiên chính ghi sau kiểm chéo
d["review"] = json.load(open(REVIEW)) if os.path.exists(REVIEW) else {"checked": False, "notes": "chờ kiểm chéo"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("ghi", J, len(d["dang_bai"]), "dạng")
