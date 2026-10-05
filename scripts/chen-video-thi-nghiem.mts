// Chèn khối video thí nghiệm (.tl-box--video) vào bài lý thuyết tương tác, lấy dữ liệu
// từ kho content/thi-nghiem/*.json (field tuỳ chọn `video`). Chạy lại được — đã chèn rồi
// thì bỏ qua, không nhân đôi khối.
//
//   npx tsx scripts/chen-video-thi-nghiem.mts                     # xem thử tất cả bài có dữ liệu
//   npx tsx scripts/chen-video-thi-nghiem.mts --bai l11-giao-thoa-song
//   npx tsx scripts/chen-video-thi-nghiem.mts --bai 31 --apply
//   npx tsx scripts/chen-video-thi-nghiem.mts --kiem               # kiểm link còn sống/nhúng được
//   npx tsx scripts/chen-video-thi-nghiem.mts --kiem --apply       # kiểm rồi ghi ten/kenh/da_kiem
//   npx tsx scripts/chen-video-thi-nghiem.mts --json > /tmp/bao-cao.json
//
// Mặc định DRY-RUN (không ghi file). Cờ:
//   --bai <slug|lesson_id>  chỉ làm một bài (số = lesson_id)
//   --kho <thư-mục>         kho thí nghiệm (mặc định content/thi-nghiem)
//   --root <thư-mục>        thư mục các bài (mặc định content/lesson-samples)
//   --kiem                  chỉ kiểm link bằng oEmbed (miễn phí, không cần API key) rồi thoát
//   --apply                 ghi thật (khi --kiem: ghi ten/kenh/da_kiem vào JSON)
//   --json                  in báo cáo JSON (cho script khác đọc)
//
// Vị trí chèn: ngay SAU hộp `.tl-box--exp[data-exp="<id>"]` (Làm–Quan sát–Rút ra); nếu bài
// chỉ có `<figure data-exp="<id>">` thì chèn sau figure. Mỗi thí nghiệm 1 khối, mỗi bài
// 1 lần cho mỗi thí nghiệm. Quy ước dữ liệu: content/thi-nghiem/README.md.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const argv = process.argv.slice(2);
function opt(name: string): string | undefined {
  const i = argv.indexOf(name);
  if (i === -1) return undefined;
  const next = argv[i + 1];
  return next && !next.startsWith("--") ? next : "";
}
const APPLY = argv.includes("--apply");
const JSON_OUT = argv.includes("--json");
const KIEM = argv.includes("--kiem");
const only = opt("--bai") || undefined;
const khoDir = path.resolve(root, opt("--kho") || "content/thi-nghiem");
const lessonRoot = path.resolve(root, opt("--root") || "content/lesson-samples");

type Video = {
  youtube_id: string;
  ten?: string;
  kenh?: string;
  nhan?: string;
  nhin_vao?: string;
  giay_bat_dau?: number;
  giay_ket_thuc?: number;
  da_kiem?: string;
};
type KhoEntry = { expTen: string; lessonId?: number | string; video: Video };

function docKho(): Map<string, KhoEntry> {
  const map = new Map<string, KhoEntry>();
  if (!fs.existsSync(khoDir)) {
    console.error(`✗ Không thấy kho thí nghiệm: ${khoDir}`);
    process.exit(1);
  }
  for (const name of fs.readdirSync(khoDir).sort()) {
    if (!/^tn-.*\.json$/.test(name)) continue;
    const data = JSON.parse(fs.readFileSync(path.join(khoDir, name), "utf8"));
    if (!data?.video?.youtube_id) continue;
    map.set(data.id, { expTen: data.ten ?? data.id, lessonId: data.lesson_id, video: data.video });
  }
  return map;
}

