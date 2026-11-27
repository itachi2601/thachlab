#!/usr/bin/env python3
# Sau khi thầy duyệt lô "Cổng mới — L10a" mẻ 1 (13 clip, thầy duyệt 27/11/2026): đổi URL clip cũ → bản mới (lấy từ khung video-khung/<tn>.json, do
# tai-cong-moi-l10a.sh ghi) trong kho content/thi-nghiem/<tn>.json + bài (theory.src.html, theory.html, bundle.json),
# rồi gắn lại khung (gan-khung-video.mts --apply). KHÔNG ghi DB (việc của dang-cong-moi-l10a.sh).
#   python3 scripts/video-thi-nghiem/doi-cong-moi-l10a.py            # xem thử: in số chỗ sẽ đổi
#   python3 scripts/video-thi-nghiem/doi-cong-moi-l10a.py --apply    # ghi file + gắn khung
#   python3 scripts/video-thi-nghiem/doi-cong-moi-l10a.py --apply tn-l10-tdvt-01 ...   # chỉ vài clip
import json, os, re, subprocess, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
APPLY = "--apply" in sys.argv
CHI = [a for a in sys.argv[1:] if a.startswith("tn-")]
# tn → thư mục bài (content/lesson-samples). Mẻ sau thêm dòng vào bảng này.
BAI = {}
for slug, tns in {
    "l10-lam-quen-voi-vat-li": "lam-quen-02", "l10-an-toan-phong-thuc-hanh": "an-toan-01 an-toan-02",
    "l10-thuc-hanh-sai-so": "sai-so-01 sai-so-02", "l10-do-dich-chuyen-quang-duong": "dd-qd-01",
    "l10-toc-do-van-toc": "tdvt-01 tdvt-03", "l10-thuc-hanh-do-toc-do": "do-toc-do-01",
    "l10-do-thi-dich-chuyen-thoi-gian": "dt-dctg-01 dt-dctg-02", "l10-chuyen-dong-bien-doi-gia-toc": "gia-toc-01 gia-toc-02",
}.items():
    for t in tns.split():
        BAI["tn-l10-" + t] = slug
loi = 0; can_gan = {}
for tn, slug in BAI.items():
    if CHI and tn not in CHI: continue
    kho_p = f"content/thi-nghiem/{tn}.json"
    moi = json.load(open(f"content/thi-nghiem/video-khung/{tn}.json", encoding="utf-8"))["video"]
    cu = json.load(open(kho_p, encoding="utf-8"))["video"]["mp4"]
    if not re.search(r"-2026112[7-9](-\d)?\.mp4$|-202612\d\d(-\d)?\.mp4$", moi):
        print(f"LOI {tn}: khung chưa trỏ bản mới ({moi[-36:]}) — chạy tai-cong-moi-l10a.sh trước"); loi += 1; continue
    if cu == moi:
        print(f"{tn}: đã đổi rồi"); can_gan.setdefault(slug, []).append(tn); continue
    cu0, moi0 = cu[:-4], moi[:-4]
    d = f"content/lesson-samples/{slug}"
    files = [kho_p] + [os.path.normpath(f"{d}/{f}") for f in ("theory.src.html", "theory.html", "bundle.json") if os.path.exists(f"{d}/{f}")]
    tong = 0
    for f in files:
        s = open(f, encoding="utf-8").read(); n = s.count(cu0)
        if f == kho_p and n == 0: print(f"LOI {tn}: kho không chứa URL cũ"); loi += 1
        if f.endswith("theory.src.html") and n == 0: print(f"LOI {tn}: {f} không chứa URL cũ")
        tong += n
        if APPLY and n: open(f, "w", encoding="utf-8").write(s.replace(cu0, moi0))
    print(f"{tn}: {cu0[-28:]} → {moi0[-28:]} · {tong} chỗ / {len(files)} file")
    can_gan.setdefault(slug, []).append(tn)
for slug, tns in can_gan.items():
    cmd = ["npx", "tsx", "scripts/gan-khung-video.mts", "--bai", slug, "--id", ",".join(tns)] + (["--apply"] if APPLY else [])
    print("==", " ".join(cmd))
    if APPLY and subprocess.run(cmd).returncode: print(f"LOI gắn khung {slug}"); loi += 1
print(f"XONG. LOI: {loi}" + ("" if APPLY else " (xem thử — thêm --apply để ghi)"))
sys.exit(1 if loi else 0)
