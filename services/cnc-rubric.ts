// Rubric chấm thi thực hành tổng hợp CNC (Lập trình → Mô phỏng → Cài đặt dao/phôi → Gia công),
// mô phỏng theo mẫu "RUBRIC ĐÁNH GIÁ KẾT QUẢ THỰC HÀNH" dùng trên giấy: 4 mức E/G/P/F theo %
// điểm tối đa, chia 2 nhóm I. KỸ THUẬT / II. THÀNH PHẦN với luật chặn giữa 2 nhóm, cộng lỗi loại
// trực tiếp và bảng xếp loại. Khác với checklist nhị phân (đúng/sai từng bước) đã có ở Bài 5/6/7 —
// rubric này do giáo viên (và sinh viên tự đánh giá trước) chấm ở mức tổng hợp cho cả kỳ thi.

export type RubricLevel = "E" | "G" | "P" | "F";

export const RUBRIC_LEVEL_PCT: Record<RubricLevel, number> = { E: 1, G: 0.75, P: 0.5, F: 0 };
export const RUBRIC_LEVEL_LABEL: Record<RubricLevel, string> = {
  E: "Xuất sắc",
  G: "Khá",
  P: "Đạt",
  F: "Không đạt",
};
export const RUBRIC_LEVELS: RubricLevel[] = ["E", "G", "P", "F"];

export interface RubricCriterion {
  id: string;
  label: string;
  maxScore: number;
  descriptors: Record<RubricLevel, string>;
}

export interface RubricGroup {
  id: string;
  title: string;
  criteria: RubricCriterion[];
}

export interface RubricClassificationBand {
  label: string;
  min: number;
}

export interface RubricDefinition {
  machine: "tien" | "phay";
  title: string;
  groups: RubricGroup[];
  gateGroupId: string;
  gatedGroupId: string;
  gateThreshold: number;
  zeroTolerance: readonly string[];
  classification: RubricClassificationBand[];
}

const CLASSIFICATION: RubricClassificationBand[] = [
  { label: "Xuất sắc (Excellent)", min: 8.5 },
  { label: "Khá (Good)", min: 7.0 },
  { label: "Đạt (Pass)", min: 5.0 },
  { label: "Không đạt (Failed)", min: 0 },
];

