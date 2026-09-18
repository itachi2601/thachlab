"use client";

import { useEffect, useState } from "react";
import { getSupabase } from "@/services/supabase";

type ExamOption = { id: number; title: string; published: boolean; duration_minutes: number };
const columns = "id, title, published, duration_minutes";
const pageSize = 12;
const control = "rounded-lg border border-white/15 bg-[#0B1020] px-3 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500";
const button = "rounded-lg border border-white/15 px-3 py-1.5 text-xs text-slate-300 hover:bg-white/10 disabled:opacity-40";

export default function ExamPicker({ value, onChange }: {
  value: number[];
  onChange: (ids: number[]) => void;
}) {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("all");
  const [page, setPage] = useState(0);
  const [retry, setRetry] = useState(0);
  const [result, setResult] = useState<{ rows: ExamOption[]; count: number; key: string } | null>(null);
  const [cache, setCache] = useState<Record<number, ExamOption>>({});
  const [failure, setFailure] = useState<{ key: string; message: string } | null>(null);
  const [selectionError, setSelectionError] = useState("");
  const requestKey = JSON.stringify([search, status, page, retry]);
  const selectedKey = value.join(",");

  useEffect(() => {
    let cancelled = false;
    const timer = setTimeout(async () => {
      try {
        let query = getSupabase().from("exams").select(columns, { count: "exact" });
        const term = search.trim();
        if (/^#?\d+$/.test(term)) {
          query = query.eq("id", Number(term.replace("#", "")));
        } else if (term) {
          // Treat SQL wildcard characters as literal search text.
          query = query.ilike("title", `%${term.replace(/[\\%_]/g, "\\$&")}%`);
        }
        if (status !== "all") query = query.eq("published", status === "published");
        const { data, count, error } = await query
          .order("created_at", { ascending: false }).order("id", { ascending: false })
          .range(page * pageSize, (page + 1) * pageSize - 1);
        if (error) throw error;
        if (cancelled) return;
        const rows = (data ?? []) as ExamOption[];
        setResult({ rows, count: count ?? 0, key: requestKey });
        setCache((old) => ({ ...old, ...Object.fromEntries(rows.map((exam) => [exam.id, exam])) }));
        setFailure(null);
      } catch (error) {
        if (!cancelled) setFailure({ key: requestKey, message: error instanceof Error ? error.message : "Không tải được kho đề." });
      }
    }, 250);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [search, status, page, retry, requestKey]);

  useEffect(() => {
    const ids = selectedKey.split(",").filter(Boolean).map(Number);
    if (!ids.length) return;
    let cancelled = false;
    async function loadSelected() {
      try {
        // Chunk requests so selections remain independent of the catalogue page / row limit.
        const rows: ExamOption[] = [];
        for (let start = 0; start < ids.length; start += 100) {
          const { data, error } = await getSupabase().from("exams").select(columns).in("id", ids.slice(start, start + 100));
          if (error) throw error;
          rows.push(...(data ?? []) as ExamOption[]);
        }
        if (!cancelled) {
          setCache((old) => ({ ...old, ...Object.fromEntries(rows.map((exam) => [exam.id, exam])) }));
          setSelectionError("");
        }
      } catch {
        if (!cancelled) setSelectionError("Không tải được thông tin đề đã chọn. Các mã đề vẫn được giữ nguyên.");
      }
    }
    void loadSelected();
    return () => { cancelled = true; };
  }, [selectedKey, retry]);

  const error = failure?.key === requestKey ? failure.message : null;
  const loading = result?.key !== requestKey && !error;
  const rows = result?.key === requestKey ? result.rows : [];
  const count = result?.key === requestKey ? result.count : 0;
  const pages = Math.max(1, Math.ceil(count / pageSize));
  function toggle(id: number) {
    onChange(value.includes(id) ? value.filter((item) => item !== id) : [...value, id]);
  }
  function move(index: number, direction: number) {
    const next = [...value];
    [next[index], next[index + direction]] = [next[index + direction], next[index]];
    onChange(next);
  }

  return (
    <div className="overflow-hidden rounded-xl border border-white/10 bg-white/[0.03]">
      <div className="border-b border-white/10 p-4">
        <h4 className="text-sm font-semibold text-white">Chọn đề từ kho</h4>
        <p className="mt-1 text-xs text-slate-400">Tìm đề, chọn để gắn vào bài học. Đổi trang hoặc bộ lọc vẫn giữ các đề đã chọn.</p>
        <div className="mt-3 flex flex-wrap gap-2">
          <input aria-label="Tìm đề theo tên hoặc mã" placeholder="Tìm tên đề hoặc mã, ví dụ #123…" value={search}
            onChange={(event) => { setSearch(event.target.value); setPage(0); }} className={`${control} min-w-0 flex-1 basis-56`} />
          <select aria-label="Trạng thái đề" value={status} onChange={(event) => { setStatus(event.target.value); setPage(0); }} className={control}>
            <option value="all">Tất cả trạng thái</option><option value="published">Đã xuất bản</option><option value="draft">Bản nháp</option>
          </select>
        </div>
      </div>
      <div className="grid divide-y divide-white/10 lg:grid-cols-[3fr_2fr] lg:divide-x lg:divide-y-0">
        <div className="min-w-0 p-3">
          <div aria-live="polite" className="mb-2 text-xs text-slate-400">{loading ? "Đang tìm đề…" : error ? "Không tải được danh sách" : `${count} đề · Mới nhất trước`}</div>
          {error && <div role="alert" className="p-3 text-sm text-red-300">{error} <button type="button" className={button} onClick={() => setRetry((n) => n + 1)}>Thử lại</button></div>}
          {!loading && !error && rows.length === 0 && <p className="py-8 text-center text-sm text-slate-400">Không có đề phù hợp. Thử tên khác hoặc đổi bộ lọc.</p>}
          <div className="max-h-96 space-y-2 overflow-y-auto">
            {rows.map((exam) => <label key={exam.id} className={`flex cursor-pointer items-start gap-3 rounded-lg border p-3 ${value.includes(exam.id) ? "border-emerald-400/40 bg-emerald-500/10" : "border-white/10 hover:bg-white/5"}`}>
              <input type="checkbox" checked={value.includes(exam.id)} onChange={() => toggle(exam.id)} className="mt-1 accent-emerald-500" />
              <span className="min-w-0"><span className="block break-words text-sm text-slate-100">{exam.title}</span>
                <span className="mt-1 block text-xs text-slate-400">#{exam.id} · {exam.duration_minutes} phút · {exam.published ? "Đã xuất bản" : "Bản nháp"}</span>
              </span>
            </label>)}
          </div>
          <div className="mt-3 flex items-center justify-between gap-2">
            <button type="button" disabled={page === 0} onClick={() => setPage((p) => p - 1)} className={button}>← Trước</button>
            <span className="text-xs text-slate-400">Trang {page + 1}{!loading && !error && ` / ${Math.max(page + 1, pages)}`}</span>
            <button type="button" disabled={loading || !!error || page + 1 >= pages} onClick={() => setPage((p) => p + 1)} className={button}>Sau →</button>
          </div>
        </div>
        <div className="min-w-0 bg-emerald-500/[0.03] p-3">
          <h4 className="text-sm font-semibold text-emerald-200">Đề đã chọn ({value.length})</h4>
          <p className="mt-1 text-xs text-slate-400">Sắp xếp theo thứ tự hiển thị trong bài học. Bấm Lưu mục / Thêm mục để áp dụng.</p>
          {selectionError && <p role="alert" className="mt-2 text-xs text-amber-300">{selectionError} <button type="button" className={button} onClick={() => setRetry((n) => n + 1)}>Thử lại</button></p>}
          {value.length === 0 && <p className="py-8 text-center text-sm text-slate-500">Chưa chọn đề nào.</p>}
          <ol className="mt-3 max-h-96 space-y-2 overflow-y-auto">
            {value.map((id, index) => <li key={id} className="rounded-lg border border-white/10 bg-[#0B1020] p-3">
              <p className="break-words text-sm text-slate-200">{index + 1}. {cache[id]?.title ?? `Đề #${id} (chưa tải được thông tin)`}</p>
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <span className="mr-auto text-xs text-slate-400">#{id}{cache[id] && !cache[id].published ? " · Bản nháp" : ""}</span>
                <button type="button" aria-label={`Đưa đề #${id} lên`} disabled={index === 0} onClick={() => move(index, -1)} className={button}>↑</button>
                <button type="button" aria-label={`Đưa đề #${id} xuống`} disabled={index === value.length - 1} onClick={() => move(index, 1)} className={button}>↓</button>
                <button type="button" aria-label={`Bỏ chọn đề #${id}`} onClick={() => toggle(id)} className={button}>Bỏ chọn</button>
              </div>
            </li>)}
          </ol>
        </div>
      </div>
    </div>
  );
}
