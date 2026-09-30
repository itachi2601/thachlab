---
name: thachlab-daily-streak
description: Nhiệm vụ hằng ngày / chuỗi ngày (streak) kiểu Duolingo-Snapchat gắn vào hệ thống rank — đã deploy 25/9/2026
metadata:
  node_type: memory
  type: project
  originSessionId: 295e4a68-9e1c-4c66-ab58-e839048087ff
  modified: 2026-09-25T15:59:57.000Z
---

Thêm nguồn RP "daily_streak" vào [[project_thachlab_rank_system]]: mỗi ngày học sinh hoàn thành >= 1 bài
tính RP đạt từ điểm tối thiểu (dùng chung ngưỡng `weekly_goal_min_score`) thì +`daily_streak_rp` (mặc định 5 RP).
Chuỗi = số ngày liên tiếp có daily_streak; hôm nay chưa xong vẫn tính chuỗi từ hôm qua (không gãy giữa ngày,
kiểu Duolingo/Snapchat — thầy chủ động chọn hướng này khi được hỏi "kiểu TikTok"). Thêm 2 danh hiệu mới:
Chuỗi 7 Ngày, Chuỗi 30 Ngày.

**Why:** thầy muốn đặt việc hằng ngày để học sinh leo rank/lấy danh hiệu, nhưng chọn hướng "gợi ý" thay vì
checklist bắt buộc (hỏi 3 câu qua AskUserQuestion, thầy chọn: gợi ý > checklist cứng; streak kiểu TikTok/Duolingo;
thẻ riêng đặt giữa RankCard và ClassRankBoard).

**How to apply:**
- Migration `docs/supabase-migration-rank-daily-streak.sql` — CREATE OR REPLACE toàn bộ `rank_eval_achievements`,
  `rank_on_result`, `rank_status_of` (copy nguyên thân hàm cũ + thêm khối mới) theo đúng pattern các migration
  incremental khác của rank system (rank-avatar, rank-class-board). Hàm mới: `rank_eval_daily_streak`,
  `rank_daily_streak_len`. Đã chạy migration + `rank_recompute_season(4)` để backfill (160 HS, 28 lượt
  daily_streak) — xác nhận qua RPC test trực tiếp, không có lỗi.
- Component `components/rank/DailyStreakCard.tsx` (ngọn lửa sáng khi `today_done`, dòng gợi ý khi chưa) +
  `RankDaily`/`daily` field trong `features/rank/types.ts` + `RankStatus`. Gắn trong `ThptStudentHome.tsx`
  giữa `RankCard` và `ClassRankBoard`, gợi ý lấy từ dữ liệu đã có sẵn trên trang (bài kiểm tra chưa làm →
  bài học tiếp theo → chủ đề cần phụ đạo), không xây thêm hệ nội dung gợi ý riêng.
- Commit `438e8ed7` (push main + deploy branch `a8c0ba0` xong 25/9/2026, build từ worktree sạch
  `.claude/worktrees/daily-streak-deploy`, không phải scratchpad /tmp — Turbopack lỗi "Symlink node_modules
  points out of filesystem root" khi worktree nằm dưới /private/tmp (symlink) + node_modules cũng symlink;
  chuyển sang `.claude/worktrees/` là hết lỗi).
- **Sự cố phiên song song:** lúc đầu `git update-index --cacheinfo` chạy thẳng lên index THẬT (không phải
  index tạm) để tách hunk `ThptStudentHome.tsx` khỏi WIP thoát-phụ-đạo của phiên khác đang mở cùng lúc — bị
  một phiên khác commit cuốn theo (nằm lẫn trong commit `640774b0` "thêm ảnh lý thuyết..." không liên quan).
  Nội dung đúng, không mất, chỉ sai chỗ. Từ lần sau: luôn dùng `GIT_INDEX_FILE=<file tạm> git read-tree HEAD`
  khi cần tách hunk khỏi working tree dùng chung — KHÔNG chạm index thật khi có nhiều phiên đang chạy. Xem
  [[project_thachlab_concurrent_sessions]].
- CHƯA test bằng tài khoản học sinh thật trên web (chỉ test RPC trực tiếp qua SQL); chưa xem UI thẻ streak
  trên trình duyệt thật.
