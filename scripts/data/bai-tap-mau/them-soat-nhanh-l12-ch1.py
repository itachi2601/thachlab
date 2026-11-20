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
        hoi="Nén khí, khí nhận 25 J công mà nội năng vẫn giảm 35 J. Nhiệt toả ra lớn hơn hay nhỏ hơn 25 J?",
        lua_chon=[ch("Lớn hơn 25 J: nhiệt toả phải bù cả công nhận vào lẫn phần nội năng giảm", True),
                  ch("Nhỏ hơn 25 J", vi_sao="Nhiệt toả nhỏ hơn công nhận thì ΔU = A + Q > 0, nội năng tăng — trái với đề."),
                  ch("Đúng bằng 25 J", vi_sao="Khi đó ΔU = 0, nội năng không đổi — trái với đề.")],
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
    (5, 2): dict(soat="dau_chieu",
        hoi="Một phần nhiệt của bếp mất ra ngoài. Vậy c, λ, L đo được lớn hơn hay nhỏ hơn giá trị thật?",
        lua_chon=[ch("Lớn hơn: Pτ đã tính cả phần nhiệt mất, đem chia cho m nên ra số lớn hơn", True),
                  ch("Nhỏ hơn: nhiệt mất ra ngoài thì số đo phải nhỏ đi", vi_sao="Số đo tính từ Pτ, mà Pτ gồm cả phần nhiệt mất; nước nhận ít hơn Pτ nên chia ra lớn hơn thật.")],
        loi_hay_gap="Nghĩ mất nhiệt làm kết quả nhỏ đi — thật ra Pτ đã gồm phần mất nên c, λ, L ra lớn hơn giá trị thật."),
    (5, 3): dict(soat="co_so",
        hoi="Nhiệt dung riêng vừa tìm có hợp lí với một kim loại không?",
        lua_chon=[ch("Có: cùng bậc trăm J/(kg·K) như bảng, nhỏ hơn hẳn c của nước", True),
                  ch("Không: c của kim loại phải lớn hơn c của nước", vi_sao="Nước có c rất lớn (4200 J/(kg·K)); kim loại trong bảng chỉ vài trăm.")],
        loi_hay_gap="Lấy Δt của kim loại là 25 − 20 = 5 K thay vì 100 − 25 = 75 K thì c ra cỡ nghìn J/(kg·K), lớn hơn cả c của nước — dấu hiệu đã sai."),
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
        if last.get("soat"):  # chạy lại sau khi sửa câu chữ: ghi đè nội dung, tiêu đề đã đổi
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
