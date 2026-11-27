"""✓ Soát nhanh cho khoá HSG KHTN 9 (bảng tra: docs/BANG-MEO-GIAI.md mục "HSG KHTN 9", bảng D) — vá tại chỗ <id>.json.

Đổi bước "Kiểm tra" cuối thành câu Soát nhanh (`soat` + `hoi` + `lua_chon`), giữ nguyên nội dung giải thích của bước.
Cùng cách làm với them-soat-nhanh-l12-ch1.py (chặng 7); chạy lại an toàn.   python3 scripts/data/bai-tap-mau/them-soat-nhanh-hsg9.py
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def ch(text, dung=False, vi_sao=None):
    c = {"text": text}
    c["dung"] = bool(dung)  # các bước khác của bài 165 ghi rõ dung: false
    if not dung:
        c["vi_sao"] = vi_sao
    return c


SOAT = {
    # CĐ05 (165) d5: cực đại công suất trên biến trở, R0 = 6 Ω nối tiếp, U = 24 V (R = 18 Ω cho 18 W là số của câu c)
    (165, 5): dict(soat="gioi_han",
        hoi="Cho $R$ rất nhỏ rồi $R$ rất lớn. Công suất trên biến trở tiến về đâu?",
        lua_chon=[ch("Cả hai đầu đều về 0, nên chỗ lớn nhất nằm ở giữa", True),
                  ch("R rất nhỏ thì lớn nhất, vì dòng lớn nhất", vi_sao="Dòng lớn nhất khi $R=0$, nhưng hiệu điện thế trên biến trở khi đó bằng 0, nên $P_R=I^2R=0$."),
                  ch("R càng lớn thì công suất càng lớn", vi_sao="$R$ rất lớn thì dòng rất nhỏ, $P_R=I^2R$ giảm dần về 0: ở $R=18\\ \\Omega$ đã chỉ còn $18\\ \\text{W}$, nhỏ hơn $24\\ \\text{W}$.")],
        loi_hay_gap="Cho rằng dòng lớn nhất hoặc điện trở lớn nhất thì công suất lớn nhất. Thử hai đầu mút $R\\to0$ và $R$ rất lớn trước khi tin đáp số."),
}

TITLE = re.compile(r'(<span class="bt-step-n">\d+</span><span>)Kiểm tra(</span>)')

for lesson in sorted({k[0] for k in SOAT}):
    p = os.path.join(HERE, f"{lesson}.json")
    J = json.load(open(p, encoding="utf-8"))
    for (les, d), s in SOAT.items():
        if les != lesson:
            continue
        dang = J["dang_bai"][d - 1]
        last = dang["buoc"][-1]
        if last.get("soat"):
            if last != {"tieu_de": "Soát nhanh", **s}:
                dang["buoc"][-1] = {"tieu_de": "Soát nhanh", **s}; print(f"{lesson} d{d}: cập nhật Soát nhanh")
            continue
        assert last["tieu_de"] == "Kiểm tra" and not last.get("hoi"), (lesson, d, last)
        html = dang["solution_html"]
        hits = list(TITLE.finditer(html))
        assert len(hits) == 1, (lesson, d, len(hits))
        dang["solution_html"] = html[:hits[0].start()] + hits[0].group(1) + "Soát nhanh" + hits[0].group(2) + html[hits[0].end():]
        dang["buoc"][-1] = {"tieu_de": "Soát nhanh", **s}
        print(f"{lesson} d{d}: + Soát nhanh ({s['soat']})")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1)
        f.write("\n")
