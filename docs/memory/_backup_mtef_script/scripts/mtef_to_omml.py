#!/usr/bin/env python3
"""
mtef_to_omml.py — chuyen cong thuc MathType (MTEF5/MathType7 va MTEF3/Equation 3.0,
nhung trong OLE oleObjectN.bin cua file .docx) sang OMML (Office Math) goc cua Word,
bang cach giai ma truc tiep du lieu nhi phan MTEF — khong can cai MathType.

Phu thuoc: olefile, lxml  (pip install olefile lxml --break-system-packages)

Cach dung:
    python3 mtef_to_omml.py scan *.docx
        In bang so luong MT7 (Equation.DSMT4/Equation.3) con lai va so OMML da co
        cho tung file. Khong sua gi ca. Dung lam buoc 1 cua skill mathtype-sang-omml.

    python3 mtef_to_omml.py convert *.docx
        Giai ma tung cong thuc MathType OLE va GHI DE THANG len file goc (khong
        backup, khong doi ten — dung theo dung quy dinh cua skill). In bao cao
        MT7 truoc/sau va so OMML cho tung file.

Lich su: viet va test lan dau 25/9/2026 khi chuyen 7 file dau tien cua bo "250+ DE
THI THU THPTQG 2026/Azota" (370/370 cong thuc parse sach, khop khi so sanh anh
render voi WMF goc). Cac quy uoc khong co trong tai lieu MTEF cong khai (o duoi
day) la tu suy ra bang cach doi chieu voi anh WMF that, KHONG phai tu tai lieu
chinh thuc — neu gap file lam sai, xem lai phan tuong ung roi doi chieu WMF gio
truoc khi sua.
"""
import argparse
import glob
import io
import re
import struct
import sys
import zipfile
from xml.sax.saxutils import escape as xesc

try:
    import olefile
except ImportError:
    print("Thieu thu vien olefile. Cai bang: pip install olefile --break-system-packages", file=sys.stderr)
    raise

from lxml import etree


# =====================================================================================
# PHAN 1 — GIAI MA MTEF (MTEF5 / MathType7 va MTEF3 / Equation Editor 3.0)
# =====================================================================================

TAG_NAMES = {
    0: 'END', 1: 'LINE', 2: 'CHAR', 3: 'TMPL', 4: 'PILE', 5: 'MATRIX',
    6: 'EMBELL', 7: 'RULER', 8: 'FONT_STYLE_DEF', 9: 'SIZE', 10: 'FULL',
    11: 'SUB', 12: 'SUB2', 13: 'SYM', 14: 'SUBSYM', 15: 'COLOR',
    16: 'COLOR_DEF', 17: 'FONT_DEF', 18: 'EQN_PREFS', 19: 'ENCODING_DEF',
}


class ParseError(Exception):
    pass


class Reader:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.nib_hi = None  # pending low nibble when mid-byte

    def eof(self):
        return self.pos >= len(self.data)

    def u8(self):
        if self.pos >= len(self.data):
            raise ParseError(f"EOF reading u8 at {self.pos}")
        v = self.data[self.pos]
        self.pos += 1
        return v

    def peek_u8(self):
        if self.pos >= len(self.data):
            return None
        return self.data[self.pos]

    def u16(self):
        if self.pos + 2 > len(self.data):
            raise ParseError(f"EOF reading u16 at {self.pos}")
        v = struct.unpack_from('<H', self.data, self.pos)[0]
        self.pos += 2
        return v

    def i16(self):
        v = self.u16()
        return v - 65536 if v >= 32768 else v

    def cstr(self):
        start = self.pos
        end = self.data.index(0, start)
        s = self.data[start:end].decode('latin-1')
        self.pos = end + 1
        return s

    def bytes_(self, n):
        v = self.data[self.pos:self.pos + n]
        self.pos += n
        return v

    # ---- nibble access, used only inside EQN_PREFS dimension arrays ----
    def read_nibble(self):
        if self.nib_hi is None:
            b = self.u8()
            self.nib_hi = b & 0x0F
            return (b >> 4) & 0x0F
        else:
            v = self.nib_hi
            self.nib_hi = None
            return v

    def align_nibble(self):
        self.nib_hi = None


def skip_dimension(r):
    """A MathType 'dimension' in EQN_PREFS is a run of nibbles (unit nibble +
    optional digit nibbles) terminated by nibble 0xF. We never need the value,
    only need to consume it correctly to keep byte alignment for what follows."""
    while True:
        if r.read_nibble() == 0xF:
            break


