-- Chỉ đọc: hiện trạng mùa 4, 5 để thiết kế mùa 2 (5/11/2026). Một câu SELECT trả JSON.
select jsonb_pretty(jsonb_build_object(
  'seasons', (select jsonb_agg(to_jsonb(s) - 'created_by' order by s.id) from rank_seasons s),
  'tiers', (select jsonb_agg(jsonb_build_object('season', season_id, 'code', code, 'sort', sort, 'name', name, 'min_rp', min_rp,
            'div', has_divisions, 'req_n', required_title_count, 'req_lv', required_title_level) order by season_id, sort) from rank_tiers),
  'sources_by_kind', (select jsonb_agg(jsonb_build_object('season', season_id, 'kind', source_kind, 'enabled', enabled, 'n', n, 'max_rp', mx))
            from (select season_id, source_kind, enabled, count(*) n, jsonb_agg(distinct max_rp) mx from rank_sources group by 1,2,3) x),
  'rp_dist', (select jsonb_agg(jsonb_build_object('season', season_id, 'p50', p50, 'p90', p90, 'max', mx)) from
            (select season_id, percentile_cont(0.5) within group (order by rp) p50, percentile_cont(0.9) within group (order by rp) p90, max(rp) mx
             from rank_student_seasons group by 1) y),
  'lop9_items', (select jsonb_agg(jsonb_build_object('class', cls, 'kind', kind, 'n', n)) from
            (select cc.class_id cls, i.kind, count(*) n
             from lesson_items i join lessons l on l.id = i.lesson_id join chapter_classes cc on cc.chapter_id = l.chapter_id
             where cc.class_id in (15,19) and l.published and coalesce(array_length(i.exam_ids,1),0) > 0
             group by 1, 2) z)
)) as j;
