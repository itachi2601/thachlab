#!/bin/bash
# UserPromptSubmit hook — nhắc khi context phiên đã lớn (mỗi request đọc lại TOÀN BỘ context,
# phiên 400k tốn gấp 4 lần phiên 100k). Đo 14 ngày tới 31/10/2026: 56% token nằm ở request >200k.
# Chỉ in 1 dòng ngắn; lỗi gì cũng im lặng, không chặn phiên.
python3 -I -c '
import json,sys
try:
    p=json.load(sys.stdin).get("transcript_path") or ""
    ctx=0
    with open(p,"rb") as f:
        f.seek(0,2); f.seek(max(0,f.tell()-400000))
        for line in f.read().decode("utf-8","ignore").splitlines():
            if "\"usage\"" not in line: continue
            try: u=json.loads(line)["message"]["usage"]
            except Exception: continue
            t=u.get("input_tokens",0)+u.get("cache_read_input_tokens",0)+u.get("cache_creation_input_tokens",0)
            if t: ctx=t
    if ctx>=180000:
        print(f"[nhac-context] Context phiên ~{ctx//1000}k token. Nếu việc trước đã xong trọn: nhắc thầy /clear (ghi /ban-giao trước nếu còn dở). Việc mới không cần lịch sử này thì nên mở phiên mới.")
except Exception:
    pass
' 2>/dev/null
exit 0
