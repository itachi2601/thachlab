"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Award, CalendarRange, ListChecks, Medal, RefreshCw, Users } from "lucide-react";
import ClassPicker from "@/components/admin/ClassPicker";
import ExamPicker from "@/components/admin/ExamPicker";
import ConfirmDialog from "@/components/ui/ConfirmDialog";
import { useToast } from "@/components/ui/Toast";
import RankBadge from "@/components/rank/RankBadge";
import type { SchoolClass } from "@/features/exams/types";
import {
  GROUP_LABELS,
  LEDGER_KIND_LABELS,
  formatRp,
  tierLabel,
  type RankLedgerEntry,
  type TitleGroup,
  type TitleLevel,
} from "@/features/rank/types";
import { fetchQuestionTopics, lessonTopics, type QuestionTopic } from "@/services/analytics";
import { fetchClasses } from "@/services/classes";
import {
  adjustRp,
  closeSeason,
  createSeason,
  fetchLedgerOf,
  fetchSeasonOverview,
  fetchSeasons,
  fetchSourceCandidates,
  fetchSources,
  fetchTiers,
  fetchTitleRows,
  fetchTitleTopicMap,
  recomputeSeason,
  recomputeStudent,
  setTitleTopics,
  updateSeason,
  updateTier,
  updateTitleRow,
  upsertSources,
  type RankSeason,
  type RankSourceRow,
  type RankTierRow,
  type RankTitleRow,
  type SeasonOverviewRow,
  type SourceCandidate,
} from "@/services/rank";

type Tab = "seasons" | "tiers" | "sources" | "titles" | "students";

const TABS: { id: Tab; label: string; icon: typeof Award }[] = [
  { id: "seasons", label: "Mùa", icon: CalendarRange },
  { id: "tiers", label: "Bậc & điều kiện", icon: Award },
  { id: "sources", label: "Bài tính RP", icon: ListChecks },
  { id: "titles", label: "Danh hiệu", icon: Medal },
  { id: "students", label: "Học sinh", icon: Users },
];

const inputCls = "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const selectCls = `${inputCls} bg-panel`;
const numCls = `${inputCls} w-24`;

const CONFIG_FIELDS: { key: string; label: string; def: number }[] = [
  { key: "practice_max_rp", label: "RP tối đa / bài luyện tập (mặc định khi bật bài)", def: 20 },
  { key: "fix_max_rp", label: "RP tối đa sửa sai / bài", def: 10 },
  { key: "weekly_goal_rp", label: "RP mục tiêu tuần", def: 30 },
  { key: "weekly_goal_count", label: "Số bài cần đạt trong tuần", def: 3 },
  { key: "weekly_goal_min_score", label: "Điểm tối thiểu (thang 10) để tính bài tuần", def: 7 },
  { key: "fix_pass_pct", label: "% đạt bài sửa sai", def: 80 },
  { key: "fix_min_pool", label: "Số câu tương đương tối thiểu trong ngân hàng", def: 5 },
  { key: "fix_quiz_count", label: "Số câu mỗi bài sửa sai", def: 10 },
];

function errMsg(e: unknown, fallback: string) {
  return e instanceof Error ? e.message : fallback;
}

export default function RankAdmin() {
  const toast = useToast();
  const [tab, setTab] = useState<Tab>("seasons");
  const [seasons, setSeasons] = useState<RankSeason[] | null>(null);
  const [seasonId, setSeasonId] = useState<number | null>(null);
  const [classes, setClasses] = useState<SchoolClass[]>([]);

  const reloadSeasons = useCallback(
    () =>
      fetchSeasons().then((list) => {
        setSeasons(list);
        setSeasonId((cur) => (cur && list.some((s) => s.id === cur) ? cur : (list.find((s) => s.status === "active") ?? list[0])?.id ?? null));
      }),
    [],
  );

  useEffect(() => {
    reloadSeasons().catch((e) => toast("error", errMsg(e, "Không tải được danh sách mùa")));
    fetchClasses(true).then(setClasses).catch(() => undefined);
  }, [reloadSeasons, toast]);

  const season = seasons?.find((s) => s.id === seasonId) ?? null;
  const classNames = (ids: number[]) => (ids.length === 0 ? "Mọi lớp THPT" : ids.map((id) => classes.find((c) => c.id === id)?.name ?? `#${id}`).join(", "));

  return (
    <div className="admin-stack">
      <div className="admin-toolbar">
        <div className="flex flex-wrap gap-1.5">
          {TABS.map((t) => {
            const Icon = t.icon;
            return (
              <button key={t.id} type="button" onClick={() => setTab(t.id)} className={`admin-chip ${tab === t.id ? "bg-primary text-white" : ""}`}>
                <Icon size={14} className="mr-1 inline" />
                {t.label}
              </button>
            );
          })}
        </div>
        {seasons && seasons.length > 0 && (
          <label className="admin-label ml-auto flex items-center gap-2">
            Mùa
            <select className={selectCls} value={seasonId ?? ""} onChange={(e) => setSeasonId(Number(e.target.value) || null)}>
              {seasons.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} · {s.status === "active" ? "đang mở" : s.status === "draft" ? "nháp" : "đã đóng"}
                </option>
              ))}
            </select>
          </label>
        )}
      </div>

      {tab === "seasons" && <SeasonsTab seasons={seasons} season={season} classNames={classNames} onChanged={reloadSeasons} />}
      {tab === "tiers" && (season ? <TiersTab season={season} /> : <NoSeason />)}
      {tab === "sources" && (season ? <SourcesTab season={season} /> : <NoSeason />)}
      {tab === "titles" && <TitlesTab />}
      {tab === "students" && (season ? <StudentsTab season={season} /> : <NoSeason />)}
    </div>
  );
}

