/**
 * Đọc file .docx (thực chất là một file zip) ngay trong trình duyệt — không thêm
 * thư viện ngoài, vì web xuất tĩnh nên mọi thứ chạy ở máy người dùng.
 *
 * Chỉ cần đủ cho OOXML: entry để trần (method 0) hoặc nén deflate (method 8),
 * giải nén bằng DecompressionStream có sẵn của trình duyệt.
 */

const EOCD_SIG = 0x06054b50;
const CENTRAL_SIG = 0x02014b50;

export type ZipEntries = Map<string, Uint8Array>;

async function inflateRaw(data: Uint8Array): Promise<Uint8Array> {
  if (typeof DecompressionStream === "undefined")
    throw new Error(
      "Trình duyệt này không giải nén được .docx — dùng Chrome/Edge/Safari bản mới.",
    );
  const stream = new Blob([data as BlobPart])
    .stream()
    .pipeThrough(new DecompressionStream("deflate-raw"));
  return new Uint8Array(await new Response(stream).arrayBuffer());
}

/** Vị trí End Of Central Directory — quét ngược từ cuối file. */
function findEocd(view: DataView, len: number): number {
  const floor = Math.max(0, len - (0xffff + 22));
  for (let i = len - 22; i >= floor; i--) {
    if (view.getUint32(i, true) === EOCD_SIG) return i;
  }
  return -1;
}

export async function unzip(bytes: Uint8Array): Promise<ZipEntries> {
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const eocd = findEocd(view, bytes.byteLength);
  if (eocd === -1) throw new Error("File không phải .docx (không thấy cấu trúc zip).");

  const count = view.getUint16(eocd + 10, true);
  const centralOffset = view.getUint32(eocd + 16, true);
  if (centralOffset === 0xffffffff)
    throw new Error("File .docx dùng định dạng zip64 — lưu lại bằng Word rồi thử lại.");

  const decoder = new TextDecoder("utf-8");
  const entries: ZipEntries = new Map();
  let p = centralOffset;

  for (let i = 0; i < count; i++) {
    if (p + 46 > bytes.byteLength || view.getUint32(p, true) !== CENTRAL_SIG) break;
    const method = view.getUint16(p + 10, true);
    const compressedSize = view.getUint32(p + 20, true);
    const nameLen = view.getUint16(p + 28, true);
    const extraLen = view.getUint16(p + 30, true);
    const commentLen = view.getUint16(p + 32, true);
    const localOffset = view.getUint32(p + 42, true);
    const name = decoder.decode(bytes.subarray(p + 46, p + 46 + nameLen));

    // Header cục bộ mới là nơi biết dữ liệu bắt đầu ở đâu (phần extra thường khác
    // phần extra trong central directory).
    const localNameLen = view.getUint16(localOffset + 26, true);
    const localExtraLen = view.getUint16(localOffset + 28, true);
    const start = localOffset + 30 + localNameLen + localExtraLen;
    const raw = bytes.subarray(start, start + compressedSize);

    if (method === 0) entries.set(name, raw);
    else if (method === 8) entries.set(name, await inflateRaw(raw));
    // method khác (bzip2, lzma…): Word không dùng — bỏ qua entry đó.

    p += 46 + nameLen + extraLen + commentLen;
  }

  return entries;
}

// ---------- Ghi zip (chiều ngược — dựng .docx để tải xuống) ----------
// Zip tối thiểu cho .docx: local header + central directory + EOCD, không zip64
// (file bài học nhỏ, không cần). Nén deflate-raw qua CompressionStream có sẵn
// của trình duyệt khi có; không có thì lưu "store" (method 0) — Word đọc được cả hai.

const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(data: Uint8Array): number {
  let c = 0xffffffff;
  for (let i = 0; i < data.length; i++) c = CRC_TABLE[(c ^ data[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

async function deflateRaw(data: Uint8Array): Promise<Uint8Array | null> {
  if (typeof CompressionStream === "undefined") return null;
  const stream = new Blob([data as BlobPart]).stream().pipeThrough(new CompressionStream("deflate-raw"));
  return new Uint8Array(await new Response(stream).arrayBuffer());
}

export interface ZipInputEntry {
  name: string;
  data: Uint8Array;
}

export async function zip(entries: ZipInputEntry[]): Promise<Uint8Array> {
  const encoder = new TextEncoder();
  const chunks: Uint8Array[] = [];
  const central: Uint8Array[] = [];
  let offset = 0;

  for (const entry of entries) {
    const nameBytes = encoder.encode(entry.name);
    const crc = crc32(entry.data);
    const compressed = await deflateRaw(entry.data);
    const method = compressed ? 8 : 0;
    const payload = compressed ?? entry.data;

    const local = new DataView(new ArrayBuffer(30));
    local.setUint32(0, 0x04034b50, true);
    local.setUint16(4, 20, true);
    local.setUint16(6, 0, true);
    local.setUint16(8, method, true);
    local.setUint16(10, 0, true);
    local.setUint16(12, 0, true);
    local.setUint32(14, crc, true);
    local.setUint32(18, payload.length, true);
    local.setUint32(22, entry.data.length, true);
    local.setUint16(26, nameBytes.length, true);
    local.setUint16(28, 0, true);
    chunks.push(new Uint8Array(local.buffer), nameBytes, payload);

    const centralHeader = new DataView(new ArrayBuffer(46));
    centralHeader.setUint32(0, 0x02014b50, true);
    centralHeader.setUint16(4, 20, true);
    centralHeader.setUint16(6, 20, true);
    centralHeader.setUint16(8, 0, true);
    centralHeader.setUint16(10, method, true);
    centralHeader.setUint16(12, 0, true);
    centralHeader.setUint16(14, 0, true);
    centralHeader.setUint32(16, crc, true);
    centralHeader.setUint32(20, payload.length, true);
    centralHeader.setUint32(24, entry.data.length, true);
    centralHeader.setUint16(28, nameBytes.length, true);
    centralHeader.setUint16(30, 0, true);
    centralHeader.setUint16(32, 0, true);
    centralHeader.setUint16(34, 0, true);
    centralHeader.setUint16(36, 0, true);
    centralHeader.setUint32(38, 0, true);
    centralHeader.setUint32(42, offset, true);
    central.push(new Uint8Array(centralHeader.buffer), nameBytes);

    offset += 30 + nameBytes.length + payload.length;
  }

  const centralStart = offset;
  const centralSize = central.reduce((n, c) => n + c.length, 0);

  const eocd = new DataView(new ArrayBuffer(22));
  eocd.setUint32(0, 0x06054b50, true);
  eocd.setUint16(8, entries.length, true);
  eocd.setUint16(10, entries.length, true);
  eocd.setUint32(12, centralSize, true);
  eocd.setUint32(16, centralStart, true);

  const all = [...chunks, ...central, new Uint8Array(eocd.buffer)];
  const total = all.reduce((n, p) => n + p.length, 0);
  const out = new Uint8Array(total);
  let p = 0;
  for (const part of all) {
    out.set(part, p);
    p += part.length;
  }
  return out;
}
