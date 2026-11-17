import type { ChieuBai } from "./types";

/**
 * MẪU TRÌNH CHIẾU BÀI TẬP MẪU — ống thuỷ ngân cắm ngược trong chậu (bài 12 trên bảng thầy, VD3 "Giọt thuỷ ngân
 * trong ống", 17/11/2026). Đề viết lại từ hình + lời giải trên bảng (28 °C, cột khí 15 cm, chênh 5 cm, p₀ = 76 cmHg
 * → t₂ ≈ 157 °C); thầy soát lại câu chữ đề trước khi dùng thật.
 *
 * Kiểm số: 76·20·301 / (71·15) = 457520 / 1065 = 429,60 K → t₂ = 156,6 °C ≈ 157 °C.
 */
export const MAU_ONG_THUY_NGAN: ChieuBai = {
  nhan: "Ví dụ 3",
  dang: "Khí trong ống có cột thuỷ ngân — nguyên lí Pascal + phương trình trạng thái",
  de_html:
    "Một ống thuỷ tinh tiết diện đều $S$, đầu trên kín, cắm thẳng đứng, miệng dưới ngập trong chậu thuỷ ngân và được giữ cố định. " +
    "Ở $28\\,^\\circ\\text{C}$, cột không khí trong ống dài $15$ cm, mực thuỷ ngân trong ống cao hơn mặt thoáng ngoài chậu $5$ cm. " +
    "Áp suất khí quyển $76$ cmHg, coi mực thuỷ ngân trong chậu không đổi. Phải nung khí trong ống tới nhiệt độ bao nhiêu để mực " +
    "thuỷ ngân trong ống ngang với mặt thoáng ngoài chậu?",
  tom_de: {
    cho: ["$t_1 = 28\\,^\\circ\\text{C}$", "$\\ell_1 = 15$ cm", "Hg trong ống cao hơn ngoài $5$ cm", "$p_0 = 76$ cmHg"],
    tim: ["$t_2 = \\,?$ để mực Hg trong = ngoài"],
  },
  hinh_dau: ["ong1"],
  hinh: ({ lop }) => <HinhOngThuyNgan lop={lop} />,
  bang: {
    hang: [
      { id: "p", nhan: "p", don_vi: "cmHg" },
      { id: "V", nhan: "V" },
      { id: "T", nhan: "T", don_vi: "K" },
    ],
    cot: [
      { id: "1", nhan: "①" },
      { id: "2", nhan: "②" },
    ],
    can_tim: ["T.2"],
  },
  buoc: [
    {
      tieu_de: "Chọn hai điểm cùng mức",
      hoi: "Điểm $A$ trong ống (ngang mặt thoáng ngoài) và điểm $B$ ở mặt thoáng — áp suất hai điểm này so với nhau thế nào?",
      dong: [
        { html: "Nguyên lí Pascal: chất lỏng đứng yên, <b>cùng mức → cùng áp suất</b>.", hinh: ["muc"] },
        { html: "$p_A = p_B = p_0 = 76$ cmHg", kieu: "ket_qua" },
      ],
      tom_tat: "Cùng mức → cùng $p$: $p_A = p_B = 76$ cmHg",
    },
    {
      tieu_de: "Áp suất khí lúc đầu",
      hoi: "$p_1$ lớn hơn hay nhỏ hơn $76$ cmHg? Vì sao?",
      dong: [
        { html: "Trên $A$ có khí ($p_1$) và cột Hg cao $5$ cm đè xuống:", hinh: ["p1"] },
        { html: "$p_A = p_1 + 5$" },
        { html: "$p_1 + 5 = 76 \\;\\Rightarrow\\; p_1 = 71$ cmHg", kieu: "ket_qua", bang: { "p.1": "71", "V.1": "15S" } },
        { html: "Hg trong ống cao hơn ngoài → khí trong ống <b>loãng hơn</b> khí quyển.", kieu: "ghi_chu" },
      ],
      tom_tat: "$p_1 = 76 - 5 = 71$ cmHg, $V_1 = 15S$",
    },
    {
      tieu_de: "Trạng thái 2: mực trong = mực ngoài",
      hoi: "Khi Hg trong ống tụt xuống ngang mặt thoáng, cột khí dài bao nhiêu? Áp suất bao nhiêu?",
      dong: [
        { html: "Ống giữ cố định, mặt Hg tụt $5$ cm: $\\ell_2 = 15 + 5 = 20$ cm", hinh: ["ong2"], bang: { "V.2": "20S" } },
        { html: "Mặt Hg trong ống ngang mặt thoáng → cùng mức:" },
        { html: "$p_2 = p_0 = 76$ cmHg", kieu: "ket_qua", bang: { "p.2": "76" } },
      ],
      tom_tat: "$V_2 = 20S$, $p_2 = 76$ cmHg",
    },
    {
      tieu_de: "Lập bảng — chọn định luật",
      hoi: "Nhìn bảng: $p$, $V$, $T$ cái nào đổi? Dùng định luật nào?",
      dong: [
        { html: "Đổi nhiệt độ sang kelvin: $T_1 = 28 + 273 = 301$ K", bang: { "T.1": "301", "T.2": "t_2+273" } },
        { html: "Cả $p$, $V$, $T$ đều đổi → <b>phương trình trạng thái</b>:" },
        { html: "$\\dfrac{p_1V_1}{T_1} = \\dfrac{p_2V_2}{T_2}$", kieu: "ket_qua" },
      ],
      tom_tat: "$p, V, T$ đều đổi → $\\dfrac{p_1V_1}{T_1} = \\dfrac{p_2V_2}{T_2}$",
    },
    {
      tieu_de: "Thay số",
      hoi: "Có cần đổi cmHg sang Pa không?",
      dong: [
        { html: "$\\dfrac{71 \\times 15S}{301} = \\dfrac{76 \\times 20S}{t_2 + 273}$" },
        { html: "Hai vế cùng đơn vị cmHg và cùng $S$ → <b>không cần đổi</b>, $S$ tự giản ước.", kieu: "ghi_chu" },
        { html: "$t_2 + 273 = \\dfrac{76 \\times 20 \\times 301}{71 \\times 15} \\approx 429{,}6$ K" },
        { html: "$t_2 \\approx 156{,}6 \\approx 157\\,^\\circ\\text{C}$", kieu: "ket_qua", hinh: ["nong"], bang: { "T.2": "429{,}6" } },
      ],
      tom_tat: "$t_2 \\approx 157\\,^\\circ\\text{C}$",
    },
  ],
  dap_so: "$t_2 \\approx 157\\,^\\circ\\text{C}$",
  nhan_dang: "Thấy <b>ống cắm ngược trong chậu chất lỏng</b> → chọn điểm trong ống ngang mặt thoáng ngoài, viết $p_{\\text{trong}} = p_0$.",
  bay: [
    "Cộng/trừ sai chiều cột Hg: Hg trong ống <b>cao hơn</b> ngoài → $p_{\\text{khí}} = p_0 - h$.",
    "Quên đổi $^\\circ\\text{C}$ sang K ở cả hai trạng thái.",
    "Quên cột khí dài thêm khi mặt Hg tụt ($\\ell_2 = 15 + 5$, không phải $15$).",
  ],
};

