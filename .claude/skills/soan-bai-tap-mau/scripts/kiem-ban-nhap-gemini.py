#!/usr/bin/env python3
"""Kiểm bản nháp bài tập mẫu do Gemini viết (trước khi Claude dựng).

  python3 kiem-ban-nhap-gemini.py scripts/data/bai-tap-mau/gemini/<lesson_id>.json

Bắt: JSON/thiếu trường · tính lại `kiem_tinh` · đáp số lệch kiem_tinh · trích_đề không có trong đề ·
hàng "cần tìm" lộ số · từ cấm (thầy/cô) · `<`/`>` trong $…$ · yccd không khớp danh mục (gợi ý gần nhất).
Thoát 1 nếu có lỗi (✗); cảnh báo (!) không chặn.
"""
import json, sys, re, math, os, difflib

CAN = ("label", "cap_do", "de_bai", "phan_tich", "can_tim", "cac_buoc", "dap_so", "kiem_tinh", "nhan_dang", "mo_phong_goi_y")
CAM = re.compile(r"\b(thầy|cô giáo|cô)\b", re.I)
SAFE = {"math": math, "abs": abs, "round": round, "min": min, "max": max, "pow": pow, "sum": sum}

def lay_chu(x):
    return json.dumps(x, ensure_ascii=False) if not isinstance(x, str) else x

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    try:
        j = json.load(open(path))
    except Exception as e:
        sys.exit(f"✗ JSON hỏng: {e}")
    lid = None
    m = re.search(r"(\d+)\.json$", path)
    if m: lid = int(m.group(1))
    topics = []
    tp = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "scripts", "data", "question-topics.json")
    if os.path.exists(tp):
        topics = [t for t in json.load(open(tp)) if lid is None or t["lesson_id"] == lid]
    names = [t["name"] for t in topics]

    err = warn = 0
    err_pre = 0
    def E(msg):
        nonlocal err; err += 1; print("  ✗", msg)
    def W(msg):
        nonlocal warn; warn += 1; print("  !", msg)

    dang = j.get("dang_bai") or []
    if len(dang) != 4:
        print(f"! số dạng = {len(dang)} (hệ bắc cầu cần ĐÚNG 4)")
    caps = [d.get("cap_do") for d in dang]
    if caps != [1, 2, 3, 4][:len(dang)]:
        print(f"✗ cap_do phải là 1,2,3,4 theo thứ tự, hiện là {caps}"); err_pre = 1
    for i, d in enumerate(dang, 1):
        print(f"\n[Dạng {i}] {d.get('label','?')}")
        for k in CAN:
            if not d.get(k): E(f"thiếu '{k}'")
        de = d.get("de_bai", "")
        full = lay_chu(d)
        if CAM.search(full): E("dùng vai 'thầy/cô' (bị cấm)")
        for blk in re.findall(r"\$([^$]+)\$", full):
            if re.search(r"(?<!\\)[<>]", blk) and not re.search(r"\\(lt|gt|leq|geq|le|ge)", blk):
                E(f"'<'/'>' trong công thức: ${blk[:40]}$ → dùng \\lt/\\gt"); break
        # trích đề phải có trong đề
        for r in d.get("phan_tich", []):
            t = (r.get("trich_de") or "").strip()
            if t and t not in de: W(f"trích đề không có nguyên văn trong đề: «{t[:40]}»")
        ct = d.get("can_tim") or {}
        if re.search(r"\d\s*(,\d+|\.\d+)?\s*\\?\s*(text)?\{?\s*(m|km|s|kg|N|J|W|cm|h)\b", lay_chu(ct.get("cong_thuc", ""))):
            W("'cần tìm' có vẻ chứa số/đơn vị (chỉ nên ghi công thức)")
        # tính lại
        kt = d.get("kiem_tinh") or []
        val = {}
        for k in kt:
            try:
                v = eval(k["bieu_thuc"], {"__builtins__": {}}, SAFE)
            except Exception as e:
                E(f"kiem_tinh «{k.get('mo_ta')}» lỗi chạy: {e}"); continue
            kv = k.get("ky_vong"); tol = k.get("sai_so_tuong_doi", 0.01)
            ok = kv is not None and (abs(v - kv) <= tol * max(abs(kv), 1e-12) or abs(v - kv) < 1e-9)
            print(f"  {'✓' if ok else '✗'} {k.get('mo_ta')}: máy = {v:.6g}, nháp = {kv}")
            if not ok: E("lệch số học")
            val[k.get("mo_ta")] = v
        # đáp số có nằm trong kiem_tinh không
        kv_all = [k.get("ky_vong") for k in kt if k.get("ky_vong") is not None]
        for a in d.get("dap_so", []):
            g = a.get("gia_tri")
            if isinstance(g, (int, float)) and kv_all:
                if not any(abs(g - x) <= 0.01 * max(abs(x), 1e-12) for x in kv_all):
                    W(f"đáp số ý {a.get('y')} = {g} không khớp mục nào của kiem_tinh (chưa được máy kiểm)")
        # yccd
        y = d.get("yccd_de_xuat", "")
        if names and y:
            if y not in names:
                gan = difflib.get_close_matches(y, names, n=3, cutoff=0.3)
                W(f"yccd '{y}' chưa có trong danh mục lesson {lid}; gần nhất: {gan}")
            elif sum(1 for n in names if n == y) == 1:
                pass
        if d.get("cap_do", 1) > 1 and not d.get("cau_noi"):
            W("thiếu 'cau_noi' (dạng này dùng lại gì từ dạng trước, thêm gì mới)")
        if d.get("dieu_ban_khong_chac"):
            W("Gemini tự khai chỗ không chắc: " + "; ".join(d["dieu_ban_khong_chac"])[:200])
    print(f"\nTổng: {err} lỗi, {warn} cảnh báo")
    sys.exit(1 if (err or err_pre) else 0)

main()
