#!/usr/bin/env python3
"""Cổng mới L11a (27/11/2026): đổi kho + bài sang bản clip mới đã tải (Storage), rồi gắn lại khung.

Với mỗi tn trong LO: lấy URL `video` của khung `content/thi-nghiem/video-khung/<tn>.json` (đã trỏ bản mới),
thay mọi URL `lesson-clips/clip/<tn>-<ngày>[-n].(mp4|webp)` cũ trong kho `content/thi-nghiem/<tn>.json`
và trong theory.src.html / theory.html / bundle.json của bài chứa tn (chèn chữ, giữ định dạng gốc).
Sau đó chạy `npx tsx scripts/gan-khung-video.mts --bai <slug> --id <tn> --apply` để data-khung theo khung mới.

Dùng (từ gốc repo):  python3 scripts/video-thi-nghiem/doi-ban-cong-moi-l11a.py [--apply] [tn ...]
Không --apply: chỉ in số chỗ sẽ đổi.
"""
import json, re, subprocess, sys
from pathlib import Path

LO = {  # tn -> slug bài
    "tn-l11-daodongdieuhoa-01": "l11-dao-dong-dieu-hoa", "tn-l11-daodongdieuhoa-03": "l11-dao-dong-dieu-hoa",
    "tn-l11-motadddh-01": "l11-mo-ta-dao-dong", "tn-l11-motadddh-02": "l11-mo-ta-dao-dong",
    "tn-l11-vantocdddh-01": "l11-van-toc-gia-toc", "tn-l11-vantocdddh-02": "l11-van-toc-gia-toc",
    "tn-l11-baitapdaodong-01": "l11-bai-tap-dao-dong", "tn-l11-baitapdaodong-02": "l11-bai-tap-dao-dong",
    "tn-l11-baitapdaodong-03": "l11-bai-tap-dao-dong",
    "tn-l11-conangdddh-01": "l11-co-nang-dao-dong", "tn-l11-conangdddh-02": "l11-co-nang-dao-dong",
    "tn-l11-tatdan-01": "l11-tat-dan-cuong-buc", "tn-l11-tatdan-02": "l11-tat-dan-cuong-buc",
    "tn-l11-tatdan-03": "l11-tat-dan-cuong-buc",
    "tn-l11-baitapnangluong-01": "l11-bai-tap-nang-luong-dao-dong",
    "tn-l11-baitapnangluong-02": "l11-bai-tap-nang-luong-dao-dong",
    "tn-l11-songngangdoc-02": "l11-song-ngang-song-doc", "tn-l11-dotansoam-02": "l11-thuc-hanh-do-tan-so-am",
    "tn-l11-giaothoa-03": "l11-giao-thoa-song", "tn-l11-songdung-01": "l11-song-dung",
    "tn-l11-baitapsong-04": "l11-bai-tap-song",
}
ROOT = Path(__file__).resolve().parents[2]
args = [a for a in sys.argv[1:] if not a.startswith("--")]
apply = "--apply" in sys.argv
ds = args or list(LO)
loi = 0
for tn in ds:
    moi = json.loads((ROOT / f"content/thi-nghiem/video-khung/{tn}.json").read_text(encoding="utf-8"))["video"]
    ten_moi = re.search(rf"/({re.escape(tn)}-[0-9]{{8}}(?:-[0-9]+)?)\.mp4$", moi)
    if not ten_moi:
        print(f"LOI {tn}: khung video lạ {moi}"); loi += 1; continue
    ten_moi = ten_moi.group(1)
    pat = re.compile(rf"(lesson-clips/clip/){re.escape(tn)}-[0-9]{{8}}(?:-[0-9]+)?\.(mp4|webp)")
    files = [ROOT / f"content/thi-nghiem/{tn}.json"] + [
        ROOT / f"content/lesson-samples/{LO[tn]}/{f}" for f in ("theory.src.html", "theory.html", "bundle.json")]
    tong = 0
    for p in files:
        s = p.read_text(encoding="utf-8")
        s2, n = pat.subn(lambda m: f"{m.group(1)}{ten_moi}.{m.group(2)}", s)
        tong += n
        if n == 0 and p.name != "bundle.json":
            print(f"  ! {tn}: không thấy URL cũ trong {p.relative_to(ROOT)}")
        if apply and s2 != s:
            p.write_text(s2, encoding="utf-8")
    print(f"{tn} → {ten_moi}: {tong} chỗ")
    if apply:
        r = subprocess.run(["npx", "tsx", "scripts/gan-khung-video.mts", "--bai", LO[tn], "--id", tn, "--apply"],
                           cwd=ROOT, capture_output=True, text=True)
        print("  gan-khung:", (r.stdout + r.stderr).strip().splitlines()[-1:] or "(trống)")
        if r.returncode:
            loi += 1
print("XONG, lỗi:", loi)
