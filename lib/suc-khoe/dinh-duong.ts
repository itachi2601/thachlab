// Mục Sức khỏe › Dinh dưỡng: tính năng lượng mục tiêu + nhật ký ăn theo ngày.
// Số liệu món ăn là ƯỚC LƯỢNG cho một phần thường gặp (tham khảo bảng USDA FoodData Central và
// Bảng thành phần thực phẩm Việt Nam) — đủ để theo dõi xu hướng, không phải số đo chính xác.
import { getSupabase } from "@/services/supabase";
import { TARGET } from "@/lib/tap-luyen/chuong-trinh";

export type Food = { id: string; name: string; unit: string; kcal: number; p: number; c: number; f: number; group: string };
export type FoodItem = Omit<Food, "group"> & { qty: number };
export type NutritionDay = { day: string; items: FoodItem[]; weight_kg: number | null; note?: string | null };
export type Sex = "nam" | "nu";
export type Goal = "tang" | "giu" | "giam";
export type NutritionProfile = { birth_year: number | null; sex: Sex | null; activity: number; goal: Goal; kcal_adjust: number };

export const FOODS: Food[] = [
  // Tinh bột
  { id: "com", name: "Cơm trắng", unit: "1 bát (150 g)", kcal: 195, p: 4, c: 43, f: 0.4, group: "Tinh bột" },
  { id: "bun", name: "Bún tươi", unit: "1 bát (150 g)", kcal: 165, p: 2.7, c: 37, f: 0.3, group: "Tinh bột" },
  { id: "banh_mi", name: "Bánh mì không", unit: "1 ổ (80 g)", kcal: 215, p: 7, c: 42, f: 2, group: "Tinh bột" },
  { id: "khoai_lang", name: "Khoai lang luộc", unit: "1 củ (150 g)", kcal: 115, p: 2.1, c: 27, f: 0.2, group: "Tinh bột" },
  { id: "yen_mach", name: "Yến mạch", unit: "40 g (khô)", kcal: 150, p: 5.3, c: 27, f: 2.6, group: "Tinh bột" },
  { id: "xoi", name: "Xôi trắng", unit: "1 gói (150 g)", kcal: 290, p: 5.5, c: 63, f: 0.6, group: "Tinh bột" },
  // Đạm
  { id: "uc_ga", name: "Ức gà (chín)", unit: "100 g", kcal: 165, p: 31, c: 0, f: 3.6, group: "Đạm" },
  { id: "trung", name: "Trứng gà", unit: "1 quả", kcal: 72, p: 6.3, c: 0.4, f: 4.8, group: "Đạm" },
  { id: "heo_nac", name: "Thịt heo nạc (chín)", unit: "100 g", kcal: 200, p: 28, c: 0, f: 9, group: "Đạm" },
  { id: "bo_nac", name: "Thịt bò nạc (chín)", unit: "100 g", kcal: 220, p: 28, c: 0, f: 11, group: "Đạm" },
  { id: "ca", name: "Cá phi lê (chín)", unit: "100 g", kcal: 130, p: 26, c: 0, f: 2.7, group: "Đạm" },
  { id: "tom", name: "Tôm (chín)", unit: "100 g", kcal: 100, p: 24, c: 0.2, f: 0.3, group: "Đạm" },
  { id: "dau_phu", name: "Đậu phụ", unit: "100 g", kcal: 76, p: 8, c: 1.9, f: 4.8, group: "Đạm" },
  { id: "whey", name: "Whey protein", unit: "1 muỗng (30 g)", kcal: 120, p: 24, c: 3, f: 1.5, group: "Đạm" },
  // Sữa
  { id: "sua_tuoi", name: "Sữa tươi không đường", unit: "1 hộp 180 ml", kcal: 115, p: 5.8, c: 8.6, f: 6.3, group: "Sữa" },
  { id: "sua_chua", name: "Sữa chua có đường", unit: "1 hộp 100 g", kcal: 100, p: 3.5, c: 15, f: 3, group: "Sữa" },
  { id: "sua_chua_hy", name: "Sữa chua Hy Lạp không đường", unit: "1 hộp 100 g", kcal: 60, p: 10, c: 3.6, f: 0.4, group: "Sữa" },
  // Món nấu sẵn
  { id: "pho_bo", name: "Phở bò", unit: "1 tô", kcal: 450, p: 25, c: 60, f: 12, group: "Món ăn" },
  { id: "bun_bo", name: "Bún bò", unit: "1 tô", kcal: 500, p: 28, c: 60, f: 15, group: "Món ăn" },
  { id: "com_tam", name: "Cơm tấm sườn", unit: "1 đĩa", kcal: 650, p: 30, c: 80, f: 22, group: "Món ăn" },
  { id: "banh_mi_thit", name: "Bánh mì thịt", unit: "1 ổ", kcal: 420, p: 18, c: 50, f: 15, group: "Món ăn" },
  { id: "mi_goi", name: "Mì gói", unit: "1 gói 75 g", kcal: 350, p: 7, c: 46, f: 15, group: "Món ăn" },
  // Rau, quả, khác
  { id: "rau", name: "Rau luộc/xào ít dầu", unit: "1 đĩa", kcal: 40, p: 2, c: 7, f: 0.3, group: "Rau quả" },
  { id: "chuoi", name: "Chuối", unit: "1 quả (120 g)", kcal: 105, p: 1.3, c: 27, f: 0.4, group: "Rau quả" },
  { id: "tao", name: "Táo", unit: "1 quả (180 g)", kcal: 95, p: 0.5, c: 25, f: 0.3, group: "Rau quả" },
  { id: "lac", name: "Lạc rang", unit: "30 g (1 nắm)", kcal: 170, p: 7.7, c: 4.8, f: 14.8, group: "Khác" },
  { id: "dau_an", name: "Dầu ăn", unit: "1 thìa canh", kcal: 120, p: 0, c: 0, f: 13.6, group: "Khác" },
  { id: "tra_sua", name: "Trà sữa trân châu", unit: "1 ly 500 ml", kcal: 400, p: 3, c: 70, f: 12, group: "Khác" },
];

