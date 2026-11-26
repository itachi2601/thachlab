"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { Dices, RotateCcw, X } from "lucide-react";
import { getSupabase } from "@/services/supabase";
import s from "./RandomCallFab.module.css";

export interface CallClass {
  id: number;
  name: string;
}

interface Student {
  id: string;
  name: string;
}

interface SessionState {
  called: string[]; // id theo thứ tự đã gọi
  absent: string[];
}

/** Một danh sách gọi được: lớp THPT (user_classes) hoặc khoá CTTC (course_enrollments). */
interface CallList {
  key: string; // "class:15" | "course:11"
  kind: "class" | "course";
  id: number;
  name: string;
  n: number | null;
}

const PICK_KEY = "goi-ten-chon"; // + ":<lessonId>" = lựa chọn riêng bài; không hậu tố = lần chọn gần nhất

function readPick(k: string): string | null {
  try {
    return window.localStorage.getItem(k);
  } catch {
    return null;
  }
}

/** Một "buổi" = danh sách + bài + ngày (giờ VN): sang ngày khác danh sách đã gọi tự làm mới. */
function storeKey(listKey: string, lessonId: number) {
  const day = new Date().toLocaleDateString("sv-SE", { timeZone: "Asia/Ho_Chi_Minh" });
  // Giữ dạng cũ "goi-ten:<classId>:..." cho lớp THPT để lượt đã gọi hôm nay không mất.
  const id = listKey.startsWith("class:") ? listKey.slice(6) : listKey;
  return `goi-ten:${id}:${lessonId}:${day}`;
}

function loadSession(key: string): SessionState {
  try {
    const raw = window.localStorage.getItem(key);
    if (raw) {
      const v = JSON.parse(raw) as Partial<SessionState>;
      return { called: Array.isArray(v.called) ? v.called : [], absent: Array.isArray(v.absent) ? v.absent : [] };
    }
  } catch {}
  return { called: [], absent: [] };
}

const EMPTY: SessionState = { called: [], absent: [] };

function randomIndex(n: number) {
  const buf = new Uint32Array(1);
  crypto.getRandomValues(buf);
  return buf[0] % n;
}

/** Tên gọi ngắn để chiếu to: "Nguyễn Văn An" → "An", kèm họ tên đầy đủ ở dòng nhỏ. */
function givenName(full: string) {
  const parts = full.trim().split(/\s+/);
  return parts[parts.length - 1] || full;
}

/**
 * Nút "Gọi tên" + phím G trên trang bài học: quay ngẫu nhiên một học sinh của lớp để trả lời câu hỏi.
 * Chỉ trang render cho giáo viên/trợ giảng. Thầy chọn danh sách (lớp THPT hoặc khoá CTTC mình dạy — RPC
 * call_roster_lists), lựa chọn nhớ theo bài. Mọi thứ chỉ tải khi mở hộp lần đầu, không thêm request lúc tải
 * trang. Em đã gọi/vắng trong buổi lưu ở localStorage của máy thầy.
 */