/** Bổ sung tên/kênh cho video ghi thiếu, lấy từ kho video dùng chung (đã kiểm oEmbed). */
function docVideoDungChung(): Map<string, Video> {
  const pool = new Map<string, Video>();
  const f = path.join(khoDir, "video-dung-chung.json");
  if (!fs.existsSync(f)) return pool;
  const data = JSON.parse(fs.readFileSync(f, "utf8"));
  for (const v of data?.videos ?? []) if (v?.youtube_id) pool.set(v.youtube_id, v);
  return pool;
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderBlock(expId: string, expTen: string, v: Video, pool: Map<string, Video>): string {
  const shared = pool.get(v.youtube_id);
  const nhan = (v.nhan ?? v.ten ?? shared?.ten ?? expTen).trim();
  const params = new URLSearchParams({ rel: "0" });
  if (typeof v.giay_bat_dau === "number") params.set("start", String(v.giay_bat_dau));
  if (typeof v.giay_ket_thuc === "number") params.set("end", String(v.giay_ket_thuc));
  const lines = [
    `<!--video:${expId}-->`,
    `<div class="tl-box tl-box--video">`,
    `<p class="tl-label">🎬 Xem thí nghiệm thật: ${escapeHtml(nhan)}</p>`,
    `<div class="tl-video"><iframe src="https://www.youtube-nocookie.com/embed/${v.youtube_id}?${params.toString()}" title="${escapeHtml(nhan)}" loading="lazy" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>`,
  ];
  if (v.nhin_vao?.trim()) lines.push(`<p><strong>Nhìn vào:</strong> ${escapeHtml(v.nhin_vao.trim())}</p>`);
  lines.push(`</div>`, ``);
  return lines.join("\n");
}

/** Vị trí kết thúc của hộp thí nghiệm / figure chứa `data-exp="<id>"`. */
function findAnchor(html: string, expId: string): { start: number; end: number } | null {
  const tagRe = /<(div|figure)\b[^>]*>/g;
  let m: RegExpExecArray | null;
  while ((m = tagRe.exec(html))) {
    const tag = m[0];
    const has = tag.includes(`data-exp="${expId}"`) || tag.includes(`data-exp='${expId}'`);
    if (!has) continue;
    const name = m[1].toLowerCase();
    if (name === "div" && !tag.includes("tl-box--exp")) continue;
    if (name === "figure") {
      const close = html.indexOf("</figure>", m.index);
      if (close === -1) return null;
      return { start: m.index, end: close + "</figure>".length };
    }
    // đếm độ sâu <div>…</div> kể từ thẻ mở của hộp thí nghiệm
    const divRe = /<div\b[^>]*>|<\/div>/g;
    divRe.lastIndex = m.index;
    let depth = 0;
    let d: RegExpExecArray | null;
    while ((d = divRe.exec(html))) {
      if (d[0].startsWith("</")) {
        depth--;
        if (depth === 0) return { start: m.index, end: d.index + d[0].length };
      } else {
        depth++;
      }
    }
    return null;
  }
  return null;
}

type KetQuaFile = { file: string; chen: string[]; boQua: string[] };

function chenVaoHtml(html: string, kho: Map<string, KhoEntry>, pool: Map<string, Video>): { html: string; chen: string[]; boQua: string[] } {
  const ids: string[] = [];
  for (const m of html.matchAll(/data-exp="([^"]+)"/g)) if (!ids.includes(m[1])) ids.push(m[1]);

  const chen: string[] = [];
  const boQua: string[] = [];
  const inserts: { pos: number; block: string }[] = [];

  for (const id of ids) {
    const entry = kho.get(id);
    if (!entry) continue;
    const { video } = entry;
    if (html.includes(`<!--video:${id}-->`)) {
      boQua.push(`${id} (đã chèn trước đó)`);
      continue;
    }
    if (html.includes(video.youtube_id)) {
      boQua.push(`${id} (bài đã có video ${video.youtube_id} chèn tay)`);
      continue;
    }
    const anchor = findAnchor(html, id);
    if (!anchor) {
      boQua.push(`${id} (không thấy hộp .tl-box--exp/figure mang data-exp này)`);
      continue;
    }
    inserts.push({ pos: anchor.end, block: renderBlock(id, entry.expTen, video, pool) });
    chen.push(`${id} → ${video.youtube_id}`);
  }

  let out = html;
  for (const { pos, block } of inserts.sort((a, b) => b.pos - a.pos)) {
    out = out.slice(0, pos) + "\n" + block + out.slice(pos);
  }
  return { html: out, chen, boQua };
}

type KiemKetQua = { id: string; ok: boolean; ten?: string; kenh?: string; ghiChu: string; soFile: number };

/**
 * Kiểm mọi `youtube_id` đang dùng bằng oEmbed của YouTube (miễn phí, không cần API key):
 * trả về tiêu đề + tên kênh, HTTP 401/404 nghĩa là video đã xoá hoặc chủ kênh cấm nhúng.
 * Có `--apply` thì ghi `ten`/`kenh`/`da_kiem` ngược lại đúng file JSON.
 */
async function kiemLink(): Promise<void> {
  const daDoc = new Map<string, unknown>(); // file → object đã parse (ghi lại 1 lần)
  const theoId = new Map<string, { files: Set<string>; ghi: ((v: { ten: string; kenh: string; da_kiem: string }) => void)[] }>();
  const them = (id: string, file: string, ghi: (v: { ten: string; kenh: string; da_kiem: string }) => void) => {
    const e = theoId.get(id) ?? { files: new Set<string>(), ghi: [] };
    e.files.add(file);
    e.ghi.push(ghi);
    theoId.set(id, e);
  };
  const doc = (file: string) => {
    if (!daDoc.has(file)) daDoc.set(file, JSON.parse(fs.readFileSync(file, "utf8")));
    return daDoc.get(file) as Record<string, unknown>;
  };

  for (const name of fs.readdirSync(khoDir).sort()) {
    if (!/^tn-.*\.json$/.test(name)) continue;
    const file = path.join(khoDir, name);
    const data = doc(file) as { video?: Record<string, unknown> };
    const id = data.video?.youtube_id;
    if (typeof id !== "string" || !id) continue;
    them(id, file, (v) => Object.assign(data.video as object, v));
  }
  const poolFile = path.join(khoDir, "video-dung-chung.json");
  if (fs.existsSync(poolFile)) {
    const data = doc(poolFile) as { videos?: Record<string, unknown>[] };
    for (const v of data.videos ?? []) {
      const id = v?.youtube_id;
      if (typeof id === "string" && id) them(id, poolFile, (x) => Object.assign(v, x));
    }
  }
  if (theoId.size === 0) {
    console.log("Kho chưa có `youtube_id` nào để kiểm.");
    return;
  }

  const homNay = new Date().toISOString().slice(0, 10);
  const daGhi = new Set<string>();
  const ketQua: KiemKetQua[] = [];

  for (const [id, muc] of theoId) {
    const url = `https://www.youtube.com/oembed?url=${encodeURIComponent(`https://www.youtube.com/watch?v=${id}`)}&format=json`;
    let kq: KiemKetQua;
    try {
      const res = await fetch(url, { headers: { "user-agent": "thachlab-kiem-video" } });
      if (!res.ok) {
        kq = { id, ok: false, ghiChu: `HTTP ${res.status}${res.status === 401 ? " (video đã xoá hoặc cấm nhúng)" : ""}`, soFile: muc.files.size };
      } else {
        const j = (await res.json()) as { title?: string; author_name?: string };
        kq = { id, ok: true, ten: j.title ?? "", kenh: j.author_name ?? "", ghiChu: "OK", soFile: muc.files.size };
        if (APPLY) {
          for (const ghi of muc.ghi) ghi({ ten: kq.ten ?? "", kenh: kq.kenh ?? "", da_kiem: homNay });
          for (const f of muc.files) daGhi.add(f);
        }
      }
    } catch (e) {
      kq = { id, ok: false, ghiChu: `lỗi mạng: ${(e as Error).message}`, soFile: muc.files.size };
    }
    ketQua.push(kq);
  }

  if (JSON_OUT) {
    console.log(JSON.stringify({ kiem: true, apply: APPLY, ketQua }, null, 1));
    return;
  }
  console.log(APPLY ? "── KIỂM LINK (oEmbed) + ĐÃ GHI ──" : "── KIỂM LINK (oEmbed; thêm --apply để ghi ten/kenh/da_kiem) ──");
  for (const k of ketQua) {
    console.log(
      k.ok
        ? `✓ ${k.id}  ${k.kenh || "?"} · ${k.ten || "?"}   [${k.soFile} file]`
        : `✗ ${k.id}  ${k.ghiChu}   [${k.soFile} file]`,
    );
  }
  if (APPLY) for (const f of daGhi) console.log(`   đã ghi: ${path.relative(root, f)}`);
  const hong = ketQua.filter((k) => !k.ok).length;
  console.log(`\n${ketQua.length} link, ${hong} link hỏng.`);
  if (hong > 0) process.exitCode = 1;
}

async function main() {
  if (KIEM) {
    await kiemLink();
    return;
  }
  const kho = docKho();
  const pool = docVideoDungChung();
  if (kho.size === 0) {
    console.log("Kho chưa có thí nghiệm nào gắn field `video` — không có gì để chèn.");
    console.log("Xem quy ước: content/thi-nghiem/README.md (mục Video thí nghiệm).");
    return;
  }

  const lessons = fs
    .readdirSync(lessonRoot, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .sort();

  const baoCao: { bai: string; lessonId?: number | string; files: KetQuaFile[]; ghi: boolean }[] = [];

  // slug → lesson_id, suy từ `nguon_trong_bai` của kho (để --bai nhận cả số lesson_id)
  const idTheoSlug = new Map<string, string>();
  for (const name of fs.readdirSync(khoDir)) {
    if (!/^tn-.*\.json$/.test(name)) continue;
    const data = JSON.parse(fs.readFileSync(path.join(khoDir, name), "utf8"));
    const nguon: string = data.nguon_trong_bai ?? "";
    const m = nguon.match(/lesson-samples\/([^/]+)\//);
    if (m && typeof data.lesson_id !== "undefined") idTheoSlug.set(m[1], String(data.lesson_id));
  }

  for (const slug of lessons) {
    const dir = path.join(lessonRoot, slug);
    const src = path.join(dir, "theory.src.html");
    const html = path.join(dir, "theory.html");
    const bundlePath = path.join(dir, "bundle.json");
    if (!fs.existsSync(html) && !fs.existsSync(src)) continue;

    // lọc theo --bai: khớp tên thư mục, hoặc lesson_id của đúng bài đó
    if (only && slug !== only && idTheoSlug.get(slug) !== only) continue;

    const files: KetQuaFile[] = [];
    let newTheoryHtml: string | null = null;

    for (const file of [src, html]) {
      if (!fs.existsSync(file)) continue;
      const before = fs.readFileSync(file, "utf8");
      const kq = chenVaoHtml(before, kho, pool);
      if (kq.chen.length === 0) {
        if (kq.boQua.length > 0) files.push({ file, chen: [], boQua: kq.boQua });
        continue;
      }
      if (APPLY) fs.writeFileSync(file, kq.html, "utf8");
      files.push({ file, chen: kq.chen, boQua: kq.boQua });
      if (file === html) newTheoryHtml = kq.html;
    }

    // bundle.json: theory_html phải khớp theory.html (validateBundle/upload đọc field này)
    if (APPLY && newTheoryHtml !== null && fs.existsSync(bundlePath)) {
      const bundle = JSON.parse(fs.readFileSync(bundlePath, "utf8"));
      if (bundle.theory_html !== newTheoryHtml) {
        bundle.theory_html = newTheoryHtml;
        fs.writeFileSync(bundlePath, JSON.stringify(bundle, null, 1) + "\n", "utf8");
        files.push({ file: bundlePath, chen: ["theory_html ← theory.html"], boQua: [] });
      }
    }

    if (files.some((f) => f.chen.length > 0)) baoCao.push({ bai: slug, files, ghi: APPLY });
  }

  if (JSON_OUT) {
    console.log(JSON.stringify({ apply: APPLY, soBai: baoCao.length, bai: baoCao }, null, 1));
    return;
  }

  const tong = baoCao.reduce((n, b) => n + b.files.reduce((k, f) => k + f.chen.length, 0), 0);
  console.log(APPLY ? "── ĐÃ GHI ──" : "── XEM THỬ (chưa ghi file; thêm --apply để ghi) ──");
  for (const b of baoCao) {
    console.log(`\n▸ ${b.bai}`);
    for (const f of b.files) {
      for (const c of f.chen) console.log(`   + ${c}   [${path.relative(root, f.file)}]`);
      for (const s of f.boQua) console.log(`   · bỏ qua: ${s}   [${path.relative(root, f.file)}]`);
    }
  }
  console.log(`\n${baoCao.length} bài, ${tong} khối video${APPLY ? " đã chèn" : " sẽ chèn"}.`);
  if (APPLY) {
    console.log("Đăng lên DB (trên Mac): bash scripts/cap-nhat-ly-thuyet-hang-loat.sh <slug>:<lesson_id> …");
  }
}

await main();
