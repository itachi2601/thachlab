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
VI_TRI = re.compile(r"^(mo_bai|truoc:.+|sau:.+)$")

def kiem_video(v, ten_truong, w):
    """Kiểm một mục video (dùng cho cả tn-*.json và video-theo-bai.json)."""
    yid = v.get("youtube_id", "")
    if not re.fullmatch(r"[\w-]{11}", str(yid)): w(f"{ten_truong}.youtube_id '{yid}' phải là 11 ký tự YouTube")
    if not v.get("nhin_vao"): w(f"{ten_truong}.nhin_vao trống — phải có câu hướng chú ý cho học sinh")
    elif len(str(v["nhin_vao"]).split()) > 40: w(f"{ten_truong}.nhin_vao dài quá 40 từ")
    st, en = v.get("giay_bat_dau"), v.get("giay_ket_thuc")
    for k, x in (("giay_bat_dau", st), ("giay_ket_thuc", en)):
        if x is not None and (not isinstance(x, (int, float)) or isinstance(x, bool) or x < 0):
            w(f"{ten_truong}.{k} phải là số ≥ 0")
    if isinstance(st, (int, float)) and isinstance(en, (int, float)) and not isinstance(st, bool) and not isinstance(en, bool):
        if en <= st: w(f"{ten_truong}.giay_ket_thuc phải lớn hơn giay_bat_dau")
        elif en - st > 120: w(f"{ten_truong} dài {en - st:.0f}s > 120s — cắt ngắn lại")

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
    v = d.get("video")
    if v is not None:
        if not isinstance(v, dict):
            w("video phải là object")
        else:
            kiem_video(v, "video", w)
    index.append({"id": d["id"], "ten": d["ten"], "loai": d["loai"], "muc_do": d["muc_do"], "lop": d["lop"], "bai": d["bai"],
                  "lesson_id": d.get("lesson_id"), "kien_thuc": d["kien_thuc"], "mo_phong": d["goi_y_mo_phong"]["loai"],
                  "co_video": bool(d.get("video")),
                  "tham_so_dieu_chinh": [t["ky_hieu"] for t in d["tham_so"] if t.get("kieu") == "dieu_chinh"]})
ids = {i["id"] for i in index}
for th in sys.argv[1:]:
    for m in re.findall(r'data-exp="([^"]+)"', pathlib.Path(th).read_text(encoding="utf8")):
        if m not in ids: err.append(f"{th}: data-exp '{m}' không có trong content/thi-nghiem/")
pool = DIR / "video-dung-chung.json"
if pool.exists():
    for n, v in enumerate(json.loads(pool.read_text(encoding="utf8")).get("videos", [])):
        if not re.fullmatch(r"[\w-]{11}", str(v.get("youtube_id", ""))):
            err.append(f"video-dung-chung.json: mục {n} youtube_id không hợp lệ")
theo_bai = DIR / "video-theo-bai.json"
if theo_bai.exists():
    giu = ROOT / "content" / "lesson-samples"
    for b in json.loads(theo_bai.read_text(encoding="utf8")).get("bai", []):
        slug = str(b.get("slug", ""))
        if not slug or (giu.exists() and not (giu / slug).is_dir()):
            err.append(f"video-theo-bai.json: slug '{slug}' không có thư mục trong content/lesson-samples/")
        for m in b.get("videos", []):
            vt = str(m.get("vi_tri", ""))
            if not VI_TRI.fullmatch(vt):
                err.append(f"video-theo-bai.json [{slug}]: vi_tri '{vt}' phải là mo_bai | truoc:<data-exp> | sau:<data-exp>")
            kiem_video(m.get("video") or {}, f"video-theo-bai.json [{slug}] {vt}", err.append)
(DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"{len(index)} thí nghiệm/ví dụ → content/thi-nghiem/index.json")
for e in err: print("✗", e)
sys.exit(1 if err else 0)
