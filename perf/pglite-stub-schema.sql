-- Schema stub sinh tự động (25/9/2026) từ information_schema.columns + pg_proc của project,
-- CHỈ để pglite kiểm tra cú pháp migration RLS/RPC (perf/rls-pglite-check.mjs). Không chạy lên DB thật.
create role anon; create role authenticated;
create schema if not exists auth;
create or replace function auth.uid() returns uuid language sql stable as $$ select null::uuid $$;
create or replace function auth.role() returns text language sql stable as $$ select null::text $$;
create or replace function auth.jwt() returns jsonb language sql stable as $$ select null::jsonb $$;

create table public."academic_subjects" (
  "code" text,
  "label" text,
  "icon" text,
  "sort_order" integer,
  "active" boolean
);
create table public."attendance_machine_photos" (
  "id" bigint,
  "session_id" bigint,
  "machine_code" text,
  "checkpoint" text,
  "storage_path" text,
  "note" text,
  "uploaded_by" uuid,
  "created_at" timestamp with time zone
);
create table public."attendance_machine_scores" (
  "session_id" bigint,
  "machine_code" text,
  "bonus_points" integer,
  "note" text,
  "updated_at" timestamp with time zone,
  "sang_loc" boolean,
  "sap_xep" boolean,
  "sach_se" boolean,
  "san_soc" boolean,
  "san_sang" boolean,
  "equipment_status" text
);
create table public."attendance_records" (
  "session_id" bigint,
  "student_id" uuid,
  "status" text,
  "checked_in_at" timestamp with time zone,
  "note" text,
  "marked_by" uuid,
  "updated_at" timestamp with time zone,
  "bonus_points" integer,
  "machine_code" text,
  "machine_selected_at" timestamp with time zone
);
create table public."attendance_session_machines" (
  "session_id" bigint,
  "machine_code" text
);
create table public."attendance_sessions" (
  "id" bigint,
  "course_id" bigint,
  "created_by" uuid,
  "created_at" timestamp with time zone,
  "title" text,
  "session_date" date,
  "starts_at" timestamp with time zone,
  "late_after" timestamp with time zone,
  "closes_at" timestamp with time zone,
  "code" text,
  "status" text,
  "note" text,
  "machine_selection_open" boolean,
  "machine_edit_override" boolean,
  "workshop" text,
  "period" text
);
create table public."bug_reports" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "updated_at" timestamp with time zone,
  "user_id" uuid,
  "reporter_name" text,
  "reporter_email" text,
  "page_url" text,
  "category" text,
  "description" text,
  "screenshot_path" text,
  "status" text,
  "admin_note" text
);
create table public."chapter_classes" (
  "chapter_id" bigint,
  "class_id" bigint
);
create table public."chapters" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "title" text,
  "sort_order" integer,
  "subject_code" text
);
create table public."checklist_attempts" (
  "id" bigint,
  "session_id" bigint,
  "course_id" bigint,
  "lesson_id" text,
  "student_id" uuid,
  "grader_id" uuid,
  "grader_role" text,
  "item_results" jsonb,
  "score" numeric,
  "total" numeric,
  "critical_ok" boolean,
  "zero_tolerance_ok" boolean,
  "passed" boolean,
  "created_at" timestamp with time zone,
  "started_at" timestamp with time zone,
  "duration_seconds" integer
);
create table public."checklist_sessions" (
  "id" bigint,
  "course_id" bigint,
  "lesson_id" text,
  "created_by" uuid,
  "created_at" timestamp with time zone,
  "title" text,
  "starts_at" timestamp with time zone,
  "closes_at" timestamp with time zone,
  "code" text,
  "status" text
);
create table public."checklist_work_starts" (
  "session_id" bigint,
  "course_id" bigint,
  "lesson_id" text,
  "student_id" uuid,
  "grader_id" uuid,
  "started_at" timestamp with time zone
);
create table public."class_announcements" (
  "id" bigint,
  "class_id" bigint,
  "kind" text,
  "body" text,
  "created_by" uuid,
  "created_at" timestamp with time zone
);
create table public."class_assessments" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "class_id" bigint,
  "exam_id" bigint,
  "lesson_id" bigint,
  "kind" text,
  "term" text,
  "sequence" integer,
  "weight" numeric,
  "published_at" timestamp with time zone
);
create table public."class_instructors" (
  "class_id" bigint,
  "instructor_id" uuid,
  "assigned_by" uuid,
  "assigned_at" timestamp with time zone
);
create table public."classes" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "name" text,
  "slug" text,
  "color" text,
  "icon" text,
  "sort_order" integer,
  "active" boolean
);
create table public."cnc_competency_permissions" (
  "course_id" bigint,
  "student_id" uuid,
  "competency_id" text,
  "status" text,
  "note" text,
  "approved_by" uuid,
  "approved_at" timestamp with time zone,
  "updated_at" timestamp with time zone
);
create table public."cnc_drawing_submissions" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "updated_at" timestamp with time zone,
  "student_id" uuid,
  "lesson_id" text,
  "file_name" text,
  "storage_path" text,
  "mime_type" text,
  "size_bytes" bigint,
  "status" text,
  "teacher_feedback" text,
  "reviewed_by" uuid,
  "reviewed_at" timestamp with time zone,
  "course_id" bigint
);
create table public."cnc_learning_records" (
  "course_id" bigint,
  "student_id" uuid,
  "lesson_id" text,
  "assessment_id" text,
  "completed" boolean,
  "latest_score" integer,
  "best_score" integer,
  "total_questions" integer,
  "attempt_count" integer,
  "last_activity_at" timestamp with time zone
);
create table public."cnc_lesson_files" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "lesson_id" text,
  "kind" text,
  "title" text,
  "file_name" text,
  "file_url" text,
  "storage_path" text,
  "mime_type" text,
  "size_bytes" bigint
);
create table public."cnc_lesson_videos" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "lesson_id" text,
  "title" text,
  "youtube_url" text,
  "youtube_id" text,
  "sort_order" integer
);
create table public."cnc_lessons" (
  "id" text,
  "title" text,
  "short_title" text,
  "duration_label" text,
  "emphasis" text,
  "body_html" text,
  "resources" jsonb,
  "sort_order" integer,
  "created_at" timestamp with time zone
);
create table public."cnc_milling_checklist_attempts" (
  "id" bigint,
  "student_id" uuid,
  "participant_key" uuid,
  "participant_name" text,
  "class_name" text,
  "checked" jsonb,
  "zero_tolerance" jsonb,
  "score" numeric,
  "max_score" numeric,
  "critical_passed" boolean,
  "zero_tolerance_passed" boolean,
  "status" text,
  "started_at" timestamp with time zone,
  "last_activity_at" timestamp with time zone,
  "passed_at" timestamp with time zone
);
create table public."cnc_milling_quiz_attempts" (
  "id" bigint,
  "student_id" uuid,
  "answers" jsonb,
  "answered_count" integer,
  "score" integer,
  "total_questions" integer,
  "status" text,
  "started_at" timestamp with time zone,
  "last_activity_at" timestamp with time zone,
  "submitted_at" timestamp with time zone,
  "participant_key" uuid,
  "participant_name" text,
  "class_name" text,
  "course_id" bigint
);
create table public."cnc_quiz_questions" (
  "id" text,
  "quiz_key" text,
  "question_type" text,
  "question" text,
  "options" jsonb,
  "correct_index" integer,
  "keywords" jsonb,
  "min_keyword_matches" integer,
  "explanation" text,
  "order_index" integer,
  "updated_by" uuid,
  "updated_at" timestamp with time zone
);
create table public."course_enrollments" (
  "course_id" bigint,
  "student_id" uuid,
  "enrolled_at" timestamp with time zone,
  "status" text,
  "approved_at" timestamp with time zone,
  "approved_by" uuid
);
create table public."course_grade_overrides" (
  "course_id" bigint,
  "student_id" uuid,
  "grade_key" text,
  "score" numeric,
  "updated_by" uuid,
  "updated_at" timestamp with time zone
);
create table public."course_instructors" (
  "course_id" bigint,
  "instructor_id" uuid,
  "assigned_by" uuid,
  "assigned_at" timestamp with time zone
);
create table public."course_offerings" (
  "id" bigint,
  "subject_id" bigint,
  "created_by" uuid,
  "created_at" timestamp with time zone,
  "name" text,
  "class_label" text,
  "school_year" text,
  "join_code" text,
  "enrollment_mode" text,
  "starts_at" date,
  "ends_at" date,
  "status" text,
  "open_lesson_ids" text[]
);
create table public."equipment_breakdown_reports" (
  "id" bigint,
  "course_id" bigint,
  "session_id" bigint,
  "machine_code" text,
  "description" text,
  "broken_photo_path" text,
  "status" text,
  "reported_by" uuid,
  "resolved_by" uuid,
  "resolved_at" timestamp with time zone,
  "resolved_note" text,
  "created_at" timestamp with time zone,
  "resolved_photo_path" text,
  "broken_at" timestamp with time zone,
  "assigned_to" uuid
);
create table public."exam_attempts" (
  "id" bigint,
  "client_token" uuid,
  "student_id" uuid,
  "exam_id" bigint,
  "item_id" bigint,
  "started_at" timestamp with time zone,
  "submitted_at" timestamp with time zone,
  "exam_result_id" bigint,
  "responses" jsonb,
  "seconds_left" integer,
  "saved_at" timestamp with time zone
);
create table public."exam_classes" (
  "exam_id" bigint,
  "class_id" bigint
);
create table public."exam_question_results" (
  "exam_result_id" bigint,
  "question_index" integer,
  "student_id" uuid,
  "exam_id" bigint,
  "topic_id" bigint,
  "topic_name" text,
  "form" text,
  "qtype" text,
  "earned" numeric,
  "max" numeric,
  "is_correct" boolean,
  "estimated" boolean,
  "created_at" timestamp with time zone,
  "manual_earned" numeric,
  "manual_max" numeric,
  "graded_by" uuid,
  "graded_at" timestamp with time zone
);
create table public."exam_results" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "student_id" uuid,
  "exam_id" bigint,
  "score" numeric,
  "detail" jsonb,
  "duration_seconds" integer,
  "course_id" bigint,
  "violation_count" integer,
  "violations" jsonb,
  "client_token" uuid
);
create table public."exams" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "title" text,
  "duration_minutes" integer,
  "published" boolean,
  "questions" jsonb,
  "question_count" integer,
  "topic" text,
  "difficulty" text,
  "type_counts" jsonb,
  "subject_code" text,
  "cnc_key" text,
  "pass_score" numeric
);
create table public."homeroom_daily_attendance" (
  "id" bigint,
  "course_id" bigint,
  "attendance_date" date,
  "headcount" integer,
  "present_count" integer,
  "absentees" jsonb,
  "submitted_by" uuid,
  "submitted_at" timestamp with time zone,
  "updated_at" timestamp with time zone
);
create table public."homeroom_monitors" (
  "course_id" bigint,
  "student_id" uuid,
  "role" text,
  "assigned_by" uuid,
  "assigned_at" timestamp with time zone
);
create table public."homeroom_term_records" (
  "course_id" bigint,
  "student_id" uuid,
  "term" text,
  "exam_score" numeric,
  "conduct" text,
  "note" text,
  "updated_by" uuid,
  "updated_at" timestamp with time zone
);
create table public."homeroom_weekly_sessions" (
  "id" bigint,
  "course_id" bigint,
  "week_no" integer,
  "met_on" date,
  "announcements" jsonb,
  "ethics_topic" text,
  "ethics_taught" jsonb,
  "headcount" integer,
  "present_count" integer,
  "created_by" uuid,
  "created_at" timestamp with time zone,
  "updated_at" timestamp with time zone
);
create table public."lesson_items" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "lesson_id" bigint,
  "kind" text,
  "title" text,
  "subtitle" text,
  "body_html" text,
  "video_url" text,
  "pdf_url" text,
  "sort_order" integer,
  "exam_ids" int8[],
  "questions" jsonb,
  "due_at" timestamp with time zone,
  "quiz_min_correct" integer,
  "practice_pass_score" numeric,
  "required" boolean
);
create table public."lesson_progress" (
  "user_id" uuid,
  "item_id" bigint,
  "done_at" timestamp with time zone,
  "course_id" bigint
);
create table public."lessons" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "chapter_id" bigint,
  "title" text,
  "sort_order" integer,
  "published" boolean,
  "lesson_kind" text,
  "description" text
);
create table public."machine_status_log" (
  "id" bigint,
  "machine_code" text,
  "status" text,
  "note" text,
  "created_by" uuid,
  "updated_by" uuid,
  "created_at" timestamp with time zone,
  "updated_at" timestamp with time zone
);
create table public."machines" (
  "code" text,
  "label" text,
  "machine_type" text,
  "is_active" boolean,
  "created_at" timestamp with time zone,
  "workshop" text,
  "status" text,
  "note" text
);
create table public."messages" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "sender_id" uuid,
  "recipient_id" uuid,
  "class_name" text,
  "subject" text,
  "body" text
);
create table public."notifications" (
  "id" bigint,
  "user_id" uuid,
  "kind" text,
  "title" text,
  "body" text,
  "href" text,
  "created_at" timestamp with time zone,
  "read_at" timestamp with time zone
);
create table public."parent_links" (
  "id" uuid,
  "code" text,
  "student_id" uuid,
  "parent_id" uuid,
  "label" text,
  "created_by" uuid,
  "created_at" timestamp with time zone,
  "claimed_at" timestamp with time zone
);
create table public."post_classes" (
  "post_id" bigint,
  "class_id" bigint
);
create table public."post_courses" (
  "post_id" bigint,
  "course_id" bigint
);
create table public."posts" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "title" text,
  "body" text,
  "video_url" text,
  "published" boolean,
  "topic" text,
  "content_type" text,
  "subject_code" text
);
create table public."practice_question_results" (
  "session_id" bigint,
  "question_index" integer,
  "student_id" uuid,
  "exam_id" bigint,
  "source_index" integer,
  "topic_id" bigint,
  "topic_name" text,
  "form" text,
  "qtype" text,
  "earned" numeric,
  "max" numeric,
  "is_correct" boolean,
  "created_at" timestamp with time zone
);
create table public."practice_sessions" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "student_id" uuid,
  "lesson_id" bigint,
  "item_id" bigint,
  "question_count" integer,
  "correct_count" integer,
  "score" numeric,
  "duration_seconds" integer,
  "timed_out" boolean,
  "client_token" uuid
);
create table public."profiles" (
  "id" uuid,
  "created_at" timestamp with time zone,
  "full_name" text,
  "class_name" text,
  "role" text,
  "student_code" text,
  "admin_area" text,
  "birth_date" date,
  "track" text,
  "display_title_code" text,
  "display_title_level" text,
  "avatar_url" text
);
create table public."question_bank" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "updated_at" timestamp with time zone,
  "subject_code" text,
  "grade" text,
  "topic_id" bigint,
  "topic_name" text,
  "form" text,
  "qtype" text,
  "difficulty" text,
  "question" jsonb,
  "content_hash" text,
  "source_exam_id" bigint,
  "source_index" integer,
  "archived" boolean,
  "note" text
);
create table public."question_topics" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "subject_code" text,
  "grade" text,
  "chapter_id" bigint,
  "lesson_id" bigint,
  "name" text,
  "sort_order" integer,
  "parent_id" bigint
);
create table public."rank_fix_attempts" (
  "id" bigint,
  "student_id" uuid,
  "season_id" bigint,
  "exam_result_id" bigint,
  "exam_id" bigint,
  "topic_id" bigint,
  "question_ids" int8[],
  "total" integer,
  "correct" integer,
  "pct" integer,
  "passed" boolean,
  "status" text,
  "created_at" timestamp with time zone,
  "submitted_at" timestamp with time zone
);
create table public."rank_gate_passes" (
  "season_id" bigint,
  "student_id" uuid,
  "tier_code" text,
  "passed_at" timestamp with time zone,
  "evidence" jsonb
);
create table public."rank_rp_awards" (
  "season_id" bigint,
  "student_id" uuid,
  "source_kind" text,
  "source_ref" text,
  "awarded" integer,
  "best_value" numeric,
  "updated_at" timestamp with time zone
);
create table public."rank_rp_ledger" (
  "id" bigint,
  "season_id" bigint,
  "student_id" uuid,
  "source_kind" text,
  "source_ref" text,
  "amount" integer,
  "reason" text,
  "ref_result_id" bigint,
  "actor" uuid,
  "created_at" timestamp with time zone
);
create table public."rank_season_results" (
  "season_id" bigint,
  "student_id" uuid,
  "rp" integer,
  "tier_code" text,
  "division" integer,
  "titles_count" integer,
  "closed_at" timestamp with time zone
);
create table public."rank_seasons" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "created_by" uuid,
  "name" text,
  "starts_on" date,
  "ends_on" date,
  "class_ids" int8[],
  "status" text,
  "config" jsonb,
  "boss_exam_id" bigint,
  "boss_pass_score" numeric,
  "closed_at" timestamp with time zone
);
create table public."rank_sources" (
  "season_id" bigint,
  "source_kind" text,
  "source_id" bigint,
  "max_rp" integer,
  "enabled" boolean
);
create table public."rank_student_seasons" (
  "season_id" bigint,
  "student_id" uuid,
  "rp" integer,
  "tier_code" text,
  "tier_sort" integer,
  "division" integer,
  "tier_reached_at" timestamp with time zone,
  "joined_at" timestamp with time zone,
  "updated_at" timestamp with time zone
);
create table public."rank_tiers" (
  "season_id" bigint,
  "code" text,
  "sort" integer,
  "name" text,
  "min_rp" integer,
  "has_divisions" boolean,
  "required_title_count" integer,
  "required_title_level" text,
  "challenge_exam_id" bigint,
  "challenge_pass_score" numeric
);
create table public."rank_title_awards" (
  "id" bigint,
  "student_id" uuid,
  "title_code" text,
  "level" text,
  "season_id" bigint,
  "evidence" jsonb,
  "awarded_at" timestamp with time zone
);
create table public."rank_title_topics" (
  "title_code" text,
  "topic_id" bigint
);
create table public."rank_titles" (
  "code" text,
  "group_code" text,
  "kind" text,
  "name" text,
  "description" text,
  "sort" integer,
  "min_questions" integer,
  "awaken_accuracy" integer,
  "master_accuracy" integer,
  "legend_challenge_exam_id" bigint,
  "legend_accuracy" integer,
  "requires" jsonb,
  "enabled" boolean
);
create table public."rubric_exam_attempts" (
  "id" bigint,
  "course_id" bigint,
  "student_id" uuid,
  "machine" text,
  "role" text,
  "grader_id" uuid,
  "item_levels" jsonb,
  "zero_tolerance_confirmed" jsonb,
  "ky_thuat_score" numeric,
  "thanh_phan_score" numeric,
  "total_score" numeric,
  "xep_loai" text,
  "notes" text,
  "created_at" timestamp with time zone,
  "updated_at" timestamp with time zone
);
create table public."staff_invites" (
  "id" uuid,
  "email" text,
  "full_name" text,
  "role" text,
  "admin_area" text,
  "class_id" bigint,
  "course_id" bigint,
  "tier" text,
  "invited_by" uuid,
  "invited_at" timestamp with time zone,
  "claimed_at" timestamp with time zone,
  "claimed_user_id" uuid,
  "code" text
);
create table public."student_alerts" (
  "id" bigint,
  "student_id" uuid,
  "class_id" bigint,
  "kind" text,
  "severity" text,
  "reason" text,
  "assessment_ids" int8[],
  "status" text,
  "assigned_to" uuid,
  "handled_by" uuid,
  "handled_note" text,
  "created_at" timestamp with time zone,
  "updated_at" timestamp with time zone
);
create table public."student_learning_presence" (
  "student_id" uuid,
  "lesson_id" bigint,
  "activity_type" text,
  "lesson_opened_at" timestamp with time zone,
  "last_seen_at" timestamp with time zone
);
create table public."subjects" (
  "id" bigint,
  "code" text,
  "name" text,
  "area" text,
  "active" boolean,
  "is_practicum" boolean
);
create table public."ta_assistant_classes" (
  "assistant_id" uuid,
  "class_id" bigint,
  "assigned_by" uuid,
  "assigned_at" timestamp with time zone
);
create table public."ta_assistants" (
  "id" uuid,
  "user_id" uuid,
  "full_name" text,
  "short_name" text,
  "tier" text,
  "retained_rate" integer,
  "bank_name" text,
  "bank_account" text,
  "active" boolean,
  "started_at" date,
  "created_at" timestamp with time zone
);
create table public."ta_flags" (
  "id" uuid,
  "assistant_id" uuid,
  "flag_date" date,
  "note" text,
  "created_at" timestamp with time zone
);
create table public."ta_leads" (
  "id" uuid,
  "student_name" text,
  "source" text,
  "attributed_session_id" uuid,
  "registered_at" date,
  "created_by" uuid,
  "created_at" timestamp with time zone
);
create table public."ta_month_reviews" (
  "assistant_id" uuid,
  "month" date,
  "scores" jsonb,
  "hourly_rate" integer,
  "note" text,
  "closed_at" timestamp with time zone,
  "snapshot" jsonb,
  "updated_by" uuid,
  "updated_at" timestamp with time zone
);
create table public."ta_policy_audit" (
  "id" bigint,
  "assistant_id" uuid,
  "month" date,
  "actor_id" uuid,
  "action" text,
  "before_value" jsonb,
  "after_value" jsonb,
  "created_at" timestamp with time zone
);
create table public."ta_rates" (
  "id" uuid,
  "tier" text,
  "effective_from" date,
  "base_rate" integer
);
create table public."ta_sessions" (
  "id" uuid,
  "assistant_id" uuid,
  "work_date" date,
  "session_type" text,
  "class_label" text,
  "start_time" time without time zone,
  "end_time" time without time zone,
  "hours" numeric,
  "student_touches" integer,
  "touch_names" text[],
  "error_note" text,
  "error_note_at" timestamp with time zone,
  "homework_given" text,
  "student_recap_ok" boolean,
  "papers_graded" integer,
  "video_url" text,
  "video_tier" text,
  "published_at" timestamp with time zone,
  "topic_source_id" uuid,
  "note" text,
  "status" text,
  "reject_reason" text,
  "created_at" timestamp with time zone,
  "approved_at" timestamp with time zone,
  "phudao_students" text[],
  "policy" jsonb,
  "class_id" bigint,
  "phudao_student_ids" uuid[]
);
create table public."ta_settings" (
  "id" boolean,
  "course_hours_cap" integer,
  "updated_at" timestamp with time zone
);
create table public."ta_video_rates" (
  "id" uuid,
  "effective_from" date,
  "price_don_gian" integer,
  "price_dung_ky" integer,
  "view_threshold_1" integer,
  "view_bonus_1" integer,
  "view_threshold_2" integer,
  "view_bonus_2" integer,
  "lead_bonus" integer,
  "monthly_budget_cap" integer
);
create table public."ta_video_stats" (
  "id" uuid,
  "session_id" uuid,
  "checked_at" date,
  "views" integer,
  "saves" integer,
  "comments" integer,
  "created_at" timestamp with time zone
);
create table public."thpt_attendance_records" (
  "session_id" bigint,
  "student_id" uuid,
  "status" text,
  "note" text,
  "marked_by" uuid,
  "marked_at" timestamp with time zone
);
create table public."thpt_attendance_sessions" (
  "id" bigint,
  "class_id" bigint,
  "created_by" uuid,
  "created_at" timestamp with time zone,
  "title" text,
  "session_date" date,
  "starts_at" timestamp with time zone,
  "note" text
);
create table public."thpt_course_schedules" (
  "id" bigint,
  "course_id" bigint,
  "weekday" smallint,
  "start_time" time without time zone,
  "end_time" time without time zone,
  "location" text
);
create table public."thpt_courses" (
  "id" bigint,
  "class_id" bigint,
  "name" text,
  "description" text,
  "school_year" text,
  "starts_at" date,
  "ends_at" date,
  "capacity" integer,
  "fee_note" text,
  "is_public" boolean,
  "status" text,
  "created_by" uuid,
  "created_at" timestamp with time zone,
  "current_topic_id" bigint,
  "pair_key" text,
  "pair_slot" text
);
create table public."thpt_registration_requests" (
  "id" bigint,
  "created_at" timestamp with time zone,
  "updated_at" timestamp with time zone,
  "user_id" uuid,
  "requested_class_id" bigint,
  "full_name" text,
  "username" text,
  "email" text,
  "phone" text,
  "parent_phone" text,
  "birth_date" date,
  "gender" text,
  "student_code" text,
  "status" text,
  "reviewed_by" uuid,
  "reviewed_at" timestamp with time zone
);
create table public."thpt_registrations" (
  "id" bigint,
  "course_id" bigint,
  "student_id" uuid,
  "registered_by" uuid,
  "child_name" text,
  "contact" text,
  "note" text,
  "status" text,
  "joined_late" boolean,
  "payment_status" text,
  "payment_note" text,
  "created_at" timestamp with time zone,
  "reviewed_by" uuid,
  "reviewed_at" timestamp with time zone,
  "known_topic_ids" int8[],
  "catchup_topic_ids" int8[],
  "catchup_done_topic_ids" int8[]
);
create table public."tutoring_exit_attempts" (
  "id" bigint,
  "tutoring_need_id" bigint,
  "student_id" uuid,
  "topic_id" bigint,
  "form" text,
  "question_ids" int8[],
  "total" integer,
  "correct" integer,
  "pct" integer,
  "passed" boolean,
  "created_at" timestamp with time zone
);
create table public."tutoring_needs" (
  "id" bigint,
  "student_id" uuid,
  "class_id" bigint,
  "topic_id" bigint,
  "form" text,
  "wrong" integer,
  "total" integer,
  "pct" integer,
  "source" text,
  "status" text,
  "assigned_to" uuid,
  "note" text,
  "first_seen_at" timestamp with time zone,
  "last_seen_at" timestamp with time zone,
  "tutored_at" timestamp with time zone,
  "cleared_at" timestamp with time zone,
  "updated_at" timestamp with time zone
);
create table public."tutoring_registrations" (
  "id" bigint,
  "slot_id" bigint,
  "student_id" uuid,
  "created_at" timestamp with time zone
);
create table public."tutoring_session_topics" (
  "id" bigint,
  "session_id" uuid,
  "student_id" uuid,
  "topic_id" bigint,
  "need_id" bigint,
  "note" text,
  "created_at" timestamp with time zone
);
create table public."tutoring_slots" (
  "id" bigint,
  "assistant_id" uuid,
  "class_id" bigint,
  "work_date" date,
  "start_time" time without time zone,
  "end_time" time without time zone,
  "topic_ids" int8[],
  "capacity" integer,
  "registered_count" integer,
  "note" text,
  "status" text,
  "created_at" timestamp with time zone
);
create table public."user_classes" (
  "user_id" uuid,
  "class_id" bigint,
  "status" text,
  "requested_at" timestamp with time zone,
  "reviewed_by" uuid,
  "reviewed_at" timestamp with time zone
);

