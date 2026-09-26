"use client";

import RankBadge from "@/components/rank/RankBadge";
import { tierMeta, type RankStatus } from "@/features/rank/types";

/**
 * Khung ảnh đại diện theo bậc rank: vành ngoài bằng kim loại của phân bậc
 * (III đồng · II bạc · I vàng; bậc không phân bậc → vàng), vành trong màu ruy-băng của bậc,
 * huy chương nhỏ ghim góc dưới phải. Chưa mở mùa → không khung, chỉ trả về ảnh.
 * Danh vị Vô Song → vành ngoài ánh cực quang (teal–tím–hồng–vàng) thay kim loại, huy hiệu Paragon ở góc.
 */

const METAL: Record<"bronze" | "silver" | "gold", string> = {
  gold: "conic-gradient(from 210deg, #fff3cf, #e2b93b 22%, #8a6a1e 45%, #f0d060 62%, #6b4f12 80%, #fff3cf)",
  silver: "conic-gradient(from 210deg, #ffffff, #d6dbe3 22%, #6f7784 45%, #eef1f5 62%, #4b525e 80%, #ffffff)",
  bronze: "conic-gradient(from 210deg, #f3d3ae, #c0803c 22%, #5c3814 45%, #e0a060 62%, #3d2410 80%, #f3d3ae)",
};
const AURORA = "conic-gradient(from 210deg, #26c6da, #7c4dff 25%, #ff8fd8 50%, #ffd166 75%, #26c6da)";

export default function RankAvatarFrame({
  status,
  size,
  children,
  className = "",
}: {
  status: RankStatus | null | undefined;
  /** Kích thước ảnh bên trong (px) — khung tự cộng thêm viền. */
  size: number;
  children: React.ReactNode;
  className?: string;
}) {
  const tier = status?.season ? status.tier : null;
  if (!tier) return <span className={`inline-block shrink-0 ${className}`}>{children}</span>;

  const paragon = !!tier.paragon;
  const meta = tierMeta(tier.code, paragon);
  const metal = tier.division === 3 ? "bronze" : tier.division === 2 ? "silver" : "gold";
  const ring = Math.max(3, Math.round(size * 0.075));
  const gap = Math.max(1, Math.round(size * 0.03));
  const badge = Math.round(size * 0.52);

  return (
    <span
      className={`relative inline-block shrink-0 rounded-full ${className}`}
      style={{ padding: ring, background: paragon ? AURORA : METAL[metal], boxShadow: `0 0 0 1px rgba(0,0,0,.45), 0 0 18px ${meta.color}66` }}
    >
      <span className="block rounded-full" style={{ padding: gap, background: `linear-gradient(135deg, ${meta.light}, ${meta.color})` }}>
        <span className="block overflow-hidden rounded-full bg-[#0b1020]" style={{ width: size, height: size }}>
          {children}
        </span>
      </span>
      <RankBadge
        code={tier.code}
        division={tier.division}
        paragon={paragon}
        size={badge}
        className="pointer-events-none absolute -bottom-1 -right-1.5 drop-shadow-[0_2px_4px_rgba(0,0,0,.7)]"
      />
    </span>
  );
}
