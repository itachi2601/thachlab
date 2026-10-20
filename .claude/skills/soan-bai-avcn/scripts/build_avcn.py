#!/usr/bin/env python3
"""Dựng bài AVCN (Anh văn chuyên ngành Cơ khí) từ <thư-mục-bài>/data/bai.json → theory.html + bundle.json.

Chạy từ gốc repo:  python3 .claude/skills/soan-bai-avcn/scripts/build_avcn.py content/lesson-samples/avcn-chapter-<n>-<slug>
Mọi nội dung nằm trong data/bai.json (từ vựng, bài đọc, quiz, đề mẫu, luyện tập); file này chỉ dàn trang.
Quy ước: HTML lưu DB không được chứa <script>/on*= — mọi tương tác là radio + :checked, <details>.
Nút nghe 🔊 là <button data-tl-speak="…">, trang bài học xử lý uỷ quyền: phát mp3 ở data-tl-audio (nếu có), không thì speechSynthesis.
Ảnh: public/assets/avcn/chapter-<n>/<key>.webp, nguồn + giấy phép trong credits.json cùng thư mục.
"""
import html as H
import json
import pathlib
import re

import sys
HERE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path.cwd()
ROOT = pathlib.Path(__file__).resolve().parents[4]
D = json.loads((HERE / "data" / "bai.json").read_text(encoding="utf-8"))
M = D["meta"]
CH = M["chapter"]
P = M["prefix"]
ASSET_DIR = ROOT / "public" / "assets" / "avcn" / f"chapter-{CH}"
ASSET_URL = f"/assets/avcn/chapter-{CH}"
CREDITS = {c["key"]: c for c in json.loads((ASSET_DIR / "credits.json").read_text(encoding="utf-8"))}
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
_qn = [0]


def nl(text) -> str:
    """Mỗi ý một dòng (quy tắc thầy 7/10 + 10/10/2026): list → <ul>; chuỗi nhiều câu → tách <br> ở ranh giới câu."""
    if isinstance(text, list):
        return '<ul class="avcn-list">' + "".join(f"<li>{x}</li>" for x in text) + "</ul>"
    parts = re.split(r"(?<=[.!?])\s+(?=(?:<[^>]+>|[\"“])*[A-ZĐÀ-Ỹ0-9])", text.strip())
    return "<br>".join(p for p in parts if p)


def esc(s: str) -> str:
    return H.escape(s, quote=True)


_AUDIO_F = ASSET_DIR / "audio.json"
AUDIO = json.loads(_AUDIO_F.read_text(encoding="utf-8")) if _AUDIO_F.exists() else {}


def speak(text: str, giong: str = "") -> str:
    """Nút 🔊. Có mp3 neural (tao_giong_doc.py → audio.json) thì thêm data-tl-audio; thiếu thì trang tự đọc bằng
    giọng trình duyệt. `giong="nam"` (lời nhân vật nam, vd. thợ cả): mp3 tra khoá "nam|…" trong audio.json và
    trang chọn giọng nam khi rơi về giọng máy (data-tl-giong)."""
    t = H.unescape(text).strip()
    f = AUDIO.get(f"nam|{t}" if giong == "nam" else t)
    au = f' data-tl-audio="{ASSET_URL}/audio/{f}"' if f else ""
    g = ' data-tl-giong="nam"' if giong == "nam" else ""
    return f'<button type="button" class="tl-speak" data-tl-speak="{esc(text)}"{g}{au} aria-label="Nghe">🔊</button>'


def photo(key: str, caption: str, small=False) -> str:
    c = CREDITS[key]
    cls = "fig avcn-photo avcn-photo--sm" if small else "fig avcn-photo"
    if "wikimedia.org" in str(c.get("page", "")):
        credit = f'Ảnh: {esc(c["author"])}, {esc(c["license"])}, <a href="{esc(c["page"])}" target="_blank" rel="noopener">Wikimedia Commons</a>'
    else:  # hình tự vẽ (SVG) — không có trang Commons
        credit = f'Hình tự vẽ, {esc(c["license"])}'
    return (f'<figure class="{cls}"><img src="{ASSET_URL}/{key}.webp" alt="{esc(caption)}" loading="lazy" '
            f'width="{c["w"]}" height="{c["h"]}"><figcaption>{caption} · {credit}</figcaption></figure>')


