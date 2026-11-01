# Khuon chung cho "clip bay" phu dao (chang C, docs/KE-HOACH-MOTION-GRAPHIC.md, 1/11/2026).
# Cau truc 20-30 s: Tinh huong (cau hoi that HS sai nhieu, dung 4-5 s, A.-D. cung mau) -> Dap an -> "Sai vi..." (ve dong
# dung co che) -> Quy tac 1 dong + cau hoi tu nho (chot_hoi cua engine). Clip bay chi import file nay + engine, khong sua engine.
from engine import *

GOLD = (180, 83, 9)


def qcard(d, t, sc, y0, lines, opts, think_at, think_end, reveal=None, kr=0.0, k=1.0, h=None, head="Dự đoán"):
    """The cau hoi: nhan head (1 tu, phu de da noi "chon mot dap an"), 1-3 dong de, 4 lua chon A.-D. CUNG mau/co/kieu, thanh dem tu think_at toi
    think_end. reveal = chi so dap an dung; kr (0..1) to xanh dap an do + lam mo cac lua chon khac."""
    if k <= 0: return
    nq = len(lines); h = h or (110 + nq * 50 + len(opts) * 70 + 40)
    y = y0 + (1 - k) * 40
    card(d, (60, y, 1020, y + h), fill=A(WHITE, k), outline=A(PURPLE, k), w=5)
    text(d, (W / 2, y + 44), head, 38, PURPLE, alpha=k)
    for j, s in enumerate(lines):
        text(d, (W / 2, y + 104 + j * 50), s, 40, INK, alpha=k)
    yo = y + 104 + nq * 50 + 30
    for j, s in enumerate(opts):
        yy = yo + j * 70; good = reveal is not None and j == reveal
        a_opt = k * (1 - 0.6 * kr) if (reveal is not None and not good) else k
        if good and kr > 0:
            d.rounded_rectangle([100, yy - 28, 980, yy + 28], radius=28, fill=A(mix(GREEN, WHITE, 0.85), kr),
                                outline=A(GREEN, kr), width=4)
        else:
            d.rounded_rectangle([100, yy - 28, 980, yy + 28], radius=28, outline=A(LIGHT, a_opt), width=3)
        col = mix(NAVY, GREEN, kr) if good else NAVY
        text(d, (134, yy), f"{'ABCD'[j]}.  {s}", 38, col, bold=good and kr > 0.5, anchor="lm", alpha=a_opt)
        if good and kr > 0: text(d, (950, yy), "✓", 44, GREEN, anchor="rm", alpha=kr)
    q = clamp((t - think_at) / max(0.1, think_end - think_at))
    if reveal is None and t >= think_at - 0.3:
        yb = y + h - 26
        d.rounded_rectangle([140, yb - 5, 940, yb + 5], radius=5, fill=A(LIGHT, k))
        if q < 1: d.rounded_rectangle([140, yb - 5, 140 + 800 * (1 - q), yb + 5], radius=5, fill=A(PURPLE, k))


def badge(d, xr, y, s, color, k, size=34):
    if k <= 0: return
    pw = tw(d, s, F(size)) + 48
    card(d, (xr - pw, y - 30, xr, y + 30), fill=A(color, k), r=30)
    text(d, (xr - pw / 2, y), s, size, WHITE, alpha=k)


def note(d, y, s, color, k, size=42, h=None, sub=None):
    """The mot y (Sai vi... / Dung la...) — chu to, mot dong neu duoc."""
    if k <= 0: return
    ls = wrap(d, s, F(size), 880); h = h or (len(ls) * size * 1.25 + 56 + (50 if sub else 0))
    yy = y + (1 - k) * 30
    card(d, (60, yy, 1020, yy + h), fill=A(WHITE, k), outline=A(color, k), w=5)
    for j, l in enumerate(ls):
        text(d, (W / 2, yy + 28 + size * 0.62 + j * size * 1.25), l, size, color, alpha=k)
    if sub: text(d, (W / 2, yy + h - 40), sub, 36, MUTED, bold=False, alpha=k)


def dash_line(d, p, q, color, w=4, seg=16, gap=12):
    L = math.dist(p, q); n = int(L // (seg + gap)) + 1
    for i in range(n):
        a = i * (seg + gap) / L; b = min(1, (i * (seg + gap) + seg) / L)
        if a >= 1: break
        d.line([(lerp(p[0], q[0], a), lerp(p[1], q[1], a)), (lerp(p[0], q[0], b), lerp(p[1], q[1], b))], fill=color, width=w)


def chevron(d, x, y, ang, color, s=18, w=5):
    """Mui ten chevron 30 do (AGENTS.md: duong suc tu net dut, mui chevron 30 do)."""
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)


def cross_in(d, x, y, r, color, w=6, alpha=1.0):
    """Dong dien di VAO mat phang: vong tron + dau X (font SF khong chac co glyph ⊗)."""
    c = A(color, alpha)
    d.ellipse([x - r, y - r, x + r, y + r], outline=c, width=w)
    e = r * 0.62
    d.line([(x - e, y - e), (x + e, y + e)], fill=c, width=w); d.line([(x - e, y + e), (x + e, y - e)], fill=c, width=w)


def frac(d, cx, cy, top, bot, size=46, color=INK, alpha=1.0, wline=None):
    """Phan so: tu / mau (chuoi rich() co _{} ^{}), gach ngang o cy."""
    f = F(size); wl = wline or max(tw(d, re.sub(r"[_^]\{([^}]*)\}", r"\1", s), f) for s in (top, bot)) + 30
    rich(d, cx, cy - size * 0.72, top, size, color, alpha=alpha)
    d.line([(cx - wl / 2, cy), (cx + wl / 2, cy)], fill=A(color, alpha), width=4)
    rich(d, cx, cy + size * 0.72, bot, size, color, alpha=alpha)
    return wl


def bay_cues(clip):
    """Tieng bao: hien cau hoi (open), het gio nghi (ding), lo dap an (ding), vao 'Sai vi' (buzz), cau tu nho (open)."""
    sc = {s["key"]: s for s in clip["scenes"]}
    h, a, s, e = sc["hoi"], sc["dapan"], sc["saivi"], sc["end"]
    return [(h["t0"] + h["M"][-1], "open"), (h["t0"] + h["T"] - 0.1, "ding"), (a["t0"] + 0.5, "ding"),
            (s["t0"] + s["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]


def answer_pill(d, y, letter, s, k):
    """Canh Dap an: chi mot dong dap an dung (khong lap lai ca the cau hoi -> do chu khong doi gap)."""
    if k <= 0: return
    yy = y + (1 - k) * 30
    d.rounded_rectangle([100, yy - 46, 980, yy + 46], radius=46, fill=A(mix(GREEN, WHITE, 0.85), k), outline=A(GREEN, k), width=5)
    text(d, (150, yy), f"{letter}.  {s}", 46, GREEN, anchor="lm", alpha=k)
    text(d, (940, yy), "✓", 52, GREEN, anchor="rm", alpha=k)
