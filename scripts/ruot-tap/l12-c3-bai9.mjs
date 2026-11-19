// Ruột tập VL12 – Chương 3 – Bài 9 · Khái niệm từ trường (lesson id 10). Quyển Chương 3 lớp 12: bài 9 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-c3-bai9.mjs (toàn bộ SVG tự vẽ; nam châm theo hình chuẩn svg_lib.py, đường sức nét đứt, mũi tên chữ V 30°).
// Nội dung theo bài web (book/cache/10.json, tải từ DB 12/11/2026): mục tiêu, dự đoán la bàn điện thoại, II.1–II.4, thí nghiệm
// Oersted, mạt sắt, cảm biến lùi xa nam châm, ba bẫy, Trả bài 4 câu, bài toán mẫu la bàn cạnh dây, thử thách ⭐–⭐⭐⭐, 4 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-c3-bai9.mjs              → scripts/ruot-tap/out/ruot-tap-vl12-c3-bai9.pdf
//       node scripts/ruot-tap/l12-c3-bai9.mjs --hinh       → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-c3-bai9/ để soát chữ/nét
import { dirname as dn, resolve as rs } from 'node:path';
import { fileURLToPath as fu } from 'node:url';
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12c3b9 as H } from './hinh-l12-c3-bai9.mjs';

