#!/usr/bin/env python3
"""Chụp ảnh xem thử cho bài lý thuyết bằng Google Chrome headless + DevTools Protocol (CDP).

Vì sao không dùng `--window-size`: Chrome trên macOS ép cửa sổ tối thiểu 500px, nên ảnh "375px" thực chất
là layout 500px. Script này điều khiển Chrome qua CDP `Emulation.setDeviceMetricsOverride` để có **đúng
375 CSS px** (và `captureBeyondViewport` để lấy trọn trang, không cần cửa sổ cao). Không cần Playwright,
không cần thư viện ngoài (tự viết WebSocket client tối thiểu bằng thư viện chuẩn).

Dùng: python3 chup_anh.py <thư-mục-xem-thu> [--rong 375] [--fig-rong 460] [--chi-hinh] [--giu-png]

Đầu vào là thư mục do build_preview.py sinh ra (xem-thu.html, sec-*.html, sec-sai.html, fig-*.html).
Sinh ra (WebP):
  xem-thu-desktop.webp   — trang xem thử ở bề ngang máy tính (820px)
  sec-<n>.webp           — từng mục <h3> ở đúng bề ngang điện thoại, mở sẵn <details> + đáp án đúng
  mau-tra-loi-sai.webp   — trạng thái chọn đáp án sai (phản hồi đỏ), nếu có sec-sai.html
  fig-<n>.webp           — từng hình SVG chụp riêng để soi nhãn
"""
import base64, json, os, pathlib, shutil, signal, socket, struct, subprocess, sys, tempfile, time, urllib.request
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BG = (15, 23, 42)


# ---------------------------------------------------------------- WebSocket tối thiểu
class WS:
    def __init__(self, url, timeout=30):
        assert url.startswith("ws://")
        rest = url[5:]
        hostport, _, pathq = rest.partition("/")
        host, _, port = hostport.partition(":")
        self.sock = socket.create_connection((host, int(port)), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (f"GET /{pathq} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
               f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
        self.sock.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.sock.recv(4096)
        if b"101" not in buf.split(b"\r\n")[0]:
            raise RuntimeError(f"bắt tay WebSocket thất bại: {buf[:120]!r}")
        self.buf = buf.split(b"\r\n\r\n", 1)[1]

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(1 << 20)
            if not chunk:
                raise ConnectionError("WebSocket đóng")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def send(self, payload: str):
        data = payload.encode()
        header = bytearray([0x81])
        n = len(data)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126); header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127); header += struct.pack(">Q", n)
        mask = os.urandom(4)
        header += mask
        self.sock.sendall(bytes(header) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def recv(self):
        """Đọc trọn một message (ghép frame nối tiếp, tự trả lời ping)."""
        chunks = []
        while True:
            b0, b1 = self._read(2)
            fin, opcode = b0 & 0x80, b0 & 0x0F
            masked, ln = b1 & 0x80, b1 & 0x7F
            if ln == 126:
                ln = struct.unpack(">H", self._read(2))[0]
            elif ln == 127:
                ln = struct.unpack(">Q", self._read(8))[0]
            mk = self._read(4) if masked else None
            data = self._read(ln)
            if mk:
                data = bytes(b ^ mk[i % 4] for i, b in enumerate(data))
            if opcode == 0x9:                      # ping → pong
                self.sock.sendall(b"\x8a\x80" + os.urandom(4))
                continue
            if opcode == 0x8:
                raise ConnectionError("WebSocket đóng bởi Chrome")
            chunks.append(data)
            if fin:
                return b"".join(chunks).decode("utf8", "replace")


class CDP:
    def __init__(self, port: int):
        targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=10))
        pages = [t for t in targets if t.get("type") == "page"]
        if not pages:
            raise RuntimeError("Chrome không có target trang nào")
        self.ws = WS(pages[0]["webSocketDebuggerUrl"])
        self.next_id = 1

    def call(self, method, **params):
        mid = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            # bỏ qua event khác


def launch_chrome():
    udd = tempfile.mkdtemp(prefix="chrome-cdp-")
    proc = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
                             "--no-default-browser-check", "--hide-scrollbars", "--remote-debugging-port=0",
                             f"--user-data-dir={udd}", "about:blank"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    port_file = pathlib.Path(udd) / "DevToolsActivePort"
    for _ in range(120):
        time.sleep(0.25)
        if port_file.exists():
            txt = port_file.read_text().splitlines()
            if txt and txt[0].strip().isdigit():
                return proc, udd, int(txt[0])
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    raise RuntimeError("Chrome không mở cổng DevTools")


