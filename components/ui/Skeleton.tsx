export function SkeletonCard() {
  return (
    <div className="animate-pulse rounded-2xl border border-white/10 bg-[#0B1020] p-6">
      <div className="h-5 w-3/4 rounded bg-white/10" />
      <div className="mt-3 h-4 w-1/2 rounded bg-white/5" />
      <div className="mt-5 h-8 w-28 rounded-full bg-white/5" />
    </div>
  );
}

export function SkeletonGrid({ count = 6 }: { count?: number }) {
  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: count }, (_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>
  );
}