def quiz(hoi: str, lua_chon, dap: int, fb_ok: str, fb_no: str, lead="", prefix=None) -> str:
    """Trắc nghiệm tự chấm (radio + CSS). Nhãn a. b. c. d. chữ thường như đề AVCN thật."""
    _qn[0] += 1
    n = f"{prefix or P}-q{_qn[0]}"
    opts = []
    for i, o in enumerate(lua_chon):
        cls = "tl-ok" if i == dap else "tl-no"
        opts.append(f'<input type="radio" name="{n}" id="{n}{chr(97+i)}"><label for="{n}{chr(97+i)}" class="tl-opt {cls}">{chr(97+i)}. {o}</label>')
    fb_ok = nl(re.sub(r"^Đúng\.\s*", "", fb_ok))
    fb_no = nl(re.sub(r"^Chưa đúng\.\s*", "", fb_no))
    return (f'{lead}<p>{hoi}</p><div class="tl-quiz">{"".join(opts)}'
            f'<div class="tl-fb tl-fb--ok"><p><strong>Đúng.</strong> {fb_ok}</p></div>'
            f'<div class="tl-fb tl-fb--no"><p><strong>Chưa đúng.</strong> {fb_no}</p></div></div>')


def quiz_tf(hoi: str, dap: bool, fb_ok: str, fb_no: str, prefix=None) -> str:
    return quiz(hoi, ["True (Đúng)", "False (Sai)"], 0 if dap else 1, fb_ok, fb_no, prefix=prefix)


def think(label: str, inner: str) -> str:
    return f'<div class="tl-box tl-box--think"><p class="tl-label">{label}</p>{inner}</div>'


def rule(label: str, inner: str) -> str:
    return f'<div class="tl-box tl-box--rule"><p class="tl-label">{label}</p>{inner}</div>'


def details(summary: str, inner: str, cls="tl-details") -> str:
    return f'<details class="{cls}"><summary>{summary}</summary>{inner}</details>'


# ---------- Mục 0: thi gì ----------
def sec_thi() -> str:
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in M["de_thi"])
    muc_tieu = "".join(f"<li>{x}</li>" for x in M["muc_tieu"])
    bang = details("Xem 5 Part của đề ứng với mục nào trong bài", f'<div class="table-scroll"><table class="tl-table avcn-tbl"><thead><tr><th>Part</th><th>Đề hỏi gì</th><th>Học ở mục</th></tr></thead><tbody>{rows}</tbody></table></div>')
    bc = M.get("boi_canh")
    if bc:  # mở bài bằng tình huống ở xưởng; mục tiêu + đề thi thu vào mục gập
        # Câu tiếng Anh của nhân vật trong tình huống (thợ cả): nghe lại đúng câu đó, giọng nam.
        nghe = (f'<p>🎧 Nghe lại đúng câu thợ cả nói: {speak(bc["cau_noi"], bc.get("giong") or "")}</p>'
                if bc.get("cau_noi") else "")
        return (f'<h3>{ROMAN[0]}. {bc["tieu_de"]}</h3>'
                + think("🔧 Tình huống ở xưởng", f'<p>{bc["tinh_huong"]}</p>{nghe}')
                + f'<p><strong>Hôm nay em sẽ:</strong> {bc["viec_can_lam"]}</p>'
                + details("Mục tiêu bài và đề cuối kỳ", f'<p>Học xong chương này em cần:</p><ul>{muc_tieu}</ul>'
                          '<p>Đề cuối kỳ có 5 Part; ba Part đầu chỉ cần <strong>nhận ra từ</strong> và <strong>tìm lại câu trong bài đọc</strong>.</p>' + bang))
    return (f'<h3>{ROMAN[0]}. Chương này học gì cho đề cuối kỳ?</h3>'
            f'<p>Đề cuối kỳ luôn có 5 Part. Ba Part đầu chỉ cần <strong>nhận ra từ</strong> và <strong>tìm lại câu trong bài đọc</strong>. Học xong chương này em cần:</p>'
            f'<ul>{muc_tieu}</ul>' + bang)