def stop_chrome(proc, udd):
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except Exception:
        pass
    time.sleep(0.3)
    shutil.rmtree(udd, ignore_errors=True)


def crop_bg(img, pad=14, trim_x=True):
    """Cắt nền #0f172a thừa. trim_x=False → giữ nguyên bề ngang (ảnh mục giữ đúng khung điện thoại)."""
    px = img.convert("RGB").load()
    w, h = img.size
    rows = [y for y in range(h) if any(sum(abs(px[x, y][i] - BG[i]) for i in range(3)) > 18 for x in range(0, w, 3))]
    cols = [x for x in range(w) if any(sum(abs(px[x, y][i] - BG[i]) for i in range(3)) > 18 for y in range(0, h, 3))]
    if not rows or not cols:
        return img, False
    x0, x1 = (max(0, cols[0] - pad), min(w, cols[-1] + pad)) if trim_x else (0, w)
    return img.crop((x0, max(0, rows[0] - pad), x1, min(h, rows[-1] + pad))), rows[-1] >= h - 4


def shoot(cdp, page, out, width, scale=2, clip_h=None, settle=0.5):
    cdp.call("Emulation.setDeviceMetricsOverride", width=width, height=900, deviceScaleFactor=scale, mobile=True)
    cdp.call("Page.navigate", url=page.as_uri())
    deadline = time.time() + 20
    while time.time() < deadline:          # chờ trang + KaTeX auto-render chạy xong
        state = cdp.call("Runtime.evaluate", expression="document.readyState").get("result", {}).get("value")
        if state == "complete":
            break
        time.sleep(0.1)
    time.sleep(settle)
    params = {"format": "png", "captureBeyondViewport": True}
    if clip_h:
        params["clip"] = {"x": 0, "y": 0, "width": width, "height": clip_h, "scale": 1}
    data = cdp.call("Page.captureScreenshot", **params)["data"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(data))
    return out


# Kiểm tràn ngang ở bề ngang điện thoại.
# Trang bài thật (.lesson-page) đặt .katex{display:inline;overflow:visible}, nên công thức NỘI DÒNG dài hơn
# bề ngang khung sẽ đẩy tràn cả trang — script báo trước để cắt/sửa công thức.
TRAN_JS = r"""
(() => {
  const cw = document.documentElement.clientWidth;
  const clipped = e => { for (let q = e.parentElement; q; q = q.parentElement) {
    const o = getComputedStyle(q).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden') return true; } return false; };
  const tran = [...document.querySelectorAll('*')].map(e => [e, e.getBoundingClientRect()])
    .filter(([e, r]) => r.right > cw + 1 && !clipped(e))
    .sort((a, b) => b[1].right - a[1].right).slice(0, 5)
    .map(([e, r]) => e.tagName + '.' + String(e.className).slice(0, 24) + ' right=' + Math.round(r.right)
      + ' | ' + (e.textContent || '').trim().slice(0, 30));
  const to = [...document.querySelectorAll('.katex')].filter(e => !e.closest('.katex-display'))
    .map(e => [e.getBoundingClientRect().width, e.textContent || ''])
    .filter(([w]) => w > cw - 40).sort((a, b) => b[0] - a[0]).slice(0, 5)
    .map(([w, t]) => 'cong thuc rong ' + Math.round(w) + 'px | ' + t.trim().slice(0, 34));
  // công thức khối rộng hơn khung → học sinh phải cuộn ngang trong ô công thức
  const cuon = [...document.querySelectorAll('.katex-display')]
    .filter(e => e.scrollWidth > e.clientWidth + 4)
    .map(e => 'cong thuc khoi phai cuon: ' + e.clientWidth + 'px khung / ' + e.scrollWidth + 'px noi dung | '
      + (e.textContent || '').trim().slice(0, 30));
  return JSON.stringify({ clientW: cw, scrollW: document.documentElement.scrollWidth, tran, to, cuon });
})()
"""


