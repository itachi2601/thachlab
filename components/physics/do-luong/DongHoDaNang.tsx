"use client";

/**
 * components/physics/do-luong/DongHoDaNang.tsx — đồng hồ đo điện đa năng hiện số (Gói A, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 3).
 * Gắn vào L10 Bài 2 (lesson 47) và L11 Thực hành đo suất điện động (lesson 45) qua MoPhongPortals khoá "dong-ho-da-nang".
 * Tự dựng, không lấy gì từ trang khác.
 *
 * Học sinh vặn núm (V⎓, V~, A⎓, Ω), chọn thang, cắm que đỏ (10A, mA, VΩ; que đen luôn ở COM), chọn mắc song song / nối tiếp,
 * rồi bấm "Chạm que". Đặt sai thì đồng hồ phản ứng như máy thật: quá thang hiện "1", chập mạch qua lỗ mA đứt cầu chì,
 * thang Ω trên mạch có điện bị cảnh báo; số học trong cham.ts (doDongHo).
 * Xem cách đọc (N6): bốn bước đặt máy cho từng tình huống + nút "Đặt đúng cho em xem". Luyện: tình huống ngẫu nhiên, chỉ lần
 * chạm que ĐẦU TIÊN được tính, đúng 5 lần liên tiếp là xong (L1, L2, L3, L4). Quy tắc UI: N2 (≤ 4 nút mỗi hàng), D2, C1/H4,
 * M1/M7, M4 (✓/✗/⚠ kèm chữ), B4.
 */

import { useState } from "react";
import { ChonCheDo, DAT_LIEN_TIEP, HangChon, phuBtn, useTienDo, type CheDo } from "./chung";
import {
  SO_MAU_DH,
  TEN_DL,
  THANG_DH,
  cauHinhDung,
  doDongHo,
  manHinhDH,
  taoNhiemVuDH,
  type CachMac,
  type CauHinhDH,
  type DaiLuongDH,
  type KetQuaDo,
  type LoCam,
  type NhiemVuDH,
} from "./cham";

const DL_ITEMS: { value: DaiLuongDH; text: string }[] = (["DCV", "ACV", "DCA", "OHM"] as const).map((v) => ({
  value: v,
  text: TEN_DL[v],
}));
const LO_ITEMS: { value: LoCam; text: string }[] = [
  { value: "10A", text: "10A" },
  { value: "mA", text: "mA" },
  { value: "VΩ", text: "VΩ" },
];
const MAC_ITEMS: { value: CachMac; text: string }[] = [
  { value: "song-song", text: "Song song" },
  { value: "noi-tiep", text: "Nối tiếp" },
];
const KHOA = "cach-do";

/* ---------------- Hình đồng hồ ---------------- */

const GOC: Record<DaiLuongDH, [number, number]> = { DCV: [-1, -1], ACV: [1, -1], DCA: [1, 1], OHM: [-1, 1] };
const JACK: { lo: LoCam | "COM"; x: number }[] = [
  { lo: "10A", x: 196 },
  { lo: "mA", x: 240 },
  { lo: "VΩ", x: 284 },
  { lo: "COM", x: 326 },
];

