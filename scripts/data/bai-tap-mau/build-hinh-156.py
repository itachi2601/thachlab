"""Bài tập mẫu Chuyên đề 07 "Thấu kính mỏng và kính lúp" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 156.
Dàn ý chung: content/hsg9/cd07-thau-kinh-kinh-lup/nguon.md (+ tinh.py) (số liệu mới tự đặt, không chép ví dụ docx).
Ba phần soạn song song, mỗi phần một module (mỗi module xuất DANG, BUILD, ANALYSIS, SOLS, STEPS, kiem_so):
  btm156_d123.py — Dạng 1–3 · btm156_d456.py — Dạng 4–7 · btm156_tl.py — tu_luan() (bài tự luận dễ → khó).
Module chưa có thì bỏ qua (để từng phần chạy thử được riêng).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-156.py   (idempotent; không ghi DB)"""
import importlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import write, inject

# Chạy thử riêng một phần (tránh hai agent ghi đè nhau): BTM156_ONLY=btm156_d456 BTM156_OUT=/tmp/x.json
ONLY = os.environ.get("BTM156_ONLY", "")
J = os.environ.get("BTM156_OUT") or os.path.join(HERE, "156.json")
DANG, BUILD, ANALYSIS, SOLS, STEPS = [], [], [], [], []
for name in ("btm156_d123", "btm156_d456"):
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
    if ONLY and ONLY != "btm156_tl":
        raise ModuleNotFoundError(name="btm156_tl")
    import btm156_tl
    TU_LUAN = btm156_tl.tu_luan()
    if hasattr(btm156_tl, "kiem_so"):
        btm156_tl.kiem_so()
except ModuleNotFoundError as e:
    if e.name != "btm156_tl":
        raise
    TU_LUAN = None

assert len(DANG) == len(BUILD) == len(ANALYSIS) == len(SOLS) == len(STEPS)
assert DANG or ONLY == "btm156_tl", "không có dạng nào"
write(J, 156, "Chuyên đề 07. Thấu kính mỏng và kính lúp", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-17"
REVIEW = os.path.join(HERE, "review-156.json")   # phiên chính ghi sau kiểm chéo
d["review"] = json.load(open(REVIEW)) if os.path.exists(REVIEW) else {"checked": False, "notes": "chờ kiểm chéo"}
import re
_TXT = {"#fbbf24": "#b45309", "#fb923c": "#c2410c", "#38bdf8": "#0369a1", "#34d399": "#047857", "#f87171": "#b91c1c"}
def _dam(o):   # chữ trong SVG: màu đậm đọc rõ trên nền sáng (giống CĐ14); khối hình giữ màu
    if isinstance(o, str):
        return re.sub(r"<(?:text|tspan)\b[^>]*>", lambda m: re.sub(r"#(?:fbbf24|fb923c|38bdf8|34d399|f87171)\b", lambda c: _TXT[c.group(0)], m.group(0)), o)
    if isinstance(o, list): return [_dam(x) for x in o]
    if isinstance(o, dict): return {k: _dam(v) for k, v in o.items()}
    return o
d = _dam(d)
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("ghi", J, len(d["dang_bai"]), "dạng")