def check_overflow(cdp, page, width=375):
    cdp.call("Emulation.setDeviceMetricsOverride", width=width, height=900, deviceScaleFactor=2, mobile=True)
    cdp.call("Page.navigate", url=page.as_uri())
    deadline = time.time() + 20
    while time.time() < deadline:
        state = cdp.call("Runtime.evaluate", expression="document.readyState").get("result", {}).get("value")
        if state == "complete":
            break
        time.sleep(0.1)
    time.sleep(0.4)
    raw = cdp.call("Runtime.evaluate", expression=TRAN_JS, returnByValue=True)["result"]["value"]
    return json.loads(raw)



def save_webp(png: pathlib.Path, out: pathlib.Path, quality=86, crop=True, trim_x=True, warn_cut=True):
    im = Image.open(png)
    cut = False
    if crop:
        im, cut = crop_bg(im, trim_x=trim_x)
    im.save(out, "WEBP", quality=quality, method=6)
    print(f"{out.name:26s} {im.width}x{im.height}  {out.stat().st_size/1024:5.0f} KB"
          + ("  ⚠ CÓ THỂ BỊ CẮT ĐÁY" if (cut and warn_cut) else ""))


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    out = pathlib.Path(argv[0]).resolve()
    width = int(argv[argv.index("--rong") + 1]) if "--rong" in argv else 375
    fig_w = int(argv[argv.index("--fig-rong") + 1]) if "--fig-rong" in argv else 460
    keep_png = "--giu-png" in argv
    only_figs = "--chi-hinh" in argv
    if not out.exists():
        print(f"Không thấy {out} — chạy build_preview.py trước")
        return 1

    pages = []   # (trang html, ảnh ra, bề ngang, scale, chiều cao cắt, cắt hai bên)
    if not only_figs:
        if (out / "xem-thu.html").exists():
            pages.append((out / "xem-thu.html", out / "xem-thu-desktop.webp", 820, 1, 1150, False))
        for s in sorted([p for p in out.glob("sec-*.html") if p.stem != "sec-sai"],
                        key=lambda p: int(p.stem.split("-")[1])):
            pages.append((s, out / f"{s.stem}.webp", width, 2, None, False))
        if (out / "sec-sai.html").exists():
            pages.append((out / "sec-sai.html", out / "mau-tra-loi-sai.webp", width, 2, 1600, False))
    for f in sorted(out.glob("fig-*.html"), key=lambda p: int(p.stem.split("-")[1])):
        pages.append((f, out / f"{f.stem}.webp", fig_w, 2, None, True))

    if not pages:
        print("⚠ không thấy sec-*.html / fig-*.html — chạy build_preview.py trước")
        return 1

    proc, udd, port = launch_chrome()
    try:
        cdp = CDP(port)
        cdp.call("Page.enable")
        if "--kiem-tran" in argv:
            bad = 0
            for page, _dst, w, _scale, _clip, _tx in pages:
                if w != width:
                    continue
                r = check_overflow(cdp, page, width)
                ok = r["scrollW"] <= r["clientW"] + 1 and not r["tran"] and not r["to"] and not r["cuon"]
                # 'to' chỉ là CẢNH BÁO: công thức nội dòng dài sát bề ngang, chưa chắc tràn
                bad += 0 if ok else 1
                print(f"{page.stem:8s} {'OK' if ok else 'TRÀN'}  clientW={r['clientW']} scrollW={r['scrollW']}")
                for line in r["tran"]:
                    print("    ↳ tràn:", line)
                for line in r["to"]:
                    print("    ↳", line)
                for line in r["cuon"]:
                    print("    ↳", line)
            print("KẾT LUẬN:", "không mục nào đẩy tràn ngang ở bề ngang điện thoại" if not bad else f"{bad} mục cần xem lại")
            return 0
        for page, dst, w, scale, clip_h, trim_x in pages:
            png = dst.with_suffix(".png")
            shoot(cdp, page, png, w, scale=scale, clip_h=clip_h)
            save_webp(png, dst, quality=85 if (w == width and scale == 2) else 90, trim_x=trim_x,
                      warn_cut=clip_h is None)   # ảnh cắt sẵn chiều cao thì không cảnh báo cắt đáy
            if not keep_png:
                png.unlink()
    finally:
        stop_chrome(proc, udd)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
