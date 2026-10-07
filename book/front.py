#!/usr/bin/env python3
"""Phần đầu sách (8 trang) + trang cuối: bìa, lời ngỏ, ký hiệu, cách đọc hình, mục lục, bản đồ chương,
mở chương, trang nháp; và các trang đệm.
   python3 front.py <pages.json>   → src/front.html, src/back.html
pages.json: {"49": {"start": 9, "n": 36}, ...}  (từ make.py)
"""
import json, sys
from pathlib import Path
import build, bw
from build import CHAPTER, head_html, load_lesson, SRC

A = Path(__file__).resolve().parent / 'assets'


def strobe_inline(name):
    return (A / name).read_text()


def toc_rows(pages):
    rows = []
    for lid in CHAPTER['lessons']:
        L = load_lesson(lid)
        st = pages.get(str(lid), {}).get('start', '')
        practical = 'Thực hành' in L['name']
        rows.append(f'<li class="{"prac" if practical else ""}"><span class="t-n">{L["num"]:02d}</span>'
                    f'<span class="t-t">{L["name"]}</span><span class="t-d"></span><span class="t-p">{st}</span></li>')
    return ''.join(rows)


def metro(pages):
    """Bản đồ chương kiểu sơ đồ tàu điện: 9 ga, ga thực hành là hình vuông."""
    names = {49: 'Độ dịch chuyển\n& quãng đường', 50: 'Tốc độ\n& vận tốc', 51: 'Thực hành\nđo tốc độ',
             52: 'Đồ thị\nđộ dịch chuyển\n– thời gian', 53: 'Chuyển động\nbiến đổi\n& gia tốc',
             54: 'Thẳng biến\nđổi đều', 55: 'Rơi\ntự do', 56: 'Thực hành\nđo g', 57: 'Chuyển động\nném'}
    W, H = 174, 150
    xs = [18, 60, 102, 144]
    pts = [(xs[0], 14), (xs[1], 14), (xs[2], 14), (xs[3], 14),
           (xs[3], 78), (xs[2], 78), (xs[1], 78), (xs[0], 78),
           (xs[0], 132)]
    path = f'M{xs[0]} 14 L166 14 L166 78 L{xs[0]} 78 L{xs[0]} 132'
    s = [f'<svg viewBox="0 0 {W} {H}" class="metro">',
         f'<path d="{path}" fill="none" stroke="#0d0d0d" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>',
         f'<path d="{path}" fill="none" stroke="#fff" stroke-width="0.7" stroke-dasharray="2 3" stroke-linejoin="round"/>']
    for idx, ((x, y), lid) in enumerate(zip(pts, CHAPTER['lessons'])):
        L = load_lesson(lid); prac = 'Thực hành' in L['name']
        if prac:
            s.append(f'<rect x="{x-4.6}" y="{y-4.6}" width="9.2" height="9.2" fill="#fff" stroke="#0d0d0d" stroke-width="1.5"/>')
        else:
            s.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#0d0d0d"/>')
        s.append(f'<text x="{x}" y="{y+1.9}" text-anchor="middle" font-size="5.2" font-weight="800" fill="{"#0d0d0d" if prac else "#fff"}" font-family="Bricolage Grotesque">{L["num"]}</text>')
        lines = names[lid].split('\n')
        st = pages.get(str(lid), {}).get('start', '')
        rows = [(ln, 700 if k == 0 else 500, '#0d0d0d', 4.2) for k, ln in enumerate(lines)] + [(f'tr. {st}', 700, '#6a6a6a', 3.7)]
        if idx == 8:                      # ga cuối: nhãn bên phải
            anchor, tx, ty0 = 'start', x + 9, y - 2
        elif y < 40:                      # hàng 1: nhãn dưới ga
            anchor, tx, ty0 = 'middle', x, y + 11
        else:                             # hàng 2: nhãn trên ga
            anchor, tx, ty0 = 'middle', x, y - 9 - (len(rows) - 1) * 5
        for k, (txt, w, col, fs) in enumerate(rows):
            s.append(f'<text x="{tx}" y="{ty0 + k*5}" text-anchor="{anchor}" font-size="{fs}" font-weight="{w}" fill="{col}">{txt}</text>')
    s.append('<text x="60" y="134" font-size="4.2" font-weight="700" fill="#0d0d0d">■ ga thực hành   ● ga lý thuyết + bài tập</text>')
    s.append('</svg>')
    return ''.join(s)


