# Thay giong may bang giong thu that cho make_video.py
#   python3 nhap_giong.py --kich-ban          -> ghi kich-ban-thu-am.md (danh sach cau de doc)
#   python3 nhap_giong.py <file thu am>       -> cat thanh tung cau, ghi de audio/sNN_MM.wav
#   python3 nhap_giong.py --may               -> xoa giong thu, quay ve giong Linh
# Thu MOT file lien: doc lan luot tung cau, nghi >= 1,5 giay giua hai cau (doc vap thi doc lai ca cau sau khoang nghi dai,
# roi xoa doan vap bang tay hoac bao lai — script chi kiem so cau).
import os, re, subprocess, sys, wave, glob, shutil
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FF = "/Users/MAC/Library/Python/3.9/lib/python/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
AUD = os.path.join(HERE, "audio"); SR = 22050

src = open(os.path.join(HERE, "make_video.py"), encoding="utf-8").read()
ns = {}; exec(src[src.index("SCENES = ["):src.index("# ---------------- am thanh")], ns)
SCENES = ns["SCENES"]
LINES = [(si, li, sc, spk) for si, sc in enumerate(SCENES) for li, (_, spk) in enumerate(sc["lines"])]

# chu phien am cho giong may -> chu viet binh thuong de nguoi doc
DOC = [("Brao", "Brown"), ("a mô ni ắc", "amoniac"), ("a xít clo hy đric", "axit clohiđric"), ("a xít", "axit"),
       ("A vô ga đrô", "Avogadro"), ("các bô níc", "cacbonic"), ("ni tơ", "nitơ"), ("bi a", "bi-a"),
       ("xen ti mét", "xentimét"), ("N A", "N-A")]
GIONG = {
 "hook": "tò mò, hạ giọng như kể chuyện bí ẩn; câu cuối hỏi chậm, bỏ lửng",
 "brown": "\"À!\" — giọng phát hiện ra; câu cuối nhấn \"quả bóng\", \"chen lấn\"",
 "three": "nhấn rời từng chữ NHỎ… LOẠN… ĐẬP, mỗi chữ dừng nửa nhịp",
 "balloon": "vui, như đang làm thí nghiệm thật; \"căng phồng\" kéo dài, \"xẹp\" hạ giọng",
 "tube": "ngạc nhiên ở câu đầu; câu cuối cười nhẹ — \"chen chợ Tết vậy\"",
 "ideal": "bình tĩnh, đếm rõ Một – Hai – Ba – Bốn; câu cuối giọng nhắc nhở",
 "mol": "rõ, chậm ở con số 6,02 nhân 10 mũ 23",
 "trap": "giọng cảnh báo, nhấn mạnh LÍT và GAM",
 "quiz": "thách thức, thân thiện — \"thử ngay nhé!\"",
 "answer": "hào hứng, như công bố kết quả",
 "recap": "ấm, chậm lại; câu cuối chốt chắc",
}

def doc(s):
    for a, b in DOC: s = s.replace(a, b)
    return s

def kich_ban():
    out = ["# Kịch bản thu âm — video Thuyết động học phân tử chất khí", "",
           f"{len(LINES)} câu. Thu **một file liền** bằng app Ghi âm trên iPhone, phòng yên tĩnh, máy cách miệng ~20 cm.",
           "Đọc lần lượt từng câu, **nghỉ ~2 giây giữa hai câu** (script cắt theo khoảng lặng). Đọc vấp thì dừng, nghỉ, đọc lại cả câu — rồi báo số câu vấp.",
           "Không đọc số thứ tự câu. Giọng gợi ý ở đầu mỗi cảnh, đọc như đang nói với một em học sinh.", ""]
    n = 0
    for si, sc in enumerate(SCENES):
        out += [f"## Cảnh {si + 1} · {sc['title']}", f"*Giọng: {GIONG.get(sc['key'], '')}*", ""]
        for li, (_, spk) in enumerate(sc["lines"]):
            n += 1; out.append(f"{n}. {doc(spk)}")
        out.append("")
    p = os.path.join(HERE, "kich-ban-thu-am.md"); open(p, "w", encoding="utf-8").write("\n".join(out)); print("ghi", p)

def doc_wav(p):
    with wave.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)

def nhap(path):
    tmp = os.path.join(HERE, "_thu.wav")
    # loc on nen, khu tieng u, chuan am luong
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR),
                    "-af", "highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11", tmp], check=True)
    x = doc_wav(tmp).astype(np.float32); os.remove(tmp)
    win = int(0.02 * SR); n = len(x) // win
    db = 20 * np.log10(np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1)) / 32768 + 1e-9)
    nguong = max(np.percentile(db, 20) + 10, -45)
    loud = db > nguong
    segs = []; i = 0
    while i < n:
        if loud[i]:
            j = i
            while j < n:
                if not loud[j]:
                    k = j
                    while k < n and not loud[k]: k += 1
                    if k - j >= int(0.9 / 0.02) or k >= n: break
                    j = k
                else: j += 1
            if (j - i) * 0.02 >= 0.35: segs.append((i, j))
            i = j
        else: i += 1
    print(f"tìm thấy {len(segs)} đoạn / cần {len(LINES)} câu")
    may = {}
    for si, li, _, _ in LINES:
        p = os.path.join(AUD, f"s{si:02d}_{li:02d}.wav")
        may[(si, li)] = len(doc_wav(p)) / SR if os.path.exists(p) else None
    for k, (a, b) in enumerate(segs):
        lab = f"{LINES[k][0] + 1}.{LINES[k][1] + 1}" if k < len(LINES) else "THỪA"
        ref = may.get(LINES[k][:2]) if k < len(LINES) else None
        warn = "  <-- lệch nhiều, kiểm lại" if ref and not (0.5 < (b - a) * 0.02 / ref < 2.0) else ""
        print(f"  câu {k + 1:2d} (cảnh {lab}): {(b - a) * 0.02:5.1f}s" + (f"  (máy {ref:4.1f}s)" if ref else "") + warn)
    if len(segs) != len(LINES):
        print("Số đoạn không khớp — chưa ghi gì. Thu lại hoặc cắt bớt đoạn vấp rồi chạy lại."); sys.exit(1)
    bk = os.path.join(HERE, "audio-may")
    if not os.path.exists(bk): shutil.copytree(AUD, bk)
    pad = int(0.15 * SR)
    for (si, li, _, _), (a, b) in zip(LINES, segs):
        y = x[max(0, a * win - pad): min(len(x), b * win + pad)]
        f = np.minimum(1, np.arange(len(y)) / (0.01 * SR)); y = y * f * f[::-1]
        with wave.open(os.path.join(AUD, f"s{si:02d}_{li:02d}.wav"), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(np.clip(y, -32768, 32767).astype(np.int16).tobytes())
    print("đã ghi giọng thu vào audio/ (giọng máy cũ ở audio-may/). Chạy: python3 make_video.py")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--kich-ban": kich_ban()
    elif a[0] == "--may":
        bk = os.path.join(HERE, "audio-may")
        if os.path.exists(bk): shutil.rmtree(AUD); shutil.copytree(bk, AUD); print("đã quay về giọng máy")
    else: nhap(a[0])
