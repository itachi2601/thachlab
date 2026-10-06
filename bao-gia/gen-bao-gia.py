# -*- coding: utf-8 -*-
"""Sinh bảng báo giá hệ thống ThachLab (đơn vị: triệu VND)."""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

H_FILL = PatternFill("solid", fgColor="1F3864")
H_FONT = Font(bold=True, color="FFFFFF", size=11)
SUB_FILL = PatternFill("solid", fgColor="D9E2F3")
TOT_FILL = PatternFill("solid", fgColor="FFF2CC")
BOLD = Font(bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

wb = Workbook()


def header(ws, row, labels, widths):
    for i, (label, width) in enumerate(zip(labels, widths), start=1):
        c = ws.cell(row=row, column=i, value=label)
        c.fill, c.font, c.border = H_FILL, H_FONT, BOX
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[row].height = 32


def style_row(ws, row, ncols, fill=None, bold=False, num_fmt="#,##0"):
    for i in range(1, ncols + 1):
        c = ws.cell(row=row, column=i)
        c.border = BOX
        if fill:
            c.fill = fill
        if bold:
            c.font = BOLD
        if i >= 2:
            c.alignment = WRAP
        if i >= 3 and isinstance(c.value, (int, float)):
            c.number_format = num_fmt


# ───────────────────────── Sheet 1 — Tóm tắt gói ─────────────────────────
ws = wb.active
ws.title = "1. Tóm tắt gói"
ws["A1"] = "BẢO GIÁ HỆ THỐNG HỌC TẬP TƯƠNG ĐƯƠNG THACHLAB"
ws["A1"].font = Font(bold=True, size=14, color="1F3864")
ws["A2"] = "Đơn vị: triệu VND · Tỷ giá tham chiếu 26.000 đ/USD · Lập ngày 05/10/2026 · Hiệu lực 30 ngày"
ws["A2"].font = Font(italic=True, size=9, color="595959")

header(ws, 4, ["Gói", "Phạm vi bàn giao", "Thời gian", "Đội", "Giá (triệu VND)",
               "≈ USD", "Vận hành (triệu/tháng)"], [10, 52, 14, 16, 18, 14, 18])
packages = [
    ("A", "Bản quyền & triển khai (white-label) bản đang chạy: cấp quyền dùng phần mềm hiện có, đổi thương hiệu, cấu hình cho 1 trường, chuyển dữ liệu, đào tạo giáo viên.",
     "4–6 tuần", "2 người", "250 – 450", "10k – 17k", "4 – 8"),
    ("B", "Xây mới phần mềm tương đương (KHÔNG gồm học liệu): 109 bảng · 261 hàm RPC · 59 trang · 232 component · 4 Edge Function · module CNC/xưởng · module lương trợ giảng · gamification 96 danh hiệu.",
     "7–10 tháng", "5 người", "900 – 1.300", "35k – 50k", "8 – 18"),
    ("C", "Hệ thống ĐẦY ĐỦ như ThachLab hôm nay = Gói B + toàn bộ học liệu: 116 bài lý thuyết tương tác, ~300 bộ đề có lời giải, 20.000 câu ngân hàng đã gắn chủ đề/dạng/độ khó, 557 ảnh tối ưu.",
     "12–18 tháng", "6–8 người + GV cộng tác", "2.000 – 3.900", "77k – 150k", "15 – 40"),
    ("D", "Gói C + hoàn thiện lộ trình tới bản 2.0: AI Tutor Socratic, mô phỏng vật lí nhúng thẳng vào bài, tạo đề theo ma trận YCCĐ × độ khó, xuất Word/PDF, đo lường mùa học.",
     "18–24 tháng", "8 người", "2.400 – 4.500", "92k – 173k", "20 – 55"),
]
r = 5
for pkg in packages:
    for i, v in enumerate(pkg, start=1):
        ws.cell(row=r, column=i, value=v)
    ws.cell(row=r, column=5).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=r, column=6).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=r, column=7).alignment = Alignment(horizontal="center", vertical="center")
    style_row(ws, r, 7, num_fmt="@")
    ws.row_dimensions[r].height = 62
    r += 1

