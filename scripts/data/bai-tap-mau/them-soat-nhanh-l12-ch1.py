"""Chặng 7 kế hoạch mẹo giải (18/11/2026): thí điểm ✓ Soát nhanh ở L12 Ch.1 Nhiệt — lesson 3, 4, 5, 8 dạng.

Đổi bước "Kiểm tra" cuối thành câu Soát nhanh (`soat` + `hoi` + `lua_chon`), giữ nguyên nội dung giải thích của bước
(hiện sau khi em trả lời). Vá tại chỗ, không chạy lại build-hinh-<id>.py. Chạy lại an toàn (bỏ qua dạng đã vá).
Bảng tra: docs/BANG-MEO-GIAI.md mục ✓.   python3 scripts/data/bai-tap-mau/them-soat-nhanh-l12-ch1.py
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def ch(text, dung=False, vi_sao=None):
    c = {"text": text}
    if dung:
        c["dung"] = True
    else:
        c["vi_sao"] = vi_sao
    return c


SOAT = {
    # Bài 2. Thang nhiệt độ
    (3, 3): dict(soat="co_so",
        hoi="Ở nhiệt độ dương, đổi từ °F sang °C thì số đọc phải lớn lên hay nhỏ đi?",
        lua_chon=[ch("Nhỏ đi: phải trừ 32 rồi chia cho 1,8", True),
                  ch("Lớn lên: nhân 1,8 rồi cộng 32", vi_sao="Đó là chiều °C → °F. Đi ngược thì làm phép ngược: trừ 32 trước, chia 1,8 sau."),
                  ch("Giữ nguyên, chỉ đổi ký hiệu", vi_sao="Hai thang khác cả gốc (0 °C ứng với 32 °F) lẫn độ lớn một độ, nên số đọc phải đổi.")],
        loi_hay_gap="Đổi °F sang °C mà ra số lớn hơn số °F ban đầu (ở nhiệt độ dương) là đã dùng nhầm công thức chiều °C → °F."),
    (3, 4): dict(soat="co_so",
        hoi="Chênh lệch nhiệt độ trong một ngày đổi ra kelvin là hàng chục hay hàng trăm?",
        lua_chon=[ch("Hàng chục: chênh lệch trên thang Kelvin bằng chênh lệch trên thang Celsius", True),
                  ch("Hàng trăm, vì số đọc kelvin luôn lớn hơn số đọc °C 273 đơn vị", vi_sao="Số 273 có ở cả hai đầu nên triệt tiêu khi lấy hiệu; chỉ một giá trị nhiệt độ mới cộng 273.")],
        loi_hay_gap="Cộng 273 vào khoảng chênh: ra hàng trăm kelvin cho một ngày nắng là dấu hiệu đã sai."),
    # Bài 3. Nội năng. Định luật 1
    (4, 2): dict(soat="dau_chieu",
        hoi="Giai đoạn 2, khí nhận nhiệt nhưng ΔU₂ âm. Có hợp lí không?",
        lua_chon=[ch("Hợp lí: công khí sinh ra (150 J) lớn hơn nhiệt nhận vào (130 J)", True),
                  ch("Không: khí nhận nhiệt thì nội năng phải tăng", vi_sao="Nội năng tăng hay giảm do TỔNG năng lượng vào và ra; khí còn sinh công đưa năng lượng ra ngoài.")],
        loi_hay_gap="Chỉ nhìn chữ “nhận nhiệt” mà kết luận nội năng tăng — phải so cả công khí sinh ra."),
    (4, 3): dict(soat="dau_chieu",
        hoi="Quá trình 1, khí bị nén (nhận công) mà nội năng vẫn giảm. Khí phải toả hay thu nhiệt?",
        lua_chon=[ch("Toả nhiệt, và nhiều hơn công nhận vào", True),
                  ch("Thu nhiệt, vì đã nhận công thì cũng nhận nhiệt", vi_sao="Nhận công và nhận nhiệt là hai đường riêng. Nhận công mà nội năng vẫn giảm thì nhiệt phải đi ra."),
                  ch("Không trao đổi nhiệt", vi_sao="Khi Q = 0 thì ΔU = A > 0, nội năng phải tăng — trái với đề.")],
        loi_hay_gap="Coi “nội năng giảm 35 J” là ΔU = +35 J thì ra khí thu nhiệt, trái với việc nội năng giảm."),
    (4, 4): dict(soat="dau_chieu",
        hoi="Khối đồng toả nhiệt cho nước mà nội năng của đồng vẫn tăng. Có hợp lí không?",
        lua_chon=[ch("Hợp lí: công mũi khoan đưa vào lớn hơn nhiệt đồng toả cho nước", True),
                  ch("Không: vật toả nhiệt thì nội năng phải giảm", vi_sao="Đồng còn nhận công của mũi khoan; nội năng tăng khi năng lượng vào (công) lớn hơn năng lượng ra (nhiệt).")],
        loi_hay_gap="Xét riêng chiều nhiệt mà quên công mũi khoan — phải cộng cả A và Q với dấu của chúng."),
    # Bài 4. Thực hành đo c, λ, L
    (5, 1): dict(soat="co_so",
        hoi="Nhiệt dung riêng của dầu ăn hợp lí ở cỡ nào?",
        lua_chon=[ch("Cỡ nghìn J/(kg·K), cùng bậc với c của nước (4200)", True),
                  ch("Cỡ vài J/(kg·K)", vi_sao="Ra cỡ vài đơn vị là đã để khối lượng bằng gam — nhỏ đi 1000 lần."),
                  ch("Cỡ vài chục J/(kg·K)", vi_sao="Ra cỡ vài chục là đã thế τ bằng phút — Q nhỏ đi 60 lần; chất lỏng quen thuộc có c cỡ nghìn J/(kg·K).")],
        loi_hay_gap="Để m bằng gam hoặc τ bằng phút thì c lệch cả nghìn lần — so ngay với c của nước."),
    (5, 2): dict(soat="co_so",
        hoi="Ba giá trị đo được đều lớn hơn số tra bảng một chút. Điều đó cho biết gì?",
        lua_chon=[ch("Hợp lí: cùng bậc với số tra bảng, lớn hơn chút ít do một phần nhiệt mất ra ngoài", True),
                  ch("Đã lấy sai mốc thời gian", vi_sao="Lấy nhầm mốc (như mốc cuối tính từ gốc) làm kết quả lớn gấp mấy lần, không chỉ lớn hơn vài phần trăm.")],
        loi_hay_gap="Lấy mốc cuối của đồ thị làm độ dài đoạn ngang thì L lớn gấp mấy lần số tra bảng — lệch quá xa là sai mốc."),
    (5, 3): dict(soat="co_so",
        hoi="Nhiệt dung riêng vừa tìm có hợp lí với một kim loại không?",
        lua_chon=[ch("Có: cùng bậc trăm J/(kg·K) như bảng, nhỏ hơn hẳn c của nước", True),
                  ch("Không: c của kim loại phải lớn hơn c của nước", vi_sao="Nước có c rất lớn (4200 J/(kg·K)); kim loại trong bảng chỉ vài trăm.")],
        loi_hay_gap="Quên nhiệt dung của vỏ nhiệt lượng kế thì c lệch khỏi bảng — luôn đối chiếu với bảng c."),
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
            print(f"{lesson} d{d}: đã có soat, bỏ qua"); continue
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
