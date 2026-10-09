import { getSupabase } from "@/services/supabase";

export type TaskRpKind = "exam" | "practice_item";

/** Câu hiện trước khi bắt đầu. null = chưa có mùa, hoặc không đọc được — ẩn dòng. */
export function taskRpMessage(input: {
  enabled: boolean;
  maxRp: number;
  awarded: number | null;
  firstOnly: boolean;
}): string | null {
  if (!input.enabled || input.maxRp <= 0) return "Bài này không tính RP.";
  if (input.awarded !== null && input.firstOnly) {
    return `Em đã nhận ${input.awarded} RP cho bài này ở lượt đầu. Làm lại để ôn, không cộng thêm RP.`;
  }
  if (!input.firstOnly) {
    return `Bài này tối đa ${input.maxRp} RP theo điểm. Làm lại điểm cao hơn thì được cộng thêm phần chênh.`;
  }
  return `Lượt đầu tiên: 10 điểm được ${input.maxRp} RP, điểm thấp hơn thì ít hơn. Làm lại không cộng thêm RP.`;
}

export async function fetchTaskRpMessage(kind: TaskRpKind, sourceId: number): Promise<string | null> {
  const supabase = getSupabase();
  const { data: status, error } = await supabase.rpc("rank_my_status");
  const seasonId = (status as { season?: { id?: number } } | null)?.season?.id;
  if (error || !seasonId) return null;
  const ref = `${kind}:${sourceId}`;
  const [{ data: src }, { data: award }, { data: season }] = await Promise.all([
    supabase
      .from("rank_sources")
      .select("max_rp, enabled")
      .eq("season_id", seasonId)
      .eq("source_kind", kind)
      .eq("source_id", sourceId)
      .maybeSingle(),
    supabase
      .from("rank_rp_awards")
      .select("awarded")
      .eq("season_id", seasonId)
      .eq("source_kind", "practice")
      .eq("source_ref", ref)
      .maybeSingle(),
    supabase.from("rank_seasons").select("config").eq("id", seasonId).maybeSingle(),
  ]);
  const cfg = (season?.config ?? {}) as { rp_first_attempt_only?: number };
  return taskRpMessage({
    enabled: !!src?.enabled,
    maxRp: Number(src?.max_rp ?? 0),
    awarded: award ? Number(award.awarded) : null,
    firstOnly: Number(cfg.rp_first_attempt_only ?? 1) >= 1,
  });
}
