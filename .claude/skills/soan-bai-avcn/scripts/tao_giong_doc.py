#!/usr/bin/env python3
"""Cách 2 (thử nghiệm): sinh file mp3 giọng neural cho mọi nút 🔊 của một chương AVCN.

Đọc theory.html đã dựng, gom các chuỗi trong data-tl-speak, sinh mp3 bằng edge-tts (giọng neural Microsoft),
ghi ra <out>/<sha1[:10]>.mp3 + manifest.json (chuỗi → tên file) + nghe-thu.html để thầy nghe trên máy.

  python3 tao_giong_doc.py <theory.html> <thu-muc-ra> [--voice en-US-AriaNeural] [--gioi-han 12] [--toc-do -10%]

Cài: python3 -m venv v && v/bin/pip install edge-tts   (cần mạng khi sinh; nghe thì không).
Lưu ý giấy phép: edge-tts là thư viện không chính thức gọi dịch vụ đọc của Microsoft Edge — chỉ dùng để NGHE THỬ.
Nếu chọn dùng thật, đổi hàm `tong_hop()` sang Azure Speech / Google Cloud TTS (cùng giọng neural, có điều khoản rõ ràng).
Chưa nối vào build_avcn.py / trang bài học: nút 🔊 vẫn dùng speechSynthesis của trình duyệt.
"""
import argparse, asyncio, hashlib, html, json, re, sys
from pathlib import Path

GIONG_THU = ["en-US-AriaNeural", "en-US-JennyNeural", "en-US-AndrewNeural", "en-GB-SoniaNeural"]


def gom_chuoi(theory: Path) -> list[str]:
    ds = re.findall(r'data-tl-speak="([^"]*)"', theory.read_text(encoding="utf-8"))
    thay_the = {}
    for s in ds:
        t = html.unescape(s).strip()
        if t:
            thay_the.setdefault(t, None)
    return list(thay_the)


def ten_file(text: str, voice: str) -> str:
    return hashlib.sha1(f"{voice}|{text}".encode()).hexdigest()[:10] + ".mp3"


async def tong_hop(text: str, voice: str, rate: str, dest: Path):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(str(dest))


async def chay(texts, voice, rate, out: Path):
    manifest = {}
    sem = asyncio.Semaphore(4)

    async def one(t):
        f = out / ten_file(t, voice)
        if not f.exists():
            async with sem:
                await tong_hop(t, voice, rate, f)
        manifest[t] = f.name

    await asyncio.gather(*(one(t) for t in texts))
    return manifest


def trang_nghe(manifest: dict, out: Path, voice: str):
    rows = "".join(
        f'<li><audio controls preload="none" src="{f}"></audio> <span>{html.escape(t)}</span></li>'
        for t, f in manifest.items()
    )
    (out / "nghe-thu.html").write_text(
        f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>Nghe thử {voice}</title><style>body{{font:16px system-ui;max-width:720px;margin:16px auto;padding:0 16px}}"
        f"li{{margin:10px 0;list-style:none}}audio{{display:block;width:100%}}</style>"
        f"<h1>{voice}</h1><ul style='padding:0'>{rows}</ul>",
        encoding="utf-8",
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("theory")
    ap.add_argument("out")
    ap.add_argument("--voice", default=GIONG_THU[0])
    ap.add_argument("--gioi-han", type=int, default=0, help="chỉ sinh N chuỗi đầu (nghe thử)")
    ap.add_argument("--toc-do", default="-10%", help="edge-tts rate, ví dụ -10%%")
    a = ap.parse_args()

    texts = gom_chuoi(Path(a.theory))
    if a.gioi_han:
        texts = texts[: a.gioi_han]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = asyncio.run(chay(texts, a.voice, a.toc_do, out))
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    trang_nghe(manifest, out, a.voice)
    kb = sum(p.stat().st_size for p in out.glob("*.mp3")) / 1024
    print(f"{len(manifest)} chuỗi · {kb:.0f} KB · giọng {a.voice} → {out}/nghe-thu.html")


if __name__ == "__main__":
    sys.exit(main())
