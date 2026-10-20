#!/usr/bin/env python3
"""Sinh file mp3 giọng neural (Azure Speech; mặc định nữ en-US-AriaNeural, giọng nam en-US-GuyNeural) cho mọi nút 🔊 của một chương AVCN.

Chạy từ gốc repo, SAU khi đã dựng theory.html một lần:
  python3 .claude/skills/soan-bai-avcn/scripts/tao_giong_doc.py content/lesson-samples/avcn-chapter-<n>-<slug>
  python3 .claude/skills/soan-bai-avcn/scripts/build_avcn.py   content/lesson-samples/avcn-chapter-<n>-<slug>   # dựng lại: nút 🔊 có data-tl-audio

Đọc data-tl-speak trong theory.html → gọi Azure → ghi public/assets/avcn/chapter-<n>/audio/<sha1[:10]>.mp3
và audio.json (chuỗi → tên file) cùng thư mục. File đã có thì bỏ qua (chạy lại không tốn thêm hạn mức).
Nút nào có data-tl-giong="nam" (lời nhân vật nam, vd. thợ cả) thì đọc bằng giọng nam; khoá manifest là "nam|chuỗi".
Tên file đã băm kèm tên giọng nên bản nam/nữ của cùng một câu không đè nhau.

Từ 20/10/2026 sinh thêm mp3 cho **phương án quiz tiếng Anh** (bấm đáp án là phát âm, xem lib/quiz-speak.ts) và cho
`data-tl-word` của câu hỏi có phương án tiếng Việt; phương án tiếng Việt/True-False bỏ qua (không đọc).
Nút 🔊 phát mp3; thiếu file hoặc lỗi tải thì tự rơi về giọng trình duyệt (speechSynthesis).

Khoá Azure Speech (tầng miễn phí F0 ~500.000 ký tự/tháng; một chương ~10.000 ký tự) đặt trong .env.local:
  AZURE_SPEECH_KEY=…   AZURE_SPEECH_REGION=southeastasia
  (tuỳ chọn: AZURE_SPEECH_VOICE, mặc định en-US-AriaNeural; AZURE_SPEECH_VOICE_NAM, mặc định en-US-GuyNeural)
Không in khoá ra màn hình. Bản thử trước đó dùng edge-tts (không chính thức) chỉ để chọn giọng, không dùng trong pipeline.
"""
import argparse, hashlib, html, json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[4]
VOICE = "en-US-AriaNeural"
VOICE_NAM = "en-US-GuyNeural"
FORMAT = "audio-24khz-48kbitrate-mono-mp3"  # ~6 KB/giây: câu 3 giây ≈ 18 KB

# Cùng luật với build_avcn.py + lib/quiz-speak.ts: phương án tiếng Anh đọc được, tiếng Việt/ngoặc thì không.
_VIET = re.compile(r"[àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]", re.I)


def doc_duoc(s: str) -> bool:
    t = html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    return bool(t) and bool(re.search(r"[A-Za-z]", t)) and not _VIET.search(t) and "(" not in t and ")" not in t


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
    """[(chuỗi, giọng)] cho mọi nút tl-speak, mọi phương án quiz tiếng Anh và mọi `data-tl-word`.
    Giọng đọc từ data-tl-giong (mặc định "" = giọng nữ). Cùng luật đọc được với build_avcn.py/lib/quiz-speak.ts."""
    h = theory.read_text(encoding="utf-8")
    out = {}
    for tag in re.findall(r'<button[^>]*class="tl-speak"[^>]*>', h):
        m = re.search(r'data-tl-speak="([^"]*)"', tag)
        if not m:
            continue
        t = html.unescape(m.group(1)).strip()
        if not t:
            continue
        g = re.search(r'data-tl-giong="([^"]*)"', tag)
        out.setdefault((t, (g.group(1).strip() if g else "")), None)
    # Bấm đáp án quiz AVCN là phát âm luôn (20/10/2026): sinh mp3 cho phương án có data-tl-say (build đánh dấu
    # phương án tiếng Anh) + từ đang hỏi ở data-tl-word. Phương án tiếng Việt không có dấu nên KHÔNG đoán theo chữ.
    for m in re.finditer(r'<label[^>]*data-tl-say="1"[^>]*>\s*[a-dA-D][.)]\s*([^<]+)</label>', h):
        t = html.unescape(m.group(1)).strip()
        if doc_duoc(t):
            out.setdefault((t, ""), None)
    for m in re.finditer(r'data-tl-word="([^"]*)"', h):
        t = html.unescape(m.group(1)).strip()
        if t:
            out.setdefault((t, ""), None)
    return list(out)


def giong_cua(env: dict, giong: str) -> str:
    if giong == "nam":
        return env.get("AZURE_SPEECH_VOICE_NAM", VOICE_NAM)
    return env.get("AZURE_SPEECH_VOICE", VOICE)


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
    voice = giong_cua(env, "")
    voice_nam = giong_cua(env, "nam")
    so_nam = sum(1 for _, g in texts if g == "nam")
    chars = sum(len(t) for t, _ in texts)
    print(f"Chapter {ch}: {len(texts)} chuỗi, {chars} ký tự — giọng nữ {voice}, "
          f"giọng nam {voice_nam} ({so_nam} chuỗi)")
    if a.dry_run:
        for t, g in texts:
            if g == "nam":
                print(f"  nam: {t[:70]}")
        return
    if not env.get("AZURE_SPEECH_KEY"):
        sys.exit("Thiếu AZURE_SPEECH_KEY trong .env.local (xem đầu file script này).")
    endpoint = env.get("AZURE_SPEECH_ENDPOINT") or \
        f"https://{env.get('AZURE_SPEECH_REGION', 'southeastasia')}.tts.speech.microsoft.com/cognitiveservices/v1"
    out.mkdir(parents=True, exist_ok=True)
    man_f = out.parent / "audio.json"
    man = json.loads(man_f.read_text(encoding="utf-8")) if man_f.exists() else {}
    moi = 0
    for t, giong in texts:
        v = giong_cua(env, giong)
        f = out / ten_file(t, v)
        if not f.exists():
            f.write_bytes(tong_hop(t, v, a.toc_do, env, endpoint))
            moi += 1
        man[f"nam|{t}" if giong == "nam" else t] = f.name
    man_f.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    kb = sum(p.stat().st_size for p in out.glob("*.mp3")) / 1024
    print(f"Sinh mới {moi}, tổng {len(man)} file, {kb:.0f} KB → {out}  (+ {man_f.name})")


if __name__ == "__main__":
    main()
