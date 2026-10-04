#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Số hoá bộ đề Vật lí 10 năm 24-25 (thư mục CT2025_VietnamTeach) lên thachlab — đường script, ít token.

    python3 scripts/dang-de-l10-24-25.py --list                      # liệt kê bộ đề + file đại diện + nguồn đáp án
    python3 scripts/dang-de-l10-24-25.py --sets "TRAN NGUYEN HAN" "LY NHAN TONG" [--dry]
    python3 scripts/dang-de-l10-24-25.py --all [--limit N] [--offset K] [--dry]

Mỗi BỘ (thư mục con hoặc file lẻ trong 1. GHK1 / 2. HK1 / ...) → đúng MỘT đề trên web:
  1. chọn 1 file đại diện (ưu tiên "đề gốc"/mã 000, rồi mã có trong file đáp án, rồi file đầu); .doc → soffice.
  2. lấy đáp án từ file rời (xlsx McMix "Đề\\câu", docx đáp án) — bảng quen thuộc đọc thẳng, lạ thì nhờ AI
     qua API (Sonnet, effort low) đọc thành JSON; không có file rời thì để convert_docx.py tự đọc mục ĐÁP ÁN trong đề.
  3. ghép thành bản "đề + BẢNG ĐÁP ÁN" theo đúng 3 bảng mà convert_docx.py (skill azota) hiểu; cắt phần TỰ LUẬN
     (parser thachlab chưa nhận câu tự luận từ .docx — ghi vào log để làm sau).
  4. mtef_to_omml_v2 → convert_docx.py → xuat_thachlab.py (nhãn trống) → upload-exam-docx.mts --drop-bad
     vào mục Kiểm tra giữa/cuối kì lớp 10 (đang ẩn). Kết quả từng bộ ghi scripts/data/de-l10-24-25-run.json,
     file trung gian + convert.log giữ ở scripts/logs/de-l10-24-25/<bộ>/ để soát.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/MAC/Documents/THPT/Lop10/00_Dung_chung/Thu_vien_tai_lieu/CT2025_VietnamTeach/đề thi /24-25/ĐỀ VẬT LÍ 10 2025"
MTEF = "/Users/MAC/Documents/THPT/Lop12/NamHoc/2026-2027/06_Azota_so_hoa/_CongCu/mtef_to_omml_v2.py"
AZ = os.path.expanduser("~/.codex/skills/azota/scripts")
SOFFICE = "/opt/homebrew/bin/soffice"
LOG = os.path.join(ROOT, "scripts/data/de-l10-24-25-log.json")
RUN = os.path.join(ROOT, "scripts/data/de-l10-24-25-run.json")
WORK = os.path.join(ROOT, "scripts/logs/de-l10-24-25")
# kỳ → (lesson_id, lesson_item_id) mục Kiểm tra giữa/cuối kì lớp 10 (lesson 113–116, đang ẩn)
TARGET = {"1. GHK1": (113, 53), "2. HK1": (114, 54), "3. GHK2": (115, 55), "4. HK2": (116, 56), "5. TỔNG HỢP": (114, 54)}
KY_LABEL = {"1. GHK1": "Giữa HK1", "2. HK1": "Cuối HK1", "3. GHK2": "Giữa HK2", "4. HK2": "Cuối HK2", "5. TỔNG HỢP": "Cuối HK1"}

sys.path.insert(0, AZ)
from docx import Document  # noqa: E402
from docx.shared import Pt  # noqa: E402

args = sys.argv[1:]
DRY = "--dry" in args


def opt(n, d=None):
    return args[args.index(n) + 1] if n in args else d


def env(name):
    for line in open(os.path.join(ROOT, ".env.local"), encoding="utf-8"):
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"')
    return None


RE_KEYNAME = re.compile(r"dap[\s_-]*a[np]|đáp[\s_-]*á[np]|dapan|hdc|huong dan cham|hướng dẫn chấm|\bda\b|\bkey\b", re.I)
RE_MATRIX = re.compile(r"ma[\s_-]*tr[aậ]n|dac ta|đặc tả|mt\+|bang dac", re.I)
RE_GOC = re.compile(r"g[oố]c", re.I)
RE_TULUAN = re.compile(r"T[ỰU]\s*LU[ẬA]N", re.I)
RE_HET = re.compile(r"^[\s\-–—−=*_.]*H[ẾE]T[\s\-–—−=*_.]*$", re.I)
RE_CAU = re.compile(r"^\s*Câu\s*(\d+)\s*[:.]")


# ---------- liệt kê bộ ----------
def list_sets():
    sets = []
    for ky in sorted(os.listdir(SRC)):
        kyd = os.path.join(SRC, ky)
        if not os.path.isdir(kyd) or ky not in TARGET and ky != "6. HSG":
            continue
        for name in sorted(os.listdir(kyd)):
            p = os.path.join(kyd, name)
            if name.startswith((".", "~$")):
                continue
            files = []
            if os.path.isdir(p):
                for r, _, fs in os.walk(p):
                    files += [os.path.join(r, f) for f in fs if not f.startswith((".", "~$"))]
            else:
                files = [p]
            exams, keys = [], []
            for f in files:
                b = os.path.basename(f)
                ext = b.rsplit(".", 1)[-1].lower()
                if ext in ("xlsx", "xls") or (ext in ("doc", "docx") and RE_KEYNAME.search(b)):
                    keys.append(f)
                elif ext in ("doc", "docx") and not RE_MATRIX.search(b):
                    exams.append(f)
            if exams and len(exams) >= 2 and not keys and not any(made_of(f) for f in exams):
                for f in sorted(exams):  # thư mục gom nhiều đề khác nhau (vd "Bộ đề team dự án") → mỗi file một bộ
                    sets.append({"ky": ky, "name": name + "/" + os.path.basename(f), "exams": [f], "keys": []})
            elif exams:
                sets.append({"ky": ky, "name": name, "exams": sorted(exams), "keys": sorted(keys)})
    return sets