r += 1
ws.cell(row=r, column=1, value="Chi phí ThachLab đã thực chi tới nay (tham chiếu, không phải giá bán)").font = BOLD
r += 1
for line in [
    "• Công: 1 người × 3 tháng (03/7 → 05/10/2026), 689 commit — nếu trả theo giá thị trường: 120 – 200 triệu.",
    "• Tiền mặt: Supabase Pro, AI API, tên miền: ~30 – 60 triệu cho cả 3 tháng (AI nén ngày công 3–5 lần).",
    "• Tổng chi phí thật: ~150 – 260 triệu. Chênh lệch với giá bán (Gói B–C) chính là giá trị sản phẩm, không phải chi phí.",
]:
    ws.cell(row=r, column=1, value=line).alignment = WRAP
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
    ws.row_dimensions[r].height = 16
    r += 1
ws.freeze_panes = "A5"

# ───────────────────────── Sheet 2 — Phần mềm ─────────────────────────
ws2 = wb.create_sheet("2. Phần mềm — chi tiết")
ws2["A1"] = "CHI TIẾT NGÀY CÔNG PHẦN MỀM (không gồm học liệu)"
ws2["A1"].font = Font(bold=True, size=13, color="1F3864")
ws2["A2"] = "Đơn giá 1,4 triệu/người-ngày = mức hỗn hợp junior→senior của đội outsource Việt Nam (2026)."
ws2["A2"].font = Font(italic=True, size=9, color="595959")

header(ws2, 4, ["STT", "Hạng mục", "Ngày công", "Đơn giá", "Thành tiền (triệu)", "Ghi chú"],
       [6, 52, 12, 10, 16, 60])
items = [
    ("Kiến trúc, hạ tầng, đăng nhập & phân quyền RLS, build tĩnh + deploy tự động", 30,
     "Next.js App Router + Supabase; 4 vai trò; xuất tĩnh ra CDN"),
    ("Quản trị tài khoản · lớp · khoá học · ghi danh · import danh sách từ Excel", 25,
     "Phân quyền 3 tầng: quản trị / giảng viên / trợ giảng"),
    ("Học liệu: chương · bài · mục, trình soạn LaTeX/KaTeX, ảnh-PDF-video, nháp & xuất bản, nhập từ Word", 40,
     "Kèm nén ảnh và sinh nội dung tĩnh cho 116 bài"),
    ("Đề thi & 3 dạng câu hỏi, chấm điểm, lưu nháp – phục hồi bài làm, chống gian lận, chấm tự luận tay + rubric", 55,
     "Luồng làm bài trên mobile 375px"),
    ("Ngân hàng câu hỏi: AI gắn chủ đề/dạng/độ khó, vẽ hình bằng AI, chống trùng (similarity), công cụ lọc & duyệt", 25,
     "Đã chạy thật trên 20.372 câu"),
    ("Đo lường & mastery: kết quả từng câu, nắm vững theo yêu cầu cần đạt, ma trận chủ đề, cảnh báo học sinh yếu", 30,
     "Là phần khác biệt cốt lõi: biết HS yếu ở đâu"),
    ("Gamification: mùa rank, sổ cái RP, 96 danh hiệu chuyên môn 3 mức, cổng thử thách, bảng tuần, chuỗi ngày", 40,
     "32 chủ đề × 3 mức + 13 bộ sưu tập"),
    ("Phụ đạo khép kín: phát hiện chủ đề hổng → xếp buổi với trợ giảng → bài tự kiểm tra để thoát", 20, ""),
    ("Trợ giảng & lương: phiên làm việc, quy chế, thưởng video theo lượt xem, chốt tháng, nhật ký kiểm toán", 22,
     "Tự động hoá tính lương trợ giảng"),
    ("Module đào tạo nghề (CTTC/CNC): máy & xưởng, điểm danh chọn máy có ảnh, checklist an toàn, rubric, nộp bản vẽ", 50,
     "25 bảng — đây là phần không LMS nào có sẵn"),
    ("Sinh hoạt chủ nhiệm · cổng phụ huynh · thông báo · tin nhắn · bài đăng · blog/tin tức", 28, ""),
    ("Chuẩn hoá UI/UX theo nghiên cứu tâm lý HS 14–18 và phụ huynh 45–60, mobile 375px, khả năng truy cập", 25,
     "2 bộ quy tắc thiết kế kèm dẫn chứng nghiên cứu"),
    ("Mô phỏng vật lí tương tác (4 tab hero + thí nghiệm ảo: ném xiên, thả hàng, giao thoa, con lắc)", 20, ""),
    ("Kiểm thử, tối ưu tốc độ (Lighthouse 68 → 91), smoke test, tài liệu kỹ thuật & sơ đồ 109 bảng", 30, ""),
    ("Quản lý dự án · khảo sát nghiệp vụ với trường · thiết kế giao diện", 25, ""),
]
r = 5
for i, (name, days, note) in enumerate(items, start=1):
    ws2.cell(row=r, column=1, value=i)
    ws2.cell(row=r, column=2, value=name)
    ws2.cell(row=r, column=3, value=days)
    ws2.cell(row=r, column=4, value=1.4)
    ws2.cell(row=r, column=5, value=f"=C{r}*D{r}")
    ws2.cell(row=r, column=6, value=note)
    style_row(ws2, r, 6, num_fmt="#,##0.0")
    ws2.cell(row=r, column=1).alignment = Alignment(horizontal="center", vertical="top")
    ws2.cell(row=r, column=3).number_format = "#,##0"
    ws2.row_dimensions[r].height = 28
    r += 1
