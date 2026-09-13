"use client";

import { useCallback, useSyncExternalStore } from "react";
import type {
  TaAssistant,
  TaAssistantClass,
  TaMonthlyScore,
  TaSessionListItem,
  TaTopicSuggestion,
  TaVideoLedgerRow,
  TaVideoRates,
} from "./queries";

/**
 * Chế độ giả lập trợ giảng — dành cho giáo viên (role "admin") xem trước đúng giao diện mà
 * một trợ giảng nhìn thấy, kể cả khi tài khoản admin chưa hề có hồ sơ trong ta_assistants.
 *
 * Cách hoạt động: bật cờ trong sessionStorage (hoặc mở /tro-giang?gialap=1), các trang
 * /tro-giang/* sẽ dựng sẵn một hồ sơ giả với id = DEMO_ASSISTANT_ID. Mọi component nhận
 * assistant đó đều tự nhận ra qua isDemoAssistant() và dùng số liệu mẫu dưới đây thay vì
 * gọi Supabase — nên không đọc, không ghi, không đụng gì tới dữ liệu thật của đội.
 *
 * Số liệu mẫu được đặt khớp công thức trong docs/supabase-migration-tro-giang.sql (bậc B2,
 * 50.000 đ/giờ; thưởng 2.000 đ/giờ khi điểm ≥ 70) để màn hình xem trước đọc ra đúng như thật.
 */

export const DEMO_ASSISTANT_ID = "demo-tro-giang";
const DEMO_STORAGE_KEY = "thachlab_preview_as_ta";
const DEMO_EVENT = "thachlab-ta-demo-change";
/** Mở /tro-giang?gialap=1 cũng bật chế độ này (nút bên /quan-tri/tro-giang dùng link đó). */
export const DEMO_QUERY_FLAG = "gialap";

export function isDemoAssistant(assistant: { id: string } | null | undefined): boolean {
  return assistant?.id === DEMO_ASSISTANT_ID;
}

function readDemoMode() {
  try {
    return sessionStorage.getItem(DEMO_STORAGE_KEY) === "1";
  } catch {
    return false;
  }
}

function subscribeDemoMode(onChange: () => void) {
  window.addEventListener("storage", onChange);
  window.addEventListener(DEMO_EVENT, onChange);
  return () => {
    window.removeEventListener("storage", onChange);
    window.removeEventListener(DEMO_EVENT, onChange);
  };
}

export function setTaDemoMode(value: boolean) {
  try {
    if (value) sessionStorage.setItem(DEMO_STORAGE_KEY, "1");
    else sessionStorage.removeItem(DEMO_STORAGE_KEY);
  } catch {
    // sessionStorage bị chặn — bỏ qua, chỉ mất chế độ xem trước.
  }
  window.dispatchEvent(new Event(DEMO_EVENT));
}

/** Cờ giả lập + hàm bật/tắt. Server render luôn ra false nên không lệch hydrate. */
export function useTaDemoMode(): [boolean, (value: boolean) => void] {
  const demo = useSyncExternalStore(subscribeDemoMode, readDemoMode, () => false);
  const set = useCallback((value: boolean) => setTaDemoMode(value), []);
  return [demo, set];
}

// ---------- Số liệu mẫu ----------

function dayOffset(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() - days);
  return d.toLocaleDateString("sv-SE"); // yyyy-mm-dd theo giờ máy
}

/** Ngày trong THÁNG NÀY, lùi tối đa `days` ngày nhưng không rơi sang tháng trước. */
function thisMonthDay(days: number): string {
  const today = new Date();
  const back = new Date();
  back.setDate(today.getDate() - days);
  if (back.getMonth() !== today.getMonth()) {
    return new Date(today.getFullYear(), today.getMonth(), 1).toLocaleDateString("sv-SE");
  }
  return back.toLocaleDateString("sv-SE");
}

export function demoAssistant(): TaAssistant {
  return {
    id: DEMO_ASSISTANT_ID,
    user_id: DEMO_ASSISTANT_ID,
    full_name: "Trần Minh Khôi (giả lập)",
    short_name: "Khôi",
    tier: "B2",
    retained_rate: null,
    active: true,
    started_at: dayOffset(180),
  };
}

/**
 * Bậc B2 = 50.000 đ/giờ. 8 buổi lên lớp (2 giờ), 3 buổi phụ đạo (1,5 giờ ×1,25),
 * 1 buổi hành chính (1 giờ) → 22,63 giờ quy đổi; 42 bài chấm ×1.500 đ.
 * Điểm 83,33 → nằm giữa hai mốc thưởng, để câu gợi ý "còn thiếu gì" cũng hiện ra.
 */
export function demoMonthlyScore(month: string): TaMonthlyScore {
  return {
    assistant_id: DEMO_ASSISTANT_ID,
    month,
    lop_sessions: 8,
    phudao_sessions: 3,
    avg_touches: 10.5,
    touches_score: 35,
    ontime_error_notes: 6,
    error_note_rate: 0.75,
    error_note_score: 15,
    complete_phudao: 2,
    phudao_complete_rate: 0.6667,
    phudao_score: 13.33,
    flag_count: 0,
    focus_score: 20,
    total_score: 83.33,
    bonus_per_hour: 2000,
    converted_hours: 22.63,
    papers_graded: 42,
    base_pay: 1131500,
    bonus_pay: 45260,
    grading_pay: 63000,
    total_pay: 1239760,
  };
}

export function demoAccruedHours(): number {
  return 168.5;
}

