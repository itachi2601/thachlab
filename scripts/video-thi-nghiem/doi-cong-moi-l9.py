#!/usr/bin/env python3
# Sau khi thầy duyệt lô "Cổng mới — L9" (27/11/2026): đổi URL clip cũ → bản mới (lấy từ khung video-khung/<tn>.json, do
# tai-cong-moi-l9.sh ghi) trong kho content/thi-nghiem/<tn>.json + bài (theory.src.html, theory.html, bundle.json),
# rồi gắn lại khung (gan-khung-video.mts --apply). KHÔNG ghi DB (việc của dang-cong-moi-l9.sh).
#   python3 scripts/video-thi-nghiem/doi-cong-moi-l9.py            # xem thử: in số chỗ sẽ đổi
#   python3 scripts/video-thi-nghiem/doi-cong-moi-l9.py --apply    # ghi file + gắn khung
#   python3 scripts/video-thi-nghiem/doi-cong-moi-l9.py --apply tn-l9-ohm-01 ...   # chỉ vài clip
import json, os, re, subprocess, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
APPLY = "--apply" in sys.argv
CHI = [a for a in sys.argv[1:] if a.startswith("tn-")]
# tn → thư mục bài (tương đối content/lesson-samples; hsg9 đi đường ../hsg9)
BAI = {}
for slug, tns in {
    "l9-dien-tro-dinh-luat-ohm": "ohm-01 ohm-02 ohm-03", "l9-doan-mach-noi-tiep-song-song": "doanmach-01 doanmach-02 doanmach-03",
    "l9-nang-luong-dong-dien-cong-suat": "congsuat-01 congsuat-03", "l9-dong-nang-the-nang": "dongthe-01 dongthe-02 dongthe-03",
    "l9-cam-ung-dien-tu": "camung-01 camung-02 camung-03", "l9-tac-dung-dong-dien-xoay-chieu": "xoaychieu-01 xoaychieu-02",
    "l9-vong-nang-luong-hoa-thach": "hoathach-01 hoathach-02", "l9-co-nang": "conang-01 conang-02 conang-03",
    "l9-cong-cong-suat": "congco-01", "l9-mo-dau-dung-cu-thuyet-trinh": "modau-01 modau-02",
    "../hsg9/cd15-am-thanh": "hsgamthanh-01 hsgamthanh-02", "l9-nang-luong-tai-tao": "taitao-01 taitao-02",
    "l9-kinh-lup-bai-tap-thau-kinh": "kinhlup-01", "l9-lang-kinh-tan-sac": "langkinh-01 langkinh-03",
    "l9-phan-xa-toan-phan": "pxtp-01", "l9-thau-kinh": "thaukinh-02 thaukinh-03", "l9-thuc-hanh-tieu-cu": "tieucu-02 tieucu-03",
}.items():
    for t in tns.split():
        BAI["tn-l9-" + t] = slug
loi = 0; can_gan = {}
for tn, slug in BAI.items():
    if CHI and tn not in CHI: continue
    kho_p = f"content/thi-nghiem/{tn}.json"
    moi = json.load(open(f"content/thi-nghiem/video-khung/{tn}.json", encoding="utf-8"))["video"]
    cu = json.load(open(kho_p, encoding="utf-8"))["video"]["mp4"]
    if not re.search(r"-2026112[7-9](-\d)?\.mp4$|-202612\d\d(-\d)?\.mp4$", moi):
        print(f"LOI {tn}: khung chưa trỏ bản mới ({moi[-36:]}) — chạy tai-cong-moi-l9.sh trước"); loi += 1; continue
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