def parse_eqn_prefs(r):
    r.u8()  # options byte
    for _ in range(2):  # two dimension arrays
        count = r.u8()
        for _ in range(count):
            skip_dimension(r)
        r.align_nibble()
    style_count = r.u8()
    styles = []
    for _ in range(style_count):
        font_index = r.u8()
        char_style = r.u8()
        styles.append((font_index, char_style))
    return styles


def parse_header_and_prefs(data, version):
    r = Reader(data)
    styles = []
    if version == 5:
        r.u8(); r.u8(); r.u8(); r.u8(); r.u8()  # ver, platform, product, version, subversion
        r.cstr()  # app key e.g. "DSMT6"/"DSMT7"
        r.u8()  # 1 optional byte
        while True:
            t = r.peek_u8()
            if t == 0x13:  # ENCODING_DEF
                r.u8(); r.cstr()
            elif t == 0x11:  # FONT_DEF
                r.u8(); r.u8(); r.cstr()
            elif t == 0x10:  # COLOR_DEF
                r.u8(); r.u16(); r.u16(); r.u16(); r.cstr()
            elif t == 0x12:
                break
            else:
                # Proprietary/unknown extension record seen before EQN_PREFS
                # (observed with MathType's TeX/LaTeX-source translator
                # metadata: tag 0x66). Format: [tag][1-byte length][payload].
                # Content unused; only skip length matters for alignment.
                r.u8()
                ln = r.u8()
                r.bytes_(ln)
        tag = r.u8()
        if tag != 0x12:
            raise ParseError(f"expected EQN_PREFS(0x12), got {tag:#x} at {r.pos}")
        styles = parse_eqn_prefs(r)
    elif version == 3:
        r.pos = 5  # MTEF3: no ENCODING_DEF/FONT_DEF/EQN_PREFS; body starts at offset 5
    else:
        raise ParseError(f"unsupported MTEF version {version}")
    return r, styles


class Rec:
    __slots__ = ('tag', '__dict__')

    def __init__(self, tag, **kw):
        self.tag = tag
        self.__dict__.update(kw)

    def __repr__(self):
        d = {k: v for k, v in self.__dict__.items() if k != 'tag'}
        return f"{TAG_NAMES.get(self.tag, self.tag)}({d})"


def read_nudge(r, options):
    if options & 0x08:
        b1 = r.u8(); b2 = r.u8()
        if b1 == 128 and b2 == 128:
            r.i16(); r.i16()


def parse_records_until_end(r, mtef_version):
    recs = []
    while True:
        if r.eof():
            break
        tag = r.u8()
        if tag == 0:
            break
        recs.append(parse_record(r, tag, mtef_version))
    return recs


def map_tmpl_selector(sel, mtef_version):
    if mtef_version == 3:
        # MTEF3 uses different selector numbers for the same templates.
        mapping = {14: 11, 15: 29, 1: 1, 13: 10}
        return mapping.get(sel, sel)
    return sel


