// So sánh output ĐƯỜNG CŨ (select bảng thô rồi tính ở client) với ĐƯỜNG MỚI (rpc tổng hợp,
// supabase/migrations/20260925130000_perf_rpc_gv.sql) cho 1 lớp / 1 đề / 1 học sinh mẫu.
//
//   npx tsx scripts/perf-compare-rpc.mts            # tự chọn lớp đông nhất, đề nhiều lượt nhất
//   npx tsx scripts/perf-compare-rpc.mts --class 18 --exam 118 --student <uuid>
//
// CHỈ ĐỌC. Dùng SUPABASE_SERVICE_ROLE_KEY trong .env.local (bỏ qua RLS để so sánh dữ liệu
// thuần); nạp key vào NEXT_PUBLIC_SUPABASE_ANON_KEY TRƯỚC khi import services/* để
// getSupabase() dùng đúng client. Nếu rpc chưa tồn tại trên DB thì in hướng dẫn, không crash.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));

function readEnvLocal(key: string): string | undefined {
  const envPath = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs.readFileSync(envPath, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}

const url = readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const serviceKey = readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !serviceKey) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY trong .env.local");
  process.exit(1);
}
process.env.NEXT_PUBLIC_SUPABASE_URL = url;
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = serviceKey;

const { getSupabase } = await import("@/services/supabase");
const analytics = await import("@/services/analytics");
const studentProfile = await import("@/services/student-profile");
const progress = await import("@/services/progress");
const { isMissingRpcError } = await import("@/services/class-rpc");

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : undefined;
}

const supabase = getSupabase();

// ---------- chọn mẫu ----------
async function pickClass(): Promise<number> {
  const fromArg = arg("class");
  if (fromArg) return Number(fromArg);
  const { data, error } = await supabase.from("user_classes").select("class_id").eq("status", "active");
  if (error) throw error;
  const count = new Map<number, number>();
  for (const row of data ?? []) count.set(row.class_id, (count.get(row.class_id) ?? 0) + 1);
  const best = [...count.entries()].sort((a, b) => b[1] - a[1])[0];
  if (!best) throw new Error("Không có lớp nào có học sinh active.");
  return best[0];
}

async function studentsOf(classId: number): Promise<string[]> {
  const { data, error } = await supabase.from("user_classes").select("user_id").eq("class_id", classId).eq("status", "active");
  if (error) throw error;
  return [...new Set((data ?? []).map((row) => row.user_id as string))];
}

