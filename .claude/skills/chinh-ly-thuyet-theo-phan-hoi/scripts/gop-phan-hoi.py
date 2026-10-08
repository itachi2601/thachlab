#!/usr/bin/env python3
"""Gộp phản hồi của học sinh ảo (Gemini) cho một bài lý thuyết.

  python3 gop-phan-hoi.py content/lesson-samples/<bài>            # in góp ý chưa xử lý
  python3 gop-phan-hoi.py content/lesson-samples/<bài> --danh-dau  # ghi các file đã gộp vào da-xu-ly.json
"""
import json, sys, glob, os, collections

MUC = {"chặn": 0, "chan": 0, "khó": 1, "kho": 1, "nhỏ": 2, "nho": 2}
VAI_OK = {"yeu", "trung-binh", "kha"}
CAN = ("id", "vi_tri", "trich_nguyen_van", "loai", "muc", "de_xuat")

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    d = os.path.join(args[0], "phan-hoi-hs")
    if not os.path.isdir(d):
        sys.exit(f"Chưa có thư mục {d}")
    sổ_path = os.path.join(d, "da-xu-ly.json")
    sổ = json.load(open(sổ_path)) if os.path.exists(sổ_path) else {"files": [], "quyet_dinh": {}}
    files = sorted(f for f in glob.glob(os.path.join(d, "*.json"))
                   if os.path.basename(f) not in ("da-xu-ly.json", "dap-an-that.json"))
    moi = [f for f in files if os.path.basename(f) not in sổ["files"]]
    if not moi:
        print("Không có file phản hồi mới."); return
    dap_an = {}
    p = os.path.join(d, "dap-an-that.json")
    if os.path.exists(p):
        dap_an = json.load(open(p))

    nhom = collections.defaultdict(list)   # (vi_tri, loai) -> [(vai, gop_y)]
    quiz = collections.defaultdict(dict)   # cau -> {vai: đáp án}
    loi = 0
    for f in moi:
        try:
            j = json.load(open(f))
        except Exception as e:
            print(f"✗ {os.path.basename(f)}: JSON hỏng ({e})"); loi += 1; continue
        vai = j.get("vai", "?")
        if vai not in VAI_OK:
            print(f"! {os.path.basename(f)}: vai '{vai}' lạ")
        for c, a in (j.get("tra_loi_quiz") or {}).items():
            quiz[c][vai] = a
        print(f"• {os.path.basename(f)} · {vai} · ~{j.get('phut_doc_uoc_tinh','?')} phút · {len(j.get('gop_y',[]))} góp ý")
        for g in j.get("gop_y", []):
            thieu = [k for k in CAN if not g.get(k)]
            if thieu:
                print(f"  ! {g.get('id','?')} thiếu {thieu}"); 
            nhom[(g.get("vi_tri", "?"), g.get("loai", "?"))].append((vai, g))

    print("\n=== GÓP Ý GỘP (≥2 vai trước, rồi mức chặn→nhỏ) ===")
    def key(item):
        (vt, lo), ls = item
        vai_n = len({v for v, _ in ls})
        m = min(MUC.get(g.get("muc", "nhỏ"), 2) for _, g in ls)
        return (-vai_n, m)
    for (vt, lo), ls in sorted(nhom.items(), key=key):
        vais = sorted({v for v, _ in ls})
        m = min((g.get("muc", "nhỏ") for _, g in ls), key=lambda x: MUC.get(x, 2))
        print(f"\n[{m.upper()}] {vt} · {lo} · {len(vais)} vai ({', '.join(vais)})")
        for v, g in ls:
            print(f"  - {g.get('id','?')}/{v}: \"{g.get('trich_nguyen_van','')}\"")
            print(f"      hiểu: {g.get('em_hieu_la','')}")
            print(f"      sửa : {g.get('de_xuat','')}")

    print("\n=== QUIZ: đáp án các vai chọn ===")
    for c in sorted(quiz):
        row = ", ".join(f"{v}={a}" for v, a in sorted(quiz[c].items()))
        mark = ""
        if c in dap_an:
            sai = [v for v, a in quiz[c].items() if a != dap_an[c]]
            mark = f"  [đúng: {dap_an[c]}]" + (f"  ✗ sai: {', '.join(sai)}" if sai else "  ✓")
        print(f"  {c}: {row}{mark}")
    if dap_an:
        tb = [a for c, ans in quiz.items() if c in dap_an for v, a in ans.items() if v == "trung-binh" and True]
        tot = sum(1 for c, ans in quiz.items() if c in dap_an and "trung-binh" in ans and ans["trung-binh"] == dap_an[c])
        n = sum(1 for c, ans in quiz.items() if c in dap_an and "trung-binh" in ans)
        if n:
            print(f"  → vai trung-bình đúng {tot}/{n} ({100*tot//n}%). Mục tiêu ≥ 90%.")

    if "--danh-dau" in sys.argv and not loi:
        sổ["files"] += [os.path.basename(f) for f in moi]
        json.dump(sổ, open(sổ_path, "w"), ensure_ascii=False, indent=2)
        print(f"\nĐã ghi {sổ_path}. Điền 'quyet_dinh' cho từng id (chap_nhan|tu_choi|hoi_thay) + ghi chú.")

main()
