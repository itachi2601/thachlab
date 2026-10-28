"""Chuyển phần "Nhãn: …" và dòng nguồn OpenStax của <figcaption> ra chú thích lề phải (thầy chốt 28/10/2026).

margin_figs(html): với mỗi <figure> có dòng "Nhãn:" trong figcaption, bỏ legend + nguồn khỏi figcaption, gắn dấu
<sup class="tl-fn"> vào đoạn <p> cấp đầu gần nhất (ngay trước hình, không có thì ngay sau), và đặt
<ol class="tl-fns"> ngay dưới hình. features/lessons/margin-notes.ts đưa chú thích sang lề ≥1280px; màn hẹp thì
nó nằm dưới hình. Không có đoạn <p> hợp lệ thì để nguyên hình (in cảnh báo)."""
import re

FIG = re.compile(r"<figure\b[^>]*>.*?</figure>", re.S)
CAP = re.compile(r"(<figcaption>)(.*?)(</figcaption>)", re.S)
BR = re.compile(r"<br\s*/?>")
BLOCK = re.compile(r"<(/?)(div|table|ul|ol|details|figure|blockquote)\b[^>]*>|<(p|h[1-6])\b[^>]*>|</p>", re.I)


def _top_level_p_end(html: str, pos: int, before: bool):
    """Vị trí ngay trước </p> của đoạn <p> cấp đầu gần pos nhất (phía trước hoặc sau); None nếu không có/lẫn tiêu đề."""
    depth = 0
    found = []  # (start_of_p, end_of_p_close_index)
    for m in BLOCK.finditer(html):
        if m.group(2):
            depth += -1 if m.group(1) else 1
        elif m.group(3) and m.group(3).lower() == "p" and depth == 0:
            end = html.find("</p>", m.start())
            if end > 0:
                found.append((m.start(), end))
    if before:
        c = [f for f in found if f[1] < pos]
        if not c:
            return None
        s, e = c[-1]
        gap = html[e + 4:pos]
    else:
        c = [f for f in found if f[0] > pos]
        if not c:
            return None
        s, e = c[0]
        gap = html[pos:s]
    if re.search(r"<h[1-6]\b|<table\b|<figure\b", gap) or len(gap) > 2500:
        return None
    return e


def margin_figs(html: str) -> str:
    used = set(re.findall(r'id="(tl-fn-[\w-]+)"', html))
    out, cursor, k = [], 0, 0
    for m in FIG.finditer(html):
        fig = m.group(0)
        cm = CAP.search(fig)
        if not cm or "Nhãn" not in cm.group(2):
            continue
        parts = BR.split(cm.group(2))
        # tách "Nhãn:" nằm giữa một dòng (vd. "Mỗi T còn một nửa. Nhãn: …")
        flat = []
        for p in parts:
            i = p.find("Nhãn:")
            if i > 0 and p[:i].strip():
                flat += [p[:i].rstrip(), p[i:]]
            else:
                flat.append(p)
        li = next((i for i, p in enumerate(flat) if "Nhãn:" in p), None)
        ci = next((i for i, p in enumerate(flat) if "Hình: OpenStax" in p), None)
        if li is None or ci is None or ci < li:
            print("  ! bỏ qua (không tách được):", re.sub(r"<[^>]+>", "", cm.group(2))[:60])
            continue
        legend = [re.sub(r"^\s*Nhãn:\s*", "", p).strip() for p in flat[li:ci]]
        credit = [re.sub(r"</?small>", "", p).strip() for p in flat[ci:]]
        keep = flat[:li]
        num = re.match(r"\s*Hình\s+(\d+)", re.sub(r"<[^>]+>", "", cm.group(2)))
        k += 1
        fid = f"tl-fn-h{num.group(1)}" if num else f"tl-fn-h{k}"
        while fid in used:
            fid += "x"
        label = f"H{num.group(1)}" if num else str(k)
        at = _top_level_p_end(html, m.start(), True)
        side = "trước"
        if at is None:
            at = _top_level_p_end(html, m.end(), False)
            side = "sau"
        if at is None:
            print("  ! bỏ qua (không có đoạn <p> cấp đầu cạnh hình):", label)
            continue
        used.add(fid)
        sup = f'<sup class="tl-fn"><a href="#{fid}">{label}</a></sup>'
        note = ('<ol class="tl-fns"><li id="%s"><strong>Nhãn trong hình:</strong> %s<br>%s</li></ol>'
                % (fid, "<br>".join(legend), "<br>".join(credit)))
        newfig = fig[:cm.start()] + cm.group(1) + "<br>".join(keep) + cm.group(3) + fig[cm.end():]
        newfig = newfig + "\n" + note
        if side == "trước":
            out.append((at, 0, sup))
            out.append((m.start(), m.end() - m.start(), newfig))
        else:
            out.append((m.start(), m.end() - m.start(), newfig))
            out.append((at, 0, sup))
    res, last = [], 0
    for pos, ln, txt in sorted(out, key=lambda x: (x[0], x[1] == 0)):
        res.append(html[last:pos]); res.append(txt); last = pos + ln
    res.append(html[last:])
    return "".join(res)