# ---------- Mục 1: đoán ----------
def sec_doan() -> str:
    # Tiêu đề/lời dẫn theo chương (meta.doan_tieu_de, meta.doan_mo_dau); mặc định là bản Chapter 8.
    out = [f'<h3>{ROMAN[1]}. Đoán trước khi học: {M.get("doan_tieu_de", "máy này tên gì?")}</h3>',
           f'<p>{M.get("doan_mo_dau", "Hai máy dưới đây em đã thấy ở xưởng. Chọn tên tiếng Anh theo trực giác, sai cũng không sao.")}</p>']
    for k in D["khoi_dong"]:
        out.append(photo(k["img"], CREDITS[k["img"]]["file"].rsplit(".", 1)[0].replace("_", " ")))
        out.append(think("🤔 Dự đoán", quiz(k["hoi"], k["lua_chon"], k["dap"], k["fb_ok"], k["fb_no"])))
    return "".join(out)


# ---------- Mục 2: từ vựng ----------
def term_card(t) -> str:
    img = f'<img src="{ASSET_URL}/{t["img"]}.webp" alt="{esc(t["term"])}" loading="lazy" width="{CREDITS[t["img"]]["w"]}" height="{CREDITS[t["img"]]["h"]}">' if t.get("img") else ""
    star = "⭐" * t.get("tier", 1)
    return (f'<div class="avcn-card{"" if img else " avcn-card--noimg"}">{img}<div class="avcn-card__body">'
            f'<p class="avcn-term">{t["term"]} <small>{t["ipa"]}</small> {speak(t["term"])} <span class="avcn-star">{star}</span></p>'
            f'<p class="avcn-vi">{t["vi"]}</p><p class="avcn-def">{t["def"]} {speak(t["def"])}</p></div></div>')


def sec_tu_vung() -> str:
    out = [f'<h3>{ROMAN[2]}. 20 từ ⭐ phải nhận ra</h3>',
           '<p>Học theo cụm 5 từ. Mỗi từ: nhìn ảnh, nghe, đọc nghĩa, rồi đọc <em>định nghĩa tiếng Anh</em>, vì Part 1 ra đề bằng chính định nghĩa đó. Sau mỗi cụm có một câu kiểm tra, làm ngay.</p>']
    if M.get("flashcard"):  # hộp link bộ Flashcard (thêm thẳng trên DB 16/10/2026) — giữ khi dựng lại
        out.append(rule("🃏 Ôn tập Flashcard tương tác (Nhìn ảnh đoán từ & Leitner 3 Hộp)",
                        '<p>Luyện phản xạ nhanh với ảnh máy xưởng thật, nghe phát âm 🔊 bản xứ và lặp lại ngắt quãng:</p>'
                        f'<p><a href="{M["flashcard"]}" target="_blank" class="tl-opt tl-ok" style="display:inline-block; font-weight:700; text-decoration:none; margin-top:4px;">'
                        f'👉 Mở bộ Flashcard Chapter {CH} (Chế độ chuẩn & Luyện đề nhìn ảnh đoán từ)</a></p>'))
    for g in D["tu_vung"]:
        out.append(f'<h4>{g["ten"]}</h4>')
        out.append('<div class="avcn-cards">' + "".join(term_card(t) for t in g["tu"]) + '</div>')
        q = g["quiz"]
        out.append(think("✅ Kiểm tra cụm này", quiz(q["hoi"], q["lua_chon"], q["dap"], q["fb_ok"], q["fb_no"])))
    # ⭐⭐: từ có `img` hiện thẻ ảnh (thêm 16/10/2026, khoá tuỳ chọn); từ không ảnh giữ dạng danh sách
    with_img = [t for t in D["tu_vung_them"] if t.get("img")]
    plain = [t for t in D["tu_vung_them"] if not t.get("img")]
    inner = ""
    if with_img:
        inner += '<div class="avcn-cards">' + "".join(
            f'<div class="avcn-card"><img src="{ASSET_URL}/{t["img"]}.webp" alt="{esc(t["term"])}" loading="lazy" width="{CREDITS[t["img"]]["w"]}" height="{CREDITS[t["img"]]["h"]}">'
            f'<div class="avcn-card__body"><p class="avcn-term">{t["term"]} {speak(t["term"])}</p><p class="avcn-vi">{t["vi"]}</p></div></div>'
            for t in with_img) + '</div>'
    if plain:
        inner += '<ul class="avcn-list">' + "".join(f'<li><strong>{t["term"]}</strong> {speak(t["term"])} — {t["vi"]}</li>' for t in plain) + '</ul>'
    out.append(details(f'⭐⭐ {len(D["tu_vung_them"])} từ thêm cho em muốn làm tốt hơn ({M.get("them_nhan", "bộ phận máy tiện, từ mô tả")})', inner))
    return "".join(out)


