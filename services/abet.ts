import { getSupabase } from "@/services/supabase";
import { compressImageFile } from "@/services/image-compress";
import type { DongDiem, LoaiTep, TrangThai } from "@/lib/abet";

/**
 * services/abet.ts — truy cập dữ liệu ABET (migration 20261127200000_abet_thu_du_lieu_pi.sql).
 * - Hàm `nop*`: dùng ở trang nộp của giáo viên, chỉ qua RPC abet_nop_* bằng token (anon được).
 * - Hàm còn lại: trang điều phối, đọc/sửa bảng trực tiếp (RLS chỉ cho admin).
 */

const BUCKET = "abet-minh-chung";

export type AbetSource = {
  id: number;
  ma_dong: string;
  nam_hoc: string;
  so: string;
  pi: string;
  hk_ctdt: number | null;
  hoc_ky: string | null;
  khoa: string | null;
  ma_hp: string | null;
  hoc_phan: string;
  cong_cu: string | null;
  noi_dung: string | null;
  diem_toi_da: number | null;
  chu_pi: string | null;
  phu_trach_so: string | null;
  han_nop: string | null;
  tuy_chon: boolean;
  trang_thai: TrangThai;
  ghi_chu: string | null;
  nhan_xet_gv: string | null;
  ly_do_khong_thu: string | null;
  token: string;
  nop_luc: string | null;
  cap_nhat_luc: string;
};

export type AbetScore = { source_id: number; mssv: string; diem: number };
export type AbetFile = {
  id: number;
  source_id: number;
  loai: LoaiTep;
  storage_path: string;
  ten_file: string;
  mime_type: string | null;
  kich_thuoc: number | null;
  tao_luc: string;
};
export type AbetHistory = { nam_hoc: string; ma: string; ti_le: number; nguon: string | null };

export type NopXem = {
  ma_dong: string;
  nam_hoc: string;
  so: string;
  pi: string;
  hoc_ky: string | null;
  khoa: string | null;
  ma_hp: string | null;
  hoc_phan: string;
  cong_cu: string | null;
  noi_dung: string | null;
  diem_toi_da: number | null;
  chu_pi: string | null;
  han_nop: string | null;
  trang_thai: TrangThai;
  nop_luc: string | null;
  nhan_xet_gv: string | null;
  ly_do_khong_thu: string | null;
  so_sv: number;
  so_dat: number;
  tep: { id: number; loai: LoaiTep; ten_file: string }[];
};

function loi(error: { message: string } | null) {
  if (error) throw new Error(error.message);
}

// ─────────────── Trang nộp (giáo viên, theo token) ───────────────

export async function nopXem(token: string): Promise<NopXem | null> {
  const { data, error } = await getSupabase().rpc("abet_nop_xem", { p_token: token });
  loi(error);
  return (data as NopXem | null) ?? null;
}

export async function nopDiem(token: string, diemToiDa: number, rows: DongDiem[], nhanXet: string) {
  const { data, error } = await getSupabase().rpc("abet_nop_diem", {
    p_token: token,
    p_diem_toi_da: diemToiDa,
    p_rows: rows,
    p_nhan_xet: nhanXet,
  });
  loi(error);
  return data as number;
}

function duoiTep(name: string) {
  const m = /\.([A-Za-z0-9]{1,5})$/.exec(name);
  return m ? m[1].toLowerCase() : "bin";
}

export async function nopTep(token: string, loai: LoaiTep, file: File) {
  const supabase = getSupabase();
  // Ảnh điện thoại (kể cả HEIC) nén về JPEG ≤1600px; PDF/Word/Excel giữ nguyên.
  const tep = await compressImageFile(file, { maxDimension: 1600, quality: 0.8 });
  const path = `${token}/${loai}/${crypto.randomUUID()}.${duoiTep(tep.name)}`;
  const { error: upErr } = await supabase.storage
    .from(BUCKET)
    .upload(path, tep, { contentType: tep.type || "application/octet-stream", upsert: false });
  loi(upErr);
  const { error } = await supabase.rpc("abet_nop_tep", {
    p_token: token,
    p_loai: loai,
    p_path: path,
    p_ten: file.name,
    p_mime: tep.type || null,
    p_size: tep.size,
  });
  loi(error);
}

export async function nopXoaTep(token: string, fileId: number) {
  const { error } = await getSupabase().rpc("abet_nop_xoa_tep", { p_token: token, p_file_id: fileId });
  loi(error);
}

export async function nopKhongThu(token: string, lyDo: string) {
  const { error } = await getSupabase().rpc("abet_nop_khong_thu", { p_token: token, p_ly_do: lyDo });
  loi(error);
}

// ─────────────── Trang điều phối (admin) ───────────────

/** PostgREST trả tối đa 1000 dòng/lần → đọc theo trang để % đạt không bị thiếu sinh viên. */
async function taiHetDiem(): Promise<{ data: AbetScore[]; error: { message: string } | null }> {
  const all: AbetScore[] = [];
  for (let from = 0; ; from += 1000) {
    const { data, error } = await getSupabase()
      .from("abet_scores")
      .select("source_id, mssv, diem")
      .order("source_id")
      .order("mssv")
      .range(from, from + 999);
    if (error) return { data: all, error };
    all.push(...((data ?? []) as AbetScore[]));
    if (!data || data.length < 1000) return { data: all, error: null };
  }
}

export async function taiDuLieuAbet() {
  const supabase = getSupabase();
  const [src, sc, fi, hi] = await Promise.all([
    supabase.from("abet_sources").select("*").order("nam_hoc").order("so").order("ma_dong"),
    taiHetDiem(),
    supabase.from("abet_files").select("*").order("id"),
    supabase.from("abet_history").select("*"),
  ]);
  loi(src.error);
  loi(sc.error);
  loi(fi.error);
  loi(hi.error);
  return {
    sources: (src.data ?? []) as AbetSource[],
    scores: ((sc.data ?? []) as AbetScore[]).map((s) => ({ ...s, diem: Number(s.diem) })),
    files: (fi.data ?? []) as AbetFile[],
    history: ((hi.data ?? []) as AbetHistory[]).map((h) => ({ ...h, ti_le: Number(h.ti_le) })),
  };
}

export type SuaSource = Partial<
  Pick<AbetSource, "chu_pi" | "han_nop" | "trang_thai" | "ghi_chu" | "diem_toi_da" | "noi_dung" | "tuy_chon">
>;

export async function suaSource(id: number, patch: SuaSource) {
  const { error } = await getSupabase()
    .from("abet_sources")
    .update({ ...patch, cap_nhat_luc: new Date().toISOString() })
    .eq("id", id);
  loi(error);
}

export async function linkTepAbet(path: string) {
  const { data, error } = await getSupabase().storage.from(BUCKET).createSignedUrl(path, 3600);
  loi(error);
  return data?.signedUrl ?? "";
}
