# Cổng mới L10b nhóm B+D+E — sửa hộp đợt 2 theo kiem-code hop-kiem-bde-v1 (28/11/2026). Không cờ = dry-run; --apply ghi.
import json, sys
E = [
 ("l10-luc-can-luc-nang", "<strong>Quan sát:</strong> qua $1\\ \\text{m}$ đầu, phễu đã rơi <strong>đều</strong>. Chồng càng nhiều, phễu rơi đều càng nhanh.",
  "<strong>Quan sát:</strong> ghi $t$ ở đoạn $1{,}50\\ \\text{m}$ cuối cho từng chồng phễu (video bên dưới)."),
 ("l10-luc-ma-sat", "đạt cực đại $F_{\\text{msn max}} = \\mu_n N$ và cân bằng $P_x$: $mg\\sin\\alpha = \\mu_n\\, mg\\cos\\alpha$, nên hệ số ma sát nghỉ $\\mu_n = \\tan\\alpha$.",
  "đạt cực đại $F_{\\text{msn max}} = \\mu_n N$. Viết điều kiện cân bằng dọc ván để tìm $\\mu_n$ theo $\\alpha$."),
 ("l10-luc-ma-sat", 'class=\\"tl-details tl-more\\"', 'class="tl-details tl-more"'),
]
ap = "--apply" in sys.argv; loi = 0
for bai, cu, moi in E:
    for f, a, b in [("theory.src.html", cu, moi), ("theory.html", cu, moi), ("bundle.json", json.dumps(cu, ensure_ascii=False)[1:-1], json.dumps(moi, ensure_ascii=False)[1:-1])]:
        p = f"content/lesson-samples/{bai}/{f}"; s = open(p, encoding="utf-8").read(); n = s.count(a)
        if n != 1: print(f"LOI {p}: {n} lần — {cu[:50]}"); loi += 1; continue
        if ap: open(p, "w", encoding="utf-8").write(s.replace(a, b))
print(f"LOI {loi} | {'apply' if ap else 'dry-run'}")
