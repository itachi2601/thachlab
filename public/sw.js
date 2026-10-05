/* ThachLab service worker (viết tay, M1 vỏ PWA).
 * Nguyên tắc: KHÔNG phục vụ nội dung học từ cache trước — services/static-content.ts tự đối chiếu
 * Supabase. Bỏ qua mọi request không phải GET, khác origin, và *.supabase.co.
 *  - /_next/static/*: file băm tên, bất biến -> cache-first.
 *  - /data/*: network-first, rớt mạng mới dùng bản cache.
 *  - điều hướng trang + dữ liệu RSC của Next (`_rsc`): network-first, rớt mạng -> bản đã cache
 *    (khớp cả khi khác query), cuối cùng "/". Nhờ đó bài/luyện đã mở xem lại được khi mất mạng.
 *  - Kết quả luyện tập mất mạng KHÔNG đi qua SW: services/lessons.ts xếp hàng ở localStorage.
 *  - RUNTIME_CACHE giới hạn MAX_RUNTIME_ENTRIES mục (xoá mục cũ nhất).
 *  - push + notificationclick: nhắc luyện 1 lần/ngày (M4), bấm vào mở /lop-hoc/ và focus tab có sẵn.
 * Đổi VERSION để dọn cache cũ. */
const VERSION = "v3";
const SHELL_CACHE = "thachlab-shell-" + VERSION;
const RUNTIME_CACHE = "thachlab-runtime-" + VERSION;
const MAX_RUNTIME_ENTRIES = 120;
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

function trimCache(cacheName) {
  return caches
    .open(cacheName)
    .then((c) =>
      c.keys().then((keys) => {
        const extra = keys.length - MAX_RUNTIME_ENTRIES;
        return extra > 0 ? Promise.all(keys.slice(0, extra).map((k) => c.delete(k))) : undefined;
      }),
    )
    .catch(() => {});
}

function networkFirst(request, cacheName, fallbackUrl) {
  return fetch(request)
    .then((res) => {
      if (res && res.ok) {
        const copy = res.clone();
        caches
          .open(cacheName)
          .then((c) => c.put(request, copy))
          .then(() => trimCache(cacheName))
          .catch(() => {});
      }
      return res;
    })
    .catch(() =>
      caches
        .match(request)
        .then((hit) => hit || caches.match(request, { ignoreSearch: true }))
        .then((hit) => hit || (fallbackUrl ? caches.match(fallbackUrl) : undefined) || Response.error()),
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
    return;
  }

  // Dữ liệu RSC khi chuyển trang phía client (static export): chỉ network-first, không fallback "/".
  if (url.searchParams.has("_rsc") || url.pathname.endsWith(".txt")) {
    event.respondWith(networkFirst(req, RUNTIME_CACHE));
  }
});

// Web Push (M4): nhắc luyện 1 lần/ngày. Payload JSON {title, body, url, tag}; hỏng thì dùng chữ mặc định.
self.addEventListener("push", (event) => {
  let d = {};
  try {
    d = event.data ? event.data.json() : {};
  } catch (e) {
    d = {};
  }
  event.waitUntil(
    self.registration.showNotification(d.title || "ThachLab", {
      body: d.body || "Hôm nay luyện 5 phút nhé?",
      icon: "/icons/icon-192.png",
      badge: "/icons/icon-192.png",
      tag: d.tag || "thachlab-daily",
      data: { url: d.url || "/lop-hoc/" },
    }),
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const target = new URL((event.notification.data && event.notification.data.url) || "/lop-hoc/", self.location.origin).href;
  event.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((list) => {
      for (const c of list) {
        if (c.url.startsWith(self.location.origin) && "focus" in c) {
          return c.focus().then(() => ("navigate" in c ? c.navigate(target).catch(() => c) : c));
        }
      }
      return self.clients.openWindow(target);
    }),
  );
});
