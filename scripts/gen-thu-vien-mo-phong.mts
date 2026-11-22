/**
 * Sinh lib/data/thu-vien-mo-phong.json cho trang công khai /mo-phong (không gọi DB).
 * Nguồn: content/thi-nghiem (clip), mảng MO_PHONG_TU_DUNG (khai tay), PhET quét từ content/lesson-samples.
 * Chạy: npx tsx scripts/gen-thu-vien-mo-phong.mts
 */
import fs from "node:fs";
import path from "node:path";

import { MO_PHONG_TRANG } from "../lib/mo-phong-trang.ts";

const ROOT = process.cwd();
const TN = path.join(ROOT, "content/thi-nghiem");

export type Loai = "mo_phong" | "clip" | "phet";
const CHU_DE = {
  co: "Cơ học",
  nhiet: "Nhiệt & chất khí",
  dien: "Điện & từ",
  song: "Sóng, âm & ánh sáng",
  hatnhan: "Hạt nhân",
  do: "Đo lường & an toàn",
} as const;
type CD = keyof typeof CHU_DE;

// slug thí nghiệm (đoạn giữa của id) → chủ đề
const SLUG_CD: Record<string, CD> = {
  "an-toan": "do", antoanpx: "do", "sai-so": "do", "lam-quen": "do", thuchanh: "do",
  boylecharles: "nhiet", apsuatdongnang: "nhiet", noinang: "nhiet", pttrangthai: "nhiet", thangnhietdo: "nhiet",
  chuyenthe: "nhiet", tdhphantu: "nhiet", "klr-apsuat": "nhiet",
  camungdt: "dien", dttruong: "dien", luctu: "dien", mayphatdien: "dien", tutruong: "dien", udcamung: "dien",
  ungdungcutu: "dien", xoaychieu: "dien", thuchanhtu: "dien", coulomb: "dien", "cuong-do-dong-dien": "dien",
  "dien-the": "dien", "dien-tro-ohm": "dien", "dien-truong": "dien", "dien-truong-deu": "dien", "do-sdd-pin": "dien",
  "nang-luong-dien": "dien", "nguon-dien": "dien", tudien: "dien", "the-nang-dien": "dien", tatdan: "dien",
  doanmach: "dien", ohm: "dien", congsuat: "dien",
  baitapsong: "song", dotansoam: "song", dotocdoam: "song", giaothoa: "song", motasong: "song", songdientu: "song",
  songdung: "song", songngangdoc: "song", hsgamthanh: "song", khucxa: "song", langkinh: "song", pxtp: "song",
  thaukinh: "song", tieucu: "song", nllk: "song", phanbach: "song",
  hatnhan: "hatnhan", phongxa: "hatnhan",
};

const cdOf = (slug: string): CD => SLUG_CD[slug] ?? "co";

type The = {
  id: string; loai: Loai; ten: string; lop: number; chu_de: CD; nhin_vao: string; href: string;
  nhan_loai: string; lesson_id?: number; poster?: string; mp4?: string; youtube_id?: string;
  giay?: number; nguon?: string; bat_dau?: number; ket_thuc?: number;
};

const nextLogin = (lessonId: number) => `/dang-nhap?next=${encodeURIComponent(`/lop-hoc/bai?id=${lessonId}`)}`;

// ---- 1. Clip thí nghiệm ----
const index = JSON.parse(fs.readFileSync(path.join(TN, "index.json"), "utf8")) as Array<Record<string, unknown>>;
const clips: The[] = [];
const loai: string[] = [];
for (const it of index) {
  if (it.co_video !== true) continue;
  const f = path.join(TN, `${it.id}.json`);
  if (!fs.existsSync(f)) continue;
  const tn = JSON.parse(fs.readFileSync(f, "utf8"));
  const v = tn.video as Record<string, unknown> | undefined;
  if (!v || !it.lesson_id) continue;
  // Clip YouTube mượn thí nghiệm khác (khac_thi_nghiem) = 2 clip nghi sai chờ thầy → loại khỏi thư viện.
  if (v.khac_thi_nghiem) { loai.push(String(it.id)); continue; }
  const slug = String(it.id).split("-").slice(2, -1).join("-");
  const base: The = {
    id: String(it.id),
    loai: "clip",
    ten: String(it.ten),
    lop: Number(it.lop),
    chu_de: cdOf(slug),
    nhin_vao: String(v.nhin_vao ?? ""),
    href: nextLogin(Number(it.lesson_id)),
    nhan_loai: "Clip",
    lesson_id: Number(it.lesson_id),
  };
  if (v.mp4) {
    clips.push({ ...base, mp4: String(v.mp4), poster: String(v.poster), giay: Number(v.giay), nguon: "Tự dựng" });
  } else if (v.youtube_id) {
    clips.push({
      ...base,
      youtube_id: String(v.youtube_id),
      poster: `https://i.ytimg.com/vi/${v.youtube_id}/hqdefault.jpg`,
      nguon: v.kenh ? `YouTube · ${String(v.kenh).trim()}` : "YouTube",
      bat_dau: v.giay_bat_dau as number | undefined,
      ket_thuc: v.giay_ket_thuc as number | undefined,
    });
  }
}