def made_of(path):
    b = os.path.basename(path)
    m = re.search(r"(?<!\d)(\d{3})(?!\d)", b)
    return m.group(1) if m else None


def pick_exam(s, key_mades):
    ex = s["exams"]
    goc = [f for f in ex if RE_GOC.search(os.path.basename(f))]
    if goc:
        return goc[0], "000"
    ex = sorted(ex, key=lambda f: (1 if re.search(r"(?<![A-Z])TL(?![A-Z])|t[ựu] lu[ậa]n", os.path.basename(f), re.I) else 0, 0 if re.search(r"(?<![A-Z])TN(?![A-Z])", os.path.basename(f)) else 1, f))
    for f in ex:
        m = made_of(f)
        if m and (not key_mades or m in key_mades):
            return f, m
    return ex[0], made_of(ex[0])


# ---------- .doc → .docx ----------
def to_docx(path, wd):
    if path.lower().endswith(".docx"):
        return path
    subprocess.run([SOFFICE, "--headless", "--convert-to", "docx", "--outdir", wd, path], capture_output=True)
    out = os.path.join(wd, os.path.splitext(os.path.basename(path))[0] + ".docx")
    return out if os.path.exists(out) else None


# ---------- đọc đáp án ----------
def split_parts(headers, values):
    """Dãy cột McMix: 1..N (phần I) | 1a..4d hoặc Đ/S đánh số liên tục (phần II) | 1..6 (phần III)
    → dap = {1:{n:X},2:{n:{y:Đ/S}},3:{n:v}}."""
    dap = {1: {}, 2: {}, 3: {}}
    pairs = [(str(h).strip().lower(), ("" if v is None else str(v).strip())) for h, v in zip(headers, values)]
    pairs = [(h, v) for h, v in pairs if h and v]

    def is_ds(v):
        return v.upper() in ("Đ", "S", "D", "T", "F", "ĐÚNG", "SAI", "DUNG")

    phase, last, flat = 1, 0, []
    for i, (h, v) in enumerate(pairs):
        if re.fullmatch(r"[ĐDS]{4}", v.upper()) and h.isdigit():
            phase = 2
            dap[2][len(dap[2]) + 1] = {y: ("Đ" if ch in "ĐD" else "S") for y, ch in zip("abcd", v.upper())}
            continue
        m2 = re.match(r"^(\d+)\s*([a-d])\)?$", h)
        if m2:
            phase = 2
            dap[2].setdefault(int(m2.group(1)), {})[m2.group(2)] = "Đ" if v.upper().startswith(("Đ", "D", "T")) else "S"
            continue
        if not h.isdigit():
            continue
        n = int(h)
        if phase == 1:
            # chuyển sang Đ/S phẳng khi gặp S/Đ, hoặc 'D' mà 4 ô kế tiếp đều là D/S (sau ít nhất 4 câu TN)
            nxt = [x[1] for x in pairs[i:i + 4]]
            if len(dap[1]) >= 4 and (v.upper() in ("S", "Đ") or (v.upper() == "D" and len(nxt) == 4 and all(is_ds(x) for x in nxt))):
                phase = 2.5
            elif n <= last and dap[1]:
                phase = 3
        if phase == 2.5:
            if is_ds(v):
                flat.append("Đ" if v.upper().startswith(("Đ", "D", "T")) else "S")
                continue
            phase = 3
        if phase == 2:
            phase = 3
        last = n
        if phase == 1 and re.fullmatch(r"[A-Da-d]", v):
            dap[1][n] = v.upper()
        elif phase == 3:
            dap[3][len(dap[3]) + 1] = v
    for k in range(0, len(flat), 4):
        dap[2][k // 4 + 1] = {y: x for y, x in zip("abcd", flat[k:k + 4])}
    return dap


def _cell(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip()


def key_from_grid(rows, made):
    """rows: list[list] của một bảng. Ba bố cục:
    (L) cột dài  MÃ ĐỀ | CÂU | ĐÁP ÁN;
    (R) hàng = mã ("Đề\\câu" McMix: hàng tiêu đề là số câu, mỗi hàng dưới là một mã);
    (C) cột = mã (hàng tiêu đề chứa ≥2 mã 3 chữ số, cột đầu là số câu)."""
    rows = [[_cell(c) for c in r] for r in rows if r]
    rows = [r for r in rows if any(r)]
    if not rows:
        return None
    is_made = lambda x: bool(re.fullmatch(r"\d{3}", x))  # noqa: E731
    # (L)
    for i, r in enumerate(rows[:3]):
        low = [c.lower() for c in r]
        if len(r) >= 3 and any("mã" in c for c in low) and any("câu" in c for c in low) and any("đáp" in c for c in low):
            im = next(j for j, c in enumerate(low) if "mã" in c)
            ic = next(j for j, c in enumerate(low) if "câu" in c)
            ia = next(j for j, c in enumerate(low) if "đáp" in c)
            by = {}
            for rr in rows[i + 1:]:
                if len(rr) > max(im, ic, ia) and is_made(rr[im]):
                    by.setdefault(rr[im], []).append((rr[ic], rr[ia]))
            row = by.get(made) or (next(iter(by.values())) if by else None)
            if row:
                return split_parts([h for h, _ in row], [v for _, v in row])
    # (R) hàng = mã
    for i, r in enumerate(rows):
        if is_made(r[0]) and sum(1 for c in r[1:] if c) >= 5:
            hdr = next((rows[j] for j in range(i - 1, -1, -1) if sum(1 for c in rows[j][1:] if c) >= 5), None)
            if not hdr:
                break
            cands = {rr[0]: rr[1:] for rr in rows[i:] if rr and is_made(rr[0])}
            row = cands.get(made) or cands.get("000") or next(iter(cands.values()))
            return split_parts(hdr[1:], row)
    # (C) cột = mã
    for i, r in enumerate(rows):
        mades = [c for c in r[1:] if is_made(c)]
        if len(mades) >= 2 or (len(r) >= 2 and is_made(r[1]) and sum(1 for c in r if c) <= 3 and len(rows) > i + 5):
            col = r.index(made) if made in r else next(j for j, c in enumerate(r) if is_made(c))
            if col == 0:
                continue
            body = rows[i + 1:]
            hdrs = [rr[0] for rr in body if rr and rr[0]]
            vals = [(rr[col] if len(rr) > col else "") for rr in body if rr and rr[0]]
            d = split_parts(hdrs, vals)
            if d[1] or d[3]:
                return d
    return None


def key_from_xlsx(path, made):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    for ws in wb.worksheets:
        d = key_from_grid([[c for c in r] for r in ws.iter_rows(values_only=True)], made)
        if d and (d[1] or d[3]):
            return d
    return None


def docx_dump(path):
    """Văn bản + bảng của file docx theo thứ tự, để đưa cho AI đọc."""
    doc = Document(path)
    out = []
    body = doc.element.body
    for el in body.iterchildren():
        tag = el.tag.split("}")[-1]
        if tag == "p":
            t = "".join(x.text or "" for x in el.iter() if x.tag.endswith("}t")).strip()
            if t:
                out.append(t)
        elif tag == "tbl":
            for tr in el.iter():
                if tr.tag.endswith("}tr"):
                    cells = []
                    for tc in tr.iterchildren():
                        if tc.tag.endswith("}tc"):
                            cells.append("".join(x.text or "" for x in tc.iter() if x.tag.endswith("}t")).strip())
                    out.append(" | ".join(cells))
            out.append("")
    return "\n".join(out)


def key_from_docx(path, made):
    doc = Document(path)
    for t in doc.tables:
        d = key_from_grid([[c.text for c in r.cells] for r in t.rows], made)
        if d and (d[1] or d[3]):
            return d
    return None


AI_SYS = ("Bạn đọc file đáp án đề Vật lí 10 và trả về JSON thuần (không markdown). Đề có thể có nhiều mã đề; "
          "chỉ lấy đáp án của MÃ ĐỀ được hỏi (nếu file chỉ có một bộ đáp án hoặc mã '000'/'gốc' thì lấy bộ đó). "
          "Phần I (trắc nghiệm A/B/C/D) đánh số lại từ 1; Phần II (đúng/sai, mỗi câu 4 ý a-d, giá trị 'Đ' hoặc 'S') "
          "đánh số lại từ 1; Phần III (trả lời ngắn, giá trị số/chuỗi ngắn) đánh số lại từ 1. Nếu đề đánh số liên tục "
          "(Câu 19-22 là phần II) thì vẫn đánh lại từ 1 trong từng phần. Bỏ qua tự luận/thang điểm. "
          'Định dạng: {"p1": {"1": "A"}, "p2": {"1": {"a": "Đ", "b": "S", "c": "Đ", "d": "S"}}, "p3": {"1": "2,5"}}. '
          "Thiếu phần nào thì để {}. Nếu không tìm thấy đáp án cho mã đó, trả {\"p1\":{},\"p2\":{},\"p3\":{},\"loi\":\"...\"}.")


def key_from_ai(text, made, tag):
    key = env("ANTHROPIC_API_KEY")
    if not key:
        return None, "thiếu ANTHROPIC_API_KEY"
    body = {"model": "claude-sonnet-5-5", "max_tokens": 12000, "output_config": {"effort": "low"}, "system": AI_SYS,
            "messages": [{"role": "user", "content": f"Mã đề cần lấy: {made or 'không rõ (lấy bộ đầu tiên/đề gốc)'}\n\n{text[:60000]}"}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"})
    data = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                data = json.loads(r.read())
            break
        except Exception as e:  # noqa: BLE001
            err = f"API lỗi: {str(e)[:120]}"
    if data is None:
        return None, err
    txt = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    usage = data.get("usage", {})
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        return None, "AI không trả JSON"
    try:
        j = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None, "JSON AI hỏng"
    dap = {1: {int(k): str(v).strip().upper() for k, v in j.get("p1", {}).items() if str(v).strip()},
           2: {int(k): {y.lower(): ("Đ" if str(x).strip().upper().startswith(("Đ", "D", "T")) else "S") for y, x in v.items()} for k, v in j.get("p2", {}).items()},
           3: {int(k): str(v).strip() for k, v in j.get("p3", {}).items() if str(v).strip()}}
    note = f"AI đọc ({usage.get('input_tokens', '?')}/{usage.get('output_tokens', '?')} tok)" + (f" — {j['loi']}" if j.get("loi") else "")
    return dap, note


# ---------- ghép đề + bảng đáp án ----------
def para_text(el):
    return "".join(x.text or "" for x in el.iter() if x.tag.endswith("}t")).strip()


RE_LABEL_AFTER = re.compile(r"^\s*(?:[A-D][.)]|[a-d]\))(?:\s|$)")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


RE_LABEL_HEAD = re.compile(r"^\s*\*?\s*([A-D][.)]|[a-d]\))")
M_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"


def _p_text(p):
    return "".join(("\t" if x.tag in (W + "tab", W + "ptab") else (x.text or "")) for x in p.iter() if x.tag in (W + "t", W + "tab", W + "ptab"))


def _split_run_at(run, kid_idx, offset=None):
    """Tách run thành 2 run tại kid_idx (và tại offset trong w:t nếu có). Trả về run thứ hai (đã chèn sau run)."""
    import copy
    kids = list(run)
    tail = copy.deepcopy(run)
    tkids = list(tail)
    # run gốc giữ kids[:kid_idx] (+ phần đầu w:t nếu offset); tail giữ kids[kid_idx:] (+ phần sau)
    for x in kids[kid_idx + (1 if offset is None else 0):]:
        if x.tag != W + "rPr":
            run.remove(x)
    for x in tkids[:kid_idx]:
        if x.tag != W + "rPr":
            tail.remove(x)
    if offset is not None:
        kids[kid_idx].text = kids[kid_idx].text[:offset]
        tkids[kid_idx].text = tkids[kid_idx].text[offset:]
        tkids[kid_idx].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        kids[kid_idx].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    else:
        tail.remove(tkids[kid_idx])  # bỏ chính w:tab
    run.addnext(tail)
    return tail


def split_option_paragraphs(doc):
    """'A. x<tab>B. y' hay 'A. x B. y' trong MỘT đoạn → mỗi phương án một đoạn (giữ run, công thức, ảnh theo đúng thứ tự).
    Sau đó sắp lại A→D (bố cục 2 cột cho A C / B D) và chèn dấu cách sau nhãn ('A.770' → 'A. 770')."""
    import copy
    n_split = 0
    body = doc.element.body
    for p in list(body.iter(W + "p")):
        text = _p_text(p)
        labels = re.findall(r"(?:^|\s)(?:[A-D][.)]|[a-d]\))(?=\s|\d|[A-Za-zÀ-ỹ])", " " + text)
        if len(labels) < 2:
            continue
        # 1) chuẩn hoá: mọi điểm cắt đưa về ranh giới run (child của p)
        changed = True
        guard = 0
        while changed and guard < 40:
            changed = False
            guard += 1
            kids_p = [c for c in p if c.tag != W + "pPr"]
            for ci, c in enumerate(kids_p):
                if c.tag != W + "r":
                    continue
                rk = list(c)
                for ki, k in enumerate(rk):
                    if k.tag in (W + "tab", W + "ptab"):
                        after = "".join(x.text or "" for x in rk[ki + 1:] if x.tag == W + "t")
                        for c2 in kids_p[ci + 1:]:
                            after += "".join(x.text or "" for x in c2.iter(W + "t"))
                            if len(after) > 6:
                                break
                        before = "".join(x.text or "" for x in rk[:ki] if x.tag == W + "t")
                        if RE_LABEL_HEAD.match(after) and (ki > 0 or ci > 0) and not (ki == 0 and ci == 0):
                            if ki == 0 and not before and all(x.tag == W + "rPr" for x in rk[:ki]):
                                continue  # tab đứng đầu run đầu: không cắt
                            _split_run_at(c, ki)
                            changed = True
                            break
                    elif k.tag == W + "t" and k.text:
                        m = re.search(r"(?<=[.\s)])\s*(?=[B-Da-d][.)](?:\s|\d|[A-Za-zÀ-ỹ]))", k.text)
                        if m and m.start() > 0 and k.text[:m.start()].strip():
                            _split_run_at(c, ki, m.start())
                            changed = True
                            break
                if changed:
                    break
        # 2) cắt đoạn tại các run bắt đầu bằng nhãn (trừ run đầu tiên)
        kids_p = [c for c in p if c.tag != W + "pPr"]
        cuts = []
        first_text_seen = False
        for ci, c in enumerate(kids_p):
            t = "".join(x.text or "" for x in c.iter(W + "t")) if c.tag == W + "r" else ""
            if c.tag == W + "r" and t.strip():
                if first_text_seen and RE_LABEL_HEAD.match(t):
                    cuts.append(ci)
                first_text_seen = True
        if not cuts:
            continue
        prev = p
        for ci in reversed(cuts):
            newp = copy.deepcopy(p)
            for x in [x for x in newp if x.tag != W + "pPr"]:
                newp.remove(x)
            for x in kids_p[ci:]:
                p.remove(x)
                newp.append(x)
            p.addnext(newp)
            kids_p = kids_p[:ci]
        n_split += 1
    # 3) chèn dấu cách sau nhãn + sắp lại thứ tự A→D trong từng câu
    paras = list(body.iter(W + "p"))
    group = []

    def flush(group):
        if len(group) >= 3:
            labs = [g[0] for g in group]
            if labs != sorted(labs) and sorted(labs) == sorted(set(labs)):
                els = [g[1] for g in group]
                order = sorted(range(len(els)), key=lambda i: labs[i])
                anchor = els[0]
                for i in order:
                    anchor.addnext(els[i]) if els[i] is not anchor else None
                    anchor = els[i]
        group.clear()

    for p in paras:
        ts = [x for x in p.iter(W + "t") if x.text and x.text.strip()]
        if not ts:
            continue
        head = ts[0].text
        m = re.match(r"^(\s*\*?\s*)([A-D][.)]|[a-d]\))(\S)", head)
        if m:
            ts[0].text = m.group(1) + m.group(2) + " " + head[m.end(2):]
            ts[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        m = RE_LABEL_HEAD.match(_p_text(p))
        if m:
            group.append((m.group(1)[0].upper(), p))
        else:
            flush(group)
    flush(group)
    return n_split


def school_from_doc(doc):
    """'TRƯỜNG THPT X' + 'SỞ GD&ĐT Y' ở 12 đoạn đầu (kể cả trong bảng) → 'THPT X – Y'."""
    texts = []
    for el in doc.element.body.iter(W + "p"):
        t = re.sub(r"\s+", " ", "".join(x.text or "" for x in el.iter(W + "t"))).strip()
        if t:
            texts.append(t)
        if len(texts) >= 14:
            break
    school = province = ""
    for t in texts:
        m = re.search(r"TR[ƯU][ỜO]NG\s+((?:THPT|THCS|PT\s*DTNT|PTDTNT|TH\s*&\s*THCS|THCS\s*&\s*THPT|THCS\s*-\s*THPT|TIỂU HỌC)[^–\-:(]{2,45})", t, re.I)
        if m and not school:
            school = re.split(r"\s*(?:KIỂM TRA|ĐỀ |NĂM HỌC|MÔN|LỚP|MÃ ĐỀ|TỔ(?!NG)|NHÓM|HỌ VÀ TÊN)", re.sub(r"\s+", " ", m.group(1)), flags=re.I)[0]
            school = " ".join(school.split()[:6]).strip(" .,")
        m = re.search(r"S[ỞO]\s+GD\s*(?:&|VÀ|-)?\s*(?:ĐT|ĐÀO TẠO)\s+([^–\-:(]{2,40})", t, re.I)
        if m and not province:
            province = re.split(r"\s*TR[ƯU][ỜO]NG", m.group(1), flags=re.I)[0]
            province = " ".join(province.split()[:3]).strip(" .,")
    if school:
        school = school.title()
        for w in ("Thpt", "Thcs", "Ptdtnt", "Dtnt", "Tp", "Hcm"):
            school = re.sub(r"\b" + w + r"\b", w.upper(), school)
        return school + (f" – {province.title()}" if province else "")
    return ""


def materialize_numbering(doc):
    """Word đánh số tự động (numPr) → ghi số vào chữ: decimal → 'Câu N. ', chữ hoa → 'A. ', chữ thường → 'a) '."""
    try:
        numbering = doc.part.numbering_part.element
    except Exception:  # noqa: BLE001
        return 0
    abs_of = {n.get(W + "numId"): n.find(W + "abstractNumId").get(W + "val") for n in numbering.findall(W + "num") if n.find(W + "abstractNumId") is not None}
    lv = {}
    for an in numbering.findall(W + "abstractNum"):
        for l in an.findall(W + "lvl"):
            fmt = l.find(W + "numFmt")
            txt = l.find(W + "lvlText")
            st = l.find(W + "start")
            lv[(an.get(W + "abstractNumId"), l.get(W + "ilvl"))] = (fmt.get(W + "val") if fmt is not None else "decimal", txt.get(W + "val") if txt is not None else "%1.", int(st.get(W + "val")) if st is not None else 1)
    counters, n_done = {}, 0
    for p in doc.element.body.iter(W + "p"):
        ppr = p.find(W + "pPr")
        npr = ppr.find(W + "numPr") if ppr is not None else None
        if npr is None or npr.find(W + "numId") is None:
            continue
        nid = npr.find(W + "numId").get(W + "val")
        il = npr.find(W + "ilvl").get(W + "val") if npr.find(W + "ilvl") is not None else "0"
        fmt, txt, st = lv.get((abs_of.get(nid), il), ("decimal", "%1.", 1))
        if fmt in ("bullet", "none"):
            continue
        key = (nid, il)
        counters[key] = counters.get(key, st - 1) + 1
        for k2 in [k for k in counters if k[0] == nid and int(k[1]) > int(il)]:
            counters.pop(k2)
        n = counters[key]
        if fmt == "upperLetter":
            label = chr(64 + n) + ". "
        elif fmt == "lowerLetter":
            label = chr(96 + n) + ") "
        elif fmt in ("decimal", "decimalZero"):
            label = ("Câu %d. " % n) if "Câu" not in txt else txt.replace("%1", str(n)) + " "
        else:
            continue
        first = next((x for x in p.iter(W + "t")), None)
        if first is None:
            r = p.makeelement(W + "r", {})
            first = r.makeelement(W + "t", {})
            r.append(first)
            p.append(r)
        if re.match(r"^\s*(Câu\s*\d|[A-D][.)]|[a-d]\))", first.text or ""):
            continue
        first.text = label + (first.text or "")
        first.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        npr.getparent().remove(npr)
        n_done += 1
    return n_done


def flatten_option_tables(doc):
    """Bảng mà mọi ô có chữ đều bắt đầu bằng nhãn A./B./a) (2x2, 1x4, 4x1) → đưa các đoạn trong ô ra ngoài, bỏ bảng."""
    n = 0
    body = doc.element.body
    for tbl in list(body.iter(W + "tbl")):
        if tbl.getparent() is not body:
            continue
        cells = [tc for tc in tbl.iter(W + "tc")]
        texts = ["".join(x.text or "" for x in tc.iter(W + "t")).strip() for tc in cells]
        nonempty = [t for t in texts if t]
        if not (2 <= len(nonempty) <= 8) or not all(RE_LABEL_HEAD.match(t) for t in nonempty):
            continue
        for tc in cells:
            for p in list(tc.findall(W + "p")):
                if "".join(x.text or "" for x in p.iter(W + "t")).strip() or p.find(".//" + W + "drawing") is not None:
                    tbl.addprevious(p)
        body.remove(tbl)
        n += 1
    return n


def _top(el, body):
    while el.getparent() is not None and el.getparent() is not body:
        el = el.getparent()
    return el


def prepare_exam(src_docx, dst, dap, cut_tail=True):
    """Chuẩn hoá tiêu đề PHẦN, cắt tự luận, nối BẢNG ĐÁP ÁN. Trả về ghi chú."""
    doc = Document(src_docx)
    notes = []
    body = doc.element.body
    nn = materialize_numbering(doc)
    if nn:
        notes.append(f"ghi số tự động vào chữ cho {nn} đoạn")
    nt = flatten_option_tables(doc)
    if nt:
        notes.append(f"trải {nt} bảng phương án thành đoạn")
    ns = split_option_paragraphs(doc)
    if ns:
        notes.append(f"tách {ns} đoạn phương án chung dòng")
    # 1) chuẩn hoá "Phần 1:", "PHẦN I:" → "PHẦN I." (convert_docx chỉ nhận dạng này); tìm Câu đầu, tiêu đề TỰ LUẬN, HẾT
    paras = list(body.iter(W + "p"))
    heads = {}  # part → index trong paras
    first_cau = None
    cut_el = None
    for i, el in enumerate(paras):
        t = para_text(el)
        m = re.match(r"^\s*(PH[ẦA]N|Ph[ầa]n)\s*(I{1,3}|[1-3]|IV|4)\s*[.:\-–]?\s*(.*)$", t)
        if m and not RE_TULUAN.search(t) and len(t) < 400:
            k = {"I": 1, "1": 1, "II": 2, "2": 2, "III": 3, "3": 3}.get(m.group(2))
            if k and k not in heads:
                heads[k] = i
                ts = [x for x in el.iter(W + "t")]
                for x in ts:
                    x.text = ""
                if ts:
                    ts[0].text = f"PHẦN {'I' * k}. {m.group(3)}"
                continue
        if first_cau is None and RE_CAU.match(t):
            first_cau = i
        is_tl = RE_TULUAN.search(t) and (re.match(r"^\s*(PH[ẦA]N|Ph[ầa]n|B\.|II\.|2\.|IV\.)", t) or t.upper().startswith("TỰ LUẬN")) and len(t) < 120
        if cut_el is None and first_cau is not None and i > first_cau and (is_tl or (cut_tail and RE_HET.match(t))):
            cut_el = (_top(el, body), "TỰ LUẬN" if is_tl else "HẾT", i)
    if first_cau is None:
        notes.append("không thấy 'Câu N.' nào")
    # 1a) không có PHẦN I trước Câu đầu → chèn
    if first_cau is not None and (1 not in heads or heads[1] > first_cau):
        top = _top(paras[first_cau], body)
        np_ = doc.paragraphs[0].insert_paragraph_before("PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn.")
        top.addprevious(np_._p)
        notes.append("chèn PHẦN I trước Câu đầu")
        heads[1] = -1
    # 1b) không có PHẦN II/III mà đáp án có (hoặc đề không tiêu đề) → suy phần theo cấu trúc câu
    need2 = (dap and dap[2] and 2 not in heads) or (not dap and 2 not in heads)
    need3 = (dap and dap[3] and 3 not in heads) or (not dap and 3 not in heads)
    if first_cau is not None and (need2 or need3):
        paras = list(body.iter(W + "p"))
        blocks = []  # (index Câu, kind)
        cur = None
        stop = cut_el[2] + 1 if cut_el else len(paras)
        for i, el in enumerate(paras[:stop]):
            t = para_text(el)
            if RE_CAU.match(t):
                cur = [i, 0, 0]
                blocks.append(cur)
            elif cur is not None:
                if re.match(r"^\s*\*?\s*[A-D][.)]", t):
                    cur[1] += 1
                elif re.match(r"^\s*\*?\s*[a-d]\)", t):
                    cur[2] += 1
        kinds = [(b[0], 1 if b[1] >= 3 else 2 if b[2] >= 3 else 3) for b in blocks]
        done = set()
        for idx, k in kinds:
            if k in (2, 3) and k not in heads and k not in done and (k == 2 and need2 or k == 3 and need3):
                # chỉ chèn khi từ đây về sau không còn câu loại 1 (tránh câu TN mất phương án vì bảng)
                later = [kk for ii, kk in kinds if ii > idx]
                if 1 in later and later.count(1) > 1:
                    continue
                top = _top(paras[idx], body)
                np_ = doc.paragraphs[0].insert_paragraph_before(TITLE_PART[k])
                top.addprevious(np_._p)
                done.add(k)
                notes.append(f"suy ra PHẦN {'I' * k} từ cấu trúc câu")
    # 1c) cắt từ tiêu đề TỰ LUẬN / HẾT tới hết
    if cut_el is not None:
        hit = False
        for el in list(body.iterchildren()):
            if el is cut_el[0]:
                hit = True
            if hit and not el.tag.endswith("}sectPr"):
                body.remove(el)
        notes.append(f"đã cắt từ '{cut_el[1]}'")
    # 1d) đối chiếu số câu thật trong đề với khoá: đề thiếu số (13→15) hay đánh số liên tục (19–22) → gán theo SỐ CÂU rồi đánh lại 1..n
    if dap:
        part, nums = 0, {1: [], 2: [], 3: []}
        for el in body.iter(W + "p"):
            t = para_text(el)
            m = re.match(r"^\s*PHẦN (I{1,3})\.", t)
            if m:
                part = len(m.group(1))
                continue
            m = RE_CAU.match(t)
            if m and part:
                nums[part].append(int(m.group(1)))
        for k in (1, 2, 3):
            if not dap[k] or not nums[k] or len(nums[k]) == len(dap[k]) and nums[k] == sorted(dap[k]):
                continue
            keys = sorted(dap[k])
            off = nums[k][0] - 1 if nums[k][0] > 1 and keys[0] == 1 else 0
            cand = [n - off for n in nums[k]]
            if all(n in dap[k] for n in cand) and len(set(cand)) == len(cand):
                dap[k] = {i + 1: dap[k][n] for i, n in enumerate(cand)}
                notes.append(f"P{k}: đề đánh số {nums[k][0]}–{nums[k][-1]} ({len(nums[k])} câu) — gán đáp án theo số câu, bỏ {len(keys) - len(cand)} đáp án thừa")
    # 2) nối bảng đáp án (3 bảng theo đúng bố cục convert_docx.py đọc)
    if dap:
        doc.add_paragraph("-------- HẾT --------")
        doc.add_paragraph("BẢNG ĐÁP ÁN")
        if dap[1]:
            ns = sorted(dap[1])
            t = doc.add_table(rows=(len(ns) + 9) // 10, cols=10)
            for j, n in enumerate(ns):
                t.rows[j // 10].cells[j % 10].text = f"{n}.{dap[1][n]}"
        if dap[2]:
            ns = sorted(dap[2])
            t = doc.add_table(rows=1, cols=6)
            for c, h in zip(t.rows[0].cells, ["Câu", "Lệnh hỏi", "Đáp án (Đ/S)", "Câu", "Lệnh hỏi", "Đáp án (Đ/S)"]):
                c.text = h
            half = (len(ns) + 1) // 2
            for j in range(half):
                for y in "abcd":
                    row = t.add_row().cells
                    for off, idx in ((0, j), (3, j + half)):
                        if idx < len(ns):
                            n = ns[idx]
                            row[off].text, row[off + 1].text, row[off + 2].text = str(n), f"{y})", dap[2][n].get(y, "")
        if dap[3]:
            ns = sorted(dap[3])
            t = doc.add_table(rows=1, cols=4)
            for c, h in zip(t.rows[0].cells, ["Câu", "Đáp án", "Câu", "Đáp án"]):
                c.text = h
            half = (len(ns) + 1) // 2
            for j in range(half):
                row = t.add_row().cells
                for off, idx in ((0, j), (2, j + half)):
                    if idx < len(ns):
                        row[off].text, row[off + 1].text = str(ns[idx]), dap[3][ns[idx]]
    doc.save(dst)
    return notes


TITLE_PART = {2: "PHẦN II. Câu trắc nghiệm đúng sai.", 3: "PHẦN III. Câu trắc nghiệm trả lời ngắn."}


# ---------- tên đề ----------
DROP = re.compile(r"^(VAT|VẬT|LY|LÝ|LI|LÍ|10|KNTT|CTST|CD|XXX|GIUA|GIỮA|CUOI|CUỐI|HK\s*[12I]*|HKI|HKII|KT|KTGK\d?|GK\d?|CK\d?|HOC|HỌC|KI|KÌ|KY|KỲ|\d{4}|\d{4}-\d{4}|24-25|DE|ĐỀ|DEDA|DEDAN|MATRAN|DEDAMATRAN|\d|SP TAP HUAN)$", re.I)


def title_of(s):
    raw = re.sub(r"\.(docx?|pdf)$", "", s["name"], flags=re.I)
    raw = re.sub(r"[@(].*$", "", raw)
    segs = [x.strip() for x in re.split(r"[-–_]", raw) if x.strip()]
    keep = []
    for sg in segs:
        words = [w for w in sg.split() if not DROP.match(w)]
        if words:
            keep.append(" ".join(words))
    school = " – ".join(keep) if keep else raw
    school = school.title()
    for w in ("Thpt", "Thcs", "Ptdtnt", "Dtnt", "Gdtx", "Tphcm", "Tp Hcm", "Hcm", "Pt ", "Vp", "Dn"):
        school = re.sub(r"\b" + re.escape(w) + r"\b", w.upper(), school)
    return f"{KY_LABEL[s['ky']]} 2024–2025 – {school}"[:140]


# ---------- chạy một bộ ----------
def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def process(s, log):
    slug = re.sub(r"[^A-Za-z0-9]+", "_", f"{s['ky'][:2]}_{s['name']}")[:80].strip("_")
    wd = os.path.join(WORK, slug)
    shutil.rmtree(wd, ignore_errors=True)
    os.makedirs(wd)
    res = {"bo": f"{s['ky']}/{s['name']}", "title": title_of(s), "notes": []}
    if s["ky"] not in TARGET:
        res["status"] = "SKIP"
        res["notes"].append("HSG — không có đích")
        return res
    # đáp án rời
    dap, key_src, key_mades = None, None, set()
    for k in s["keys"]:
        if k.lower().endswith((".xlsx", ".xls")):
            try:
                import openpyxl
                wb = openpyxl.load_workbook(k, data_only=True)
                for ws in wb.worksheets:
                    for r in ws.iter_rows(values_only=True):
                        for c in r:
                            if re.fullmatch(r"\d{3}", _cell(c)):
                                key_mades.add(_cell(c))
            except Exception:  # noqa: BLE001
                pass
    exam, made = pick_exam(s, key_mades)
    res["file"] = os.path.relpath(exam, SRC)
    res["made"] = made
    exam_docx = to_docx(exam, wd)
    if not exam_docx:
        res["status"] = "LỖI"
        res["notes"].append("không chuyển được .doc")
        return res
    for k in s["keys"]:
        try:
            if k.lower().endswith(".xlsx"):
                dap, key_src = key_from_xlsx(k, made), "xlsx"
            elif k.lower().endswith(".xls"):
                kd = to_docx(k, wd)  # soffice không đổi xls→docx; bỏ qua
                dap = None
            else:
                kd = to_docx(k, wd)
                if kd:
                    dap, key_src = key_from_docx(kd, made), "docx"
                    if not dap or not (dap[1] or dap[3]):
                        dap, note = key_from_ai(docx_dump(kd), made, slug)
                        key_src = "docx→AI"
                        res["notes"].append(note or "")
        except Exception as e:  # noqa: BLE001
            res["notes"].append(f"đọc đáp án {os.path.basename(k)} lỗi: {str(e)[:100]}")
        if dap and (dap[1] or dap[3]):
            break
    if not dap and not s["keys"]:
        key_src = "inline"
        full = docx_dump(exam_docx)
        m = re.search(r"\n[^\n]*(?:H[ẾE]T\s*[-–—=*_.]*\s*\n|ĐÁP ÁN|HƯỚNG DẪN CHẤM)", full)
        tail = full[m.start():] if m else ""
        if len(tail.strip()) > 40:
            dap, note = key_from_ai(tail, made, slug)
            key_src = "inline→AI"
            res["notes"].append(note or "")
            if dap and not (dap[1] or dap[3]):
                dap = None
    res["key"] = key_src
    if dap:
        res["dap_an"] = {"I": len(dap[1]), "II": len(dap[2]), "III": len(dap[3])}
    # ghép + chuỗi azota
    merged = os.path.join(wd, "de_goc.docx")
    try:
        res["notes"] += prepare_exam(exam_docx, merged, dap, cut_tail=bool(dap))
        sc = school_from_doc(Document(exam_docx))
        if sc:
            res["title"] = f"{KY_LABEL[s['ky']]} 2024–2025 – {sc}"[:140]
    except Exception as e:  # noqa: BLE001
        res["status"] = "LỖI"
        res["notes"].append(f"ghép đề lỗi: {str(e)[:150]}")
        return res
    run(["python3", MTEF, "convert", merged])
    c = run(["python3", f"{AZ}/convert_docx.py", merged, f"{wd}/de_azota.docx"])
    open(f"{wd}/convert.log", "w").write(c.stdout + "\n--- stderr ---\n" + c.stderr)
    if c.returncode:
        res["status"] = "LỖI"
        res["notes"].append("convert_docx lỗi: " + c.stderr.strip()[-200:])
        return res
    res["convert"] = [ln for ln in (c.stdout + c.stderr).splitlines() if ln.startswith(("Phần", "[lưu ý]"))]
    # Lưới an toàn: số câu convert_docx đọc được phải khớp số đáp án từng phần — lệch là đáp án sẽ gán sai câu
    if dap:
        got = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r"^Phần (\d): (\d+) câu", c.stdout + c.stderr, re.M)}
        lech = [f"P{k}: đề {got.get(k, 0)} câu / đáp án {len(dap[k])}" for k in (1, 2, 3) if dap[k] and got.get(k, 0) and got.get(k, 0) != len(dap[k])]
        for k in (1, 2, 3):
            if dap[k] and not got.get(k, 0):
                res["notes"].append(f"P{k}: khoá có {len(dap[k])} đáp án nhưng đề không có câu phần này — bỏ qua phần khoá")
        if not got.get(1, 0) and not got.get(2, 0) and not got.get(3, 0):
            lech = ["đề 0 câu (convert_docx không đọc được câu nào)"]
        if lech:
            res["status"] = "LỆCH"
            res["notes"].append("số câu lệch số đáp án — không đăng: " + "; ".join(lech))
            return res
    open(f"{wd}/nhan.json", "w").write("{}")
    x = run(["python3", f"{AZ}/xuat_thachlab.py", f"{wd}/de_azota.docx", f"{wd}/nhan.json", f"{wd}/de_thachlab.docx"])
    open(f"{wd}/xuat.log", "w").write(x.stdout + "\n--- stderr ---\n" + x.stderr)
    if x.returncode or not os.path.exists(f"{wd}/de_thachlab.docx"):
        res["status"] = "LỖI"
        res["notes"].append("xuat_thachlab lỗi: " + x.stderr.strip()[-200:])
        return res
    res["xuat"] = [ln for ln in (x.stdout + x.stderr).splitlines() if ln.startswith("[đề]")][:8]
    lesson, item = TARGET[s["ky"]]
    cmd = ["npx", "tsx", "scripts/upload-exam-docx.mts", f"{wd}/de_thachlab.docx", "--title", res["title"], "--lesson", str(lesson),
           "--item", str(item), "--duration", "45", "--drop-bad", "--min-keep", "10", "--drop-mathtype", "--log", LOG, "--src", res["bo"]]
    if DRY:
        cmd.append("--dry")
    u = run(cmd, cwd=ROOT)
    open(f"{wd}/upload.log", "w").write(u.stdout + "\n--- stderr ---\n" + u.stderr)
    out = [ln for ln in (u.stdout + u.stderr).strip().splitlines() if ln.strip()]
    res["status"] = {0: "OK", 2: "SKIP>20%", 3: "TRÙNG"}.get(u.returncode, "LỖI")
    res["upload"] = out[-3:]
    return res


def main():
    sets = list_sets()
    if "--list" in args:
        for s in sets:
            ex, made = pick_exam(s, set())
            print(f"{s['ky']:12} | {s['name'][:70]:70} | đề:{len(s['exams'])} key:{len(s['keys'])} | {os.path.basename(ex)[:40]} mã {made}")
        print(len(sets), "bộ")
        return
    if "--sets" in args:
        pats = []
        i = args.index("--sets") + 1
        while i < len(args) and not args[i].startswith("--"):
            pats.append(args[i].lower())
            i += 1
        chosen = [s for s in sets if any(p in s["name"].lower() for p in pats)]
    elif "--all" in args:
        chosen = [s for s in sets if s["ky"] in TARGET]
        off, lim = int(opt("--offset", 0)), int(opt("--limit", 10**6))
        chosen = chosen[off:off + lim]
    else:
        print(__doc__)
        return
    log = json.load(open(LOG)) if os.path.exists(LOG) else {}
    done = set(log)
    runres = json.load(open(RUN)) if os.path.exists(RUN) else {}
    os.makedirs(WORK, exist_ok=True)
    for s in chosen:
        bo = f"{s['ky']}/{s['name']}"
        if bo in done and not DRY:
            print("= đã đăng, bỏ qua:", bo)
            continue
        r = process(s, log)
        runres[bo] = r
        print(f"[{r.get('status')}] {bo}\n   → {r.get('title')} | file {os.path.basename(r.get('file', '?'))} mã {r.get('made')} | đáp án {r.get('key')} {r.get('dap_an', '')}")
        for ln in r.get("convert", []) + r.get("xuat", []) + r.get("upload", []) + r.get("notes", []):
            if ln:
                print("     ", ln[:220])
        if not DRY:
            json.dump(runres, open(RUN, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