export default function RandomCallFab({
  lessonId,
  classes,
  defaultClassId,
}: {
  lessonId: number;
  classes: CallClass[];
  defaultClassId: number | null;
}) {
  const [open, setOpen] = useState(false);
  // Danh sách thầy gọi được: tải khi mở lần đầu; lỗi → dùng các lớp gắn với chương (props).
  const [lists, setLists] = useState<CallList[] | null>(null);
  const fallbackLists = useMemo<CallList[]>(
    () => classes.map((c) => ({ key: `class:${c.id}`, kind: "class" as const, id: c.id, name: c.name, n: null })),
    [classes],
  );
  const allLists = lists ?? fallbackLists;
  // Thứ tự chọn: chọn tay lúc này → đã chọn cho bài này → ?class= → lần chọn gần nhất → lớp đầu của chương.
  const [pickedKey, setPickedKey] = useState<string | null>(null);
  const has = (k: string | null) => !!k && allLists.some((l) => l.key === k);
  const candidates = [
    pickedKey,
    open ? readPick(`${PICK_KEY}:${lessonId}`) : null,
    defaultClassId != null ? `class:${defaultClassId}` : null,
    open ? readPick(PICK_KEY) : null,
    fallbackLists[0]?.key ?? null,
    allLists[0]?.key ?? null,
  ];
  const listKey = candidates.find((k) => has(k)) ?? null;
  const list = allLists.find((l) => l.key === listKey) ?? null;
  const [rosters, setRosters] = useState<Record<string, Student[]>>({});
  const [loadErrors, setLoadErrors] = useState<Record<string, string>>({});
  const [sessions, setSessions] = useState<Record<string, SessionState>>({});
  const [noRepeat, setNoRepeat] = useState(true);
  const [shownState, setShownState] = useState<{ key: string; student: Student } | null>(null);
  const [spinning, setSpinning] = useState(false);
  const timer = useRef<number | null>(null);

  const key = listKey ? storeKey(listKey, lessonId) : null;
  const roster = listKey ? rosters[listKey] : undefined;
  const loadError = listKey ? loadErrors[listKey] ?? null : null;
  const session: SessionState = key ? sessions[key] ?? (open ? loadSession(key) : EMPTY) : EMPTY;
  const shown = shownState && shownState.key === key ? shownState.student : null;
  const setShown = (st: Student | null) => setShownState(st && key ? { key, student: st } : null);

  // Các danh sách thầy dạy (lớp THPT + khoá CTTC) — tải một lần khi mở hộp lần đầu.
  const listsAsked = useRef(false);
  useEffect(() => {
    if (!open || listsAsked.current) return;
    listsAsked.current = true;
    getSupabase()
      .rpc("call_roster_lists")
      .then(({ data, error }) => {
        if (error || !Array.isArray(data)) return; // giữ fallback theo chương
        const chapterIds = new Set(classes.map((c) => c.id));
        const rows = (data as { kind: string; id: number; name: string; n: number }[])
          .filter((r) => (r.kind === "class" || r.kind === "course") && (r.n > 0 || (r.kind === "class" && chapterIds.has(r.id))))
          .map((r) => ({ key: `${r.kind}:${r.id}`, kind: r.kind as "class" | "course", id: r.id, name: r.name, n: r.n }));
        if (rows.length > 0) setLists(rows);
      });
  }, [open, classes]);

  // Tải học sinh của danh sách đang chọn khi cần.
  useEffect(() => {
    if (!open || !list || rosters[list.key]) return;
    let stale = false;
    const k = list.key;
    const req =
      list.kind === "course"
        ? getSupabase().rpc("course_call_roster", { p_course_id: list.id })
        : getSupabase().rpc("class_call_roster", { p_class_id: list.id });
    req.then(({ data, error }) => {
      if (stale) return;
      if (error) {
        setLoadErrors((prev) => ({ ...prev, [k]: "Chưa tải được danh sách. Thử lại sau hoặc kiểm tra quyền dạy lớp này." }));
        return;
      }
      const students = ((data ?? []) as { student_id: string; full_name: string }[]).map((r) => ({
        id: r.student_id,
        name: r.full_name,
      }));
      setRosters((prev) => ({ ...prev, [k]: students }));
    });
    return () => {
      stale = true;
    };
  }, [open, list, rosters]);

  function pickList(k: string) {
    setPickedKey(k);
    try {
      window.localStorage.setItem(`${PICK_KEY}:${lessonId}`, k);
      window.localStorage.setItem(PICK_KEY, k);
    } catch {}
  }

  const save = (next: SessionState) => {
    if (!key) return;
    setSessions((prev) => ({ ...prev, [key]: next }));
    try {
      window.localStorage.setItem(key, JSON.stringify(next));
    } catch {}
  };

  const byId = useMemo(() => new Map((roster ?? []).map((st) => [st.id, st])), [roster]);
  const present = useMemo(() => (roster ?? []).filter((st) => !session.absent.includes(st.id)), [roster, session.absent]);
  const pool = useMemo(
    () => (noRepeat ? present.filter((st) => !session.called.includes(st.id)) : present),
    [present, noRepeat, session.called],
  );

  const spin = () => {
    if (spinning || pool.length === 0) return;
    const winner = pool[randomIndex(pool.length)];
    const reduce = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    if (reduce || present.length < 2) {
      setShown(winner);
      save({ ...session, called: [...session.called.filter((x) => x !== winner.id), winner.id] });
      return;
    }
    setSpinning(true);
    // Chạy lướt tên ~1,8 giây, chậm dần rồi dừng ở em được chọn.
    let delay = 50;
    let elapsed = 0;
    const tick = () => {
      elapsed += delay;
      if (elapsed >= 1800) {
        setShown(winner);
        setSpinning(false);
        save({ ...session, called: [...session.called.filter((x) => x !== winner.id), winner.id] });
        return;
      }
      setShown(present[randomIndex(present.length)]);
      delay = Math.min(delay * 1.12, 260);
      timer.current = window.setTimeout(tick, delay);
    };
    tick();
  };

  useEffect(() => () => {
    if (timer.current) window.clearTimeout(timer.current);
  }, []);

  // Phím G mở; trong hộp: Space/Enter quay, Esc đóng.
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.tagName === "SELECT" || t.isContentEditable)) return;
      if (!open) {
        if (e.key === "g" || e.key === "G") {
          e.preventDefault();
          e.stopPropagation();
          setOpen(true);
        }
        return;
      }
      if (e.key === "Escape") {
        e.preventDefault();
        e.stopPropagation();
        setOpen(false);
      } else if (e.key === " " || e.key === "Enter") {
        if (t && t.tagName === "BUTTON" && e.key === "Enter") return;
        e.preventDefault();
        e.stopPropagation();
        spin();
      }
    }
    window.addEventListener("keydown", onKey, true);
    return () => window.removeEventListener("keydown", onKey, true);
  }, [open, spin]);

  function toggleAbsent(id: string) {
    const absent = session.absent.includes(id) ? session.absent.filter((x) => x !== id) : [...session.absent, id];
    save({ ...session, absent });
    if (shown?.id === id && !session.absent.includes(id)) setShown(null);
  }

  function markShownAbsent() {
    if (!shown) return;
    save({
      called: session.called.filter((x) => x !== shown.id),
      absent: session.absent.includes(shown.id) ? session.absent : [...session.absent, shown.id],
    });
    setShown(null);
  }

  function resetSession() {
    save({ called: [], absent: session.absent });
    setShown(null);
  }

  const calledList = session.called.map((id) => byId.get(id)).filter((x): x is Student => !!x);
  const exhausted = roster && roster.length > 0 && pool.length === 0;

  return (
    <>
      {!open && (
        <div className={s.float}>
          <button type="button" className={s.fab} onClick={() => setOpen(true)} title="Quay số gọi một em trả lời (G)">
            <Dices size={16} aria-hidden />
            <span>Gọi tên</span>
          </button>
        </div>
      )}
      {open && (
        <div className={s.overlay} role="dialog" aria-modal="true" aria-label="Gọi tên ngẫu nhiên">
          <div className={s.panel}>
            <header className={s.head}>
              <h2>Gọi tên ngẫu nhiên</h2>
              {allLists.length > 1 ? (
                <select
                  className={s.select}
                  value={listKey ?? ""}
                  onChange={(e) => pickList(e.target.value)}
                  aria-label="Chọn danh sách để gọi"
                >
                  {(["course", "class"] as const).map((kind) => {
                    const group = allLists.filter((l) => l.kind === kind);
                    if (group.length === 0) return null;
                    return (
                      <optgroup key={kind} label={kind === "course" ? "Khoá CTTC" : "Lớp THPT"}>
                        {group.map((l) => (
                          <option key={l.key} value={l.key}>
                            {l.name}
                            {l.n != null ? ` (${l.n})` : ""}
                          </option>
                        ))}
                      </optgroup>
                    );
                  })}
                </select>
              ) : list ? (
                <span className={s.className}>{list.name}</span>
              ) : null}
              <button type="button" className={s.close} onClick={() => setOpen(false)} aria-label="Đóng (Esc)">
                <X size={22} aria-hidden />
              </button>
            </header>

            <div className={s.stage} aria-live="polite">
              {loadError ? (
                <p className={s.hint}>{loadError}</p>
              ) : !list ? (
                <p className={s.hint}>Chưa có danh sách nào thầy được gọi.</p>
              ) : !roster ? (
                <p className={s.hint}>Đang tải danh sách…</p>
              ) : roster.length === 0 ? (
                <p className={s.hint}>Danh sách này chưa có học sinh đang học.</p>
              ) : shown ? (
                <div className={`${s.result} ${spinning ? s.rolling : s.landed}`} key={spinning ? "roll" : shown.id}>
                  <strong>{givenName(shown.name)}</strong>
                  <span>{shown.name}</span>
                </div>
              ) : exhausted ? (
                <p className={s.hint}>Đã gọi hết các em có mặt. Bấm “Buổi mới” để gọi lại từ đầu.</p>
              ) : (
                <p className={s.hint}>Bấm Quay (hoặc phím cách) để chọn một em.</p>
              )}
            </div>

            <div className={s.actions}>
              <button type="button" className={s.spin} onClick={spin} disabled={spinning || pool.length === 0}>
                <Dices size={22} aria-hidden /> {spinning ? "Đang quay…" : shown ? "Quay em khác" : "Quay"}
              </button>
              {shown && !spinning && (
                <button type="button" className={s.ghost} onClick={markShownAbsent} title="Em này vắng — bỏ khỏi lượt quay">
                  Em này vắng
                </button>
              )}
            </div>

            {roster && roster.length > 0 && (
              <>
                <div className={s.meta}>
                  <label className={s.toggle}>
                    <input type="checkbox" checked={noRepeat} onChange={(e) => setNoRepeat(e.target.checked)} />
                    Không gọi lại em đã gọi trong buổi
                  </label>
                  <span>
                    Còn {pool.length}/{present.length} em · vắng {session.absent.length}
                  </span>
                </div>

                {calledList.length > 0 && (
                  <section className={s.called}>
                    <h3>
                      Đã gọi ({calledList.length})
                      <button type="button" onClick={resetSession} className={s.reset}>
                        <RotateCcw size={14} aria-hidden /> Buổi mới
                      </button>
                    </h3>
                    <ol>
                      {calledList.map((st) => (
                        <li key={st.id}>{st.name}</li>
                      ))}
                    </ol>
                  </section>
                )}

                <details className={s.roster}>
                  <summary>Danh sách lớp ({roster.length}) — chạm tên để đánh dấu vắng</summary>
                  <ul>
                    {roster.map((st) => {
                      const absent = session.absent.includes(st.id);
                      return (
                        <li key={st.id}>
                          <button
                            type="button"
                            className={absent ? s.absent : undefined}
                            aria-pressed={absent}
                            onClick={() => toggleAbsent(st.id)}
                          >
                            {st.name}
                            {absent && <em> · vắng</em>}
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                </details>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
}