// ---- 2. Mô phỏng tự dựng (khai tay; mỗi cái có trang riêng /mo-phong/<slug>) ----
// Dụng cụ đo của Gói A thêm vào lib/mo-phong-trang.ts là tự có thẻ.
const moPhong: The[] = MO_PHONG_TRANG.map((m) => ({
  id: `mp-${m.slug}`, loai: "mo_phong", ten: m.ten, lop: m.lop, chu_de: m.chu_de, nhin_vao: m.nhin_vao,
  href: `/mo-phong/${m.slug}`, nhan_loai: "Mô phỏng",
}));

// ---- 3. PhET quét từ bài ----
const PHET: Record<string, { ten: string; chu_de: CD; nhin_vao: string }> = {
  "pendulum-lab": { ten: "Phòng thí nghiệm con lắc", chu_de: "co", nhin_vao: "Đổi chiều dài dây, chu kì thay đổi thế nào?" },
  "projectile-motion": { ten: "Chuyển động ném", chu_de: "co", nhin_vao: "Tầm xa thay đổi ra sao khi đổi góc ném?" },
  "collision-lab": { ten: "Phòng thí nghiệm va chạm", chu_de: "co", nhin_vao: "Động lượng tổng trước và sau va chạm." },
  "energy-skate-park-basics": { ten: "Công viên trượt: năng lượng", chu_de: "co", nhin_vao: "Động năng và thế năng đổi chỗ cho nhau ở đâu?" },
  "forces-and-motion-basics": { ten: "Lực và chuyển động", chu_de: "co", nhin_vao: "Hai đội kéo thì hộp đi về phía nào?" },
  "hookes-law": { ten: "Định luật Hooke", chu_de: "co", nhin_vao: "Lực kéo và độ dãn lò xo có tỉ lệ không?" },
  "masses-and-springs": { ten: "Vật nặng và lò xo", chu_de: "co", nhin_vao: "Đổi khối lượng, lò xo dãn bao nhiêu?" },
  "vector-addition": { ten: "Cộng vectơ", chu_de: "co", nhin_vao: "Tổng của hai vectơ nằm ở đâu?" },
  "density": { ten: "Khối lượng riêng", chu_de: "co", nhin_vao: "Vật nào chìm, vật nào nổi trong nước?" },
  "under-pressure": { ten: "Áp suất chất lỏng", chu_de: "co", nhin_vao: "Áp suất tăng thế nào khi xuống sâu?" },
  "energy-forms-and-changes": { ten: "Các dạng năng lượng", chu_de: "nhiet", nhin_vao: "Năng lượng đi từ nguồn tới đâu?" },
  "gas-properties": { ten: "Tính chất của chất khí", chu_de: "nhiet", nhin_vao: "Nung nóng thì áp suất thay đổi ra sao?" },
  "states-of-matter": { ten: "Các trạng thái của vật chất", chu_de: "nhiet", nhin_vao: "Phân tử chuyển động thế nào khi nóng lên?" },
  "diffusion": { ten: "Sự khuếch tán", chu_de: "nhiet", nhin_vao: "Hạt lan sang bên kia nhanh cỡ nào?" },
  "circuit-construction-kit-dc": { ten: "Lắp mạch điện một chiều", chu_de: "dien", nhin_vao: "Đóng công tắc thì dòng điện đi theo đường nào?" },
  "ohms-law": { ten: "Định luật Ôm", chu_de: "dien", nhin_vao: "Tăng điện áp thì cường độ dòng điện đổi ra sao?" },
  "resistance-in-a-wire": { ten: "Điện trở của dây dẫn", chu_de: "dien", nhin_vao: "Dây dài hơn, mảnh hơn thì điện trở thế nào?" },
  "charges-and-fields": { ten: "Điện tích và điện trường", chu_de: "dien", nhin_vao: "Đường sức đi từ điện tích nào tới điện tích nào?" },
  "coulombs-law": { ten: "Định luật Cu-lông", chu_de: "dien", nhin_vao: "Lực thay đổi thế nào khi tăng khoảng cách?" },
  "capacitor-lab-basics": { ten: "Tụ điện", chu_de: "dien", nhin_vao: "Điện tích trên bản tụ thay đổi ra sao?" },
  "faradays-law": { ten: "Định luật Faraday", chu_de: "dien", nhin_vao: "Kéo nam châm nhanh hơn thì bóng đèn sáng thế nào?" },
  "generator": { ten: "Máy phát điện", chu_de: "dien", nhin_vao: "Quay nhanh hơn thì điện áp ra đổi thế nào?" },
  "magnet-and-compass": { ten: "Nam châm và la bàn", chu_de: "dien", nhin_vao: "Kim la bàn chỉ về phía nào quanh nam châm?" },
  "wave-on-a-string": { ten: "Sóng trên dây", chu_de: "song", nhin_vao: "Đổi tần số thì bước sóng thay đổi ra sao?" },
  "sound-waves": { ten: "Sóng âm", chu_de: "song", nhin_vao: "Âm cao hay thấp ứng với sóng thế nào?" },
  "wave-interference": { ten: "Giao thoa sóng", chu_de: "song", nhin_vao: "Hai nguồn gặp nhau, chỗ nào đứng yên?" },
  "bending-light": { ten: "Ánh sáng bị bẻ cong", chu_de: "song", nhin_vao: "Tia sáng gãy về phía nào khi vào nước?" },
  "geometric-optics": { ten: "Quang hình học", chu_de: "song", nhin_vao: "Ảnh thật hay ảo khi dịch vật lại gần thấu kính?" },
  "rutherford-scattering": { ten: "Tán xạ Rơ-dơ-pho", chu_de: "hatnhan", nhin_vao: "Hạt anpha lệch nhiều ở đâu?" },
  "build-an-atom": { ten: "Xây dựng nguyên tử", chu_de: "hatnhan", nhin_vao: "Thêm nơtron thì nguyên tố có đổi không?" },
  "isotopes-and-atomic-mass": { ten: "Đồng vị và khối lượng nguyên tử", chu_de: "hatnhan", nhin_vao: "Khối lượng nguyên tử trung bình thay đổi ra sao?" },
  "alpha-decay": { ten: "Phân rã anpha", chu_de: "hatnhan", nhin_vao: "Hạt nhân con có số proton thế nào?" },
  "beta-decay": { ten: "Phân rã beta", chu_de: "hatnhan", nhin_vao: "Nơtron biến thành hạt nào?" },
};
const phetLop = new Map<string, Set<number>>();
const lessonDirs = fs.readdirSync(path.join(ROOT, "content/lesson-samples"), { withFileTypes: true }).filter((d) => d.isDirectory());
for (const d of lessonDirs) {
  const f = path.join(ROOT, "content/lesson-samples", d.name, "theory.src.html");
  if (!fs.existsSync(f)) continue;
  const lop = Number(/^l(\d+)-/.exec(d.name)?.[1] ?? 0);
  if (!lop) continue;
  for (const m of fs.readFileSync(f, "utf8").matchAll(/phet\.colorado\.edu\/sims\/html\/([a-z0-9-]+)\/latest\//g)) {
    if (!phetLop.has(m[1])) phetLop.set(m[1], new Set());
    phetLop.get(m[1])!.add(lop);
  }
}
const phet: The[] = [];
for (const [slug, lops] of phetLop) {
  const meta = PHET[slug];
  if (!meta) { console.warn("PhET chưa khai:", slug); continue; }
  const lop = Math.min(...lops);
  phet.push({
    id: `phet-${slug}`, loai: "phet", ten: meta.ten, lop, chu_de: meta.chu_de, nhin_vao: meta.nhin_vao,
    href: `https://phet.colorado.edu/sims/html/${slug}/latest/${slug}_all.html?locale=vi`,
    nhan_loai: "PhET", nguon: "PhET, Đại học Colorado Boulder · CC BY 4.0",
  });
}

const the = [...moPhong, ...phet, ...clips];
const out = {
  chu_de: CHU_DE,
  the,
};
fs.writeFileSync(path.join(ROOT, "lib/data/thu-vien-mo-phong.json"), JSON.stringify(out) + "\n");
console.log(`mô phỏng ${moPhong.length} · PhET ${phet.length} · clip ${clips.length} · loại ${loai.length}: ${loai.join(", ")}`);
