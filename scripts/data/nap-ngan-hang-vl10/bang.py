"""Bảng pipe-markdown (pandoc) bị dán phẳng trong <p> -> <table> đúng kiểu ngân hàng. Idempotent."""
import re
TD = 'style="border:1px solid currentColor;padding:4px 10px"'
def _cells(parts, n):
    rows, i = [], 0
    while i + n <= len(parts):
        rows.append([c.strip() for c in parts[i:i + n]]); i += n + 1
    return rows
def flat_table(inner):
    """inner: nội dung một đoạn chỉ gồm bảng (đã nối 1 dòng). Trả HTML <table> hoặc None."""
    t = inner.strip()
    if not (t.startswith('|') and t.endswith('|')): return None
    parts = t.split('|')[1:-1]
    # tìm hàng ngăn cách |:---:|---|
    sep = [i for i, c in enumerate(parts) if re.fullmatch(r'\s*:?-{2,}:?\s*', c)]
    if not sep: return None
    n = 0
    while sep[0] + n < len(parts) and re.fullmatch(r'\s*:?-{2,}:?\s*', parts[sep[0] + n]): n += 1
    # hàng tiêu đề nằm ngay trước hàng ngăn cách
    start = sep[0] - (n + 1)
    if start < 0: return None
    body = parts[start:]
    rows = _cells(body, n)
    # bỏ hàng ngăn cách (hàng thứ 2)
    rows = [r for k, r in enumerate(rows) if k != 1]
    if not rows or any(len(r) != n for r in rows): return None
    h = ''.join(f'<th {TD}>{c}</th>' for c in rows[0])
    b = ''.join('<tr>' + ''.join(f'<td {TD}>{c}</td>' for c in r) + '</tr>' for r in rows[1:])
    return f'<table style="border-collapse:collapse;margin:0.5rem 0"><tr>{h}</tr>{b}</table>'
def fix_html(s):
    """Thay mọi <p ...>|bảng|</p> trong chuỗi HTML bằng <table>."""
    def rep(m):
        inner = re.sub(r'\s+', ' ', m.group(2))
        t = flat_table(inner)
        return t if t else m.group(0)
    return re.sub(r'(<p[^>]*>)\s*(\|.*?\|)\s*</p>', rep, s, flags=re.S)
if __name__ == '__main__':
    x = '<p class="a">|   <strong>Thời gian (s)</strong>    |  0  |  2  | |:---:|:---:|:---:| | <strong>Độ dịch chuyển (m)</strong> |  0  |  2  |</p>'
    print(fix_html(x))
