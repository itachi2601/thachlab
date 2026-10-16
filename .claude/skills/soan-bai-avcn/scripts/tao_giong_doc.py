#!/usr/bin/env python3
"""Sinh file mp3 giọng neural (Azure Speech, en-US-AriaNeural) cho mọi nút 🔊 của một chương AVCN.

Chạy từ gốc repo, SAU khi đã dựng theory.html một lần:
  python3 .claude/skills/soan-bai-avcn/scripts/tao_giong_doc.py content/lesson-samples/avcn-chapter-<n>-<slug>
  python3 .claude/skills/soan-bai-avcn/scripts/build_avcn.py   content/lesson-samples/avcn-chapter-<n>-<slug>   # dựng lại: nút 🔊 có data-tl-audio

Đọc data-tl-speak trong theory.html → gọi Azure → ghi public/assets/avcn/chapter-<n>/audio/<sha1[:10]>.mp3
và audio.json (chuỗi → tên file) cùng thư mục. File đã có thì bỏ qua (chạy lại không tốn thêm hạn mức).
Nút 🔊 phát mp3; thiếu file hoặc lỗi tải thì tự rơi về giọng trình duyệt (speechSynthesis).

Khoá Azure Speech (tầng miễn phí F0 ~500.000 ký tự/tháng; một chương ~10.000 ký tự) đặt trong .env.local:
  AZURE_SPEECH_KEY=…   AZURE_SPEECH_REGION=southeastasia   (tuỳ chọn: AZURE_SPEECH_VOICE, mặc định en-US-AriaNeural)
Không in khoá ra màn hình. Bản thử trước đó dùng edge-tts (không chính thức) chỉ để chọn giọng, không dùng trong pipeline.
"""
import argparse, hashlib, html, json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[4]
VOICE = "en-US-AriaNeural"
FORMAT = "audio-24khz-48kbitrate-mono-mp3"  # ~6 KB/giây: câu 3 giây ≈ 18 KB


def doc_env() -> dict:
    env = dict(os.environ)
    f = ROOT / ".env.local"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*([A-Z0-9_]+)\s*=\s*(.*)$", line)
            if m and m.group(1) not in env:
                env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


def gom_chuoi(theory: Path) -> list:
    out = {}
    for s in re.findall(r'data-tl-speak="([^"]*)"', theory.read_text(encoding="utf-8")):
        t = html.unescape(s).strip()
        if t:
            out.setdefault(t, None)
    return list(out)


def ten_file(text: str, voice: str) -> str:
    return hashlib.sha1(f"{voice}|{text}".encode()).hexdigest()[:10] + ".mp3"


def tong_hop(text: str, voice: str, rate: str, env: dict, endpoint: str) -> bytes:
    ssml = (f"<speak version='1.0' xml:lang='en-US'><voice name='{voice}'>"
            f"<prosody rate='{rate}'>{escape(text)}</prosody></voice></speak>")
    req = urllib.request.Request(
        endpoint, data=ssml.encode("utf-8"), method="POST",
        headers={"Ocp-Apim-Subscription-Key": env["AZURE_SPEECH_KEY"], "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": FORMAT, "User-Agent": "thachlab-avcn"})
    for lan in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            if len(data) < 500:
                raise RuntimeError(f"mp3 quá ngắn ({len(data)} byte)")
            return data
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                sys.exit(f"Azure từ chối khoá (HTTP {e.code}) — kiểm AZURE_SPEECH_KEY / AZURE_SPEECH_REGION")
            if lan == 2:
                raise
        except Exception:
            if lan == 2:
                raise
        time.sleep(1.5 * (lan + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("thu_muc_bai")
    ap.add_argument("--out", help="mặc định public/assets/avcn/chapter-<n>/audio")
    ap.add_argument("--toc-do", default="-10%")
    ap.add_argument("--gioi-han", type=int, default=0, help="chỉ sinh N chuỗi đầu (thử)")
    ap.add_argument("--dry-run", action="store_true", help="chỉ đếm chuỗi/ký tự, không gọi Azure")
    a = ap.parse_args()

    bai = Path(a.thu_muc_bai).resolve()
    ch = json.loads((bai / "data" / "bai.json").read_text(encoding="utf-8"))["meta"]["chapter"]
    out = Path(a.out) if a.out else ROOT / "public" / "assets" / "avcn" / f"chapter-{ch}" / "audio"
    texts = gom_chuoi(bai / "theory.html")
    if a.gioi_han:
        texts = texts[: a.gioi_han]
    env = doc_env()
    voice = env.get("AZURE_SPEECH_VOICE", VOICE)
    chars = sum(len(t) for t in texts)
    print(f"Chapter {ch}: {len(texts)} chuỗi, {chars} ký tự, giọng {voice}")
    if a.dry_run:
        return
    if not env.get("AZURE_SPEECH_KEY"):
        sys.exit("Thiếu AZURE_SPEECH_KEY trong .env.local (xem đầu file script này).")
    endpoint = env.get("AZURE_SPEECH_ENDPOINT") or \
        f"https://{env.get('AZURE_SPEECH_REGION', 'southeastasia')}.tts.speech.microsoft.com/cognitiveservices/v1"
    out.mkdir(parents=True, exist_ok=True)
    man_f = out.parent / "audio.json"
    man = json.loads(man_f.read_text(encoding="utf-8")) if man_f.exists() else {}
    moi = 0
    for t in texts:
        f = out / ten_file(t, voice)
        if not f.exists():
            f.write_bytes(tong_hop(t, voice, a.toc_do, env, endpoint))
            moi += 1
        man[t] = f.name
    man_f.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    kb = sum(p.stat().st_size for p in out.glob("*.mp3")) / 1024
    print(f"Sinh mới {moi}, tổng {len(man)} file, {kb:.0f} KB → {out}  (+ {man_f.name})")


if __name__ == "__main__":
    main()