export const RUBRIC_TURN: RubricDefinition = {
  machine: "tien",
  title: "Rubric đánh giá thi thực hành tổng hợp — Tiện CNC",
  gateGroupId: "ky-thuat",
  gatedGroupId: "thanh-phan",
  gateThreshold: 3.5,
  classification: CLASSIFICATION,
  zeroTolerance: [
    "Để xảy ra đâm dao vào phôi, mâm cặp hoặc bộ phận máy do bấm nhầm nút hay di chuyển sai hướng.",
    "Vi phạm an toàn nghiêm trọng (mở cửa/đưa tay vào vùng cắt khi trục chính còn quay, không mặc bảo hộ...).",
    "Chạy chương trình cắt thật ở AUTO mà chưa mô phỏng hoặc chưa Test Offset bằng MDI + Single Block.",
    "Báo cáo sai kết quả đo kiểm sản phẩm (không đo thật hoặc gian dối số liệu).",
  ],
  groups: [
    {
      id: "ky-thuat",
      title: "I. KỸ THUẬT",
      criteria: [
        {
          id: "lap-trinh",
          label: "1. Lập trình (đọc bản vẽ, lập quy trình công nghệ, viết chương trình tiện)",
          maxScore: 1.5,
          descriptors: {
            E: "Đúng hoàn toàn cú pháp, đúng chu trình (G71/G70/G92...), đúng toàn bộ tọa độ then chốt theo bản vẽ, trình bày rõ ràng có chú thích.",
            G: "Đúng cơ bản về chu trình và tọa độ; có 1 lỗi nhỏ (thiếu M-code an toàn, làm tròn số...) tự phát hiện và sửa được.",
            P: "Cần giảng viên nhắc/hướng dẫn mới hoàn thiện; có nhầm lẫn tọa độ hoặc chu trình nhưng sửa được trước khi mô phỏng.",
            F: "Sai cú pháp nghiêm trọng, sai chu trình hoặc sai tọa độ chính, không hoàn thành được chương trình.",
          },
        },
        {
          id: "mo-phong",
          label: "2. Mô phỏng (kiểm tra quỹ đạo dao, không va chạm, đúng biên dạng)",
          maxScore: 1.0,
          descriptors: {
            E: "Mô phỏng chạy mượt, không va chạm với mâm cặp/ụ động, biên dạng khớp hoàn toàn bản vẽ; tự kiểm tra kỹ trước khi chuyển sang cắt thật.",
            G: "Biên dạng đúng; có 1 lỗi nhỏ trong mô phỏng tự phát hiện và sửa trước khi cắt thật.",
            P: "Cần giảng viên nhắc mới phát hiện lỗi mô phỏng; kết quả cuối cùng đúng.",
            F: "Không mô phỏng, hoặc mô phỏng phát hiện va chạm/sai biên dạng nhưng vẫn chạy máy thật.",
          },
        },
        {
          id: "cai-dat",
          label: "3. Cài đặt dao và phôi (đối chiếu checklist thao tác chi tiết cùng bài)",
          maxScore: 2.5,
          descriptors: {
            E: "Gá phôi chắc chắn, xác định đúng gốc phôi và bù dao (X, Z, R), kiểm chứng đầy đủ trước khi cắt thật — đúng toàn bộ quy trình.",
            G: "Đúng quy trình và kết quả; có 1 sai sót nhỏ, tự phát hiện và sửa trước khi chạy.",
            P: "Cần giảng viên hướng dẫn để hoàn thành; có nhầm lẫn khi cài đặt nhưng sửa được trước khi phát lệnh.",
            F: "Sai dấu/công thức, nhầm dao hoặc ô offset, gây va chạm hoặc không xác định được gốc.",
          },
        },
        {
          id: "gia-cong",
          label: "4. Gia công và đo kiểm sản phẩm",
          maxScore: 2.0,
          descriptors: {
            E: "Gia công đúng trình tự (thô → tinh → ren/rãnh nếu có), sản phẩm đạt kích thước trong dung sai, bề mặt đạt độ bóng yêu cầu.",
            G: "Sản phẩm đạt yêu cầu; có 1 lỗi nhỏ trong quá trình gia công không ảnh hưởng kết quả cuối.",
            P: "Cần giảng viên nhắc trong quá trình gia công; sản phẩm cuối vẫn đạt dung sai.",
            F: "Sản phẩm sai kích thước ngoài dung sai, hỏng phôi, hoặc không hoàn thành gia công.",
          },
        },
      ],
    },
    {
      id: "thanh-phan",
      title: "II. THÀNH PHẦN",
      criteria: [
        {
          id: "van-hanh-an-toan",
          label: "5. Thao tác vận hành và Test Offset bằng MDI trước khi chạy thật",
          maxScore: 1.0,
          descriptors: {
            E: "Luôn kiểm soát tốc độ/Single Block khi cần, xác nhận đúng vị trí an toàn trước khi phát lệnh chạy thật.",
            G: "Có 1 lỗi nhập nhỏ và tự sửa ngay trước Cycle Start; kết quả kiểm tra đúng và an toàn.",
            P: "Cần nhắc để hoàn thành; kết quả cuối đúng, không phát sinh chuyển động nguy hiểm.",
            F: "Không Test Offset bằng MDI, hoặc thao tác gây chuyển động nguy hiểm, giảng viên phải can thiệp.",
          },
        },
        {
          id: "an-toan-lao-dong",
          label: "6. An toàn lao động trong suốt quá trình thi",
          maxScore: 1.0,
          descriptors: {
            E: "Tuân thủ đầy đủ quy định, giữ khoảng cách an toàn, chủ động kiểm soát tình huống.",
            G: "Có 1 nhắc nhở nhỏ, không gây nguy hiểm và khắc phục ngay.",
            P: "Cần nhắc 2–3 lần về thao tác an toàn nhưng chưa phát sinh sự cố.",
            F: "Vi phạm nghiêm trọng; để xảy ra va chạm/đâm dao hoặc giảng viên phải dừng máy.",
          },
        },
        {
          id: "5s",
          label: "7. Sắp xếp nơi làm việc (5S)",
          maxScore: 0.5,
          descriptors: {
            E: "Dụng cụ đúng vị trí, khu vực máy sạch, thu gom phoi và hoàn trả đầy đủ sau bài thi.",
            G: "Nhìn chung gọn sạch, còn sót ít phoi/dụng cụ và tự khắc phục.",
            P: "Chỉ hoàn tất vệ sinh, sắp xếp sau khi được nhắc.",
            F: "Không vệ sinh hoặc không hoàn trả dụng cụ, để khu vực làm việc mất trật tự.",
          },
        },
        {
          id: "thoi-gian",
          label: "8. Thời gian hoàn thành",
          maxScore: 0.5,
          descriptors: {
            E: "Hoàn thành trong thời gian chuẩn (≤ T).",
            G: "Hoàn thành quá thời gian chuẩn không quá 10% (> T đến 1,10T).",
            P: "Hoàn thành quá thời gian chuẩn trên 10% đến 25% (> 1,10T đến 1,25T).",
            F: "Quá 1,25T hoặc không hoàn thành.",
          },
        },
      ],
    },
  ],
};

