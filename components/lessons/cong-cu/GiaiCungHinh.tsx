"use client";

import { useEffect, useRef, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import StepwiseSolution from "@/components/lessons/StepwiseSolution";
import DoThi from "@/components/lessons/cong-cu/DoThi";
import GiaoThoaHaiNguon from "@/components/lessons/cong-cu/GiaoThoaHaiNguon";
import ThanhNangLuong from "@/components/lessons/cong-cu/ThanhNangLuong";
import TuTruong from "@/components/lessons/cong-cu/TuTruong";
import SongDay from "@/components/lessons/cong-cu/SongDay";
import VanGiaoThoa from "@/components/lessons/cong-cu/VanGiaoThoa";
import VongTronPha from "@/components/lessons/cong-cu/VongTronPha";
import SoDoVecto from "@/components/lessons/cong-cu/SoDoVecto";
import DienTruongDeu from "@/components/lessons/cong-cu/DienTruongDeu";
import MachDien from "@/components/lessons/cong-cu/MachDien";
import { getTomDe, TomDeBar, TomDeSide, useStickyTop } from "@/components/lessons/TomDe";
import type { LessonWorkedQuestion, WorkedTool } from "@/features/lessons/types";

/**
 * Giải từng bước CÙNG hình (thầy góp ý 2/11/2026): trên điện thoại hình dính nửa trên màn hình, em làm từng bước ở
 * nửa dưới — làm bước nào thấy ngay hình của bước đó, không phải cuộn qua lại (N8 split-attention, Chandler & Sweller).
 * Mỗi lần chỉ một bước (N5); lời giải đầy đủ gập ở dưới cùng. Hình của bước chỉ vẽ khi em đã làm xong bước đó.
 * Mọi bước có câu hỏi đều tự làm (fading giau_het, thầy chốt 2/11 sau góp ý học sinh ảo: "4/6 bước chỉ đọc đáp số").
 */

function Hinh({ tool, layer }: { tool: WorkedTool; layer: number }) {
  if (tool.loai === "giao_thoa_2_nguon") return <GiaoThoaHaiNguon {...tool} layer={layer} />;
  if (tool.loai === "vong_tron") return <VongTronPha {...tool} layer={layer} />;
  if (tool.loai === "song_day") return <SongDay {...tool} layer={layer} />;
  if (tool.loai === "van_giao_thoa") return <VanGiaoThoa {...tool} layer={layer} />;
  if (tool.loai === "do_thi") return <DoThi {...tool} layer={layer} />;
  if (tool.loai === "tu_truong") return <TuTruong {...tool} layer={layer} />;
  if (tool.loai === "thanh_nang_luong") return <ThanhNangLuong {...tool} layer={layer} />;
  if (tool.loai === "so_do_vecto" || tool.loai === "thanh_moment") return <SoDoVecto {...tool} layer={layer} />;
  if (tool.loai === "dien_truong_deu") return <DienTruongDeu {...tool} layer={layer} />;
  if (tool.loai === "mach_dien") return <MachDien {...tool} layer={layer} />;
  return null;
}

export default function GiaiCungHinh({
  q,
  tool,
  color,
  jump,
  onAllOpen,
}: {
  q: LessonWorkedQuestion;
  tool: WorkedTool;
  color: string;
  jump: { idx: number; n: number } | null;
  onAllOpen: () => void;
}) {
  const n = q.buoc?.length ?? 0;
  const [step, setStep] = useState(0);
  // bước em đã mở xem (bước tự mở vì không có câu hỏi thì chưa chắc đã xem) — để dòng nhắc không nói "xem lại" bước chưa xem (HS ảo 3/11)
  const [seen, setSeen] = useState<number[]>([0]);
  const visit = (i: number) => {
    setStep(i);
    setSeen((s) => (s.includes(i) ? s : [...s, i]));
  };
  const [opened, setOpened] = useState(0); // số bước đầu đã làm xong liên tiếp
  const [full, setFull] = useState(false);
  const [deOpen, setDeOpen] = useState(false); // tóm đề mở đè lên (điện thoại)
  const top = useStickyTop();
  const splitRef = useRef<HTMLDivElement>(null);

  // gỡ rối từ bài tương tự: nhảy về đúng bước
  const [seenJump, setSeenJump] = useState(jump);
  if (jump !== seenJump) {
    setSeenJump(jump);
    if (jump) visit(Math.min(Math.max(jump.idx, 0), n - 1));
  }

  // đưa hình về đúng chỗ (đỉnh khung ngay dưới thanh dính) để bước hiện ngay dưới hình, không bị hình che
  const align = () => {
    const dy = (splitRef.current?.getBoundingClientRect().top ?? top) - top;
    if (Math.abs(dy) > 4) window.scrollTo({ top: window.scrollY + dy, behavior: "instant" });
  };
  // gỡ rối: StepwiseSolution không tự cuộn khi có `only` (scrollIntoView center đặt tiêu đề bước dưới hình dính — HS ảo 3/11);
  // cuộn ở đây sau khi bước đã vẽ, để đỉnh bước nằm ngay dưới hình
  useEffect(() => {
    if (!jump) return;
    const t = setTimeout(align, 60);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jump]);
  const go = (i: number) => {
    visit(i);
    setDeOpen(false);
    align();
  };

  // Vừa trả lời đúng bước đang làm: lời giải ngắn của bước hiện ở đầu khung bước. Nếu lúc gõ trang đã cuộn (bàn phím
  // điện thoại đẩy ô nhập lên) thì phần đó nằm dưới hình dính → cuộn về cho thấy (HS ảo 2/11: "lời giải bị đẩy khỏi tầm mắt").
  // `opened` có thể nhảy nhiều bước một lúc (các bước sau không có câu hỏi, vd "Hướng của gia tốc", "Kiểm tra") — HS ảo 3/11:
  // điều kiện `opened === step + 1` bỏ qua ca này nên lời giải bước nằm khuất dưới hình. Chỉ cần bước đang xem vừa được mở.
  const prevOpened = useRef(opened);
  useEffect(() => {
    const was = prevOpened.current;
    prevOpened.current = opened;
    if (opened <= was || step < was || step >= opened) return;
    const el = document.activeElement;
    if (el instanceof HTMLElement && splitRef.current?.contains(el)) el.blur(); // đóng bàn phím trước khi đo
    const fix = () => {
      const stick = splitRef.current?.querySelector(".cc-sticky")?.getBoundingClientRect().bottom ?? 0;
      const stepsTop = splitRef.current?.querySelector(".cc-steps")?.getBoundingClientRect().top ?? stick;
      if (stepsTop < stick - 4) align();
    };
    const t = setTimeout(fix, 60), t2 = setTimeout(fix, 450); // lần 2: sau khi bàn phím đóng, khung nhìn đổi cỡ
    return () => {
      clearTimeout(t);
      clearTimeout(t2);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [opened]);
  const layer = Math.min(opened, step + 1);
  const tomDe = getTomDe(q);
  const canNext = step + 1 < n && step + 1 <= opened;
  const title = q.buoc?.[step]?.tieu_de ?? "";
  // một dòng cố định dưới nút: nói vì sao ▶ khoá / đã mở / đã xong (L1 phản hồi, D2 nút không nhảy chỗ)
  const hint =
    step + 1 >= n
      ? opened >= n
        ? "✓ Xong cả bài — tự trình bày lại, rồi so với lời giải đầy đủ ở cuối."
        : "Trả lời bước này để hoàn thành."
      : canNext
        ? step + 1 === opened
          ? "Xong bước này — bấm ▶ sang bước tiếp."
          : seen.includes(step + 1)
            ? "Bấm ▶ xem lại bước sau."
            : `Bấm ▶ xem bước ${step + 2}.`
        : "Trả lời câu hỏi bên dưới để mở bước sau.";

  return (
    <div ref={splitRef} className="cc-split">
      <div className={full ? "cc-sticky cc-sticky--off" : "cc-sticky"} style={{ top }}>
        {/* Tóm đề (thử 3/11): một dòng "Tìm" ở ĐẦU khối dính (thầy 3/11: để dưới nút thì bị thanh điều hướng đáy che) — số liệu "Cho" đã nằm trên hình (N4); chạm thì đè lên, trang không xô (D2, N8) */}
        {tomDe && <TomDeBar tomDe={tomDe} problemHtml={q.problem_html} open={deOpen} setOpen={setDeOpen} />}
        <Hinh tool={tool} layer={layer} />
        <div className="cc-stepper">
          <button type="button" aria-label="Bước trước" disabled={step <= 0} onClick={() => go(step - 1)}>
            ◀
          </button>
          <span className="cc-step-title">
            Bước {step + 1}/{n} · <ContentHtml html={title} className="inline" />
          </span>
          <button
            type="button"
            aria-label="Bước sau"
            disabled={!canNext}
            className={canNext && step + 1 === opened ? "cc-next-ready" : undefined}
            style={canNext ? { borderColor: color, color } : undefined}
            onClick={() => go(step + 1)}
          >
            ▶
          </button>
        </div>
        <p className="cc-hint" aria-live="polite">
          {hint}
        </p>
      </div>
      {tomDe && <TomDeSide tomDe={tomDe} top={top} />}
      <div className="cc-steps">
        <StepwiseSolution q={q} color={color} jump={jump} onAllOpen={onAllOpen} onProgress={setOpened} only={step} fading="giau_het" />
      </div>
      <div className="bt-meo">
        <button type="button" className="bt-meo-head" aria-expanded={full} onClick={() => setFull((o) => !o)}>
          <span>Lời giải đầy đủ</span>
          <span aria-hidden="true">{full ? "▲" : "▼"}</span>
        </button>
        {full && (
          <div className="bt-meo-body">
            <ContentHtml html={q.solution_html ?? ""} className="block leading-relaxed" />
          </div>
        )}
      </div>
    </div>
  );
}
