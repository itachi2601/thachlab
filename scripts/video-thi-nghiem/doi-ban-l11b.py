#!/usr/bin/env python3
"""Cổng mới L11b (27/11/2026): sau khi thầy duyệt, đổi kho + bài sang bản clip mới rồi gắn lại khung.

Bản mới lấy từ trường "video" của khung `content/thi-nghiem/video-khung/<tn>.json` (tai-cong-moi-l11b.sh đã ghi sau khi tải).
Mỗi clip: thay mọi `clip/<tn>-<ngày>[-N].mp4|.webp` trong kho `<tn>.json`, `theory.src.html`, `theory.html`, `bundle.json` của bài
(bài lấy từ `nguon_trong_bai` của kho) bằng bản mới; rồi `gan-khung-video.mts --bai <slug> --id <tn> --apply`.

  /usr/bin/python3 scripts/video-thi-nghiem/doi-ban-l11b.py            # xem thử: in số chỗ sẽ thay
  /usr/bin/python3 scripts/video-thi-nghiem/doi-ban-l11b.py --apply    # ghi file + gắn khung
  ... --apply tn-l11-tudien-01 tn-l11-ohm-02                            # chỉ vài clip
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LO = """tn-l11-coulomb-01 tn-l11-coulomb-02 tn-l11-cuong-do-dong-dien-02 tn-l11-dien-the-01 tn-l11-dien-the-02
tn-l11-dien-tro-ohm-01 tn-l11-dien-tro-ohm-02 tn-l11-dien-tro-ohm-03 tn-l11-dien-truong-02 tn-l11-dien-truong-deu-01
tn-l11-dien-truong-deu-02 tn-l11-dien-truong-deu-03 tn-l11-do-sdd-pin-01 tn-l11-do-sdd-pin-02 tn-l11-dotocdoam-01
tn-l11-dotocdoam-03 tn-l11-nang-luong-dien-02 tn-l11-nang-luong-dien-03 tn-l11-nguon-dien-01 tn-l11-nguon-dien-02
tn-l11-nguon-dien-03 tn-l11-the-nang-dien-01 tn-l11-tudien-01 tn-l11-tudien-02 tn-l11-tudien-03 tn-l12-tdhphantu-04""".split()

args = [a for a in sys.argv[1:] if not a.startswith("--")]
APPLY = "--apply" in sys.argv
lo = args or LO
loi = 0
for tn in lo:
    khung_p = ROOT / f"content/thi-nghiem/video-khung/{tn}.json"
    kho_p = ROOT / f"content/thi-nghiem/{tn}.json"
    if not khung_p.exists():
        print(f"LOI {tn}: thiếu khung"); loi += 1; continue
    mp4 = json.loads(khung_p.read_text(encoding="utf-8"))["video"]
    m = re.search(rf"clip/({re.escape(tn)}-\d{{8}}(?:-\d+)?)\.mp4$", mp4)
    if not m:
        print(f"LOI {tn}: URL khung lạ {mp4}"); loi += 1; continue
    moi = m.group(1)
    kho = json.loads(kho_p.read_text(encoding="utf-8"))
    bai = Path(kho["nguon_trong_bai"]).parent
    pat = re.compile(rf"clip/{re.escape(tn)}-\d{{8}}(?:-\d+)?\.(mp4|webp)")
    tong = 0
    for p in [kho_p, ROOT / bai / "theory.src.html", ROOT / bai / "theory.html", ROOT / bai / "bundle.json"]:
        s = p.read_text(encoding="utf-8")
        cu = sorted({x.group(0) for x in pat.finditer(s)})
        n = len(pat.findall(s))
        s2 = pat.sub(lambda x: f"clip/{moi}.{x.group(1)}", s)
        tong += n
        print(f"  {tn} {p.relative_to(ROOT)}: {n} chỗ {cu} → {moi}")
        if APPLY and s2 != s:
            p.write_text(s2, encoding="utf-8")
    if tong == 0:
        print(f"LOI {tn}: không thấy URL cũ nào"); loi += 1; continue
    if APPLY:
        r = subprocess.run(["npx", "tsx", "scripts/gan-khung-video.mts", "--bai", bai.name, "--id", tn, "--apply"],
                           cwd=ROOT, capture_output=True, text=True)
        print(r.stdout.strip()[-400:])
        if r.returncode:
            print(f"LOI {tn}: gan-khung-video {r.stderr[-400:]}"); loi += 1
print(f"XONG. LOI: {loi}")
