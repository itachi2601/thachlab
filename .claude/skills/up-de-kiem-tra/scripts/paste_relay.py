#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""paste_relay.py — đưa `bundle.json` (~70 KB) vào ô JSON của /quan-tri/nhap-bai.

Gói của một đề đầy đủ quá lớn để gõ tay vào textarea, mà trang admin KHÔNG có ô
upload file. Những cách tưởng là hiển nhiên đều hỏng trong Browser pane:

  ✗ `pbcopy` + `computer key cmd+v`  — phím tổng hợp của pane không chạm clipboard OS
  ✗ `navigator.clipboard.readText()` — Read permission denied
  ✗ `fetch('http://127.0.0.1:…')` từ trang https — mixed content, ERR_BLOCKED_BY_CLIENT
  ✗ HTTPS localhost tự ký            — pane từ chối điều hướng, không hiện interstitial
  ✗ `window.open(...)`               — pane biến thành điều hướng CÙNG tab, mất state
  ✗ dán thẳng chuỗi vào tool call    — ~20k token và dễ sai một ký tự

Cách chạy được: điều hướng tab sang một trang localhost, trang đó tự nhảy về
thachlab kèm payload trong URL hash (hash không bao giờ gửi lên server).

    python3 paste_relay.py bundle.json          # in ra URL relay rồi chạy nền

  1. `navigate` tab của Browser pane tới URL relay mà script in ra.
  2. Đợi ~3 s — tab tự quay lại /quan-tri/nhap-bai/ với `#b64=…` trong URL.
  3. Chạy JS trên tab đó (giải mã + gán textarea):

     const b64 = location.hash.replace(/^#b64=/, '');
     const bin = atob(b64);
     const u8 = new Uint8Array(bin.length);
     for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
     window.__bundleText = new TextDecoder('utf-8').decode(u8);
     history.replaceState(null, '', location.pathname);
     const ta = document.querySelectorAll('textarea')[0];
     Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value')
       .set.call(ta, window.__bundleText);
     ta.dispatchEvent(new Event('input', { bubbles: true }));

     Phải dùng native setter rồi bắn sự kiện `input` — React bỏ qua `ta.value = …`.

  4. CHỌN Lớp → Môn → Chương → Bài SAU BƯỚC NÀY. Relay làm tab điều hướng nên mọi
     lựa chọn trước đó mất sạch.
  5. Ô JSON nằm trong khối gập "Nâng cao: dán gói JSON…" ở đầu trang — script gán
     `.value` thẳng vào DOM nên gập/mở không ảnh hưởng, nhưng phải BẤM MỞ khối đó
     (bấm vào dòng tóm tắt) trước khi bấm "Nạp gói", vì nút đang ẩn lúc khối gập.
  6. Bấm "Nạp gói", đọc bảng validate (khung đỏ cạnh nút "Đăng bài học" ở cuối trang)
     + khung "Nhãn chủ đề trước khi đăng" (mục riêng, sau phần Đề), rồi Đăng.
  7. Ctrl-C script (hoặc `pkill -f paste_relay.py`) khi xong.

Lưu ý thao tác pane: ĐỪNG `resize_window` để emulate viewport — toạ độ click lệch
khỏi ảnh chụp. Dùng `ref` từ `find`/`read_page` và `form_input` cho <select>.
"""
import argparse
import http.server
import os
import socketserver
import sys
import tempfile

RELAY_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>relay</title></head>
<body style="font-family:system-ui;padding:20px"><p id="s">relaying…</p>
<script>
(async () => {
  const s = document.getElementById('s');
  try {
    const r = await fetch('bundle.json', { cache: 'no-store' });
    const buf = new Uint8Array(await r.arrayBuffer());
    let bin = '';
    for (let i = 0; i < buf.length; i += 0x8000)
      bin += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
    const b64 = btoa(bin);
    s.textContent = 'relaying ' + b64.length + ' chars…';
    location.replace('__TARGET__#b64=' + b64);
  } catch (e) { s.textContent = 'ERR ' + e.message; }
})();
</script></body></html>
"""

TARGET = 'https://thachlab.id.vn/quan-tri/nhap-bai/'


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('bundle', help='đường dẫn bundle.json')
    ap.add_argument('--port', type=int, default=8791)
    ap.add_argument('--target', default=TARGET, help='trang nhận payload')
    a = ap.parse_args()

    src = os.path.abspath(a.bundle)
    if not os.path.isfile(src):
        sys.exit(f'LỖI: không thấy {src}')
    n = os.path.getsize(src)

    d = tempfile.mkdtemp(prefix='paste-relay-')
    with open(src, 'rb') as f, open(os.path.join(d, 'bundle.json'), 'wb') as g:
        g.write(f.read())
    with open(os.path.join(d, 'relay.html'), 'w', encoding='utf-8') as f:
        f.write(RELAY_HTML.replace('__TARGET__', a.target))
    os.chdir(d)

    class H(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-store')
            super().end_headers()

        def log_message(self, *a):
            pass

    socketserver.TCPServer.allow_reuse_address = True
    url = f'http://127.0.0.1:{a.port}/relay.html'
    print(f'bundle {n:,} bytes  →  navigate Browser pane tới:\n  {url}\n'
          f'Sau ~3 s tab quay về {a.target} với #b64=… — xem docstring cho bước JS tiếp theo.',
          flush=True)
    with socketserver.TCPServer(('127.0.0.1', a.port), H) as s:
        try:
            s.serve_forever()
        except KeyboardInterrupt:
            print('\ndừng relay.')


if __name__ == '__main__':
    main()
