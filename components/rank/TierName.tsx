import { divisionLabel, tierMeta } from "@/features/rank/types";

/** Tên bậc theo thiết kế huy chương: tiếng Anh lớn (Cinzel) trên, tiếng Việt nhỏ (Playfair) dưới; cỡ sm đưa phân bậc xuống dòng dưới cho vừa ô hẹp. */
export default function TierName({
  code,
  division,
  size = "md",
  align = "left",
  className = "",
}: {
  code: string | null | undefined;
  division?: number | null;
  size?: "sm" | "md" | "lg";
  align?: "left" | "center";
  className?: string;
}) {
  const meta = tierMeta(code);
  const div = divisionLabel(division);
  const en = size === "lg" ? "text-3xl tracking-[0.18em] sm:text-4xl" : size === "md" ? "text-base tracking-[0.14em] sm:text-lg" : "text-[10px] tracking-[0.02em] sm:text-[13px] sm:tracking-[0.06em]";
  const vi = size === "lg" ? "text-base tracking-[0.2em]" : size === "md" ? "text-xs tracking-[0.18em]" : "text-[8px] tracking-[0.04em] sm:text-[10px] sm:tracking-[0.12em]";
  return (
    <span className={`block leading-none ${align === "center" ? "text-center" : "text-left"} ${className}`}>
      <span
        className={`block truncate font-bold uppercase ${en}`}
        style={{ fontFamily: "var(--font-cinzel), Cinzel, serif", color: meta.light }}
      >
        {meta.en}
        {div && size !== "sm" ? ` ${div}` : ""}
      </span>
      <span
        className={`mt-1 block truncate font-semibold uppercase text-slate-400 ${vi}`}
        style={{ fontFamily: "var(--font-playfair), \"Playfair Display\", serif" }}
      >
        {div && size === "sm" ? `${div} · ` : ""}
        {meta.name}
      </span>
    </span>
  );
}