def line_legend():
    def ln(dash, w, col='#0d0d0d', arrow=True):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        mk = ' marker-end="url(#lg)"' if arrow else ''
        return f'<svg viewBox="0 0 40 8" class="lg"><line x1="1" y1="4" x2="36" y2="4" stroke="{col}" stroke-width="{w}"{d}{mk}/></svg>'
    defs = '<svg width="0" height="0"><defs><marker id="lg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#0d0d0d"/></marker></defs></svg>'
    rows = [(ln(None, 1.8), 'Nét đậm', 'vectơ chính: vận tốc, lực…'),
            (ln('7 4', 1.4), 'Nét đứt', 'đường đi, quỹ đạo của vật'),
            (ln('9 3 2 3', 1.4), 'Nét chấm gạch', 'độ dịch chuyển hay đại lượng thứ hai'),
            (ln(None, 1.4, '#6b6b6b'), 'Nét xám', 'đại lượng thứ ba'),
            ('<svg viewBox="0 0 40 8" class="lg"><rect x="2" y="0.5" width="34" height="7" fill="url(#bwHatch)" stroke="#0d0d0d" stroke-width=".5"/></svg>', 'Gạch chéo', 'vùng được tô, thứ hai'),
            ('<svg viewBox="0 0 40 8" class="lg"><rect x="2" y="0.5" width="34" height="7" fill="rgba(0,0,0,.14)" stroke="#0d0d0d" stroke-width=".5"/></svg>', 'Nền xám', 'vùng được tô, thứ nhất')]
    hatch = f'<svg width="0" height="0"><defs>{bw.HATCH_DEFS}</defs></svg>'
    out = ''.join(f'<div class="lg-r"><div class="lg-s">{a}</div><div class="lg-n">{b}</div><div class="lg-d">{c}</div></div>' for a, b, c in rows)
    return defs + hatch + out


