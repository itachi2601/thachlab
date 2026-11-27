"use client";

/**
 * Trang điều phối ABET (/quan-tri/abet) — thay cho file Excel "ABET MET - Theo dõi đánh giá SO-PI".
 * - Bảng tiến độ: mỗi dòng PI × học phần, sửa chủ PI/hạn/trạng thái tại chỗ, chép tin nhắn kèm link nộp.
 * - Tổng hợp: % sinh viên đạt theo PI và SO (gộp sinh viên), so với năm đánh giá trước, câu viết sẵn cho báo cáo.
 * - Chi tiết dòng: bảng điểm đã nộp, tệp minh chứng (mở bằng link ký 1 giờ), tải CSV để lưu vào Drive.
 * Dữ liệu: services/abet.ts; quy ước tính: lib/abet.ts.
 */

import { useCallback, useEffect, useMemo, useState } from "react";
import { Check, ChevronDown, ChevronRight, Copy, Download, ExternalLink, Loader2, RefreshCw } from "lucide-react";
import {
  cauBaoCao,
  demDat,
  ketLuan,
  MUC_TIEU_PI,
  namSoSanh,
  NHAN_LOAI_TEP,
  NHAN_TRANG_THAI,
  phanTram,
  tinNhan,
  type DongTongHop,
  type TrangThai,
} from "@/lib/abet";
import { SITE_URL } from "@/lib/site";
import {
  linkTepAbet,
  suaSource,
  taiDuLieuAbet,
  type AbetFile,
  type AbetHistory,
  type AbetScore,
  type AbetSource,
  type SuaSource,
} from "@/services/abet";

const TRANG_THAI: TrangThai[] = ["chua_gui", "da_gui", "da_nop", "da_duyet", "khong_thu_duoc"];
const MAU_TRANG_THAI: Record<TrangThai, string> = {
  chua_gui: "bg-surface-2 text-muted",
  da_gui: "bg-primary-soft text-primary",
  da_nop: "bg-warn/15 text-warn",
  da_duyet: "bg-ok/15 text-ok",
  khong_thu_duoc: "bg-danger/10 text-danger",
};