export const ACTIVITY = [
  { v: 1.375, label: "Ít vận động", hint: "Ngồi nhiều, tập 1–2 buổi/tuần" },
  { v: 1.55, label: "Vừa", hint: "Gym 3 buổi + trượt băng" },
  { v: 1.725, label: "Nhiều", hint: "Tập nặng gần như mỗi ngày" },
];
export const GOAL_KCAL: Record<Goal, number> = { tang: 250, giu: 0, giam: -400 };
export const GOAL_LABEL: Record<Goal, string> = { tang: "Tăng cơ chậm", giu: "Giữ cân", giam: "Giảm mỡ" };
export const DEFAULT_PROFILE: NutritionProfile = { birth_year: null, sex: "nam", activity: 1.55, goal: "tang", kcal_adjust: 0 };

/** BMR theo Mifflin–St Jeor (1990): sai số ±10% cho đa số người. */
export const bmr = (kg: number, cm: number, age: number, sex: Sex) => 10 * kg + 6.25 * cm - 5 * age + (sex === "nam" ? 5 : -161);

export function targets(prof: NutritionProfile, kg: number, cm: number, year: number) {
  if (!prof.birth_year || !prof.sex) return null;
  const age = year - prof.birth_year;
  const base = bmr(kg, cm, age, prof.sex);
  const tdee = base * prof.activity;
  const kcal = Math.round((tdee + GOAL_KCAL[prof.goal] + prof.kcal_adjust) / 10) * 10;
  const p = Math.round(kg * (prof.goal === "giam" ? 2 : 1.8)); // 1,6–2,2 g/kg
  const f = Math.round((kcal * 0.27) / 9); // ~27% năng lượng từ chất béo
  const c = Math.max(0, Math.round((kcal - p * 4 - f * 9) / 4));
  return { age, bmr: Math.round(base), tdee: Math.round(tdee), kcal, p, c, f, pRange: TARGET.proteinGPerKg.map((g) => Math.round(g * kg)) };
}