def parse_record(r, tag, mtef_version):
    name = TAG_NAMES.get(tag)

    if name == 'LINE':
        options = r.u8()
        read_nudge(r, options)
        empty = bool(options & 0x01)
        children = [] if empty else parse_records_until_end(r, mtef_version)
        return Rec(tag, kind='LINE', options=options, children=children)

    if name == 'CHAR':
        if mtef_version == 3:
            typeface = r.u8()
            mtcode = r.u16()
            return Rec(tag, kind='CHAR', typeface=typeface, mtcode=mtcode,
                       extra_char=None, extra_u16=None, embell=[])
        options = r.u8()
        read_nudge(r, options)
        typeface = r.u8()
        mtcode = None
        if not (options & 0x20):
            mtcode = r.u16()
        extra_char = r.u8() if (options & 0x04) else None
        extra_u16 = r.u16() if (options & 0x10) else None
        embell = parse_records_until_end(r, mtef_version) if (options & 0x01) else []
        return Rec(tag, kind='CHAR', typeface=typeface, mtcode=mtcode,
                   extra_char=extra_char, extra_u16=extra_u16, embell=embell)

    if name == 'TMPL':
        if mtef_version == 3:
            sel = r.u8(); var = r.u8(); options = r.u8()
        else:
            options = r.u8()
            read_nudge(r, options)
            sel = r.u8()
            var = r.u8()
            if var & 0x80:
                var = (var, r.u8())
            options = r.u8()
        sel = map_tmpl_selector(sel, mtef_version)
        slots = []
        while True:
            if r.eof():
                break
            t = r.u8()
            if t == 0:
                break
            slots.append(parse_record(r, t, mtef_version))
        return Rec(tag, kind='TMPL', selector=sel, variation=var, options=options, slots=slots)

    if name == 'PILE':
        options = r.u8()
        read_nudge(r, options)
        halign = r.u8(); valign = r.u8()
        lines = []
        while True:
            if r.eof():
                break
            t = r.u8()
            if t == 0:
                break
            lines.append(parse_record(r, t, mtef_version))
        return Rec(tag, kind='PILE', halign=halign, valign=valign, lines=lines)

    if name == 'MATRIX':
        # Not seen in the corpus this was built against — best-effort so it
        # never crashes; verify visually if this path ever actually triggers.
        options = r.u8()
        read_nudge(r, options)
        rows = r.u8(); cols = r.u8()
        r.u8(); r.u8(); r.u8(); r.u8(); r.u8()  # valign,halign,vspacing,hspacing,parts
        cells = []
        for _ in range(rows * cols):
            t = r.u8()
            cells.append(None if t == 0 else parse_record(r, t, mtef_version))
        return Rec(tag, kind='MATRIX', rows=rows, cols=cols, cells=cells)

    if name == 'EMBELL':
        options = r.u8()
        read_nudge(r, options)
        code = r.u8()
        return Rec(tag, kind='EMBELL', code=code)

    if name == 'FONT_STYLE_DEF':
        return Rec(tag, kind='FONT_STYLE_DEF', idx=r.u8())

    if name == 'SIZE':
        v = r.u8()
        extra = r.i16() if v == 100 else None
        return Rec(tag, kind='SIZE', v=v, extra=extra)

    if name in ('FULL', 'SUB', 'SUB2', 'SYM', 'SUBSYM'):
        return Rec(tag, kind=name)

    if name == 'COLOR':
        return Rec(tag, kind='COLOR', idx=r.u8())

    if name == 'RULER':
        return Rec(tag, kind='RULER')

    if name == 'COLOR_DEF':
        r.u16(); r.u16(); r.u16(); r.cstr()
        return Rec(tag, kind='COLOR_DEF')

    if name == 'FONT_DEF':
        idx = r.u8(); nm = r.cstr()
        return Rec(tag, kind='FONT_DEF', idx=idx, name=nm)

    if name == 'ENCODING_DEF':
        r.cstr()
        return Rec(tag, kind='ENCODING_DEF')

    if name == 'EQN_PREFS':
        parse_eqn_prefs(r)
        return Rec(tag, kind='EQN_PREFS')

    raise ParseError(f"unhandled tag {tag} ({name}) at pos {r.pos}")


def parse_mtef(data):
    """data: bytes of the 'Equation Native' OLE stream WITHOUT the 28-byte
    EQNOLEFILEHDR (i.e. data[0] must be the MTEF version byte, 3 or 5)."""
    version = data[0]
    r, styles = parse_header_and_prefs(data, version)
    top = parse_records_until_end(r, version)
    # Top level can carry more than one END(0)-terminated row-group in a row
    # (e.g. a watermark text run appended as a second "row" right after the
    # visible formula, or a lone empty group). Keep consuming these
    # soft-separated groups until true EOF instead of leaving valid trailing
    # records unparsed -- a genuine desync still raises inside
    # parse_records_until_end itself.
    while not r.eof():
        top.extend(parse_records_until_end(r, version))
    return {'version': version, 'styles': styles, 'top': top, 'trailing': data[r.pos:]}


# =====================================================================================
# PHAN 2 — SINH OMML TU CAY DA GIAI MA
# =====================================================================================

OMML_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

# typeface (0x80 + slot so) -> kieu chu toan hoc co ban, cua 8 slot chuan cua
# MathType. Da kiem chung bang cach render anh WMF that cua cong thuc trong bo
# "250+ DE THI THU 2026": Variable(3)=nghieng, Vector(7)=dam; CA chu Hy Lap
# thuong/hoa deu DUNG (khong nghieng) — kiem tra qua ky tu mu, Delta.
BASE_STYLE = {
    0x81: 'p',  # Text
    0x82: 'p',  # Function
    0x83: 'i',  # Variable
    0x84: 'p',  # LC Greek
    0x85: 'p',  # UC Greek
    0x86: 'p',  # Symbol
    0x87: 'b',  # Vector-Matrix
    0x88: 'p',  # Number
}

MT_EXTRA_SPACE = 0xEF02