function HinhDongHo({ ch, man, donVi, chiDut }: { ch: CauHinhDH; man: string; donVi: string; chiDut: boolean }) {
  const th = THANG_DH[ch.dl][ch.thang];
  const cx = 92;
  const cy = 136;
  const [gx, gy] = GOC[ch.dl];
  return (
    <svg
      viewBox="0 0 360 196"
      className="block w-full select-none text-ink"
      role="img"
      aria-label={`Đồng hồ đa năng: núm ${TEN_DL[ch.dl]} thang ${th.ten}, que đỏ lỗ ${ch.lo}. Màn hiện ${man} ${donVi}.`}
    >
      <rect
        x={8}
        y={4}
        width={344}
        height={188}
        rx={16}
        fill="var(--color-surface-2)"
        stroke="currentColor"
        strokeWidth={1.4}
      />
      {/* màn hiện số */}
      <rect x={28} y={14} width={304} height={62} rx={8} fill="var(--color-panel)" stroke="var(--color-line-strong)" />
      <text
        x={254}
        y={62}
        textAnchor="end"
        fontSize={40}
        fontFamily="ui-monospace, monospace"
        fontWeight={700}
        fill="currentColor"
      >
        {man}
      </text>
      <text x={316} y={62} textAnchor="end" fontSize={18} fill="currentColor">
        {donVi}
      </text>
      {chiDut && (
        <text x={40} y={38} fontSize={16} fontWeight={700} fill="var(--color-danger)">
          ⚠ cầu chì đứt
        </text>
      )}
      {/* núm xoay */}
      <circle cx={cx} cy={cy} r={30} fill="var(--color-panel)" stroke="currentColor" strokeWidth={1.6} />
      <line
        x1={cx}
        y1={cy}
        x2={cx + gx * 22}
        y2={cy + gy * 22}
        stroke="var(--color-primary)"
        strokeWidth={5}
        strokeLinecap="round"
      />
      {(Object.keys(GOC) as DaiLuongDH[]).map((d) => (
        <text
          key={d}
          x={cx + GOC[d][0] * 52}
          y={cy + GOC[d][1] * 36 + 6}
          textAnchor="middle"
          fontSize={16}
          fontWeight={d === ch.dl ? 700 : 400}
          fill={d === ch.dl ? "var(--color-primary)" : "currentColor"}
        >
          {TEN_DL[d]}
        </text>
      ))}
      {/* lỗ cắm */}
      {JACK.map((j) => {
        const red = j.lo === ch.lo;
        const black = j.lo === "COM";
        return (
          <g key={j.lo}>
            <text x={j.x} y={112} textAnchor="middle" fontSize={16} fill="currentColor">
              {j.lo}
            </text>
            <circle
              cx={j.x}
              cy={140}
              r={13}
              fill={red ? "var(--color-danger)" : black ? "#1f2937" : "var(--color-panel)"}
              stroke="currentColor"
              strokeWidth={1.4}
            />
            {(red || black) && (
              <path
                d={`M${j.x},153 C${j.x},172 ${j.x + (red ? -10 : 10)},178 ${j.x + (red ? -14 : 12)},192`}
                fill="none"
                stroke={red ? "var(--color-danger)" : "#64748b"}
                strokeWidth={4}
              />
            )}
          </g>
        );
      })}
    </svg>
  );
}

/* ---------------- Component chính ---------------- */

function moiNhiemVuNgauNhien(cu?: NhiemVuDH): NhiemVuDH {
  for (let lan = 0; lan < 10; lan++) {
    const nv = taoNhiemVuDH(Math.floor(Math.random() * SO_MAU_DH));
    if (!cu || nv.de !== cu.de) return nv;
  }
  return taoNhiemVuDH(0);
}

const KY_HIEU: Record<KetQuaDo["loai"], { t: string; cls: string }> = {
  dung: { t: "✓ Đúng.", cls: "text-ok" },
  "chua-toi-uu": { t: "≈ Đo được, chưa tốt nhất.", cls: "text-warn" },
  sai: { t: "✗ Chưa đúng.", cls: "text-danger" },
  "nguy-hiem": { t: "⚠ Nguy hiểm.", cls: "text-danger" },
};

