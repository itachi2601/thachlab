// Nhập BẢNG ĐỀ XUẤT VIDEO đã được thầy duyệt (markdown) vào kho dữ liệu JSON.
// Nhờ script này mà không ai phải chép tay `youtube_id` từ bảng vào JSON (chỗ dễ sai nhất).
//
//   npx tsx scripts/nhap-video-de-xuat.mts content/thi-nghiem/video-de-xuat-l11-chuong2.md            # xem thử
//   npx tsx scripts/nhap-video-de-xuat.mts <bảng.md> --ra /tmp/kho-thu                                # ghi ra kho tạm
//   npx tsx scripts/nhap-video-de-xuat.mts <bảng.md> --apply                                           # ghi vào kho thật
//
// Quy trình chuẩn (bảng chưa duyệt thì KHÔNG nhập gì):
//   1. nhập ra kho tạm  → 2. `chen-video-thi-nghiem.mts --kiem --kho <kho tạm>` kiểm link còn sống
//   → 3. `--apply` vào kho thật → 4. `chen-video-thi-nghiem.mts --apply` chèn vào bài → 5. đăng lô.
//
// Cột nhận theo TÊN ở dòng tiêu đề (đổi thứ tự được): `Bài`, `Vị trí`, `Link`, `Nhãn`,
// `Nhìn vào`, `Duyệt?`, `start–end`. Chỉ dòng có `Duyệt?` = x/✓/có mới được nhập.
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
const bangPath = argv.find((a) => !a.startsWith("--") && a !== opt("--kho") && a !== opt("--ra"));
const khoDir = path.resolve(root, opt("--kho") || "content/thi-nghiem");
const raDir = opt("--ra") ? path.resolve(root, opt("--ra") as string) : null;

if (!bangPath || !fs.existsSync(bangPath)) {
  console.error("Dùng: npx tsx scripts/nhap-video-de-xuat.mts <bảng.md> [--kho <dir>] [--ra <dir>] [--apply]");
  process.exit(1);
}
if (APPLY && raDir) {
  console.error("Chọn một: --apply (ghi kho thật) hoặc --ra <dir> (ghi kho tạm).");
  process.exit(1);
}

/** Ghi JSON giữ đúng kiểu trình bày của file gốc (indent + có/không newline cuối). */
function ghiJsonGiuDinhDang(file: string, obj: unknown): void {
  const raw = fs.readFileSync(file, "utf8");
  const m = /\n( +)"/.exec(raw);
  const indent = m ? m[1].length : 1;
  fs.writeFileSync(file, JSON.stringify(obj, null, indent) + (raw.endsWith("\n") ? "\n" : ""), "utf8");
}

/** Lấy id 11 ký tự từ link YouTube (watch / youtu.be / embed / shorts / live). */
function youtubeIdTuLink(link: string): string | null {
  const s = link.trim().replace(/[),.;]+$/, "");
  if (/^[\w-]{11}$/.test(s)) return s;
  const m =
    /[?&]v=([\w-]{11})/.exec(s) ??
    /youtu\.be\/([\w-]{11})/.exec(s) ??
    /\/embed\/([\w-]{11})/.exec(s) ??
    /\/(?:shorts|live)\/([\w-]{11})/.exec(s);
  return m ? m[1] : null;
}

/** `1:10–2:05` | `70-125` | `1:10` → [giây bắt đầu, giây kết thúc?] */
function phutGiay(s: string): number | null {
  const t = s.trim();
  if (!t) return null;
  const m = /^(?:(\d+):)?(\d+)(?::(\d+))?$/.exec(t);
  if (!m) return null;
  const [a, b, c] = [m[1], m[2], m[3]];
  if (c !== undefined) return Number(a) * 3600 + Number(b) * 60 + Number(c);
  if (a !== undefined) return Number(a) * 60 + Number(b);
  return Number(b);
}

function tachKhoang(s: string): { bat_dau?: number; ket_thuc?: number } {
  const t = s.trim();
  if (!t) return {};
  const phan = t.split(/[–—~]|\s+-\s+|\s+đến\s+/i).map((x) => x.trim()).filter(Boolean);
  const bat_dau = phan[0] ? phutGiay(phan[0]) : null;
  const ket_thuc = phan[1] ? phutGiay(phan[1]) : null;
  return {
    ...(bat_dau !== null ? { bat_dau } : {}),
    ...(ket_thuc !== null ? { ket_thuc } : {}),
  };
}