# ---------- Mục 3: bài đọc ----------
def sec_bai_doc() -> str:
    out = [f'<h3>{ROMAN[3]}. Bài đọc: Part 2 của đề lấy nguyên văn từ đây</h3>',
           '<p>Đọc từng câu tiếng Anh trước. Chạm vào câu: <strong>đoán nghĩa từ in đậm trước</strong> (chọn 1 trong 3), từ khác chưa biết thì chạm xem nghĩa, rồi mới tự dịch cả câu và mở bản dịch. Bấm 🔊 để nghe. Mục tiêu không phải dịch hay, mà là <strong>nhớ câu nào nói về cái gì</strong> để khi thi tìm lại được.</p>']
    vi_map = {t["term"].lower(): t["vi"] for g in D["tu_vung"] for t in g["tu"]}
    vi_map.update({t["term"].lower(): t["vi"] for t in D["tu_vung_them"]})
    for a in D["bai_doc"]:
        out.append(f'<h4>{a["ten"]}</h4>')
        # Cách thầy dạy (13/10/2026): với TỪNG câu, em đoán nghĩa các từ quan trọng (in đậm) trước, rồi mới mở bản dịch cả câu.
        def key_vi(w):
            return (a.get("tu_khoa") or {}).get(w) or vi_map.get(w.lower()) or next((v for k, v in vi_map.items() if k in w.lower() or w.lower() in k), "")
        for i, cau in enumerate(a["cau"], 1):
            en, vi = cau[0], cau[1]
            them = cau[2] if len(cau) > 2 else {}
            plain = re.sub(r"<[^>]+>", "", en)
            inner = ""
            doan = them.get("doan") or []
            # Thầy chốt 16/10/2026: mỗi câu đố tối đa 2 từ chuyên ngành/từ thi (3 phương án, đoán trước rồi mới biết đáp án);
            # từ thường em không biết thì chạm hiện nghĩa, không đố (G1/N2 — tránh quá tải lựa chọn).
            if doan:
                assert len(doan) <= 2, f"{a['ten']} câu {i}: tối đa 2 từ đố"
                qs = []
                for d in doan:
                    assert len(d["lua_chon"]) == 3, f"{a['ten']} câu {i} '{d['tu']}': cần đúng 3 phương án"
                    dung = d["lua_chon"][d["dap"]]
                    qs.append(quiz(f'<b>{d["tu"]}</b> {speak(d["tu"])} nghĩa là gì?', d["lua_chon"], d["dap"],
                                   d["giai"], f"Nghĩa đúng: <b>{dung}</b>. {d['giai']}"))
                inner += '<p><strong>Bước 1.</strong> Đoán nghĩa từ in đậm. Chọn rồi mới biết đáp án, sai cũng không sao.</p>' + "".join(qs)
                nghia = them.get("nghia") or {}
                if nghia:
                    items = "".join("<li>" + details(f"{w} {speak(w)}", f"<p>{v}</p>") + "</li>" for w, v in nghia.items())
                    inner += f'<p><strong>Bước 2.</strong> Từ khác chưa biết? Chạm để xem nghĩa.</p><ul class="avcn-list">{items}</ul>'
                inner += f'<p><strong>Bước {3 if nghia else 2}.</strong> Ghép lại, tự dịch cả câu trong đầu, rồi mới mở bản dịch.</p>'
            else:
                keys = []
                for w in re.findall(r"<b>(.*?)</b>", en):
                    if w.lower() not in [k.lower() for k in keys]:
                        keys.append(w)
                if keys:
                    items = "".join("<li>" + details(f"{w} {speak(w)}", "<p>" + (key_vi(w) or "(tra ở mục Từ vựng)") + "</p>") + "</li>" for w in keys)
                    inner += f'<p><strong>Bước 1.</strong> Đoán nghĩa các từ in đậm, rồi bấm từng từ để đối chiếu.</p><ul class="avcn-list">{items}</ul><p><strong>Bước 2.</strong> Ghép lại, tự dịch cả câu, rồi mở bản dịch.</p>'
            inner += details("Xem bản dịch cả câu", f'<p class="avcn-trans">{vi}</p>')
            out.append(details(f'<span class="avcn-n">({i})</span> {en} {speak(plain)}', inner, cls="tl-details avcn-sent"))
        q = a["quiz"]
        out.append(think("🔎 Tập làm Part 2 với bài này",
                         quiz(q["hoi"], q["lua_chon"], q["dap"], q["fb_ok"], q["fb_no"])
                         + quiz_tf(a["dung_sai"]["hoi"], a["dung_sai"]["dap"], a["dung_sai"]["fb_ok"], a["dung_sai"]["fb_no"])))
    if D.get("bang"):  # bảng so sánh của chương: {ten, cot[], hang[][]}
        b = D["bang"]
        head = "".join(f"<th>{c}</th>" for c in b["cot"])
        body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in b["hang"])
        out.append(rule(f'📘 {b["ten"]}', f'<div class="table-scroll"><table class="tl-table avcn-tbl"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'))
        return "".join(out)
    out.append(rule("📘 Bảng so sánh 5 phương pháp (hay ra Đúng/Sai)",
                    '<div class="table-scroll"><table class="tl-table avcn-tbl"><thead><tr><th>Method</th><th>Workpiece (phôi)</th><th>Tool (dao)</th></tr></thead><tbody>'
                    '<tr><td>Turning</td><td><strong>rotates</strong></td><td>fixed</td></tr>'
                    '<tr><td>Milling</td><td>fixed</td><td><strong>rotates</strong></td></tr>'
                    '<tr><td>Drilling</td><td>fixed</td><td>bit <strong>rotates</strong></td></tr>'
                    '<tr><td>Grinding</td><td>moves</td><td>abrasive wheel spins</td></tr>'
                    '<tr><td>Sawing</td><td>clamped</td><td>toothed blade</td></tr></tbody></table></div>'))
    return "".join(out)


