#!/usr/bin/env python3
"""Gộp bài SHCN 3 năm (content/shcn-3-nam/hk*/bNN.{sv,gv}.md) thành 2 file Word.

    python3 scripts/xuat-shcn-3-nam-docx.py <thư mục ra>

Ra: SHCN-3-nam_Tai-lieu-sinh-vien.docx, SHCN-3-nam_Kich-ban-giang-vien.docx (A4 dọc, Times New Roman,
mục lục, mỗi bài sang trang mới). Cần pandoc.
"""
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "shcn-3-nam"
HK_TEN = {
    1: "Năm 1 · HK1 — Đứng vững khi xa nhà",
    2: "Năm 1 · HK2 — Học có phương pháp, sống có nề nếp",
    3: "Năm 2 · HK3 — Giao tiếp và làm việc nhóm",
    4: "Năm 2 · HK4 — Tự quản trị: kế hoạch, vấn đề, tiền",
    5: "Năm 3 · HK5 — Vào doanh nghiệp: tác phong và đạo đức nghề",
    6: "Năm 3 · HK6 — Tìm việc và sống tự lập hẳn",
}
PAGE_BREAK = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'


def nhan_bai(n: int) -> str:
    return {0: "Khởi động", 15: "Tổng kết"}.get(n, f"Bài {n}")


def doc_bai(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    body = text[m.end():] if m else text
    n = int(re.search(r"b(\d\d)\.", path.name).group(1))
    lines = body.strip().splitlines()
    out = []
    for line in lines:
        if line.startswith("# "):
            ten = re.sub(r"\s+—\s+kịch bản giảng viên\s*$", "", line[2:].strip())
            out.append(f"## {nhan_bai(n)}. {ten}")
        elif re.match(r"#{2,5} ", line):
            out.append("#" + line)
        else:
            out.append(line)
    # Pandoc cần dòng trống trước danh sách/bảng; bản .md (GitHub) thì không — chèn cho chắc.
    fixed = []
    block = re.compile(r"\s*([-*] |\d+\. |\|)")
    for line in out:
        if fixed and block.match(line) and fixed[-1].strip() and not block.match(fixed[-1]):
            fixed.append("")
        fixed.append(line)
    body = "\n".join(fixed)
    body = re.sub(r"<details>\s*<summary>(.*?)</summary>", r"**\1**\n", body)
    body = body.replace("</details>", "")
    return body


def tao_reference(tmp: Path) -> Path:
    ref = tmp / "ref.docx"
    with open(ref, "wb") as f:
        subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"], stdout=f, check=True)
    with zipfile.ZipFile(ref) as z:
        files = {n: z.read(n) for n in z.namelist()}
    s = files["word/styles.xml"].decode()
    s = re.sub(r"<w:rFonts [^>]*/>", '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
               'w:eastAsia="Times New Roman" w:cs="Times New Roman" />', s)
    s = s.replace('<w:sz w:val="24" />\n        <w:szCs w:val="24" />',
                  '<w:sz w:val="26" />\n        <w:szCs w:val="26" />', 1)
    s = s.replace('<w:spacing w:after="200" />', '<w:spacing w:after="100" />', 1)
    s = re.sub(r'<w:color w:val="[0-9A-Fa-f]{6}"', '<w:color w:val="1F3864"', s)
    borders = "<w:tblBorders>" + "".join(
        f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        for e in ["top", "left", "bottom", "right", "insideH", "insideV"]) + "</w:tblBorders>"
    s = s.replace('<w:tblInd w:w="0" w:type="dxa" />', '<w:tblInd w:w="0" w:type="dxa" />' + borders, 1)
    s = s.replace('<w:tblStylePr w:type="firstRow">\n      <w:tcPr>',
                  '<w:tblStylePr w:type="firstRow">\n      <w:rPr><w:b/></w:rPr>\n'
                  '      <w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="DCE6F2"/>', 1)
    s = s.replace('<w:basedOn w:val="TableNormal" />\n    <w:semiHidden />',
                  '<w:basedOn w:val="TableNormal" />\n    <w:semiHidden />\n'
                  '    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>', 1)
    files["word/styles.xml"] = s.encode()
    with zipfile.ZipFile(ref, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in files.items():
            z.writestr(n, b)
    return ref


def hau_xu_ly(docx: Path):
    with zipfile.ZipFile(docx) as z:
        files = {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
    s = files["word/document.xml"].decode()
    sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" '
            'w:bottom="1134" w:left="1418" w:header="567" w:footer="567" w:gutter="0"/></w:sectPr>')
    s, n = re.subn(r"<w:sectPr\b.*?</w:sectPr>", sect, s, flags=re.S)
    if n == 0:
        s = s.replace("</w:body>", sect + "</w:body>")
    s = re.sub(r"<w:tblW [^>]*/>", '<w:tblW w:w="5000" w:type="pct"/>', s)
    files["word/document.xml"] = s.encode()
    with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as z:
        for name, b in files.items():
            z.writestr(name, b)


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        ref = tao_reference(tmp)
        for ban, tieu_de, ten_file in [
            ("sv", "Tài liệu sinh viên", "SHCN-3-nam_Tai-lieu-sinh-vien.docx"),
            ("gv", "Kịch bản giảng viên", "SHCN-3-nam_Kich-ban-giang-vien.docx"),
        ]:
            parts = [f'---\ntitle: "SINH HOẠT CHỦ NHIỆM 3 NĂM — TỰ LẬP TỪNG BƯỚC"\nsubtitle: "{tieu_de}"\n---\n']
            thieu = []
            for hk in range(1, 7):
                files = sorted((SRC / f"hk{hk}").glob(f"b??.{ban}.md"))
                if not files:
                    thieu.append(f"hk{hk}")
                    continue
                parts.append(PAGE_BREAK + f"\n# {HK_TEN[hk]}\n")
                for i, f in enumerate(files):
                    if i:
                        parts.append(PAGE_BREAK)
                    parts.append(doc_bai(f))
            md = tmp / f"{ban}.md"
            md.write_text("\n\n".join(parts), encoding="utf-8")
            out = out_dir / ten_file
            subprocess.run(["pandoc", str(md), "-o", str(out), "--reference-doc", str(ref),
                            "--toc", "--toc-depth=2", "-M", "toc-title=Mục lục"], check=True)
            hau_xu_ly(out)
            print(f"{out}  (thiếu: {', '.join(thieu) or 'không'})")


if __name__ == "__main__":
    main()