def style_for_typeface(typeface, styles):
    idx = typeface - 0x80
    if typeface in BASE_STYLE:
        base = BASE_STYLE[typeface]
        bold = base in ('b', 'bi')
        italic = base in ('i', 'bi')
    else:
        # Custom/extended style slot (typeface >= 0x89) beyond the 8 standard
        # ones — there is no fixed typographic convention here, only what the
        # per-equation EQN_PREFS style table says.
        bold = italic = False
    if 0 <= idx < len(styles):
        _, char_style = styles[idx]
        # char_style bits are ADDITIVE overrides on top of the slot's base
        # convention (0 == "no override", not "force upright/non-bold").
        if char_style & 0x01:
            bold = True
        if char_style & 0x02:
            italic = True
    elif typeface not in BASE_STYLE:
        italic = True  # unknown extended style with no table entry: italic is the safer default
    if bold and italic:
        return 'bi'
    if bold:
        return 'b'
    if italic:
        return 'i'
    return 'p'


def char_text(rec):
    """Unicode text this CHAR record contributes to running text, or None to skip."""
    tf = rec.typeface
    code = rec.mtcode
    if code is None:
        code = rec.extra_u16 if rec.extra_u16 is not None else rec.extra_char
    if code is None:
        return None
    if tf == 0x96:
        return None  # template glyph marker (bracket/accent piece) — never emits text directly
    if tf == 0x98:  # "MT Extra" symbol font
        if code == MT_EXTRA_SPACE:
            return ' '
        if 0xEF00 <= code <= 0xEFFF:
            return None
        return chr(code)
    try:
        return chr(code)
    except (ValueError, OverflowError):
        return None


MARKER_KINDS = {'FULL', 'SUB', 'SUB2', 'SYM', 'SUBSYM', 'COLOR', 'COLOR_DEF',
                'FONT_DEF', 'ENCODING_DEF', 'EQN_PREFS', 'RULER', 'FONT_STYLE_DEF', 'SIZE'}


def is_marker(rec):
    # These carry no renderable content of their own; in real MTEF streams they
    # show up as slot-role placeholders (SUB/SUB2/FULL/SYM/SUBSYM) or as
    # inline formatting state changes (COLOR/COLOR_DEF/...) mixed into a
    # LINE's children list or a TMPL's own slot list. Color is intentionally
    # NOT reproduced (cosmetic-only limitation, see module docstring/SKILL.md).
    return rec.kind in MARKER_KINDS


def is_empty_line(rec):
    return rec.kind == 'LINE' and (bool(rec.options & 0x01) or len(rec.children) == 0)


def run_xml(text, sty):
    if text == '':
        return ''
    rpr = f'<m:rPr><m:sty m:val="{sty}"/></m:rPr>'
    return f'<m:r>{rpr}<m:t xml:space="preserve">{xesc(text)}</m:t></m:r>'


class Ctx:
    def __init__(self, styles):
        self.styles = styles


def render_line(line_rec, ctx):
    if line_rec is None:
        return ''
    if line_rec.kind == 'LINE':
        return render_children(line_rec.children, ctx)
    return render_children([line_rec], ctx)


def render_children(children, ctx):
    atoms = [c for c in children if c is not None and not is_marker(c)]

    out = []
    pending_text = []
    pending_sty = [None]  # boxed so the nested closures below can mutate it

    def flush_text():
        if pending_text:
            txt = ''.join(t for t, _ in pending_text)
            out.append(run_xml(txt, pending_sty[0]))
            pending_text.clear()
        pending_sty[0] = None

    def pop_last_char_as_base():
        """Sub/sup templates take the immediately preceding element as base;
        if that element is a multi-character run, split its LAST character
        off as the base (per skill note)."""
        if pending_text:
            last_text, last_sty = pending_text[-1]
            if len(last_text) > 1:
                pending_text[-1] = (last_text[:-1], last_sty)
                return run_xml(last_text[-1], last_sty)
            pending_text.pop()
            if not pending_text:
                pending_sty[0] = None
            return run_xml(last_text, last_sty)
        if out:
            return out.pop()
        return ''

    i = 0
    n = len(atoms)
    while i < n:
        rec = atoms[i]

        if rec.kind == 'CHAR':
            text = char_text(rec)
            if text is None:
                i += 1
                continue
            sty = style_for_typeface(rec.typeface, ctx.styles)
            if pending_text and pending_sty[0] == sty:
                pending_text.append((text, sty))
            else:
                flush_text()
                pending_text.append((text, sty))
                pending_sty[0] = sty
            # Character-level embellishments (accents attached to a single
            # char via rec.embell, e.g. prime) could not be reliably mapped
            # from the sample data available (see SKILL.md limitations) —
            # intentionally skipped rather than guessed.
            i += 1
            continue

        if rec.kind == 'TMPL':
            sel = rec.selector
            if sel in (27, 28):  # postfix subscript / superscript
                base = pop_last_char_as_base()
                flush_text()
                content = render_sub_or_sup_content(rec, ctx)
                if sel == 27:
                    out.append(f'<m:sSub><m:e>{base}</m:e><m:sub>{content["sub"]}</m:sub></m:sSub>')
                else:
                    out.append(f'<m:sSup><m:e>{base}</m:e><m:sup>{content["sup"]}</m:sup></m:sSup>')
                i += 1
                continue
            if sel == 29:  # PRE-sub+sup (nuclear/isotope notation: base follows, not precedes)
                flush_text()
                content = render_sub_or_sup_content(rec, ctx)
                base = ''
                j = i + 1
                if j < n:
                    base = render_atom_as_base(atoms[j], ctx)
                    i = j + 1
                else:
                    i += 1
                out.append(f'<m:sPre><m:sub>{content["sub"]}</m:sub><m:sup>{content["sup"]}</m:sup><m:e>{base}</m:e></m:sPre>')
                continue
            flush_text()
            out.append(render_tmpl_self_contained(rec, ctx))
            i += 1
            continue

        if rec.kind == 'PILE':
            flush_text()
            out.append(render_pile(rec, ctx))
            i += 1
            continue

        if rec.kind == 'MATRIX':
            flush_text()
            out.append(render_matrix(rec, ctx))
            i += 1
            continue

        i += 1  # unknown atom kind: skip defensively

    flush_text()
    return ''.join(out)


