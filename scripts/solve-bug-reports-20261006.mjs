import fs from "fs";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const key = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!url || !key) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY.");
  process.exit(1);
}

async function main() {
  console.log("=== BẮT ĐẦU THỰC HIỆN CÁC MỤC 1, 2, 4 ===");

  // --- 1. MỤC 1: SỬA CÂU 71 ĐỀ 72 ---
  console.log("\n--- [1] Sửa câu 71 đề 72 ---");
  const e72Res = await fetch(`${url}/rest/v1/exams?id=eq.72&select=id,title,questions`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` }
  });
  const e72 = (await e72Res.json())[0];
  const oldQ71 = e72.questions[70];
  console.log("Old options câu 71 đề 72:", oldQ71.options);
  // Sửa 127°C. -> 27°C.
  const newQ71 = { ...oldQ71, options: ["400 K.", "27°C.", "400°C.", "600°C."] };
  const newQuestions72 = [...e72.questions];
  newQuestions72[70] = newQ71;

  const updateE72 = await fetch(`${url}/rest/v1/exams?id=eq.72`, {
    method: "PATCH",
    headers: {
      apikey: key,
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ questions: newQuestions72 })
  });
  console.log("Cập nhật đề 72 status:", updateE72.status);

  // Cập nhật trong question_bank nếu có
  const qb72Res = await fetch(`${url}/rest/v1/question_bank?source_exam_id=eq.72&source_index=eq.70&select=id,question`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` }
  });
  const qb72 = await qb72Res.json();
  if (qb72 && qb72.length > 0) {
    const qbItem = qb72[0];
    const updatedQbQ = { ...qbItem.question, options: ["400 K.", "27°C.", "400°C.", "600°C."] };
    await fetch(`${url}/rest/v1/question_bank?id=eq.${qbItem.id}`, {
      method: "PATCH",
      headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ question: updatedQbQ })
    });
    console.log("Đã cập nhật question_bank id", qbItem.id);
  }

  // --- SỬA CÂU 2 ĐỀ 474 (bỏ dấu * thừa) ---
  console.log("\n--- Sửa câu 2 đề 474 (bỏ dấu * thừa) ---");
  const e474Res = await fetch(`${url}/rest/v1/exams?id=eq.474&select=id,questions`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` }
  });
  const e474 = (await e474Res.json())[0];
  const q2_474 = e474.questions[1];
  if (q2_474 && q2_474.options) {
    const newOpts = q2_474.options.map(o => o.replace(/\s*\*\s*$/, "").trim());
    e474.questions[1] = { ...q2_474, options: newOpts };
    await fetch(`${url}/rest/v1/exams?id=eq.474`, {
      method: "PATCH",
      headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ questions: e474.questions })
    });
    console.log("Đã chuẩn hoá câu 2 đề 474:", newOpts);
  }

  // --- 2. MỤC 2: CÔ LẬP CÁC CÂU THIẾU ẢNH TRONG ĐỀ 44, 49, 259 ---
  console.log("\n--- [2] Cô lập các câu thiếu ảnh trong đề 44, 49, 259 ---");
  const backupData = {
    isolated_at: new Date().toISOString(),
    exams: []
  };

  // A. Đề 44
  const e44Res = await fetch(`${url}/rest/v1/exams?id=eq.44&select=id,title,questions`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` }
  });
  const e44 = (await e44Res.json())[0];
  const e44IndicesToRemove = new Set([28, 29, 30, 31, 32, 33, 34, 37, 38, 39, 40, 41, 44, 45, 46, 50, 51, 52, 53, 54]);
  const e44Isolated = [];
  const e44Kept = [];
  e44.questions.forEach((q, idx) => {
    if (e44IndicesToRemove.has(idx)) {
      e44Isolated.push({ original_index: idx, question: q });
    } else {
      e44Kept.push(q);
    }
  });
  backupData.exams.push({ exam_id: 44, title: e44.title, isolated_count: e44Isolated.length, questions: e44Isolated });
  console.log(`Đề 44: Cô lập ${e44Isolated.length} câu, giữ lại ${e44Kept.length} câu.`);

  const updateE44 = await fetch(`${url}/rest/v1/exams?id=eq.44`, {
    method: "PATCH",
    headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ questions: e44Kept, question_count: e44Kept.length })
  });
  console.log("Cập nhật Đề 44 status:", updateE44.status);

  // B. Đề 49
  const e49Res = await fetch(`${url}/rest/v1/exams?id=eq.49&select=id,title,questions`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` }
  });
  const e49 = (await e49Res.json())[0];
  const e49IndicesToRemove = new Set([38, 39, 56]); // Câu 39, 40, 57
  const e49Isolated = [];
  const e49Kept = [];
  e49.questions.forEach((q, idx) => {
    if (e49IndicesToRemove.has(idx)) {
      e49Isolated.push({ original_index: idx, question: q });
    } else {
      e49Kept.push(q);
    }
  });
  backupData.exams.push({ exam_id: 49, title: e49.title, isolated_count: e49Isolated.length, questions: e49Isolated });
  console.log(`Đề 49: Cô lập ${e49Isolated.length} câu, giữ lại ${e49Kept.length} câu.`);

  const updateE49 = await fetch(`${url}/rest/v1/exams?id=eq.49`, {
    method: "PATCH",
    headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ questions: e49Kept, question_count: e49Kept.length })
  });
  console.log("Cập nhật Đề 49 status:", updateE49.status);

  // C. Đề 259
  const e259Res = await fetch(`${url}/rest/v1/exams?id=eq.259&select=id,title,questions`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` }
  });
  const e259 = (await e259Res.json())[0];
  const e259IndicesToRemove = new Set([20]); // Câu 21
  const e259Isolated = [];
  const e259Kept = [];
  e259.questions.forEach((q, idx) => {
    if (e259IndicesToRemove.has(idx)) {
      e259Isolated.push({ original_index: idx, question: q });
    } else {
      e259Kept.push(q);
    }
  });
  backupData.exams.push({ exam_id: 259, title: e259.title, isolated_count: e259Isolated.length, questions: e259Isolated });
  console.log(`Đề 259: Cô lập ${e259Isolated.length} câu, giữ lại ${e259Kept.length} câu.`);

  const updateE259 = await fetch(`${url}/rest/v1/exams?id=eq.259`, {
    method: "PATCH",
    headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ questions: e259Kept, question_count: e259Kept.length })
  });
  console.log("Cập nhật Đề 259 status:", updateE259.status);

  // Lưu file backup
  fs.mkdirSync("scripts/logs", { recursive: true });
  const backupFile = `scripts/logs/isolated-questions-backup-${Date.now()}.json`;
  fs.writeFileSync(backupFile, JSON.stringify(backupData, null, 2), "utf8");
  console.log(`Đã lưu toàn bộ các câu cô lập vào file backup: ${backupFile}`);

  // Cập nhật archived trong question_bank
  console.log("\n--- Cập nhật question_bank (đặt archived = true cho các câu cô lập) ---");
  // Với đề 44
  const qb44Res = await fetch(`${url}/rest/v1/question_bank?source_exam_id=eq.44&select=id,source_index`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` }
  });
  const qb44 = await qb44Res.json();
  let arch44 = 0;
  for (const item of qb44) {
    if (e44IndicesToRemove.has(item.source_index)) {
      await fetch(`${url}/rest/v1/question_bank?id=eq.${item.id}`, {
        method: "PATCH",
        headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
        body: JSON.stringify({ archived: true, note: "Tạm cô lập do thiếu hình ảnh/đồ thị minh hoạ (chờ bổ sung hình)" })
      });
      arch44++;
    }
  }
  console.log(`Đã archive ${arch44} câu trong question_bank cho Đề 44.`);

  // Với đề 49
  const qb49Res = await fetch(`${url}/rest/v1/question_bank?source_exam_id=eq.49&select=id,source_index`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` }
  });
  const qb49 = await qb49Res.json();
  let arch49 = 0;
  for (const item of qb49) {
    if (e49IndicesToRemove.has(item.source_index)) {
      await fetch(`${url}/rest/v1/question_bank?id=eq.${item.id}`, {
        method: "PATCH",
        headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
        body: JSON.stringify({ archived: true, note: "Tạm cô lập do thiếu hình ảnh/đồ thị minh hoạ (chờ bổ sung hình)" })
      });
      arch49++;
    }
  }
  console.log(`Đã archive ${arch49} câu trong question_bank cho Đề 49.`);

  // Với đề 259
  const qb259Res = await fetch(`${url}/rest/v1/question_bank?source_exam_id=eq.259&select=id,source_index`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` }
  });
  const qb259 = await qb259Res.json();
  let arch259 = 0;
  for (const item of qb259) {
    if (e259IndicesToRemove.has(item.source_index)) {
      await fetch(`${url}/rest/v1/question_bank?id=eq.${item.id}`, {
        method: "PATCH",
        headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
        body: JSON.stringify({ archived: true, note: "Tạm cô lập do thiếu hình ảnh/dữ kiện (chờ bổ sung hình)" })
      });
      arch259++;
    }
  }
  console.log(`Đã archive ${arch259} câu trong question_bank cho Đề 259.`);

  // --- 4. MỤC 4: CẬP NHẬT TRẠNG THÁI BÁO LỖI ---
  console.log("\n--- [4] Cập nhật trạng thái các báo lỗi sang ĐÃ XỬ LÝ (da_xu_ly) ---");
  const updates = [
    {
      id: 58,
      status: "da_xu_ly",
      admin_note: "Thầy đã tạm thời cô lập và ẩn 20 câu thiếu đồ thị/hình ảnh ra khỏi bài luyện tập của đề này để các em làm bài không bị lỗi; thầy sẽ bổ sung đầy đủ hình ảnh và đưa trở lại sau. Cảm ơn Khang đã báo lỗi!"
    },
    {
      id: 57,
      status: "da_xu_ly",
      admin_note: "Thầy đã sửa phương án B từ 127°C thành 27°C để tránh trùng với đáp án đúng 400 K. Cảm ơn em đã phát hiện và báo cho thầy!"
    },
    {
      id: 56,
      status: "da_xu_ly",
      admin_note: "Thầy đã mở rộng hạn mức: buổi phụ đạo nay không còn giới hạn tối đa 4 em nữa, trợ giảng có thể chọn bất kỳ số học sinh nào (hệ số giữ 1.4 cho từ 3 em trở lên)."
    },
    {
      id: 55,
      status: "da_xu_ly",
      admin_note: "Thầy đã tạm thời cô lập các câu hỏi thiếu hình ảnh hai ống dây ra khỏi bài luyện tập; thầy sẽ bổ sung hình minh hoạ sau. Cảm ơn em đã gửi kèm ảnh chụp!"
    },
    {
      id: 54,
      status: "da_xu_ly",
      admin_note: "Thầy đã kiểm tra và tạm cô lập câu 21 thiếu dữ kiện/hình vẽ ra khỏi đề kiểm tra. Cảm ơn Khải đã báo kèm ảnh chụp!"
    },
    {
      id: 52,
      status: "da_xu_ly",
      admin_note: "Thầy đã rà soát lại các phương án ở đề 474 và chuẩn hoá lại câu chữ. Cảm ơn em đã báo!"
    },
    {
      id: 51,
      status: "da_xu_ly",
      admin_note: "Thầy đã rà soát lại các phương án ở đề 474 và chuẩn hoá lại câu chữ. Cảm ơn em đã báo!"
    },
    {
      id: 49,
      status: "da_xu_ly",
      admin_note: "Thầy đã gỡ giới hạn tối đa 4 em: nay con có thể nhập thêm học sinh trong ca phụ đạo bình thường nhé."
    },
    {
      id: 48,
      status: "da_xu_ly",
      admin_note: "Khi làm bài, học sinh vẫn có thể nộp bài bình thường dù chưa làm hết (hệ thống sẽ hiển thị hộp thoại xác nhận số câu chưa làm trước khi nộp)."
    },
    {
      id: 47,
      status: "da_xu_ly",
      admin_note: "Nhãn 'X phần hổng' hiển thị số chủ đề kiến thức mà học sinh đang bị hổng theo phân tích mastery để trợ giảng nắm thông tin kèm cặp."
    },
    {
      id: 45,
      status: "da_xu_ly",
      admin_note: "Cảm ơn góp ý của em. Tính năng xem đáp án trước khi làm kiểm tra sẽ làm mất tính đánh giá của bài kiểm tra nên hệ thống không hỗ trợ; em xem được đầy đủ đáp án và lời giải chi tiết ngay sau khi nộp bài."
    },
    {
      id: 44,
      status: "da_xu_ly",
      admin_note: "Thầy đã tạm thời cô lập các câu thiếu đồ thị ra khỏi bài luyện tập để các em làm bài bình thường, và đang cập nhật lại hình ảnh."
    },
    {
      id: 5,
      status: "da_xu_ly",
      admin_note: "Trang xem lại bài làm đã có nút 'Ẩn bảng câu' ở góc trên bảng số câu để thu gọn bảng khi xem chi tiết. Cảm ơn em đã góp ý!"
    },
    {
      id: 4,
      status: "da_xu_ly",
      admin_note: "Trang xem lại bài làm đã có nút 'Ẩn bảng câu' ở góc trên bảng số câu để thu gọn bảng khi xem chi tiết. Cảm ơn em đã góp ý!"
    }
  ];

  for (const u of updates) {
    const res = await fetch(`${url}/rest/v1/bug_reports?id=eq.${u.id}`, {
      method: "PATCH",
      headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        status: u.status,
        admin_note: u.admin_note,
        updated_at: new Date().toISOString()
      })
    });
    console.log(`Updated bug report #${u.id} -> ${u.status} (HTTP ${res.status})`);
  }

  console.log("\n=== HOÀN TẤT TOÀN BỘ CÔNG VIỆC! ===");
}

main().catch(err => {
  console.error("Lỗi:", err);
  process.exit(1);
});