async function pickExamAndStudent(studentIds: string[]): Promise<{ examId: number | null; studentId: string | null }> {
  const { data, error } = await supabase.from("exam_results").select("exam_id, student_id").in("student_id", studentIds);
  if (error) throw error;
  const byExam = new Map<number, number>();
  const byStudent = new Map<string, number>();
  for (const row of data ?? []) {
    byExam.set(row.exam_id, (byExam.get(row.exam_id) ?? 0) + 1);
    byStudent.set(row.student_id, (byStudent.get(row.student_id) ?? 0) + 1);
  }
  const examArg = arg("exam");
  const studentArg = arg("student");
  return {
    examId: examArg ? Number(examArg) : ([...byExam.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? null),
    studentId: studentArg ?? ([...byStudent.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? null),
  };
}

// ---------- kiểm tra rpc có tồn tại chưa ----------
async function rpcExists(name: string, params: Record<string, unknown>): Promise<boolean> {
  const { error } = await supabase.rpc(name, params);
  if (!error) return true;
  if (isMissingRpcError(error)) {
    console.log(`  [${name}] RPC chưa có — chạy migration supabase/migrations/20260925130000_perf_rpc_gv.sql rồi chạy lại.`);
    return false;
  }
  console.log(`  [${name}] rpc lỗi: ${error.code ?? ""} ${error.message}`);
  return false;
}

// ---------- so sánh ----------
type Json = null | boolean | number | string | Json[] | { [k: string]: Json };
function stable(value: unknown): string {
  return JSON.stringify(value, (_k, v: Json) => {
    if (v && typeof v === "object" && !Array.isArray(v)) {
      return Object.fromEntries(Object.keys(v).sort().map((k) => [k, (v as Record<string, Json>)[k]]));
    }
    return v;
  });
}
function sortBy<T>(list: T[], key: (item: T) => string): T[] {
  return [...list].sort((a, b) => key(a).localeCompare(key(b)));
}
function report(label: string, oldValue: unknown, newValue: unknown) {
  compared += 1;
  const a = stable(oldValue);
  const b = stable(newValue);
  if (a === b) {
    console.log(`  ✓ ${label}: giống hệt (${Array.isArray(oldValue) ? `${oldValue.length} phần tử` : "1 đối tượng"})`);
    return true;
  }
  console.log(`  ✗ ${label}: KHÁC`);
  console.log(`      cũ : ${a.slice(0, 400)}${a.length > 400 ? "…" : ""}`);
  console.log(`      mới: ${b.slice(0, 400)}${b.length > 400 ? "…" : ""}`);
  return false;
}

// ---------- chạy ----------
const classId = await pickClass();
const studentIds = await studentsOf(classId);
const { examId, studentId } = await pickExamAndStudent(studentIds);
console.log(`Lớp ${classId}: ${studentIds.length} học sinh · đề mẫu ${examId ?? "(không có)"} · học sinh mẫu ${studentId ?? "(không có)"}`);

let allSame = true;
let compared = 0;

if (examId) {
  console.log("\n[1] fetchExamOverview — get_class_exam_best");
  if (await rpcExists("get_class_exam_best", { p_exam: examId, p_students: studentIds.slice(0, 1) })) {
    const [oldValue, newValue] = await Promise.all([
      analytics.fetchExamOverviewDirect(examId, studentIds),
      analytics.fetchExamOverviewRpc(examId, studentIds),
    ]);
    allSame = report("thẻ tổng quan", oldValue, newValue) && allSame;
  }

  console.log("\n[2] fetchWrongestQuestions — get_class_exam_question_stats");
  if (await rpcExists("get_class_exam_question_stats", { p_exam: examId, p_students: studentIds.slice(0, 1) })) {
    const [oldValue, newValue] = await Promise.all([
      analytics.fetchWrongestQuestionsDirect(examId, studentIds),
      analytics.fetchWrongestQuestionsRpc(examId, studentIds),
    ]);
    allSame = report("câu sai nhiều nhất", sortBy(oldValue, (q) => String(q.questionIndex).padStart(4, "0")), sortBy(newValue ?? [], (q) => String(q.questionIndex).padStart(4, "0"))) && allSame;
  }

  console.log("\n[3] fetchClassTopicMatrix — get_class_topic_matrix");
  if (await rpcExists("get_class_topic_matrix", { p_students: studentIds.slice(0, 1), p_exam: examId })) {
    const [oldExam, newExam, oldAll, newAll] = await Promise.all([
      analytics.fetchClassTopicMatrixDirect(studentIds, examId),
      analytics.fetchClassTopicMatrixRpc(studentIds, examId),
      analytics.fetchClassTopicMatrixDirect(studentIds),
      analytics.fetchClassTopicMatrixRpc(studentIds),
    ]);
    allSame = report("ma trận (1 đề)", sortBy(oldExam, (g) => g.key), sortBy(newExam ?? [], (g) => g.key)) && allSame;
    allSame = report("ma trận (mọi đề)", sortBy(oldAll, (g) => g.key), sortBy(newAll ?? [], (g) => g.key)) && allSame;
  }
}

if (studentId) {
  console.log("\n[4] fetchStudentLearningHistory — get_student_learning_history");
  if (await rpcExists("get_student_learning_history", { p_student: studentId })) {
    const [oldValue, newValue] = await Promise.all([
      progress.fetchStudentLearningHistory(studentId),
      studentProfile.fetchStudentLearningHistoryRpc(studentId),
    ]);
    const key = (e: { at: string; activity: string; title: string; detail: string }) => `${e.at}|${e.activity}|${e.title}|${e.detail}`;
    allSame = report("lịch sử học tập", sortBy(oldValue, key), sortBy(newValue ?? [], key)) && allSame;
  }
}

console.log("\n[5] ta_monthly_scores — chỉ kiểm tra tồn tại (hàm gốc ta_monthly_score tự chặn service role vì auth.uid() null)");
{
  const { error } = await supabase.rpc("ta_monthly_scores", { p_assistant_ids: [], p_month: "2026-09-01" });
  if (!error) console.log("  ✓ rpc tồn tại, mảng rỗng → 0 dòng");
  else if (isMissingRpcError(error)) console.log("  [ta_monthly_scores] RPC chưa có — chạy migration rồi chạy lại.");
  else console.log(`  rpc lỗi: ${error.code ?? ""} ${error.message}`);
}

console.log(compared === 0 ? "\nKẾT LUẬN: chưa so được cặp nào — chạy migration rồi chạy lại." : allSame ? `\nKẾT LUẬN: ${compared} cặp đã so đều giống hệt.` : "\nKẾT LUẬN: có sai khác — xem chi tiết ở trên (hoà điểm/thứ tự ngẫu nhiên có thể gây lệch nhỏ ở avgSeconds/topicId).");
