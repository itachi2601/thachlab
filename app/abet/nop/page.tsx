"use client";

/**
 * app/abet/nop/page.tsx — trang giáo viên (chủ PI) nộp dữ liệu ABET qua link /abet/nop/?ma=<token>.
 *
 * Không cần tài khoản: mọi đọc/ghi đi qua RPC abet_nop_* kiểm token (migration 20261127200000).
 * Người dùng là giáo viên 35–60 tuổi mở link từ Zalo trên điện thoại → theo tinh thần bộ quy tắc
 * phụ huynh (docs/QUY-TAC-THIET-KE-PHU-HUYNH.md): chữ ≥17px, nút ≥48px, mỗi bước một khung có số,
 * nói rõ "trang chỉ lấy MSSV và điểm" để giáo viên yên tâm dán cả bảng có họ tên.
 */

import { useCallback, useEffect, useMemo, useState, useSyncExternalStore } from "react";
import { CheckCircle2, FileUp, Loader2, Trash2 } from "lucide-react";
import { demDat, docBangDan, docSo, NHAN_LOAI_TEP, NHAN_TRANG_THAI, phanTram, type LoaiTep } from "@/lib/abet";
import { nopDiem, nopKhongThu, nopTep, nopXem, nopXoaTep, type NopXem } from "@/services/abet";

function subscribe(onChange: () => void) {
  window.addEventListener("pageshow", onChange);
  window.addEventListener("popstate", onChange);
  return () => {
    window.removeEventListener("pageshow", onChange);
    window.removeEventListener("popstate", onChange);
  };
}
// Đọc thẳng window.location (không useSearchParams): link mở từ Zalo trên iOS đôi khi trả query rỗng.
const tokenTuDiaChi = () => (new URLSearchParams(window.location.search).get("ma") ?? "").trim();

const LOAI_TEP: LoaiTep[] = ["de_dap_an", "bai_mau_cao", "bai_mau_tb", "bai_mau_thap"];

function ngay(iso: string | null) {
  if (!iso) return "";
  const d = iso.length <= 10 ? new Date(`${iso}T00:00:00`) : new Date(iso);
  return d.toLocaleDateString("vi-VN");
}
function gio(iso: string) {
  return new Date(iso).toLocaleString("vi-VN", {
    hour: "2-digit",
    minute: "2-digit",
    day: "2-digit",
    month: "2-digit",
  });
}

function Khung({ so, tieuDe, children }: { so?: number; tieuDe: string; children: React.ReactNode }) {
  return (
    <section className="rounded-2xl border border-line bg-panel p-5 sm:p-6">
      <h2 className="flex items-center gap-3 text-lg font-semibold text-ink">
        {so ? (
          <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-base text-white">
            {so}
          </span>
        ) : null}
        {tieuDe}
      </h2>
      <div className="mt-4 space-y-3">{children}</div>
    </section>
  );
}

