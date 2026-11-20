# Xuat khung ban tuong tac (content/thi-nghiem/video-khung/<id>.json) cho MOT clip da dung.
#   python3 scripts/video-thi-nghiem/xuat-khung.py <ten clip>           -> in NHAP JSON (moc giay doan tu engine, chu lay tu kho thi nghiem)
#   python3 scripts/video-thi-nghiem/xuat-khung.py <ten clip> --kiem    -> kiem file JSON da co (K1-K6 trong skill dung-video-thi-nghiem)
#   cau_chot (tuy chon): dung 4 lua chon 'A. '..'D. ', giai_thich cho TUNG lua chon, chi so dung 0..3, giay trong canh Chot truoc Goi y
# Ban nhap chi la xuat phat: sua tay moc quan_sat/rut_ra theo phu de, viet cau hoi trung tinh (kiem), lua chon, dap an.
import importlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import engine
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
KHO = os.path.join(ROOT, "content", "thi-nghiem")
KHUNG = os.path.join(KHO, "video-khung")
name = sys.argv[1]
mod = importlib.import_module("clips." + name); clip = mod.CLIP; engine.build(clip)
cid = clip["id"]; sc = clip["scenes"]
def tu(s): return len(re.findall(r"[A-Za-zÀ-ỹđĐ]{2,}|\d+(?:[,.]\d+)?", s))
if "--kiem" in sys.argv:
    d = json.load(open(os.path.join(KHUNG, cid + ".json"))); loi = []
    o = d["o"]; dd = d["dung_dua"]; ket = [x["giay"] for x in o][1:] + [clip["TOTAL"]]
    if abs(d["tong_giay"] - clip["TOTAL"]) > 0.15: loi.append(f"tong_giay {d['tong_giay']} lech engine {clip['TOTAL']:.1f}")
    if [x["giay"] for x in o] != sorted(x["giay"] for x in o): loi.append("moc giay cac o khong tang dan")
    for x, e in zip(o, ket):                              # K3: chu o <= 2,3 tu/giay (mo 140 tu/phut) + 2 tu
        if x["khoa"] == "du_doan": continue
        n = tu(x["kiem"] if x["khoa"] == "gia_thuyet" and x.get("kiem") else x["chu"])   # Giả thuyết: chỉ `kiem` hiện trong lúc phát
        gioi = (e - x["giay"]) * 2.3 + 2
        if n > gioi: loi.append(f"K3 o {x['khoa']}: {n} tu / {e - x['giay']:.1f}s (toi da ~{gioi:.0f})")
    if re.search(r"<[^>]*>|DOI TEN|NGAYTHANG", json.dumps(d, ensure_ascii=False)): loi.append("con cho trong chua dien (<...>, DOI TEN, NGAYTHANG)")
    gk = {x["khoa"]: x["giay"] for x in o}
    if dd["giay"] > gk["dung_cu"]: loi.append(f"K9 diem dung {dd['giay']}s sau dau o dung_cu {gk['dung_cu']}s (hinh canh sau lo ra)")
    if dd["giay"] < gk["du_doan"]: loi.append("K9 diem dung truoc o du_doan")
    if not o[0].get("kiem"): loi.append("K2 o gia_thuyet thieu `kiem` (cau trung tinh)")
    elif tu(o[0]["kiem"]) < 4: loi.append("K2 `kiem` qua ngan")
    if "cues" in clip:                                    # K9: diem dung khong cat ngang tieng bao (tieng bao nam 0-0,35 s truoc diem dung)
        for g, k in clip["cues"](clip):
            if k != "tick" and 0 <= dd["giay"] - g < 0.35: loi.append(f"K9 diem dung {dd['giay']}s trung tieng '{k}' {g:.1f}s")
    if not 0 <= dd["dung"] < len(dd["chon"]): loi.append("dung ngoai khoang lua chon")
    for k in ("giai_thich_dung", "giai_thich_sai"):
        if re.match(r"\s*(Đúng|Chưa khớp)", dd[k]): loi.append(f"{k} mo dau bang 'Đúng/Chưa khớp' (component da them tien to)")
    cc = d.get("cau_chot")                                # viec 2 (19/11/2026): cau chot A-D, tuy chon
    if cc is not None:
        en = next((s for s in sc if s["key"] == "end"), sc[-1])
        ch = cc.get("chon") or []; gt = cc.get("giai_thich") or []
        if len(ch) != 4: loi.append(f"cau_chot: can dung 4 lua chon, dang co {len(ch)}")
        for j, c in enumerate(ch[:4]):
            if not c.startswith("ABCD"[j] + ". "): loi.append(f"cau_chot: lua chon {j} phai mo dau '{'ABCD'[j]}. ' (E1)")
        if len(set(c[3:].strip().lower() for c in ch)) != len(ch): loi.append("cau_chot: co lua chon trung nhau")
        if len(gt) != 4 or len(gt) != len(ch) or any(not str(g).strip() for g in gt): loi.append(f"cau_chot: thieu giai thich (can 4 cau, moi lua chon mot cau; dang co {len([g for g in gt if str(g).strip()])})")
        if not isinstance(cc.get("dung"), int) or not 0 <= cc["dung"] < max(len(ch), 1): loi.append(f"cau_chot: chi so dung {cc.get('dung')!r} ngoai 0..{len(ch) - 1}")
        if not str(cc.get("cau_hoi", "")).strip(): loi.append("cau_chot: thieu cau_hoi")
        for j, g in enumerate(gt):
            if re.match(r"\s*(Đúng|Sai|Chưa khớp|Chính xác)", str(g)): loi.append(f"cau_chot giai_thich[{j}] mo dau bang 'Đúng/Sai' (component da them tien to; K6)")
        n = [tu(c[3:]) for c in ch]
        if ch and min(n) and max(n) / min(n) > 1.8: loi.append(f"cau_chot: do dai lua chon lech {n} tu (lo dap an bang hinh thuc)")
        g = cc.get("giay", -1)
        if not (o[-1]["giay"] < g and en["t0"] <= g < clip["TOTAL"] - 0.5): loi.append(f"cau_chot giay {g}: phai trong canh Chot ({en['t0']:.1f}s..{clip['TOTAL'] - 0.5:.1f}s), sau o cuoi")
        if g <= dd["giay"]: loi.append("cau_chot giay truoc diem dung Du doan")
        if cc.get("cau_hoi", "").strip() == dd["cau_hoi"].strip(): loi.append("cau_chot trung cau Du doan")
        if "cues" in clip:
            for gc, k in clip["cues"](clip):
                if k != "tick" and 0 <= g - gc < 0.35: loi.append(f"K9 cau_chot dung {g}s trung tieng '{k}' {gc:.1f}s")
    if any(re.search(r"\b\d+\s?%", x["chu"]) for x in o):
        loi.append("K5 co so % trong chu o: doi chieu voi kho thi nghiem + hinh (khong de 5%/8% mau thuan)")
    print(cid, "OK" if not loi else "CAN SUA:"); [print(" -", l) for l in loi]; sys.exit(1 if loi else 0)
