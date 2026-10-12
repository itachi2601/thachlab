#!/usr/bin/env python3
"""In text một chương của giáo trình .docx (pandoc) để soạn bai.json hoặc dán cho Gemini.
Dùng: python3 trich_chuong.py "<giáo trình.docx>" <số chương>   (cần pandoc)"""
import re, subprocess, sys
if len(sys.argv) < 3:
    sys.exit(__doc__)
docx, n = sys.argv[1], int(sys.argv[2])
txt = subprocess.run(["pandoc", docx, "-t", "plain", "--wrap=none"], capture_output=True, text=True, check=True).stdout
heads = [m.start() for m in re.finditer(r"^Chapter \d+:", txt, flags=re.M)]
starts = [i for i in heads if re.match(rf"Chapter {n}:", txt[i:])]
if not starts:
    sys.exit(f"không thấy 'Chapter {n}:' trong {docx}")
s = starts[0]
e = min([i for i in heads if i > s], default=len(txt))
print(txt[s:e].strip())
