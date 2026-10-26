// Tải clip hiện tượng tự dựng/tự quay lên Storage (bucket lesson-clips) thay cho YouTube, rồi ghi vào kho thí nghiệm.
// Quy tắc: docs/QUY-TAC-THIET-KE.md V9 · kế hoạch: docs/KE-HOACH-CLIP-ANH-DONG.md
//
//   npx tsx scripts/tai-clip-len-storage.mts <clip.mp4> --tn <id-thi-nghiem> [--anh-bia 8] \
//       [--nhan "..."] [--nhin-vao "..."]            # xem thử: kiểm file, tạo ảnh bìa, không ghi gì
//   ... --apply                                       # tải mp4 + ảnh bìa lên, ghi `video` vào content/thi-nghiem/<id>.json
//
// Sau đó: npx tsx scripts/chen-video-thi-nghiem.mts --bai <slug> [--apply] để chèn <video> vào bài.
// Vì sao không YouTube: tải tay mất công; API YouTube của dự án chưa qua kiểm duyệt chỉ cho video "Riêng tư"
// (học sinh không xem được); thẻ <video preload="none"> không kéo ~1 MB JS và không gợi ý video khác (V5, G2).
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { createClient } from "@supabase/supabase-js";

const argv = process.argv.slice(2);
const opt = (n: string) => {
  const i = argv.indexOf(n);
  return i >= 0 ? argv[i + 1] : undefined;
};
const APPLY = argv.includes("--apply");
const file = argv.find((a) => a.endsWith(".mp4"));
const tn = opt("--tn");
const giayBia = Number(opt("--anh-bia") ?? "1"); // khung đầu: không lộ kết luận clip
// Bucket riêng cho clip (mp4 + ảnh bìa webp); lesson-media chỉ nhận ảnh.
const BUCKET = opt("--bucket") ?? "lesson-clips";
if (!file || !tn || !fs.existsSync(file)) {
  console.error("Dùng: npx tsx scripts/tai-clip-len-storage.mts <clip.mp4> --tn <id> [--anh-bia giây] [--apply]");
  process.exit(1);
}

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const khoFile = path.join(root, "content/thi-nghiem", `${tn}.json`);
if (!fs.existsSync(khoFile)) {
  console.error(`✗ Không thấy ${khoFile}`);
  process.exit(1);
}

// .env.local nằm ở repo chính; worktree thì lấy qua git common dir.
function readEnv(name: string): string | undefined {
  if (process.env[name]) return process.env[name];
  const common = path.resolve(root, execFileSync("git", ["rev-parse", "--git-common-dir"], { cwd: root }).toString().trim());
  for (const dir of [root, path.dirname(common)]) {
    const p = path.join(dir, ".env.local");
    if (!fs.existsSync(p)) continue;
    const m = new RegExp(`^${name}=(.*)$`, "m").exec(fs.readFileSync(p, "utf8"));
    if (m) return m[1].trim().replace(/^["']|["']$/g, "");
  }
}

const ffmpeg = (() => {
  try {
    return execFileSync("python3", ["-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"]).toString().trim();
  } catch {
    return "ffmpeg";
  }
})();

// ---- kiểm clip theo V9 ----
const kb = Math.round(fs.statSync(file).size / 1024);
const info = (() => {
  try {
    execFileSync(ffmpeg, ["-hide_banner", "-i", file], { stdio: "pipe" });
  } catch (e) {
    return String((e as { stderr?: Buffer }).stderr ?? "");
  }
  return "";
})();
const dm = /Duration: (\d+):(\d+):([\d.]+)/.exec(info);
const giay = dm ? Number(dm[1]) * 3600 + Number(dm[2]) * 60 + Number(dm[3]) : NaN;
const coTieng = /Audio:/.test(info);
const loi: string[] = [];
if (!(giay >= 8 && giay <= 30)) loi.push(`thời lượng ${giay.toFixed(1)} s ngoài 8–30 s (V9)`);
if (kb > 3072) loi.push(`${kb} KB > 3 MB — nén lại (crf cao hơn / 720p)`);
console.log(`clip: ${path.basename(file)} · ${giay.toFixed(1)} s · ${kb} KB · ${coTieng ? "có tiếng" : "không tiếng"}`);
if (loi.length) {
  for (const l of loi) console.error("✗ " + l);
  process.exit(1);
}

// ---- ảnh bìa ----
const bia = path.join(os.tmpdir(), path.basename(file).replace(/\.mp4$/, "-bia.webp"));
execFileSync(ffmpeg, ["-y", "-loglevel", "error", "-ss", String(giayBia), "-i", file, "-frames:v", "1",
  "-vf", "scale=960:-2", "-quality", "70", bia]);
console.log(`ảnh bìa: ${bia} · ${Math.round(fs.statSync(bia).size / 1024)} KB (giây ${giayBia})`);

const ngay = new Date().toISOString().slice(0, 10).replace(/-/g, "");
const dich = { mp4: `clip/${tn}-${ngay}.mp4`, bia: `clip/${tn}-${ngay}.webp` };
console.log(`đích: ${BUCKET}/${dich.mp4} + ${dich.bia}`);
if (!APPLY) {
  console.log("(xem thử — thêm --apply để tải lên và ghi kho)");
  process.exit(0);
}

const url = readEnv("NEXT_PUBLIC_SUPABASE_URL");
const key = readEnv("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) {
  console.error("✗ thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local");
  process.exit(1);
}
const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
async function tai(local: string, dst: string, contentType: string): Promise<string> {
  const { error } = await sb.storage.from(BUCKET).upload(dst, fs.readFileSync(local), {
    contentType,
    cacheControl: "31536000",
    upsert: false,
  });
  if (error) throw new Error(`${dst}: ${error.message}`);
  return sb.storage.from(BUCKET).getPublicUrl(dst).data.publicUrl;
}
const mp4Url = await tai(file, dich.mp4, "video/mp4");
const biaUrl = await tai(bia, dich.bia, "image/webp");
const kt = await fetch(mp4Url, { method: "HEAD" });
console.log(`✓ đã tải: ${mp4Url} (HEAD ${kt.status})`);

// ---- ghi kho, giữ kiểu thụt lề của file ----
const raw = fs.readFileSync(khoFile, "utf8");
const data = JSON.parse(raw);
data.video = {
  ...(data.video ?? {}),
  mp4: mp4Url,
  poster: biaUrl,
  ...(opt("--nhan") ? { nhan: opt("--nhan") } : {}),
  ...(opt("--nhin-vao") ? { nhin_vao: opt("--nhin-vao") } : {}),
  giay: Math.round(giay),
  nguon: "tự dựng",
  da_kiem: new Date().toISOString().slice(0, 10),
};
// Ghi đè đúng mục "video" bằng chữ, giữ nguyên kiểu trình bày phần còn lại (dung_cu… viết gọn một dòng/đối tượng).
const indent = /\n( +)"/.exec(raw)?.[1].length ?? 2;
const pad = " ".repeat(indent);
const khoi = `${pad}"video": ` + JSON.stringify(data.video, null, indent).replace(/\n/g, `\n${pad}`);
let moi = raw.replace(new RegExp(`,?\\n${pad}"video": \\{[^{}]*\\}`), "");
moi = moi.replace(/\s*\}\s*$/, `,\n${khoi}\n}`) + (raw.endsWith("\n") ? "\n" : "");
JSON.parse(moi);
fs.writeFileSync(khoFile, moi, "utf8");
console.log(`✓ ghi video vào ${path.relative(root, khoFile)}`);