kho = json.load(open(os.path.join(KHO, cid + ".json")))
hook = sc[0]; do = sc[1]; cu = sc[-2]
nhap = dict(id=cid, ten=kho["ten"] + "  (DOI TEN: khong duoc lo dap an, K1)",
    video="https://jgvbdbpvjdntdgzthumv.supabase.co/storage/v1/object/public/lesson-clips/clip/" + cid + "-<NGAYTHANG>-2.mp4",
    tong_giay=round(clip["TOTAL"], 1),
    o=[dict(khoa="gia_thuyet", giay=0, chu=(kho.get("gia_thuyet") or [kho.get("muc_tieu", "<GIA THUYET>")])[0], kiem="<CAU TRUNG TINH: khong neu quan he can doan>"),
       dict(khoa="du_doan", giay=round(hook["t0"] + hook["M"][-1], 1), chu="<CAU HOI DU DOAN>"),
       dict(khoa="dung_cu", giay=round(do["t0"], 1), chu="<<= 8 tu neu o hien < 4 s>"),
       dict(khoa="quan_sat", giay=round(do["t0"] + do["M"][-1], 1), chu=" ".join((kho.get("cac_buoc") or {}).get("quan_sat", ["<QUAN SAT>"])[:1])),
       dict(khoa="rut_ra", giay=round(sc[2]["t0"], 1), chu=((kho.get("cac_buoc") or {}).get("rut_ra") or ["<RUT RA>"])[0]),
       dict(khoa="chua_noi", giay=round(cu["t0"], 1), chu=(kho.get("khong_chung_minh") or ["<>"])[0])],
    dung_dua=dict(giay=round(hook["t0"] + hook["T"] - 0.15, 1), cau_hoi="<CAU HOI>", chon=["A. ", "B. ", "C. "], dung=0,
        giai_thich_dung="<khong mo dau bang 'Đúng'>", giai_thich_sai="<khong mo dau bang 'Chưa khớp'>"),
    cau_chot=dict(giay=round(next((s for s in sc if s["key"] == "end"), sc[-1])["t0"] + next((s for s in sc if s["key"] == "end"), sc[-1])["M"][0] + 1.4, 1), cau_hoi="<CAU HOI THU NGHI trong canh Chot>",
        chon=["A. ", "B. ", "C. ", "D. "], dung=0, giai_thich=["<cho A>", "<cho B>", "<cho C>", "<cho D>"]))
print(json.dumps(nhap, ensure_ascii=False, indent=2))
print("\n# LUU Y: moc quan_sat/rut_ra o day chi la doan (rut_ra = canh thu 3); dat theo PHU DE co noi dung do (K4).", file=sys.stderr)
print("\n# canh cua clip (de sua moc o cho khop phu de):", file=sys.stderr)
for s in sc:
    print(f"#  {s['t0']:5.1f}s [{s['key']}] {s['title']}: " + " | ".join(f"{s['t0']+m:.1f} {c}" for m, c in zip(s["M"], s["caps"])), file=sys.stderr)