def build_front(pages):
    total = sum(p['n'] for p in pages.values()) if pages else 0
    html = head_html('Vật lí 10 — Chương 2 · Động học (bản thử)', 1)
    mp = metro(pages)
    # 1 — bìa
    html += f'''<section class="cover">
  <div class="cv-art">{strobe_inline('strobe-big-ink.svg')}</div>
  <div class="cv-top"><span>VẬT LÍ 10</span><span>SỔ TAY TỰ HỌC</span></div>
  <div class="cv-num">02</div>
  <h1 class="cv-title">ĐỘNG<br>HỌC</h1>
  <p class="cv-sub">Mô tả chuyển động của mọi vật — từ chiếc xe buýt tới quả bóng bay trên sân.</p>
  <div class="cv-foot"><div class="cv-rules"><span>VIẾT TAY</span><span>TỰ GIẢI</span><span>ĐỐI CHIẾU</span></div>
  <div class="cv-brand"><b>THẠCH LAB</b><span>thachlab.id.vn</span></div></div>
  <div class="cv-tag">BẢN THỬ · CHƯƠNG 2</div>
</section>'''
    # 2 — cách học + ký hiệu
    html += '''<section class="plain p-learn">
  <h2 class="pg-h"><span class="pg-k">CÁCH DÙNG SÁCH</span>Học để nhớ lâu, không phải để thuộc nhanh</h2>
  <ol class="steps4">
    <li><span class="s4-n">1</span><div><h4>Đoán trước khi đọc</h4><p>Gặp khung <b>DỰ ĐOÁN</b>, em chọn theo cảm giác rồi ghi vì sao. Đoán sai không sao — đó là lúc não chú ý nhất.</p></div></li>
    <li><span class="s4-n">2</span><div><h4>Điền chỗ trống khi nghe giảng</h4><p>Công thức quan trọng và bảng phân tích đề để trống: em tự điền bằng bút chì, ghi bằng lời của mình.</p></div></li>
    <li><span class="s4-n">3</span><div><h4>Làm xong rồi mới quét đáp án</h4><p>Đáp án, gợi ý và lời giải bài tập mẫu nằm trên web: quét mã QR cuối bài. Luyện tập và giải đề cũng làm trên web.</p></div></li>
    <li><span class="s4-n">4</span><div><h4>Ba ngày sau, làm lại</h4><p>Che các ô đã điền và nhớ lại vào <b>ngày thứ ba</b>. Nhớ lại khó một chút mới là lúc học được nhiều nhất.</p></div></li>
  </ol>
  <div class="sym-grid">
    <div class="sym"><div class="sym-demo"><div class="key sm"><span class="key-l">GHI NHỚ</span><p>Công thức · ý chính</p></div></div><p><b>GHI NHỚ</b> — điều cần thuộc; công thức để trống cho em điền.</p></div>
    <div class="sym"><div class="sym-demo"><div style="padding:3mm">Vậy <span class="fb" style="min-width:26mm"><i class="fbn">1</i></span> là công thức cần nhớ.</div></div><p><b>Ô điền</b> — chấm trống có số nhỏ; đáp án cùng số trên web.</p></div>
    <div class="sym"><div class="sym-demo"><div class="quiz sm"><div class="q-h"><span class="q-tag">CÂU 1</span></div><p>Khung nét đứt, 4 đáp án</p></div></div><p><b>Câu hỏi</b> — khoanh một đáp án, ghi “em chọn”.</p></div>
    <div class="sym"><div class="sym-demo"><div class="exp sm"><div class="exp-h"><span>THÍ NGHIỆM</span></div><div class="step"><div class="st-l">LÀM</div><div class="st-b">…</div></div></div></div><p><b>Thí nghiệm</b> — Làm · Quan sát · Rút ra, có chỗ ghi số liệu.</p></div>
  </div>
  <div class="note-box"><b>Dùng cùng website.</b> Trên lớp, thầy cô chiếu mô phỏng; em quét mã QR ở đầu bài hoặc cạnh hình có nhãn “mô phỏng trên web” để tự chạy lại ở nhà. Một bài đọc lý thuyết khoảng 15–20 phút.</div>
</section>'''
    # 3 — cách đọc hình + mục lục
    html += f'''<section class="plain p-toc">
  <h2 class="pg-h"><span class="pg-k">CÁCH ĐỌC HÌNH</span>Sách in đen–trắng: mỗi màu là một kiểu nét</h2>
  <div class="lg-box">{line_legend()}</div>
  <h2 class="pg-h pg-h2"><span class="pg-k">MỤC LỤC</span>Chương 2 · Động học</h2>
  <ol class="toc">{toc_rows(pages)}</ol>
</section>'''
    # 4 — bản đồ chương
    html += f'''<section class="plain p-map">
  <h2 class="pg-h"><span class="pg-k">BẢN ĐỒ CHƯƠNG</span>Chín ga trên tuyến “Động học”</h2>
  <p class="lead">Bài này dựng trên bài trước. Đi lần lượt từ ga 4 đến ga 12 — nếu lạc, quay lại ga liền trước.</p>
  <div class="metro-wrap">{mp}</div>
  <div class="map-list">
    <div><b>Bài 4–5</b> Mô tả vị trí và cách đo nhanh chậm</div>
    <div><b>Bài 6–7</b> Tự đo, tự vẽ đồ thị chuyển động</div>
    <div><b>Bài 8–10</b> Khi vận tốc thay đổi: gia tốc</div>
    <div><b>Bài 11–12</b> Đo g, rồi ghép hai chuyển động: ném</div>
  </div>
  <div class="dl-lab">Mục tiêu của em cho chương này (viết ngắn, cụ thể):</div>''' + build.dl(3) + '</section>'
    html += '</body></html>'
    out = SRC / 'front.html'; out.write_text(html); return out


