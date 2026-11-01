# Gom câu cũ của bài 83, 84 (đăng 12/10 bằng --giu-cu nên còn nằm rời sau các dạng mới) thành một mục "Bài tập tự luận".
# Nguồn: old/<id>.json (dump-bai-tap-mau-cu.mts 1/11/2026). Chỉ ghi khoá tu_luan của <id>.json; dạng mới không đổi.
import json, os, re
D = os.path.dirname(os.path.abspath(__file__))

def tach(old, n_moi):
    """Câu cũ nằm sau n_moi dạng mới; mục 'Dạng 2: …' của bài 83 gộp nhiều câu → tách theo 'Câu N.'."""
    cau = {}
    for x in old[n_moi:]:
        for p in re.split(r'(?=<p[^>]*>\s*<strong[^>]*>\s*Câu \d+\.)', x["body_html"]):
            m = re.search(r'Câu (\d+)\.', p)
            if m and int(m.group(1)) not in cau:
                cau[int(m.group(1))] = p
    return cau

def tu_luan(cau, order, muc):
    parts = []
    for k, c in enumerate(order, 1):
        h = re.sub(r'<strong[^>]*>\s*Câu \d+\.\s*</strong>\s*', '', cau[c], count=1)
        h = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", h)
        h = re.sub(r'alt="[^"]*"', f'alt="Hình bài {k}"', h)   # alt cũ chứa cả đoạn đề lẫn "Câu N." do lúc nhập
        m = re.search(r'<p[^>]*>\s*<strong[^>]*>\s*Hướng dẫn giải\s*</strong>\s*</p>', h)
        if m:
            h = h[:m.start()] + '<details><summary>Hướng dẫn giải</summary>' + h[m.end():] + '</details>'
        parts.append(f'<h4>Bài {k} · {muc[c]}</h4>{h}')
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))

DE, TB, KHO = "Dễ", "Trung bình", "Khó"
CAU = {
    # Câu 15 bỏ: đề mất giá trị chiết suất ("n = ." — MathType rơi khi nhập).
    83: (5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 16, 18],
         {**{c: DE for c in (1, 2, 3, 4, 5, 6)}, **{c: TB for c in (7, 8, 9, 10, 11, 12, 13, 14, 17)}, 16: KHO, 18: KHO}),
    84: (4, [4, 6, 1, 2, 3, 5, 7], {4: DE, 6: DE, 1: DE, 2: TB, 3: TB, 5: TB, 7: TB}),
}
for lid, (n_moi, order, muc) in CAU.items():
    old = json.load(open(f"{D}/old/{lid}.json"))["questions"]
    p = f"{D}/{lid}.json"; d = json.load(open(p))
    assert len(d["dang_bai"]) == n_moi
    cau = tach(old, n_moi)
    d["tu_luan"] = tu_luan(cau, order, muc)
    json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
    print(lid, "câu cũ:", sorted(cau), "→ tự luận", len(order), "bài")
