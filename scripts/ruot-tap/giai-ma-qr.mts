// Giải mã QR trong ảnh PNG (vd. trang 4 ruột tập: pdftoppm -r 300 -f 4 -l 4 -png <pdf> q) để chắc mã mở đúng link.
// Chạy: npx tsx scripts/ruot-tap/giai-ma-qr.mts scripts/ruot-tap/out/q-4.png
import jsQR from "jsqr";
import sharp from "sharp";

const file = process.argv[2];
if (!file) throw new Error("Dùng: npx tsx scripts/ruot-tap/giai-ma-qr.mts <ảnh.png>");
const { data, info } = await sharp(file).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
const hit = jsQR(new Uint8ClampedArray(data), info.width, info.height);
console.log(hit ? `QR → ${hit.data}` : "KHÔNG giải mã được QR");
process.exit(hit ? 0 : 1);
