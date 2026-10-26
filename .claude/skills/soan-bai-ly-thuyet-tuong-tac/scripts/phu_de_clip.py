#!/usr/bin/env python3
"""Cắt clip hiện tượng + gắn phụ đề từ khoá cứng vào hình (quy tắc V9 trong docs/QUY-TAC-THIET-KE.md).

Dùng:
    python3 phu_de_clip.py <clip-goc.mp4|.mov> <phu-de.json> <ra.mp4> [--rong 720]

phu-de.json:
    {"tu": 3.0, "den": 18.0,                       # đoạn giữ lại trong clip gốc (giây); bỏ thì lấy cả clip
     "phu_de": [{"tu": 0.5, "den": 4, "chu": "Nhúng nước nóng"},   # mốc tính từ đầu đoạn đã cắt
                {"tu": 4.5, "den": 9, "chu": "Bóng căng phồng"}]}

Quy ước V9: clip 10–20 giây, KHÔNG lời (script bỏ tiếng), mỗi phụ đề ≤ 8 chữ, hiện đúng lúc hiện tượng xảy ra.
Script cảnh báo khi vượt; ra mp4 H.264 không tiếng, rộng ≤ 720 px, faststart (tải lên YouTube không công khai
rồi nhúng `<div class="tl-video"><iframe …youtube-nocookie…>` trong hộp thí nghiệm — V5, V8).
"""
import argparse, json, pathlib, subprocess, sys, tempfile

FF = "/Users/MAC/Library/Python/3.9/lib/python/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip"); ap.add_argument("phu_de"); ap.add_argument("ra")
    ap.add_argument("--rong", type=int, default=720)
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.phu_de).read_text(encoding="utf8"))
    cues = cfg.get("phu_de", [])

    canh = []
    tu, den = cfg.get("tu"), cfg.get("den")
    if tu is not None and den is not None and not 10 <= den - tu <= 20:
        canh.append(f"clip dài {den - tu:.1f} s — V9 khuyên 10–20 s")
    for c in cues:
        if len(c["chu"].split()) > 8:
            canh.append(f"phụ đề > 8 chữ: {c['chu']}")

    tmp = pathlib.Path(tempfile.mkdtemp())
    filt = [f"scale='min({a.rong},iw)':-2"]
    for i, c in enumerate(cues):
        f = tmp / f"c{i}.txt"
        f.write_text(c["chu"], encoding="utf8")          # textfile: khỏi phải escape dấu ':' ',' tiếng Việt
        filt.append(
            f"drawtext=fontfile='{FONT}':textfile='{f}':fontsize=h/16:fontcolor=white:"
            f"box=1:boxcolor=black@0.6:boxborderw=14:x=(w-text_w)/2:y=h-text_h-h/12:"
            f"enable='between(t,{c['tu']},{c['den']})'")
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "error"]
    if tu is not None:
        cmd += ["-ss", str(tu)]
    cmd += ["-i", a.clip]
    if tu is not None and den is not None:
        cmd += ["-t", str(den - tu)]
    cmd += ["-vf", ",".join(filt), "-an", "-c:v", "libx264", "-crf", "28", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.ra]
    subprocess.run(cmd, check=True)
    kb = pathlib.Path(a.ra).stat().st_size / 1024
    print(f"ok {a.ra} · {kb:.0f} KB · {len(cues)} phụ đề")
    for c in canh:
        print("⚠", c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
