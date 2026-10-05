// Sinh icon PWA (PNG, <20KB mỗi file) từ ô vuông chữ "T" của logo ThachLab.
// Chạy: node scripts/gen-pwa-icons.mjs   (cần sharp có sẵn trong node_modules)
import sharp from "sharp";
import { mkdirSync, statSync } from "node:fs";

const BG = "#05070b"; // --color-bg trong app/globals.css
const BLUE = "#2563eb";
mkdirSync("public/icons", { recursive: true });

// any: ô bo góc xanh trên nền tối; maskable: xanh tràn viền, chữ T nằm trong vùng an toàn (~60% giữa).
function svg({ maskable, size }) {
  const tile = maskable
    ? `<rect width="512" height="512" fill="${BLUE}"/>`
    : `<rect width="512" height="512" fill="${BG}"/><rect x="76" y="76" width="360" height="360" rx="84" fill="${BLUE}"/>`;
  const s = maskable ? 1.0 : 1.2;
  const w = 130 * s;
  const bar = 36 * s;
  const stem = 36 * s;
  const totalH = 186 * s;
  const x0 = 256 - w / 2;
  const y0 = 256 - totalH / 2;
  const t =
    `<rect x="${x0}" y="${y0}" width="${w}" height="${bar}" fill="#fff"/>` +
    `<rect x="${256 - stem / 2}" y="${y0}" width="${stem}" height="${totalH}" fill="#fff"/>`;
  return Buffer.from(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 512 512">${tile}${t}</svg>`,
  );
}

const jobs = [
  ["icon-192.png", 192, false],
  ["icon-512.png", 512, false],
  ["icon-maskable-512.png", 512, true],
  ["apple-touch-icon.png", 180, true], // iOS tự bo góc nên để xanh tràn viền
];
for (const [name, size, maskable] of jobs) {
  const out = `public/icons/${name}`;
  await sharp(svg({ maskable, size })).png({ palette: true, compressionLevel: 9 }).toFile(out);
  console.log(out, statSync(out).size, "bytes");
}
