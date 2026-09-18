/**
 * Dựng một file .docx mẫu (zip, entry để trần) để kiểm thử bộ đọc đề Word.
 * Không cần thư viện ngoài: tự ghi local header + central directory.
 */

const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[i] = c >>> 0;
  }
  return table;
})();

function crc32(bytes) {
  let c = 0xffffffff;
  for (const b of bytes) c = CRC_TABLE[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

/** entries: [{ name, data: Uint8Array }] → Uint8Array của file zip. */
export function makeZip(entries) {
  const enc = new TextEncoder();
  const chunks = [];
  const central = [];
  let offset = 0;

  for (const { name, data } of entries) {
    const nameBytes = enc.encode(name);
    const crc = crc32(data);
    const local = new Uint8Array(30 + nameBytes.length);
    const lv = new DataView(local.buffer);
    lv.setUint32(0, 0x04034b50, true);
    lv.setUint16(4, 20, true);
    lv.setUint16(8, 0, true); // stored
    lv.setUint32(14, crc, true);
    lv.setUint32(18, data.length, true);
    lv.setUint32(22, data.length, true);
    lv.setUint16(26, nameBytes.length, true);
    local.set(nameBytes, 30);

    const head = new Uint8Array(46 + nameBytes.length);
    const cv = new DataView(head.buffer);
    cv.setUint32(0, 0x02014b50, true);
    cv.setUint16(4, 20, true);
    cv.setUint16(6, 20, true);
    cv.setUint16(10, 0, true);
    cv.setUint32(16, crc, true);
    cv.setUint32(20, data.length, true);
    cv.setUint32(24, data.length, true);
    cv.setUint16(28, nameBytes.length, true);
    cv.setUint32(42, offset, true);
    head.set(nameBytes, 46);
    central.push(head);

    chunks.push(local, data);
    offset += local.length + data.length;
  }

  const centralSize = central.reduce((n, c) => n + c.length, 0);
  const end = new Uint8Array(22);
  const ev = new DataView(end.buffer);
  ev.setUint32(0, 0x06054b50, true);
  ev.setUint16(8, central.length, true);
  ev.setUint16(10, central.length, true);
  ev.setUint32(12, centralSize, true);
  ev.setUint32(16, offset, true);

  const all = [...chunks, ...central, end];
  const total = all.reduce((n, c) => n + c.length, 0);
  const out = new Uint8Array(total);
  let p = 0;
  for (const c of all) {
    out.set(c, p);
    p += c.length;
  }
  return out;
}

const NS =
  'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" ' +
  'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" ' +
  'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ' +
  'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" ' +
  'xmlns:v="urn:schemas-microsoft-com:vml" ' +
  'xmlns:o="urn:schemas-microsoft-com:office:office"';

const p = (runs) => `<w:p>${runs}</w:p>`;
const t = (text) => `<w:r><w:t xml:space="preserve">${text}</w:t></w:r>`;
const tab = '<w:r><w:tab/></w:r>';

/** v = s/t bằng Office Math (đúng thứ Word sinh ra khi gõ Alt+=). */
const FRACTION =
  '<m:oMath><m:r><m:t>v</m:t></m:r><m:r><m:t>=</m:t></m:r>' +
  '<m:f><m:num><m:r><m:t>s</m:t></m:r></m:num><m:den><m:r><m:t>t</m:t></m:r></m:den></m:f></m:oMath>';

/** a₀ + √(2gh) — mũ, chỉ số, căn, ký hiệu Hy Lạp. */
const RADICAL =
  '<m:oMath><m:sSub><m:e><m:r><m:t>a</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub>' +
  '<m:r><m:t>+</m:t></m:r><m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/>' +
  '<m:e><m:r><m:t>2gh</m:t></m:r></m:e></m:rad><m:r><m:t>·α</m:t></m:r></m:oMath>';

/** Công thức MathType còn ở dạng OLE — chỉ là ảnh WMF, không đọc được. */
const MATHTYPE_OLE =
  '<w:r><w:object><v:shape><v:imagedata r:id="rId9"/></v:shape>' +
  '<o:OLEObject Type="Embed" ProgID="Equation.DSMT4" r:id="rId9"/></w:object></w:r>';

const DRAWING_IMAGE =
  '<w:r><w:drawing><wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">' +
  '<a:graphic><a:graphicData><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">' +
  '<pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill></pic:pic></a:graphicData></a:graphic>' +
  "</wp:inline></w:drawing></w:r>";

// PNG 1×1 trong suốt
const PNG_BASE64 =
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=";

const DOCUMENT = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document ${NS}><w:body>
${p(t("SỞ GD&amp;ĐT — ĐỀ KIỂM TRA GIỮA KỲ I — Thời gian 45 phút"))}
${p(t("PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn"))}
${p(t("Câu 1. Công thức tính tốc độ trung bình là ") + FRACTION + t(" đúng không?"))}
${p(t("A. 1 m/s") + tab + t("*B. 2 m/s") + tab + t("C. 3 m/s") + tab + t("D. 4 m/s"))}
${p(t("Lời giải: Tốc độ trung bình bằng quãng đường chia thời gian."))}
${p(t("Câu 2. Cho hình vẽ bên, đại lượng ") + RADICAL + t(" có giá trị nào sau đây?") )}
${p(DRAWING_IMAGE)}
<w:tbl>
  <w:tr><w:tc>${p(t("A. 5"))}</w:tc><w:tc>${p(t("B. 6"))}</w:tc><w:tc>${p(t("*C. 7"))}</w:tc><w:tc>${p(t("D. 8"))}</w:tc></w:tr>
</w:tbl>
${p(t("Câu 3. Biểu thức ") + MATHTYPE_OLE + t(" nào sau đây đúng?"))}
${p(t("A. x") + tab + t("B. y") + tab + t("C. z") + tab + t("D. t"))}
${p(t("Đáp án: D"))}
${p(t("PHẦN II. Câu trắc nghiệm đúng sai"))}
${p(t("Câu 4. Xét chuyển động rơi tự do:"))}
${p(t("*a) Gia tốc không đổi."))}
${p(t("b) Vận tốc không đổi."))}
${p(t("*c) Quãng đường tỉ lệ với bình phương thời gian."))}
${p(t("d) Thời gian rơi phụ thuộc khối lượng."))}
${p(t("PHẦN III. Câu trắc nghiệm trả lời ngắn"))}
${p(t("Câu 5. Vật rơi từ độ cao 20 m, lấy g = 10 m/s². Thời gian rơi (s) là bao nhiêu?"))}
${p(t("Đáp án: 2"))}
</w:body></w:document>`;

const RELS = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>
<Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/oleObject" Target="embeddings/oleObject1.bin"/>
</Relationships>`;

export function sampleDocx() {
  const enc = new TextEncoder();
  return makeZip([
    { name: "[Content_Types].xml", data: enc.encode('<?xml version="1.0"?><Types/>') },
    { name: "word/document.xml", data: enc.encode(DOCUMENT) },
    { name: "word/_rels/document.xml.rels", data: enc.encode(RELS) },
    { name: "word/media/image1.png", data: Uint8Array.from(Buffer.from(PNG_BASE64, "base64")) },
    { name: "word/embeddings/oleObject1.bin", data: new Uint8Array([1, 2, 3, 4]) },
  ]);
}