first, last = 5, r - 1
ws2.cell(row=r, column=2, value="CỘNG CHI PHÍ GỐC (người-ngày × đơn giá)")
ws2.cell(row=r, column=3, value=f"=SUM(C{first}:C{last})")
ws2.cell(row=r, column=5, value=f"=SUM(E{first}:E{last})")
style_row(ws2, r, 6, fill=TOT_FILL, bold=True)
cost_row = r
r += 2
ws2.cell(row=r, column=2, value="Giá bán thấp (hệ số 1,35 — lợi nhuận + bảo hành 12 tháng + rủi ro thấp)")
ws2.cell(row=r, column=5, value=f"=E{cost_row}*1.35")
style_row(ws2, r, 6, fill=SUB_FILL, bold=True)
r += 1
ws2.cell(row=r, column=2, value="Giá bán cao (hệ số 1,9 — gồm rủi ro phạm vi, hỗ trợ 12 tháng, chuyển giao)")
ws2.cell(row=r, column=5, value=f"=E{cost_row}*1.9")
style_row(ws2, r, 6, fill=SUB_FILL, bold=True)
r += 2
for note in [
    "Cách đọc: nếu thuê ngoài làm lại đúng khối lượng này, khoảng 900 – 1.300 triệu là hợp lý; dưới 700 triệu thì đội làm sẽ phải cắt bớt module (thường cắt CNC, gamification hoặc tối ưu tốc độ trước).",
    "Nếu dùng AI hỗ trợ như ThachLab đang làm, ngày công thực tế giảm còn ~250–300 người-ngày, nhưng giá bán không giảm tương ứng vì khách trả cho kết quả, không trả cho số giờ gõ phím.",
]:
    ws2.cell(row=r, column=1, value=note).alignment = WRAP
    ws2.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    r += 1
ws2.freeze_panes = "A5"

# ───────────────────────── Sheet 3 — Học liệu ─────────────────────────
ws3 = wb.create_sheet("3. Học liệu — chi tiết")
ws3["A1"] = "CHI TIẾT HỌC LIỆU (chiếm hơn nửa giá trị hệ thống đầy đủ)"
ws3["A1"].font = Font(bold=True, size=13, color="1F3864")
ws3["A2"] = "Số lượng lấy từ cơ sở dữ liệu production ngày 05/10/2026. Đơn vị: triệu VND."
ws3["A2"].font = Font(italic=True, size=9, color="595959")

header(ws3, 4, ["STT", "Hạng mục", "Số lượng", "Đơn giá thấp", "Đơn giá cao",
                "Thành tiền thấp", "Thành tiền cao", "Ghi chú"], [6, 40, 12, 12, 12, 14, 14, 46])
