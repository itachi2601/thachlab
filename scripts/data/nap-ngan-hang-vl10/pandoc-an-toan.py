#!/usr/bin/env python3
"""pandoc docx -> md; nếu pandoc sập (bảng lạ) thì bỏ từng bảng tới khi chạy được (bảng bị bỏ in ra, thường là bảng lý thuyết). Dùng: python3 pandoc-an-toan.py <docx> <md> <thư-mục-media>"""
import sys, zipfile, re, subprocess, shutil
src, out, media = sys.argv[1:4]
FMT = 'markdown+tex_math_dollars+pipe_tables-smart-simple_tables-multiline_tables-grid_tables'
def run(p): return subprocess.run(['pandoc', p, '-t', FMT, '--wrap=none', '--columns=100000', f'--extract-media={media}', '-o', out], capture_output=True, text=True)
if run(src).returncode == 0: print('ok'); sys.exit(0)
x = zipfile.ZipFile(src).read('word/document.xml').decode()
tb = list(re.finditer(r'<w:tbl>.*?</w:tbl>', x, flags=re.S))
def build(xml, dst):
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zo:
        for it in zi.infolist(): zo.writestr(it, xml.encode() if it.filename == 'word/document.xml' else zi.read(it.filename))
for i, m in enumerate(tb):
    build(x[:m.start()] + x[m.end():], '/tmp/pa.docx')
    if subprocess.run(['pandoc', '/tmp/pa.docx', '-t', 'json'], capture_output=True).returncode == 0:
        print('đã bỏ bảng', i, ':', re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(0)))[:120]); shutil.copy('/tmp/pa.docx', src.replace('.docx', '-an-toan.docx')); run('/tmp/pa.docx'); sys.exit(0)
print('KHÔNG cứu được'); sys.exit(1)