# ---------- Mục 4: mẫu câu ----------
def sec_mau_cau() -> str:
    out = [f'<h3>{ROMAN[4]}. Hai mẫu câu đủ dùng cho Part 4 và Part 5</h3>',
           '<p>Không cần học hết ngữ pháp. Đề dịch của chương này chỉ dùng hai mẫu dưới đây.</p>']
    for m in D["mau_cau"]:
        vd = "".join(f'<li>{en} {speak(en)}<br><span class="avcn-trans">{vi}</span></li>' for en, vi in m["vd"])
        out.append(rule(f'📘 {m["ten"]}', f'<ul class="avcn-list">{vd}</ul>{nl(m["ghi_chu"])}'))
    return "".join(out)


# ---------- Mục 5: gắn nhãn máy tiện ----------
def lathe_svg(numbers_only: bool) -> str:
    svg = (ASSET_DIR / "lathe_diagram.svg").read_text(encoding="utf-8")
    svg = re.sub(r'<text[^>]*>(CƠ CẤU MÁY TIỆN|Chạm/rà chuột)[^<]*</text>', "", svg)
    svg = re.sub(r'\s(width|height|style)="[^"]*"', "", svg, count=3)
    if numbers_only:
        svg = re.sub(r'<text[^>]*>(GEARBOX|Rotation \(Quay\)|Feed \(Tiến dao\))</text>', "", svg)
        def badge(m):
            w = int(m.group(1)); cx = w // 2
            return (f'<rect x="{cx-22}" y="-6" width="44" height="34" rx="17" fill="#0284c7"/>\n'
                    f'    <text x="{cx}" y="19" text-anchor="middle" fill="#ffffff" font-size="24" font-weight="bold">{m.group(2)}</text>')
        svg = re.sub(r'<rect width="(\d+)" height="22" rx="11" fill="#0284c7"/>\s*<text x="\d+" y="15"[^>]*>(\d)\. [A-Za-z ]+</text>', badge, svg)
    return svg