def filler(label='TRANG GHI CHÚ TỰ DO'):
    return (f'<section class="free"><div class="free-h"><span>{label}</span><span class="free-t">vẽ sơ đồ tư duy của bài · ghi điều em còn băn khoăn</span></div><div class="dotgrid full"></div></section>')


def build_back(pages, takeaways):
    html = head_html('Tổng kết chương 2', 1)
    # tổng kết chương
    rows = ''.join(f'<div class="sum-b"><div class="sum-n">{n:02d}</div><div class="sum-c"><h4>{t}</h4>{h}</div></div>' for n, t, h in takeaways)
    html += f'''<section class="plain p-sum">
  <h2 class="pg-h"><span class="pg-k">TỔNG KẾT CHƯƠNG</span>Mang về sau chương “Động học”</h2>
  <div class="sum-grid">{rows}</div>
</section>'''
    html += '''<section class="plain p-self">
  <h2 class="pg-h"><span class="pg-k">TỰ ĐÁNH GIÁ</span>Em làm được gì sau chương này?</h2>
  <p class="lead">Tô đậm ô thích hợp. Chỗ nào chưa chắc, ghi số bài ở bên phải để quay lại ôn.</p>
  <table class="tbl selfeval"><thead><tr><th>Em có thể…</th><th>Chắc</th><th>Tạm</th><th>Chưa</th><th>Ôn ở bài</th></tr></thead><tbody>
  <tr><td>Phân biệt độ dịch chuyển và quãng đường, tính được cả hai</td><td><span class="cb"></span></td><td><span class="cb"></span></td><td><span class="cb"></span></td><td>4</td></tr>
  <tr><td>Phân biệt tốc độ và vận tốc, tính tốc độ trung bình</td><td><span class="cb"></span></td><td><span class="cb"></span></td><td><span class="cb"></span></td><td>4, 5</td></tr>
  <tr><td>Đo tốc độ bằng cổng quang và tính sai số</td><td><span class="cb"></span></td><td><span class="cb"></span></td><td><span class="cb"></span></td><td>6</td></tr>
  <tr><td>Đọc và vẽ đồ thị độ dịch chuyển – thời gian; tính vận tốc từ độ dốc</td><td><span class="cb"></span></td><td><span class="cb"></span></td><td><span class="cb"></span></td><td>7</td></tr>
  <tr><td>Tính gia tốc; nhận ra nhanh dần, chậm dần</td><td><span class="cb"></span></td><td><span class="cb"></span></td><td><span class="cb"></span></td><td>8</td></tr>
  <tr><td>Dùng công thức chuyển động thẳng biến đổi đều và đồ thị v–t</td><td><span class="cb"></span></td><td><span class="cb"></span></td><td><span class="cb"></span></td><td>9</td></tr>
  <tr><td>Giải bài rơi tự do (thời gian rơi, vận tốc chạm đất)</td><td><span class="cb"></span></td><td><span class="cb"></span></td><td><span class="cb"></span></td><td>10, 11</td></tr>
  <tr><td>Phân tích chuyển động ném thành hai chuyển động độc lập</td><td><span class="cb"></span></td><td><span class="cb"></span></td><td><span class="cb"></span></td><td>12</td></tr>
  </tbody></table>
  <div class="dl-lab">Điều em còn băn khoăn sau chương này:</div>''' + build.dl(5) + '</section>'
    html += '</body></html>'
    out = SRC / 'back.html'; out.write_text(html); return out


if __name__ == '__main__':
    pages = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
    print(build_front(pages))
