// Phía học sinh của "Đố vui lớp học": không đăng nhập, gọi RPC ẩn danh bằng fetch thuần (không kéo supabase-js).
import type { PlayerState } from "@/features/quiz-live/types";
import { restRpc } from "./supabase-rest";

export interface JoinResult {
  room_id: number;
  player_id: number;
  token: string;
  title: string;
  nickname: string;
}

export async function joinQuiz(pin: string, nickname: string): Promise<JoinResult> {
  return (await restRpc("quiz_join", { p_pin: pin, p_nickname: nickname })) as JoinResult;
}

export async function getPlayerState(room: number, token: string): Promise<PlayerState> {
  return (await restRpc("quiz_state", { p_room: room, p_token: token })) as PlayerState;
}

export async function sendAnswer(room: number, token: string, choice: number): Promise<void> {
  await restRpc("quiz_answer", { p_room: room, p_token: token, p_choice: choice });
}