def sec_gan_nhan() -> str:
    g = D["gan_nhan"]
    if g.get("svg"):  # hình gắn nhãn riêng của chương (SVG chỉ có số) + bo_phan [[term, vi], ...]
        svg = (ASSET_DIR / g["svg"]).read_text(encoding="utf-8")
        n = len(g["bo_phan"])
        ans = "".join(f'<li><strong>{i}. {t}</strong> {speak(t)} — {v}</li>' for i, (t, v) in enumerate(g["bo_phan"], 1))
        return (f'<h3>{ROMAN[5]}. {g["tieu_de"]}</h3><p>{g["mo_ta"]}</p>'
                f'<figure class="fig" data-tl="1">{svg}<figcaption>Hình 1. {g["chu_thich"]}</figcaption></figure>'
                + think("✅ Kiểm tra", quiz(g["hoi"], g["lua_chon"], g["dap"], g["fb_ok"], g["fb_no"]))
                + details(f"Xem đáp án {n} bộ phận", f'<ul class="avcn-list">{ans}</ul>'))
    names = ["headstock", "chuck", "tool post", "tailstock", "carriage", "bed", "lead screw"]
    vi = dict((t["term"], t["vi"]) for t in D["tu_vung_them"])
    ans = "".join(f'<li><strong>{i}. {n}</strong> {speak(n)} — {vi.get(n, "")}</li>' for i, n in enumerate(names, 1))
    return (f'<h3>{ROMAN[5]}. Bộ phận máy tiện: nói được tên khi chỉ vào máy</h3>'
            '<p>Giáo trình có bài Speaking "mô tả các bộ phận máy tiện". Nhìn hình, tự gọi tên 7 bộ phận trước, rồi mở đáp án.</p>'
            f'<figure class="fig" data-tl="1">{lathe_svg(True)}<figcaption>Hình 1. Máy tiện: 7 bộ phận đánh số. Tự gọi tên trước khi mở đáp án.</figcaption></figure>'
            + think("✅ Kiểm tra", quiz(g["hoi"], g["lua_chon"], g["dap"], g["fb_ok"], g["fb_no"]))
            + details("Xem đáp án 7 bộ phận", f'<ul class="avcn-list">{ans}</ul>'))


# ---------- Mục 6: SOP ----------
def sec_sop() -> str:
    s = D["sop"]
    box = " · ".join(f"<strong>{w}</strong>" for w in s["hop_tu"])
    dap = "".join(f"<li>({i}) {w}</li>" for i, w in enumerate(s["dap"], 1))  # <ul>
    q = s["quiz"]
    doan_noi = re.sub(r"\(\d\) ______", "", s["doan"])
    return (f'<h3>{ROMAN[6]}. {s.get("tieu_de", "Vận hành máy tiện: điền động từ (kiểu Part 3)")}</h3>'
            f'<p>Part 3 cho một hộp từ và một đoạn văn có chỗ trống. Cách làm: đọc cả câu, nhìn từ đứng <em>ngay sau</em> chỗ trống, rồi chọn từ trong hộp. {s.get("mo_ta", "Thử với đoạn hướng dẫn vận hành máy tiện:")}</p>'
            f'<p class="avcn-box">Hộp từ: {box}</p>'
            f'<div class="avcn-passage"><p>{s["doan"]} {speak(doan_noi)}</p></div>'
            + think("✅ Kiểm tra", quiz(q["hoi"], q["lua_chon"], q["dap"], q["fb_ok"], q["fb_no"]))
            + details("Xem đáp án cả 5 chỗ trống", f'<ul class="avcn-list">{dap}</ul>'))