export const RUBRIC_MILL: RubricDefinition = {
  machine: "phay",
  title: "Rubric đánh giá thi thực hành tổng hợp — Phay CNC",
  gateGroupId: "ky-thuat",
  gatedGroupId: "thanh-phan",
  gateThreshold: 3.5,
  classification: CLASSIFICATION,
  zeroTolerance: [
    "Để xảy ra đâm dao vào phôi, ê-tô hoặc bộ phận máy do bấm nhầm nút hay di chuyển sai hướng.",
    "Vi phạm an toàn nghiêm trọng (mở cửa/đưa tay vào vùng dao khi trục chính còn quay, không mặc bảo hộ...).",
    "Chạy chương trình cắt thật ở AUTO mà chưa mô phỏng hoặc chưa Test Offset bằng MDI + Single Block.",
    "Báo cáo sai kết quả đo kiểm sản phẩm (không đo thật hoặc gian dối số liệu).",
  ],
  groups: [
    {
      id: "ky-thuat",
      title: "I. KỸ THUẬT",
      criteria: [
        {
          id: "lap-trinh",
          label: "1. Lập trình (đọc bản vẽ, lập quy trình công nghệ, viết chương trình phay)",
          maxScore: 1.5,
          descriptors: {
            E: "Đúng hoàn toàn cú pháp, đúng bù dao G41/G42, đúng chu trình và toàn bộ tọa độ then chốt theo bản vẽ, trình bày rõ ràng có chú thích.",
            G: "Đúng cơ bản về biên dạng và tọa độ; có 1 lỗi nhỏ tự phát hiện và sửa được.",
            P: "Cần giảng viên nhắc/hướng dẫn mới hoàn thiện; có nhầm lẫn tọa độ hoặc chu trình nhưng sửa được trước khi mô phỏng.",
            F: "Sai cú pháp nghiêm trọng, sai chu trình hoặc sai tọa độ chính, không hoàn thành được chương trình.",
          },
        },
        {
          id: "mo-phong",
          label: "2. Mô phỏng (kiểm tra quỹ đạo dao, không va chạm, đúng biên dạng)",
          maxScore: 1.0,
          descriptors: {
            E: "Mô phỏng chạy mượt, không va chạm với ê-tô/phôi, biên dạng khớp hoàn toàn bản vẽ; tự kiểm tra kỹ trước khi chuyển sang cắt thật.",
            G: "Biên dạng đúng; có 1 lỗi nhỏ trong mô phỏng tự phát hiện và sửa trước khi cắt thật.",
            P: "Cần giảng viên nhắc mới phát hiện lỗi mô phỏng; kết quả cuối cùng đúng.",
            F: "Không mô phỏng, hoặc mô phỏng phát hiện va chạm/sai biên dạng nhưng vẫn chạy máy thật.",
          },
        },
        {
          id: "cai-dat",
          label: "3. Cài đặt dao và phôi (đối chiếu checklist thao tác chi tiết cùng bài)",
          maxScore: 2.5,
          descriptors: {
            E: "Gá phôi chắc chắn trên ê-tô, xác định đúng gốc phôi G54 và bù dao (chiều dài/bán kính), kiểm chứng đầy đủ trước khi cắt thật.",
            G: "Đúng quy trình và kết quả; có 1 sai sót nhỏ, tự phát hiện và sửa trước khi chạy.",
            P: "Cần giảng viên hướng dẫn để hoàn thành; có nhầm lẫn khi cài đặt nhưng sửa được trước khi phát lệnh.",
            F: "Sai dấu/công thức, nhầm dao hoặc ô offset H/D, gây va chạm hoặc không xác định được gốc.",
          },
        },
        {
          id: "gia-cong",
          label: "4. Gia công và đo kiểm sản phẩm",
          maxScore: 2.0,
          descriptors: {
            E: "Gia công đúng trình tự (thô → tinh → khoan/tarô nếu có), sản phẩm đạt kích thước trong dung sai, bề mặt đạt độ bóng yêu cầu.",
            G: "Sản phẩm đạt yêu cầu; có 1 lỗi nhỏ trong quá trình gia công không ảnh hưởng kết quả cuối.",
            P: "Cần giảng viên nhắc trong quá trình gia công; sản phẩm cuối vẫn đạt dung sai.",
            F: "Sản phẩm sai kích thước ngoài dung sai, hỏng phôi, hoặc không hoàn thành gia công.",
          },
        },
      ],
    },
    {
      id: "thanh-phan",
      title: "II. THÀNH PHẦN",
      criteria: [
        {
          id: "van-hanh-an-toan",
          label: "5. Thao tác vận hành và Test Offset bằng MDI trước khi chạy thật",
          maxScore: 1.0,
          descriptors: {
            E: "Luôn kiểm soát tốc độ/Single Block khi cần, xác nhận đúng vị trí an toàn trước khi phát lệnh chạy thật.",
            G: "Có 1 lỗi nhập nhỏ và tự sửa ngay trước Cycle Start; kết quả kiểm tra đúng và an toàn.",
            P: "Cần nhắc để hoàn thành; kết quả cuối đúng, không phát sinh chuyển động nguy hiểm.",
            F: "Không Test Offset bằng MDI, hoặc thao tác gây chuyển động nguy hiểm, giảng viên phải can thiệp.",
          },
        },
        {
          id: "an-toan-lao-dong",
          label: "6. An toàn lao động trong suốt quá trình thi",
          maxScore: 1.0,
          descriptors: {
            E: "Tuân thủ đầy đủ quy định, giữ khoảng cách an toàn, chủ động kiểm soát tình huống.",
            G: "Có 1 nhắc nhở nhỏ, không gây nguy hiểm và khắc phục ngay.",
            P: "Cần nhắc 2–3 lần về thao tác an toàn nhưng chưa phát sinh sự cố.",
            F: "Vi phạm nghiêm trọng; để xảy ra va chạm/đâm dao hoặc giảng viên phải dừng máy.",
          },
        },
        {
          id: "5s",
          label: "7. Sắp xếp nơi làm việc (5S)",
          maxScore: 0.5,
          descriptors: {
            E: "Dụng cụ đúng vị trí, khu vực máy sạch, thu gom phoi và hoàn trả đầy đủ sau bài thi.",
            G: "Nhìn chung gọn sạch, còn sót ít phoi/dụng cụ và tự khắc phục.",
            P: "Chỉ hoàn tất vệ sinh, sắp xếp sau khi được nhắc.",
            F: "Không vệ sinh hoặc không hoàn trả dụng cụ, để khu vực làm việc mất trật tự.",
          },
        },
        {
          id: "thoi-gian",
          label: "8. Thời gian hoàn thành",
          maxScore: 0.5,
          descriptors: {
            E: "Hoàn thành trong thời gian chuẩn (≤ T).",
            G: "Hoàn thành quá thời gian chuẩn không quá 10% (> T đến 1,10T).",
            P: "Hoàn thành quá thời gian chuẩn trên 10% đến 25% (> 1,10T đến 1,25T).",
            F: "Quá 1,25T hoặc không hoàn thành.",
          },
        },
      ],
    },
  ],
};

