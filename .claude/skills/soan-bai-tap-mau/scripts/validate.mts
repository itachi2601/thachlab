// npx tsx .claude/skills/soan-bai-tap-mau/scripts/validate.mts scripts/data/bai-tap-mau/<id>.json
import fs from "node:fs";
import { loadTopics, validate } from "./lib";
const f = process.argv[2];
if (!f) { console.error("Dùng: validate.mts <file.json>"); process.exit(1); }
const { errors, warnings } = validate(JSON.parse(fs.readFileSync(f, "utf8")), loadTopics());
warnings.forEach((w) => console.warn("  ! " + w));
if (errors.length) { console.error("✗ " + f + "\n   - " + errors.join("\n   - ")); process.exit(1); }
console.log("✓ " + f + " qua validate");