def render_atom_as_base(rec, ctx):
    if rec.kind == 'CHAR':
        text = char_text(rec)
        if text is None:
            return ''
        return run_xml(text, style_for_typeface(rec.typeface, ctx.styles))
    if rec.kind == 'LINE':
        return render_line(rec, ctx)
    if rec.kind == 'TMPL':
        return render_tmpl_self_contained(rec, ctx)
    if rec.kind == 'PILE':
        return render_pile(rec, ctx)
    if rec.kind == 'MATRIX':
        return render_matrix(rec, ctx)
    return ''


def render_sub_or_sup_content(tmpl_rec, ctx):
    """selector 27 (sub), 28 (sup), 29 (pre sub+sup): collect the meaningful
    (non-empty) LINE slots, in order. MTEF pads sub-only/sup-only templates
    with an extra empty LINE placeholder for the unused role, and precedes
    slots with a marker tag (SUB/SUB2/...) that carries no data of its own —
    both are already filtered out here (markers by kind, empties by flag)."""
    lines = [s for s in tmpl_rec.slots if s is not None and s.kind == 'LINE' and not is_empty_line(s)]
    sel = tmpl_rec.selector
    if sel == 27:
        return {'sub': render_line(lines[0], ctx) if lines else '', 'sup': ''}
    if sel == 28:
        return {'sub': '', 'sup': render_line(lines[-1], ctx) if lines else ''}
    sub = render_line(lines[0], ctx) if len(lines) >= 1 else ''
    sup = render_line(lines[1], ctx) if len(lines) >= 2 else ''
    return {'sub': sub, 'sup': sup}


DELIM_SELECTORS = {1, 2, 3, 4}


def render_tmpl_self_contained(rec, ctx):
    sel = rec.selector
    slots = [s for s in rec.slots if s is not None]

    if sel in DELIM_SELECTORS:
        return render_delimiter(rec, ctx)

    if sel == 10:  # radical (sqrt / nth root)
        content_slots = [s for s in slots if s.kind in ('LINE', 'PILE')]
        body = content_slots[0] if len(content_slots) >= 1 else None
        index = content_slots[1] if len(content_slots) >= 2 else None
        body_xml = render_line(body, ctx)
        if index is None or is_empty_line(index):
            return (f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>'
                    f'<m:deg></m:deg><m:e>{body_xml}</m:e></m:rad>')
        return f'<m:rad><m:deg>{render_line(index, ctx)}</m:deg><m:e>{body_xml}</m:e></m:rad>'

    if sel == 11:  # fraction (slots list may contain a stray FULL marker between num/den)
        content_slots = [s for s in slots if s.kind in ('LINE', 'PILE')]
        num = content_slots[0] if len(content_slots) >= 1 else None
        den = content_slots[1] if len(content_slots) >= 2 else None
        return f'<m:f><m:num>{render_line(num, ctx)}</m:num><m:den>{render_line(den, ctx)}</m:den></m:f>'

    if sel in (13, 31):  # accent: bar/overline, or vector-arrow (or any other explicit glyph)
        return render_accent(rec, ctx)

    if sel == 14:  # arrow with an annotation above it (rare; best-effort — see SKILL.md)
        return render_arrow_annotation(rec, ctx)

    # Unknown selector: best-effort fallback so content is never silently
    # dropped, without claiming a specific visual shape. If this ever
    # triggers on real input, render-compare against the WMF to find out
    # what it actually is and add a proper handler above.
    parts = []
    for s in slots:
        if s.kind in ('LINE', 'PILE'):
            parts.append(render_line(s, ctx))
        elif s.kind == 'CHAR':
            parts.append(render_atom_as_base(s, ctx))
    return ''.join(parts)