content = [
    ("Bài lý thuyết tương tác (soạn mới + quiz 6 đoạn + 2 vòng kiểm chéo + hình)", 116, 3, 6,
     "Mỗi bài có quiz tương tác, thí nghiệm ảo, chống học vẹt"),
    ("Bộ đề kiểm tra / thi thử có lời giải (20–40 câu, gắn chủ đề + độ khó)", 300, 0.5, 1.5,
     "Trong DB đang có 671 đề, gồm cả kiểm tra nhanh lý thuyết"),
    ("Câu ngân hàng đã gắn chủ đề · dạng · độ khó · hình vẽ", 20000, 0.025, 0.06,
     "25.000 – 60.000 đ/câu cho biên tập + AI + kiểm chéo"),
    ("Ảnh và hình vẽ minh hoạ đã nén, tối ưu (webp, ≤1200px)", 557, 0.09, 0.22,
     "Bắt buộc nén trước khi đăng để giữ tốc độ tải"),
    ("Hiệu đính chuyên môn theo khối 10–12 (giáo viên Vật lí/Hoá bộ môn)", 1, 100, 200,
     "Trả theo gói; nếu trả theo buổi: ~600k–1,2 triệu/buổi"),
]
r = 5
for i, (name, qty, low, high, note) in enumerate(content, start=1):
    ws3.cell(row=r, column=1, value=i)
    ws3.cell(row=r, column=2, value=name)
    ws3.cell(row=r, column=3, value=qty)
    ws3.cell(row=r, column=4, value=low)
    ws3.cell(row=r, column=5, value=high)
    ws3.cell(row=r, column=6, value=f"=C{r}*D{r}")
    ws3.cell(row=r, column=7, value=f"=C{r}*E{r}")
    ws3.cell(row=r, column=8, value=note)
    style_row(ws3, r, 8, num_fmt="#,##0.00")
    for col in (1, 3):
        ws3.cell(row=r, column=col).alignment = Alignment(horizontal="center", vertical="top")
    ws3.cell(row=r, column=3).number_format = "#,##0"
    ws3.row_dimensions[r].height = 30
    r += 1
ws3.cell(row=r, column=2, value="CỘNG HỌC LIỆU")
ws3.cell(row=r, column=6, value=f"=SUM(F5:F{r-1})")
ws3.cell(row=r, column=7, value=f"=SUM(G5:G{r-1})")
style_row(ws3, r, 8, fill=TOT_FILL, bold=True)
content_row = r
r += 2
ws3.cell(row=r, column=2, value="TỔNG GÓI C — phần mềm + học liệu (thấp)")
ws3.cell(row=r, column=6, value=f"='2. Phần mềm — chi tiết'!E{cost_row}*1.35+F{content_row}")
style_row(ws3, r, 8, fill=TOT_FILL, bold=True)
r += 1
ws3.cell(row=r, column=2, value="TỔNG GÓI C — phần mềm + học liệu (cao)")
ws3.cell(row=r, column=6, value=f"='2. Phần mềm — chi tiết'!E{cost_row}*1.9+G{content_row}")
style_row(ws3, r, 8, fill=TOT_FILL, bold=True)
r += 2
ws3.cell(row=r, column=1, value="Lưu ý: học liệu là tài sản dùng lại được cho nhiều trường — trường thứ 2 trở đi chỉ trả phần cấu hình, không trả lại tiền nội dung.").alignment = WRAP
ws3.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
ws3.freeze_panes = "A5"

# ───────────────────────── Sheet 4 — Vận hành ─────────────────────────
ws4 = wb.create_sheet("4. Vận hành hằng năm")
header(ws4, 2, ["Khoản chi", "Thấp (triệu/tháng)", "Cao (triệu/tháng)",
                "Thấp (triệu/năm)", "Cao (triệu/năm)", "Ghi chú"], [46, 16, 16, 16, 16, 56])
opex = [
    ("Hạ tầng Supabase Pro (Singapore) + storage ảnh/PDF", 0.65, 3,
     "0,65 triệu ≈ 25 USD/tháng; tăng khi ảnh và bài làm nhiều"),
    ("API AI (soạn đề, gắn độ khó, vẽ hình, AI Tutor sau này)", 1, 8,
     "ThachLab đang dùng DeepSeek — rẻ hơn Claude/GPT cùng khối lượng"),
    ("Tên miền + CDN/hosting tĩnh (bản build tĩnh rất nhẹ)", 0.1, 0.5, ""),
    ("Bảo trì & nâng cấp (12–18%/năm giá trị phần mềm ~1 tỷ)", 10, 15,
     "Sửa lỗi, cập nhật Next.js/Supabase, sao lưu, giám sát"),
    ("Vận hành nội dung & hỗ trợ người dùng (đăng bài, kiểm đề, trả lời GV/PH)", 5, 15,
     "Có thể dùng chính giáo viên/trợ giảng của trường để giảm chi phí"),
]
r = 3
for name, low, high, note in opex:
    ws4.cell(row=r, column=1, value=name)
    ws4.cell(row=r, column=2, value=low)
    ws4.cell(row=r, column=3, value=high)
    ws4.cell(row=r, column=4, value=f"=B{r}*12")
    ws4.cell(row=r, column=5, value=f"=C{r}*12")
    ws4.cell(row=r, column=6, value=note)
    style_row(ws4, r, 6, num_fmt="#,##0.0")
    ws4.row_dimensions[r].height = 28
    r += 1
