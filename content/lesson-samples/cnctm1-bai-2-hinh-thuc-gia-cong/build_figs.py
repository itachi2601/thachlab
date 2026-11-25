#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 2, thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
"""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FONT = 'font-family="system-ui, sans-serif" font-size="13"'


def fig(svg, cap):
    return f'<figure class="fig" data-tl="1">{svg}<figcaption>{cap}</figcaption></figure>'


# Hình 1: sơ đồ nhiệt luyện nhiệt độ – thời gian, ba cách làm nguội
def fig1():
    o = []
    o.append(f'<svg viewBox="0 0 420 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sơ đồ nhiệt luyện" {FONT}>')
    # trục
    o.append('<line x1="40" y1="210" x2="405" y2="210" stroke="currentColor" stroke-width="1.5"/>')
    o.append('<line x1="40" y1="210" x2="40" y2="70" stroke="currentColor" stroke-width="1.5"/>')
    o.append('<path d="M34 80 L40 70 L46 80" fill="none" stroke="currentColor" stroke-width="1.5"/>')
    o.append('<path d="M395 204 L405 210 L395 216" fill="none" stroke="currentColor" stroke-width="1.5"/>')
    o.append('<text x="48" y="80" fill="currentColor" font-size="12">nhiệt độ</text>')
    o.append('<text x="330" y="232" fill="currentColor" font-size="12">thời gian</text>')
    # nung + giữ
    o.append('<path d="M40 205 L130 100 L210 100" fill="none" stroke="currentColor" stroke-width="2.5"/>')
    o.append('<text x="70" y="140" fill="currentColor" font-weight="700">I</text>')
    o.append('<text x="164" y="92" fill="currentColor" font-weight="700">II</text>')
    o.append('<text x="56" y="160" fill="currentColor" font-size="12">nung</text>')
    o.append('<text x="150" y="122" fill="currentColor" font-size="12">giữ nhiệt</text>')
    # ba đường nguội (giai đoạn III)
    o.append('<path d="M210 100 C215 160 222 200 238 207" fill="none" stroke="#dc2626" stroke-width="2.5"/>')
    o.append('<path d="M210 100 C240 150 270 195 320 205" fill="none" stroke="#059669" stroke-width="2.5"/>')
    o.append('<path d="M210 100 C280 120 350 165 400 192" fill="none" stroke="#0284c7" stroke-width="2.5"/>')
    o.append('<text x="222" y="150" fill="currentColor" font-weight="700">III</text>')
    # chú giải, mỗi ý một dòng
    rows = [("#dc2626", "nguội nhanh (nước, dầu) → TÔI"),
            ("#059669", "nguội trong không khí → THƯỜNG HOÁ"),
            ("#0284c7", "nguội chậm cùng lò → Ủ")]
    for i, (c, s) in enumerate(rows):
        y = 18 + i * 20
        o.append(f'<line x1="150" y1="{y - 4}" x2="172" y2="{y - 4}" stroke="{c}" stroke-width="3"/>')
        o.append(f'<text x="178" y="{y}" fill="currentColor" font-size="12">{s}</text>')
    o.append('</svg>')
    return fig("".join(o), "Hình 1. Ba giai đoạn nhiệt luyện. Cùng nung và giữ nhiệt, cách làm nguội quyết định thép mềm hay cứng.")


# Hình 2: thớ kim loại khi cắt ren (tiện) và khi cán ren
def teeth(x0, dy=0, amp=30):
    return " ".join(f"{x0 + i * 20},{(80 if i % 2 == 0 else 80 - amp) + dy}" for i in range(9))


def fig2():
    o = []
    o.append(f'<svg viewBox="0 0 420 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Thớ kim loại khi tiện ren và khi cán ren" {FONT}>')
    o.append('<defs>')
    for side, x0 in (("l", 15), ("r", 225)):
        o.append(f'<clipPath id="f2-c{side}"><polygon points="{x0},140 {teeth(x0)} {x0 + 160},140"/></clipPath>')
    o.append('</defs>')
    # trái: thớ thẳng bị cắt đứt
    o.append('<g clip-path="url(#f2-cl)" stroke="#0284c7" stroke-width="1.3">')
    for y in range(56, 140, 8):
        o.append(f'<line x1="15" y1="{y}" x2="175" y2="{y}"/>')
    o.append('</g>')
    # phải: thớ uốn theo biên dạng răng, càng sâu càng phẳng
    o.append('<g clip-path="url(#f2-cr)" fill="none" stroke="#059669" stroke-width="1.3">')
    for k, dy in enumerate(range(4, 64, 8)):
        amp = max(30 - k * 4, 0)
        o.append(f'<polyline points="{teeth(225, dy, amp)}"/>')
    o.append('</g>')
    for side, x0 in (("l", 15), ("r", 225)):
        o.append(f'<polygon points="{x0},140 {teeth(x0)} {x0 + 160},140" fill="none" stroke="currentColor" stroke-width="2"/>')
    o.append('<text x="15" y="30" fill="currentColor" font-weight="700">Tiện ren (có phoi)</text>')
    o.append('<text x="225" y="30" fill="currentColor" font-weight="700">Cán ren (không phoi)</text>')
    o.append('<text x="15" y="162" fill="currentColor" font-size="12">Thớ thẳng bị cắt đứt</text>')
    o.append('<text x="15" y="180" fill="currentColor" font-size="12">ở sườn răng.</text>')
    o.append('<text x="225" y="162" fill="currentColor" font-size="12">Thớ uốn theo răng,</text>')
    o.append('<text x="225" y="180" fill="currentColor" font-size="12">không bị cắt, bề mặt biến cứng.</text>')
    o.append('</svg>')
    return fig("".join(o), "Hình 2. Cùng một biên dạng ren, cách làm khác nhau cho thớ kim loại khác nhau (hình minh hoạ, không theo tỉ lệ).")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