if (process.argv[2] === '--hinh') {
  const { createRequire } = await import('node:module');
  const { existsSync, mkdirSync, writeFileSync } = await import('node:fs');
  const { dirname, resolve } = await import('node:path');
  const { fileURLToPath, pathToFileURL } = await import('node:url');
  const HERE = dirname(fileURLToPath(import.meta.url));
  const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
  const puppeteer = createRequire(BOOK + 'package.json')('puppeteer-core');
  const F = resolve(HERE, 'fonts') + '/source-sans-3-';
  const css = ['latin', 'latin-ext', 'vietnamese'].flatMap((s) => [400, 700].map((w) => `@font-face{font-family:BV;font-weight:${w};src:url("${pathToFileURL(`${F}${s}-${w}-normal.woff2`).href}")}`)).join('')
    + 'body{margin:0;font-family:BV,sans-serif;zoom:4}.fig{margin:0;width:46mm;border:.3mm solid #d3dbec;border-radius:1.5mm;padding:1mm 1.5mm .6mm;background:#fff}.fig svg{display:block;width:100%;height:auto}figcaption{font-size:2.95mm;color:#5f6a88;line-height:1.3;margin-top:.4mm}';
  const out = resolve(HERE, 'out/hinh-l12-c3-bai9'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  for (const [name, fn] of Object.entries(H)) {
    writeFileSync(out + '/_tmp.html', `<!doctype html><meta charset="utf-8"><style>${css}</style>${fn()}`);
    await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
    await pg.evaluate('document.fonts.ready');
    await (await pg.$('.fig')).screenshot({ path: `${out}/${name}.png` });
    console.log(`${name}.png`);
  }
  await b.close();
  process.exit(0);
}

const K = khoiTao({ bai: 9, lid: 10, ten: 'KHÁI NIỆM TỪ TRƯỜNG', lop: 12, baiDau: 9, sub: 'Vật lí 12 · Chương 3: Từ trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const uT = (s) => nw(m(`${s}\\ \\mu\\mathrm T`));
const Bd = '<i>B</i><sub>đ</sub>', Bday = '<i>B</i><sub>dây</sub>', BdV = (v) => nw(`${Bd} ${m(`=${v}\\ \\mu\\mathrm T`)}`), al = m('\\alpha'), dg = (s) => nw(m(`${s}^\\circ`));

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 9 · KHÁI NIỆM TỪ TRƯỜNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Kể lại thí nghiệm <b>Oersted</b>; nêu ba cặp <b>tương tác từ</b>`)}
${dong(`${ck}Nêu <b>từ trường</b> là gì và cách xác định hướng của nó tại một điểm`)}
${dong(`${ck}Nêu tính chất của <b>đường sức từ</b>; nhận ra từ trường đều`)}
${dong(`${ck}Mô tả độ mạnh từ trường bằng <b>cảm ứng từ</b>; tổng hợp hai từ trường vuông góc`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Mở la bàn trong điện thoại, xoay máy đủ kiểu: kim đỏ vẫn chỉ một phía. Đặt máy sát cửa sắt, kim quay ngoắt. Kim la bàn luôn chỉ về hướng bắc vì:</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', 'Nam châm trong điện thoại hút kim về một phía')}
${opt('B', 'Trái Đất là nam châm khổng lồ, từ trường của nó định hướng kim')}
${opt('C', 'Không khí quanh Trái Đất đẩy kim quay')}
${opt('D', 'Trọng lực kéo đầu nặng của kim về phía bắc')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.laBanCua()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Tương tác từ', '1·4')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Nam châm hút được: sắt, ${f(16)}, ${f(16)}, ${f(16)}.</div>
<div>Mỗi nam châm có hai cực: cực ${f(14)} (N) và cực ${f(14)} (S). Không có nam châm ${f(16)} cực.</div>
<div>Hai cực cùng tên thì ${f(16)}; khác tên thì ${f(16)}. Lực đó gọi là ${f(20)}.</div>
<div style="margin-top:.6mm">Hình bên: cặp (1) ${f(16)} · cặp (2) ${f(16)}</div></div>
${H.tuongTac()}</div>
${box(cau('<b>Làm nhanh.</b> Bẻ đôi một thanh nam châm ở chính giữa: em được gì ở mỗi mảnh?', 1))}
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('THÍ NGHIỆM OERSTED · TỪ TRƯỜNG')}
${h3(1, 'Thí nghiệm Oersted (1820): dây dẫn đặt trên kim nam châm', '2·1')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div><b>Giả thuyết:</b> dòng điện có tác dụng ${f(14)}, tức điện và từ có liên hệ.</div>
<div><b>Làm:</b> kim đứng yên theo hướng Bắc – Nam; căng dây đồng ngay trên kim, song song với kim. Đóng mạch vài giây rồi ngắt; đảo hai đầu pin, làm lại. (Coi dây đồng không nhiễm từ.)</div>
<div><b>Quan sát:</b> chưa có dòng, kim ${f(36)}</div>
<div>đóng mạch, kim ${f(22)}; ngắt mạch, kim ${f(26)}</div>
<div>đảo chiều dòng, kim ${f(36)}</div>
<div><b>Rút ra:</b> dòng điện sinh ra ${f(22)} quanh dây; nó tác dụng ${f(16)} lên kim nên kim quay.</div>
<div><b>Chưa nói được gì:</b> chưa cho biết ${f(40)}</div></div>
${H.oersted()}</div>
<div class="card soft" style="padding:1mm 3mm"><b>Ba cặp có tương tác từ:</b> nam châm – ${f(20)} · nam châm – ${f(20)} · dòng điện – ${f(20)}</div>
${h3(2, 'II.2 · Từ trường và hướng của từ trường', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Từ trường là dạng ${f(18)} tồn tại quanh ${f(20)} và quanh ${f(20)},</div>
<div>biểu hiện bằng ${f(18)} tác dụng lên nam châm hay dòng điện đặt trong nó.</div>
<div>Muốn biết ở một chỗ có từ trường không: đặt ở đó ${f(36)} xem có ${f(30)}</div>
<div><b>Hướng của từ trường</b> tại một điểm: chiều ${f(10)} ${m('\\to')} ${f(10)} của kim nam châm nhỏ nằm ${f(20)} tại đó.</div>
<div><b>Kim làm “đầu dò”:</b> đặt kim nhỏ quanh thanh nam châm, chờ kim đứng yên: đầu N quay ra xa cực ${f(10)}, hướng về cực ${f(10)} của thanh.</div>
</div>
${h3(3, 'Từ trường của dòng điện', '2·3')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Dây thẳng dài:</b> đường sức là những đường ${f(16)}, nằm trong mặt phẳng ${f(22)} với dây, tâm ${f(16)}.</div>
<div><b>Quy tắc nắm tay phải:</b> ngón cái chỉ chiều ${f(22)}, các ngón khum lại chỉ chiều ${f(22)}.</div>
<div><b>Dòng điện tròn:</b> nhìn vào thấy dòng chạy cùng chiều kim đồng hồ là mặt ${f(12)}; ngược chiều là mặt ${f(12)}.</div>
<div><b>Ống dây dài:</b> bên trong là từ trường ${f(14)}.</div></div>
${H.dayThang()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ĐƯỜNG SỨC TỪ · CẢM ỨNG TỪ')}
${h3(1, 'II.3 · Đường sức từ', '3·1')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div><b>Định nghĩa:</b> đường sức từ là đường vẽ sao cho ${f(22)} tại mỗi điểm trùng với ${f(30)}.</div>
<div style="margin-top:.6mm"><b>Bốn tính chất</b> (Tiếp – Kín – Không Cắt – Mau):</div>
<div>• Ngoài nam châm: ra ở cực ${f(12)}, vào ở cực ${f(12)};</div>
<div>&nbsp; trong nam châm đi từ ${f(10)} sang ${f(10)} ${m('\\Rightarrow')} đường cong ${f(14)}.</div>
<div>• Qua mỗi điểm chỉ vẽ được ${f(22)} đường sức (không ${f(14)}).</div>
<div>• Chỗ mau thì từ trường ${f(14)}; chỗ thưa thì ${f(14)}.</div>
<div><b>Từ trường đều:</b> đường sức ${f(14)}, ${f(18)}, ${f(18)};</div>
<div>gặp ở khe giữa hai cực nam châm ${f(14)} và trong lòng ${f(20)}.</div></div>
${H.duongSucThanh()}</div>
${h3(2, 'Thí nghiệm: rắc mạt sắt xem hình dạng đường sức', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> đặt thanh nam châm dưới tấm nhựa trong, rắc mạt sắt mịn, gõ nhẹ mép tấm; lặp lại với hai thanh đặt cùng cực đối diện, rồi với nam châm chữ U.</div>
<div><b>Quan sát:</b> mạt sắt nối thành ${f(26)} — gọi là ${f(20)}. Giữa hai cực chữ U: ${f(30)}</div>
<div><b>Rút ra:</b> từ phổ là ${f(20)}; đường sức từ là ${f(36)}</div>
</div>
${h3(3, 'II.4 · Đo từ trường: cảm ứng từ', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Cảm ứng từ ${m('\\vec B')} là ${f(14)}: hướng là ${f(28)}, độ lớn cho biết từ trường ${f(22)}</div>
<div>Đơn vị: ${f(14)} (T) · ${nw(`${m('1\\ \\mathrm{mT}=')} ${f(14)} T`)} · ${nw(`${m('1\\ \\mu\\mathrm T=')} ${f(14)} T`)} · Trái Đất ở nước ta: vài chục ${m('\\mu\\mathrm T')}.</div>
<div>Nhiều nguồn: từ trường tổng hợp là ${f(30)} các từ trường thành phần.</div>
<table style="margin-top:.6mm"><tr><th style="width:44mm">Hai từ trường</th><th>Độ lớn tổng hợp ${m('B')}</th><th style="width:36mm">Hướng</th></tr>
<tr><td>Cùng phương, cùng chiều</td><td></td><td></td></tr><tr><td>Cùng phương, ngược chiều</td><td></td><td></td></tr>
<tr><td style="height:10mm">Vuông góc (${m('\\vec B_1\\perp\\vec B_2')})</td><td></td><td>${m('\\tan\\alpha=')}</td></tr></table>
</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('SỐ LIỆU · BA CÁI BẪY · TRẢ BÀI')}
${h3(1, 'Thí nghiệm dựng lại: cảm biến lùi xa nam châm', '4·1')}
<div class="fig-side" style="${fs(36)}"><div>
<div style="font-size:var(--fs-sm);line-height:1.35;margin-bottom:.6mm">Lùi cảm biến từ của điện thoại xa dần thanh nam châm; mỗi khoảng cách đọc 3 lần, lấy trung bình.</div>
<table class="tbl-ct"><tr><th>${m('d')} (cm)</th><th>2</th><th>4</th><th>6</th><th>8</th><th>10</th></tr>
<tr><td>${m('B')} (${m('\\mu\\mathrm T')})</td><td>1000</td><td>125</td><td>62</td><td>50</td><td>48</td></tr></table>
<div style="margin-top:.6mm">${m('d')}: 2 ${m('\\to')} 4 cm, ${m('B')} giảm ${f(12)} lần · 4 ${m('\\to')} 8 cm, giảm ${f(12)} lần</div>
<div>Ra xa, số đọc chững lại cỡ ${uT('50')} vì ${f(40)}</div></div>
${H.camBien()}</div>
${h3(2, 'III · Ba cái bẫy hay sập', '4·2')}
<div class="card fig-side" style="${fs(38)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Ra xa thì từ trường hết.”</b> Từ trường chỉ ${f(18)} dần; ở đủ xa dụng cụ không phát hiện ra. Lực từ chỉ xuất hiện khi có ${f(26)}</span></div>
<div class="trap">${ck}<span><b>“Đường sức từ có thật.”</b> Mạt sắt xếp chuỗi là có thật (từ phổ); đường sức là đường vẽ theo ${f(18)}</span></div>
<div class="trap">${ck}<span><b>“Cực từ trùng cực địa lí.”</b> Gần bắc địa lí là cực từ ${f(14)}; trục từ lệch trục quay khoảng ${dg('10')}. Kim la bàn không chỉ đúng kinh tuyến; góc lệch đó gọi là ${f(22)}</span></div></div>
${H.traiDat()}</div>
${h3(3, 'IV · Trả bài 4 câu', '4·3')}
${box(`${tb('1. Nam châm có mấy cực? Hai nam châm tương tác với nhau thế nào?')}${lines(1)}
${tb('2. Từ trường là gì? Làm sao biết có từ trường ở một chỗ?')}${lines(1)}
${tb('3. Hướng của từ trường tại một điểm được quy ước thế nào?')}${lines(1)}
${tb('4. Định nghĩa, bốn tính chất của đường sức từ; từ trường đều?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/4 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·4')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: la bàn đặt cạnh dây dẫn', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">La bàn nằm ngang đặt dưới dây dẫn thẳng nằm theo phương bắc – nam; thành phần nằm ngang của từ trường Trái Đất ${BdV('30')} hướng bắc.<br><b>a)</b> Có dòng điện: từ trường của dây nằm ngang, vuông góc ${Bd}, độ lớn ${m('B_1')}; kim lệch ${dg('53')} ${nw(`(${m('\\tan53^\\circ\\approx1{,}33')})`)}. Tính ${m('B_1')}.<br><b>b)</b> Quay dây cho từ trường của dây hướng đúng về bắc, vẫn độ lớn ${m('B_1')}: cảm ứng từ tổng hợp; kim có lệch?<br><b>c)</b> Giảm dòng để từ trường của dây còn ${uT('30')}, vẫn vuông góc ${Bd}: cảm ứng từ tổng hợp, góc lệch của kim.</div>
<div class="fig-side" style="${fs(40)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('\\tan\\alpha=')} ……… ${m('\\Rightarrow')} <i>B</i><sub>1</sub> =`, 2)}${wl(`b) hai từ trường ${f(26)} ${m('\\Rightarrow')} ${m('B=')}`, 1)}${wl(`c) hai từ trường ${f(26)} ${m('\\Rightarrow')} ${m('B=')}`, 1)}${wl(`&nbsp;&nbsp;&nbsp; ${m('\\tan\\alpha=')}`, 1)}</div>${H.vectoMau()}</div>
${h3(2, 'Điền bước còn thiếu: thêm dây thứ hai', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;min-height:5mm;line-height:1.35"><b>Bước 1 (cho sẵn):</b> ${Bd} = ${uT('30')} hướng bắc; dây thứ nhất tạo ${uT('40')} hướng bắc; dây thứ hai tạo ${uT('30')} hướng đông.</div>
${wl(`Bước 2: thành phần bắc = ${f(16)} ; thành phần đông = ${f(16)} ${m('\\Rightarrow')} ${m('B=')}`, 1)}${wl(`Bước 3: ${m('\\tan\\alpha=')} ${f(14)} ${m('\\Rightarrow')} kim lệch ${f(14)} về phía ${f(14)}`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Hai cách biết trong phòng có từ trường khác ngoài từ trường Trái Đất?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Hai thanh nam châm thẳng hàng, hai cực N quay vào nhau: giữa hai cực, chỗ nào từ trường bằng 0, chỗ nào mạnh nhất?`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Tăng dần dòng điện trong dây đặt trên la bàn: kim lệch tới đâu? Có lệch quá ${dg('90')} được không?`, 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Chiều từ trường và độ mạnh quanh thanh nam châm',
    de: `Thanh nam châm thẳng nằm ngang, cực N bên phải, cực S bên trái. M: phía trên, chính giữa thanh (ngoài thanh); P: trên đường thẳng chứa thanh, bên phải cực N; Q: chính giữa, bên trong thanh.<br><b>a)</b> tại M, P, Q từ trường hướng sang trái hay sang phải<br><b>b)</b> A gần cực N có đường sức mau, B ở xa có đường sức thưa: từ trường ở đâu mạnh hơn<br><b>c)</b> chuỗi mạt sắt cong quanh thanh có phải chính là đường sức từ không`,
    nd: `Ngoài thanh đi từ ${f(10)} sang ${f(10)}; trong thanh đi từ ${f(10)} sang ${f(10)}; mau thì ${f(14)}`, a: ['a<sub>M</sub>', 'a<sub>P</sub>', 'a<sub>Q</sub>', 'b', 'c'], cot: 5, gi: 8, fig: H.thanhD1() },
  { t: 'Dạng 2 · Dễ · Chiều từ trường quanh dây thẳng (nắm tay phải)',
    de: `Dây dẫn thẳng dài vuông góc với trang giấy, dòng điện hướng ra phía người nhìn. Kim nam châm nhỏ trong mặt phẳng trang: A bên phải dây, cách ${nw('2 cm')}; B phía trên dây, cách ${nw('2 cm')}; C bên trái dây, cách ${nw('6 cm')}.<br><b>a)</b> chiều từ trường tại A, B, C (lên, xuống, sang trái, sang phải)<br><b>b)</b> đảo chiều dòng điện: chiều từ trường tại A<br><b>c)</b> từ trường tại B hay C mạnh hơn; vì sao`,
    nd: `Đường sức là đường tròn ${f(28)} khi nhìn từ phía người nhìn; chiều từ trường là ${f(22)} của đường tròn`, a: ['a<sub>A</sub>', 'a<sub>B</sub>', 'a<sub>C</sub>', 'b', 'c'], cot: 5, gi: 7, fig: H.dayD2() },
  { t: 'Dạng 3 · Trung bình · La bàn dưới dây: tổng hợp hai từ trường vuông góc',
    de: `La bàn nằm ngang; ${BdV('40')} hướng bắc. Dây thẳng dài nằm ngang theo phương bắc – nam, ngay phía trên la bàn; dòng điện chạy từ nam đến bắc thì kim lệch ${dg('37')} về phía tây. Chỉ xét từ trường của dây và của Trái Đất; từ trường của dây tại kim nằm ngang. Lấy ${nw(m('\\tan37^\\circ\\approx0{,}754'))}, ${nw(m('\\cos37^\\circ\\approx0{,}799'))}.<br><b>a)</b> cảm ứng từ ${Bday} của dây tại la bàn<br><b>b)</b> cảm ứng từ tổng hợp tại kim<br><b>c)</b> đảo chiều dòng điện (độ lớn không đổi): kim lệch về phía nào, bao nhiêu độ`,
    nd: `Kim chỉ theo vectơ ${f(16)}; ${nw(`${m('\\tan\\alpha=')} ${f(16)}`)}; ${nw(`${m('B=')} ${f(22)}`)}`, a: ['a', 'b', 'c'], gi: 6, fig: H.laBanD3() },
  { t: 'Dạng 4 · Khó · Hai dây quanh la bàn: chiều từ trường rồi tổng hợp',
    de: `Hai dây thẳng dài, nằm ngang theo phương bắc – nam: dây (1) ngay phía trên la bàn, dây (2) ngay phía dưới; ${BdV('40')} hướng bắc. Riêng dây (1) có dòng nam ${m('\\to')} bắc thì từ trường của nó tại la bàn là ${nw(`${m('B_1=30\\ \\mu\\mathrm T')}`)}. Cho dòng vào cả hai: dây (1) nam ${m('\\to')} bắc, dây (2) bắc ${m('\\to')} nam, kim lệch ${dg('45')} về phía tây. Từ trường của mỗi dây tại kim đều nằm ngang.<br><b>a)</b> chiều từ trường của mỗi dây tại la bàn<br><b>b)</b> cảm ứng từ ${m('B_2')} của dây (2) tại la bàn<br><b>c)</b> đổi chiều dòng ở dây (2), độ lớn giữ nguyên: cảm ứng từ tổng hợp và góc lệch của kim; lệch về phía nào`,
    nd: `Nắm tay phải cho ${f(16)} dây; cùng phương thì cộng/trừ ${f(14)}, rồi tổng hợp với ${Bd} bằng ${f(16)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], cot: 5, gi: 6, fig: H.haiDayD4() },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở (thầy chốt 10/11), ô đáp số cuối dòng của ý; đáp số tính bằng Python 12/11/2026.
const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const chi = 'Chỉ xét từ trường của dây và của Trái Đất; từ trường của dây tại kim nằm ngang.';
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Thanh nam châm thẳng đặt đứng, cực N ở trên, cực S ở dưới. M: bên phải, ngang chính giữa thanh (ngoài thanh); P: trên đường thẳng chứa thanh, phía trên cực N; Q: chính giữa, bên trong thanh.<br><b>a)</b> tại M, P, Q từ trường hướng lên hay xuống<br><b>b)</b> hai thanh nam châm giống hệt đặt thẳng hàng, hai cực N đối diện nhau: từ trường tại trung điểm O giữa hai cực bằng bao nhiêu`, o: ['a<sub>M</sub>', 'a<sub>P</sub>', 'a<sub>Q</sub>', 'b'], ow: { 'a<sub>M</sub>': 16, 'a<sub>P</sub>': 16, 'a<sub>Q</sub>': 16, b: 22 } },
    { t: 'Dạng 1 · Bài 2', de: `Nam châm chữ U đặt nằm ngang, hai đầu cực đối diện nhau qua một khe hẹp: cực N bên trái, cực S bên phải.<br><b>a)</b> trong khe, từ trường hướng sang trái hay sang phải<br><b>b)</b> đường sức trong khe có dạng gì; từ trường ở đó gọi là gì<br><b>c)</b> hai đường sức trong khe có thể cắt nhau không; vì sao`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { a: 20, 'b<sub>1</sub>': 30, 'b<sub>2</sub>': 25, c: 25 } },
    { t: 'Dạng 2 · Bài 1', de: `Dây dẫn thẳng dài vuông góc với trang giấy, dòng điện đi vào trang. Kim nam châm nhỏ: A bên trái dây, cách ${nw('3 cm')}; B phía dưới dây, cách ${nw('3 cm')}; C bên phải dây, cách ${nw('1 cm')}.<br><b>a)</b> chiều từ trường tại A, B, C (lên, xuống, sang trái, sang phải)<br><b>b)</b> từ trường tại A hay C mạnh hơn`, fig: H.dayTT(), fw: 36, o: ['a<sub>A</sub>', 'a<sub>B</sub>', 'a<sub>C</sub>', 'b'], ow: 16 },
    { t: 'Dạng 2 · Bài 2', de: `Dây dẫn thẳng đứng xuyên qua mặt bàn nằm ngang, dòng điện đi từ dưới lên. Nhìn từ trên xuống.<br><b>a)</b> đường sức trên mặt bàn có dạng gì; quay cùng hay ngược chiều kim đồng hồ<br><b>b)</b> điểm D ở phía đông của dây: từ trường tại D hướng bắc, nam, đông hay tây<br><b>c)</b> đảo chiều dòng điện: từ trường tại D hướng nào`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: { 'a<sub>1</sub>': 22, 'a<sub>2</sub>': 22, b: 18, c: 18 } },
    nhap(6),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `La bàn nằm ngang; ${BdV('36')} hướng bắc. Dây thẳng dài nằm ngang theo phương bắc – nam, ngay phía trên la bàn; dòng điện chạy từ bắc đến nam thì kim lệch ${dg('30')}. ${chi} Lấy ${nw(m('\\tan30^\\circ\\approx0{,}577'))}, ${nw(m('\\cos30^\\circ\\approx0{,}866'))}.<br><b>a)</b> kim lệch về phía đông hay tây<br><b>b)</b> cảm ứng từ ${Bday} của dây tại la bàn<br><b>c)</b> cảm ứng từ tổng hợp tại kim`, o: ['a', 'b', 'c'], ow: { a: 18 } },
    { t: 'Dạng 3 · Bài 2', de: `La bàn nằm ngang; ${BdV('30')} hướng bắc. Dây thẳng dài nằm ngang theo phương bắc – nam, ngay phía dưới la bàn, dòng điện chạy từ nam đến bắc; từ trường của dây tại la bàn ${uT('40')}. ${chi} Lấy ${m('\\tan 53^\\circ\\approx 1{,}33')}.<br><b>a)</b> kim lệch về phía đông hay tây<br><b>b)</b> cảm ứng từ tổng hợp tại kim<br><b>c)</b> góc lệch của kim so với hướng bắc`, o: ['a', 'b', 'c'], ow: { a: 18 } },
    { t: 'Dạng 4 · Bài 1', de: `Hai dây thẳng dài, nằm ngang theo phương bắc – nam: dây (1) ngay phía trên la bàn, dây (2) ngay phía dưới; cả hai có dòng chạy từ nam đến bắc. ${BdV('40')} hướng bắc; tại la bàn, từ trường của dây (1) là ${uT('50')}, của dây (2) là ${uT('20')}, đều nằm ngang.<br><b>a)</b> chiều từ trường của dây (1), dây (2) tại la bàn (đông/tây)<br><b>b)</b> cảm ứng từ tổng hợp của hai dây; hướng<br><b>c)</b> cảm ứng từ tổng hợp tại kim; kim lệch bao nhiêu độ, về phía nào`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'a<sub>1</sub>': 14, 'a<sub>2</sub>': 14, b: 22, 'c<sub>1</sub>': 18, 'c<sub>2</sub>': 22 } },
    { t: 'Dạng 4 · Bài 2', de: `Như dạng 4: dây (1) ngay phía trên la bàn, dòng nam ${m('\\to')} bắc, từ trường của nó tại la bàn ${uT('20')}; ${BdV('30')} hướng bắc. Thêm dòng vào dây (2) ngay phía dưới, chạy bắc ${m('\\to')} nam: kim lệch ${dg('53')} ${nw(`(${m('\\tan53^\\circ\\approx1{,}33')})`)}. Từ trường mỗi dây tại kim nằm ngang.<br><b>a)</b> chiều từ trường của dây (2) tại la bàn<br><b>b)</b> cảm ứng từ ${m('B_2')} của dây (2) tại la bàn<br><b>c)</b> đổi chiều dòng ở dây (2), độ lớn giữ nguyên: cảm ứng từ tổng hợp tại kim; kim chỉ hướng nào`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { a: 18, b: 20, 'c<sub>1</sub>': 20, 'c<sub>2</sub>': 20 } },
    nhap(3),
  ]],
  dap: [
    `D1·1: a<sub>M</sub>) xuống · a<sub>P</sub>) lên · a<sub>Q</sub>) lên · b) bằng 0 (hai từ trường bằng nhau, ngược chiều) &nbsp;|&nbsp; D1·2: a) sang phải · b<sub>1</sub>) thẳng, song song, cách đều · b<sub>2</sub>) từ trường đều · c) không, mỗi điểm chỉ một hướng từ trường &nbsp;|&nbsp; D2·1: a<sub>A</sub>) lên · a<sub>B</sub>) sang trái · a<sub>C</sub>) xuống · b) C (gần dây hơn) &nbsp;|&nbsp; D2·2: a<sub>1</sub>) đường tròn, tâm trên dây · a<sub>2</sub>) ngược chiều kim đồng hồ · b) bắc · c) nam`,
    `D3·1: a) đông · b) ≈ 20,8 ${m('\\mu')}T · c) ≈ 41,6 ${m('\\mu')}T &nbsp;|&nbsp; D3·2: a) đông · b) 50 ${m('\\mu')}T · c) ≈ 53° &nbsp;|&nbsp; D4·1: a<sub>1</sub>) tây · a<sub>2</sub>) đông · b) 30 ${m('\\mu')}T, hướng tây · c<sub>1</sub>) 50 ${m('\\mu')}T · c<sub>2</sub>) ≈ 37° về phía tây &nbsp;|&nbsp; D4·2: a) tây · b) ≈ 20 ${m('\\mu')}T · c<sub>1</sub>) ≈ 30 ${m('\\mu')}T · c<sub>2</sub>) hướng bắc (không lệch)`,
  ],
};

const HERE = dn(fu(import.meta.url));
await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'tương tác từ 1·4 · Oersted 2·1 · từ trường 2·2 · dòng điện 2·3 · đường sức 3·1 · mạt sắt 3·2 · cảm ứng từ 3·3 · số liệu 4·1 · bẫy 4·2 · bài toán mẫu 5·1 · dạng 1–2 → 6·1 · dạng 3–4 → 7·1',
  out: process.argv[2] ?? rs(HERE, 'out/ruot-tap-vl12-c3-bai9.pdf'),
});