export const RUBRIC_BY_MACHINE: Record<"tien" | "phay", RubricDefinition> = {
  tien: RUBRIC_TURN,
  phay: RUBRIC_MILL,
};

export interface RubricScoreResult {
  groupScores: Record<string, number>;
  gatePassed: boolean;
  totalScore: number;
  xepLoai: string;
  zeroToleranceFailed: boolean;
}

export function rubricMaxScore(rubric: RubricDefinition, groupId?: string) {
  const groups = groupId ? rubric.groups.filter((g) => g.id === groupId) : rubric.groups;
  return groups.reduce((sum, g) => sum + g.criteria.reduce((s, c) => s + c.maxScore, 0), 0);
}

export function isRubricComplete(rubric: RubricDefinition, levels: Record<string, RubricLevel | undefined>) {
  return rubric.groups.every((group) => group.criteria.every((criterion) => levels[criterion.id]));
}

export function gradeRubricExam(
  rubric: RubricDefinition,
  levels: Record<string, RubricLevel | undefined>,
  zeroToleranceConfirmed: Record<number, boolean>,
): RubricScoreResult {
  const groupScores: Record<string, number> = {};
  for (const group of rubric.groups) {
    groupScores[group.id] = group.criteria.reduce((sum, criterion) => {
      const level = levels[criterion.id];
      return sum + (level ? RUBRIC_LEVEL_PCT[level] * criterion.maxScore : 0);
    }, 0);
  }

  const gateScore = groupScores[rubric.gateGroupId] ?? 0;
  const gatePassed = gateScore >= rubric.gateThreshold;
  const gatedScore = gatePassed ? (groupScores[rubric.gatedGroupId] ?? 0) : 0;
  const totalScore = Math.round((gateScore + gatedScore) * 100) / 100;

  const zeroToleranceFailed = rubric.zeroTolerance.some((_, index) => !zeroToleranceConfirmed[index]);
  const band = rubric.classification.find((item) => totalScore >= item.min);
  const xepLoai = zeroToleranceFailed ? "Không đạt (lỗi loại trực tiếp)" : (band?.label ?? "Không đạt (Failed)");

  return { groupScores, gatePassed, totalScore, xepLoai, zeroToleranceFailed };
}
