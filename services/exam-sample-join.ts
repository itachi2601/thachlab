import { fetchMyClassRequest, requestClassJoin } from "@/services/classes";

/**
 * Học sinh vừa đăng ký từ đề mẫu thường chưa có dòng user_classes.
 * Nếu đề này nằm trong 3 đề mẫu và em chưa vào lớp nào, vào đúng lớp của đề rồi làm.
 * Chỉ gọi khi đọc đề thất bại — lượt làm đã vào lớp không thêm request.
 */
export async function joinSampleClassIfUnset(examId: number, userId: string): Promise<boolean> {
  const mine = await fetchMyClassRequest(userId);
  if (mine) return false;
  const res = await fetch("/data/exam-samples.json");
  if (!res.ok) return false;
  const data = (await res.json()) as { samples?: { id: number; classId?: number }[] };
  const sample = data.samples?.find((item) => item.id === examId);
  if (!sample?.classId) return false;
  await requestClassJoin(sample.classId);
  return true;
}