const DUYET = /^\s*(x|✓|✔|v|có|co|yes|y|ok)\s*$/i;

/** Object JSON trong kho: `tn-*.json` có `video`, `video-theo-bai.json` có `bai[]`. */
type VideoJson = Record<string, unknown>;
type BaiEntry = { slug: string; lesson_id?: number; videos: { vi_tri: string; video: VideoJson }[] };
type KhoObj = { bai?: BaiEntry[]; video?: VideoJson } & Record<string, unknown>;

type Dong = Record<string, string>;
function docBang(md: string): { dong: Dong[]; thieuDuyet: number; loi: string[] } {
  const lines = md.split("\n").filter((l) => l.trim().startsWith("|"));
  const loi: string[] = [];
  if (lines.length < 2) return { dong: [], thieuDuyet: 0, loi: ["Bảng không có dòng dữ liệu nào."] };
  const cat = (l: string) =>
    l.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((x) => x.replace(/[*`]/g, "").trim());
  const header = cat(lines[0]);
  const dong: Dong[] = [];
  let thieuDuyet = 0;
  for (const l of lines.slice(1)) {
    const cells = cat(l);
    if (cells.every((c) => /^:?-{2,}:?$/.test(c))) continue; // dòng kẻ |---|---|
    const o: Dong = {};
    header.forEach((h, i) => (o[h] = cells[i] ?? ""));
    if (!Object.values(o).some((v) => v)) continue;
    if (!DUYET.test(o["Duyệt?"] ?? "")) {
      thieuDuyet++;
      continue;
    }
    dong.push(o);
  }
  return { dong, thieuDuyet, loi };
}

function main() {
  const md = fs.readFileSync(bangPath as string, "utf8");
  const { dong, thieuDuyet, loi } = docBang(md);
  const ra = raDir ?? khoDir;
  if (!fs.existsSync(ra)) fs.mkdirSync(ra, { recursive: true });

  // slug → lesson_id (tra từ kho thật, để mở bài ghi kèm lesson_id)
  const idTheoSlug = new Map<string, number>();
  for (const name of fs.readdirSync(khoDir)) {
    if (!/^tn-.*\.json$/.test(name)) continue;
    const d = JSON.parse(fs.readFileSync(path.join(khoDir, name), "utf8"));
    const m = /lesson-samples\/([^/]+)\//.exec(d.nguon_trong_bai ?? "");
    if (m && typeof d.lesson_id !== "undefined") idTheoSlug.set(m[1], d.lesson_id);
  }

  const daGhi = new Map<string, { obj: KhoObj; goc: string }>(); // file đích → object
  const nhan = (file: string): { obj: KhoObj; goc: string } => {
    if (!daGhi.has(file)) {
      const goc = fs.existsSync(file) ? file : path.join(ra, path.basename(file));
      const obj: KhoObj = fs.existsSync(goc)
        ? (JSON.parse(fs.readFileSync(goc, "utf8")) as KhoObj)
        : { bai: [] };
      daGhi.set(file, { obj, goc });
    }
    return daGhi.get(file)!;
  };

  const ok: string[] = [];
  const bo: string[] = [];
  const daDungTrongBang = new Set<string>(); // `${slug}|${youtube_id}` — chặn 2 dòng cùng bài dùng 1 clip
  for (const d of dong) {
    const slug = (d["Bài"] ?? "").trim();
    const viTri = (d["Vị trí"] ?? "").trim();
    const id = youtubeIdTuLink(d["Link"] ?? "");
    if (!slug || !viTri || !id) {
      bo.push(`thiếu Bài/Vị trí/Link hợp lệ (${JSON.stringify(d).slice(0, 120)})`);
      continue;
    }
    if (!(d["Nhìn vào"] ?? "").trim()) {
      bo.push(`${slug} ${viTri}: thiếu "Nhìn vào"`);
      continue;
    }
    // Cùng một clip xuất hiện 2 lần trong một bài là lỗi ÂM THẦM: script chèn sẽ bỏ qua
    // (vì bài đã có id đó) mà không ai biết. Chặn ngay ở đây, cả 2 kiểu: trùng trong bảng
    // và trùng với clip đã nằm sẵn trong HTML của bài.
    if (daDungTrongBang.has(`${slug}|${id}`)) {
      bo.push(`${slug} ${viTri}: clip ${id} đã dùng ở một dòng khác của cùng bài — chọn clip khác`);
      continue;
    }
    const htmlBai = path.join(root, "content", "lesson-samples", slug, "theory.html");
    if (fs.existsSync(htmlBai) && fs.readFileSync(htmlBai, "utf8").includes(id)) {
      bo.push(`${slug} ${viTri}: clip ${id} đã nằm trong bài (chèn tay hoặc dòng khác) — chọn clip khác`);
      continue;
    }
    daDungTrongBang.add(`${slug}|${id}`);
    const { bat_dau, ket_thuc } = tachKhoang(d["start–end"] ?? "");
    const video: Record<string, unknown> = { youtube_id: id };
    const nhanVideo = (d["Nhãn"] ?? "").trim();
    if (nhanVideo) video.nhan = nhanVideo;
    video.nhin_vao = (d["Nhìn vào"] ?? "").trim();
    if (bat_dau !== undefined) video.giay_bat_dau = bat_dau;
    if (ket_thuc !== undefined) video.giay_ket_thuc = ket_thuc;

    if (viTri === "mo_bai") {
      const file = path.join(khoDir, "video-theo-bai.json");
      const { obj } = nhan(file);
      obj.bai = obj.bai ?? [];
      let b = obj.bai.find((x) => x.slug === slug);
      if (!b) {
        b = { slug, ...(idTheoSlug.has(slug) ? { lesson_id: idTheoSlug.get(slug) } : {}), videos: [] };
        obj.bai.push(b);
      }
      b.videos = (b.videos ?? []).filter((x) => x.vi_tri !== viTri);
      b.videos.push({ vi_tri: viTri, video });
    } else {
      const f = path.join(khoDir, `${viTri}.json`);
      if (!fs.existsSync(f)) {
        bo.push(`${slug} ${viTri}: không có file ${viTri}.json trong kho`);
        continue;
      }
      const { obj } = nhan(f);
      obj.video = video;
    }
    ok.push(`${slug} ${viTri} → ${id}${bat_dau !== undefined ? ` [${bat_dau}s–${ket_thuc ?? "?"}s]` : ""}`);
  }

  if (JSON_OUT) {
    console.log(JSON.stringify({ bang: bangPath, apply: APPLY, ra, nhan: ok, bo, thieuDuyet, loi }, null, 1));
    return;
  }
  console.log(`Bảng: ${path.relative(root, bangPath as string)}`);
  for (const l of loi) console.log(`✗ ${l}`);
  for (const o of ok) console.log(`✓ ${o}`);
  for (const b of bo) console.log(`· bỏ: ${b}`);
  console.log(
    `\n${ok.length} dòng được nhập, ${thieuDuyet} dòng chưa duyệt (bỏ qua), ${bo.length} dòng lỗi.`,
  );

  if (ok.length === 0) return;
  if (APPLY) {
    for (const [file, { obj }] of daGhi) {
      ghiJsonGiuDinhDang(file, obj);
      console.log(`   đã ghi: ${path.relative(root, file)}`);
    }
    console.log("\nKiểm link + điền tên kênh: npx tsx scripts/chen-video-thi-nghiem.mts --kiem --apply");
  } else if (raDir) {
    for (const [file, { obj }] of daGhi) {
      const out = path.join(raDir, path.basename(file));
      fs.writeFileSync(out, JSON.stringify(obj, null, 1) + "\n", "utf8");
      console.log(`   đã ghi ra kho tạm: ${path.relative(root, out)}`);
    }
    console.log(`\nKiểm link trước khi nhập thật: npx tsx scripts/chen-video-thi-nghiem.mts --kiem --kho ${path.relative(root, raDir)}`);
  } else {
    console.log("\n(xem thử — thêm --ra <dir> để ghi kho tạm, hoặc --apply để ghi kho thật)");
  }
}

main();
