"""Chặng 8 kế hoạch mẹo giải (18/11/2026): ⚖ Lập tỉ số — vá các dạng "so hai trạng thái" chưa theo quy tắc ⚖.

Chọn dạng: quét 37 dạng có bước đáp số "lần" + số sai theo question_dang 60 ngày (scripts/sql/dang-sai-nhieu.sql).
Phần lớn dạng tỉ số đã đúng quy tắc (9·2, 19·3, 28·4, 70·1, 159·3, 164·1). Vá 4 dạng:
  26·3  Đồ thị năng lượng theo li độ (76 % sai, 96 lượt — dạng sai nhiều thứ 2 toàn site): W_t/W = (x/A)², khỏi đổi đơn vị
  152·4 Hao phí truyền tải: bỏ tính I', P'hp riêng rồi mới chia → một dòng (U'/U)²
  15·3  Bán kính hạt nhân: tỉ số lấy từ số khối (A_U/A_Zn)^(1/3), không chia hai số đã làm tròn
  40·2  Năng lượng tụ: thêm câu nhận dạng ⚖
Số bước không đổi (khớp .bt-step). Chạy lại an toàn (mỗi thay thế kiểm chuỗi gốc, đã vá thì bỏ qua).
Bảng tra: docs/BANG-MEO-GIAI.md mục ⚖.   python3 scripts/data/bai-tap-mau/them-ti-so-chang8.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DAU = "⚖"  # dấu đã vá

def thay(s, cu, moi, nhan):
    if moi in s:
        return s
    assert s.count(cu) == 1, f"{nhan}: chuỗi gốc xuất hiện {s.count(cu)} lần"
    return s.replace(cu, moi)


def vá(lesson, dang_no, fn):
    p = os.path.join(HERE, f"{lesson}.json")
    d = json.load(open(p, encoding="utf-8"))
    x = d["dang_bai"][dang_no - 1]
    so_buoc = x["solution_html"].count('class="bt-step"')
    fn(x)
    assert x["solution_html"].count('class="bt-step"') == so_buoc == len(x["buoc"]), f"{lesson}·{dang_no}: lệch số bước"
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(p, "a", encoding="utf-8").write("\n")
    print(f"{lesson}·{dang_no} ✓")


# 26·3 — Bài 7. Bài tập về sự chuyển hoá năng lượng trong dao động điều hoà
def d26_3(x):
    s = x["solution_html"]
    s = thay(s,
        r"$$W_t=\dfrac{1}{2}kx^2=\dfrac{1}{2}\cdot20\cdot0{,}03^2=9\ \text{mJ}$$",
        r"<p>Cùng lò xo nên $k$ giữ nguyên; lập tỉ số với cơ năng, khỏi đổi đơn vị:</p>"
        r"$$\dfrac{W_t}{W}=\dfrac{\frac{1}{2}kx^2}{\frac{1}{2}kA^2}=\left(\dfrac{x}{A}\right)^2$$"
        r"$$\dfrac{W_t}{W}=\left(\dfrac{3}{6}\right)^2=\dfrac{1}{4}$$"
        r"$$W_t=\dfrac{36}{4}=9\ \text{mJ}$$", "26·3 bước 2")
    s = thay(s,
        r"rồi $k=\dfrac{2W}{A^2}$.</p>",
        r"rồi $k=\dfrac{2W}{A^2}$. Hỏi năng lượng tại li độ $x$ → ⚖ lập tỉ số $\dfrac{W_t}{W}=\left(\dfrac{x}{A}\right)^2$, giữ nguyên $k$.</p>",
        "26·3 nhận dạng")
    x["solution_html"] = s
    b = x["buoc"][1]
    if DAU not in b["loi_hay_gap"]:
        b["loi_hay_gap"] += r" ⚖ Lấy $\dfrac{W_t}{W}=\dfrac{x}{A}=\dfrac{1}{2}$ (quên bình phương) thì ra $W_t=18$ mJ, sai."
    b["chon_buoc_ke"][0]["text"] = r"$\dfrac{W_t}{W}=\left(\dfrac{x}{A}\right)^2$ rồi $W_{\text{đ}}=W-W_t$"


# 152·4 — Chuyên đề 08. Cảm ứng điện từ (HSG 9): hao phí truyền tải
def d152_4(x):
    x["solution_html"] = thay(x["solution_html"],
        r"<p>$U$ tăng $\dfrac{60}{15}=4$ lần nên $I$ giảm $4$ lần :</p>$$I'=\dfrac{600\,000}{60\,000}=10\ \text{A}$$"
        r"$$P'_{\text{hp}}=24\cdot10^2=2400\ \text{W}$$$$\dfrac{P_{\text{hp}}}{P'_{\text{hp}}}=\dfrac{38\,400}{2400}=16=4^2$$",
        r"<p>Giữ nguyên $P$ truyền đi và $R$ của dây ; $P_{\text{hp}}=\dfrac{P^2R}{U^2}$ nên ⚖ lập tỉ số, khỏi tính lại $I$ :</p>"
        r"$$\dfrac{P_{\text{hp}}}{P'_{\text{hp}}}=\left(\dfrac{U'}{U}\right)^2=\left(\dfrac{60}{15}\right)^2=4^2=16$$"
        r"$$P'_{\text{hp}}=\dfrac{38\,400}{16}=2400\ \text{W}$$",
        "152·4 bước 4")


# 15·3 — Bài 14. Hạt nhân và mô hình nguyên tử (L12)
def d15_3(x):
    s = x["solution_html"]
    s = thay(s,
        r"$$\dfrac{R_{\text{U}}}{R_{\text{Zn}}}=\dfrac{7{,}44}{4{,}8}$$",
        r"<p>Cùng hệ số $1{,}2\cdot10^{-15}$ nên giữ nguyên, ⚖ chỉ còn tỉ số số khối (khỏi chia hai số đã làm tròn):</p>"
        r"$$\dfrac{R_{\text{U}}}{R_{\text{Zn}}}=\left(\dfrac{238}{64}\right)^{1/3}$$",
        "15·3 bước 3")
    s = thay(s,
        r"=\left(\dfrac{R_{\text{U}}}{R_{\text{Zn}}}\right)^3=1{,}55^3$$",
        r"=\left(\dfrac{R_{\text{U}}}{R_{\text{Zn}}}\right)^3=\dfrac{238}{64}$$",
        "15·3 bước 4")
    x["solution_html"] = s
    x["buoc"][2]["chon_buoc_ke"][0]["text"] = r"Lập tỉ số: hệ số $1{,}2\cdot10^{-15}$ triệt tiêu, còn $\left(\dfrac{A_{\text{U}}}{A_{\text{Zn}}}\right)^{1/3}$"


# 40·2 — Bài 21. Tụ điện (L11)
def d40_2(x):
    x["solution_html"] = thay(x["solution_html"],
        r"→ dùng $W=\dfrac12CU^2$ (hoặc $\dfrac12QU$).</p>",
        r"→ dùng $W=\dfrac12CU^2$ (hoặc $\dfrac12QU$). Thấy <strong>$U$ tăng/giảm $n$ lần trên cùng một tụ</strong> → ⚖ lập tỉ số $\dfrac{W'}{W}=\left(\dfrac{U'}{U}\right)^2$, giữ nguyên $C$.</p>",
        "40·2 nhận dạng")


# Bổ sung sau soát kiem-code (18/11): câu ⚖ vào trường `nhan_dang` (hiện trên thẻ dạng), lựa chọn bước kế 40·2, kiểm độc lập 15·3.
def them_nhan_dang(x, ve):
    if DAU not in x["nhan_dang"]:
        x["nhan_dang"] = x["nhan_dang"].rstrip(". ") + ". " + ve


def bo_sung_26(x):
    them_nhan_dang(x, r"Hỏi năng lượng tại li độ $x$ → <b>⚖ lập tỉ số</b> $\dfrac{W_t}{W}=\left(\dfrac{x}{A}\right)^2$.")


def bo_sung_152(x):
    them_nhan_dang(x, r"<b>⚖ lập tỉ số</b> $\left(\dfrac{U'}{U}\right)^2$, không tính lại $I$.")


def bo_sung_15(x):
    them_nhan_dang(x, r"Hỏi <b>gấp bao nhiêu lần</b> → <b>⚖ lập tỉ số</b> từ số khối, hệ số $1{,}2\cdot10^{-15}$ triệt tiêu.")
    x["solution_html"] = thay(x["solution_html"],
        r"$V\propto R^3\propto A$ : $\dfrac{238}{64}\approx3{,}72$ ✓ khớp.",
        r"$V\propto R^3\propto A$ : lập phương tỉ số bán kính $1{,}55^3\approx3{,}72$ ✓ khớp.",
        "15·3 kiểm tra")
    b = x["buoc"][2]
    if DAU not in b["loi_hay_gap"]:
        b["loi_hay_gap"] += r" ⚖ Chia hai bán kính đã làm tròn dễ lệch chữ số cuối — lấy tỉ số từ số khối."


def bo_sung_40(x):
    them_nhan_dang(x, r"<b>$U$ đổi $n$ lần</b> → <b>⚖ lập tỉ số</b> $\left(\dfrac{U'}{U}\right)^2$, giữ nguyên $C$.")
    x["buoc"][2]["chon_buoc_ke"][0]["text"] = r"Lập tỉ số $\dfrac{W'}{W}=\left(\dfrac{U'}{U}\right)^2$, giữ nguyên $C$"


if __name__ == "__main__":
    vá(26, 3, d26_3)
    vá(152, 4, d152_4)
    vá(15, 3, d15_3)
    vá(40, 2, d40_2)
    vá(26, 3, bo_sung_26)
    vá(152, 4, bo_sung_152)
    vá(15, 3, bo_sung_15)
    vá(40, 2, bo_sung_40)
