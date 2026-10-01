#!/usr/bin/env python3
"""Kiểm kho thí nghiệm content/thi-nghiem/*.json, sinh index.json, và kiểm liên kết từ bài lý thuyết.
Dùng (từ gốc repo thachlab, nơi có content/thi-nghiem/):  python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/thi_nghiem.py [theory.html ...]
Mã thoát 1 nếu có lỗi. Chỉ dùng thư viện chuẩn."""
import json, re, sys, pathlib
_cwd = pathlib.Path.cwd()
ROOT = _cwd if (_cwd / "content" / "thi-nghiem").exists() else pathlib.Path(__file__).resolve().parents[4]
DIR = ROOT / "content" / "thi-nghiem"
LOAI = {"thi_nghiem", "vi_du"}
MUC_DO = {"co_ban", "trung_binh", "nang_cao"}
KIEU = {"dieu_chinh", "do_duoc", "tinh_ra", "co_dinh"}
SIM = {"2d_dong_hoc", "so_do_luc", "do_thi", "bang_so_lieu"}
BAT_BUOC = ["id", "ten", "loai", "muc_do", "mon", "lop", "bai", "kien_thuc", "muc_tieu", "dung_cu", "cac_buoc",
            "tham_so", "mo_hinh", "so_lieu_mau", "ket_qua_ky_vong", "hien_tuong_hay_sai", "goi_y_mo_phong"]
err, index = [], []
for f in sorted(DIR.glob("tn-*.json")):
    d = json.loads(f.read_text(encoding="utf8"))
    w = lambda m: err.append(f"{f.name}: {m}")
    for k in BAT_BUOC:
        if k not in d: w(f"thiếu trường {k}")
    if d.get("id") != f.stem: w("id phải trùng tên file")
    if d.get("loai") not in LOAI: w(f"loai phải thuộc {sorted(LOAI)}")
    if d.get("muc_do") not in MUC_DO: w(f"muc_do phải thuộc {sorted(MUC_DO)}")
    for kt in d.get("kien_thuc", []):
        if not re.fullmatch(r"[a-z0-9_]+\.[a-z0-9_]+", kt): w(f"kien_thuc '{kt}' phải dạng chu_de.y_nho (a-z, 0-9, _)")
    c = d.get("cac_buoc", {})
    for k in ("lam", "quan_sat", "rut_ra"):
        if not c.get(k): w(f"cac_buoc.{k} trống")
    ks = set()
    for t in d.get("tham_so", []):
        if t.get("kieu") not in KIEU: w(f"tham_so {t.get('ky_hieu')}: kieu sai")
        if t.get("ky_hieu") in ks: w(f"tham_so trùng ký hiệu {t.get('ky_hieu')}")
        ks.add(t.get("ky_hieu"))
        if t.get("kieu") == "dieu_chinh":
            for k in ("min", "max", "mac_dinh"):
                if k not in t: w(f"tham_so {t['ky_hieu']}: thiếu {k}")
            if all(k in t for k in ("min", "max", "mac_dinh")) and not t["min"] <= t["mac_dinh"] <= t["max"]:
                w(f"tham_so {t['ky_hieu']}: mac_dinh ngoài [min,max]")
        if t.get("kieu") == "co_dinh" and "gia_tri" not in t: w(f"tham_so {t['ky_hieu']}: thiếu gia_tri")
    if not any(t.get("kieu") == "dieu_chinh" for t in d.get("tham_so", [])): w("cần ít nhất 1 tham số điều chỉnh để mô phỏng")
    if not d.get("mo_hinh", {}).get("phuong_trinh"): w("mo_hinh.phuong_trinh trống")
    sl = d.get("so_lieu_mau", {})
    for r in sl.get("hang", []):
        if len(r) != len(sl.get("cot", [])): w(f"so_lieu_mau: hàng {r} lệch số cột")
    if d.get("goi_y_mo_phong", {}).get("loai", "").split("+")[0] not in SIM: w("goi_y_mo_phong.loai không hợp lệ")
    index.append({"id": d["id"], "ten": d["ten"], "loai": d["loai"], "muc_do": d["muc_do"], "lop": d["lop"], "bai": d["bai"],
                  "lesson_id": d.get("lesson_id"), "kien_thuc": d["kien_thuc"], "mo_phong": d["goi_y_mo_phong"]["loai"],
                  "tham_so_dieu_chinh": [t["ky_hieu"] for t in d["tham_so"] if t.get("kieu") == "dieu_chinh"]})
ids = {i["id"] for i in index}
for th in sys.argv[1:]:
    for m in re.findall(r'data-exp="([^"]+)"', pathlib.Path(th).read_text(encoding="utf8")):
        if m not in ids: err.append(f"{th}: data-exp '{m}' không có trong content/thi-nghiem/")
(DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"{len(index)} thí nghiệm/ví dụ → content/thi-nghiem/index.json")
for e in err: print("✗", e)
sys.exit(1 if err else 0)