export function demoSessions(): TaSessionListItem[] {
  return [
    {
      id: "demo-s1",
      work_date: thisMonthDay(1),
      session_type: "lop",
      class_label: "12A1",
      phudao_students: [],
      hours: 2,
      student_touches: 13,
      papers_graded: null,
      status: "submitted",
      reject_reason: null,
    },
    {
      id: "demo-s2",
      work_date: thisMonthDay(3),
      session_type: "phudao",
      class_label: null,
      phudao_students: ["Minh", "Khoa", "Ngân"],
      hours: 1.5,
      student_touches: null,
      papers_graded: null,
      status: "approved",
      reject_reason: null,
    },
    {
      id: "demo-s3",
      work_date: thisMonthDay(4),
      session_type: "chambai",
      class_label: "12A1",
      phudao_students: [],
      hours: null,
      student_touches: null,
      papers_graded: 24,
      status: "approved",
      reject_reason: null,
    },
    {
      id: "demo-s4",
      work_date: thisMonthDay(6),
      session_type: "lop",
      class_label: "11B2",
      phudao_students: [],
      hours: 2,
      student_touches: 8,
      papers_graded: null,
      status: "rejected",
      reject_reason: "Chưa ghi lỗi sai lặp lại của lớp, em bổ sung rồi ghi lại buổi này nhé.",
    },
    {
      id: "demo-s5",
      work_date: thisMonthDay(8),
      session_type: "video",
      class_label: null,
      phudao_students: [],
      hours: null,
      student_touches: null,
      papers_graded: null,
      status: "approved",
      reject_reason: null,
    },
    {
      id: "demo-s6",
      work_date: thisMonthDay(10),
      session_type: "hanhchinh",
      class_label: null,
      phudao_students: [],
      hours: 1,
      student_touches: null,
      papers_graded: null,
      status: "approved",
      reject_reason: null,
    },
  ];
}

export function demoClasses(): TaAssistantClass[] {
  return [
    { class_id: -1, name: "11B2 (giả lập)" },
    { class_id: -2, name: "12A1 (giả lập)" },
  ];
}

export function demoTopics(): TaTopicSuggestion[] {
  return [
    {
      session_id: "demo-topic-1",
      work_date: thisMonthDay(1),
      class_label: "12A1",
      error_note: "Quên đổi đơn vị khi thay số vào công thức chu kỳ con lắc đơn.",
    },
    {
      session_id: "demo-topic-2",
      work_date: thisMonthDay(6),
      class_label: "11B2",
      error_note: "Vẽ sai chiều lực căng dây khi vật chuyển động tròn đều.",
    },
  ];
}

export function demoTopic(sessionId: string): TaTopicSuggestion | null {
  return demoTopics().find((t) => t.session_id === sessionId) ?? null;
}

/** Đúng bằng giá trị mặc định của ta_video_rates trong migration. */
export function demoVideoRates(): TaVideoRates {
  return {
    effective_from: dayOffset(365),
    price_don_gian: 120000,
    price_dung_ky: 200000,
    view_threshold_1: 10000,
    view_bonus_1: 50000,
    view_threshold_2: 50000,
    view_bonus_2: 150000,
    lead_bonus: 300000,
    monthly_budget_cap: 1200000,
  };
}

export function demoVideoLedger(): TaVideoLedgerRow[] {
  return [
    {
      session_id: "demo-v1",
      assistant_id: DEMO_ASSISTANT_ID,
      work_date: thisMonthDay(8),
      video_tier: "dung_ky",
      video_url: "https://www.tiktok.com/@thachlab/video/0000000000000000001",
      published_at: `${thisMonthDay(8)}T12:00:00.000Z`,
      status: "approved",
      reject_reason: null,
      topic_source_id: "demo-topic-2",
      latest_checked_at: `${dayOffset(2)}T12:00:00.000Z`,
      latest_views: 62300,
      latest_saves: 1840,
      latest_comments: 96,
      view_bonus: 200000,
      production_pay: 200000,
      lead_count: 1,
      lead_bonus: 300000,
      total_pay: 700000,
    },
    {
      session_id: "demo-v2",
      assistant_id: DEMO_ASSISTANT_ID,
      work_date: thisMonthDay(12),
      video_tier: "don_gian",
      video_url: "https://www.tiktok.com/@thachlab/video/0000000000000000002",
      published_at: `${thisMonthDay(12)}T12:00:00.000Z`,
      status: "approved",
      reject_reason: null,
      topic_source_id: null,
      latest_checked_at: `${dayOffset(2)}T12:00:00.000Z`,
      latest_views: 14800,
      latest_saves: 320,
      latest_comments: 18,
      view_bonus: 50000,
      production_pay: 120000,
      lead_count: 0,
      lead_bonus: 0,
      total_pay: 170000,
    },
    {
      session_id: "demo-v3",
      assistant_id: DEMO_ASSISTANT_ID,
      work_date: thisMonthDay(2),
      video_tier: "don_gian",
      video_url: "https://www.tiktok.com/@thachlab/video/0000000000000000003",
      published_at: `${thisMonthDay(2)}T12:00:00.000Z`,
      status: "submitted",
      reject_reason: null,
      topic_source_id: "demo-topic-1",
      latest_checked_at: null,
      latest_views: 3200,
      latest_saves: 64,
      latest_comments: 5,
      view_bonus: 0,
      production_pay: 120000,
      lead_count: 0,
      lead_bonus: 0,
      total_pay: 120000,
    },
  ];
}
