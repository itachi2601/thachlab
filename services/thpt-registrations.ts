import { getSupabase } from "@/services/supabase";

export type ThptRegistrationStatus = "pending" | "approved" | "rejected";

export interface ThptRegistrationRequest {
  id: number;
  created_at: string;
  user_id: string;
  requested_class_id: number;
  full_name: string;
  username: string;
  email: string;
  phone: string;
  parent_phone: string;
  birth_date: string | null;
  gender: string;
  student_code: string;
  status: ThptRegistrationStatus;
}

export async function fetchThptRegistrations(classId: number) {
  const { data, error } = await getSupabase()
    .from("thpt_registration_requests")
    .select("id, created_at, user_id, requested_class_id, full_name, username, email, phone, parent_phone, birth_date, gender, student_code, status")
    .eq("requested_class_id", classId)
    .order("created_at", { ascending: false });
  if (error) throw error;
  return (data ?? []) as ThptRegistrationRequest[];
}

export async function reviewThptRegistration(
  requestId: number,
  status: Exclude<ThptRegistrationStatus, "pending">,
) {
  const { error } = await getSupabase().rpc("review_thpt_registration", {
    p_request_id: requestId,
    p_status: status,
  });
  if (error) throw error;
}
