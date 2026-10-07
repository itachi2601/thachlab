"""Đổi nội dung web (màu) sang đen–trắng cho sách in.

Quy ước nét (dùng thống nhất cả cuốn, có bảng chú giải ở trang "Cách dùng sách"):
  đỏ     → nét đen ĐẬM liền        (vectơ chính: vận tốc, lực…)
  cam    → nét ĐỨT                 (đường đi, quỹ đạo)
  xanh lá→ nét CHẤM GẠCH           (độ dịch chuyển, đại lượng thứ hai)
  xanh dương → nét XÁM liền        (đại lượng thứ ba)
Vùng tô: xanh dương → nền xám nhạt, xanh lá → gạch chéo, cam → chấm.
"""
import re

# ---------- 1. Màu trong SVG ----------
HEX = {
    '#f87171': 'red', '#ef4444': 'red', '#dc2626': 'red',
    '#fb923c': 'orange', '#f97316': 'orange',
    '#34d399': 'green', '#4ade80': 'green', '#10b981': 'green',
    '#38bdf8': 'blue', '#22d3ee': 'blue', '#3b82f6': 'blue',
    '#a78bfa': 'purple', '#8b5cf6': 'purple',
    '#facc15': 'yellow', '#fbbf24': 'yellow',
}
STROKE = {   # (màu xám, dasharray, nhân độ dày)
    'red': ('#000', None, 1.25),
    'orange': ('#1a1a1a', '7 4', 1.0),
    'green': ('#1a1a1a', '9 3 2 3', 1.0),
    'blue': ('#6b6b6b', None, 1.0),
    'purple': ('#444', '3 3', 1.0),
    'yellow': ('#8a8a8a', None, 1.0),
}
FILL = {     # màu đặc (chấm, đầu mũi tên, chữ)
    'red': '#000', 'orange': '#1a1a1a', 'green': '#2b2b2b', 'blue': '#6b6b6b',
    'purple': '#444', 'yellow': '#8a8a8a',
}
HATCH_DEFS = (
    '<pattern id="bwHatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
    '<line x1="0" y1="0" x2="0" y2="5" stroke="#444" stroke-width="1.3"/></pattern>'
    '<pattern id="bwDots" width="5" height="5" patternUnits="userSpaceOnUse">'
    '<circle cx="2.5" cy="2.5" r="0.9" fill="#444"/></pattern>'
)


def _hue_of_rgb(r, g, b):
    r_, g_, b_ = r / 255, g / 255, b / 255
    # phân loại thô theo kênh trội
    if r > 200 and g < 150 and b < 150: return 'red'
    if r > 200 and 100 < g < 190 and b < 110: return 'orange'
    if g > 180 and b < 190 and r < 120: return 'green'
    if b > 200 and r < 100: return 'blue'
    if b > 200 and r > 120: return 'purple'
    if r > 200 and g > 180 and b < 100: return 'yellow'
    return None


def _rgba_fill(m):
    r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
    a = float(m.group(4)) if m.group(4) else 1.0
    hue = _hue_of_rgb(r, g, b)
    if hue == 'green':
        return 'url(#bwHatch)'
    if hue == 'orange':
        return 'url(#bwDots)'
    if hue is None:   # xám sẵn
        return f'rgba(0,0,0,{a*0.5:.2f})'
    return f'rgba(0,0,0,{min(a*0.55, 0.45):.2f})'


def _hex_name(v):
    v = v.lower()
    if len(v) == 4:
        v = '#' + ''.join(c * 2 for c in v[1:])
    return HEX.get(v)


