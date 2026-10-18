"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { BookOpen, ClipboardList, CornerDownLeft, GraduationCap, Search, type LucideIcon } from "lucide-react";
import { AREA_ITEMS, OVERVIEW_ITEM, SHARED_ITEMS } from "@/components/admin/nav";
import { getSupabase, supabaseConfigured } from "@/services/supabase";

interface Hit {
  key: string;
  group: "Trang" | "Học sinh" | "Đề" | "Bài học";
  title: string;
  sub?: string;
  href: string;
  icon: LucideIcon;
}

const NAV_HITS: Hit[] = [OVERVIEW_ITEM, ...AREA_ITEMS.thpt, ...AREA_ITEMS.cttc, ...SHARED_ITEMS].map((item) => ({
  key: `nav:${item.href}`,
  group: "Trang",
  title: item.label,
  sub: item.desc,
  href: item.href,
  icon: item.icon,
}));

/** Bỏ dấu + chữ thường để gõ "hoc sinh" vẫn ra "Học sinh". */
function fold(text: string): string {
  return text.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toLowerCase();
}

/** Ký tự có nghĩa trong bộ lọc PostgREST/ilike — bỏ đi để chuỗi gõ vào không thành cú pháp. */
function safe(text: string): string {
  return text.replace(/[%_,()\\*]/g, " ").trim();
}

