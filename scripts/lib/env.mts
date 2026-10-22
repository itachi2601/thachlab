// Đọc biến môi trường cho script: ưu tiên process.env, rồi .env.local ở gốc repo.
// Dùng chung thay cho 36 bản copy readEnvLocal rải trong scripts/ (rà soát 22/10/2026) —
// script mới import từ đây; script cũ chuyển dần khi có dịp sửa.
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

let cache: Record<string, string> | null = null;

function loadEnvLocal(): Record<string, string> {
  if (cache) return cache;
  cache = {};
  for (const name of [".env.local", ".env"]) {
    let raw: string;
    try {
      raw = readFileSync(resolve(process.cwd(), name), "utf8");
    } catch {
      continue;
    }
    for (const line of raw.split("\n")) {
      const m = line.match(/^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$/);
      if (!m) continue;
      let v = m[2];
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
      if (!(m[1] in cache)) cache[m[1]] = v;
    }
  }
  return cache;
}

export function readEnvLocal(key: string): string | undefined {
  return process.env[key] ?? loadEnvLocal()[key];
}

export function requireEnv(key: string): string {
  const v = readEnvLocal(key);
  if (!v) {
    console.error(`Thiếu ${key} (đặt trong env hoặc .env.local ở gốc repo).`);
    process.exit(1);
  }
  return v;
}