-- hàm public: stub cùng chữ ký, thân raise (migration sẽ create or replace những hàm cần sửa)
create or replace function public.add_machine_status_log(p_machine_code text, p_status text, p_note text) returns bigint language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.admin_search_accounts(p_query text, p_role text) returns TABLE(id uuid, full_name text, class_name text, student_code text, role text, admin_area text, track text, email text, ta_tier text, ta_active boolean) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.admin_set_account_role(p_user_id uuid, p_role text, p_tier text) returns text language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.apply_parent_link(p_user_id uuid, p_code text) returns uuid language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.apply_staff_invite(p_user_id uuid, p_email text, p_code text) returns uuid language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.assists_class(p_class bigint) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.can_manage_class(p_class_id bigint) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.can_manage_course(p_course_id bigint) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.claim_parent_link(p_code text) returns TABLE(student_name text, class_name text) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.claim_staff_invite(p_code text) returns TABLE(role text, class_name text, tier text) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.cleanup_old_machine_photos(p_course_id bigint, p_keep_session_id bigint) returns text[] language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.count_question_types(qs jsonb) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.create_post_with_targets(p_title text, p_body text, p_video_url text, p_content_type text, p_subject_code text, p_class_ids bigint[], p_course_ids bigint[]) returns bigint language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.evaluate_student_alerts(p_student uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.find_similar_bank_questions(p_grade text, p_threshold real) returns TABLE(topic_id bigint, topic_name text, id1 bigint, id2 bigint, similarity real) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.get_exam_rank(p_exam_id bigint) returns TABLE(rnk integer, total integer, my_best numeric) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.get_periodic_rank(p_class_id bigint) returns TABLE(rnk integer, total integer, my_avg numeric, class_avg numeric) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.get_periodic_rank_of(p_student uuid, p_class_id bigint) returns TABLE(rnk integer, total integer, my_avg numeric, class_avg numeric) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.grade_essay_answer(p_exam_result_id bigint, p_question_index integer, p_earned numeric, p_max numeric) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.handle_new_user() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.is_admin() returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.is_course_member(p_course_id bigint) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.is_first_on_machine(p_session_id bigint, p_machine_code text) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.is_homeroom_classmate(p_profile_id uuid) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.is_homeroom_monitor(p_course_id bigint) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.is_parent_of(p_student uuid) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.is_photo_duty_machine(p_session_id bigint, p_machine_code text) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.is_photo_duty_workshop(p_session_id bigint) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.list_cnc_course_classmates(p_course_id bigint) returns TABLE(student_id uuid, full_name text, class_name text) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.manages_class(p_class bigint) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.notify_class_staff(p_class_id bigint, p_kind text, p_title text, p_body text, p_href text, p_except uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.notify_student_side(p_student uuid, p_kind text, p_title text, p_body text, p_href_student text, p_href_parent text, p_extra uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.notify_user(p_user uuid, p_kind text, p_title text, p_body text, p_href text) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.question_bank_plain_text(q jsonb) returns text language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.question_content_hash(q jsonb) returns text language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.question_topic_sync_children() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.question_topic_tree_guard() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_adjust_rp(p_season bigint, p_student uuid, p_delta integer, p_reason text) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_award(p_season bigint, p_student uuid, p_kind text, p_ref text, p_value integer, p_reason text, p_result_ref bigint) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_best_pct(p_student uuid, p_exam bigint, p_from timestamp with time zone, p_to timestamp with time zone) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_can_view(p_student uuid) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_cfg(p_season bigint, p_key text, p_default numeric) returns numeric language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_class_board(p_class_id bigint) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_class_groups(p_class_id bigint) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_close_season(p_season bigint) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_create_season(p_name text, p_starts date, p_ends date, p_class_ids bigint[], p_activate boolean) returns bigint language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_display_title_guard() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_ensure_member(p_season bigint, p_student uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_eval_achievements(p_season bigint, p_student uuid, p_at timestamp with time zone) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_eval_gates(p_season bigint, p_student uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_eval_titles(p_student uuid, p_season bigint) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_eval_weekly_goal(p_season bigint, p_student uuid, p_at timestamp with time zone) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_fix_quiz_start(p_exam_result_id bigint, p_topic_id bigint) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_fix_quiz_submit(p_attempt_id bigint, p_correct integer) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_grant_title(p_student uuid, p_title text, p_level text, p_season bigint, p_evidence jsonb) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_is_staff() returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_ledger_of(p_student uuid, p_season bigint, p_limit integer) returns TABLE(id bigint, season_id bigint, source_kind text, source_ref text, amount integer, reason text, ref_result_id bigint, actor_name text, created_at timestamp with time zone) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_level_rank(p_level text) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_my_status() returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_my_titles() returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_on_result(p_student uuid, p_kind text, p_source_id bigint, p_score numeric, p_at timestamp with time zone, p_result_ref bigint) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_recompute_season(p_season bigint) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_recompute_student(p_season bigint, p_student uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_refresh_student(p_season bigint, p_student uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_score_to_rp(p_score numeric, p_max integer) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_season_for_at(p_student uuid, p_at timestamp with time zone) returns bigint language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_season_overview(p_season bigint) returns TABLE(student_id uuid, full_name text, class_names text, rp integer, tier_code text, tier_sort integer, division integer, titles_count integer, last_award_at timestamp with time zone, pending_gate text) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_seasons_guard() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_seasons_of(p_student uuid) returns TABLE(season_id bigint, name text, starts_on date, ends_on date, status text, rp integer, tier_code text, division integer, titles_count integer) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_seed_tiers(p_season bigint) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_set_display_title(p_code text, p_level text) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_status_of(p_student uuid) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_tier_code_by_rp(p_season bigint, p_rp integer) returns text language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_tier_info(p_season bigint, p_code text, p_rp integer) returns TABLE(code text, name text, sort integer, tier_min integer, next_min integer, division integer, div_min integer, div_max integer) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_tier_needs_gate(t rank_tiers) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_tiers_guard() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_title_is_active(p_title text) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_title_stats(p_student uuid, p_title text) returns TABLE(n integer, correct integer, covered integer, total_topics integer, acc integer) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.rank_titles_at_level(p_student uuid, p_level text) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_titles_of(p_student uuid) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_vn_date(p_at timestamp with time zone) returns date language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.rank_week_start(p_at timestamp with time zone) returns date language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.record_cnc_learning_result(p_course_id bigint, p_lesson_id text, p_assessment_id text, p_score integer, p_total integer, p_completed boolean) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.refresh_class_tutoring_needs(p_class bigint) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.refresh_tutoring_needs(p_student uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.report_equipment_breakdown(p_course_id bigint, p_session_id bigint, p_machine_code text, p_description text, p_storage_path text, p_broken_at timestamp with time zone, p_reported_by uuid) returns bigint language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.report_equipment_breakdown(p_course_id bigint, p_session_id bigint, p_machine_code text, p_description text, p_storage_path text, p_broken_at timestamp with time zone) returns bigint language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.request_course_enrollment(p_join_code text) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.resolve_equipment_breakdown(p_id bigint, p_note text, p_resolved_photo_path text) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.resolve_equipment_breakdown(p_id bigint, p_note text, p_resolved_photo_path text, p_resolved_by uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.review_thpt_registration(p_request_id bigint, p_status text) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.seed_absent_attendance_for_enrollment() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.seed_absent_attendance_for_session() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.select_attendance_machine(p_session_id bigint, p_machine_code text) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.set_profile_track_cttc() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.set_profile_track_thpt() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.start_checklist_attempt(p_course_id bigint, p_code text, p_student_id uuid, p_lesson_id text) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.start_equipment_repair(p_id bigint) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.start_equipment_repair(p_id bigint, p_assigned_to uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.student_outcome_gaps(p_students uuid[], p_window integer) returns TABLE(student_id uuid, parent_topic_id bigint, topic_id bigint, topic_name text, form text, total integer, wrong integer) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.submit_attendance_code(p_course_id bigint, p_code text) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.submit_attendance_machine_photo(p_session_id bigint, p_machine_code text, p_checkpoint text, p_storage_path text, p_note text) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.submit_checklist_result(p_course_id bigint, p_code text, p_student_id uuid, p_lesson_id text, p_item_results jsonb, p_score numeric, p_critical_ok boolean, p_zero_tolerance_ok boolean, p_passed boolean) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.sweep_missed_assessments(p_class bigint, p_days integer) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.sync_exam_to_bank(p_exam_id bigint) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.ta_accrued_hours(p_assistant_id uuid) returns numeric language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.ta_converted_hours(p_session_type text, p_hours numeric, p_student_count integer) returns numeric language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.ta_course_total_hours() returns numeric language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.ta_current_assistant_id() returns uuid language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.ta_monthly_policy(p_assistant_id uuid, p_month date) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.ta_monthly_score(p_assistant_id uuid, p_month date) returns TABLE(assistant_id uuid, month date, lop_sessions integer, phudao_sessions integer, avg_touches numeric, touches_score numeric, ontime_error_notes integer, error_note_rate numeric, error_note_score numeric, complete_phudao integer, phudao_complete_rate numeric, phudao_score numeric, flag_count integer, focus_score numeric, total_score numeric, bonus_per_hour integer, converted_hours numeric, papers_graded integer, base_pay numeric, bonus_pay numeric, grading_pay numeric, total_pay numeric) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.ta_policy_session_guard() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.ta_policy_today() returns date language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.ta_save_month_review(p_assistant_id uuid, p_month date, p_scores jsonb, p_rate integer, p_note text, p_close boolean) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.ta_session_student_count(p_students text[]) returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.ta_session_student_link_guard() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.ta_team_monthly_hours(p_months integer) returns TABLE(month date, converted_hours numeric, session_count integer) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.ta_topic_exploitation_rate(p_days integer) returns TABLE(eligible_count integer, used_count integer, rate numeric) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.ta_video_admin_summary(p_month date) returns TABLE(month date, videos_published integer, total_views numeric, total_saves numeric, total_comments numeric, leads_count integer, production_spend numeric, view_bonus_spend numeric, lead_bonus_spend numeric, total_spend numeric, budget_cap integer, over_budget boolean, cost_per_lead numeric) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.ta_video_ledger(p_assistant_id uuid) returns TABLE(session_id uuid, assistant_id uuid, work_date date, video_tier text, video_url text, published_at timestamp with time zone, status text, reject_reason text, topic_source_id uuid, latest_checked_at date, latest_views integer, latest_saves integer, latest_comments integer, view_bonus numeric, production_pay numeric, lead_count integer, lead_bonus numeric, total_pay numeric) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.ta_video_topic_suggestions(p_days integer) returns TABLE(session_id uuid, work_date date, class_label text, error_note text) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.teaches_student(p_student uuid) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.thpt_attach_student(p_id bigint, p_student_id uuid) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.thpt_course_grade(p_course_id bigint) returns text language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.thpt_course_seats(p_course_ids bigint[]) returns TABLE(course_id bigint, taken integer) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.thpt_has_registration(p_course_id bigint) returns boolean language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.thpt_register(p_course_id bigint, p_student_id uuid, p_child_name text, p_contact text, p_note text) returns jsonb language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.thpt_registration_display_name(p_reg thpt_registrations) returns text language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.thpt_review_registration(p_id bigint, p_status text) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.thpt_set_catchup(p_registration_id bigint, p_known_topic_ids bigint[]) returns bigint[] language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.thpt_taught_topics(p_course_id bigint) returns TABLE(id bigint, name text, chapter_id bigint, chapter_title text, sort_order integer) language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.touch_student_alert() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.touch_tutoring_need() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_bank_tags_to_exams() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_bank_touch() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_catchup_progress() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_claim_parent_link() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_claim_staff_invite() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_eqr_tutoring_needs() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_exam_classes_sync_bank() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_exam_result_alert() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_exams_sync_bank() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_notify_parent_linked() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_notify_registration() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_notify_slot_for_catchup() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_question_topics_rename_bank() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_rank_exam_result() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_rank_practice_session() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_rank_question_results() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_sync_thpt_registration() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_ta_assistant_role() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_ta_sessions_error_note_at() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_ta_sessions_video_topic_check() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_tutoring_covered() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.trg_tutoring_exit_attempt_clear() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.tutoring_exit_attempt_guard() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.tutoring_slot_register() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.tutoring_slot_unregister() returns trigger language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.unread_notification_count() returns integer language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
create or replace function public.update_machine_status_log(p_id bigint, p_status text, p_note text, p_created_at timestamp with time zone) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.update_post_with_targets(p_post_id bigint, p_title text, p_body text, p_video_url text, p_content_type text, p_subject_code text, p_class_ids bigint[], p_course_ids bigint[]) returns void language plpgsql as $$ begin raise exception 'stub'; end $$;
create or replace function public.vn_today() returns date language plpgsql as $$ begin raise exception 'stub'; return null; end $$;