/** Tìm chung khu quản trị: Ctrl/Cmd+K hoặc phím "/" — trang, học sinh, đề (gõ số = mã đề), bài học. */
export default function AdminSearch() {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [remote, setRemote] = useState<Hit[]>([]);
  const [busy, setBusy] = useState(false);
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const reqId = useRef(0);

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      const target = event.target as HTMLElement | null;
      const typing = !!target && (target.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName));
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setOpen(true);
      } else if (event.key === "/" && !typing && !event.metaKey && !event.ctrlKey) {
        event.preventDefault();
        setOpen(true);
      } else if (event.key === "Escape") {
        setOpen(false);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  useEffect(() => {
    if (open) {
      setQuery("");
      setRemote([]);
      setActive(0);
      requestAnimationFrame(() => inputRef.current?.focus());
    }
  }, [open]);

  // Truy vấn DB sau 250ms ngừng gõ; bỏ kết quả của lần gõ cũ nếu đã gõ tiếp.
  useEffect(() => {
    const q = safe(query);
    if (!open || q.length < 2 || !supabaseConfigured) {
      setRemote([]);
      setBusy(false);
      return;
    }
    const id = ++reqId.current;
    setBusy(true);
    const timer = setTimeout(async () => {
      const sb = getSupabase();
      const like = `%${q}%`;
      const asId = /^#?\d{1,9}$/.test(q) ? Number(q.replace("#", "")) : null;
      // "bài 7 lớp 12": tách "lớp N" làm bộ lọc lớp, các từ còn lại đều phải có trong tên bài.
      const gradeMatch = q.match(/l[ớo]p\s*(\d{1,2})/i);
      const grade = gradeMatch?.[1] ?? null;
      const words = q.replace(/l[ớo]p\s*\d{1,2}/i, " ").replace(/^#/, "").split(/\s+/).filter(Boolean);
      let lessonQuery = sb
        .from("lessons")
        .select("id, title, published, chapters(title, chapter_classes(classes(name)))")
        .order("id", { ascending: false })
        .limit(grade ? 40 : 6);
      for (const w of words) lessonQuery = lessonQuery.ilike("title", `%${w}%`);
      const [students, examsByTitle, examById, lessons] = await Promise.all([
        sb.from("profiles").select("id, full_name, class_name, student_code").eq("role", "student").or(`full_name.ilike.${like},student_code.ilike.${like}`).limit(6),
        sb.from("exams").select("id, title, published").ilike("title", like).order("id", { ascending: false }).limit(6),
        asId ? sb.from("exams").select("id, title, published").eq("id", asId) : Promise.resolve({ data: [], error: null }),
        words.length ? lessonQuery : Promise.resolve({ data: [], error: null }),
      ]);
      if (id !== reqId.current) return;
      const hits: Hit[] = [];
      for (const row of examById.data ?? []) hits.push(examHit(row as ExamRow));
      for (const row of students.data ?? []) {
        const s = row as { id: string; full_name: string | null; class_name: string | null; student_code: string | null };
        hits.push({
          key: `hs:${s.id}`,
          group: "Học sinh",
          title: s.full_name || "(chưa có tên)",
          sub: [s.class_name, s.student_code].filter(Boolean).join(" · ") || undefined,
          href: `/quan-tri/hoc-sinh?student=${s.id}`,
          icon: GraduationCap,
        });
      }
      for (const row of examsByTitle.data ?? []) {
        if (!hits.some((h) => h.key === `de:${(row as ExamRow).id}`)) hits.push(examHit(row as ExamRow));
      }
      type LessonRow = {
        id: number;
        title: string;
        published: boolean;
        chapters: { title: string; chapter_classes: { classes: { name: string } | null }[] } | null;
      };
      let lessonRows = (lessons.data ?? []) as unknown as LessonRow[];
      if (grade) {
        lessonRows = lessonRows
          .filter((l) => l.chapters?.chapter_classes.some((cc) => cc.classes?.name.includes(grade)))
          .slice(0, 6);
      }
      for (const l of lessonRows) {
        const where = [
          l.chapters?.chapter_classes.map((cc) => cc.classes?.name).filter(Boolean).join(", "),
          l.chapters?.title,
        ]
          .filter(Boolean)
          .join(" · ");
        hits.push({
          key: `bai:${l.id}`,
          group: "Bài học",
          title: l.title,
          sub: [where, l.published ? "" : "Đang ẩn"].filter(Boolean).join(" · ") || undefined,
          href: `/quan-tri/bai-hoc?lesson=${l.id}`,
          icon: BookOpen,
        });
      }
      // Gom theo nhóm (đề trùng mã đứng đầu) để mỗi nhóm chỉ có một tiêu đề.
      const rank = { "Đề": 0, "Học sinh": 1, "Bài học": 2, Trang: 3 } as const;
      setRemote(hits.sort((a, b) => rank[a.group] - rank[b.group]));
      setBusy(false);
    }, 250);
    return () => clearTimeout(timer);
  }, [query, open]);

  const results = useMemo(() => {
    const q = fold(query.trim());
    const pages = q ? NAV_HITS.filter((h) => fold(`${h.title} ${h.sub ?? ""}`).includes(q)).slice(0, 5) : NAV_HITS.slice(0, 6);
    return [...remote, ...pages];
  }, [query, remote]);

  useEffect(() => setActive(0), [results.length]);

  function go(hit: Hit) {
    setOpen(false);
    router.push(hit.href);
  }

  function onInputKey(event: React.KeyboardEvent) {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      setActive((i) => Math.min(results.length - 1, i + 1));
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      setActive((i) => Math.max(0, i - 1));
    } else if (event.key === "Enter" && results[active]) {
      event.preventDefault();
      go(results[active]);
    }
  }

  return (
    <>
      <button type="button" className="admin-burger" style={{ width: "auto", padding: "0 12px", gap: 8 }} onClick={() => setOpen(true)} aria-label="Tìm kiếm (Ctrl+K)">
        <Search size={16} />
        <span className="hidden text-xs font-semibold sm:inline">Tìm… <kbd className="ml-1 rounded border border-white/15 px-1 text-[10px]">⌘K</kbd></span>
      </button>

      {open && (
        <div className="fixed inset-0 z-[60] flex items-start justify-center bg-black/60 p-4 pt-[12vh]" onClick={() => setOpen(false)}>
          <div role="dialog" aria-modal="true" aria-label="Tìm kiếm" className="w-full max-w-xl overflow-hidden rounded-2xl border border-white/10 bg-panel shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center gap-3 border-b border-white/10 px-4">
              <Search size={17} className="shrink-0 text-slate-500" />
              <input
                ref={inputRef}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={onInputKey}
                placeholder="Tên học sinh, mã đề (#978), bài 7 lớp 12, tên trang…"
                className="h-14 w-full bg-transparent text-sm text-white placeholder:text-slate-500 focus:outline-none"
              />
              {busy && <span className="h-3 w-3 shrink-0 animate-spin rounded-full border-2 border-slate-500 border-t-transparent" aria-label="Đang tìm" />}
            </div>
            <ul className="max-h-[50vh] overflow-y-auto p-2" role="listbox">
              {results.length === 0 && <li className="p-6 text-center text-sm text-slate-500">Không có kết quả.</li>}
              {results.map((hit, i) => {
                const Icon = hit.icon;
                const showGroup = i === 0 || results[i - 1].group !== hit.group;
                return (
                  <li key={hit.key} role="option" aria-selected={i === active}>
                    {showGroup && <p className="px-3 pb-1 pt-2 text-[11px] font-bold uppercase tracking-wide text-slate-500">{hit.group}</p>}
                    <button
                      type="button"
                      onMouseEnter={() => setActive(i)}
                      onClick={() => go(hit)}
                      className={`flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left ${i === active ? "bg-white/10" : ""}`}
                    >
                      <Icon size={16} className="shrink-0 text-slate-400" />
                      <span className="min-w-0 flex-1">
                        <span className="block truncate text-sm font-semibold text-white">{hit.title}</span>
                        {hit.sub && <span className="block truncate text-xs text-slate-500">{hit.sub}</span>}
                      </span>
                      {i === active && <CornerDownLeft size={14} className="shrink-0 text-slate-500" />}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        </div>
      )}
    </>
  );
}

interface ExamRow {
  id: number;
  title: string;
  published: boolean;
}

function examHit(row: ExamRow): Hit {
  return {
    key: `de:${row.id}`,
    group: "Đề",
    title: `#${row.id} · ${row.title}`,
    sub: row.published ? undefined : "Đang ẩn",
    href: `/quan-tri/sua-de?exam=${row.id}`,
    icon: ClipboardList,
  };
}
