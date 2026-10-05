// Hàm dùng chung cho việc so nội dung lý thuyết giữa FILE và DB, bỏ qua khối video.
// Dùng ở: scripts/update-ly-thuyet-from-bundle.mts (chặn ghi đè), scripts/so-file-voi-db.mts (kiểm loạt).

/** Bỏ mọi khối `.tl-box--video` (kể cả marker `<!--video:…-->`) khỏi HTML. */
export function boKhoiVideoHtml(html: string): string {
  let out = html;
  for (;;) {
    const i = out.indexOf('<div class="tl-box tl-box--video">');
    if (i === -1) break;
    const divRe = /<div\b[^>]*>|<\/div>/g;
    divRe.lastIndex = i;
    let depth = 0;
    let end = -1;
    let m: RegExpExecArray | null;
    while ((m = divRe.exec(out))) {
      if (m[0].startsWith("</")) {
        depth--;
        if (depth === 0) {
          end = m.index + m[0].length;
          break;
        }
      } else {
        depth++;
      }
    }
    if (end === -1) break;
    out = out.slice(0, i) + out.slice(end);
  }
  return out;
}

/** Phần nội dung còn lại sau khi bỏ khối video, đã gộp khoảng trắng để so cho khỏi lệch vô nghĩa. */
export function chuanHoaNgoaiVideo(html: string): string {
  return boKhoiVideoHtml(html)
    .replace(/<!--video:[^>]*-->\s*/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

export function demKhoiVideo(html: string): number {
  return (html.match(/tl-box--video/g) ?? []).length;
}

/** Chỗ khác nhau đầu tiên giữa hai chuỗi đã chuẩn hoá — chỉ in một cửa sổ ngắn quanh chỗ đó. */
export function choKhacDauTien(a: string, b: string): string {
  let i = 0;
  while (i < a.length && i < b.length && a[i] === b[i]) i++;
  const dau = Math.max(0, i - 60);
  const cuoi = i + 140;
  return (
    `  vị trí ký tự ${i}\n` +
    `  DB : …${a.slice(dau, cuoi)}…\n` +
    `  file: …${b.slice(dau, cuoi)}…`
  );
}