def render_delimiter(rec, ctx):
    """selector 1/2/3 = ( ) / { } / [ ] ; selector 4 = absolute-value bars.
    variation bit0 = show left glyph, bit1 = show right glyph (a system of
    equations uses a one-sided '{' with bit1 clear). The actual glyph
    characters are given as trailing CHAR(typeface=0x96) records inside the
    template's own slot list — except selector 4, whose two glyphs are
    growing-bracket PUA pieces (not literal '|'); we always render those as
    a plain '|' since that's what they visually are in every sample seen."""
    var = rec.variation
    if isinstance(var, tuple):
        var = var[0]
    show_left = bool(var & 0x01)
    show_right = bool(var & 0x02)

    body = None
    glyphs = []
    for s in rec.slots:
        if s is None:
            continue
        if s.kind in ('LINE', 'PILE') and body is None:
            body = s
        elif s.kind == 'CHAR':
            glyphs.append(s)

    if rec.selector == 4:
        beg_chr, end_chr = '|', '|'
    else:
        beg_chr = chr(glyphs[0].mtcode) if len(glyphs) >= 1 and glyphs[0].mtcode else ''
        end_chr = chr(glyphs[1].mtcode) if len(glyphs) >= 2 and glyphs[1].mtcode else (
            chr(glyphs[0].mtcode) if len(glyphs) == 1 and not show_left and show_right and glyphs[0].mtcode else '')
        if not show_left:
            beg_chr = ''
        if not show_right:
            end_chr = ''

    content = render_pile(body, ctx) if (body is not None and body.kind == 'PILE') else render_line(body, ctx)
    beg_attr = xesc(beg_chr) if beg_chr else ''
    end_attr = xesc(end_chr) if end_chr else ''
    return (f'<m:d><m:dPr><m:begChr m:val="{beg_attr}"/><m:endChr m:val="{end_attr}"/>'
            f'<m:grow m:val="1"/></m:dPr><m:e>{content}</m:e></m:d>')


def render_pile(pile_rec, ctx):
    """A PILE (vertical stack of LINEs) — used standalone for a multi-line
    worked solution, or nested inside a delimiter for a system of equations."""
    if pile_rec is None:
        return ''
    rows = []
    for line in pile_rec.lines:
        if line is None or line.kind != 'LINE':
            continue
        rows.append(f'<m:e>{render_line(line, ctx)}</m:e>')
    return f'<m:eqArr>{"".join(rows)}</m:eqArr>'


def render_matrix(rec, ctx):
    # Not observed in the corpus this was built against — best-effort so we
    # never crash. Verify visually (render-compare vs WMF) before trusting
    # this on real input.
    cols = rec.cols or 1
    rows_xml = []
    for r0 in range(rec.rows):
        row_cells = rec.cells[r0 * cols:(r0 + 1) * cols]
        row_xml = ''.join(f'<m:e>{render_atom_as_base(c, ctx) if c else ""}</m:e>' for c in row_cells)
        rows_xml.append(f'<m:mr>{row_xml}</m:mr>')
    return f'<m:m>{"".join(rows_xml)}</m:m>'


def render_accent(rec, ctx):
    """selector 13 and 31 both turned out to be the same underlying
    'accent' template in practice: if the slot list has a trailing
    CHAR(typeface=0x96) glyph, that glyph IS the accent character to draw
    (e.g. U+20D7 combining right arrow above -> vector); if there's no such
    glyph, it's MathType's plain bar/overline accent (selector 13, var=0 in
    every sample seen)."""
    slots = [s for s in rec.slots if s is not None]
    body = None
    glyph = None
    for s in slots:
        if s.kind == 'LINE' and body is None:
            body = s
        elif s.kind == 'CHAR' and s.typeface == 0x96:
            glyph = s
    content = render_line(body, ctx)
    if glyph is not None and glyph.mtcode:
        return f'<m:acc><m:accPr><m:chr m:val="{xesc(chr(glyph.mtcode))}"/></m:accPr><m:e>{content}</m:e></m:acc>'
    return f'<m:bar><m:barPr><m:pos m:val="top"/></m:barPr><m:e>{content}</m:e></m:bar>'