def _tag_fix(m):
    tag = m.group(0)
    name = re.match(r'<(\w+)', tag).group(1)
    # stroke
    sm = re.search(r'\bstroke="([^"]+)"', tag)
    if sm:
        hue = _hex_name(sm.group(1))
        if hue is None and sm.group(1).startswith('rgba'):
            rm = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', sm.group(1))
            if rm:
                hue = _hue_of_rgb(*map(int, rm.groups()))
        if hue:
            col, dash, mult = STROKE[hue]
            tag = tag.replace(sm.group(0), f'stroke="{col}"')
            if dash and name in ('line', 'path', 'polyline', 'polygon', 'rect') and 'stroke-dasharray' not in tag:
                tag = tag.replace(f'<{name}', f'<{name} stroke-dasharray="{dash}"', 1)
            wm = re.search(r'stroke-width="([\d.]+)"', tag)
            if wm and mult != 1.0:
                tag = tag.replace(wm.group(0), f'stroke-width="{float(wm.group(1))*mult:.2f}"')
    # fill
    fm = re.search(r'\bfill="([^"]+)"', tag)
    if fm:
        v = fm.group(1)
        hue = _hex_name(v) if v.startswith('#') else None
        if hue:
            tag = tag.replace(fm.group(0), f'fill="{FILL[hue]}"')
        elif v.startswith('rgba') or v.startswith('rgb('):
            rm = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?', v)
            if rm:
                tag = tag.replace(fm.group(0), f'fill="{_rgba_fill(rm)}"')
    return tag


SUBTXT = str.maketrans('₀₁₂₃₄₅₆₇₈₉ₙₓ₋', '0123456789nx−')


def gray_svg(svg: str) -> str:
    svg = svg.translate(SUBTXT).replace('①', '(1)').replace('②', '(2)').replace('③', '(3)').replace('④', '(4)')
    svg = re.sub(r'(<svg\b[^>]*?viewBox="0 0 ([\d.]+) [\d.]+"[^>]*?)>', lambda m: m.group(0) if 'style=' in m.group(1) else m.group(1) + f' style="width:{min(float(m.group(2))*0.228,170):.0f}mm;max-width:100%">', svg, count=1)
    svg = re.sub(r'<(?:line|path|polyline|polygon|rect|circle|ellipse|text|tspan)\b[^>]*>', _tag_fix, svg)
    # màu nằm trong style="..." (hiếm)
    svg = re.sub(r'style="[^"]*"', lambda m: re.sub(r'#[0-9a-fA-F]{6}', lambda c: FILL.get(_hex_name(c.group(0)) or '', c.group(0)), m.group(0)), svg)
    # chèn pattern vào <defs> (hoặc tạo mới)
    if '<defs>' in svg:
        svg = svg.replace('<defs>', '<defs>' + HATCH_DEFS, 1)
    else:
        svg = re.sub(r'(<svg\b[^>]*>)', r'\1<defs>' + HATCH_DEFS + '</defs>', svg, count=1)
    return svg


