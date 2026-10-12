# Lấy ảnh Wikimedia Commons có giấy phép mở (Python chuẩn, không cần thư viện ngoài trừ Pillow để nén)

Chỉ nhận `LicenseShortName` chứa CC0 / CC BY / CC BY-SA / Public domain; loại NC, ND. Ghi tác giả + giấy phép + link trang
file vào `credits.json` (script dựng in chú thích dưới ảnh). Tải bản `iiurlwidth=1000`, nén WebP ≤ 150 KB, rộng ≤ 1000 px.
Header `User-Agent` bắt buộc (Commons chặn request không tên).

```python
import json, urllib.request, urllib.parse, re, io
from PIL import Image
API = "https://commons.wikimedia.org/w/api.php"; H = {"User-Agent": "thachlab-lesson-bot/1.0 (<email thầy>)"}
def get(p):
    p.update(format="json"); return json.load(urllib.request.urlopen(urllib.request.Request(API + "?" + urllib.parse.urlencode(p), headers=H), timeout=30))
def search(q, n=8):  # trả về [{title, lic, artist, thumb, page, w, h}] đã lọc giấy phép
    d = get(dict(action="query", generator="search", gsrsearch="filetype:bitmap " + q, gsrnamespace=6, gsrlimit=n, prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=1000))
    rows = []
    for pg in d.get("query", {}).get("pages", {}).values():
        ii = pg["imageinfo"][0]; em = ii.get("extmetadata", {}); lic = em.get("LicenseShortName", {}).get("value", "")
        if not any(k in lic for k in ["CC0", "CC BY", "Public domain"]) or "NC" in lic or "ND" in lic: continue
        rows.append(dict(title=pg["title"], lic=lic, artist=re.sub("<[^>]+>", "", em.get("Artist", {}).get("value", "")).strip()[:60], thumb=ii.get("thumburl"), page=ii["descriptionurl"], w=ii["width"], h=ii["height"]))
    return rows
def save_webp(row, key, out_dir):  # tải + nén; trả về dict cho credits.json
    data = urllib.request.urlopen(urllib.request.Request(row["thumb"], headers=H), timeout=60).read()
    im = Image.open(io.BytesIO(data)).convert("RGB"); im.thumbnail((1000, 1000)); q = 82
    while True:
        b = io.BytesIO(); im.save(b, "WEBP", quality=q)
        if b.tell() <= 150_000 or q <= 40: break
        q -= 8
    open(f"{out_dir}/{key}.webp", "wb").write(b.getvalue())
    return dict(key=key, file=row["title"].replace("File:", ""), license=row["lic"], author=row["artist"], page=row["page"], w=im.width, h=im.height, kb=round(b.tell() / 1024))
```

Từ khoá tìm hay được: tên vật + "workshop"/"tool" (vd `metal lathe workshop`, `bench grinder`, `twist drill bit`). Kết quả lệch
(cùng tên khác nghĩa: "Hacksaw Ridge", "Mile End Mill") → thêm từ ngữ cảnh. Ghép contact sheet (PIL) xem một lần, không
Read từng ảnh.