export const sumItems = (items: FoodItem[]) =>
  items.reduce((a, i) => ({ kcal: a.kcal + i.kcal * i.qty, p: a.p + i.p * i.qty, c: a.c + i.c * i.qty, f: a.f + i.f * i.qty }), { kcal: 0, p: 0, c: 0, f: 0 });

/** Trung bình cân theo tuần (thứ Hai) từ các ngày có cân, mới nhất trước. */
export function weeklyWeights(days: NutritionDay[]) {
  const map = new Map<string, number[]>();
  for (const d of days) {
    if (d.weight_kg == null) continue;
    const x = new Date(`${d.day}T00:00:00`);
    x.setDate(x.getDate() - ((x.getDay() + 6) % 7));
    const k = `${x.getFullYear()}-${String(x.getMonth() + 1).padStart(2, "0")}-${String(x.getDate()).padStart(2, "0")}`;
    map.set(k, [...(map.get(k) ?? []), d.weight_kg]);
  }
  return [...map.entries()]
    .map(([week, ws]) => ({ week, avg: ws.reduce((a, b) => a + b, 0) / ws.length, n: ws.length }))
    .sort((a, b) => b.week.localeCompare(a.week));
}

/** Quy tắc chỉnh năng lượng (RULES_TEXT): cần ≥3 tuần, mỗi tuần ≥3 lần cân. */
export function adjustAdvice(weeks: ReturnType<typeof weeklyWeights>, goal: Goal) {
  const ok = weeks.filter((w) => w.n >= 3).slice(0, 3);
  if (ok.length < 3) return { kind: "chua-du" as const, delta: 0, text: "Cân buổi sáng ít nhất 3 lần/tuần, đủ 3 tuần mới đủ dữ liệu để chỉnh." };
  const g1 = ok[0].avg - ok[1].avg,
    g2 = ok[1].avg - ok[2].avg;
  if (goal === "tang") {
    if (g1 > 0.4 && g2 > 0.4) return { kind: "bot" as const, delta: -150, text: "Cân tăng hơn 0,4 kg/tuần hai tuần liền — dễ tích mỡ. Bớt 150 kcal/ngày." };
    if (g1 < 0.1 && g2 < 0.1) return { kind: "them" as const, delta: 150, text: "Cân gần như đứng yên hai tuần — thêm 150 kcal/ngày (ưu tiên tinh bột quanh buổi tập)." };
    return { kind: "giu" as const, delta: 0, text: `Đang tăng ${fmt1(g1)} kg/tuần — đúng nhịp ${fmt1(TARGET.weightGainPerWeek[0])}–${fmt1(TARGET.weightGainPerWeek[1])} kg. Giữ nguyên.` };
  }
  if (goal === "giam") {
    if (g1 > -0.2 && g2 > -0.2) return { kind: "bot" as const, delta: -150, text: "Cân giảm chậm hơn 0,2 kg/tuần hai tuần liền — bớt 150 kcal/ngày." };
    if (g1 < -1 && g2 < -1) return { kind: "them" as const, delta: 150, text: "Giảm nhanh hơn 1 kg/tuần — dễ mất cơ. Thêm 150 kcal/ngày." };
    return { kind: "giu" as const, delta: 0, text: "Đang giảm đúng nhịp. Giữ nguyên." };
  }
  if (Math.abs(g1) > 0.3 && Math.abs(g2) > 0.3 && Math.sign(g1) === Math.sign(g2))
    return { kind: g1 > 0 ? ("bot" as const) : ("them" as const), delta: g1 > 0 ? -150 : 150, text: `Cân ${g1 > 0 ? "tăng" : "giảm"} đều hai tuần — chỉnh ${g1 > 0 ? "bớt" : "thêm"} 150 kcal/ngày.` };
  return { kind: "giu" as const, delta: 0, text: "Cân ổn định. Giữ nguyên." };
}
const fmt1 = (n: number) => (Math.round(n * 100) / 100).toLocaleString("vi-VN");