# ---------- 2. Chữ nhắc màu ----------
# Mỗi luật: (regex, thay thế). Thứ tự quan trọng. Chỉ đổi khi đứng sau danh từ chỉ nét/vật vẽ,
# để không đụng vào "đèn đỏ", "đèn xanh".
_N_ARROW = r'(mũi tên|vectơ|véc tơ|vecto)'
_N_LINE = r'(nét|vạch|đường|đoạn|cung|tia|dây)'
_N_DOT = r'(chấm|điểm|vòng|hạt|viên bi|quả bóng|xe|vật)'
_N_AREA = r'(hình|tam giác|chữ nhật|dải|vùng|miền|phần|diện tích|ô)'
TEXT_RULES = [
    (rf'\b{_N_ARROW} nét đứt xanh lá', r'\1 nét chấm gạch'),
    (rf'\b{_N_ARROW} (?:xanh lá|xanh lục)', r'\1 nét chấm gạch'),
    (rf'\b{_N_ARROW} (?:xanh dương|xanh)', r'\1 nét xám'),
    (rf'\b{_N_ARROW} đỏ', r'\1 nét đậm'),
    (rf'\b{_N_ARROW} cam', r'\1 nét đứt'),
    (r'\b(nét|đường) cam\b', r'\1 nét đứt'),
    (r'\b(nét|đường) đỏ\b', r'\1 nét đậm'),
    (r'\b(nét|đường) xanh lá\b', r'\1 nét chấm gạch'),
    (r'\b(nét|đường) xanh dương\b', r'\1 nét xám'),
    (r'\bnét nét\b', 'nét'),
    (rf'\b{_N_LINE} cam\b', r'\1 nét đứt'),
    (rf'\b{_N_LINE} đỏ\b', r'\1 nét đậm'),
    (rf'\b{_N_LINE} xanh lá\b', r'\1 nét chấm gạch'),
    (rf'\b{_N_LINE} xanh dương\b', r'\1 nét xám'),
    (rf'\b{_N_LINE} xanh\b(?! dần)', r'\1 nét xám'),
    (r'\b(chấm|điểm) (?:cam|xanh|đỏ)\b', r'\1 đen'),
    (r'\bvạch xanh\b', 'vạch đen'),
    (rf'\b{_N_AREA} xanh dương\b', r'\1 xám nhạt'),
    (rf'\b{_N_AREA} xanh lá\b', r'\1 gạch chéo'),
    (rf'\b{_N_AREA} (?:xanh|cam)\b', r'\1 chấm bi'),
    (r'\btô màu\b', 'tô xám'),
    (r'\btô xanh\b', 'tô xám'),
    (r'\btô cam\b', 'tô chấm bi'),
    (r'\bcam\b(?= \$)', 'nét đứt'),
    (r'\(đỏ\)', '(nét đậm)'),
    (r'\(cam\)', '(nét đứt)'),
    (r'\(xanh lá\)', '(nét chấm gạch)'),
    (r'\(xanh dương\)', '(nét xám)'),
    (r'\(xanh\)', '(nét xám)'),
    (r'\bxanh dương\b(?! dần)', 'nét xám'),
    (r'\bxanh lá\b', 'nét chấm gạch'),
    (r'\b(trên thanh|dải|thanh) (?:xanh)\b', r'\1 xám'),
    (r'\bdải xanh\b', 'dải xám'),
    (r'\bvạch cam\b', 'vạch đứt'),
    (r'\bnét đỏ đứt\b', 'nét đứt đậm'),
    (r'\bcam\b(?= \()', 'nét đứt'),
    (r'\bnét đứt \(nét đứt\)', 'nét đứt'),
]


def rewrite_color_words(html: str) -> str:
    for pat, rep in TEXT_RULES:
        html = re.sub(pat, rep, html, flags=re.I)
    return html


# ---------- 3. Emoji → icon vẽ tay ----------
def _ic(body, vb='0 0 24 24'):
    return (f'<svg class="ic" viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')

