"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ArrowLeft, ArrowRight, Check, RotateCcw } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { useAuth } from "@/components/auth/AuthProvider";
import { supabaseConfigured, getSupabase } from "@/services/supabase";
import { fetchChaptersStatic, fetchClassesStatic, fetchLessonsStatic } from "@/services/static-content";
import { fetchMyProgressMarks } from "@/services/lessons";
import { fetchChapterMastery, MASTERY_ICON, MASTERY_LABEL, type MasteryLevel } from "@/services/mastery";
import { ON_TAP_THEO_BAI } from "@/content/on-tap";
import type { Chapter } from "@/features/lessons/types";
import type { SchoolClass } from "@/features/exams/types";
import {
  NUT_MO_TA,
  NUT_NHAN,
  demXong,
  dungBanDo,
  nutTiepTheo,
  type BaiTrenDuong,
  type MucGon,
  type TheBai,
} from "@/features/lo-trinh/ban-do";
import s from "./lo-trinh.module.css";

/**
 * Lộ trình kiểu Duolingo — GĐ1 (docs/LO-TRINH-KIEU-DUOLINGO.md, bản thử 26/11/2026): bản đồ một chương, chỉ đọc
 * dữ liệu sẵn có (lesson_progress, exam_results, get_chapter_mastery, on_tap_trang_thai). Không bảng mới, không
 * RP/huy hiệu trên trang (L3), một nút nổi duy nhất "Học tiếp" (L5, N7), không chuyển động (G2).
 */

type TrangThai = { slug: string; the_id: string; han_on: string };

function BanDo({ chapterId }: { chapterId: number }) {
  const { session, loading } = useAuth();
  const [chuong, setChuong] = useState<Chapter | null>(null);
  const [bai, setBai] = useState<BaiTrenDuong[] | null>(null);
  const [loi, setLoi] = useState<string | null>(null);

  useEffect(() => {
    if (loading) return;
    let huy = false;
    void (async () => {
      try {
        const [chapters, allLessons] = await Promise.all([fetchChaptersStatic(), fetchLessonsStatic()]);
        const ch = chapters.find((c) => c.id === chapterId) ?? null;
        const lessons = allLessons
          .filter(
            (l) => l.chapter_id === chapterId && (l.lesson_kind === "bai_hoc" || l.lesson_kind === "kiem_tra_chuong"),
          )
          .sort((a, b) => a.sort_order - b.sort_order || a.id - b.id);
        if (!ch || lessons.length === 0) {
          if (!huy) setLoi("Không tìm thấy chương này.");
          return;
        }
        const ids = lessons.map((l) => l.id);
        const userId = session?.user.id;
        const sb = getSupabase();
        const coThe = lessons.filter((l) => ON_TAP_THEO_BAI[l.id]?.so_the);

        const [itemsRes, dau, mastery, trangThai] = await Promise.all([
          sb
            .from("lesson_items")
            .select("id, lesson_id, kind, exam_ids")
            .in("lesson_id", ids)
            .not("published_at", "is", null),
          userId ? fetchMyProgressMarks(userId).catch(() => null) : Promise.resolve(null),
          userId
            ? fetchChapterMastery(chapterId).catch(() => new Map<number, MasteryLevel>())
            : Promise.resolve(new Map<number, MasteryLevel>()),
          userId
            ? Promise.all(
                coThe.map((l) =>
                  sb
                    .rpc("on_tap_trang_thai", { p_slug: ON_TAP_THEO_BAI[l.id].slug })
                    .then(({ data, error }) => (error ? null : ((data ?? []) as TrangThai[]))),
                ),
              )
            : Promise.resolve(null),
        ]);

        const now = Date.now();
        const the = new Map<number, TheBai>();
        coThe.forEach((l, i) => {
          const rows = trangThai?.[i] ?? null;
          the.set(l.id, {
            coThe: true,
            daOn: rows ? rows.length > 0 : null,
            denHan: rows ? rows.filter((r) => new Date(r.han_on).getTime() <= now).length : 0,
          });
        });
        const items = ((itemsRes.data ?? []) as MucGon[]).map((m) => ({ ...m, exam_ids: m.exam_ids ?? [] }));
        if (huy) return;
        setChuong(ch);
        setBai(dungBanDo({ lessons, items, dau, the, mastery }));
      } catch {
        if (!huy) setLoi("Chưa tải được lộ trình. Em thử lại sau ít phút.");
      }
    })();
    return () => {
      huy = true;
    };
  }, [chapterId, session, loading]);

  if (loi) return <p className={s.trong}>{loi}</p>;
  if (!bai || !chuong) return <p className={s.trong}>Đang tải lộ trình…</p>;

  const tiep = nutTiepTheo(bai);
  const { xong, tong } = demXong(bai);
  const denHan = bai.reduce((n, b) => n + b.denHan, 0);
  const tiepKey = tiep ? `${tiep.bai.id}-${tiep.nut.loai}` : "";

  return (
    <>
      <header className={s.dau}>
        <Link href="/lop-hoc/lo-trinh" className={s.quayLai}>
          <ArrowLeft size={16} aria-hidden /> Các chương
        </Link>
        <h1 className={s.tieuDe}>{chuong.title}</h1>
        {session && tong > 0 && (
          <p className={s.tienDo}>
            {xong}/{tong} bước
          </p>
        )}
      </header>

      {tiep ? (
        <Link href={tiep.nut.href} className={s.hocTiep}>
          <span>
            <span className={s.hocTiepNhan}>Học tiếp</span>
            <span className={s.hocTiepTen}>
              {tiep.bai.so ? `Bài ${tiep.bai.so} · ` : ""}
              {NUT_NHAN[tiep.nut.loai]}: {NUT_MO_TA[tiep.nut.loai].toLowerCase()}
            </span>
          </span>
          <ArrowRight size={22} aria-hidden />
        </Link>
      ) : tong > 0 ? (
        <p className={s.xongChuong}>Em đã đi hết các bước của chương này.</p>
      ) : !session ? (
        <Link
          href={`/dang-nhap?next=${encodeURIComponent(`/lop-hoc/lo-trinh?chuong=${chapterId}`)}`}
          className={s.hocTiep}
        >
          <span>
            <span className={s.hocTiepNhan}>Đăng nhập để đi lộ trình</span>
            <span className={s.hocTiepTen}>Lộ trình nhớ em đã đi tới bước nào</span>
          </span>
          <ArrowRight size={22} aria-hidden />
        </Link>
      ) : null}

      {denHan > 0 && (
        <Link href="/lop-hoc/on-the" className={s.onDenHan}>
          <RotateCcw size={18} aria-hidden /> Ôn {denHan} thẻ đến hạn (3–5 phút)
        </Link>
      )}

      <ol className={s.duong}>
        {bai.map((b) => (
          <li key={b.id} className={s.bai}>
            <div className={s.baiDau}>
              <span className={s.baiSo}>{b.so ?? "•"}</span>
              <span className={s.baiTen}>{b.ten}</span>
              {b.mastery && b.mastery !== "insufficient" && (
                <span className={s.mastery} title={MASTERY_LABEL[b.mastery]} aria-label={MASTERY_LABEL[b.mastery]}>
                  {MASTERY_ICON[b.mastery]}
                </span>
              )}
            </div>
            {b.nut.length > 0 ? (
              <ol className={s.hangNut}>
                {b.nut.map((n) => {
                  const hienTai = `${b.id}-${n.loai}` === tiepKey;
                  const cls = [s.nut, n.xong ? s.nutXong : "", hienTai ? s.nutHienTai : ""].join(" ");
                  return (
                    <li key={n.loai}>
                      <Link
                        href={n.href}
                        className={cls}
                        aria-current={hienTai ? "step" : undefined}
                        aria-label={`${NUT_NHAN[n.loai]}${n.xong ? " (đã xong)" : ""}: ${NUT_MO_TA[n.loai]}`}
                      >
                        <span className={s.tron}>{n.xong ? <Check size={20} aria-hidden /> : null}</span>
                        <span className={s.nutNhan}>{NUT_NHAN[n.loai]}</span>
                      </Link>
                    </li>
                  );
                })}
              </ol>
            ) : (
              <Link href={`/lop-hoc/bai?id=${b.id}`} className={s.moBai}>
                Mở bài
              </Link>
            )}
            {b.denHan > 0 && <p className={s.baiDenHan}>{b.denHan} thẻ đến hạn ôn</p>}
          </li>
        ))}
      </ol>
    </>
  );
}

