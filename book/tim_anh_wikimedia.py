"""Tìm ảnh THỰC TẾ trên Wikimedia Commons cho sách in: mỗi bài một truy vấn tiếng Anh (sửa Q), lọc JPEG ≥800px giấy phép
CC BY/BY-SA/CC0/PD, lấy 4 ứng viên → wm/ung-vien.json + tờ ghép wm/to-ghep.jpg (xem 1 ảnh là chọn được cả chương).
Chạy trong thư mục nháp: /usr/bin/python3 book/tim_anh_wikimedia.py. API trả 429 nếu gọi dồn → đã có nghỉ 1,5 s + thử lại.
Chọn xong: tải thumb 900px, xám + autocontrast, ≤150 KB vào book/assets/anh-that/, khai báo anh_that trong hồ sơ sách."""
import json, urllib.request, urllib.error, urllib.parse, re, sys
from PIL import Image, ImageDraw
import io
Q = {58:'tugboats towing ship', 59:'crash test dummy', 60:'bobsleigh start push', 61:'Falcon 9 launch',
     62:'plumb bob', 63:'tire tread', 64:'skydiving formation freefall', 65:'playground slide',
     66:'claw hammer', 67:'traffic signal suspended span wire'}
UA = {'User-Agent': 'thachlab-book-builder/1.0 (educational print book)'}
OK = re.compile(r'^(CC BY(-SA)? [\d.]+|CC0|Public domain|PD.*)$', re.I)
import time
def get(u):
    for t in range(5):
        try:
            time.sleep(1.5); return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read()
        except urllib.error.HTTPError as e:
            if e.code!=429: raise
            time.sleep(10*(t+1))
    raise SystemExit('429 mãi')
out = {}
for lid, q in Q.items():
    u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'action':'query','format':'json','generator':'search',
        'gsrsearch':q+' filetype:bitmap','gsrnamespace':6,'gsrlimit':15,'prop':'imageinfo','iiprop':'url|extmetadata|mime|size','iiurlwidth':900})
    pages = sorted(json.loads(get(u)).get('query',{}).get('pages',{}).values(), key=lambda p:p.get('index',0))
    c = []
    for p in pages:
        ii = p['imageinfo'][0]; m = ii.get('extmetadata',{})
        lic = m.get('LicenseShortName',{}).get('value','')
        if ii['mime']!='image/jpeg' or not OK.match(lic.strip()) or ii['width']<800: continue
        art = re.sub(r'<[^>]+>','',m.get('Artist',{}).get('value','')).strip()[:60]
        c.append({'title':p['title'],'thumb':ii['thumburl'],'lic':lic,'artist':art,'page':ii['descriptionurl']})
        if len(c)==4: break
    out[lid]=c; print(lid, len(c), [x['title'][5:40] for x in c])
json.dump(out, open('wm/ung-vien.json','w'), ensure_ascii=False, indent=1)
# tờ ghép: mỗi bài 1 hàng, 4 ảnh 220px
W=220; sheet=Image.new('RGB',(60+4*(W+8), len(out)*(W*3//4+8)),'white'); d=ImageDraw.Draw(sheet)
for r,(lid,c) in enumerate(out.items()):
    y=r*(W*3//4+8); d.text((4,y+10),str(lid),fill='black')
    for k,x in enumerate(c):
        try:
            im=Image.open(io.BytesIO(get(x['thumb']))).convert('RGB'); im.thumbnail((W,W*3//4))
            sheet.paste(im,(60+k*(W+8),y)); d.text((62+k*(W+8),y+2),str(k),fill='red')
        except Exception as e: print('loi',lid,k,e)
sheet.save('wm/to-ghep.jpg',quality=70)
