// Khởi động audit ngân hàng câu hỏi như một tiến trình TÁCH HẲN (detached) để không bị giết khi phiên agent chạy lệnh khác.
// Dùng: node scripts/run-audit-detached.mjs <stage|full> <resumeOrInFile> [conc]
//   stage=full → chạy lượt 1 (resume) rồi tự nối lượt 3 (phán xử) trên cùng file.
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const stage = process.argv[2] ?? "1";
const file = process.argv[3];
const conc = process.argv[4] ?? "80";
if (!file) { console.error("thiếu file resume/in"); process.exit(1); }

const S = "scripts/audit-question-bank-answers.mts";
const logPath = path.join("scripts", "logs", `run-stage${stage}.out`);
const out = fs.openSync(logPath, "a");

let cmd;
if (stage === "full") {
  cmd = `npx tsx ${S} --stage 1 --resume ${file} --conc ${conc} && npx tsx ${S} --stage 3 --in ${file} --conc ${conc}`;
} else {
  const flag = stage === "1" ? "--resume" : "--in";
  cmd = `npx tsx ${S} --stage ${stage} ${flag} ${file} --conc ${conc}`;
}

const child = spawn("sh", ["-c", cmd], { detached: true, stdio: ["ignore", out, out] });
child.unref();
fs.writeFileSync(path.join("scripts", "logs", "audit.pid"), String(child.pid));
console.log(`Đã khởi động detached PID=${child.pid} → log: ${logPath}`);