function NoSeason() {
  return <p className="admin-empty">Chưa có mùa nào — tạo mùa ở tab “Mùa” trước.</p>;
}

// ============================================================
// Mùa
// ============================================================
function SeasonsTab({
  seasons,
  season,
  classNames,
  onChanged,
}: {
  seasons: RankSeason[] | null;
  season: RankSeason | null;
  classNames: (ids: number[]) => string;
  onChanged: () => Promise<void>;
}) {
  const toast = useToast();
  const [name, setName] = useState("");
  const [startsOn, setStartsOn] = useState("");
  const [endsOn, setEndsOn] = useState("");
  const [classIds, setClassIds] = useState<number[]>([]);
  const [activate, setActivate] = useState(false);
  const [busy, setBusy] = useState(false);
  const [confirm, setConfirm] = useState<{ kind: "close" | "recompute"; id: number } | null>(null);

  async function create() {
    if (!name.trim() || !startsOn || !endsOn) {
      toast("error", "Cần tên mùa, ngày bắt đầu và kết thúc");
      return;
    }
    setBusy(true);
    try {
      await createSeason({ name: name.trim(), startsOn, endsOn, classIds, activate });
      toast("success", "Đã tạo mùa" + (activate ? " và mở ngay" : ""));
      setName("");
      setStartsOn("");
      setEndsOn("");
      setClassIds([]);
      setActivate(false);
      await onChanged();
    } catch (e) {
      toast("error", errMsg(e, "Không tạo được mùa"));
    } finally {
      setBusy(false);
    }
  }

  async function setStatus(id: number, status: RankSeason["status"]) {
    setBusy(true);
    try {
      if (status === "closed") {
        const n = await closeSeason(id);
        toast("success", `Đã đóng mùa — lưu kết quả ${n} học sinh`);
      } else {
        await updateSeason(id, { status });
        toast("success", status === "active" ? "Đã mở mùa" : "Đã chuyển về nháp");
      }
      await onChanged();
    } catch (e) {
      toast("error", errMsg(e, "Không đổi được trạng thái"));
    } finally {
      setBusy(false);
    }
  }

  async function recompute(id: number) {
    setBusy(true);
    try {
      const n = await recomputeSeason(id);
      toast("success", `Đã tính lại cho ${n} học sinh`);
    } catch (e) {
      toast("error", errMsg(e, "Không tính lại được"));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="admin-stack">
      <section className="admin-card">
        <h2 className="admin-h2">Tạo mùa mới</h2>
        <p className="admin-lead">Mỗi mùa 6–8 tuần. RP tính riêng từng mùa; danh hiệu chuyên môn giữ qua các mùa. Một lớp chỉ có một mùa đang mở tại một thời điểm.</p>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <input className={inputCls} placeholder="Tên mùa (VD: Mùa 1 · HK1 2026–2027)" value={name} onChange={(e) => setName(e.target.value)} />
          <input className={inputCls} type="date" value={startsOn} onChange={(e) => setStartsOn(e.target.value)} />
          <input className={inputCls} type="date" value={endsOn} onChange={(e) => setEndsOn(e.target.value)} />
        </div>
        <div className="mt-4">
          <ClassPicker selected={classIds} onChange={setClassIds} />
        </div>
        <label className="mt-3 flex items-center gap-2 text-sm text-slate-300">
          <input type="checkbox" checked={activate} onChange={(e) => setActivate(e.target.checked)} /> Mở ngay sau khi tạo
        </label>
        <button type="button" className="admin-btn admin-btn--primary mt-4" disabled={busy} onClick={create}>
          Tạo mùa
        </button>
      </section>

      <section className="admin-card">
        <h2 className="admin-h2">Các mùa</h2>
        {!seasons ? (
          <p className="admin-muted">Đang tải…</p>
        ) : seasons.length === 0 ? (
          <p className="admin-empty">Chưa có mùa nào.</p>
        ) : (
          <ul className="mt-3 space-y-2">
            {seasons.map((s) => (
              <li key={s.id} className="flex flex-wrap items-center gap-3 rounded-xl border border-white/10 p-3">
                <span className={`admin-badge ${s.status === "active" ? "admin-badge--ok" : s.status === "closed" ? "" : "admin-badge--warn"}`}>
                  {s.status === "active" ? "Đang mở" : s.status === "closed" ? "Đã đóng" : "Nháp"}
                </span>
                <span className="min-w-0 flex-1">
                  <b className="text-white">{s.name}</b>
                  <span className="block text-xs text-slate-500">
                    {new Date(s.starts_on).toLocaleDateString("vi-VN")} – {new Date(s.ends_on).toLocaleDateString("vi-VN")} · {classNames(s.class_ids)}
                  </span>
                </span>
                {s.status === "draft" && (
                  <button type="button" className="admin-btn admin-btn--sm admin-btn--primary" disabled={busy} onClick={() => setStatus(s.id, "active")}>
                    Mở mùa
                  </button>
                )}
                {s.status === "active" && (
                  <>
                    <button type="button" className="admin-btn admin-btn--sm admin-btn--ghost" disabled={busy} onClick={() => setConfirm({ kind: "recompute", id: s.id })}>
                      <RefreshCw size={13} className="mr-1 inline" />
                      Tính lại
                    </button>
                    <button type="button" className="admin-btn admin-btn--sm admin-btn--danger" disabled={busy} onClick={() => setConfirm({ kind: "close", id: s.id })}>
                      Đóng mùa
                    </button>
                  </>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>

      {season && season.status !== "closed" && <SeasonConfigForm key={season.id} season={season} onSaved={onChanged} />}

      <ConfirmDialog
        open={confirm !== null}
        title={confirm?.kind === "close" ? "Đóng mùa này?" : "Tính lại RP cả mùa?"}
        description={
          confirm?.kind === "close"
            ? "Lưu bậc và RP cuối cùng của mọi học sinh. Lịch sử và danh hiệu giữ nguyên. Không hoàn tác được."
            : "Quét lại mọi bài trong khung mùa theo đúng luật hiện tại; chỉ cộng phần còn thiếu, không cộng trùng. Dùng khi vừa bật thêm bài hoặc có học sinh vào lớp muộn."
        }
        confirmLabel={confirm?.kind === "close" ? "Đóng mùa" : "Tính lại"}
        onCancel={() => setConfirm(null)}
        onConfirm={() => {
          const c = confirm;
          setConfirm(null);
          if (!c) return;
          if (c.kind === "close") setStatus(c.id, "closed");
          else recompute(c.id);
        }}
      />
    </div>
  );
}

// Remount theo key={season.id} để state khởi tạo từ props, không cần đồng bộ trong effect.
function SeasonConfigForm({ season, onSaved }: { season: RankSeason; onSaved: () => Promise<void> }) {
  const toast = useToast();
  const [busy, setBusy] = useState(false);
  const [config, setConfig] = useState<Record<string, string>>(() => {
    const next: Record<string, string> = {};
    for (const f of CONFIG_FIELDS) next[f.key] = String(season.config?.[f.key] ?? f.def);
    return next;
  });
  const [bossExam, setBossExam] = useState<number[]>(season.boss_exam_id ? [season.boss_exam_id] : []);
  const [bossPass, setBossPass] = useState(String(season.boss_pass_score ?? 8));

  async function saveConfig() {
    setBusy(true);
    try {
      const cfg: Record<string, number> = {};
      for (const f of CONFIG_FIELDS) {
        const v = Number(config[f.key]);
        if (!Number.isFinite(v) || v < 0) throw new Error(`Giá trị không hợp lệ: ${f.label}`);
        cfg[f.key] = v;
      }
      await updateSeason(season.id, {
        config: cfg,
        boss_exam_id: bossExam[0] ?? null,
        boss_pass_score: Number(bossPass) || null,
      });
      toast("success", "Đã lưu cấu hình mùa");
      await onSaved();
    } catch (e) {
      toast("error", errMsg(e, "Không lưu được"));
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="admin-card">
      <h2 className="admin-h2">Cấu hình mùa “{season.name}”</h2>
      <div className="mt-3 grid gap-3 sm:grid-cols-2">
        {CONFIG_FIELDS.map((f) => (
          <label key={f.key} className="admin-label flex items-center justify-between gap-3">
            <span>{f.label}</span>
            <input className={numCls} type="number" min={0} value={config[f.key] ?? ""} onChange={(e) => setConfig((c) => ({ ...c, [f.key]: e.target.value }))} />
          </label>
        ))}
      </div>
      <div className="mt-5">
        <p className="admin-label mb-2">Đề “Trùm Cuối” của mùa (tuỳ chọn) — điểm đạt thang 10:</p>
        <div className="flex items-center gap-3">
          <input className={numCls} type="number" min={0} max={10} step={0.5} value={bossPass} onChange={(e) => setBossPass(e.target.value)} />
          <span className="text-xs text-slate-500">{bossExam[0] ? `Đề #${bossExam[0]}` : "Chưa chọn đề"}</span>
        </div>
        <div className="mt-2">
          <ExamPicker value={bossExam} onChange={(ids) => setBossExam(ids.length ? [ids[ids.length - 1]] : [])} />
        </div>
      </div>
      <button type="button" className="admin-btn admin-btn--primary mt-4" disabled={busy} onClick={saveConfig}>
        Lưu cấu hình
      </button>
    </section>
  );
}

// ============================================================
// Bậc & điều kiện
// ============================================================
function TiersTab({ season }: { season: RankSeason }) {
  const toast = useToast();
  const [tiers, setTiers] = useState<RankTierRow[] | null>(null);
  const [draft, setDraft] = useState<Record<string, Partial<RankTierRow>>>({});
  const [busy, setBusy] = useState<string | null>(null);

  const load = useCallback(() => {
    fetchTiers(season.id).then(setTiers).catch((e) => toast("error", errMsg(e, "Không tải được bậc")));
  }, [season.id, toast]);
  useEffect(load, [load]);

  function val<K extends keyof RankTierRow>(t: RankTierRow, k: K): RankTierRow[K] {
    return (draft[t.code]?.[k] as RankTierRow[K] | undefined) ?? t[k];
  }
  function set(code: string, patch: Partial<RankTierRow>) {
    setDraft((d) => ({ ...d, [code]: { ...d[code], ...patch } }));
  }

  async function save(t: RankTierRow) {
    const patch = draft[t.code];
    if (!patch) return;
    setBusy(t.code);
    try {
      await updateTier(season.id, t.code, patch);
      toast("success", `Đã lưu bậc ${t.name}`);
      setDraft((d) => {
        const n = { ...d };
        delete n[t.code];
        return n;
      });
      load();
    } catch (e) {
      toast("error", errMsg(e, "Không lưu được"));
    } finally {
      setBusy(null);
    }
  }

  const readOnly = season.status === "closed";

  return (
    <section className="admin-card">
      <h2 className="admin-h2">Ngưỡng RP và điều kiện lên hạng</h2>
      <p className="admin-lead">
        Phân bậc III → II → I tự chia đều trong dải RP của bậc (không hở, không chồng). Từ Nhật Hoa trở lên cần danh hiệu chuyên môn; Thiên Thể và Chí Tôn bắt buộc có đề thử thách — chưa gán thì học sinh không thể lên bậc đó.
      </p>
      {!tiers ? (
        <p className="admin-muted">Đang tải…</p>
      ) : (
        <div className="mt-4 space-y-3">
          {tiers.map((t) => {
            const chal = val(t, "challenge_exam_id");
            return (
              <div key={t.code} className="rounded-xl border border-white/10 p-3">
                <div className="flex flex-wrap items-center gap-3">
                  <RankBadge code={t.code} size={32} />
                  <b className="w-28 text-white">{t.name}</b>
                  <label className="admin-label flex items-center gap-2">
                    Từ RP
                    <input className={numCls} type="number" min={0} disabled={readOnly} value={val(t, "min_rp")} onChange={(e) => set(t.code, { min_rp: Number(e.target.value) })} />
                  </label>
                  <label className="admin-label flex items-center gap-2">
                    Cần
                    <input className="w-16 rounded-xl border border-white/10 bg-white/5 px-2 py-2 text-sm text-white" type="number" min={0} disabled={readOnly} value={val(t, "required_title_count")} onChange={(e) => set(t.code, { required_title_count: Number(e.target.value) })} />
                    danh hiệu mức
                    <select className={selectCls} disabled={readOnly} value={val(t, "required_title_level") ?? "thuc_tinh"} onChange={(e) => set(t.code, { required_title_level: e.target.value as TitleLevel })}>
                      <option value="thuc_tinh">Thức Tỉnh</option>
                      <option value="lam_chu">Làm Chủ</option>
                      <option value="huyen_thoai">Huyền Thoại</option>
                    </select>
                  </label>
                  <label className="admin-label flex items-center gap-2">
                    Đề thử thách {chal ? `#${chal}` : "(chưa gán)"} · đạt từ
                    <input className="w-16 rounded-xl border border-white/10 bg-white/5 px-2 py-2 text-sm text-white" type="number" min={0} max={10} step={0.5} disabled={readOnly} value={val(t, "challenge_pass_score") ?? 8} onChange={(e) => set(t.code, { challenge_pass_score: Number(e.target.value) })} />
                    /10
                  </label>
                  {chal && !readOnly && (
                    <button type="button" className="admin-btn admin-btn--sm admin-btn--ghost" onClick={() => set(t.code, { challenge_exam_id: null })}>
                      Bỏ đề
                    </button>
                  )}
                  {!readOnly && (
                    <button type="button" className="admin-btn admin-btn--sm admin-btn--primary ml-auto" disabled={!draft[t.code] || busy === t.code} onClick={() => save(t)}>
                      Lưu
                    </button>
                  )}
                </div>
                {!readOnly && (
                  <details className="mt-2">
                    <summary className="cursor-pointer text-xs text-slate-400">Chọn đề thử thách cho {t.name}</summary>
                    <div className="mt-2">
                      <ExamPicker value={chal ? [chal] : []} onChange={(ids) => set(t.code, { challenge_exam_id: ids.length ? ids[ids.length - 1] : null })} />
                    </div>
                  </details>
                )}
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}

// ============================================================
// Bài tính RP
// ============================================================
function SourcesTab({ season }: { season: RankSeason }) {
  const toast = useToast();
  const [candidates, setCandidates] = useState<SourceCandidate[] | null>(null);
  const [rows, setRows] = useState<Map<string, RankSourceRow>>(new Map());
  const [dirty, setDirty] = useState<Set<string>>(new Set());
  const [busy, setBusy] = useState(false);
  const defMax = Number(season.config?.practice_max_rp ?? 20);

  useEffect(() => {
    Promise.all([fetchSourceCandidates(), fetchSources(season.id)])
      .then(([cands, srcs]) => {
        setCandidates(cands);
        setRows(new Map(srcs.map((s) => [`${s.source_kind}:${s.source_id}`, s])));
        setDirty(new Set());
      })
      .catch((e) => toast("error", errMsg(e, "Không tải được danh sách bài")));
  }, [season.id, toast]);

  const visible = useMemo(() => {
    if (!candidates) return [];
    if (season.class_ids.length === 0) return candidates;
    return candidates.filter((c) => c.classIds.length === 0 || c.classIds.some((id) => season.class_ids.includes(id)));
  }, [candidates, season.class_ids]);

  const grouped = useMemo(() => {
    const byChapter = new Map<number, { title: string; lessons: Map<number, { title: string; items: SourceCandidate[] }> }>();
    for (const c of visible) {
      const ch = byChapter.get(c.chapterId) ?? { title: c.chapterTitle, lessons: new Map() };
      const ls = ch.lessons.get(c.lessonId) ?? { title: c.lessonTitle, items: [] };
      ls.items.push(c);
      ch.lessons.set(c.lessonId, ls);
      byChapter.set(c.chapterId, ch);
    }
    return byChapter;
  }, [visible]);

  function key(c: SourceCandidate) {
    return `${c.kind}:${c.id}`;
  }
  function rowOf(c: SourceCandidate): RankSourceRow {
    return rows.get(key(c)) ?? { season_id: season.id, source_kind: c.kind, source_id: c.id, max_rp: defMax, enabled: false };
  }
  function setRow(c: SourceCandidate, patch: Partial<RankSourceRow>) {
    const k = key(c);
    setRows((m) => new Map(m).set(k, { ...rowOf(c), ...patch }));
    setDirty((d) => new Set(d).add(k));
  }
  function bulk(kind: SourceCandidate["itemKind"], enabled: boolean) {
    for (const c of visible) if (c.itemKind === kind) setRow(c, { enabled });
  }

  async function save() {
    setBusy(true);
    try {
      const changed = Array.from(dirty).map((k) => rows.get(k)!).filter(Boolean);
      await upsertSources(changed);
      toast("success", `Đã lưu ${changed.length} bài`);
      setDirty(new Set());
    } catch (e) {
      toast("error", errMsg(e, "Không lưu được"));
    } finally {
      setBusy(false);
    }
  }

  const enabledCount = visible.filter((c) => rowOf(c).enabled).length;
  const readOnly = season.status === "closed";

  return (
    <section className="admin-card">
      <div className="flex flex-wrap items-center gap-2">
        <h2 className="admin-h2">Bài được tính RP</h2>
        <span className="admin-muted ml-auto text-xs">{enabledCount}/{visible.length} bài đang bật</span>
      </div>
      <p className="admin-lead">Chỉ bài được bật mới cộng RP (tối đa theo cột RP, theo kết quả tốt nhất). Sửa sai chỉ áp dụng cho BTVN / kiểm tra (có kết quả từng câu).</p>
      {!readOnly && (
        <div className="mt-3 flex flex-wrap gap-2">
          <button type="button" className="admin-chip" onClick={() => bulk("luyen_tap", true)}>Bật mọi luyện tập</button>
          <button type="button" className="admin-chip" onClick={() => bulk("bai_tap_ve_nha", true)}>Bật mọi BTVN</button>
          <button type="button" className="admin-chip" onClick={() => bulk("kiem_tra", true)}>Bật mọi kiểm tra</button>
          <button type="button" className="admin-chip" onClick={() => { bulk("luyen_tap", false); bulk("bai_tap_ve_nha", false); bulk("kiem_tra", false); }}>Tắt tất cả</button>
          <button type="button" className="admin-btn admin-btn--sm admin-btn--primary ml-auto" disabled={dirty.size === 0 || busy} onClick={save}>
            Lưu ({dirty.size})
          </button>
        </div>
      )}
      {!candidates ? (
        <p className="admin-muted mt-3">Đang tải…</p>
      ) : grouped.size === 0 ? (
        <p className="admin-empty mt-3">Không có bài nào cho lớp của mùa này.</p>
      ) : (
        <div className="mt-4 space-y-4">
          {Array.from(grouped.entries()).map(([chId, ch]) => (
            <details key={chId} className="rounded-xl border border-white/10 p-3" open>
              <summary className="cursor-pointer font-semibold text-white">{ch.title}</summary>
              <div className="mt-2 space-y-3">
                {Array.from(ch.lessons.entries()).map(([lsId, ls]) => (
                  <div key={lsId}>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{ls.title}</p>
                    <ul className="mt-1 space-y-1">
                      {ls.items.map((c) => {
                        const r = rowOf(c);
                        return (
                          <li key={key(c)} className="flex flex-wrap items-center gap-3 rounded-lg px-2 py-1 hover:bg-white/5">
                            <label className="flex min-w-0 flex-1 items-center gap-2 text-sm text-slate-200">
                              <input type="checkbox" disabled={readOnly} checked={r.enabled} onChange={(e) => setRow(c, { enabled: e.target.checked })} />
                              <span className="truncate">{c.title}</span>
                              <span className="admin-badge">{c.itemKind === "luyen_tap" ? "Luyện tập" : c.itemKind === "bai_tap_ve_nha" ? "BTVN" : "Kiểm tra"}</span>
                            </label>
                            <label className="admin-label flex items-center gap-1 text-xs">
                              RP
                              <input className="w-16 rounded-lg border border-white/10 bg-white/5 px-2 py-1 text-sm text-white" type="number" min={0} max={200} disabled={readOnly} value={r.max_rp} onChange={(e) => setRow(c, { max_rp: Number(e.target.value) })} />
                            </label>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                ))}
              </div>
            </details>
          ))}
        </div>
      )}
    </section>
  );
}

// ============================================================
// Danh hiệu
// ============================================================
function TitlesTab() {
  const toast = useToast();
  const [titles, setTitles] = useState<RankTitleRow[] | null>(null);
  const [topicMap, setTopicMap] = useState<Map<string, number[]>>(new Map());
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [open, setOpen] = useState<string | null>(null);
  const [draft, setDraft] = useState<Record<string, Partial<RankTitleRow> & { topicIds?: number[] }>>({});
  const [busy, setBusy] = useState<string | null>(null);

  const load = useCallback(() => {
    Promise.all([fetchTitleRows(), fetchTitleTopicMap(), fetchQuestionTopics()])
      .then(([t, m, q]) => {
        setTitles(t);
        setTopicMap(m);
        setTopics(lessonTopics(q));
      })
      .catch((e) => toast("error", errMsg(e, "Không tải được danh hiệu")));
  }, [toast]);
  useEffect(load, [load]);

  const topicsByGrade = useMemo(() => {
    const m = new Map<string, QuestionTopic[]>();
    for (const t of topics) m.set(t.grade, [...(m.get(t.grade) ?? []), t]);
    return Array.from(m.entries()).sort(([a], [b]) => Number(a) - Number(b));
  }, [topics]);

  function val<K extends keyof RankTitleRow>(t: RankTitleRow, k: K): RankTitleRow[K] {
    return (draft[t.code]?.[k] as RankTitleRow[K] | undefined) ?? t[k];
  }
  function topicIdsOf(t: RankTitleRow): number[] {
    return draft[t.code]?.topicIds ?? topicMap.get(t.code) ?? [];
  }
  function set(code: string, patch: Partial<RankTitleRow> & { topicIds?: number[] }) {
    setDraft((d) => ({ ...d, [code]: { ...d[code], ...patch } }));
  }

  async function save(t: RankTitleRow) {
    const d = draft[t.code];
    if (!d) return;
    setBusy(t.code);
    try {
      const { topicIds, ...patch } = d;
      if (Object.keys(patch).length) await updateTitleRow(t.code, patch);
      if (topicIds) await setTitleTopics(t.code, topicIds);
      toast("success", `Đã lưu ${t.name}`);
      setDraft((x) => {
        const n = { ...x };
        delete n[t.code];
        return n;
      });
      load();
    } catch (e) {
      toast("error", errMsg(e, "Không lưu được"));
    } finally {
      setBusy(null);
    }
  }

  async function toggleEnabled(t: RankTitleRow, enabled: boolean) {
    try {
      await updateTitleRow(t.code, { enabled });
      setTitles((list) => list?.map((x) => (x.code === t.code ? { ...x, enabled } : x)) ?? null);
    } catch (e) {
      toast("error", errMsg(e, "Không đổi được"));
    }
  }

  const groups: TitleGroup[] = ["co_hoc", "dao_dong_song", "dien_tu", "nhiet_hoc", "hien_dai", "bo_suu_tap", "thanh_tich"];

  return (
    <div className="admin-stack">
      <section className="admin-card">
        <h2 className="admin-h2">Danh hiệu chuyên môn</h2>
        <p className="admin-lead">
          Mỗi danh hiệu gắn với các chủ đề tầng bài. Thức Tỉnh: đủ số câu tối thiểu, chạm ≥ ½ chủ đề, đúng ≥ ngưỡng. Làm Chủ: gấp đôi số câu, đủ mọi chủ đề, đúng ≥ ngưỡng cao hơn. Huyền Thoại: Làm Chủ + đề thử thách. Danh hiệu chưa gắn chủ đề sẽ không active.
        </p>
        {!titles ? (
          <p className="admin-muted">Đang tải…</p>
        ) : (
          groups.map((g) => {
            const list = titles.filter((t) => t.group_code === g);
            if (list.length === 0) return null;
            return (
              <div key={g} className="mt-4">
                <h3 className="admin-h3">{GROUP_LABELS[g]}</h3>
                <ul className="mt-2 space-y-2">
                  {list.map((t) => {
                    const ids = topicIdsOf(t);
                    const isOpen = open === t.code;
                    const specialist = t.kind === "specialist";
                    return (
                      <li key={t.code} className={`rounded-xl border p-3 ${t.enabled ? "border-white/10" : "border-white/5 opacity-60"}`}>
                        <div className="flex flex-wrap items-center gap-3">
                          <label className="flex items-center gap-2">
                            <input type="checkbox" checked={t.enabled} onChange={(e) => toggleEnabled(t, e.target.checked)} />
                          </label>
                          <span className="min-w-0 flex-1">
                            <b className="text-white">{t.name}</b>
                            <span className="ml-2 text-xs text-slate-500">{t.description}</span>
                            {specialist && (
                              <span className={`ml-2 admin-badge ${ids.length ? "admin-badge--ok" : "admin-badge--warn"}`}>
                                {ids.length ? `${ids.length} chủ đề` : "chưa gắn chủ đề"}
                              </span>
                            )}
                          </span>
                          {specialist && (
                            <button type="button" className="admin-btn admin-btn--sm admin-btn--ghost" onClick={() => setOpen(isOpen ? null : t.code)}>
                              {isOpen ? "Thu gọn" : "Chỉnh"}
                            </button>
                          )}
                        </div>
                        {specialist && isOpen && (
                          <div className="mt-3 space-y-3 border-t border-white/5 pt-3">
                            <div className="grid gap-3 sm:grid-cols-4">
                              <label className="admin-label">Số câu tối thiểu<input className={`${numCls} mt-1 block`} type="number" min={1} value={val(t, "min_questions")} onChange={(e) => set(t.code, { min_questions: Number(e.target.value) })} /></label>
                              <label className="admin-label">% Thức Tỉnh<input className={`${numCls} mt-1 block`} type="number" min={0} max={100} value={val(t, "awaken_accuracy")} onChange={(e) => set(t.code, { awaken_accuracy: Number(e.target.value) })} /></label>
                              <label className="admin-label">% Làm Chủ<input className={`${numCls} mt-1 block`} type="number" min={0} max={100} value={val(t, "master_accuracy")} onChange={(e) => set(t.code, { master_accuracy: Number(e.target.value) })} /></label>
                              <label className="admin-label">% đề Huyền Thoại<input className={`${numCls} mt-1 block`} type="number" min={0} max={100} value={val(t, "legend_accuracy")} onChange={(e) => set(t.code, { legend_accuracy: Number(e.target.value) })} /></label>
                            </div>
                            <div>
                              <p className="admin-label mb-1">Chủ đề (tầng bài):</p>
                              {topicsByGrade.map(([grade, list2]) => (
                                <div key={grade} className="mb-2">
                                  <p className="text-[11px] font-semibold uppercase tracking-wide text-slate-500">Lớp {grade}</p>
                                  <div className="mt-1 flex flex-wrap gap-1.5">
                                    {list2.map((q) => {
                                      const on = ids.includes(q.id);
                                      return (
                                        <button key={q.id} type="button" className={`admin-chip ${on ? "bg-primary text-white" : ""}`} onClick={() => set(t.code, { topicIds: on ? ids.filter((x) => x !== q.id) : [...ids, q.id] })}>
                                          {q.name}
                                        </button>
                                      );
                                    })}
                                  </div>
                                </div>
                              ))}
                            </div>
                            <details>
                              <summary className="cursor-pointer text-xs text-slate-400">
                                Đề thử thách Huyền Thoại {val(t, "legend_challenge_exam_id") ? `· #${val(t, "legend_challenge_exam_id")}` : "· chưa gán"}
                              </summary>
                              <div className="mt-2">
                                <ExamPicker value={val(t, "legend_challenge_exam_id") ? [val(t, "legend_challenge_exam_id")!] : []} onChange={(x) => set(t.code, { legend_challenge_exam_id: x.length ? x[x.length - 1] : null })} />
                              </div>
                            </details>
                            <button type="button" className="admin-btn admin-btn--sm admin-btn--primary" disabled={!draft[t.code] || busy === t.code} onClick={() => save(t)}>
                              Lưu
                            </button>
                          </div>
                        )}
                      </li>
                    );
                  })}
                </ul>
              </div>
            );
          })
        )}
      </section>
    </div>
  );
}

// ============================================================
// Học sinh
// ============================================================
function StudentsTab({ season }: { season: RankSeason }) {
  const toast = useToast();
  const [rows, setRows] = useState<SeasonOverviewRow[] | null>(null);
  const [selected, setSelected] = useState<SeasonOverviewRow | null>(null);
  const [ledger, setLedger] = useState<RankLedgerEntry[]>([]);
  const [delta, setDelta] = useState("");
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [search, setSearch] = useState("");

  const load = useCallback(() => {
    fetchSeasonOverview(season.id).then(setRows).catch((e) => toast("error", errMsg(e, "Không tải được")));
  }, [season.id, toast]);
  useEffect(load, [load]);

  useEffect(() => {
    if (!selected) return;
    fetchLedgerOf(selected.student_id, season.id, 100).then(setLedger).catch(() => setLedger([]));
  }, [selected, season.id]);

  async function submitAdjust() {
    if (!selected) return;
    const d = Number(delta);
    if (!Number.isInteger(d) || d === 0) {
      toast("error", "Nhập số RP nguyên khác 0 (âm để trừ)");
      return;
    }
    if (!reason.trim()) {
      toast("error", "Cần ghi lý do — lý do hiện trong lịch sử của học sinh");
      return;
    }
    setBusy(true);
    try {
      await adjustRp(season.id, selected.student_id, d, reason.trim());
      toast("success", `Đã ${d > 0 ? "cộng" : "trừ"} ${Math.abs(d)} RP`);
      setDelta("");
      setReason("");
      load();
      fetchLedgerOf(selected.student_id, season.id, 100).then(setLedger).catch(() => undefined);
    } catch (e) {
      toast("error", errMsg(e, "Không điều chỉnh được"));
    } finally {
      setBusy(false);
    }
  }

  async function recompute() {
    if (!selected) return;
    setBusy(true);
    try {
      await recomputeStudent(season.id, selected.student_id);
      toast("success", "Đã tính lại cho học sinh này");
      load();
      fetchLedgerOf(selected.student_id, season.id, 100).then(setLedger).catch(() => undefined);
    } catch (e) {
      toast("error", errMsg(e, "Không tính lại được"));
    } finally {
      setBusy(false);
    }
  }

  const filtered = (rows ?? []).filter((r) => !search || r.full_name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="admin-grid">
      <section className="admin-card">
        <div className="flex flex-wrap items-center gap-2">
          <h2 className="admin-h2">Học sinh · {season.name}</h2>
          <input className={`${inputCls} ml-auto`} placeholder="Tìm tên…" value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>
        {!rows ? (
          <p className="admin-muted mt-3">Đang tải…</p>
        ) : (
          <div className="admin-table-wrap mt-3">
            <table className="w-full text-sm">
              <thead className="text-left text-xs uppercase tracking-wide text-slate-500">
                <tr>
                  <th className="py-2">Học sinh</th>
                  <th>Bậc</th>
                  <th className="text-right">RP</th>
                  <th className="text-right">Danh hiệu</th>
                  <th>Ghi chú</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((r) => (
                  <tr key={r.student_id} className={`cursor-pointer border-t border-white/5 hover:bg-white/5 ${selected?.student_id === r.student_id ? "bg-white/5" : ""}`} onClick={() => setSelected(r)}>
                    <td className="py-2">
                      <b className="text-white">{r.full_name}</b>
                      <span className="block text-xs text-slate-500">{r.class_names}</span>
                    </td>
                    <td>
                      <span className="inline-flex items-center gap-1.5">
                        <RankBadge code={r.tier_code} division={r.division} size={22} />
                        {tierLabel(r.tier_code, r.division)}
                      </span>
                    </td>
                    <td className="text-right text-white">{formatRp(r.rp)}</td>
                    <td className="text-right">{r.titles_count}</td>
                    <td className="text-xs text-amber-300">{r.pending_gate ? `Đủ RP lên ${r.pending_gate}, thiếu điều kiện` : ""}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="admin-card">
        {!selected ? (
          <p className="admin-empty">Chọn một học sinh để xem lịch sử RP và điều chỉnh.</p>
        ) : (
          <>
            <h2 className="admin-h2">{selected.full_name}</h2>
            <p className="admin-muted text-xs">
              {tierLabel(selected.tier_code, selected.division)} · {formatRp(selected.rp)} RP · {selected.titles_count} danh hiệu
            </p>
            {season.status === "active" && (
              <div className="mt-3 rounded-xl border border-white/10 p-3">
                <p className="admin-label mb-2">Điều chỉnh RP (ghi lý do — hiện trong lịch sử của học sinh)</p>
                <div className="flex flex-wrap gap-2">
                  <input className={numCls} type="number" placeholder="±RP" value={delta} onChange={(e) => setDelta(e.target.value)} />
                  <input className={`${inputCls} min-w-0 flex-1`} placeholder="Lý do" value={reason} onChange={(e) => setReason(e.target.value)} />
                  <button type="button" className="admin-btn admin-btn--sm admin-btn--primary" disabled={busy} onClick={submitAdjust}>Ghi</button>
                  <button type="button" className="admin-btn admin-btn--sm admin-btn--ghost" disabled={busy} onClick={recompute}>
                    <RefreshCw size={13} className="mr-1 inline" />Tính lại
                  </button>
                </div>
              </div>
            )}
            <h3 className="admin-h3 mt-4">Lịch sử RP</h3>
            {ledger.length === 0 ? (
              <p className="admin-muted text-xs">Chưa có dòng nào.</p>
            ) : (
              <ul className="mt-2 max-h-[28rem] divide-y divide-white/5 overflow-y-auto">
                {ledger.map((l) => (
                  <li key={l.id} className="flex gap-3 py-2 text-sm">
                    <span className={`w-12 shrink-0 text-right font-semibold ${l.amount >= 0 ? "text-emerald-300" : "text-red-300"}`}>{l.amount >= 0 ? "+" : ""}{l.amount}</span>
                    <span className="min-w-0 flex-1">
                      <span className="block text-slate-200">{l.reason || LEDGER_KIND_LABELS[l.source_kind]}</span>
                      <span className="text-xs text-slate-500">
                        {LEDGER_KIND_LABELS[l.source_kind]}{l.actor_name ? ` · ${l.actor_name}` : ""} · {new Date(l.created_at).toLocaleString("vi-VN")}
                      </span>
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </>
        )}
      </section>
    </div>
  );
}