ws4.cell(row=r, column=1, value="TỔNG VẬN HÀNH")
ws4.cell(row=r, column=2, value=f"=SUM(B3:B{r-1})")
ws4.cell(row=r, column=3, value=f"=SUM(C3:C{r-1})")
ws4.cell(row=r, column=4, value=f"=SUM(D3:D{r-1})")
ws4.cell(row=r, column=5, value=f"=SUM(E3:E{r-1})")
style_row(ws4, r, 6, fill=TOT_FILL, bold=True)
r += 2
ws4.cell(row=r, column=1, value="Chi phí một lần khi khởi động").font = BOLD
r += 1
header(ws4, r, ["Hạng mục", "Thấp (triệu)", "Cao (triệu)", "", "", "Ghi chú"], [46, 16, 16, 16, 16, 56])
r += 1
for name, low, high, note in [
    ("Khảo sát nghiệp vụ, chuyển dữ liệu học sinh cũ, cấu hình trường", 30, 80, "1 lần"),
    ("Đào tạo giáo viên & trợ giảng (2–3 buổi + tài liệu)", 20, 40, "1 lần"),
    ("Kiểm toán bảo mật RLS & sao lưu dữ liệu (khuyến nghị bắt buộc)", 30, 60,
     "Hệ thống có 109 bảng và 261 hàm — nên rà trước khi mở cho phụ huynh"),
]:
    ws4.cell(row=r, column=1, value=name)
    ws4.cell(row=r, column=2, value=low)
    ws4.cell(row=r, column=3, value=high)
    ws4.cell(row=r, column=6, value=note)
    style_row(ws4, r, 6, num_fmt="#,##0")
    r += 1
r += 1
ws4.cell(row=r, column=1, value="Mô hình thuê bao thay thế (nếu không bán đứt): 15.000 – 25.000 đ/học sinh/tháng, tối thiểu 3–5 triệu/tháng/trường.")
ws4.cell(row=r, column=1).font = BOLD
ws4.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)

# ───────────────────────── Sheet 5 — Tham chiếu thị trường ─────────────────────────
ws5 = wb.create_sheet("5. Tham chiếu thị trường")
header(ws5, 2, ["Phương án", "Chi phí", "Có gì / thiếu gì"], [40, 34, 74])
anchors = [
    ("Thuê LMS nước ngoài (Canvas, MoodleCloud, Google Classroom + add-on)",
     "30.000 – 120.000 đ/HS/năm\n(1.000 HS ≈ 30–120 triệu/năm)",
     "Đủ để giao bài và chấm trắc nghiệm. THIẾU: nắm vững theo yêu cầu cần đạt, gamification 96 danh hiệu, phụ đạo khép kín, module xưởng CNC + điểm danh chọn máy, lương trợ giảng, cổng phụ huynh theo chuẩn tuổi 45–60."),
    ("Thuê đội outsource Việt Nam làm LMS may đo (mức cơ bản)",
     "600 – 1.500 triệu\n6–9 tháng",
     "Có tài khoản, lớp, đề, chấm điểm. Thường KHÔNG có: đo lường theo chủ đề, gamification nhiều mùa, module nghề/xưởng, và không ai tối ưu tốc độ tới Lighthouse 91."),
    ("Hệ thống quản lý đào tạo nghề + ERP xưởng (riêng module CNC)",
     "500 – 2.000 triệu",
     "Điểm danh, checklist an toàn, rubric, quản lý máy. Không có phần học tập THPT và động lực học sinh."),
    ("Mua lại bản quyền ThachLab + triển khai (Gói A)",
     "250 – 450 triệu + 4–8 triệu/tháng",
     "Dùng ngay bản đã chạy thật với 416 tài khoản, 671 đề, 20.372 câu hỏi. Rủi ro thấp nhất, có ngay trong 4–6 tuần."),
    ("Xây mới hoàn toàn tương đương (Gói C)",
     "2.000 – 3.900 triệu\n12–18 tháng",
     "Sở hữu mã nguồn và học liệu. Đây là giá của việc đi lại toàn bộ 3 tháng ròng rã của ThachLab bằng một đội 6–8 người."),
]
r = 3
for name, cost, note in anchors:
    ws5.cell(row=r, column=1, value=name)
    ws5.cell(row=r, column=2, value=cost)
    ws5.cell(row=r, column=3, value=note)
    style_row(ws5, r, 3, num_fmt="@")
    ws5.cell(row=r, column=2).alignment = WRAP
    ws5.row_dimensions[r].height = 62
    r += 1

