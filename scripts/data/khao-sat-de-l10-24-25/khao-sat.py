import os, re, sys, zipfile, json, collections
SRC = sys.argv[1]
rows = []
def text_of(z):
    try: x = z.read('word/document.xml').decode('utf8','ignore')
    except KeyError: return ''
    x = re.sub(r'</w:p>', '\n', x)
    return re.sub(r'<[^>]+>', '', x)
for root, dirs, files in os.walk(SRC):
    for f in files:
        if f.startswith('~$') or f.startswith('.'): continue
        p = os.path.join(root, f); ext = f.rsplit('.',1)[-1].lower()
        rel = os.path.relpath(p, SRC); top = rel.split('/')[0]
        r = dict(rel=rel, top=top, ext=ext, size=os.path.getsize(p), dir=os.path.dirname(rel))
        name = f.lower()
        r['role'] = ('key' if re.search(r'dap[\s_-]*an|đáp[\s_-]*án|hdc|huong dan cham|hướng dẫn chấm', name) else
                     'matrix' if re.search(r'ma[\s_-]*tr[aậ]n|dac ta|đặc tả|mt\+|bang dac', name) else 'exam')
        r['made'] = bool(re.search(r'(ma[_\s-]*de|mã|made|^\d{3}\b|^de \d{3}|^đề \d|de \d{3}|mđ|-de \d|đề \d\b|_\d{3}_)', name))
        r['goc'] = bool(re.search(r'g[oố]c', name))
        if ext == 'docx':
            try:
                z = zipfile.ZipFile(p); names = z.namelist()
                r['media'] = sum(1 for n in names if n.startswith('word/media/'))
                r['ole'] = sum(1 for n in names if n.startswith('word/embeddings/'))
                r['omml'] = z.read('word/document.xml').count(b'<m:oMath')
                t = text_of(z)
                r['phan'] = [bool(re.search(k, t, re.I)) for k in (r'PH[AẦ]N\s*I\b', r'PH[AẦ]N\s*II\b', r'PH[AẦ]N\s*III\b')]
                r['tuluan'] = bool(re.search(r'T[ỰU]\s*LU[ẬA]N', t, re.I))
                nums = [int(m) for m in re.findall(r'(?:^|\n)\s*C[âa]u\s*(\d{1,2})\s*[.:]', t)]
                r['ncau'] = max(nums) if nums else 0
                r['star'] = len(re.findall(r'\*\s*[A-D]\s*[.:]|[A-D]\s*[.:]\s*\*', t))
                r['dapan_section'] = bool(re.search(r'(ĐÁP ÁN|Đáp án|HƯỚNG DẪN CHẤM|BẢNG ĐÁP ÁN)', t))
                r['loigiai'] = len(re.findall(r'(Lời giải|Hướng dẫn giải|Giải:)', t))
                r['chude'] = bool(re.search(r'Chủ đề\s*:', t))
                r['hinh'] = len(re.findall(r'(hình vẽ|đồ thị|hình bên|sơ đồ|như hình)', t, re.I))
            except Exception as e: r['err'] = str(e)[:60]
        rows.append(r)
json.dump(rows, open(sys.argv[2],'w'), ensure_ascii=False, indent=0)
C = collections.Counter
docx = [r for r in rows if r['ext']=='docx' and 'ncau' in r]
exams = [r for r in docx if r['role']=='exam']
print('tổng file', len(rows), '| docx', len(docx), '| docx vai trò:', C(r['role'] for r in docx))
print('đề docx: ncau>0', sum(1 for r in exams if r['ncau']>0), '| có Phần I/II/III đủ', sum(1 for r in exams if all(r['phan'])), '| có tự luận', sum(1 for r in exams if r['tuluan']), '| cả 3 phần + tự luận', sum(1 for r in exams if all(r['phan']) and r['tuluan']))
print('đề có star>=10', sum(1 for r in exams if r['star']>=10), '| có mục đáp án trong file', sum(1 for r in exams if r['dapan_section']), '| không star & không mục đáp án', sum(1 for r in exams if r['star']<10 and not r['dapan_section']))
print('có lời giải', sum(1 for r in exams if r['loigiai']>=5), '| có nhãn Chủ đề', sum(1 for r in exams if r['chude']))
print('ảnh: 0', sum(1 for r in exams if r['media']==0), '| 1-5', sum(1 for r in exams if 0<r['media']<=5), '| >5', sum(1 for r in exams if r['media']>5))
print('OLE>0', sum(1 for r in exams if r['ole']>0), '| OMML>0', sum(1 for r in exams if r['omml']>0), '| cả hai =0', sum(1 for r in exams if r['ole']==0 and r['omml']==0))
print('theo kỳ:', {k: C(r['top'] for r in exams if (all(r['phan']) if k=='3phan' else r['tuluan'])) for k in ('3phan','tuluan')})
# bộ đề: nhóm theo thư mục; file lẻ cấp 1 = 1 bộ
sets = collections.defaultdict(list)
for r in rows:
    if r['ext'] in ('doc','docx','pdf') and r['role']=='exam':
        key = r['dir'] if r['dir'] else r['rel']
        sets[key].append(r)
print('số bộ đề ước tính (thư mục hoặc file lẻ):', len(sets), '| theo kỳ:', C(k.split('/')[0] for k in sets))
only_doc = [k for k,v in sets.items() if all(r['ext']=='doc' for r in v)]
only_pdf = [k for k,v in sets.items() if all(r['ext']=='pdf' for r in v)]
print('bộ chỉ có .doc:', len(only_doc), '| bộ chỉ có .pdf:', len(only_pdf), '| bộ có file gốc:', sum(1 for v in sets.values() if any(r['goc'] for r in v)), '| bộ nhiều mã đề:', sum(1 for v in sets.values() if sum(r['made'] for r in v)>=2))
print('xlsx đáp án:', sum(1 for r in rows if r['ext'] in('xlsx','xls')), '| bộ có file đáp án rời:', sum(1 for k in sets if any(r['role']=='key' and r['dir']==k for r in rows)))
