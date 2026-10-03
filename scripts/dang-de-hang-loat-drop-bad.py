#!/usr/bin/env python3
# Đăng cả thư mục đề đã Azota lên mục 277, tự bỏ câu thiếu đáp án/thiếu hình (skill dang-de-hang-loat).
#   python3 scripts/dang-de-hang-loat-drop-bad.py [--limit N] [--offset K] [--dry]
import json, os, re, shutil, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/MAC/Documents/THPT/số hoá THPT/các đề đã xong"
MTEF = "/Users/MAC/Documents/THPT/Lop12/NamHoc/2026-2027/06_Azota_so_hoa/_CongCu/mtef_to_omml_v2.py"
AZ = "/Users/MAC/.codex/skills/azota/scripts"
LOG = os.path.join(ROOT, "scripts/data/bulk-de-thi-thu-log.json")
args = sys.argv[1:]
def opt(n, d=None): return args[args.index(n) + 1] if n in args else d
limit, offset, dry = int(opt("--limit", 10**6)), int(opt("--offset", 0)), "--dry" in args
log = json.load(open(LOG))
files = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".docx") and not f.startswith("~$") and f not in log)
files = files[offset:offset + limit]
def title_of(f):
    n = re.sub(r"_Azota\.docx$|\.docx$", "", f); n = re.sub(r"^\d+\.\s*", "", n).strip()
    return "Thi thử TN – " + n.title().replace("Thpt", "THPT").replace("Gd&Dt", "GD&ĐT")
res = {}
for f in files:
    w = tempfile.mkdtemp(prefix="dd_")
    try:
        shutil.copy(os.path.join(SRC, f), f"{w}/de_goc.docx")
        def run(cmd, **k): return subprocess.run(cmd, capture_output=True, text=True, **k)
        run(["python3", MTEF, "convert", f"{w}/de_goc.docx"])
        c = run(["python3", f"{AZ}/convert_docx.py", f"{w}/de_goc.docx", f"{w}/de_azota.docx"])
        if c.returncode: res[f] = "convert lỗi: " + c.stderr[-200:]; print("✕", f, res[f], flush=True); continue
        open(f"{w}/nhan.json", "w").write("{}")
        x = run(["python3", f"{AZ}/xuat_thachlab.py", f"{w}/de_azota.docx", f"{w}/nhan.json", f"{w}/out.docx"])
        if x.returncode or not os.path.exists(f"{w}/out.docx"): res[f] = "xuất lỗi: " + x.stderr[-200:]; print("✕", f, res[f], flush=True); continue
        cmd = ["npx", "tsx", "scripts/upload-exam-docx.mts", f"{w}/out.docx", "--title", title_of(f), "--lesson", "132", "--item", "277",
               "--duration", "50", "--drop-bad", "--log", LOG, "--src", f]
        if dry: cmd.append("--dry")
        u = run(cmd, cwd=ROOT)
        out = (u.stdout + u.stderr).strip().splitlines()
        tag = {0: "OK", 2: "SKIP>20%", 3: "TRÙNG"}.get(u.returncode, "LỖI")
        res[f] = tag + " | " + (out[-1] if out else "")
        print(f"[{tag}] {f} :: {out[-1] if out else ''}", flush=True)
    finally:
        shutil.rmtree(w, ignore_errors=True)
json.dump(res, open(os.path.join(ROOT, "scripts/data/bulk-de-thi-thu-run-2026-10-03.json"), "w"), ensure_ascii=False, indent=1)
