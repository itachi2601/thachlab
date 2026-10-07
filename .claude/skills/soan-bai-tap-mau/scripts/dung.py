"""Phần DÙNG CHUNG để dựng một bài tập mẫu có cấu trúc (skill soan-bai-tap-mau). Mỗi bài có script riêng
`scripts/data/bai-tap-mau/build-hinh-<lesson_id>.py` (mẫu: build-hinh-57.py) import module này.

  from dung import *     # sau khi sys.path.insert(0, <.claude/skills/soan-bai-tap-mau/scripts>)

Cung cấp: sub (nhãn có chỉ số dưới), smil / ball (mô phỏng SMIL chạy MỘT lần khi bấm), tbl (bảng phân tích đề),
M/P/A + sol (lời giải ngắt bước/dòng), strip, inject (ghi vào JSON).  Hình: hinh.py (fig, arrow, dim, arc, axes…).
"""
import json, math, re, os
from hinh import *

def sub(x, y, base, s, c="currentColor", size=13, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{s}</tspan></text>')

def smil(attr, vals, dur):
    return f'<animate attributeName="{attr}" values="{";".join(f"{v:.1f}" for v in vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'

def ball(pts, hold, sec_per_interval):
    """Mô phỏng hiện tượng: quả cầu chạy dọc quỹ đạo TÍNH THẬT (mẫu cách đều thời gian). hold = số mẫu dừng ở cuối trước khi lặp."""
    n = len(pts); idx = list(range(n)); dur = sec_per_interval * (len(idx) - 1)   # chạy MỘT lần khi bấm nút, dừng ở khung cuối (B4)
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cx", [pts[i][0] for i in idx], dur)}{smil("cy", [pts[i][1] for i in idx], dur)}</circle>')

def tbl(rows):
    body = "".join(f"<tr><td>{c}</td><td>{d_}</td><td>{k_}</td></tr>" for c, d_, k_ in rows)
    return ('<p>Mỗi câu của đề: <strong>cho dữ liệu gì, gọi kiến thức nào?</strong> Hàng có ⚠ là <strong>điều kiện áp dụng</strong> — kiểm tra trước khi dùng công thức.</p>'
            '<div class="table-scroll"><table class="tl-table tl-table--data"><thead><tr><th>Câu trong đề</th><th>Dữ liệu</th><th>Kiến thức liên quan</th></tr></thead><tbody>'
            + body + '</tbody></table></div>')

# ───────────── Lời giải: ngắt dòng, mỗi công thức một dòng (docs/QUY-TAC-THIET-KE C1/C4/H5/B3/N7) ─────────────
def M(x):   return ("m", x)
def P(x):   return ("p", x)
def A(x):   return ("a", x)
def sol(recall, steps, finals, note):
    out = '<div class="bt-sol">'
    out += '<div class="tl-box"><p class="tl-label">Kiến thức cần gọi lại</p><ol>' + "".join(f"<li>{r}</li>" for r in recall) + "</ol></div>"
    for n, (title, els) in enumerate(steps, 1):
        out += f'<div class="bt-step"><p class="bt-step-title"><span class="bt-step-n">{n}</span><span>{title}</span></p>'
        for kind, x in els:
            if kind == "p": out += f"<p>{x}</p>"
            elif kind == "m": out += f"$${x}$$"
            else: out += f'<div class="bt-ans">$${x}$$</div>' if not x.startswith("T:") else f'<div class="bt-ans"><p>{x[2:]}</p></div>'
        out += "</div>"
    out += '<div class="bt-final"><p><strong>Đáp số</strong></p>' + "".join(f"<p>{f}</p>" for f in finals) + "</div>"
    out += f'<p class="bt-note">{note}</p><p class="bt-note">3 ngày sau che lời giải và giải lại từ đầu.</p></div>'
    return out

def strip(html):
    return re.sub(r'<figure class="fig"[^>]*data-bt="[^"]*".*?</figure>', "", html, flags=re.S)


def inject(json_path, build, analysis, sols):
    """build[i](k): k=0 hình mô phỏng dưới đề; k=2 hình dữ kiện tĩnh cho phần phân tích. Idempotent (xoá figure[data-bt] cũ)."""
    d = json.load(open(json_path))
    for i, fn in enumerate(build):
        q = d["dang_bai"][i]
        q["problem_html"] = strip(q["problem_html"]) + fn(0)     # mô phỏng nằm DƯỚI đề
        q["analysis_html"] = fn(2) + tbl(analysis[i])             # hình dữ kiện + bảng Câu trong đề | Dữ liệu | Kiến thức
        q.pop("hints_html", None)
        q["solution_html"] = sols[i]
    json.dump(d, open(json_path, "w"), ensure_ascii=False, indent=1)
    print("ok", len(d["dang_bai"]))


def tu_luan_tu(old, order, muc, label="Bài tập tự luận (xếp từ dễ đến khó)"):
    """Gom các ví dụ CŨ chưa biên tập thành một mục "Bài tập tự luận": `old` = questions cũ (scripts/data/bai-tap-mau/old/<id>.json),
    `order` = chỉ số trong `old` theo thứ tự dễ→khó, `muc` = {chỉ số: "Dễ"|"Trung bình"|"Khó"|"Nâng cao"}.
    Đề hiện sẵn, lời giải gốc thu vào <details>. Ví dụ đã biên tập thành dạng mới thì KHÔNG đưa vào `order`."""
    parts = []
    for k, i in enumerate(order, 1):
        h = old[i]["body_html"]
        h = re.sub(r"Ví dụ \d+:?", f"Bài {k}.", h, count=1)
        h = h.replace("Hướng dẫn giải", "", 1)
        if "</table></div>" in h:
            de, gi = h.split("</table></div>", 1)
            parts.append(f'<h4>Bài {k} · {muc.get(i, "")}</h4>{de}</table></div><details><summary>Hướng dẫn giải</summary>{gi}</details>')
        else:
            parts.append(f'<h4>Bài {k} · {muc.get(i, "")}</h4>{h}')
    return dict(label=label, body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))

def write(json_path, lesson_id, lesson_title, dang, build, analysis, sols, tu_luan=None):
    """Ghi file JSON hoàn chỉnh. `dang` = [dict(label, topic, form="bai_tap", problem_html=<đề chữ>)] xếp DỄ → KHÓ.
    review.checked=False cho tới khi kiểm chéo (kiem-code) xong."""
    d = {"lesson_id": lesson_id, "lesson_title": lesson_title, "generated_at": "2026-10-07",
         "review": {"checked": False, "notes": "chờ kiểm chéo"},
         "dang_bai": [dict(form="bai_tap", **x) for x in dang]}
    if tu_luan: d["tu_luan"] = tu_luan
    for i, x in enumerate(d["dang_bai"]):
        x["solution_html"] = ""
    json.dump(d, open(json_path, "w"), ensure_ascii=False, indent=1)
    inject(json_path, build, analysis, sols)