# ---------- Mục 7: trả bài ----------
def sec_tra_bai() -> str:
    items = "".join(details(q, f'<p>{a}</p>') for q, a in D["tra_bai"])
    return (f'<h3>{ROMAN[7]}. Trả bài: gấp sách lại, trả lời 8 câu</h3>'
            '<p>Nhớ lại được là nhớ lâu. Với mỗi câu: <strong>nói ra đáp án trước</strong>, rồi mới bấm mở. Câu nào không trả lời được thì quay lên mục tương ứng, rồi sang tab <strong>Đề mẫu</strong>.</p>'
            + think("🎤 Trả bài", items)
            + (f'<p><strong>Quay lại tình huống đầu bài:</strong> {M["boi_canh"]["quay_lai"]}</p>' if M.get("boi_canh") else ""))


def build_theory() -> str:
    parts = [sec_thi(), sec_doan(), sec_tu_vung(), sec_bai_doc(), sec_mau_cau(), sec_gan_nhan(), sec_sop(), sec_tra_bai()]
    html = "\n".join(parts) + "\n"
    return html + sec_nguon_anh(html)


# ---------- Nguồn ảnh (CC BY / BY-SA đòi ghi tác giả; thêm 16/10/2026) ----------
def sec_nguon_anh(html: str) -> str:
    used = []
    for k in re.findall(rf'{re.escape(ASSET_URL)}/([\w\-]+)\.webp', html):
        if k in CREDITS and k not in used:
            used.append(k)
    rows = []
    for k in used:
        c = CREDITS[k]
        if not c.get("author") or "wikimedia.org" not in str(c.get("page", "")):
            continue  # hình tự vẽ không cần ghi nguồn
        rows.append(f'<li>{esc(k.replace("-", " "))}: {esc(c["author"])}, {esc(c["license"])}, <a href="{esc(c["page"])}" target="_blank" rel="noopener">Wikimedia Commons</a></li>')
    if not rows:
        return ""
    return details(f"Nguồn ảnh ({len(rows)} ảnh)", '<ul class="avcn-list">' + "".join(rows) + "</ul>")


# ---------- Đề mẫu (tab Bài mẫu) ----------
def worked_examples():
    """Tab Bài mẫu: 5 Part, mỗi câu là quiz tự chấm (Part 1–3), Part 4–5 là bản dịch mở dần. Tiền tố radio riêng để không trùng tab Học."""
    e = D["de_mau"]
    X = f"{P}m"
    out = []

    def tactic(items):
        return f'<div class="tl-box tl-box--rule"><p class="tl-label">🎯 Chiến thuật</p>{nl(items)}</div>'

    # Part 1
    body = ['<p><strong>Part 1: Choose the correct answer.</strong> (đề thật 10 câu)</p>', tactic(e["part1_chien_thuat"])]
    for i, q in enumerate(e["part1"], 1):
        if q.get("img"):  # câu "Look at the picture": nhúng ảnh thật (khoá ảnh trong credits.json), không ghi chú [hình: …] lộ đáp án
            body.append(photo(q["img"], f"Hình câu {i}", small=True))
        body.append(quiz(f'<strong>{i}.</strong> {q["q"]}', q["opts"], q["ans"], q["why"], "Gạch từ khoá trong định nghĩa rồi so với nghĩa đã học.", prefix=X))
    out.append({"label": "Part 1 · Chọn từ theo định nghĩa / ảnh", "body_html": "".join(body)})
    # Part 2
    p2 = e["part2"]
    body = ['<p><strong>Part 2: Read the article and answer the questions.</strong></p>', tactic(e["part2_chien_thuat"]),
            f'<div class="avcn-passage"><p>{p2["doan"]}</p></div>', '<p><strong>2.1 Fill in the blanks with one word from the article.</strong></p>']
    for i, q in enumerate(p2["dien"], 1):
        body.append(quiz(f'<strong>{i}.</strong> {q["q"]}', q["opts"], q["opts"].index(q["ans"]), q["why"], "Tìm câu trong đoạn có cùng từ khoá với câu hỏi, rồi chép đúng từ.", prefix=X))
    body.append('<p><strong>2.2 True (T) or False (F)?</strong></p>')
    for i, q in enumerate(p2["ds"], 1):
        body.append(quiz_tf(f'<strong>{i}.</strong> {q["q"]}', q["ans"], q["why"], "So từng chữ với câu trong đoạn: chỗ nào bị đổi?", prefix=X))
    out.append({"label": "Part 2 · Đọc hiểu: điền 1 từ + Đúng/Sai", "body_html": "".join(body)})
    # Part 3
    p3 = e["part3"]
    body = ['<p><strong>Part 3: Fill in the blanks using the words in the box.</strong></p>', tactic(p3["chien_thuat"]),
            f'<p class="avcn-box">Hộp từ: {" · ".join(f"<strong>{w}</strong>" for w in p3["hop_tu"])}</p>',
            f'<div class="avcn-passage"><p>{p3["doan"]}</p></div>']
    for i, w in enumerate(p3["dap"], 1):
        body.append(quiz(f'Chỗ trống <strong>({i})</strong>:', p3["hop_tu"], p3["hop_tu"].index(w), f'({i}) = <em>{w}</em>.', "Đọc lại cả câu chứa chỗ trống: từ đứng trước và sau nó gợi loại từ gì?", prefix=X))
    out.append({"label": "Part 3 · Điền từ cho sẵn", "body_html": "".join(body)})
    # Part 4
    p4 = e["part4"]
    body = ['<p><strong>Part 4: Translate the paragraph into Vietnamese.</strong></p>', tactic(p4["chien_thuat"]),
            f'<div class="avcn-passage"><p>{p4["en"]}</p></div>',
            '<p>Viết bản dịch của em ra giấy trước, rồi mới mở bản tham khảo và tự so từng cụm.</p>',
            details("Bản dịch tham khảo", f'<p>{p4["vi"]}</p>')]
    out.append({"label": "Part 4 · Dịch Anh → Việt", "body_html": "".join(body)})
    # Part 5
    p5 = e["part5"]
    body = ['<p><strong>Part 5: Translate the sentence into English.</strong></p>', tactic(p5["chien_thuat"]),
            f'<div class="avcn-passage"><p>{p5["vi"]}</p></div>',
            '<p>Viết câu tiếng Anh của em ra giấy trước, rồi mới mở câu tham khảo.</p>',
            details("Câu tham khảo", f'<p>{p5["en"]}</p>')]
    out.append({"label": "Part 5 · Dịch Việt → Anh", "body_html": "".join(body)})
    return out