export default function DongHoDaNang() {
  const [cheDo, setCheDo] = useState<CheDo>("xem");
  const [iXem, setIXem] = useState(0);
  const [nvLuyen, setNvLuyen] = useState<NhiemVuDH>(() => taoNhiemVuDH(0));
  const [ch, setCh] = useState<CauHinhDH>({ dl: "DCV", thang: 3, lo: "VΩ", mac: "song-song" });
  const [kq, setKq] = useState<KetQuaDo | null>(null);
  const [chiDut, setChiDut] = useState(false);
  const [daTinh, setDaTinh] = useState(false);
  const { tienDo, ghi } = useTienDo("thachlab:do-luong:dong-ho-da-nang:v1");

  const xem = cheDo === "xem";
  const nv = xem ? taoNhiemVuDH(iXem, false) : nvLuyen;
  const th = THANG_DH[ch.dl][ch.thang];
  const td = tienDo[KHOA];

  const doiCh = (p: Partial<CauHinhDH>) => {
    setCh((c) => {
      const n = { ...c, ...p };
      if (p.dl && p.dl !== c.dl) n.thang = THANG_DH[p.dl].length - 1; // đổi đại lượng: về thang lớn nhất cho an toàn
      return n;
    });
    setKq(null);
  };

  const cham = (c: CauHinhDH = ch) => {
    const r = doDongHo(nv, c, chiDut);
    setKq(r);
    if (r.chiDut) setChiDut(true);
    if (!xem && !daTinh) {
      setDaTinh(true);
      ghi(KHOA, r.loai === "dung");
    }
  };

  const doiCheDo = (v: CheDo) => {
    setCheDo(v);
    setKq(null);
    setChiDut(false);
    if (v === "luyen") {
      setNvLuyen((cu) => moiNhiemVuNgauNhien(cu));
      setDaTinh(false);
    }
  };
  const cauMoi = () => {
    setNvLuyen((cu) => moiNhiemVuNgauNhien(cu));
    setKq(null);
    setChiDut(false);
    setDaTinh(false);
  };
  const doiTinhHuong = (d: number) => {
    setIXem((i) => (i + d + SO_MAU_DH) % SO_MAU_DH);
    setKq(null);
    setChiDut(false);
  };

  const dung = cauHinhDung(nv);
  const manCho = ch.dl === "OHM" ? "1" : manHinhDH(0, th);

  return (
    <section
      className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
      aria-label="Đồng hồ đo điện đa năng"
    >
      <h2 className="font-display text-lg font-semibold">Đồng hồ đa năng: đặt máy đúng trước khi đo</h2>
      <div className="mt-3">
        <ChonCheDo value={cheDo} onChange={doiCheDo} />
      </div>

      <div className="mt-3 rounded-xl border border-line bg-surface-2 p-3">
        {xem && (
          <div className="mb-2 flex items-center gap-2">
            <button type="button" className={phuBtn} aria-label="Tình huống trước" onClick={() => doiTinhHuong(-1)}>
              ◀
            </button>
            <p className="flex-1 text-center text-sm text-muted">
              Tình huống {iXem + 1}/{SO_MAU_DH}
            </p>
            <button type="button" className={phuBtn} aria-label="Tình huống sau" onClick={() => doiTinhHuong(1)}>
              ▶
            </button>
          </div>
        )}
        <p className="text-base font-medium">{nv.de}</p>
      </div>

      <div className="mt-3">
        <HinhDongHo ch={ch} man={kq ? kq.man : manCho} donVi={kq ? kq.donVi : th.donVi} chiDut={chiDut} />
      </div>

      <div className="mt-3 space-y-2">
        <HangChon labelTren label="Núm vặn" items={DL_ITEMS} value={ch.dl} onChange={(v) => doiCh({ dl: v })} />
        <HangChon labelTren
          label="Thang"
          items={THANG_DH[ch.dl].map((t, i) => ({ value: i, text: t.ten }))}
          value={ch.thang}
          onChange={(v) => doiCh({ thang: v })}
        />
        <HangChon labelTren label="Que đỏ cắm lỗ (que đen luôn ở COM)" items={LO_ITEMS} value={ch.lo} onChange={(v) => doiCh({ lo: v })} />
        <HangChon labelTren label="Cách mắc que" items={MAC_ITEMS} value={ch.mac} onChange={(v) => doiCh({ mac: v })} />
        <div className="flex gap-2">
          <button
            type="button"
            className="min-h-11 flex-1 rounded-lg bg-primary px-4 text-sm font-semibold text-white"
            onClick={() => cham()}
          >
            Chạm que, đọc số
          </button>
          {chiDut && (
            <button
              type="button"
              className={phuBtn}
              onClick={() => {
                setChiDut(false);
                setKq(null);
              }}
            >
              Thay cầu chì
            </button>
          )}
        </div>
      </div>

      {kq && (
        <p className="mt-3 text-base leading-relaxed" aria-live="polite">
          <span className={`font-semibold ${KY_HIEU[kq.loai].cls}`}>{KY_HIEU[kq.loai].t}</span> {kq.loi}
        </p>
      )}

      {xem ? (
        <div className="mt-3 space-y-2">
          <ol className="space-y-2 text-base leading-relaxed">
            <li className="rounded-lg bg-surface-2 px-3 py-2">
              1. <b>Núm:</b> chọn đại lượng cần đo → <b>{TEN_DL[dung.dl]}</b>
              {dung.dl === "DCV" ? " (một chiều)" : dung.dl === "ACV" ? " (xoay chiều)" : ""}.
            </li>
            <li className="rounded-lg bg-surface-2 px-3 py-2">
              2. <b>Thang:</b> nhỏ nhất mà vẫn lớn hơn giá trị ước lượng → <b>{THANG_DH[dung.dl][dung.thang].ten}</b>.
              Chưa ước lượng được thì bắt đầu từ thang lớn nhất rồi hạ dần.
            </li>
            <li className="rounded-lg bg-surface-2 px-3 py-2">
              3. <b>Que đỏ:</b> lỗ <b>{dung.lo}</b>
              {dung.lo === "VΩ"
                ? " (đo V và Ω)"
                : dung.lo === "mA"
                  ? " (dòng nhỏ hơn 200 mA)"
                  : " (dòng từ 200 mA trở lên)"}
              ; que đen ở COM.
            </li>
            <li className="rounded-lg bg-surface-2 px-3 py-2">
              4. <b>Mắc:</b>{" "}
              {dung.dl === "DCA" ? (
                <>
                  <b>nối tiếp</b>: ngắt mạch một chỗ rồi nối đồng hồ vào chỗ hở.
                </>
              ) : dung.dl === "OHM" ? (
                <>
                  <b>song song</b> hai đầu điện trở đã tháo khỏi mạch, không có điện.
                </>
              ) : (
                <>
                  <b>song song</b>: chạm hai que vào hai cực.
                </>
              )}
            </li>
          </ol>
          <button
            type="button"
            className={`${phuBtn} w-full`}
            onClick={() => {
              setCh(dung);
              setChiDut(false);
              cham(dung);
            }}
          >
            Đặt đúng cho em xem
          </button>
          <p className="text-sm text-muted">
            Thử đặt sai (thang quá nhỏ, que đỏ ở lỗ mA khi đo pin…) để xem đồng hồ phản ứng thế nào.
          </p>
        </div>
      ) : (
        <div className="mt-3 space-y-2">
          {kq && (
            <button
              type="button"
              className="min-h-11 w-full rounded-lg bg-primary px-4 text-sm font-semibold text-white"
              onClick={cauMoi}
            >
              Tình huống khác
            </button>
          )}
          <p className="text-sm text-muted">
            {td?.done ? (
              <span className="font-semibold text-ok">✓ Đã xong nhiệm vụ đặt đồng hồ.</span>
            ) : (
              <>
                Chỉ lần chạm que đầu tiên mỗi tình huống được tính. Đặt đúng liên tiếp{" "}
                {Math.min(td?.streak ?? 0, DAT_LIEN_TIEP)}/{DAT_LIEN_TIEP} lần là xong.
              </>
            )}
          </p>
        </div>
      )}
    </section>
  );
}