/** Hình bài ống thuỷ ngân — SVG nét theo theme, các lớp bật dần theo bước. Màu: --s1 trạng thái ①, --s2 trạng thái ②, --key ý chính. */
export function HinhOngThuyNgan({ lop }: { lop: Set<string> }) {
  const on = (id: string) => lop.has(id);
  return (
    <svg viewBox="0 0 360 270" role="img" aria-label="Ống thuỷ tinh cắm ngược trong chậu thuỷ ngân" style={{ width: "100%", height: "auto" }}>
      <defs>
        <marker id="otn-mui" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M1 1 L8 5 L1 9" fill="none" stroke="currentColor" strokeWidth="1.6" />
        </marker>
      </defs>
      {/* Chậu + thuỷ ngân */}
      <path d="M32 160 L50 245 Q50 252 58 252 L302 252 Q310 252 310 245 L328 160 Z" fill="var(--hg)" />
      <path d="M30 150 L50 245 Q50 252 58 252 L302 252 Q310 252 310 245 L330 150" fill="none" stroke="currentColor" strokeWidth="2" />

      {/* Ống ① */}
      <rect x="91" y="41" width="20" height="89" fill="var(--s1-nhat)" />
      <rect x="91" y="130" width="20" height="30" fill="var(--hg)" />
      <path d="M90 228 V40 H112 V228" fill="none" stroke="currentColor" strokeWidth="2" />
      <text x="101" y="28" textAnchor="middle" className="otn-chu" fill="var(--s1)">①</text>
      <g stroke="var(--s1)" strokeWidth="1.6">
        <path d="M76 41 V130 M71 41 H81 M71 130 H81" />
        <path d="M76 132 V160 M71 160 H81" />
      </g>
      <text x="68" y="90" textAnchor="end" className="otn-chu" fill="var(--s1)">15 cm</text>
      <text x="68" y="151" textAnchor="end" className="otn-chu" fill="var(--s1)">5 cm</text>

      {/* Pascal: hai điểm cùng mức */}
      <g className="otn-lop" data-on={on("muc")}>
        <line x1="18" y1="160" x2="342" y2="160" stroke="var(--key)" strokeWidth="2" strokeDasharray="7 5" />
        <circle cx="101" cy="160" r="4" fill="var(--key)" />
        <circle cx="150" cy="160" r="4" fill="var(--key)" />
        <text x="101" y="182" textAnchor="middle" className="otn-chu otn-vien" fill="var(--key)">A</text>
        <text x="150" y="182" textAnchor="middle" className="otn-chu otn-vien" fill="var(--key)">B</text>
        <line x1="166" y1="108" x2="166" y2="152" stroke="currentColor" strokeWidth="1.8" markerEnd="url(#otn-mui)" />
        <text x="174" y="124" className="otn-chu" fill="currentColor">p₀</text>
      </g>

      {/* p₁ trong khí ① */}
      <g className="otn-lop" data-on={on("p1")}>
        <text x="101" y="92" textAnchor="middle" className="otn-chu otn-dam" fill="var(--s1)">p₁</text>
        <line x1="101" y1="133" x2="101" y2="152" stroke="var(--s1)" strokeWidth="1.8" markerEnd="url(#otn-mui)" />
      </g>

      {/* Ống ② — cùng ống, sau khi nung */}
      <g className="otn-lop" data-on={on("ong2")}>
        <line x1="112" y1="40" x2="248" y2="40" stroke="currentColor" strokeWidth="1.2" strokeDasharray="4 4" opacity="0.6" />
        <rect x="249" y="41" width="20" height="119" fill="var(--s2-nhat)" />
        <path d="M248 228 V40 H270 V228" fill="none" stroke="currentColor" strokeWidth="2" />
        <text x="259" y="28" textAnchor="middle" className="otn-chu" fill="var(--s2)">②</text>
        <text x="259" y="104" textAnchor="middle" className="otn-chu otn-dam" fill="var(--s2)">p₂</text>
        <g stroke="var(--s2)" strokeWidth="1.6">
          <path d="M284 41 V160 M279 41 H289 M279 160 H289" />
        </g>
        <text x="293" y="105" className="otn-chu" fill="var(--s2)">20 cm</text>
      </g>

      {/* Đáp số trên hình */}
      <g className="otn-lop" data-on={on("nong")}>
        <text x="259" y="214" textAnchor="middle" className="otn-chu otn-dam otn-vien" fill="var(--s2)">157 °C</text>
      </g>
    </svg>
  );
}
