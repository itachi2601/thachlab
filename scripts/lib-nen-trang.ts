// Đưa NỀN ảnh về trắng, giữ nguyên hình: cắt khung viền đồng màu, phóng 3× (Lanczos), nền (màu phổ biến nhất) → trắng.
// Dùng chung cho lam-trang-nen-anh.mts (ảnh trong thư mục cau/) và nen-trang-theo-url.mts (ảnh theo URL Storage).
import sharp from "sharp";

export const SCALE = 3;

export async function lamTrangNen(input: string | Buffer): Promise<{ png: Buffer; bg: number[] }> {
  const { data, info } = await sharp(input).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const { width: w, height: h } = info;
  const cnt = new Map<number, { n: number; r: number; g: number; b: number }>();
  for (let y = 0; y < h; y++)
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 3;
      const k = (data[i] >> 3) * 1024 + (data[i + 1] >> 3) * 32 + (data[i + 2] >> 3);
      const e = cnt.get(k) ?? { n: 0, r: 0, g: 0, b: 0 };
      e.n++; e.r += data[i]; e.g += data[i + 1]; e.b += data[i + 2]; cnt.set(k, e);
    }
  const bg = [...cnt.values()].sort((a, b) => b.n - a.n)[0];
  const B = [bg.r / bg.n, bg.g / bg.n, bg.b / bg.n];
  // Khung viền: dải mép đồng màu (độ lệch < 2) mà khác nền > 6 → cắt (+1 px), kẻo sau khi nền thành trắng khung hiện thành viền đen.
  const lum = (x: number, y: number) => data[(y * w + x) * 3 + 1];
  const lineOk = (pts: [number, number][]) => {
    const v = pts.map(([x, y]) => lum(x, y));
    const m = v.reduce((a, b) => a + b, 0) / v.length;
    const sd = Math.sqrt(v.reduce((a, b) => a + (b - m) ** 2, 0) / v.length);
    return sd < 2 && Math.abs(m - B[1]) > 6;
  };
  let t = 0, bt = 0, l = 0, r = 0;
  const row = (y: number): [number, number][] => Array.from({ length: w }, (_, x) => [x, y]);
  const col = (x: number): [number, number][] => Array.from({ length: h }, (_, y) => [x, y]);
  while (t < h / 4 && lineOk(row(t))) t++;
  while (bt < h / 4 && lineOk(row(h - 1 - bt))) bt++;
  while (l < w / 4 && lineOk(col(l))) l++;
  while (r < w / 4 && lineOk(col(w - 1 - r))) r++;
  const pad = (n: number) => (n ? n + 1 : 0);
  const crop = { left: pad(l), top: pad(t), width: w - pad(l) - pad(r), height: h - pad(t) - pad(bt) };
  const big = await sharp(input).removeAlpha().extract(crop).resize({ width: crop.width * SCALE, kernel: "lanczos3" }).raw().toBuffer({ resolveWithObject: true });
  const out = Buffer.alloc(big.data.length);
  for (let i = 0; i < big.data.length; i += 3) {
    const rr = Math.min(255, (big.data[i] * 255) / B[0]);
    const gg = Math.min(255, (big.data[i + 1] * 255) / B[1]);
    const bb = Math.min(255, (big.data[i + 2] * 255) / B[2]);
    const white = rr > 238 && gg > 238 && bb > 238;
    out[i] = white ? 255 : rr; out[i + 1] = white ? 255 : gg; out[i + 2] = white ? 255 : bb;
  }
  const png = await sharp(out, { raw: { width: big.info.width, height: big.info.height, channels: 3 } }).png({ compressionLevel: 9 }).toBuffer();
  return { png, bg: B.map(Math.round) };
}