def exam_questions():
    L = D["luyen_tap"]
    topic = f"AVCN C{CH}: {M['title_en']}"
    qs = []
    for q in L["mc"]:
        qs.append({"type": "multiple_choice", "question": q["q"], "options": q["opts"], "answer": q["ans"],
                   "explanation": q["why"], "topic": topic, "form": "ly_thuyet", "difficulty": "de"})
    for q in L["tf"]:
        qs.append({"type": "true_false", "question": q["q"], "statements": [{"text": t, "answer": a} for t, a in q["st"]],
                   "explanation": q["why"], "topic": topic, "form": "ly_thuyet", "difficulty": "de"})
    return topic, qs


def main():
    theory = build_theory()
    n_theory = _qn[0]
    (HERE / "theory.html").write_text(theory, encoding="utf-8")
    topic, qs = exam_questions()
    bundle = {
        "schema": "thachlab.lesson-bundle/v1",
        "target": {"class_name": "Anh văn chuyên ngành Cơ khí", "chapter_title": "Technical English for Mechanical Engineering",
                   "lesson_title": f"Chapter {CH}: {M['title_en']} — {M['title_vi']}"},
        "theory_title": "Học",
        "theory_subtitle": f"{M['minutes']} phút · 20 từ ⭐ · {len(D['bai_doc'])} bài đọc",
        "theory_html": theory,
        "worked_examples": worked_examples(),
        "exam": {"title": f"Luyện tập Chapter {CH}: {M['title_en']}", "topic": topic, "difficulty": "de",
                 "duration_minutes": 20, "subject_code": "avcn", "questions": qs, "new_topics": [topic]},
        "raster_images": [],
    }
    (HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf-8")
    words = len(re.sub(r"<[^>]+>", " ", theory).split())
    print(f"theory.html {len(theory)} ký tự, ~{words} từ, {n_theory} quiz · bundle: {len(bundle['worked_examples'])} Part mẫu, {len(qs)} câu luyện tập")


if __name__ == "__main__":
    main()