def render_arrow_annotation(rec, ctx):
    """selector 14: an arrow (base = CHAR typeface 0x96) with a caption above
    it, e.g. a reaction/process arrow with conditions written above. Only
    ever seen once in the corpus this was built against — treated as
    m:limUpp (centered caption above the base), which matched the WMF render
    in that one sample. If a caption BELOW the arrow ever shows up in real
    input, this will currently drop it; check by render-comparing vs WMF."""
    slots = [s for s in rec.slots if s is not None]
    base = None
    annotation = None
    for s in slots:
        if s.kind == 'CHAR':
            base = s
        elif s.kind == 'LINE' and not is_empty_line(s) and annotation is None:
            annotation = s
    if base is not None and base.kind == 'CHAR' and base.mtcode:
        base_xml = run_xml(chr(base.mtcode), 'p')
    else:
        base_xml = render_atom_as_base(base, ctx) if base else ''
    if annotation is None:
        return base_xml
    return f'<m:limUpp><m:e>{base_xml}</m:e><m:lim>{render_line(annotation, ctx)}</m:lim></m:limUpp>'


def build_omath(tree):
    ctx = Ctx(tree['styles'])
    parts = []
    for rec in tree['top']:
        parts.append(render_line(rec, ctx) if rec.kind == 'LINE' else render_atom_as_base(rec, ctx))
    return f'<m:oMath>{"".join(parts)}</m:oMath>'


# =====================================================================================
# PHAN 3 — AP DUNG VAO FILE .DOCX (doc oleObjectN.bin, ghep qua .rels, thay
# <w:object> bang <m:oMath>, giu nguyen moi phan khac cua zip)
# =====================================================================================

NSW = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NSO = '{urn:schemas-microsoft-com:office:office}'
NSR = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

# Cac phan co the chua cong thuc, ngoai word/document.xml. 7 file dau tien
# (25/9/2026) khong dung phan nao trong so nay, nhung header/footer/footnote
# co the co o file khac trong lo 141 file con lai — nen van xu ly day du.
CANDIDATE_PART_GLOBS = (
    'word/document.xml',
    'word/header*.xml',
    'word/footer*.xml',
    'word/footnotes.xml',
    'word/endnotes.xml',
)


class ConvertResult:
    def __init__(self):
        self.total_objects = 0
        self.converted = 0
        self.errors = []  # list of (part, target, message)


def load_rels(z, part_name):
    d, base = part_name.rsplit('/', 1)
    rels_path = f'{d}/_rels/{base}.rels'
    try:
        data = z.read(rels_path)
    except KeyError:
        return {}
    root = etree.fromstring(data)
    return {rel.get('Id'): rel.get('Target') for rel in root}


def resolve_target(part_name, target):
    if target.startswith('/'):
        return target.lstrip('/')
    return part_name.rsplit('/', 1)[0] + '/' + target


def convert_equation_bytes(raw_ole_bytes):
    """raw_ole_bytes: full contents of one oleObjectN.bin (an OLE compound
    file). Returns an '<m:oMath>...</m:oMath>' XML string, or raises."""
    o = olefile.OleFileIO(io.BytesIO(raw_ole_bytes))
    if not o.exists('Equation Native'):
        raise ValueError('no Equation Native stream (not a MathType OLE object)')
    data = o.openstream('Equation Native').read()
    body = data[28:]  # strip EQNOLEFILEHDR
    if not body or body[0] not in (3, 5):
        raise ValueError(f'unsupported MTEF version byte {body[0] if body else None}')
    tree = parse_mtef(body)
    if len(tree['trailing']) != 0:
        raise ValueError(f'{len(tree["trailing"])} trailing bytes left after parse (likely a parser desync)')
    return build_omath(tree)


def patch_part_xml(xml_bytes, z, part_name, result):
    root = etree.fromstring(xml_bytes)
    changed = False
    rels = load_rels(z, part_name)

    for obj in list(root.iter(f'{NSW}object')):
        ole_el = obj.find(f'{NSO}OLEObject')
        if ole_el is None:
            continue
        if 'Equation' not in ole_el.get('ProgID', ''):
            continue  # some other embedded object type (e.g. a real OLE spreadsheet) — leave untouched
        result.total_objects += 1
        ole_rid = ole_el.get(f'{NSR}id')
        target = rels.get(ole_rid)
        if not target:
            result.errors.append((part_name, f'rid={ole_rid}', 'no rels target found'))
            continue
        bin_path = resolve_target(part_name, target)
        try:
            omath_xml = convert_equation_bytes(z.read(bin_path))
        except Exception as e:
            result.errors.append((part_name, bin_path, f'{type(e).__name__}: {e}'))
            continue

        run = obj
        while run is not None and run.tag != f'{NSW}r':
            run = run.getparent()
        if run is None:
            result.errors.append((part_name, bin_path, 'no enclosing w:r found'))
            continue
        parent = run.getparent()
        idx = list(parent).index(run)

        wrapped = omath_xml.replace('<m:oMath>', f'<m:oMath xmlns:m="{OMML_NS}">', 1)
        try:
            new_el = etree.fromstring(wrapped.encode('utf-8'))
        except etree.XMLSyntaxError as e:
            result.errors.append((part_name, bin_path, f'generated OMML not well-formed: {e}'))
            continue

        new_el.tail = run.tail
        parent.remove(run)
        parent.insert(idx, new_el)
        result.converted += 1
        changed = True

    if not changed:
        return xml_bytes, False
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), True