export default function AbetNopPage() {
  const token = useSyncExternalStore(subscribe, tokenTuDiaChi, () => "");
  const [info, setInfo] = useState<NopXem | null>(null);
  const [trangThaiTai, setTrangThaiTai] = useState<"dang" | "xong" | "khong_thay">("dang");
  const [loiTai, setLoiTai] = useState("");

  const [diemToiDaText, setDiemToiDaText] = useState("");
  const [bang, setBang] = useState("");
  const [nhanXet, setNhanXet] = useState("");
  const [dangNop, setDangNop] = useState(false);
  const [thongBao, setThongBao] = useState<{ loai: "ok" | "loi"; text: string } | null>(null);
  const [dangTaiTep, setDangTaiTep] = useState<LoaiTep | null>(null);
  const [loiTep, setLoiTep] = useState("");
  const [moKhongThu, setMoKhongThu] = useState(false);
  const [lyDo, setLyDo] = useState("");

  const tai = useCallback(
    (giuForm = false) => {
      if (!token) return;
      nopXem(token)
        .then((d) => {
          setInfo(d);
          setTrangThaiTai(d ? "xong" : "khong_thay");
          if (d && !giuForm && d.diem_toi_da) setDiemToiDaText(String(d.diem_toi_da));
          if (d && !giuForm && d.nhan_xet_gv) setNhanXet(d.nhan_xet_gv);
        })
        .catch((e: unknown) => {
          setLoiTai(e instanceof Error ? e.message : "Không tải được.");
          setTrangThaiTai("xong");
        });
    },
    [token],
  );
  useEffect(() => {
    tai();
  }, [tai]);

  const diemToiDa = docSo(diemToiDaText);
  const doc = useMemo(() => docBangDan(bang, diemToiDa), [bang, diemToiDa]);
  const soDat = demDat(
    doc.rows.map((r) => r.diem),
    diemToiDa,
  );
  const khoa = info?.trang_thai === "da_duyet";

  async function nop() {
    if (!diemToiDa) return setThongBao({ loai: "loi", text: "Thầy/cô ghi điểm tối đa của câu PI ở bước 1 trước nhé." });
    if (!doc.rows.length) return setThongBao({ loai: "loi", text: "Chưa đọc được dòng điểm nào ở bước 2." });
    if (doc.loi.length)
      return setThongBao({ loai: "loi", text: "Còn dòng chưa đọc được (danh sách màu đỏ). Sửa lại rồi nộp." });
    setDangNop(true);
    setThongBao(null);
    try {
      const n = await nopDiem(token, diemToiDa, doc.rows, nhanXet);
      setThongBao({ loai: "ok", text: `Đã nhận ${n} sinh viên. Em cảm ơn thầy/cô!` });
      setBang("");
      tai(true);
    } catch (e) {
      setThongBao({ loai: "loi", text: e instanceof Error ? e.message : "Nộp không được, thử lại sau." });
    } finally {
      setDangNop(false);
    }
  }

  async function chonTep(loai: LoaiTep, files: FileList | null) {
    if (!files?.length) return;
    setDangTaiTep(loai);
    setLoiTep("");
    try {
      for (const f of Array.from(files)) await nopTep(token, loai, f);
      tai(true);
    } catch (e) {
      setLoiTep(e instanceof Error ? e.message : "Tải tệp không được.");
    } finally {
      setDangTaiTep(null);
    }
  }

  async function boTep(id: number) {
    try {
      await nopXoaTep(token, id);
      tai(true);
    } catch (e) {
      setLoiTep(e instanceof Error ? e.message : "Không bỏ được tệp.");
    }
  }

  async function baoKhongThu() {
    try {
      await nopKhongThu(token, lyDo);
      setMoKhongThu(false);
      tai(true);
    } catch (e) {
      setThongBao({ loai: "loi", text: e instanceof Error ? e.message : "Không ghi được." });
    }
  }

  return (
    <main className="min-h-screen bg-bg px-4 py-6 text-[17px] leading-relaxed text-ink sm:py-10">
      <div className="mx-auto max-w-2xl space-y-5">
        <header>
          <p className="text-sm font-medium uppercase tracking-wide text-muted">Khoa Cơ khí · Kiểm định ABET</p>
          <h1 className="mt-1 text-2xl font-bold text-ink">Nộp dữ liệu chuẩn đầu ra</h1>
        </header>

        {!token ? (
          <p className="rounded-2xl border border-line bg-panel p-5">
            Link thiếu mã. Thầy/cô mở lại đúng link được gửi qua Zalo giúp em.
          </p>
        ) : trangThaiTai === "dang" ? (
          <p className="flex items-center gap-2 text-muted">
            <Loader2 className="h-5 w-5 animate-spin" /> Đang mở…
          </p>
        ) : loiTai ? (
          <p className="rounded-2xl border border-line bg-panel p-5 text-danger">{loiTai}</p>
        ) : !info ? (
          <p className="rounded-2xl border border-line bg-panel p-5">
            Link không đúng hoặc đã hết hiệu lực. Thầy/cô nhắn lại cho người gửi link giúp em.
          </p>
        ) : (
          <>
            <section className="rounded-2xl border border-line bg-panel p-5 sm:p-6">
              <p className="text-sm text-muted">
                {info.nam_hoc} · {info.so} · {info.pi}
              </p>
              <p className="mt-1 text-xl font-semibold text-ink">
                {info.hoc_phan}
                {info.khoa ? ` — ${info.khoa}` : ""}
                {info.hoc_ky ? ` (${info.hoc_ky})` : ""}
              </p>
              <p className="mt-3">
                <span className="text-muted">Dữ liệu cần lấy: </span>
                <strong>{info.noi_dung}</strong>
              </p>
              {info.han_nop ? (
                <p className="mt-1">
                  <span className="text-muted">Hạn nộp: </span>
                  <strong>{ngay(info.han_nop)}</strong>
                </p>
              ) : null}
              <p className="mt-3 inline-block rounded-full bg-surface-2 px-3 py-1 text-sm">
                Trạng thái: {NHAN_TRANG_THAI[info.trang_thai]}
                {info.trang_thai === "da_nop" && info.nop_luc
                  ? ` lúc ${gio(info.nop_luc)} · ${info.so_sv} sinh viên · ${phanTram(info.so_sv ? info.so_dat / info.so_sv : null)} đạt`
                  : ""}
              </p>
              {info.trang_thai === "khong_thu_duoc" ? (
                <p className="mt-2 text-muted">
                  Đã ghi: {info.ly_do_khong_thu}. Nếu tìm lại được điểm, thầy/cô vẫn nộp bình thường ở dưới.
                </p>
              ) : null}
              {khoa ? (
                <p className="mt-2 text-muted">
                  Dòng này đã được khoa duyệt và khoá. Cần sửa gì thầy/cô nhắn người gửi link.
                </p>
              ) : null}
            </section>

            {!khoa ? (
              <>
                <Khung so={1} tieuDe="Điểm tối đa của câu/phần này">
                  <p className="text-muted">Ví dụ câu 1 được 2 điểm trên thang 10 thì ghi 2.</p>
                  <input
                    inputMode="decimal"
                    value={diemToiDaText}
                    onChange={(e) => setDiemToiDaText(e.target.value)}
                    placeholder="Ví dụ: 2"
                    className="h-12 w-40 rounded-xl border border-line-strong bg-panel px-4 text-lg text-ink"
                    aria-label="Điểm tối đa của câu PI"
                  />
                </Khung>

                <Khung so={2} tieuDe="Dán bảng MSSV và điểm câu này">
                  <p className="text-muted">
                    Chọn hai cột MSSV và điểm trong Excel, chép rồi dán vào ô dưới. Có thêm cột họ tên, số thứ tự cũng
                    được: trang <strong className="text-ink">chỉ lấy MSSV và điểm</strong>, không gửi họ tên.
                  </p>
                  <textarea
                    value={bang}
                    onChange={(e) => setBang(e.target.value)}
                    rows={7}
                    placeholder={"0306241001\t1,5\n0306241002\t2\n…"}
                    className="w-full rounded-xl border border-line-strong bg-panel p-3 font-mono text-base text-ink"
                    aria-label="Bảng MSSV và điểm"
                  />
                  {bang.trim() ? (
                    <div className="rounded-xl bg-surface-2 p-3 text-base">
                      <p>
                        Đọc được <strong>{doc.rows.length}</strong> sinh viên
                        {diemToiDa ? (
                          <>
                            {" "}
                            · <strong>{soDat}</strong> em đạt từ 60% điểm câu (
                            {phanTram(doc.rows.length ? soDat / doc.rows.length : null)})
                          </>
                        ) : null}
                        .
                      </p>
                      {doc.lap.length ? <p className="mt-1 text-warn">Bỏ MSSV lặp: {doc.lap.join(", ")}</p> : null}
                      {doc.boQua.length ? (
                        <p className="mt-1 text-muted">
                          Bỏ qua {doc.boQua.length} dòng không có MSSV (thường là dòng tiêu đề):{" "}
                          {doc.boQua.slice(0, 3).join(" · ")}
                          {doc.boQua.length > 3 ? " …" : ""}
                        </p>
                      ) : null}
                      {doc.loi.length ? (
                        <ul className="mt-1 list-disc pl-5 text-danger">
                          {doc.loi.slice(0, 8).map((l) => (
                            <li key={l}>{l}</li>
                          ))}
                          {doc.loi.length > 8 ? <li>… và {doc.loi.length - 8} dòng nữa</li> : null}
                        </ul>
                      ) : null}
                    </div>
                  ) : null}
                  <label className="block">
                    <span className="text-muted">Nhận xét ngắn về kết quả câu này (không bắt buộc)</span>
                    <textarea
                      value={nhanXet}
                      onChange={(e) => setNhanXet(e.target.value)}
                      rows={2}
                      className="mt-1 w-full rounded-xl border border-line-strong bg-panel p-3 text-base text-ink"
                    />
                  </label>
                  <button
                    type="button"
                    onClick={nop}
                    disabled={dangNop}
                    className="flex min-h-12 items-center gap-2 rounded-xl bg-primary px-6 text-lg font-semibold text-white hover:bg-primary-dark disabled:opacity-60"
                  >
                    {dangNop ? <Loader2 className="h-5 w-5 animate-spin" /> : null}
                    {info.trang_thai === "da_nop" ? "Nộp lại (thay bảng cũ)" : "Nộp bảng điểm"}
                  </button>
                  {thongBao ? (
                    <p className={thongBao.loai === "ok" ? "flex items-center gap-2 text-ok" : "text-danger"}>
                      {thongBao.loai === "ok" ? <CheckCircle2 className="h-5 w-5" /> : null}
                      {thongBao.text}
                    </p>
                  ) : null}
                </Khung>

                <Khung so={3} tieuDe="Đề + đáp án và 3 bài mẫu">
                  <p className="text-muted">Chụp bằng điện thoại là được (ảnh tự thu nhỏ). Nhận cả PDF, Word, Excel.</p>
                  {LOAI_TEP.map((loai) => {
                    const daCo = info.tep.filter((t) => t.loai === loai);
                    return (
                      <div key={loai} className="rounded-xl border border-line p-3">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <span className="font-medium">
                            {daCo.length ? <CheckCircle2 className="mr-1 inline h-5 w-5 text-ok" /> : null}
                            {NHAN_LOAI_TEP[loai]}
                          </span>
                          <label className="flex min-h-12 cursor-pointer items-center gap-2 rounded-xl border border-line-strong px-4 text-base font-medium text-primary hover:bg-surface-2">
                            {dangTaiTep === loai ? (
                              <Loader2 className="h-5 w-5 animate-spin" />
                            ) : (
                              <FileUp className="h-5 w-5" />
                            )}
                            {daCo.length ? "Thêm tệp" : "Chọn tệp"}
                            <input
                              type="file"
                              multiple
                              accept="image/*,.heic,.pdf,.doc,.docx,.xls,.xlsx"
                              className="sr-only"
                              disabled={dangTaiTep !== null}
                              onChange={(e) => {
                                void chonTep(loai, e.target.files);
                                e.target.value = "";
                              }}
                            />
                          </label>
                        </div>
                        {daCo.length ? (
                          <ul className="mt-2 space-y-1 text-base">
                            {daCo.map((t) => (
                              <li key={t.id} className="flex items-center justify-between gap-2">
                                <span className="truncate text-muted">{t.ten_file}</span>
                                <button
                                  type="button"
                                  onClick={() => boTep(t.id)}
                                  className="flex min-h-11 items-center gap-1 px-2 text-sm text-danger"
                                  aria-label={`Bỏ tệp ${t.ten_file}`}
                                >
                                  <Trash2 className="h-4 w-4" /> Bỏ
                                </button>
                              </li>
                            ))}
                          </ul>
                        ) : null}
                      </div>
                    );
                  })}
                  {loiTep ? <p className="text-danger">{loiTep}</p> : null}
                </Khung>

                {info.trang_thai === "da_nop" ? null : (
                  <section className="rounded-2xl border border-dashed border-line p-5">
                    {!moKhongThu ? (
                      <button
                        type="button"
                        onClick={() => setMoKhongThu(true)}
                        className="min-h-12 text-base font-medium text-muted underline"
                      >
                        Không còn bài thi hoặc điểm từng câu?
                      </button>
                    ) : (
                      <div className="space-y-3">
                        <p>Không sao cả, khoa sẽ lấy bù ở năm sau. Thầy/cô ghi ngắn lý do giúp em:</p>
                        <textarea
                          value={lyDo}
                          onChange={(e) => setLyDo(e.target.value)}
                          rows={2}
                          placeholder="Ví dụ: bài thi đã trả phòng đào tạo, chỉ còn điểm tổng"
                          className="w-full rounded-xl border border-line-strong bg-panel p-3 text-base text-ink"
                        />
                        <div className="flex flex-wrap gap-3">
                          <button
                            type="button"
                            onClick={baoKhongThu}
                            className="min-h-12 rounded-xl border border-line-strong px-5 text-base font-semibold text-ink hover:bg-surface-2"
                          >
                            Báo không còn dữ liệu
                          </button>
                          <button
                            type="button"
                            onClick={() => setMoKhongThu(false)}
                            className="min-h-12 px-3 text-base text-muted"
                          >
                            Thôi
                          </button>
                        </div>
                      </div>
                    )}
                  </section>
                )}
              </>
            ) : null}
          </>
        )}
      </div>
    </main>
  );
}