# ───────────────────────── Sheet 6 — Giả định ─────────────────────────
ws6 = wb.create_sheet("6. Giả định & phạm vi")
header(ws6, 2, ["Nhóm", "Nội dung"], [26, 110])
assumptions = [
    ("Căn cứ định giá", "Số liệu lấy trực tiếp từ mã nguồn và cơ sở dữ liệu production ngày 05/10/2026: 108.298 dòng mã (TS/TSX/SQL/script), 26.030 dòng SQL, 109 bảng, 261 hàm RPC, 59 trang, 232 component, 4 Edge Function, 689 commit trong 3 tháng."),
    ("Dữ liệu thật đang chạy", "416 tài khoản, 126 bài học / 268 mục, 671 đề, 20.372 câu ngân hàng, 17.366 kết quả từng câu, 112 ghi danh khoá học, 92 máy CNC."),
    ("Đơn giá", "1,4 triệu/người-ngày là mức hỗn hợp của đội 5 người (2 senior, 2 mid, 1 junior) tại Việt Nam 2026, đã gồm BHXH, quản lý và thiết bị. Agency tính 1,8–2,5 triệu/ngày thì giá cao hơn 25–40%."),
    ("Tỷ giá", "26.000 đ/USD. Giá đã gồm VAT? — CHƯA. Cộng thêm 8–10% nếu xuất hoá đơn."),
    ("Đã bao gồm", "Mã nguồn bàn giao, tài liệu kỹ thuật, cơ sở dữ liệu, sao lưu, bảo hành sửa lỗi 12 tháng, đào tạo 2–3 buổi, hỗ trợ go-live."),
    ("KHÔNG bao gồm", "Tiền mua học liệu bản quyền của nhà xuất bản; chi phí máy chủ/API hằng tháng; thiết bị vân tay/máy quét điểm danh; nhân sự vận hành nội dung; tích hợp AZOTA hoặc hệ thống tài chính của trường (báo giá riêng 40–120 triệu/tích hợp)."),
    ("Rủi ro đã tính vào giá cao", "Phạm vi thay đổi giữa chừng, dữ liệu cũ bẩn khi chuyển đổi, yêu cầu đặc thù của từng trường, thời gian chờ giáo viên duyệt học liệu."),
    ("Rủi ro CHƯA được xử lý trong hệ thống hiện tại", "Chưa có kiểm thử tự động cho 109 bảng/261 hàm; phần RLS cần được kiểm toán riêng trước khi mở rộng; hiệu quả sư phạm của gamification chưa được đo bằng dữ liệu mùa học — chính ROADMAP của ThachLab cũng ghi đây là việc số 1."),
    ("Điều kiện thanh toán đề xuất", "30% tạm ứng khi ký · 30% khi nghiệm thu module lõi · 30% khi go-live · 10% sau 30 ngày chạy thật. Gói A: 50% / 50%."),
    ("Hiệu lực", "30 ngày kể từ 05/10/2026. Giá thay đổi nếu phạm vi, số trường hoặc số học sinh thay đổi."),
]
r = 3
for group, note in assumptions:
    ws6.cell(row=r, column=1, value=group)
    ws6.cell(row=r, column=2, value=note)
    style_row(ws6, r, 2, num_fmt="@")
    ws6.cell(row=r, column=1).font = BOLD
    ws6.row_dimensions[r].height = 46
    r += 1

wb.save("/Users/MAC/Projects/thachlab/bao-gia/BAO-GIA-He-thong-ThachLab-2026-10.xlsx")
print("saved")
