/** Ngày lịch Việt Nam, đếm từ mốc UTC — cùng một ngày thì mọi máy thấy cùng một bài. */
export function vietnamDayIndex(now = new Date()): number {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: "Asia/Ho_Chi_Minh",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(now);
  const year = Number(parts.find((part) => part.type === "year")?.value);
  const month = Number(parts.find((part) => part.type === "month")?.value);
  const day = Number(parts.find((part) => part.type === "day")?.value);
  return Math.floor(Date.UTC(year, month - 1, day) / 86_400_000);
}

/** Một bài nổi bật, rồi tối đa `othersCount` bài kế tiếp trong vòng. */
export function rotatePhysicsAround<T>(items: T[], dayIndex: number, othersCount = 3): { featured: T; others: T[] } {
  const count = items.length;
  const start = ((dayIndex % count) + count) % count;
  const others: T[] = [];
  for (let step = 1; step < count && others.length < othersCount; step++) {
    others.push(items[(start + step) % count]);
  }
  return { featured: items[start], others };
}
