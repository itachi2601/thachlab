# Gắn khung video tương tác THẲNG vào bản lý thuyết đang có trên DB (không qua file repo — repo hay lệch DB).
# Chỉ sửa thẻ mở hộp `<!--video:ID--><div class="tl-box tl-box--video…">` có JSON ở content/thi-nghiem/video-khung/ID.json,
# tự kiểm "bỏ thuộc tính khung thì y hệt bản DB", sao lưu scripts/logs/ly-thuyet-bai<id>-khung-backup-*.json rồi PATCH.
#   python3 scripts/video-thi-nghiem/gan-khung-db.py 14 9            # xem trước
#   python3 scripts/video-thi-nghiem/gan-khung-db.py 14 9 --apply    # ghi (chạy trong tab terminal: Bash bị chặn supabase.co)
# Hoàn tác một bài: PATCH lại body_html trong file sao lưu.
import json,re,sys,os,time,urllib.request
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APPLY='--apply' in sys.argv
env={}
for l in open(os.path.join(ROOT,'.env.local')):
  if '=' in l and not l.startswith('#'):
    k,v=l.strip().split('=',1); env[k]=v.strip('"')
U=env['NEXT_PUBLIC_SUPABASE_URL'];K=env['SUPABASE_SERVICE_ROLE_KEY']
def req(q,method='GET',body=None):
  r=urllib.request.Request(U+'/rest/v1/'+q,method=method,data=body,headers={'apikey':K,'Authorization':'Bearer '+K,'Content-Type':'application/json','Prefer':'return=representation'})
  return json.load(urllib.request.urlopen(r))
LESSONS=[int(x) for x in sys.argv[1:] if x.isdigit()]
BLOCK=re.compile(r'(<!--video:(tn-[a-z0-9-]+)-->\s*<div class="tl-box tl-box--video)((?: [a-z0-9-]+)*)"((?: data-khung="[^"]*")?)>((?:(?!<!--video:)[\s\S])*?<video src="([^"]+)"(?: poster="([^"]+)")?)')
esc=lambda s:s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
KD=ROOT+'/content/thi-nghiem/video-khung/'
for lid in LESSONS:
  rows=req(f'lesson_items?lesson_id=eq.{lid}&kind=eq.ly_thuyet&select=id,body_html')
  assert len(rows)==1,(lid,len(rows))
  it=rows[0]; old=it['body_html']; ghi=[]; bo=[]
  def f(m):
    head,id_,cls,oldk,rest,mp4,poster=m.groups()
    p=KD+id_+'.json'
    if not os.path.exists(p): bo.append(id_); return m.group(0)
    d=json.load(open(p))
    s=json.dumps(d,ensure_ascii=False)
    assert not re.search(r'-->|\]>|</(?:style|title)',s,re.I)
    d['video']=mp4
    if poster: d['poster']=poster
    ghi.append(id_)
    classes=cls.replace(' tl-box--khung','')
    return f'{head}{classes} tl-box--khung" data-khung="{esc(json.dumps(d,ensure_ascii=False,separators=(",",":")))}">{rest}'
  new=BLOCK.sub(f,old)
  # kiểm: bỏ thuộc tính khung khỏi bản mới phải ra đúng bản DB
  back=re.sub(r' tl-box--khung" data-khung="[^"]*">','">',new)
  ok = back==re.sub(r' tl-box--khung" data-khung="[^"]*">','">',old)
  print(lid, it['id'], 'gắn:',ghi, 'bỏ qua:',bo, '| chỉ khác thẻ mở:',ok, '| tl-box--video trong DB:', old.count('tl-box--video'), 'comment video:', old.count('<!--video:'))
  if APPLY and ghi and ok and new!=old:
    bk=f'{ROOT}/scripts/logs/ly-thuyet-bai{lid}-khung-backup-{int(time.time())}.json'
    json.dump({'item_id':it['id'],'lesson_id':lid,'body_html':old},open(bk,'w'),ensure_ascii=False)
    r=req(f'lesson_items?id=eq.{it["id"]}','PATCH',json.dumps({'body_html':new}).encode())
    assert r and r[0]['body_html']==new
    print('   ĐÃ GHI, sao lưu', bk)
