import { SkeletonGrid } from "@/components/ui/Skeleton";

export default function Loading() {
  return (
    <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
      <div className="mb-8 h-10 w-56 animate-pulse rounded-lg bg-white/10" />
      <SkeletonGrid count={3} />
    </main>
  );
}