function linkNop(token: string) {
  return `${SITE_URL}/abet/nop/?ma=${token}`;
}
function homNay() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
function boDau(s: string) {
  return s
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/đ/g, "d")
    .replace(/Đ/g, "D")
    .replace(/[^A-Za-z0-9]/g, "");
}
/** Tên file theo quy ước thư mục minh chứng: PI2.1_CNCTM1_CDCK24_HK2-2526.csv */
function tenCsv(s: AbetSource) {
  const nam = s.nam_hoc.replace(/^20(\d\d)-20(\d\d)$/, "$1$2");
  return `${s.pi}_${boDau(s.hoc_phan)}_${boDau(s.khoa ?? "")}_${s.hoc_ky ?? ""}-${nam}.csv`;
}
function taiCsv(s: AbetSource, diem: AbetScore[]) {
  const dong = ["MSSV,Diem cau PI,Diem toi da,Ti le,Dat"];
  for (const d of [...diem].sort((a, b) => a.mssv.localeCompare(b.mssv))) {
    const tl = s.diem_toi_da ? d.diem / s.diem_toi_da : 0;
    dong.push(`${d.mssv},${d.diem},${s.diem_toi_da ?? ""},${tl.toFixed(3)},${demDat([d.diem], s.diem_toi_da)}`);
  }
  const blob = new Blob(["﻿" + dong.join("\n")], { type: "text/csv;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = tenCsv(s);
  a.click();
  URL.revokeObjectURL(a.href);
}

export default function AbetOverview() {
  const [sources, setSources] = useState<AbetSource[]>([]);
  const [scores, setScores] = useState<AbetScore[]>([]);
  const [files, setFiles] = useState<AbetFile[]>([]);
  const [history, setHistory] = useState<AbetHistory[]>([]);
  const [dangTai, setDangTai] = useState(true);
  const [loi, setLoi] = useState("");
  const [nam, setNam] = useState("2025-2026");
  const [mo, setMo] = useState<number | null>(null);
  const [daChep, setDaChep] = useState<number | null>(null);
  const [daChepBaoCao, setDaChepBaoCao] = useState(false);

  const nap = useCallback(() => {
    taiDuLieuAbet()
      .then((d) => {
        setSources(d.sources);
        setScores(d.scores);
        setFiles(d.files);
        setHistory(d.history);
        setLoi("");
      })
      .catch((e: unknown) => setLoi(e instanceof Error ? e.message : "Không tải được dữ liệu ABET."))
      .finally(() => setDangTai(false));
  }, []);
  useEffect(() => {
    nap();
  }, [nap]);

  const cacNam = useMemo(() => Array.from(new Set(sources.map((s) => s.nam_hoc))).sort(), [sources]);
  const dongNam = useMemo(() => sources.filter((s) => s.nam_hoc === nam), [sources, nam]);
  const diemTheoDong = useMemo(() => {
    const m = new Map<number, AbetScore[]>();
    for (const sc of scores) m.set(sc.source_id, [...(m.get(sc.source_id) ?? []), sc]);
    return m;
  }, [scores]);
  const tepTheoDong = useMemo(() => {
    const m = new Map<number, AbetFile[]>();
    for (const f of files) m.set(f.source_id, [...(m.get(f.source_id) ?? []), f]);
    return m;
  }, [files]);

  function thongKe(s: AbetSource) {
    const d = diemTheoDong.get(s.id) ?? [];
    const dat = demDat(
      d.map((x) => x.diem),
      s.diem_toi_da,
    );
    return { n: d.length, dat, tiLe: d.length && s.diem_toi_da ? dat / d.length : null };
  }

  // Tổng hợp gộp sinh viên: theo PI rồi theo SO, chỉ tính dòng đã nộp/đã duyệt.
  const tongHop = useMemo(() => {
    const truoc = namSoSanh(nam);
    const lichSu = (ma: string) => history.find((h) => h.nam_hoc === truoc && h.ma === ma)?.ti_le ?? null;
    const gom = (key: (s: AbetSource) => string) => {
      const m = new Map<string, { n: number; dat: number }>();
      for (const s of dongNam) {
        const k = key(s);
        const cur = m.get(k) ?? { n: 0, dat: 0 };
        if (s.trang_thai === "da_nop" || s.trang_thai === "da_duyet") {
          const d = diemTheoDong.get(s.id) ?? [];
          cur.n += d.length;
          cur.dat += demDat(
            d.map((x) => x.diem),
            s.diem_toi_da,
          );
        }
        m.set(k, cur);
      }
      return Array.from(m.entries())
        .sort(([a], [b]) => a.localeCompare(b, "vi", { numeric: true }))
        .map(([ma, v]): DongTongHop => ({
          nam_hoc: nam,
          ma,
          so_sv: v.n,
          so_dat: v.dat,
          ti_le: v.n ? v.dat / v.n : null,
          nam_truoc: truoc,
          ti_le_truoc: lichSu(ma),
        }));
    };
    return { pi: gom((s) => s.pi), so: gom((s) => s.so) };
  }, [dongNam, diemTheoDong, history, nam]);

  async function sua(s: AbetSource, patch: SuaSource) {
    setSources((cur) => cur.map((x) => (x.id === s.id ? { ...x, ...patch } : x)));
    try {
      await suaSource(s.id, patch);
    } catch (e) {
      setLoi(e instanceof Error ? e.message : "Không lưu được.");
      nap();
    }
  }

  async function chepTin(s: AbetSource) {
    const text = tinNhan({ ...s, link: linkNop(s.token) });
    try {
      await navigator.clipboard.writeText(text);
      setDaChep(s.id);
      setTimeout(() => setDaChep(null), 2000);
      if (s.trang_thai === "chua_gui") void sua(s, { trang_thai: "da_gui" });
    } catch {
      window.prompt("Chép tin nhắn:", text);
    }
  }

  async function moTep(f: AbetFile) {
    try {
      const url = await linkTepAbet(f.storage_path);
      window.open(url, "_blank", "noopener");
    } catch (e) {
      setLoi(e instanceof Error ? e.message : "Không mở được tệp.");
    }
  }

  async function chepBaoCao() {
    const text = [...tongHop.pi, ...tongHop.so].map(cauBaoCao).filter(Boolean).join("\n");
    await navigator.clipboard.writeText(text || "Chưa có dữ liệu.");
    setDaChepBaoCao(true);
    setTimeout(() => setDaChepBaoCao(false), 2000);
  }

  if (dangTai) {
    return (
      <p className="flex items-center gap-2 p-6 text-muted">
        <Loader2 className="h-5 w-5 animate-spin" /> Đang tải dữ liệu ABET…
      </p>
    );
  }

  const homnay = homNay();
  const dem = (t: TrangThai) => dongNam.filter((s) => s.trang_thai === t).length;
  const treHan = dongNam.filter(
    (s) => s.han_nop && s.han_nop < homnay && (s.trang_thai === "chua_gui" || s.trang_thai === "da_gui"),
  ).length;
  const cacSo = Array.from(new Set(dongNam.map((s) => s.so))).sort();

  return (
    <div className="mx-auto max-w-6xl space-y-6 px-4 py-6 text-ink">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">ABET MET — dữ liệu PI</h1>
          <p className="text-sm text-muted">
            Sinh viên đạt khi điểm câu PI ≥ 60% điểm tối đa; PI/SO đạt khi ≥ {phanTram(MUC_TIEU_PI)} sinh viên đạt.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {cacNam.map((n) => (
            <button
              key={n}
              type="button"
              onClick={() => setNam(n)}
              className={`min-h-10 rounded-lg px-3 text-sm font-medium ${n === nam ? "bg-primary-soft text-primary" : "bg-surface-2 text-muted"}`}
            >
              {n}
            </button>
          ))}
          <button
            type="button"
            onClick={nap}
            className="flex min-h-10 items-center gap-1 rounded-lg border border-line px-3 text-sm text-muted"
            aria-label="Tải lại"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
      </header>

      {loi ? <p className="rounded-lg bg-danger/10 p-3 text-danger">{loi}</p> : null}

      <div className="flex flex-wrap gap-2 text-sm">
        {TRANG_THAI.map((t) => (
          <span key={t} className={`rounded-full px-3 py-1 ${MAU_TRANG_THAI[t]}`}>
            {NHAN_TRANG_THAI[t]}: {dem(t)}
          </span>
        ))}
        {treHan ? (
          <span className="rounded-full bg-danger/10 px-3 py-1 text-danger">Quá hạn chưa nộp: {treHan}</span>
        ) : null}
      </div>

      {/* ───────── Tổng hợp ───────── */}
      <section className="rounded-2xl border border-line bg-panel p-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-lg font-semibold">Tổng hợp {nam}</h2>
          <button
            type="button"
            onClick={chepBaoCao}
            className="flex min-h-10 items-center gap-1 rounded-lg border border-line px-3 text-sm"
          >
            {daChepBaoCao ? <Check className="h-4 w-4 text-ok" /> : <Copy className="h-4 w-4" />} Chép câu cho báo cáo
          </button>
        </div>
        <div className="mt-3 overflow-x-auto">
          <table className="w-full min-w-[560px] text-sm">
            <thead className="text-left text-muted">
              <tr>
                <th className="py-1 pr-3">PI / SO</th>
                <th className="pr-3">Số SV</th>
                <th className="pr-3">Đạt</th>
                <th className="pr-3">% đạt</th>
                <th className="pr-3">Kết luận</th>
                <th>Năm {namSoSanh(nam)}</th>
              </tr>
            </thead>
            <tbody>
              {[...tongHop.pi, ...tongHop.so].map((d) => (
                <tr key={d.ma} className={`border-t border-line ${d.ma.startsWith("SO") ? "font-semibold" : ""}`}>
                  <td className="py-1.5 pr-3">{d.ma}</td>
                  <td className="pr-3">{d.so_sv || "—"}</td>
                  <td className="pr-3">{d.so_sv ? d.so_dat : "—"}</td>
                  <td className="pr-3">{phanTram(d.ti_le)}</td>
                  <td
                    className={`pr-3 ${d.ti_le === null ? "text-muted" : d.ti_le >= MUC_TIEU_PI ? "text-ok" : "text-danger"}`}
                  >
                    {ketLuan(d.ti_le)}
                  </td>
                  <td className="text-muted">{phanTram(d.ti_le_truoc)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* ───────── Kế hoạch / tiến độ ───────── */}
      {cacSo.map((so) => (
        <section key={so} className="space-y-2">
          <h2 className="text-lg font-semibold">
            {so}
            <span className="ml-2 text-sm font-normal text-muted">
              phụ trách: {dongNam.find((s) => s.so === so)?.phu_trach_so ?? "—"}
            </span>
          </h2>
          {dongNam
            .filter((s) => s.so === so)
            .map((s) => {
              const tk = thongKe(s);
              const tep = tepTheoDong.get(s.id) ?? [];
              const quaHan =
                s.han_nop && s.han_nop < homnay && (s.trang_thai === "chua_gui" || s.trang_thai === "da_gui");
              const dangMo = mo === s.id;
              return (
                <div key={s.id} className="rounded-xl border border-line bg-panel p-3">
                  <div className="flex flex-wrap items-start gap-x-4 gap-y-2">
                    <button
                      type="button"
                      onClick={() => setMo(dangMo ? null : s.id)}
                      className="flex min-w-0 flex-1 items-start gap-2 text-left"
                    >
                      {dangMo ? (
                        <ChevronDown className="mt-1 h-4 w-4 shrink-0" />
                      ) : (
                        <ChevronRight className="mt-1 h-4 w-4 shrink-0" />
                      )}
                      <span className="min-w-0">
                        <span className="font-semibold">{s.pi}</span> <span className="text-muted">{s.ma_dong}</span>
                        {s.tuy_chon ? (
                          <span className="ml-2 rounded bg-surface-2 px-1.5 text-xs text-muted">tuỳ chọn</span>
                        ) : null}
                        <span className="block">
                          {s.hoc_phan} · {s.khoa} · {s.hoc_ky}
                        </span>
                        <span className="block text-sm text-muted">{s.noi_dung}</span>
                      </span>
                    </button>
                    <div className="flex flex-wrap items-center gap-2 text-sm">
                      <input
                        defaultValue={s.chu_pi ?? ""}
                        placeholder="Chủ PI"
                        onBlur={(e) => {
                          const v = e.target.value.trim() || null;
                          if (v !== s.chu_pi) void sua(s, { chu_pi: v });
                        }}
                        className="h-10 w-40 rounded-lg border border-line-strong bg-panel px-2"
                        aria-label={`Chủ PI ${s.ma_dong}`}
                      />
                      <input
                        type="date"
                        value={s.han_nop ?? ""}
                        onChange={(e) => void sua(s, { han_nop: e.target.value || null })}
                        className={`h-10 rounded-lg border bg-panel px-2 ${quaHan ? "border-danger text-danger" : "border-line-strong"}`}
                        aria-label={`Hạn nộp ${s.ma_dong}`}
                      />
                      <select
                        value={s.trang_thai}
                        onChange={(e) => void sua(s, { trang_thai: e.target.value as TrangThai })}
                        className={`h-10 rounded-lg px-2 ${MAU_TRANG_THAI[s.trang_thai]}`}
                        aria-label={`Trạng thái ${s.ma_dong}`}
                      >
                        {TRANG_THAI.map((t) => (
                          <option key={t} value={t}>
                            {NHAN_TRANG_THAI[t]}
                          </option>
                        ))}
                      </select>
                      <span className="min-w-24 text-right tabular-nums">
                        {tk.n ? `${tk.n} SV · ${phanTram(tk.tiLe)}` : "—"}
                        <span className="block text-xs text-muted">{tep.length} tệp</span>
                      </span>
                      <button
                        type="button"
                        onClick={() => void chepTin(s)}
                        className="flex h-10 items-center gap-1 rounded-lg bg-primary px-3 font-medium text-white hover:bg-primary-dark"
                      >
                        {daChep === s.id ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />} Tin nhắn
                      </button>
                      <a
                        href={linkNop(s.token).replace(SITE_URL, "")}
                        target="_blank"
                        rel="noopener"
                        className="flex h-10 items-center rounded-lg border border-line px-2 text-muted"
                        aria-label={`Mở link nộp ${s.ma_dong}`}
                      >
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    </div>
                  </div>

                  {dangMo ? (
                    <div className="mt-3 grid gap-4 border-t border-line pt-3 text-sm md:grid-cols-2">
                      <div className="space-y-2">
                        <p>
                          <span className="text-muted">Học phần:</span> {s.ma_hp ?? "—"} · {s.cong_cu} · điểm tối đa câu
                          PI: {s.diem_toi_da ?? "chưa có"}
                        </p>
                        {s.nop_luc ? (
                          <p className="text-muted">Nộp lúc {new Date(s.nop_luc).toLocaleString("vi-VN")}</p>
                        ) : null}
                        {s.nhan_xet_gv ? (
                          <p>
                            <span className="text-muted">Nhận xét GV:</span> {s.nhan_xet_gv}
                          </p>
                        ) : null}
                        {s.ly_do_khong_thu ? (
                          <p className="text-danger">
                            <span className="text-muted">Không thu được:</span> {s.ly_do_khong_thu}
                          </p>
                        ) : null}
                        <label className="block">
                          <span className="text-muted">Ghi chú điều phối</span>
                          <textarea
                            defaultValue={s.ghi_chu ?? ""}
                            rows={2}
                            onBlur={(e) => {
                              const v = e.target.value.trim() || null;
                              if (v !== s.ghi_chu) void sua(s, { ghi_chu: v });
                            }}
                            className="mt-1 w-full rounded-lg border border-line-strong bg-panel p-2"
                          />
                        </label>
                        <p className="break-all text-xs text-muted">{linkNop(s.token)}</p>
                      </div>
                      <div className="space-y-3">
                        <div>
                          <p className="font-medium">Tệp minh chứng</p>
                          {tep.length ? (
                            <ul className="mt-1 space-y-1">
                              {tep.map((f) => (
                                <li key={f.id}>
                                  <button
                                    type="button"
                                    onClick={() => void moTep(f)}
                                    className="text-left text-primary underline"
                                  >
                                    {NHAN_LOAI_TEP[f.loai]}: {f.ten_file}
                                  </button>
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <p className="text-muted">Chưa có.</p>
                          )}
                        </div>
                        <div>
                          <div className="flex items-center justify-between">
                            <p className="font-medium">Bảng điểm ({tk.n} SV)</p>
                            {tk.n ? (
                              <button
                                type="button"
                                onClick={() => taiCsv(s, diemTheoDong.get(s.id) ?? [])}
                                className="flex items-center gap-1 text-primary"
                              >
                                <Download className="h-4 w-4" /> CSV
                              </button>
                            ) : null}
                          </div>
                          {tk.n ? (
                            <div className="mt-1 max-h-48 overflow-y-auto rounded-lg bg-surface-2 p-2 font-mono text-xs">
                              {[...(diemTheoDong.get(s.id) ?? [])]
                                .sort((a, b) => a.mssv.localeCompare(b.mssv))
                                .map((d) => (
                                  <div key={d.mssv} className={demDat([d.diem], s.diem_toi_da) ? "" : "text-danger"}>
                                    {d.mssv} · {d.diem}
                                  </div>
                                ))}
                            </div>
                          ) : null}
                        </div>
                      </div>
                    </div>
                  ) : null}
                </div>
              );
            })}
        </section>
      ))}
    </div>
  );
}
