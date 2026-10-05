/* ThachLab service worker (viết tay, M1 vỏ PWA).
 * Nguyên tắc: KHÔNG phục vụ nội dung học từ cache trước — services/static-content.ts tự đối chiếu
 * Supabase. Bỏ qua mọi request không phải GET, khác origin, và *.supabase.co.
 *  - /_next/static/*: file băm tên, bất biến -> cache-first.
 *  - /data/*: network-first, rớt mạng mới dùng bản cache.
 *  - điều hướng trang: network-first, rớt mạng -> trang đã cache hoặc "/".
 * Đổi VERSION để dọn cache cũ. */
const VERSION = "v1";
const SHELL_CACHE = "thachlab-shell-" + VERSION;
const RUNTIME_CACHE = "thachlab-runtime-" + VERSION;
const SHELL = ["/", "/icons/icon-192.png", "/icons/icon-512.png"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(SHELL_CACHE)
      .then((c) => c.addAll(SHELL))
      .catch(() => {})
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((k) => k.startsWith("thachlab-") && k !== SHELL_CACHE && k !== RUNTIME_CACHE)
            .map((k) => caches.delete(k)),
        ),
      )
      .then(() => self.clients.claim()),
  );
});

function networkFirst(request, cacheName, fallbackUrl) {
  return fetch(request)
    .then((res) => {
      if (res && res.ok) {
        const copy = res.clone();
        caches.open(cacheName).then((c) => c.put(request, copy)).catch(() => {});
      }
      return res;
    })
    .catch(() =>
      caches.match(request).then((hit) => hit || (fallbackUrl ? caches.match(fallbackUrl) : undefined) || Response.error()),
    );
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // gồm cả *.supabase.co
  if (url.hostname.endsWith("supabase.co")) return;

  if (url.pathname.startsWith("/_next/static/")) {
    event.respondWith(
      caches.match(req).then(
        (hit) =>
          hit ||
          fetch(req).then((res) => {
            if (res && res.ok) {
              const copy = res.clone();
              caches.open(RUNTIME_CACHE).then((c) => c.put(req, copy)).catch(() => {});
            }
            return res;
          }),
      ),
    );
    return;
  }

  if (url.pathname.startsWith("/data/")) {
    event.respondWith(networkFirst(req, RUNTIME_CACHE));
    return;
  }

  if (req.mode === "navigate") {
    event.respondWith(networkFirst(req, RUNTIME_CACHE, "/"));
  }
});