// ---- lưu trữ: Supabase + bản sao localStorage (mất mạng vẫn ghi, lần sau gửi lại) ----
const K_DAYS = "dinhduong:days";
const K_PENDING = "dinhduong:pending";
const K_PROFILE = "dinhduong:profile";
function lsGet<T>(k: string, fb: T): T {
  try {
    const v = localStorage.getItem(k);
    return v ? (JSON.parse(v) as T) : fb;
  } catch {
    return fb;
  }
}
function lsSet(k: string, v: unknown) {
  try {
    localStorage.setItem(k, JSON.stringify(v));
  } catch {
    /* bộ nhớ đầy / ẩn danh */
  }
}

export async function fetchDays(sinceIso: string): Promise<{ list: NutritionDay[]; offline: boolean }> {
  const local = lsGet<Record<string, NutritionDay>>(K_DAYS, {});
  try {
    await flushPending();
    const { data, error } = await getSupabase().from("nutrition_days").select("day,items,weight_kg,note").gte("day", sinceIso).order("day", { ascending: false });
    if (error) throw error;
    const list = (data ?? []).map((r) => ({ ...r, weight_kg: r.weight_kg == null ? null : Number(r.weight_kg) })) as NutritionDay[];
    const pend = new Set(lsGet<string[]>(K_PENDING, []));
    const merged: Record<string, NutritionDay> = {};
    for (const d of list) merged[d.day] = d;
    for (const k of pend) if (local[k]) merged[k] = local[k]; // bản chưa gửi được mới hơn
    lsSet(K_DAYS, merged);
    return { list: Object.values(merged).sort((a, b) => b.day.localeCompare(a.day)), offline: false };
  } catch {
    return { list: Object.values(local).sort((a, b) => b.day.localeCompare(a.day)), offline: true };
  }
}

async function upsertDay(d: NutritionDay) {
  const { error } = await getSupabase()
    .from("nutrition_days")
    .upsert({ ...d, updated_at: new Date().toISOString() }, { onConflict: "user_id,day" });
  if (error) throw error;
}

/** Ghi một ngày; true nếu đã lên máy chủ. */
export async function saveDay(d: NutritionDay): Promise<boolean> {
  lsSet(K_DAYS, { ...lsGet<Record<string, NutritionDay>>(K_DAYS, {}), [d.day]: d });
  const pend = new Set(lsGet<string[]>(K_PENDING, []));
  try {
    await upsertDay(d);
    pend.delete(d.day);
    lsSet(K_PENDING, [...pend]);
    return true;
  } catch {
    pend.add(d.day);
    lsSet(K_PENDING, [...pend]);
    return false;
  }
}

async function flushPending() {
  const pend = lsGet<string[]>(K_PENDING, []);
  if (!pend.length) return;
  const local = lsGet<Record<string, NutritionDay>>(K_DAYS, {});
  const left: string[] = [];
  for (const k of pend) {
    try {
      if (local[k]) await upsertDay(local[k]);
    } catch {
      left.push(k);
    }
  }
  lsSet(K_PENDING, left);
}

export async function fetchProfile(): Promise<NutritionProfile> {
  try {
    const { data, error } = await getSupabase().from("nutrition_profile").select("birth_year,sex,activity,goal,kcal_adjust").maybeSingle();
    if (error) throw error;
    const p = data ? ({ ...DEFAULT_PROFILE, ...data, activity: Number(data.activity ?? DEFAULT_PROFILE.activity) } as NutritionProfile) : lsGet(K_PROFILE, DEFAULT_PROFILE);
    lsSet(K_PROFILE, p);
    return p;
  } catch {
    return lsGet(K_PROFILE, DEFAULT_PROFILE);
  }
}
export async function saveProfile(p: NutritionProfile) {
  lsSet(K_PROFILE, p);
  const { error } = await getSupabase()
    .from("nutrition_profile")
    .upsert({ ...p, updated_at: new Date().toISOString() }, { onConflict: "user_id" });
  if (error) throw error;
}
