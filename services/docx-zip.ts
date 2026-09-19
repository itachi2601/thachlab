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