def convert_docx(src_path, dst_path, result=None):
    """Convert every MathType OLE equation in src_path and write the result
    to dst_path (dst_path may equal src_path to overwrite in place — the
    whole source is buffered in memory first, so this is safe)."""
    if result is None:
        result = ConvertResult()

    with open(src_path, 'rb') as f:
        src_bytes = f.read()
    zin = zipfile.ZipFile(io.BytesIO(src_bytes))
    names = set(zin.namelist())

    target_parts = set()
    for pattern in CANDIDATE_PART_GLOBS:
        if '*' in pattern:
            target_parts.update(n for n in names if re.fullmatch(pattern.replace('*', r'\d+'), n))
        elif pattern in names:
            target_parts.add(pattern)

    new_parts = {}
    for name in target_parts:
        data = zin.read(name)
        new_data, changed = patch_part_xml(data, zin, name, result)
        if changed:
            new_parts[name] = new_data

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            zout.writestr(item, new_parts.get(item.filename, zin.read(item.filename)))

    with open(dst_path, 'wb') as f:
        f.write(buf.getvalue())
    return result


# =====================================================================================
# PHAN 4 — CLI
# =====================================================================================

def scan_file(path):
    z = zipfile.ZipFile(path)
    mt7 = omml_ct = 0
    for n in z.namelist():
        if n.endswith('.xml') and any(k in n for k in ('document', 'header', 'footer', 'footnote', 'endnote')):
            x = z.read(n).decode('utf8', 'ignore')
            mt7 += len(re.findall(r'Equation\.DSMT4|Equation\.3', x))
            omml_ct += len(re.findall(r'<m:oMath[ >]', x))
            omml_ct += len(re.findall(r'<m:oMath/>', x))  # self-closing (empty) form, if any
    return mt7, omml_ct


def cmd_scan(paths):
    print(f"{'MT7':>5}  {'OMML':>5}  file")
    for p in paths:
        try:
            mt7, omml_ct = scan_file(p)
        except Exception as e:
            print(f"{'ERR':>5}  {'ERR':>5}  {p}  ({type(e).__name__}: {e})")
            continue
        print(f"{mt7:5d}  {omml_ct:5d}  {p}")


def cmd_convert(paths):
    any_errors = False
    for p in paths:
        mt7_before, omml_before = scan_file(p)
        result = ConvertResult()
        try:
            convert_docx(p, p, result)
        except Exception as e:
            print(f"=== {p} ===\n  LOI KHONG CHUYEN DUOC FILE: {type(e).__name__}: {e}")
            any_errors = True
            continue
        mt7_after, omml_after = scan_file(p)
        print(f"=== {p} ===")
        print(f"  MT7: {mt7_before} -> {mt7_after}   OMML: {omml_before} -> {omml_after}"
              f"   (objects_found={result.total_objects}, converted={result.converted})")
        if mt7_after != 0:
            print(f"  CANH BAO: con {mt7_after} MT7 chua chuyen duoc (xem loi ben duoi neu co).")
            any_errors = True
        for e in result.errors:
            print(f"  ERR: {e}")
            any_errors = True
    if any_errors:
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p_scan = sub.add_parser('scan', help='Quet MT7/OMML, khong sua gi ca')
    p_scan.add_argument('files', nargs='+')
    p_conv = sub.add_parser('convert', help='Giai ma va GHI DE THANG len tung file (khong backup)')
    p_conv.add_argument('files', nargs='+')
    args = ap.parse_args()

    # Cho phep shell chua expand duoc glob (vd goi tu noi khac voi dau ngoac kep).
    paths = []
    for pat in args.files:
        expanded = glob.glob(pat)
        paths.extend(expanded if expanded else [pat])

    if args.cmd == 'scan':
        cmd_scan(paths)
    elif args.cmd == 'convert':
        cmd_convert(paths)


if __name__ == '__main__':
    main()