/** Không có ?chuong=: danh sách chương có bộ thẻ ôn (lớp 10–12), gom theo lớp. */
function DanhSachChuong() {
  const [nhom, setNhom] = useState<{ lop: SchoolClass; chuong: Chapter[] }[] | null>(null);
  useEffect(() => {
    void (async () => {
      const [classes, chapters, lessons] = await Promise.all([
        fetchClassesStatic(),
        fetchChaptersStatic(),
        fetchLessonsStatic(),
      ]);
      const coThe = new Set(lessons.filter((l) => ON_TAP_THEO_BAI[l.id]?.so_the).map((l) => l.chapter_id));
      const out = classes
        .filter((c) => c.active)
        .sort((a, b) => a.sort_order - b.sort_order)
        .map((lop) => ({
          lop,
          chuong: chapters
            .filter((c) => coThe.has(c.id) && c.classIds.includes(lop.id))
            .sort((a, b) => a.sort_order - b.sort_order),
        }))
        .filter((g) => g.chuong.length > 0);
      setNhom(out);
    })();
  }, []);

  if (!nhom) return <p className={s.trong}>Đang tải…</p>;
  return (
    <>
      <header className={s.dau}>
        <h1 className={s.tieuDe}>Lộ trình tự học</h1>
        <p className={s.tienDo}>Mỗi bài 5 bước ngắn: Hiểu → Nhớ → Mẫu → Luyện → Chốt.</p>
      </header>
      {nhom.map((g) => (
        <section key={g.lop.id} className={s.nhomLop}>
          <h2 className={s.tenLop}>{/^\d+$/.test(g.lop.name) ? `Lớp ${g.lop.name}` : g.lop.name}</h2>
          <ul className={s.dsChuong}>
            {g.chuong.map((c) => (
              <li key={c.id}>
                <Link href={`/lop-hoc/lo-trinh?chuong=${c.id}`} className={s.dongChuong}>
                  <span>{c.title}</span>
                  <ArrowRight size={18} aria-hidden />
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </>
  );
}

function LoTrinh() {
  const sp = useSearchParams();
  const id = Number(sp.get("chuong"));
  if (!supabaseConfigured) return <p className={s.trong}>Hệ thống đang được cấu hình.</p>;
  return Number.isInteger(id) && id > 0 ? <BanDo chapterId={id} /> : <DanhSachChuong />;
}

export default function LoTrinhPage() {
  return (
    <>
      <Navbar />
      <main className={`${s.khung} mx-auto min-h-screen w-full max-w-xl px-4 pt-24 pb-28 sm:px-5 sm:pt-28`}>
        <Suspense fallback={<p className={s.trong}>Đang tải…</p>}>
          <LoTrinh />
        </Suspense>
      </main>
      <Footer variant="app" />
    </>
  );
}
