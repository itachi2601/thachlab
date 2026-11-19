# python3 scripts/video-thi-nghiem/render.py <ten clip trong clips/> [--preview | --kich-ban | --sheet]
# Cong soat moi (19/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 3; nam o day vi engine.py khong sua khi co phien dang dung lo):
#   --do-chu     cong A2: LOI neu canh > 180 tu/phut; LOI neu 2 khoi chu moi (ngoai phu de) cach nhau < 2 s;
#                LOI neu chu than canh nho hon 48 px trong mp4; LOI neu hinh dung yen > 4 s. Thoat ma 1 khi co LOI.
#   --sheet-375  cong B: anh ghep moi khung thu ve 283x503 (co hien thi that trong bai) -> ra/<id>-sheet-375.png
# Cac co khac (--preview, --kich-ban, --sheet, dung mp4) chuyen thang cho engine.run.
import importlib, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
from PIL import Image, ImageDraw

TPM_MAX = 180        # tu/phut toi da moi canh
NHIP_GIAY = 2.0      # hai khoi chu moi phai cach nhau >= so giay nay
CHU_MIN_PX = 48      # chu than canh nho nhat trong mp4 (da nhan SCALE)
DUNG_YEN_MAX = 4.0   # hinh khong doi qua so giay nay
BUOC = 0.2

def do_chu_moi(clip):
    rec, state = [], {"chrome": False}
    orig_text = ImageDraw.ImageDraw.text; orig_chrome = engine.chrome
    def spy(self, xy, s, *a, **k):
        fill = k.get("fill", a[0] if a else None); f = k.get("font")
        al = fill[3] / 255 if isinstance(fill, tuple) and len(fill) == 4 else 1.0
        if al >= 0.6 and isinstance(s, str) and s.strip():
            px = (getattr(f, "size", 0) or 0) * (1.0 if state["chrome"] else engine.SCALE)
            rec.append((s.strip(), xy[1], px, state["chrome"]))
        return orig_text(self, xy, s, *a, **k)
    def chrome_spy(*a, **k):
        state["chrome"] = True
        try: return orig_chrome(*a, **k)
        finally: state["chrome"] = False
    ImageDraw.ImageDraw.text = spy; engine.chrome = chrome_spy
    loi = 0; tong = 0
    try:
        for sc in clip["scenes"]:
            seen = {}; nho = {}; prev = None; run0 = 0.0; dung = []
            t = 0.0
            while t < sc["T"]:
                rec.clear(); img = engine.frame(clip, sc["t0"] + t)
                for s, y, px, chrome in rec:
                    if chrome or y < 150 or y > 1840 or s == sc["title"] or any(s in c for c in sc["caps"]): continue
                    if engine.n_tu(s) >= 2:
                        k = re.sub(r"\d+([,.]\d+)?", "#", s)
                        if k not in seen: seen[k] = (t, y)
                    if px and px < CHU_MIN_PX - 0.5: nho[s] = min(nho.get(s, 999), px)
                g = np.asarray(img.crop((0, 285, 1080, 1500)).convert("L").resize((108, 122)), dtype=np.int16)
                if prev is not None and np.abs(g - prev).mean() > 0.25: run0 = t
                prev = g
                if t - run0 > DUNG_YEN_MAX and (not dung or dung[-1][0] != run0): dung.append([run0, t])
                elif dung and dung[-1][0] == run0: dung[-1][1] = t
                t += BUOC
            w = sum(engine.n_tu(k) for k in seen) + sum(engine.n_tu(c) for c in sc["caps"]); tong += w
            tpm = w / sc["T"] * 60
            msgs = []
            if tpm > TPM_MAX: msgs.append(f"quá dày {tpm:.0f} > {TPM_MAX} từ/phút")
            # khoi chu = cac chuoi hien trong cung 0,3 s va cach nhau < 130 px theo y
            moc = sorted(seen.values()); khoi = []
            for tt, y in moc:
                if khoi and tt - khoi[-1][0] < 0.35 and abs(y - khoi[-1][1]) < 130: continue
                khoi.append((tt, y))
            for a, b in zip(khoi, khoi[1:]):
                if b[0] - a[0] < NHIP_GIAY - 0.01 and b[0] - a[0] > 0.05:
                    msgs.append(f"2 khối chữ mới cách {b[0] - a[0]:.1f}s ({a[0]:.1f}s→{b[0]:.1f}s)")
                    break
            if nho:
                ds = sorted(nho.items(), key=lambda x: x[1])[:3]
                msgs.append("chữ < 48px: " + "; ".join(f"“{s[:24]}” {p:.0f}px" for s, p in ds) + (f" (+{len(nho) - 3})" if len(nho) > 3 else ""))
            for a, b in dung:
                if b - a > DUNG_YEN_MAX: msgs.append(f"hình đứng yên {b - a:.1f}s ({a:.1f}s→{b:.1f}s)")
            loi += len(msgs)
            print(f"[{sc['key']}] {sc['T']:.1f}s  {w} từ  {tpm:.0f} từ/phút" + ("".join("\n    LỖI " + m for m in msgs)))
    finally:
        ImageDraw.ImageDraw.text = orig_text; engine.chrome = orig_chrome
    tpm = tong / clip["TOTAL"] * 60
    print(f"CẢ CLIP {tong} từ / {clip['TOTAL']:.1f}s = {tpm:.0f} từ/phút (đích ≤ 200); {loi} LỖI" + ("  ← KHÔNG QUA CỔNG A2" if loi else "  ← qua"))
    return loi

def sheet_375(clip):
    ts = []
    for sc in clip["scenes"]:
        ts += [sc["t0"] + m + 1.6 for m in sc["M"]] + [sc["t0"] + sc["T"] - 0.1]
    cw, ch, cols = 283, 503, 4; rows = (len(ts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * ch), (0, 0, 0))
    for i, t in enumerate(ts):
        sheet.paste(engine.frame(clip, t).resize((cw, ch), Image.LANCZOS), ((i % cols) * cw, (i // cols) * ch))
    sp = os.path.join(engine.OUT, clip["id"] + "-sheet-375.png"); sheet.save(sp)
    print(sp); print("khung (trái→phải, trên→dưới):", ", ".join(f"{t:.1f}s" for t in ts))

if __name__ == "__main__":
    mod = importlib.import_module("clips." + sys.argv[1]); argv = sys.argv[2:]
    if "--do-chu" in argv:
        engine.build(mod.CLIP); print(f"{mod.CLIP['id']}: {mod.CLIP['TOTAL']:.1f}s")
        sys.exit(1 if do_chu_moi(mod.CLIP) else 0)
    if "--sheet-375" in argv:
        engine.build(mod.CLIP); print(f"{mod.CLIP['id']}: {mod.CLIP['TOTAL']:.1f}s"); sheet_375(mod.CLIP); sys.exit(0)
    engine.run(mod.CLIP, argv)