ICONS = {
    'target': _ic('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor"/>'),
    'pencil': _ic('<path d="M4 20l1-4L16.5 4.5a2.1 2.1 0 013 3L8 19l-4 1z"/><path d="M14 7l3 3"/>'),
    'bulb': _ic('<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 00-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0012 3z"/>'),
    'flask': _ic('<path d="M9 3h6M10 3v6L5 18a2 2 0 001.8 3h10.4A2 2 0 0019 18l-5-9V3"/><path d="M7.5 15h9"/>'),
    'key': _ic('<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M16 7l3 3M14 9l2 2"/>'),
    'mic': _ic('<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0014 0M12 18v3M9 21h6"/>'),
    'clock': _ic('<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 3h6"/>'),
    'chart': _ic('<path d="M4 20V4M4 20h16"/><rect x="7" y="12" width="3" height="6"/><rect x="12" y="8" width="3" height="10"/><rect x="17" y="5" width="3" height="13"/>'),
    'trend': _ic('<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>'),
    'cycle': _ic('<path d="M20 11a8 8 0 00-14-4M4 13a8 8 0 0014 4"/><path d="M6 3v4h4M18 21v-4h-4"/>'),
    'warn': _ic('<path d="M12 3l10 18H2L12 3z"/><path d="M12 10v5"/><circle cx="12" cy="18" r="0.6" fill="currentColor"/>'),
    'check': _ic('<path d="M4 12.5l5 5L20 6.5"/>'),
    'calc': _ic('<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8"/><path d="M8.5 12h1M12 12h1M15.5 12h1M8.5 16h1M12 16h1M15.5 16h1"/>'),
    'eye': _ic('<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'),
    'plus': _ic('<path d="M12 5v14M5 12h14"/>'),
    'film': _ic('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/>'),
    'ruler': _ic('<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>'),
    'build': _ic('<path d="M3 21h18M6 21V9l6-5 6 5v12"/><path d="M10 21v-6h4v6"/>'),
    'train': _ic('<rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 11h14M9 20l-2 1M15 20l2 1M9 14h.01M15 14h.01"/>'),
    'car': _ic('<path d="M4 15l2-6a2 2 0 012-1.4h8A2 2 0 0118 9l2 6v4h-3v-2H7v2H4z"/><circle cx="8" cy="14" r="0.8" fill="currentColor"/><circle cx="16" cy="14" r="0.8" fill="currentColor"/>'),
    'phone': _ic('<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>'),
}
EMOJI = {
    '🎯': 'target', '✍': 'pencil', '📝': 'pencil', '🤔': 'bulb', '🔬': 'flask', '🔑': 'key',
    '🎤': 'mic', '⏱': 'clock', '📊': 'chart', '📈': 'trend', '🔄': 'cycle', '🔁': 'cycle',
    '⚠': 'warn', '✅': 'check', '🧮': 'calc', '👀': 'eye', '➕': 'plus', '🎞': 'film',
    '📐': 'ruler', '🏗': 'build', '🚆': 'train', '🚗': 'car', '📱': 'phone',
}


def emoji_to_icons(html: str) -> str:
    html = html.replace('️', '')
    for em, name in EMOJI.items():
        html = html.replace(em, f'<span class="ico">{ICONS[name]}</span>')
    html = html.replace('⭐', '★')
    return html


SUB = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9',
       'ₙ': 'n', 'ₓ': 'x', '₋': '−'}


def fix_glyphs(html: str) -> str:
    # chỉ số dưới Unicode → <sub>
    html = re.sub('[' + ''.join(SUB) + ']+', lambda m: '<sub>' + ''.join(SUB[c] for c in m.group(0)) + '</sub>', html)
    # ①②③… → vòng tròn vẽ bằng CSS
    for i, ch in enumerate('①②③④⑤⑥⑦⑧⑨', 1):
        html = html.replace(ch, f'<span class="cn">{i}</span>')
    return html


def fix_math(m: str) -> str:
    """Trong $...$: không được chèn thẻ HTML; đổi ký tự lạ sang lệnh KaTeX."""
    for i, ch in enumerate('①②③④⑤⑥⑦⑧⑨', 1):
        m = m.replace(ch, '\\boxed{%d}' % i)
    m = m.replace('✓', '\\checkmark ').replace('✅', '\\checkmark ')
    m = re.sub('[' + ''.join(SUB) + ']+', lambda x: '_{' + ''.join(SUB[c] for c in x.group(0)) + '}', m)
    m = m.replace('<', '\\lt ').replace('>', '\\gt ')
    return m


WEB = False   # True: xuất dữ liệu cho web (giữ màu/emoji gốc, chỉ sửa công thức)

_TOKEN = re.compile(r'(<svg\b.*?</svg>|\$\$.*?\$\$|\$[^$\n]*?\$)', re.S)


def to_print(html: str) -> str:
    """Toàn bộ biến đổi 'đen–trắng' cho một đoạn HTML (đã gồm SVG và công thức)."""
    out = []
    for tok in _TOKEN.split(html):
        if WEB:
            out.append(fix_math(tok) if tok.startswith('$') else tok)
        elif tok.startswith('<svg'):
            out.append(gray_svg(rewrite_color_words(tok)))
        elif tok.startswith('$'):
            out.append(fix_math(tok))
        else:
            out.append(fix_glyphs(emoji_to_icons(rewrite_color_words(tok))))
    return ''.join(out)
