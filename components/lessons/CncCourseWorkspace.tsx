"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import {
  AlertTriangle,
  BookOpen,
  Check,
  ChevronDown,
  ChevronRight,
  CirclePlay,
  ClipboardCheck,
  Clock3,
  Download,
  FileQuestion,
  FileText,
  GraduationCap,
  LockKeyhole,
  MonitorPlay,
  Paperclip,
  Presentation,
  Search,
  Send,
  ShieldCheck,
  UploadCloud,
  Users,
  Wrench,
} from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import CrossCheckChecklist from "@/components/lessons/CrossCheckChecklist";
import {
  CNC_COURSE_ITEMS,
  CNC_LESSON_1_QUIZ,
  CNC_LESSON_2_QUIZ,
  CNC_LESSON_3_QUIZ,
  CNC_MILL_COMMAND_TRANSLATION_QUIZ,
  CNC_TURN_COMMAND_TRANSLATION_QUIZ,
  CNC_LESSON_4_MILL_QUIZ,
  CNC_LESSON_4_TURN_QUIZ,
} from "@/services/cnc-lms";
import {
  fetchCncLessonFiles,
  formatFileSize,
  type CncLessonFile,
} from "@/services/cnc-lesson-files";
import {
  fetchCncLessonVideos,
  getYouTubeEmbedUrl,
  type CncLessonVideo,
} from "@/services/cnc-lesson-videos";
import {
  fetchMyCncDrawingSubmission,
  submitCncDrawing,
  type CncDrawingSubmission,
} from "@/services/cnc-drawing-submissions";
import { saveCncMillingQuizAttempt } from "@/services/cnc-milling-quiz-attempts";
import { fetchCncLearningRecords, recordCncLearningResult } from "@/services/cnc-learning-records";
import turningExercises from "@/data/cnc/tien_bai345.json";
import millingExercises from "@/data/cnc/phay_bai345.json";
import operationTurnQuiz from "@/data/cnc/operation-turn.json";
import toolSetupTurnQuiz from "@/data/cnc/tool-setup-turn.json";
import operationMillQuiz from "@/data/cnc/operation-mill.json";
import toolSetupMillQuiz from "@/data/cnc/tool-setup-mill.json";
import { CNC_TOTAL_ASSESSMENTS, completedCncLessons, passedAssessmentKeys } from "@/services/cnc-progress";
import { cncCompetencyStates, fetchCourseCompetencyPermissions, type CompetencyPermission } from "@/services/cnc-competencies";

const lessons = CNC_COURSE_ITEMS.filter((item) => item.id !== "intro");
const lessonMeta: Record<string, { theory: number; practice: number; test: number; operation?: boolean; safetyGate?: boolean }> = {
  "lesson-1": { theory: 2, practice: 0, test: 0 },
  "lesson-2": { theory: 2, practice: 5, test: 1 },
  "lesson-3": { theory: 2, practice: 5, test: 1 },
  "lesson-4-turn": { theory: 1, practice: 7, test: 1, operation: true, safetyGate: true },
  "lesson-4-mill": { theory: 1, practice: 7, test: 1, operation: true, safetyGate: true },
  "lesson-5": { theory: 1, practice: 15, test: 1, operation: true },
  "lesson-6": { theory: 1, practice: 15, test: 1, operation: true },
};

const tabs = [
  { id: "outcomes", label: "Chuẩn đầu ra", short: "CĐR", description: "Năng lực cần đạt sau bài học", icon: GraduationCap },
  { id: "slides", label: "Nội dung bài học", short: "Bài giảng", description: "PowerPoint và nội dung trọng tâm", icon: Presentation },
  { id: "video", label: "Video bài giảng", short: "Video", description: "Video hướng dẫn và bài giảng bổ trợ", icon: MonitorPlay },
  { id: "test", label: "Kiểm tra", short: "Kiểm tra", description: "Đánh giá kết quả và điều kiện mở khóa", icon: FileQuestion },
  { id: "resources", label: "Tài liệu", short: "Tài liệu", description: "Tệp học tập và checklist thực hành", icon: FileText },
] as const;

export const millingChecklistSections: MillingChecklistSection[] = [
  {
    id: "prep",
    title: "I. Chuẩn bị và gá lắp",
    maxScore: 1,
    items: [
      { id: "1", label: "Chuẩn bị đầy đủ đầu dò cơ khí lệch tâm (Edge Finder / wiggler, gồm 2 phần trụ nối bằng lò xo) Ø8 mm và Z-Setter đồng hồ có chiều cao chuẩn 50 mm.", score: 0.5, note: "Thiếu dụng cụ: không có điểm." },
      { id: "2", label: "Gá phôi lên ê-tô chắc chắn, đúng kỹ thuật; sử dụng tấm kê (parallels) nếu cần và xác định rõ cao độ.", score: 0.5, note: "Phôi lỏng hoặc lệch: không đạt." },
    ],
  },
  {
    id: "xy",
    title: "II. Xác định tọa độ biên phôi (trục X, Y)",
    maxScore: 3,
    items: [
      { id: "3.1", label: "Chuyển sang JOG/HANDLE; cho trục chính quay tốc độ thấp khi dùng đầu dò cơ khí hoặc đứng yên khi dùng đầu dò quang.", score: 0.5, note: "Chạy sai chế độ vận hành: 0 điểm." },
      { id: "3.2", label: "Đưa đầu dò tới biên trái phôi theo X; dùng tay quay vi sai (X10 rồi X1) tiến từ từ đến khi đầu dò nhảy từ lệch tâm về đồng tâm và dừng ngay.", score: 0.5, note: "Ép quá chặt hoặc không chuyển nấc xung nhỏ khi cách phôi dưới 5 mm: không đạt." },
      { id: "3.3", label: "Đọc X_M đúng thời điểm đầu dò nhảy tâm; tính X_thực = X_M ± D/2 (D = 10 mm, dấu tùy biên trái/phải) và nhập vào X của G54 bằng [INPUT].", score: 0.5, note: "Sai dấu hoặc quên bán kính đầu dò: không đạt." },
      { id: "4.1", label: "Nâng dao an toàn theo trục Z rồi di chuyển sang biên trước phôi theo phương Y.", score: 0.5, note: "Không nâng Z gây va chạm: lỗi an toàn nặng.", critical: true },
      { id: "4.2", label: "Hạ Z xuống cao độ dò; cho trục chính quay và tiến dò biên Y bằng đầu dò cơ khí lệch tâm đến khi đầu dò nhảy về đồng tâm.", score: 0.5, note: "Dò từ từ, không ép đầu dò vào phôi." },
      { id: "4.3", label: "Đọc Y_M tại thời điểm nhảy tâm; tính Y_thực = Y_M ± D/2, nhập vào Y của G54 bằng [INPUT] và xác lập X0Y0 tại đúng đỉnh góc đã chọn.", score: 0.5, note: "Kiểm tra đúng dấu và đúng ô tọa độ." },
    ],
  },
  {
    id: "tool",
    title: "III. Cài đặt thông số chiều dài dao (Tool Offset)",
    maxScore: 2.5,
    items: [
      { id: "5", label: "Đặt Z-Setter tại vị trí tham chiếu chuẩn trên bàn máy và gọi đúng dao cần cài đặt ra trục chính bằng T… M06.", score: 0.5, note: "Kiểm tra đúng dụng cụ trước khi đo." },
      { id: "6", label: "Dùng HANDLE đưa trục Z xuống từ từ đến khi mũi dao chạm Z-Setter và kim về đúng vạch 0.", score: 1, note: "Lao dao quá nhanh làm hỏng Z-Setter: không đạt.", critical: true },
      { id: "7", label: "Vào OFFSET → GEOMETRY, chọn đúng H của dao; nhập chiều cao Z-Setter (ví dụ Z50.0) và [MEASURE].", score: 1, note: "Nhập nhầm hàng/cột dao khác: 0 điểm." },
    ],
  },
  {
    id: "z",
    title: "IV. Cài đặt gốc phôi trục Z (Work Offset G54)",
    maxScore: 1.5,
    items: [
      { id: "8", label: "Gọi dao chuẩn và dùng tay quay đưa mũi dao tiếp xúc nhẹ với bề mặt làm việc mong muốn của phôi.", score: 0.5, note: "Tiếp xúc nhẹ, không ép dao." },
      { id: "9", label: "Tại WORK OFFSET, nhập Z_M vào G54 cột Z và cộng/trừ đúng chiều cao ê-tô/tấm kê nếu gốc ở đáy.", score: 1, note: "Sai dấu cao độ đồ gá: không đạt." },
    ],
  },
  {
    id: "test",
    title: "V. Kiểm tra an toàn và chạy thử (Test Offset – MDI)",
    maxScore: 2,
    items: [
      { id: "10", label: "Nâng Z lên vị trí cao an toàn; chuyển MDI và nhập đúng: G90 G54; T1 M06; M3 S800; G43 H01 G00 X0 Y0; Z10; Z0; M5.", score: 1, note: "Thiếu G43 H01: 0 điểm.", critical: true },
      { id: "11", label: "Bật SBL, nhấn CYCLE START để chạy từng lệnh; xác nhận dao tới đúng X/Y, dừng tại Z10 và chạm đúng mặt phôi ở Z0.", score: 1, note: "Dao đâm phôi hoặc dừng sai khoảng cách: không đạt.", critical: true },
    ],
  },
];

export const millingZeroTolerance = [
  "Không nâng trục Z lên cao khi di chuyển dao giữa các biên phôi, gây va đập hoặc cọ xát dao vào phôi.",
  "Để xảy ra đâm dao vào phôi, ê-tô hoặc Z-Setter do bấm nhầm nút hoặc di chuyển sai hướng.",
  "Cho trục chính quay quá tốc độ cho phép khi dò biên bằng đầu dò cơ khí lệch tâm, gây văng hoặc gãy đầu dò.",
  "Không chạy thử Test Offset ở chế độ MDI trước khi vận hành tự động.",
] as const;

export const turningChecklistSections: MillingChecklistSection[] = [
  {
    id: "turn-prep",
    title: "I. Chuẩn bị và gá lắp",
    maxScore: 1,
    items: [
      { id: "T1", label: "Chuẩn bị đầy đủ thước cặp đo phôi, lục giác mở chấu mâm cặp và dao tiện cần dùng.", score: 0.3, note: "Thiếu dụng cụ hoặc dùng sai loại thước đo: không đạt." },
      { id: "T2", label: "Kiểm tra chiều dài phôi bằng thước cặp trước khi gá và ghi lại giá trị H_phôi.", score: 0.3, note: "Đo sau khi đã kẹp hoặc sai vị trí chuẩn: không đạt." },
      { id: "T3", label: "Dùng lục giác mở chấu mâm cặp, gá phôi và siết với lực kẹp vừa đủ, đúng kỹ thuật.", score: 0.4, note: "Phôi lỏng hoặc lệch tâm: không đạt.", critical: true },
    ],
  },
  {
    id: "turn-work-offset",
    title: "II. Cài đặt thông số phôi",
    maxScore: 2,
    items: [
      { id: "T4.1", label: "Nhấn OFFSET, vào bảng Work Shift; nhấn DEL đưa dữ liệu X, Z về 0.", score: 0.5, note: "Không xóa dữ liệu cũ có thể gây chồng lấn offset." },
      { id: "T4.2", label: "Lấy khoảng cách MA (khoảng cách từ điểm chuẩn máy M đến mặt đầu mâm cặp A), thêm dấu âm và nhập vào ô Z cột Shift Value.", score: 0.5, note: "Sai dấu hoặc nhập nhầm cột: không đạt." },
      { id: "T4.3", label: "Lấy chiều dài phôi AW (khoảng cách từ mặt đầu mâm cặp A đến gốc toạ độ phôi W) đã đo, thêm dấu âm và nhập vào Z cột Measurement.", score: 0.5, note: "Phải dùng số đo của phôi thực tế đang gá." },
      { id: "T4.4", label: "Kiểm tra lại Z Work Shift và xác nhận không dùng phương pháp chạm dao vào phôi để lấy gốc Z.", score: 0.5, note: "Dùng lại phương pháp cũ: không đạt.", critical: true },
    ],
  },
  {
    id: "turn-tool-setup",
    title: "III. Cài đặt thông số dao (Tool Geometry)",
    maxScore: 3.5,
    items: [
      { id: "T5.1", label: "Nhấn OFFSET, vào Geometry; nhấn DEL đưa toàn bộ dữ liệu cột X, Z về 0.", score: 0.5, note: "Không xóa offset dao cũ: không đạt." },
      { id: "T5.2", label: "Chuyển sang MDI, nhấn PROGRM, chọn dao cần cài và gọi T0202.", score: 0.5, note: "Gọi sai mã dao hoặc offset: không đạt." },
      { id: "T5.3", label: "Cho trục chính quay bằng lệnh M03 S800 trên máy TURN 55.", score: 0.5, note: "Sai chiều quay hoặc tốc độ quá cao: lỗi an toàn.", critical: true },
      { id: "T5.4", label: "Chuyển sang JOG và nhấn POS để mở màn hình Position.", score: 0.5, note: "Xác nhận đúng chế độ trước khi di chuyển dao." },
      { id: "T5.5", label: "Đặt bước tiến 40%, đưa dao cách mặt đầu khoảng 5 mm theo Z rồi giảm xuống 2% trước khi tiếp cận.", score: 0.5, note: "Giữ 40% khi cách phôi dưới 5 mm: lỗi an toàn nặng.", critical: true },
      { id: "T5.6", label: "Ở bước tiến 2%, chạm nhẹ mặt đầu phôi và ghi vị trí Z trên màn hình Position Absolute.", score: 0.5, note: "Chạm quá mạnh gây xước phôi hoặc mẻ dao: không đạt." },
      { id: "T5.7", label: "Nhấn OFFSET vào Geometry và nhập giá trị Z vừa ghi vào ô nhớ 02 cột Z.", score: 0.5, note: "Nhập nhầm ô nhớ hoặc dao khác: không đạt." },
    ],
  },
  {
    id: "turn-x",
    title: "IV. Xác định X dao — tiện thử đo đường kính",
    maxScore: 2.5,
    items: [
      { id: "T6.1", label: "Đưa dao cách mặt trụ khoảng 5 mm theo X rồi tiến từ từ cho dao chạm mặt trụ.", score: 0.5, note: "Tiến bước lớn khi dao cách phôi dưới 5 mm: không đạt." },
      { id: "T6.2", label: "Đưa dao theo Z ra ngoài mặt đầu khoảng 5 mm và lấy chiều sâu cắt khoảng 1 mm.", score: 0.5, note: "Kiểm tra hướng trục trước khi di chuyển." },
      { id: "T6.3", label: "Tiện đoạn trụ ngắn L = 10 mm rồi lùi dao theo Z ra ngoài mặt đầu khoảng 50 mm.", score: 0.5, note: "Không lùi dao an toàn trước khi dừng trục chính: lỗi an toàn.", critical: true },
      { id: "T6.4", label: "Dừng hẳn trục chính, mở cửa và đo đường kính đoạn trụ vừa tiện bằng thước cặp; ghi lại kết quả.", score: 0.5, note: "Mở cửa khi trục chính chưa dừng hẳn: lỗi an toàn nặng.", critical: true },
      { id: "T6.5", label: "Mở OFFSET → Geometry, chọn ô nhớ 02 cột X; nhập X cộng đường kính vừa đo và nhấn F4 MEASURE.", score: 0.5, note: "Nhập bán kính thay vì đường kính hoặc sai cấu trúc: không đạt." },
    ],
  },
  {
    id: "turn-test",
    title: "V. Kiểm tra an toàn và hoàn tất (Test Offset)",
    maxScore: 1,
    items: [
      { id: "T7.1", label: "Đóng cửa máy, chuyển sang MDI, bật Single Block (SBL), gọi T0202 và chạy thử kiểm tra dao di chuyển đúng theo offset vừa cài.", score: 0.5, note: "Không chạy Test Offset bằng MDI + SBL: không đạt.", critical: true },
      { id: "T7.2", label: "Hoàn thành cài đặt dao, phôi; vệ sinh khu vực, tắt trục chính và đưa máy về trạng thái an toàn.", score: 0.5, note: "Bàn giao máy sạch và ở trạng thái an toàn." },
    ],
  },
];

export const turningZeroTolerance = [
  "Không để xảy ra đâm dao vào phôi, mâm cặp hoặc bộ phận máy do bấm nhầm nút hay di chuyển sai hướng.",
  "Không mở cửa khi trục chính chưa dừng hẳn và không vận hành khi cửa an toàn chưa đóng.",
  "Không dùng phương pháp chạm dao vào phôi để lấy gốc Z; phải dùng thước cặp đo H_phôi.",
  "Phải chạy thử Test Offset ở chế độ MDI + Single Block trước khi vận hành tự động.",
] as const;

type TabId = (typeof tabs)[number]["id"];

export type MillingChecklistItem = {
  id: string;
  label: string;
  score: number;
  note: string;
  critical?: boolean;
};

export type MillingChecklistSection = {
  id: string;
  title: string;
  maxScore: number;
  items: MillingChecklistItem[];
};

export default function CncCourseWorkspace({ embedded = false, courseId }: { embedded?: boolean; courseId?: number }) {
  const { profile: viewerProfile, session } = useAuth();
  const [lessonId, setLessonId] = useState("lesson-1");
  const [expandedLessonId, setExpandedLessonId] = useState<string | null>(null);
  const [tab, setTab] = useState<TabId | null>(null);
  const [lessonSearch, setLessonSearch] = useState("");
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const [completed, setCompleted] = useState<Record<string, boolean>>({});
  const [passedAssessments, setPassedAssessments] = useState<Set<string>>(new Set());
  const [competencyPermissions, setCompetencyPermissions] = useState<CompetencyPermission[]>([]);
  const [lessonFiles, setLessonFiles] = useState<CncLessonFile[]>([]);
  const [lessonVideos, setLessonVideos] = useState<CncLessonVideo[]>([]);
  const markCompleted = useCallback((completedLessonId: string) => {
    setCompleted((current) => current[completedLessonId] ? current : ({ ...current, [completedLessonId]: true }));
    setPassedAssessments((current) => new Set(current).add(`${completedLessonId}:final`));
    if (courseId && session?.user.id && viewerProfile?.role !== "admin") void recordCncLearningResult({ courseId, lessonId: completedLessonId, completed: true });
  }, [courseId, session?.user.id, viewerProfile?.role]);

  const recordQuiz = useCallback((quizLessonId: string, assessmentId: string, quizScore: number, total: number, didPass: boolean) => {
    if (didPass) setPassedAssessments((current) => new Set(current).add(`${quizLessonId}:${assessmentId}`));
    if (!courseId || !session?.user.id || viewerProfile?.role === "admin") return;
    void recordCncLearningResult({ courseId, lessonId: quizLessonId, assessmentId, score: quizScore, total, completed: didPass });
  }, [courseId, session?.user.id, viewerProfile?.role]);

  const lesson = lessons.find((item) => item.id === lessonId) ?? lessons[0];
  const meta = lessonMeta[lesson.id];
  const safetyQuiz = lesson.id === "lesson-4-mill"
    ? CNC_LESSON_4_MILL_QUIZ
    : CNC_LESSON_4_TURN_QUIZ;
  const requiredSafetyScore = safetyQuiz.length;
  const score = useMemo(
    () => safetyQuiz.filter((q) => answers[q.id] === q.correctIndex).length,
    [answers, safetyQuiz],
  );
  const passed = submitted && score >= requiredSafetyScore;
  const progress = Math.round((passedAssessments.size / CNC_TOTAL_ASSESSMENTS) * 100);
  const visibleLessons = lessons.filter((item) =>
    `${item.title} ${item.shortTitle}`.toLocaleLowerCase("vi-VN").includes(
      lessonSearch.trim().toLocaleLowerCase("vi-VN"),
    ),
  );

  useEffect(() => {
    if (!courseId || !session?.user.id || viewerProfile?.role === "admin") return;
    let cancelled = false;
    fetchCncLearningRecords(courseId, session.user.id).then((rows) => {
      if (!cancelled) {
        setCompleted(Object.fromEntries([...completedCncLessons(rows)].map((id) => [id, true])));
        setPassedAssessments(passedAssessmentKeys(rows));
      }
    }).catch(() => undefined);
    return () => { cancelled = true; };
  }, [courseId, session?.user.id, viewerProfile?.role]);

  useEffect(() => {
    if (!courseId || !session?.user.id || viewerProfile?.role === "admin") return;
    void fetchCourseCompetencyPermissions(courseId, session.user.id).then(setCompetencyPermissions).catch(() => setCompetencyPermissions([]));
  }, [courseId, session?.user.id, viewerProfile?.role]);

  useEffect(() => {
    const requestedLesson = new URLSearchParams(window.location.search).get("bai");
    if (!requestedLesson || !lessons.some((item) => item.id === requestedLesson)) return;
    const timer = window.setTimeout(() => {
      setLessonId(requestedLesson);
      setExpandedLessonId(requestedLesson);
      setTab("outcomes");
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    let cancelled = false;
    fetchCncLessonFiles(lessonId)
      .then((files) => {
        if (!cancelled) setLessonFiles(files);
      })
      .catch(() => {
        if (!cancelled) setLessonFiles([]);
      });
    return () => {
      cancelled = true;
    };
  }, [lessonId]);

  useEffect(() => {
    let cancelled = false;
    fetchCncLessonVideos(lessonId)
      .then((videos) => {
        if (!cancelled) setLessonVideos(videos);
      })
      .catch(() => {
        if (!cancelled) setLessonVideos([]);
      });
    return () => {
      cancelled = true;
    };
  }, [lessonId]);

  const selectLesson = (id: string) => {
    if (expandedLessonId === id) {
      setExpandedLessonId(null);
      setTab(null);
      return;
    }
    setLessonId(id);
    setExpandedLessonId(id);
    setTab("outcomes");
    setAnswers({});
    setSubmitted(false);
  };

  const renderSectionContent = (sectionId: TabId) => {
    if (sectionId === "outcomes") return <Outcomes lesson={lesson} meta={meta} />;
    if (sectionId === "slides") return <Slides lesson={lesson} files={lessonFiles.filter((file) => file.kind === "powerpoint")} />;
    if (sectionId === "video") return <Video lesson={lesson} videos={lessonVideos} />;
    if (sectionId === "test") {
      if (meta.safetyGate) {
        return <OperationTestSuite key={lesson.id} machine={lesson.id === "lesson-4-turn" ? "tiện" : "phay"} courseId={courseId} onResult={(assessmentId,value,total,didPass)=>recordQuiz(lesson.id,assessmentId,value,total,didPass)} onCompleted={() => setCompleted(current=>({...current,[lesson.id]:true}))} />;
      }
      if (lesson.id === "lesson-5" || lesson.id === "lesson-6") {
        return <DrawingSubmissionTest key={lesson.id} lessonId={lesson.id} lessonTitle={lesson.shortTitle} courseId={courseId} onApproved={markCompleted} />;
      }
      if (lesson.id === "lesson-2" || lesson.id === "lesson-3") {
        return <ProgrammingTestSuite key={lesson.id} lessonId={lesson.id} lessonTitle={lesson.shortTitle} courseId={courseId} onResult={(assessmentId,value,total,didPass)=>recordQuiz(lesson.id,assessmentId,value,total,didPass)} onPassed={() => undefined} />;
      }
      return <StandardTest key={lesson.id} lessonId={lesson.id} lessonTitle={lesson.shortTitle} onResult={(value,total,didPass)=>recordQuiz(lesson.id,"final",value,total,didPass)} onPassed={() => markCompleted(lesson.id)} />;
    }
    const isOperationChecklist = lesson.id === "lesson-4-turn" || lesson.id === "lesson-4-mill";
    const operationChecklistEnabled = viewerProfile?.role === "admin" || ["machine-operation", "tool-setup"].every((assessmentId) => passedAssessments.has(`${lesson.id}:${assessmentId}`));
    return isOperationChecklist
      ? <PracticalChecklistPanel machine={lesson.id === "lesson-4-turn" ? "tiện" : "phay"} lessonId={lesson.id as "lesson-4-turn" | "lesson-4-mill"} enabled={operationChecklistEnabled} courseId={courseId} />
      : <Resources lesson={lesson} files={lessonFiles.filter((file) => file.kind === "material")} />;
  };

  return (
    <div className={`cnc-shell ${embedded ? "cnc-embedded" : ""}`}>
      <header className="cnc-course-header">
        <div className="cnc-breadcrumb">
          <Link href="/lop-hoc?tab=cttc">Lớp học</Link><ChevronRight size={14} /><Link href="/lop-hoc?tab=cttc">CTTC</Link><ChevronRight size={14} />Gia công CNC
        </div>
        <div className="cnc-header-grid">
          <div>
            <span className="cnc-kicker"><Wrench size={14} /> Học phần chuyên ngành</span>
            <h1>Gia công <em>CNC</em></h1>
            <p>Thực tập máy tiện, máy phay điều khiển theo chương trình số</p>
          </div>
          <div className="cnc-progress-card" aria-label={`Tiến độ ${progress}%`}>
            <div><span>Tiến độ học phần</span><strong>{progress}%</strong></div>
            <div className="cnc-progress-track"><i style={{ width: `${progress}%` }} /></div>
            <small>{passedAssessments.size}/{CNC_TOTAL_ASSESSMENTS} bài kiểm tra đã đạt</small>
          </div>
        </div>
        <div className="cnc-stats">
          <span><Clock3 />70 tiết</span><span><BookOpen />7 bài học</span><span><ShieldCheck />2 cổng an toàn vận hành</span>
        </div>
      </header>

      <div className="cnc-workspace cnc-accordion-workspace">
        <section className="cnc-course-outline">
          <div className="cnc-nav-heading"><span>Chương trình Gia công CNC</span><small>7 BÀI HỌC</small></div>
          <label className="cnc-lesson-search">
            <Search size={20} />
            <input value={lessonSearch} onChange={(event) => setLessonSearch(event.target.value)} placeholder="Tìm bài học…" />
          </label>
          <div className="cnc-lesson-stack">
            {visibleLessons.map((item) => {
              const index = lessons.findIndex((candidate) => candidate.id === item.id);
              const itemMeta = lessonMeta[item.id];
              const active = expandedLessonId === item.id;
              const competencyStates = cncCompetencyStates(Array.from(passedAssessments).map(key => { const separator=key.lastIndexOf(":"); return {course_id:courseId??0,student_id:session?.user.id??"",lesson_id:key.slice(0,separator),assessment_id:key.slice(separator+1),completed:true,latest_score:null,best_score:null,total_questions:null,attempt_count:1,last_activity_at:""}; }),competencyPermissions);
              const locked = viewerProfile?.role !== "admin" && ((item.id === "lesson-5" && !competencyStates["turn-machining"].approved) || (item.id === "lesson-6" && !competencyStates["mill-machining"].approved));
              return (
                <article key={item.id} className={`cnc-lesson-accordion ${active ? "expanded" : ""} ${locked ? "locked" : ""}`}>
                  <button
                    type="button"
                    disabled={locked}
                    onClick={() => selectLesson(item.id)}
                    className="cnc-lesson-toggle"
                    aria-expanded={active}
                    aria-controls={`cnc-lesson-panel-${item.id}`}
                    aria-label={`${active ? "Thu gọn" : "Mở"} ${item.shortTitle}`}
                  >
                    <span className={`cnc-lesson-number ${completed[item.id] ? "done" : ""}`}>
                      {completed[item.id] ? <Check size={15} /> : index + 1}
                    </span>
                    <span className="cnc-lesson-copy">
                      <strong>{item.shortTitle}</strong>
                      <small>{item.duration} · {itemMeta.practice ? `${itemMeta.practice} thực hành` : "Lý thuyết"}</small>
                    </span>
                    {locked ? <LockKeyhole className="safety-icon" size={15} /> : itemMeta.safetyGate && <ShieldCheck className="safety-icon" size={16} />}
                    <span className={`cnc-lesson-collapse-label ${active ? "active" : ""}`}>
                      {active ? "Thu gọn" : "Mở bài"}
                    </span>
                    <ChevronDown className="cnc-accordion-chevron" size={18} />
                  </button>

                  {active && (
                    <div id={`cnc-lesson-panel-${item.id}`} className="cnc-lesson-panel">
                      <div className="cnc-lesson-hero">
                        <div className="cnc-title-row">
                          <div>
                            <span className="cnc-eyebrow">CTTC · GIA CÔNG CNC · BÀI {index + 1}</span>
                            <h2>{item.title.replace(/^Bài \d+: /, "")}</h2>
                            {"emphasis" in item && item.emphasis && <p>{item.emphasis}</p>}
                          </div>
                          {itemMeta.operation && <span className="cnc-operation-badge"><ShieldCheck size={16} /> {itemMeta.safetyGate ? "Bài vận hành" : "Bài gia công"}</span>}
                        </div>
                        <div className="cnc-lesson-progress-row">
                          <div className="cnc-section-progress-ring"><strong>{completed[lesson.id] ? 5 : tabs.findIndex((itemTab) => itemTab.id === tab) + 1}<small>/5</small></strong></div>
                          <nav className="cnc-section-pills" aria-label="Đi nhanh đến phần bài học">
                            {tabs.map(({ id, label }, tabIndex) => {
                              const displayLabel = (item.id === "lesson-4-turn" || item.id === "lesson-4-mill") && id === "resources" ? "Check list" : label;
                              return <button key={id} type="button" onClick={() => setTab(id)} className={`${id} ${tab === id ? "active" : ""}`}><i />{tabIndex + 1}. {displayLabel}</button>;
                            })}
                          </nav>
                        </div>
                      </div>

                      <div className="cnc-learning-sections">
                        {tabs.map(({ id, label, description, icon: Icon }, tabIndex) => {
                          const displayLabel = (item.id === "lesson-4-turn" || item.id === "lesson-4-mill") && id === "resources" ? "Check list" : label;
                          const isActive = tab === id;
                          return <section key={id} className={`cnc-learning-section ${id} ${isActive ? "active" : ""}`}>
                            <header>
                              <span>§ {tabIndex + 1}</span>
                              <div><Icon size={19} /><strong>{displayLabel}</strong></div>
                              <i />
                              <small>{completed[lesson.id] ? "Xong" : isActive ? "Đang mở" : "Chưa xong"}</small>
                              <b>1</b>
                            </header>
                            <button
                              type="button"
                              className="cnc-learning-card"
                              onClick={() => setTab((current) => current === id ? null : id)}
                              aria-expanded={isActive}
                              aria-controls={`cnc-section-${lesson.id}-${id}`}
                              aria-label={`${isActive ? "Thu gọn" : "Mở"} mục ${displayLabel}`}
                            >
                              <span><Icon size={22} /></span>
                              <div><strong>{displayLabel}</strong><small>{description}</small></div>
                              <b>{isActive ? "Thu gọn" : id === "test" ? "Làm bài" : "Xem"}<ChevronDown size={17} /></b>
                            </button>
                            {isActive && <div id={`cnc-section-${lesson.id}-${id}`} className="cnc-section-body cnc-content">{renderSectionContent(id)}</div>}
                          </section>;
                        })}
                      </div>

                      <div className="cnc-lesson-footer">
                        <span>{completed[lesson.id] ? <><Check size={16} /> Đã hoàn thành bài học</> : lesson.id === "lesson-4-mill" ? "Hoàn thành kiểm tra trước máy và Checklist đạt yêu cầu để kết thúc bài" : "Bài học sẽ tự động hoàn thành khi sinh viên vượt qua bài kiểm tra"}</span>
                      </div>
                    </div>
                  )}
                </article>
              );
            })}
            {visibleLessons.length === 0 && <div className="cnc-search-empty">Không tìm thấy bài học phù hợp.</div>}
          </div>
          <div className="cnc-support"><ShieldCheck size={20} /><div><strong>An toàn là ưu tiên</strong><p>Bài vận hành phải đạt đúng ngưỡng kiểm tra trước máy của từng bài.</p></div></div>
        </section>
      </div>
    </div>
  );
}

function DrawingSubmissionTest({ lessonId, lessonTitle, courseId, onApproved }: { lessonId: string; lessonTitle: string; courseId?: number; onApproved: (lessonId: string) => void }) {
  const { session, profile, loading: authLoading } = useAuth();
  const [submission, setSubmission] = useState<CncDrawingSubmission | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const isSimulation = lessonId.endsWith("-simulation");

  useEffect(() => {
    if (authLoading) return;
    if (!session) {
      setLoading(false);
      return;
    }
    let cancelled = false;
    setLoading(true);
    fetchMyCncDrawingSubmission(lessonId, courseId)
      .then((data) => {
        if (cancelled) return;
        setSubmission(data);
        if (data?.status === "approved") onApproved(lessonId);
      })
      .catch((cause) => {
        if (!cancelled) setError(cause instanceof Error ? cause.message : "Không tải được hồ sơ bản vẽ.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [authLoading, courseId, lessonId, onApproved, session]);

  function selectFile(file: File | undefined) {
    if (!file) return;
    if (!/\.(pdf|dwg|dxf|doc|docx|png|jpe?g|webp|nc|txt|mp4|mov)$/i.test(file.name)) {
      setError(isSimulation ? "Minh chứng phải là chương trình NC, tài liệu, ảnh hoặc video." : "Bản vẽ phải có định dạng PDF, DWG, DXF, Word hoặc ảnh.");
      return;
    }
    if (file.size > 25 * 1024 * 1024) {
      setError("Tệp bản vẽ vượt quá giới hạn 25 MB.");
      return;
    }
    setError("");
    setSelectedFile(file);
  }

  async function submitSelectedFile() {
    if (!selectedFile) return;
    setUploading(true);
    setError("");
    try {
      const result = await submitCncDrawing({ lessonId, file: selectedFile, courseId });
      setSubmission(result);
      setSelectedFile(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không nộp được bản vẽ.");
    } finally {
      setUploading(false);
    }
  }

  const machine = lessonId.includes("lesson-2") || lessonId === "lesson-5" ? "tiện" : "phay";
  const status = submission?.status;
  return <>
    <SectionHeading icon={FileQuestion} kicker="MỤC 04" title={isSimulation ? "Mô phỏng và kiểm chứng" : "Nộp bản vẽ để duyệt"} description={isSimulation ? "Nộp chương trình NC cùng ảnh hoặc video kết quả mô phỏng để giảng viên kiểm tra." : `Giảng viên kiểm tra bản vẽ trước khi cho phép sinh viên gia công ${machine} trên máy CNC.`} />
    <div className={`cnc-drawing-gate ${status ?? "empty"}`}>
      <div className="cnc-drawing-icon">{status === "approved" ? <Check size={28} /> : status === "rejected" ? <FileQuestion size={28} /> : <UploadCloud size={28} />}</div>
      <div className="cnc-drawing-copy">
        <span>{isSimulation ? "MINH CHỨNG MÔ PHỎNG" : "HỒ SƠ GIA CÔNG"} · {lessonTitle.toUpperCase()}</span>
        <h3>{status === "approved" ? (isSimulation ? "Kết quả mô phỏng đã được duyệt" : "Bản vẽ đã được giảng viên duyệt") : status === "pending" ? (isSimulation ? "Kết quả mô phỏng đang chờ duyệt" : "Bản vẽ đang chờ giảng viên duyệt") : status === "rejected" ? "Giảng viên yêu cầu nộp lại" : (isSimulation ? "Nộp kết quả mô phỏng" : "Nộp bản vẽ gia công")}</h3>
        <p>{status === "approved" ? (isSimulation ? "Bài mô phỏng và kiểm chứng đã đạt yêu cầu." : `Sinh viên đã được mở khóa và được phép tiến hành gia công ${machine} trên máy CNC.`) : status === "pending" ? "Bạn sẽ nhận được kết quả ngay tại đây sau khi giảng viên kiểm tra." : status === "rejected" ? (submission?.teacher_feedback || "Hãy chỉnh sửa theo yêu cầu và nộp lại.") : (isSimulation ? "Chấp nhận NC, TXT, PDF, Word, ảnh hoặc video; dung lượng tối đa 25 MB." : "Chấp nhận PDF, DWG, DXF, Word hoặc ảnh; dung lượng tối đa 25 MB.")}</p>
        {submission && <small>{submission.file_name} · Nộp lúc {new Date(submission.updated_at).toLocaleString("vi-VN")}</small>}
      </div>
      <b>{status === "approved" ? "ĐÃ DUYỆT" : status === "pending" ? "CHỜ DUYỆT" : status === "rejected" ? "NỘP LẠI" : "CHƯA NỘP"}</b>
    </div>
    {loading || authLoading ? <div className="cnc-file-empty">Đang tải trạng thái hồ sơ…</div> : !session ? (
      <div className="cnc-drawing-action"><p>Hãy đăng nhập bằng tài khoản sinh viên để nộp và theo dõi bản vẽ.</p><Link href="/dang-nhap">Đăng nhập</Link></div>
    ) : status !== "pending" && status !== "approved" ? (
      <div className="cnc-drawing-submit-box">
        <label className={`cnc-drawing-upload ${uploading ? "busy" : ""}`}>
          <Paperclip size={19} />
          <span>{selectedFile ? "Chọn file khác" : (isSimulation ? "Đính kèm minh chứng" : "Đính kèm bản vẽ")}</span>
          <input type="file" accept={isSimulation ? ".nc,.txt,.pdf,.doc,.docx,.png,.jpg,.jpeg,.webp,.mp4,.mov" : ".pdf,.dwg,.dxf,.doc,.docx,.png,.jpg,.jpeg,.webp"} disabled={uploading} onChange={(event) => { selectFile(event.target.files?.[0]); event.currentTarget.value = ""; }} />
        </label>
        {selectedFile && <div className="cnc-selected-drawing">
          <div><Paperclip size={16} /><span><strong>{selectedFile.name}</strong><small>{formatFileSize(selectedFile.size)}</small></span></div>
          <button type="button" disabled={uploading} onClick={submitSelectedFile}><Send size={16} />{uploading ? "Đang nộp…" : "Nộp cho giảng viên"}</button>
        </div>}
        {profile?.role === "admin" && <small className="cnc-admin-preview-note">Đang xem bằng tài khoản quản trị; nút được hiển thị để kiểm tra giao diện sinh viên.</small>}
      </div>
    ) : null}
    {error && <div className="cnc-result">{error}</div>}
  </>;
}

function Outcomes({ lesson, meta }: { lesson: (typeof lessons)[number]; meta: (typeof lessonMeta)[string] }) {
  const outcomes = "overview" in lesson && lesson.overview
    ? [lesson.overview.outcome, lesson.overview.purpose]
    : [
        `Trình bày đúng quy trình và nguyên tắc của ${lesson.shortTitle.toLowerCase()}.`,
        "Thực hiện nhiệm vụ theo bản vẽ, thông số công nghệ và tiêu chuẩn an toàn xưởng.",
        "Tự kiểm tra kết quả, phát hiện sai hỏng và đề xuất biện pháp khắc phục.",
      ];
  return <>
    <SectionHeading icon={GraduationCap} kicker="MỤC 01" title="Chuẩn đầu ra bài học" description="Sau khi hoàn thành bài học, sinh viên có thể:" />
    <div className="cnc-outcomes">
      {outcomes.map((item, index) => <div key={item}><span>CĐR {index + 1}</span><p>{item}</p><Check size={18} /></div>)}
    </div>
    <div className="cnc-allocation">
      <strong>Phân bổ thời gian</strong>
      <div><span><i className="theory" />Lý thuyết <b>{meta.theory} tiết</b></span><span><i className="practice" />Bài tập / thực hành <b>{meta.practice} tiết</b></span><span><i className="exam" />Kiểm tra <b>{meta.test} tiết</b></span></div>
    </div>
  </>;
}

function Slides({ lesson, files }: { lesson: (typeof lessons)[number]; files: CncLessonFile[] }) {
  const topics = "topics" in lesson && lesson.topics ? lesson.topics : [];
  const detailedContent = "lessonContent" in lesson ? lesson.lessonContent : undefined;
  return <>
    <SectionHeading icon={Presentation} kicker="MỤC 02" title="Nội dung bài học" description="Bài giảng PowerPoint và các nội dung trọng tâm của bài." />
    {files.length === 0 ? (
      <div className="cnc-file-empty"><Presentation size={28} /><div><strong>Chưa có PowerPoint</strong><p>Giảng viên chưa tải bài giảng PowerPoint cho bài học này.</p></div></div>
    ) : files.map((file, index) => (
      <article className="cnc-ppt-viewer-card" key={file.id}>
        <div className="cnc-ppt-viewer-frame">
          <iframe
            src={`https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(file.file_url)}`}
            title={`Bài giảng ${file.title}`}
            loading="lazy"
            allowFullScreen
          />
        </div>
        <div className="cnc-ppt-viewer-info">
          <div><span>{index === 0 ? "BÀI GIẢNG CHÍNH" : `BÀI GIẢNG BỔ SUNG ${index}`}</span><h3>{file.title}</h3><p>{file.file_name} · {formatFileSize(file.size_bytes)}</p></div>
          <small><CirclePlay size={14} /> Xem trực tiếp trên trang · Không cung cấp nút tải xuống</small>
        </div>
      </article>
    ))}
    {detailedContent ? <>
      <h3 className="cnc-subheading">Giáo trình nội dung chi tiết</h3>
      <div className="cnc-detailed-content">
        {detailedContent.map((section) => <article key={section.title}>
          <h4>{section.title}</h4>
          {section.paragraphs.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
          <ul>{section.bullets.map((bullet) => <li key={bullet}>{bullet}</li>)}</ul>
        </article>)}
      </div>
    </> : <>
      <h3 className="cnc-subheading">Nội dung chính</h3>
      <div className="cnc-topic-list">{topics.map((topic, i) => <div key={topic}><span>{String(i + 1).padStart(2, "0")}</span><p>{topic}</p></div>)}</div>
    </>}
  </>;
}

function Video({ lesson, videos }: { lesson: (typeof lessons)[number]; videos: CncLessonVideo[] }) {
  return <>
    <SectionHeading icon={MonitorPlay} kicker="MỤC 03" title="Video bài giảng" description={`${videos.length || "Chưa có"} video YouTube · Giảng viên Nguyễn Văn Toàn`} />
    {videos.length === 0 ? (
      <div className="cnc-file-empty"><MonitorPlay size={28} /><div><strong>Chưa có video bài giảng</strong><p>Giảng viên chưa đăng video YouTube cho bài học này.</p></div></div>
    ) : (
      <div className="cnc-video-list">
        {videos.map((video, index) => (
          <article className="cnc-video" key={video.id}>
            <div className="cnc-video-frame">
              <iframe
                src={getYouTubeEmbedUrl(video.youtube_id)}
                title={video.title}
                loading="lazy"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowFullScreen
              />
            </div>
            <div><span>VIDEO {String(index + 1).padStart(2, "0")}</span><h3>{video.title}</h3><p>{lesson.shortTitle} · Giảng viên: Nguyễn Văn Toàn</p></div>
          </article>
        ))}
      </div>
    )}
  </>;
}

function StandardTest({ lessonId, lessonTitle, onPassed, onResult, showHeading = true }: { lessonId: string; lessonTitle: string; onPassed: () => void; onResult?: (score:number,total:number,passed:boolean)=>void; showHeading?: boolean }) {
  const quiz = lessonId === "lesson-1"
    ? CNC_LESSON_1_QUIZ
    : lessonId === "lesson-2"
      ? CNC_LESSON_2_QUIZ
      : lessonId === "lesson-3"
        ? CNC_LESSON_3_QUIZ
        : null;
  const lessonNumber = lessonId.replace("lesson-", "");
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const score = quiz?.filter((question) => answers[question.id] === question.correctIndex).length ?? 0;
  const requiredScore = quiz ? Math.ceil(quiz.length * 0.8) : 0;
  const passed = submitted && score >= requiredScore;

  if (!quiz) return <>
    <SectionHeading icon={FileQuestion} kicker="MỤC 04" title="Kiểm tra cuối bài" description="Đánh giá mức độ đạt chuẩn đầu ra của bài học." />
    <div className="cnc-standard-test"><FileQuestion size={34} /><div><span>BÀI KIỂM TRA</span><h3>{lessonTitle}</h3><p>10 câu trắc nghiệm · 15 phút · Yêu cầu đạt 80%</p></div><button>Bắt đầu làm bài <ChevronRight size={16} /></button></div>
  </>;

  return <>
    {showHeading && <SectionHeading icon={FileQuestion} kicker="MỤC 04" title={`Kiểm tra cuối Bài ${lessonNumber}`} description={lessonId === "lesson-1" ? "Đề trắc nghiệm tổng quan về máy tiện, máy phay CNC." : lessonId === "lesson-2" ? "Đề trắc nghiệm lập trình tiện CNC trên hệ Fanuc 21T." : "Đề trắc nghiệm lập trình phay CNC trên hệ Fanuc 21M."} />}
    <div className="cnc-gate-banner">
      <FileQuestion size={26} />
      <div><span>BÀI KIỂM TRA KIẾN THỨC</span><h3>{lessonTitle}</h3><p><strong>20 câu trắc nghiệm</strong> · 30 phút · Đạt từ <strong>16/20 câu (80%)</strong></p></div>
      <b className={passed ? "passed" : ""}>{submitted ? `${score}/20` : "80%"}<small>{passed ? "ĐÃ ĐẠT" : "YÊU CẦU"}</small></b>
    </div>
    <div className="cnc-quiz">
      {quiz.map((question, questionIndex) => (
        <fieldset key={question.id} className={submitted && answers[question.id] !== question.correctIndex ? "wrong" : ""}>
          <legend><span>{questionIndex + 1}</span>{question.question}</legend>
          {question.options.map((option, optionIndex) => (
            <label key={option}>
              <input
                type="radio"
                name={question.id}
                checked={answers[question.id] === optionIndex}
                onChange={() => {
                  setSubmitted(false);
                  setAnswers((current) => ({ ...current, [question.id]: optionIndex }));
                }}
              />
              <i />{String.fromCharCode(65 + optionIndex)}. {option}
            </label>
          ))}
          {submitted && <p>{answers[question.id] === question.correctIndex ? "Chính xác. " : `Đáp án đúng: ${String.fromCharCode(65 + question.correctIndex)}. `}{question.explanation}</p>}
        </fieldset>
      ))}
    </div>
    <button className="cnc-submit" disabled={Object.keys(answers).length < quiz.length} onClick={() => { const didPass=score>=requiredScore; setSubmitted(true); onResult?.(score,quiz.length,didPass); if (didPass) onPassed(); }}><FileQuestion size={18} /> Nộp bài kiểm tra Bài {lessonNumber}</button>
    {submitted && <div className={`cnc-result ${passed ? "passed" : ""}`}>{passed ? `Đạt — Bạn trả lời đúng ${score}/20 câu và đã hoàn thành bài kiểm tra.` : `Chưa đạt — Bạn trả lời đúng ${score}/20 câu. Cần ít nhất 16 câu đúng; hãy xem giải thích và làm lại.`}</div>}
  </>;
}

function ProgrammingTestSuite({ lessonId, lessonTitle, courseId, onPassed, onResult }: { lessonId: "lesson-2" | "lesson-3"; lessonTitle: string; courseId?: number; onPassed: () => void; onResult?: (assessmentId:string,score:number,total:number,passed:boolean)=>void }) {
  const [level, setLevel] = useState<"exercise-1"|"exercise-2"|"exercise-3"|"exercise-4"|"exercise-5">("exercise-1");
  const levels = [
    { id: "exercise-1" as const, name: "Bài tập 1", note: "Nhận biết câu lệnh · 20 câu" },
    { id: "exercise-2" as const, name: "Bài tập 2", note: "Đọc hiểu và dịch block lệnh" },
    { id: "exercise-3" as const, name: "Bài tập 3", note: "Điền khuyết chương trình" },
    { id: "exercise-4" as const, name: "Bài tập 4", note: "Viết chương trình từ bản vẽ" },
    { id: "exercise-5" as const, name: "Bài tập 5", note: "Mô phỏng và kiểm chứng" },
  ];
  return <div className="cnc-programming-suite space-y-5">
    <SectionHeading icon={FileQuestion} kicker="BỘ 5 BÀI TẬP LẬP TRÌNH CNC" title={`Kiểm tra ${lessonTitle}`} description="Từ nhận biết câu lệnh đến viết, mô phỏng và kiểm chứng chương trình NC." />
    <div className="cnc-programming-tabs grid gap-2 sm:grid-cols-2 xl:grid-cols-5">{levels.map((item)=><button key={item.id} type="button" onClick={()=>setLevel(item.id)} className={`rounded-xl border p-3 text-left transition ${level===item.id?"active border-[#e85d24] bg-[#fff2ec] text-[#b94317]":"border-[#dfe4e8] bg-white text-[#52616d] hover:border-[#efb399]"}`}><strong className="block text-xs">{item.name}</strong><small className="mt-1 block text-[10px] opacity-70">{item.note}</small></button>)}</div>
    {level === "exercise-1" && <StandardTest lessonId={lessonId} lessonTitle={lessonTitle} onPassed={onPassed} onResult={(score,total,passed)=>onResult?.("exercise-1",score,total,passed)} showHeading={false} />}
    {level === "exercise-2" && <CommandTranslationChallenge machine={lessonId === "lesson-2" ? "turn" : "mill"} onResult={(score,total,passed)=>onResult?.("exercise-2",score,total,passed)} />}
    {level === "exercise-3" && <FillBlankNcExercise machine={lessonId === "lesson-2" ? "turn" : "mill"} onResult={(score,total,passed)=>onResult?.("exercise-3",score,total,passed)} />}
    {level === "exercise-4" && <ProgramFromDrawingExercise machine={lessonId === "lesson-2" ? "turn" : "mill"} onResult={(score,total,passed)=>onResult?.("exercise-4",score,total,passed)} />}
    {level === "exercise-5" && <SimulationEvidenceExercise machine={lessonId === "lesson-2" ? "turn" : "mill"} lessonId={`${lessonId}-simulation`} lessonTitle={`Mô phỏng ${lessonTitle}`} courseId={courseId} onApproved={()=>onResult?.("exercise-5",100,100,true)} />}
  </div>;
}

function CommandTranslationChallenge({machine,onResult}:{machine:"turn"|"mill";onResult?: (score:number,total:number,passed:boolean)=>void}) {
  const [choice,setChoice]=useState(""); const [checked,setChecked]=useState(false); const command=machine==="turn"?"G01 X30 Z-25 F0.20":"G02 X50 Y30 R15 F200";
  const correct=machine==="turn"?"turn-translate":"mill-translate";
  if (machine === "mill") return <MillingCommandTranslationQuiz onResult={onResult} />;
  if (machine === "turn") return <TurningCommandTranslationQuiz onResult={onResult} />;
  return <div className="rounded-2xl border border-[#dfe4e8] bg-white p-5"><span className="text-[10px] font-black tracking-[.15em] text-[#e85d24]">DẠNG 2 · DỊCH LỆNH</span><h3 className="mt-2 text-lg font-extrabold text-[#17232c]">Dịch câu lệnh sang ngôn ngữ công nghệ</h3><pre className="mt-4 rounded-xl bg-[#101820] p-5 text-center font-mono text-xl font-bold text-[#b9f6d0]">{command}</pre><div className="mt-4 grid gap-2">{machine==="turn"?<><label className="rounded-xl border border-[#dfe4e8] p-3 text-sm text-[#52616d]"><input type="radio" name="translate-turn" value="turn-translate" onChange={(event)=>{setChoice(event.target.value);setChecked(false)}}/> Tiện thẳng đến X30, Z−25 với lượng chạy dao 0,20 mm/vòng</label><label className="rounded-xl border border-[#dfe4e8] p-3 text-sm text-[#52616d]"><input type="radio" name="translate-turn" value="rapid" onChange={(event)=>{setChoice(event.target.value);setChecked(false)}}/> Chạy nhanh đến X30, Z−25</label></>:<><label className="rounded-xl border border-[#dfe4e8] p-3 text-sm text-[#52616d]"><input type="radio" name="translate-mill" value="mill-translate" onChange={(event)=>{setChoice(event.target.value);setChecked(false)}}/> Nội suy cung tròn chiều kim đồng hồ đến X50 Y30, bán kính 15, F200</label><label className="rounded-xl border border-[#dfe4e8] p-3 text-sm text-[#52616d]"><input type="radio" name="translate-mill" value="line" onChange={(event)=>{setChoice(event.target.value);setChecked(false)}}/> Phay đường thẳng đến X50 Y30</label></>}</div><button type="button" disabled={!choice} onClick={()=>setChecked(true)} className="mt-3 rounded-full bg-[#e85d24] px-5 py-2.5 text-sm font-bold text-white disabled:opacity-40">Kiểm tra bản dịch</button>{checked&&<p className={`mt-3 rounded-xl p-3 text-sm ${choice===correct?"bg-emerald-50 text-emerald-700":"bg-red-50 text-red-700"}`}>{choice===correct?"Chính xác — bản dịch thể hiện đủ dạng chuyển động, tọa độ và lượng chạy dao.":"Chưa đúng — cần dịch đầy đủ mã G, tọa độ đích và thông số F/R."}</p>}</div>;
}

function TurningCommandTranslationQuiz({onResult}:{onResult?: (score:number,total:number,passed:boolean)=>void}){
  const quiz=CNC_TURN_COMMAND_TRANSLATION_QUIZ;const[answers,setAnswers]=useState<Record<string,number>>({});const[submitted,setSubmitted]=useState(false);const score=quiz.filter(question=>answers[question.id]===question.correctIndex).length;const required=Math.ceil(quiz.length*.8);const passed=submitted&&score>=required;
  return <><div className="cnc-gate-banner"><FileQuestion size={26}/><div><span>DẠNG 2 · DỊCH LỆNH</span><h3>Dịch block G-code/M-code tiện CNC</h3><p><strong>20 câu trắc nghiệm</strong> · Đạt từ <strong>16/20 câu (80%)</strong></p></div><b className={passed?"passed":""}>{submitted?`${score}/20`:"80%"}<small>{passed?"ĐÃ ĐẠT":"YÊU CẦU"}</small></b></div><div className="cnc-quiz">{quiz.map((question,index)=><fieldset key={question.id} className={submitted&&answers[question.id]!==question.correctIndex?"wrong":""}><legend><span>{index+1}</span><code>{question.question}</code></legend>{question.options.map((option,optionIndex)=><label key={option}><input type="radio" name={question.id} checked={answers[question.id]===optionIndex} onChange={()=>{setSubmitted(false);setAnswers(current=>({...current,[question.id]:optionIndex}))}}/><i/>{String.fromCharCode(65+optionIndex)}. {option}</label>)}{submitted&&<p>{answers[question.id]===question.correctIndex?"Chính xác. ":`Đáp án đúng: ${String.fromCharCode(65+question.correctIndex)}. `}{question.explanation}</p>}</fieldset>)}</div><button className="cnc-submit" disabled={Object.keys(answers).length<quiz.length} onClick={()=>{setSubmitted(true);onResult?.(score,quiz.length,score>=required)}}><FileQuestion size={18}/>Nộp bài Dạng 2</button>{submitted&&<div className={`cnc-result ${passed?"passed":""}`}>{passed?`Đạt — Bạn trả lời đúng ${score}/20 câu.`:`Chưa đạt — Bạn trả lời đúng ${score}/20 câu. Cần ít nhất 16 câu đúng.`}</div>}</>;
}

function MillingCommandTranslationQuiz({onResult}:{onResult?: (score:number,total:number,passed:boolean)=>void}) {
  const quiz = CNC_MILL_COMMAND_TRANSLATION_QUIZ;
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const score = quiz.filter((question) => answers[question.id] === question.correctIndex).length;
  const requiredScore = Math.ceil(quiz.length * 0.8);
  const passed = submitted && score >= requiredScore;

  return <>
    <div className="cnc-gate-banner">
      <FileQuestion size={26} />
      <div><span>DẠNG 2 · DỊCH LỆNH G-CODE</span><h3>Dịch câu lệnh sang ngôn ngữ công nghệ</h3><p><strong>20 câu trắc nghiệm</strong> · Đạt từ <strong>16/20 câu (80%)</strong></p></div>
      <b className={passed ? "passed" : ""}>{submitted ? `${score}/20` : "80%"}<small>{passed ? "ĐÃ ĐẠT" : "YÊU CẦU"}</small></b>
    </div>
    <div className="cnc-quiz">
      {quiz.map((question, questionIndex) => (
        <fieldset key={question.id} className={submitted && answers[question.id] !== question.correctIndex ? "wrong" : ""}>
          <legend><span>{questionIndex + 1}</span><code>{question.question}</code></legend>
          {question.options.map((option, optionIndex) => (
            <label key={option}>
              <input type="radio" name={question.id} checked={answers[question.id] === optionIndex} onChange={() => { setSubmitted(false); setAnswers((current) => ({ ...current, [question.id]: optionIndex })); }} />
              <i />{String.fromCharCode(65 + optionIndex)}. {option}
            </label>
          ))}
          {submitted && <p>{answers[question.id] === question.correctIndex ? "Chính xác. " : `Đáp án đúng: ${String.fromCharCode(65 + question.correctIndex)}. `}{question.explanation}</p>}
        </fieldset>
      ))}
    </div>
    <button className="cnc-submit" disabled={Object.keys(answers).length < quiz.length} onClick={() => {setSubmitted(true);onResult?.(score,quiz.length,score>=requiredScore);}}><FileQuestion size={18} /> Nộp bài Dạng 2</button>
    {submitted && <div className={`cnc-result ${passed ? "passed" : ""}`}>{passed ? `Đạt — Bạn trả lời đúng ${score}/20 câu.` : `Chưa đạt — Bạn trả lời đúng ${score}/20 câu. Cần ít nhất 16 câu đúng; hãy xem giải thích và làm lại.`}</div>}
  </>;
}

function FillBlankNcExercise({machine,onResult}:{machine:"turn"|"mill";onResult?:(score:number,total:number,passed:boolean)=>void}){
  return machine==="turn"?<TurningFillBlankExercise onResult={onResult}/>:<MillingFillBlankExercise onResult={onResult}/>;
}

function MillingFillBlankExercise({onResult}:{onResult?:(score:number,total:number,passed:boolean)=>void}){
  const exercise=millingExercises.exercises[0] as {title:string;levels:(FillLevel&{level:string})[]};
  const[level,setLevel]=useState<"de"|"kho">("de");
  const selected=exercise.levels.find(item=>item.level===level)??exercise.levels[0];
  const imageMap:{[key:string]:string}={"de":"/images/cnc/phay_bai3_de.png","kho":"/images/cnc/phay_bai3_kho.png"};
  return <div className="rounded-2xl border border-[#dfe4e8] bg-white p-5"><span className="text-[10px] font-black tracking-[.15em] text-[#e85d24]">BÀI TẬP 3 · ĐIỀN KHUYẾT CHƯƠNG TRÌNH</span><h3 className="mt-2 text-lg font-extrabold text-[#17232c]">{exercise.title}</h3><p className="mt-2 text-sm text-[#71808c]">Quan sát bản vẽ và thông số công nghệ, sau đó điền các giá trị còn thiếu trong chương trình.</p><div className="mt-5 overflow-hidden rounded-2xl border border-[#dfe4e8] bg-white"><Image src={imageMap[level]} alt="Bản vẽ chi tiết milling exercise" width={1048} height={956} className="h-auto w-full" unoptimized priority/></div><LevelPicker value={level} onChange={setLevel}/><FillBlankLevel key={`mill-${level}`} level={selected} onResult={onResult}/></div>;
}

const turningFillBlankProgram=[
  "O0001",
  "N5   G90 G71 G18 G95;",
  "N10  T___[B1]___;",
  "N15  M3 S___[B2]___;",
  "N20  G0 X___[B3]___ Z0;",
  "N25  G1 X-1 Z0 F___[B4]___;",
  "N30  G0 X20 Z___[B5]___;",
  "N35  G73 U___[B6]___ R___[B7]___;",
  "N40  G73 P___[B8]___ Q___[B9]___ U0.5 W0.5;",
  "N45  G0 G41 X10 Z5;",
  "N50  G1 X10 Z0;",
  "N55  G1 X10 Z-___[B10]___;",
  "N60  G1 X___[B11]___ Z-15;",
  "N65  G1 X16 Z-___[B12]___;",
  "N70  G1 X___[B13]___ Z-25;",
  "N75  G0 G40 X40;",
  "N80  G0 Z20;",
  "N85  T___[B14]___;",
  "N90  M3 S___[B15]___ F0.1;",
  "N95  G0 G41 X20 Z5;",
  "N100 G72 P50 Q70;",
  "N105 G0 G40 X40;",
  "N110 G0 Z20;",
  "N115 M30;",
  "%",
];

const turningFillBlankAnswers=[
  {id:"B1",answer:"0202",note:"Dao tiện thô T0202."},{id:"B2",answer:"800",note:"Tốc độ tiện thô n₁ = 800 vòng/phút."},{id:"B3",answer:"22",note:"Đường kính tiếp cận lớn hơn phôi Ø20."},{id:"B4",answer:"0.2",note:"Lượng chạy dao tiện thô S₁ = 0,2 mm/vòng."},{id:"B5",answer:"5",note:"Điểm tiếp cận cách mặt đầu Z5."},{id:"B6",answer:"1",note:"Chiều sâu mỗi lát cắt thô t₁ = 1 mm."},{id:"B7",answer:"1",note:"Khoảng lùi dao của chu trình G73."},{id:"B8",answer:"45",note:"Block bắt đầu biên dạng là N45."},{id:"B9",answer:"70",note:"Block kết thúc biên dạng là N70."},{id:"B10",answer:"3",note:"P2 nằm tại Z-3."},{id:"B11",answer:"16",note:"Đường kính đoạn côn kết thúc là Ø16."},{id:"B12",answer:"25",note:"P4 nằm tại Z-25."},{id:"B13",answer:"20",note:"Đường kính bậc cuối là Ø20."},{id:"B14",answer:"0404",note:"Dao tiện tinh T0404."},{id:"B15",answer:"1000",note:"Tốc độ tiện tinh n₂ = 1000 vòng/phút."},
];

function TurningFillBlankExercise({onResult}:{onResult?:(score:number,total:number,passed:boolean)=>void}){return <div className="rounded-2xl border border-[#dfe4e8] bg-white p-5"><span className="text-[10px] font-black tracking-[.15em] text-[#e85d24]">BÀI TẬP 3 · ĐIỀN KHUYẾT CHƯƠNG TRÌNH TIỆN</span><h3 className="mt-2 text-lg font-extrabold text-[#17232c]">Hoàn thành chương trình gia công trục bậc – côn</h3><p className="mt-2 text-sm text-[#71808c]">Quan sát bản vẽ và thông số công nghệ, sau đó điền các giá trị còn thiếu trong chương trình.</p><div className="mt-5 overflow-hidden rounded-2xl border border-[#dfe4e8] bg-white"><Image src="/images/cnc/bai-3-tien-dien-khuyet.png" alt="Bản vẽ chi tiết tiện trục bậc và côn" width={1054} height={876} className="h-auto w-full" unoptimized priority/></div><div className="mt-4 grid gap-3 sm:grid-cols-2"><div className="rounded-xl border border-orange-100 bg-orange-50 p-4"><strong className="text-sm text-[#17232c]">Tiện thô</strong><ul className="mt-2 space-y-1 text-sm text-[#52616d]"><li>Dao T0202 · n₁ = 800 vòng/phút</li><li>S₁ = 0,2 mm/vòng · t₁ = 1 mm</li></ul></div><div className="rounded-xl border border-cyan-100 bg-cyan-50 p-4"><strong className="text-sm text-[#17232c]">Tiện tinh</strong><ul className="mt-2 space-y-1 text-sm text-[#52616d]"><li>Dao T0404 · n₂ = 1000 vòng/phút</li><li>S₂ = 0,1 mm/vòng · t₂ = 0,5 mm</li></ul></div></div><FillBlankLevel level={{part_ref:"Phôi Ø20 dài 60 mm; biên dạng Ø10 × 3, côn đến Ø16 tại Z-15 và đoạn Ø16 đến Z-25.",part_image_note:"Gốc W đặt tại tâm mặt đầu chi tiết, Z0 ở mặt đầu bên phải.",program_with_blanks:turningFillBlankProgram,blanks:turningFillBlankAnswers}} onResult={onResult}/></div>}

function InputBlank({id,values,setValues}:{id:string;values:Record<string,string>;setValues:React.Dispatch<React.SetStateAction<Record<string,string>>>}){return <input aria-label={`Giá trị ${id}`} value={values[id]??""} onChange={event=>setValues(current=>({...current,[id]:event.target.value}))} className="mx-1 inline-block w-16 rounded border border-cyan-300/30 bg-white/10 px-2 py-1 text-center text-white outline-none focus:border-cyan-300"/>}

type FillLevel={part_ref:string;part_image_note:string;program_with_blanks:string[];blanks:{id:string;answer:string;note:string}[]};
function FillBlankLevel({level,onResult}:{level:FillLevel;onResult?:(score:number,total:number,passed:boolean)=>void}){const[values,setValues]=useState<Record<string,string>>({});const[submitted,setSubmitted]=useState(false);const normalized=(value:string)=>value.trim().toUpperCase().replace(/^G(?=\d)/,"");const score=level.blanks.filter(item=>normalized(values[item.id]??"")===normalized(item.answer)).length;return <><div className="mt-4 rounded-xl border border-orange-100 bg-orange-50 p-4"><strong className="text-sm text-[#17232c]">Chi tiết gia công</strong><p className="mt-1 text-sm text-[#52616d]">{level.part_ref}</p><small className="mt-2 block text-[#8a6b5d]">Gợi ý bản vẽ: {level.part_image_note}</small></div><div className="mt-4 overflow-x-auto rounded-xl bg-[#101820] p-5 font-mono text-sm leading-9 text-[#b9f6d0]">{level.program_with_blanks.map((line,index)=><div key={index} className="whitespace-nowrap">{line.split(/___\[([^\]]+)\]___/g).map((part,i)=>i%2?<InputBlank key={part} id={part} values={values} setValues={setValues}/>:<span key={i}>{part}</span>)}</div>)}</div><button className="mt-4 rounded-full bg-[#e85d24] px-5 py-2.5 text-sm font-bold text-white disabled:opacity-40" disabled={Object.keys(values).length<level.blanks.length} onClick={()=>{setSubmitted(true);onResult?.(score,level.blanks.length,score===level.blanks.length)}}>Kiểm tra {level.blanks.length} ô trống</button>{submitted&&<div className={`mt-3 rounded-xl p-4 text-sm ${score===level.blanks.length?"bg-emerald-50 text-emerald-700":"bg-amber-50 text-amber-800"}`}><strong>{score===level.blanks.length?"Đạt — Tất cả giá trị đều chính xác.":`Đúng ${score}/${level.blanks.length} ô.`}</strong>{score<level.blanks.length&&<ul className="mt-2 list-disc space-y-1 pl-5">{level.blanks.filter(item=>normalized(values[item.id]??"")!==normalized(item.answer)).map(item=><li key={item.id}>{item.id}: {item.note}</li>)}</ul>}</div>}</>}

function LevelPicker({value,onChange}:{value:"de"|"kho";onChange:(value:"de"|"kho")=>void}){return <div className="mt-4 inline-flex rounded-xl bg-[#f1f4f6] p-1"><button type="button" onClick={()=>onChange("de")} className={`rounded-lg px-4 py-2 text-sm font-bold ${value==="de"?"bg-white text-[#e85d24] shadow-sm":"text-[#71808c]"}`}>Mức dễ</button><button type="button" onClick={()=>onChange("kho")} className={`rounded-lg px-4 py-2 text-sm font-bold ${value==="kho"?"bg-white text-[#e85d24] shadow-sm":"text-[#71808c]"}`}>Mức khó</button></div>}

type ProgramLevel={part_ref:string;image?:string;required_elements:string[];expected_key_coordinates:{point:string;X:number;Y?:number;Z?:number}[];teacher_rubric:{criterion:string;weight:string}[]};
function ProgramFromDrawingExercise({machine,onResult}:{machine:"turn"|"mill";onResult?:(score:number,total:number,passed:boolean)=>void}){const exercise=(machine==="turn"?turningExercises:millingExercises).exercises[1] as {title:string;levels:(ProgramLevel&{level:string})[]};const[level,setLevel]=useState<"de"|"kho">("de");const selected=exercise.levels.find(item=>item.level===level)??exercise.levels[0];return <div className="rounded-2xl border border-[#dfe4e8] bg-white p-5"><span className="text-[10px] font-black tracking-[.15em] text-[#e85d24]">BÀI TẬP 4 · VIẾT CHƯƠNG TRÌNH TỪ BẢN VẼ</span><h3 className="mt-2 text-lg font-extrabold text-[#17232c]">{exercise.title}</h3>{selected.image&&<div className="mt-5 overflow-hidden rounded-2xl border border-[#dfe4e8] bg-white"><Image src={selected.image} alt="Bản vẽ chi tiết bài tập 4" width={1876} height={1580} className="h-auto w-full" unoptimized priority/></div>}{exercise.levels.length>1&&<LevelPicker value={level} onChange={setLevel}/>}<ProgramLevelChallenge key={`${machine}-${level}`} machine={machine} level={selected} onResult={onResult}/></div>}

function ProgramLevelChallenge({machine,level,onResult}:{machine:"turn"|"mill";level:ProgramLevel;onResult?:(score:number,total:number,passed:boolean)=>void}){const[code,setCode]=useState(machine==="turn"?"G90 G95 G18\nT0202\n":"G21 G90 G94 G17\nG54\nT01 M06\nG43 H01 Z50\n");const[result,setResult]=useState<string[]|null>(null);function check(){const value=code.toUpperCase().replace(/\s+/g," ");const tests:[boolean,string][]=[[machine==="mill"?value.includes("G54"):true,"Thiếu khai báo gốc phôi G54"],[/M0?3/.test(value),"Thiếu lệnh quay trục chính M03"],[/M0?5/.test(value),"Thiếu lệnh dừng trục chính M05"],[/M0?30/.test(value),"Thiếu lệnh kết thúc M30"],...level.expected_key_coordinates.map(point=>{const coords=[`X${point.X}`,point.Y!==undefined?`Y${point.Y}`:`Z${point.Z}`];return [coords.every(coord=>new RegExp(`${coord.replace("-","\\-")}(?:\\.0+)?(?:[\\s;]|$)`).test(value)),`Thiếu hoặc sai tọa độ ${point.point}: ${coords.join(" ")}`] as [boolean,string]})];if(machine==="turn")tests.push([/T0?202/.test(value),"Thiếu dao tiện thô T0202"],[/T0?404/.test(value),"Thiếu dao tiện tinh T0404"],[/G95/.test(value),"Thiếu chế độ chạy dao G95 (mm/vòng)"],[/G(?:73|71|0?1)/.test(value),"Thiếu chu trình G73/G71 hoặc nội suy G01"]);else tests.push([/T0?1\s+M0?6/.test(value),"Thiếu T01 M06"],[/G43\s+H0?1/.test(value),"Thiếu bù chiều dài G43 H01"],[/G4[12]/.test(value),"Thiếu bù bán kính G41/G42"],[/G40/.test(value),"Thiếu hủy bù bán kính G40"]);if(level.part_ref.includes("ren"))tests.push([/T0?202/.test(value),"Thiếu dao tiện ren T0202"],[/G(?:92|76)/.test(value),"Thiếu chu trình tiện ren G92/G76"],[/F1(?:\.5|,5)/.test(value),"Sai hoặc thiếu bước ren F1.5"]);if(level.part_ref.includes("cung"))tests.push([/G0?[23]/.test(value),"Thiếu nội suy cung G02/G03"],[/(?:I|J|R)-?\d/.test(value),"Thiếu thông số I, J hoặc R"]);const missing=tests.filter(([ok])=>!ok).map(([,message])=>message);setResult(missing);onResult?.(tests.length-missing.length,tests.length,missing.length===0)}return <div className="mt-4 grid gap-5 lg:grid-cols-[.9fr_1.1fr]"><div><div className="rounded-xl bg-orange-50 p-4"><strong className="text-sm text-[#17232c]">Đề bài</strong><p className="mt-1 text-sm text-[#52616d]">{level.part_ref}</p></div><h4 className="mt-4 font-bold text-[#17232c]">Các yêu cầu cần đạt</h4><ul className="mt-2 list-disc space-y-2 pl-5 text-sm text-[#52616d]">{level.required_elements.map(item=><li key={item}>{item}</li>)}</ul><h4 className="mt-4 font-bold text-[#17232c]">Rubric giáo viên</h4>{level.teacher_rubric.map(item=><div key={item.criterion} className="mt-2 flex justify-between gap-3 border-b border-[#edf0f2] pb-2 text-xs text-[#52616d]"><span>{item.criterion}</span><strong>{item.weight}</strong></div>)}</div><div className="rounded-2xl bg-[#101820] p-5"><span className="text-[10px] font-black tracking-[.15em] text-[#67e8f9]">NC CODE CHECKER · {machine==="turn"?"FANUC 21T":"FANUC 21M"}</span><textarea value={code} onChange={event=>{setCode(event.target.value);setResult(null)}} spellCheck={false} className="mt-4 min-h-96 w-full rounded-xl border border-white/10 bg-[#080d12] p-4 font-mono text-sm leading-7 text-[#b9f6d0]"/><button type="button" onClick={check} className="mt-3 rounded-full bg-[#e85d24] px-5 py-2.5 text-sm font-bold text-white">Kiểm tra chương trình</button>{result&&<div className={`mt-3 rounded-xl p-4 text-sm ${result.length===0?"bg-emerald-500/15 text-emerald-200":"bg-amber-500/15 text-amber-100"}`}>{result.length===0?<strong>Đạt — Chương trình đáp ứng đầy đủ tiêu chí tự động.</strong>:<><strong>Còn {result.length} tiêu chí cần sửa:</strong><ul className="mt-2 list-disc space-y-1 pl-5">{result.map(item=><li key={item}>{item}</li>)}</ul></>}</div>}</div></div>}

function SimulationEvidenceExercise({machine,...props}:{machine:"turn"|"mill";lessonId:string;lessonTitle:string;courseId?:number;onApproved:(lessonId:string)=>void}){const exercise=(machine==="turn"?turningExercises:millingExercises).exercises[2];return <div><div className="mb-5 rounded-2xl border border-[#dfe4e8] bg-white p-5"><span className="text-[10px] font-black tracking-[.15em] text-[#e85d24]">BÀI TẬP 5 · MÔ PHỎNG VÀ KIỂM CHỨNG</span><h3 className="mt-2 text-lg font-extrabold text-[#17232c]">{exercise.title}</h3><p className="mt-2 text-sm leading-6 text-[#52616d]">{exercise.instructions}</p><h4 className="mt-4 font-bold text-[#17232c]">Hồ sơ cần nộp</h4><ul className="mt-2 list-disc space-y-2 pl-5 text-sm text-[#52616d]">{exercise.submission_requirements?.map(item=><li key={item}>{item}</li>)}</ul><h4 className="mt-4 font-bold text-[#17232c]">Rubric chấm của giáo viên</h4>{exercise.teacher_rubric?.map(item=><div key={item.criterion} className="mt-2 flex justify-between gap-3 border-b border-[#edf0f2] pb-2 text-xs text-[#52616d]"><span>{item.criterion}</span><strong>{item.weight}</strong></div>)}</div><DrawingSubmissionTest {...props}/></div>}

function MillingDrawingCodeChallenge({onResult}:{onResult?:(score:number,total:number,passed:boolean)=>void}) {
  const starter="G21 G17 G90 G54\nT01 M06\nS1500 M03\nG00 X0 Y0 Z5\nG01 Z-2 F100\n";
  const [code,setCode]=useState(starter); const [result,setResult]=useState<string[]|null>(null);
  function checkCode(){const value=code.toUpperCase().replace(/\s+/g," ");const checks=[[/G21/,"Thiếu khai báo hệ mét G21"],[/G90/,"Thiếu chế độ tuyệt đối G90"],[/G54/,"Thiếu gốc phôi G54"],[/M0?3/,"Thiếu lệnh quay trục chính M03"],[/X60(?:\.0+)?\s+Y0(?:\.0+)?/,"Chưa đi đến điểm X60 Y0"],[/X60(?:\.0+)?\s+Y40(?:\.0+)?/,"Chưa đi đến điểm X60 Y40"],[/X0(?:\.0+)?\s+Y40(?:\.0+)?/,"Chưa đi đến điểm X0 Y40"],[/X0(?:\.0+)?\s+Y0(?:\.0+)?/,"Chưa khép kín biên dạng tại X0 Y0"],[/M30/,"Thiếu lệnh kết thúc M30"]] as const;const missing=checks.filter(([pattern])=>!pattern.test(value)).map(([,message])=>message);setResult(missing);onResult?.(checks.length-missing.length,checks.length,missing.length===0);}
  return <div className="grid gap-5 lg:grid-cols-[.9fr_1.1fr]"><div className="rounded-2xl border border-[#dfe4e8] bg-white p-5"><span className="text-[10px] font-black tracking-[.15em] text-[#e85d24]">DẠNG 3 · VIẾT CHƯƠNG TRÌNH TỪ BẢN VẼ</span><h3 className="mt-2 text-lg font-extrabold text-[#17232c]">Phay biên dạng chữ nhật 60 × 40</h3><p className="mt-2 text-sm text-[#71808c]">Gốc phôi tại góc trái dưới; chiều sâu Z = −2 mm. Viết quỹ đạo theo chiều kim đồng hồ.</p><svg viewBox="0 0 360 260" className="mt-4 w-full rounded-xl bg-[#f5f7f8]" role="img" aria-label="Bản vẽ phay hình chữ nhật 60 nhân 40 milimét"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#71808c"/></marker></defs><rect x="80" y="55" width="210" height="140" fill="#fff" stroke="#17232c" strokeWidth="4"/><circle cx="80" cy="195" r="6" fill="#e85d24"/><text x="54" y="220" fill="#e85d24" fontSize="13" fontWeight="700">G54 (0,0)</text><line x1="80" y1="225" x2="290" y2="225" stroke="#71808c" markerStart="url(#arrow)" markerEnd="url(#arrow)"/><text x="175" y="248" fill="#52616d" fontSize="14">60 mm</text><line x1="320" y1="55" x2="320" y2="195" stroke="#71808c" markerStart="url(#arrow)" markerEnd="url(#arrow)"/><text x="330" y="130" fill="#52616d" fontSize="14" transform="rotate(90 330 130)">40 mm</text></svg></div><div className="rounded-2xl border border-[#283745] bg-[#101820] p-5"><div className="flex items-center justify-between"><div><span className="text-[10px] font-black tracking-[.15em] text-[#67e8f9]">NC CODE CHECKER · THỬ NGHIỆM</span><h3 className="mt-1 text-lg font-bold text-white">Nhập chương trình FANUC 21M</h3></div><span className="rounded-full bg-white/10 px-3 py-1 text-xs text-slate-300">9 tiêu chí</span></div><textarea value={code} onChange={(event)=>{setCode(event.target.value);setResult(null)}} spellCheck={false} className="mt-4 min-h-72 w-full rounded-xl border border-white/10 bg-[#080d12] p-4 font-mono text-sm leading-7 text-[#b9f6d0]"/><button type="button" onClick={checkCode} className="mt-3 rounded-full bg-[#e85d24] px-5 py-2.5 text-sm font-bold text-white">Kiểm tra chương trình</button>{result&&<div className={`mt-3 rounded-xl p-4 text-sm ${result.length===0?"bg-emerald-500/15 text-emerald-200":"bg-amber-500/15 text-amber-100"}`}>{result.length===0?<strong>Đạt — Chương trình có đủ lệnh và đi qua đúng 4 đỉnh của biên dạng.</strong>:<><strong>Còn {result.length} tiêu chí cần sửa:</strong><ul className="mt-2 list-disc space-y-1 pl-5">{result.map((item)=><li key={item}>{item}</li>)}</ul></>}</div>}</div></div>;
}

function TurningDrawingCodeChallenge({onResult}:{onResult?:(score:number,total:number,passed:boolean)=>void}){const starter="G21 G90\nT0101\nG97 S1200 M03\nG00 X42 Z2\n";const[code,setCode]=useState(starter);const[result,setResult]=useState<string[]|null>(null);function checkCode(){const value=code.toUpperCase().replace(/\s+/g," ");const checks=[[/G21/,"Thiếu G21"],[/G90/,"Thiếu G90"],[/T0?101/,"Thiếu gọi dao T0101"],[/M0?3/,"Thiếu M03"],[/X40(?:\.0+)?\s+Z0(?:\.0+)?/,"Chưa đến điểm X40 Z0"],[/X30(?:\.0+)?\s+Z-20(?:\.0+)?/,"Chưa tiện đến X30 Z−20"],[/X40(?:\.0+)?\s+Z-35(?:\.0+)?/,"Chưa tạo bậc X40 Z−35"],[/M30/,"Thiếu M30"]] as const;const missing=checks.filter(([pattern])=>!pattern.test(value)).map(([,message])=>message);setResult(missing);onResult?.(checks.length-missing.length,checks.length,missing.length===0);}return <div className="grid gap-5 lg:grid-cols-[.9fr_1.1fr]"><div className="rounded-2xl border border-[#dfe4e8] bg-white p-5"><span className="text-[10px] font-black tracking-[.15em] text-[#e85d24]">DẠNG 3 · VIẾT CHƯƠNG TRÌNH TỪ BẢN VẼ</span><h3 className="mt-2 text-lg font-extrabold text-[#17232c]">Tiện trục bậc Ø40/Ø30</h3><p className="mt-2 text-sm text-[#71808c]">Gốc Z0 tại mặt đầu; đoạn Ø30 dài 20 mm, tổng chiều dài 35 mm.</p><svg viewBox="0 0 380 240" className="mt-4 w-full rounded-xl bg-[#f5f7f8]" role="img" aria-label="Bản vẽ tiện trục bậc đường kính 40 và 30"><path d="M55 60 H300 V90 H210 V150 H300 V180 H55 Z" fill="#fff" stroke="#17232c" strokeWidth="4"/><line x1="55" y1="120" x2="325" y2="120" stroke="#94a0a9" strokeDasharray="7 5"/><text x="220" y="82" fill="#52616d" fontSize="14">Ø40</text><text x="120" y="112" fill="#e85d24" fontSize="14">Ø30 × 20</text><text x="210" y="215" fill="#52616d" fontSize="14">L = 35 mm</text><circle cx="300" cy="120" r="5" fill="#e85d24"/><text x="306" y="115" fill="#e85d24" fontSize="12">Z0</text></svg></div><div className="rounded-2xl border border-[#283745] bg-[#101820] p-5"><span className="text-[10px] font-black tracking-[.15em] text-[#67e8f9]">NC CODE CHECKER · FANUC 21T</span><h3 className="mt-1 text-lg font-bold text-white">Nhập chương trình tiện</h3><textarea value={code} onChange={(event)=>{setCode(event.target.value);setResult(null)}} spellCheck={false} className="mt-4 min-h-72 w-full rounded-xl border border-white/10 bg-[#080d12] p-4 font-mono text-sm leading-7 text-[#b9f6d0]"/><button type="button" onClick={checkCode} className="mt-3 rounded-full bg-[#e85d24] px-5 py-2.5 text-sm font-bold text-white">Kiểm tra chương trình</button>{result&&<div className={`mt-3 rounded-xl p-4 text-sm ${result.length===0?"bg-emerald-500/15 text-emerald-200":"bg-amber-500/15 text-amber-100"}`}>{result.length===0?<strong>Đạt — chương trình đi qua đủ các điểm biên dạng trục bậc.</strong>:<><strong>Còn {result.length} tiêu chí cần sửa:</strong><ul className="mt-2 list-disc space-y-1 pl-5">{result.map((item)=><li key={item}>{item}</li>)}</ul></>}</div>}</div></div>}

type QuizQuestion={id:string;question:string;options:string[];correctIndex:number;explanation:string};
type SafetyQuiz=QuizQuestion[];

function OperationTestSuite({machine,courseId,onResult,onCompleted}:{machine:"tiện"|"phay";courseId?:number;onResult:(assessmentId:string,score:number,total:number,passed:boolean)=>void;onCompleted:()=>void}){
  const[active,setActive]=useState<"machine-operation"|"tool-setup">("machine-operation");
  const[passedParts,setPassedParts]=useState<Record<string,boolean>>({});
  const operationQuiz:SafetyQuiz=machine==="tiện"?operationTurnQuiz:operationMillQuiz;
  const toolQuiz:SafetyQuiz=machine==="tiện"?toolSetupTurnQuiz:toolSetupMillQuiz;
  function recordPart(assessmentId:string,value:number,total:number,didPass:boolean){onResult(assessmentId,value,total,didPass);if(!didPass)return;const next={...passedParts,[assessmentId]:true};setPassedParts(next);if(next["machine-operation"]&&next["tool-setup"])onCompleted()}
  return <div className="space-y-5"><SectionHeading icon={ShieldCheck} kicker={`KIỂM TRA VẬN HÀNH MÁY ${machine.toUpperCase()}`} title="Hai bài kiểm tra kỹ năng vận hành" description="Hoàn thành riêng bài vận hành máy và bài cài đặt dao; điểm từng bài được lưu độc lập."/><div className="grid gap-3 sm:grid-cols-2"><button type="button" onClick={()=>setActive("machine-operation")} className={`rounded-2xl border p-4 text-left ${active==="machine-operation"?"border-[#e85d24] bg-[#fff2ec]":"border-[#dfe4e8] bg-white"}`}><small className="font-black text-[#e85d24]">BÀI KIỂM TRA 1</small><strong className="mt-1 block text-[#17232c]">Vận hành máy {machine}</strong><span className="mt-1 block text-xs text-[#71808c]">{operationQuiz.length} câu · quy trình, an toàn và thao tác máy</span></button><button type="button" onClick={()=>setActive("tool-setup")} className={`rounded-2xl border p-4 text-left ${active==="tool-setup"?"border-[#e85d24] bg-[#fff2ec]":"border-[#dfe4e8] bg-white"}`}><small className="font-black text-[#e85d24]">BÀI KIỂM TRA 2</small><strong className="mt-1 block text-[#17232c]">Cài đặt dao {machine}</strong><span className="mt-1 block text-xs text-[#71808c]">{toolQuiz.length} câu · rà dao, offset và kiểm tra dao</span></button></div><IndependentSafetyQuiz key={`${machine}-${active}`} quiz={active==="machine-operation"?operationQuiz:toolQuiz} machine={machine} title={active==="machine-operation"?`Kiểm tra vận hành máy ${machine}`:`Kiểm tra cài đặt dao ${machine}`} assessmentId={active} courseId={courseId} onResult={recordPart}/></div>
}

function IndependentSafetyQuiz({quiz,machine,title,assessmentId,courseId,onResult}:{quiz:SafetyQuiz;machine:"tiện"|"phay";title:string;assessmentId:string;courseId?:number;onResult:(assessmentId:string,score:number,total:number,passed:boolean)=>void}){const[answers,setAnswers]=useState<Record<string,number>>({});const[submitted,setSubmitted]=useState(false);const score=quiz.filter(question=>answers[question.id]===question.correctIndex).length;return <SafetyGate quiz={quiz} answers={answers} setAnswers={setAnswers} submitted={submitted} setSubmitted={setSubmitted} score={score} requiredScore={quiz.length} passed={submitted&&score===quiz.length} machine={machine} courseId={courseId} title={title} onResult={(value,total,didPass)=>onResult(assessmentId,value,total,didPass)} onPassed={()=>undefined}/>}

function SafetyGate({ quiz, answers, setAnswers, submitted, setSubmitted, score, requiredScore, passed, machine, courseId, title, onPassed, onResult }: { quiz: SafetyQuiz; answers: Record<string, number>; setAnswers: React.Dispatch<React.SetStateAction<Record<string, number>>>; submitted: boolean; setSubmitted: (value: boolean) => void; score: number; requiredScore: number; passed: boolean; machine: "tiện" | "phay"; courseId?: number; title?:string; onPassed: () => void; onResult?: (score:number,total:number,passed:boolean)=>void }) {
  const { profile } = useAuth();
  const [trackingError, setTrackingError] = useState("");
  const [participantName, setParticipantName] = useState("");
  const [className, setClassName] = useState("");
  const [quizStarted, setQuizStarted] = useState(machine !== "phay");

  useEffect(() => {
    if (machine !== "phay") return;
    const savedName = window.localStorage.getItem("cnc-live-name") ?? "";
    const savedClass = window.localStorage.getItem("cnc-live-class") ?? "";
    const nextName = profile?.full_name || savedName;
    const nextClass = profile?.class_name || savedClass;
    setParticipantName(nextName);
    setClassName(nextClass);
    if (nextName) setQuizStarted(true);
  }, [machine, profile?.class_name, profile?.full_name]);

  useEffect(() => {
    if (machine !== "phay" || !quizStarted || !participantName.trim() || profile?.role === "admin") return;
    const timer = window.setTimeout(() => {
      saveCncMillingQuizAttempt({
        courseId,
        participantName,
        className,
        answers,
        score,
        totalQuestions: quiz.length,
        status: "in_progress",
      })
        .then(() => setTrackingError(""))
        .catch(() => setTrackingError("Không thể cập nhật tiến độ trực tiếp. Vui lòng kiểm tra kết nối mạng."));
    }, 400);
    return () => window.clearTimeout(timer);
  }, [answers, className, machine, participantName, profile?.role, quiz.length, quizStarted, score]);

  if (machine === "phay" && !quizStarted) {
    return <form className="cnc-quiz-join" onSubmit={(event) => {
      event.preventDefault();
      if (!participantName.trim()) return;
      window.localStorage.setItem("cnc-live-name", participantName.trim());
      window.localStorage.setItem("cnc-live-class", className.trim());
      setQuizStarted(true);
    }}>
      <div className="cnc-quiz-join-mark"><ShieldCheck size={30} /></div>
      <div>
        <small>THAM GIA KHÔNG CẦN ĐĂNG NHẬP</small>
        <strong>Bắt đầu bài kiểm tra vận hành phay</strong>
        <p>Nhập tên để giáo viên nhận diện trên màn hình thi trực tiếp.</p>
      </div>
      <input value={participantName} onChange={(event) => setParticipantName(event.target.value)} placeholder="Họ và tên học sinh" required />
      <input value={className} onChange={(event) => setClassName(event.target.value)} placeholder="Lớp (không bắt buộc)" />
      <button type="submit">Vào làm bài</button>
    </form>;
  }

  async function submitSafetyQuiz() {
    setSubmitted(true);
    const didPass = score >= requiredScore;
    onResult?.(score, quiz.length, didPass);
    if (machine === "phay" && profile?.role !== "admin") {
      try {
        await saveCncMillingQuizAttempt({
          courseId,
          participantName,
          className,
          answers,
          score,
          totalQuestions: quiz.length,
          status: didPass ? "passed" : "failed",
        });
        setTrackingError("");
      } catch {
        setTrackingError("Chưa gửi được kết quả đến giáo viên. Vui lòng thử nộp lại.");
        return;
      }
    }
    if (didPass) onPassed();
  }

  return <>
    <div className="cnc-gate-banner"><ShieldCheck size={26} /><div><span>CHỐT CHẶN AN TOÀN MÁY {machine.toUpperCase()}</span><h3>{title??`Kiểm tra trước khi lên máy ${machine}`}</h3><p>Phải trả lời đúng tối thiểu <strong>{requiredScore}/{quiz.length} câu</strong>. Hoàn thành cả hai bài để đạt phần kiểm tra.</p></div><b className={passed ? "passed" : ""}>{submitted ? `${score}/${quiz.length}` : `${Math.round((requiredScore / quiz.length) * 100)}%`}<small>{passed ? "ĐÃ ĐẠT" : "YÊU CẦU"}</small></b></div>
    {machine === "phay" && profile?.role !== "admin" && <div className="cnc-live-tracking-note"><i /><span>Đang thi với tên <strong>{participantName}</strong>{className ? ` · Lớp ${className}` : ""}. Giáo viên có thể theo dõi tiến độ trực tiếp.</span><button type="button" onClick={() => setQuizStarted(false)}>Đổi tên</button></div>}
    {trackingError && <div className="cnc-result">{trackingError}</div>}
    <div className="cnc-quiz">
      {quiz.map((question, qi) => <fieldset key={question.id} className={submitted && answers[question.id] !== question.correctIndex ? "wrong" : ""}>
        <legend><span>{qi + 1}</span>{question.question}</legend>
        {question.options.map((option, oi) => <label key={option}><input type="radio" name={question.id} checked={answers[question.id] === oi} onChange={() => { setSubmitted(false); setAnswers((current) => ({ ...current, [question.id]: oi })); }} /><i />{option}</label>)}
        {submitted && answers[question.id] !== question.correctIndex && <p>{question.explanation}</p>}
      </fieldset>)}
    </div>
    <button className="cnc-submit" disabled={Object.keys(answers).length < quiz.length} onClick={submitSafetyQuiz}><ShieldCheck size={18} /> Nộp bài kiểm tra an toàn máy {machine}</button>
    {submitted && <div className={`cnc-result ${passed ? "passed" : ""}`}>{passed ? (machine === "phay" ? "Đạt — Bạn đã được phép thực hiện Checklist vận hành máy phay CNC." : "Đạt — Bài Gia công tiện CNC đã được mở khóa.") : `Chưa đạt — Bạn trả lời đúng ${score}/${quiz.length} câu, cần tối thiểu ${requiredScore}/${quiz.length}. Hãy xem giải thích và làm lại.`}</div>}
  </>;
}

function PracticalChecklistPanel({ machine, lessonId, enabled, courseId }: { machine: "tiện" | "phay"; lessonId: "lesson-4-turn" | "lesson-4-mill"; enabled: boolean; courseId?: number }) {
  const [mode, setMode] = useState<"practice" | "cross-check">("practice");
  return <>
    <div className="cnc-checklist-mode-toggle">
      <button type="button" className={mode === "practice" ? "active" : ""} onClick={() => setMode("practice")}><ClipboardCheck size={15} /> Tự luyện tập</button>
      <button type="button" className={mode === "cross-check" ? "active" : ""} onClick={() => setMode("cross-check")}><Users size={15} /> Chấm chéo (thi)</button>
    </div>
    {mode === "practice"
      ? <><p className="cnc-checklist-hint">Chế độ tự luyện tập — tự đánh dấu để ôn lại quy trình, không tính điểm và không lưu lại.</p><OperationChecklist machine={machine} enabled={enabled} onPassed={() => undefined} /></>
      : <CrossCheckChecklist machine={machine} lessonId={lessonId} courseId={courseId} />}
  </>;
}

function OperationChecklist({ machine, enabled, onPassed }: { machine: "tiện" | "phay"; enabled: boolean; onPassed: (lessonId: string) => void }) {
  const [checked, setChecked] = useState<Record<string, boolean>>({});
  const [zeroToleranceClear, setZeroToleranceClear] = useState<Record<number, boolean>>({});
  const sections = machine === "tiện" ? turningChecklistSections : millingChecklistSections;
  const zeroTolerance = machine === "tiện" ? turningZeroTolerance : millingZeroTolerance;
  const lessonId = machine === "tiện" ? "lesson-4-turn" : "lesson-4-mill";
  const items = sections.flatMap((section) => section.items);
  const score = items.reduce((total, item) => total + (checked[item.id] ? item.score : 0), 0);
  const criticalPassed = items.filter((item) => "critical" in item && item.critical).every((item) => checked[item.id]);
  const zeroTolerancePassed = zeroTolerance.every((_, index) => zeroToleranceClear[index]);
  const passed = enabled && score >= 8 && criticalPassed && zeroTolerancePassed;

  useEffect(() => {
    if (passed) onPassed(lessonId);
  }, [lessonId, onPassed, passed]);

  return <>
    <SectionHeading icon={ClipboardCheck} kicker="MỤC 05" title="Check list kỹ năng thực hành" description={machine === "tiện" ? "Gá phôi, cài đặt offset phôi và dao trên máy tiện CNC." : "Cài đặt dao, phôi trên máy phay CNC và kiểm tra Test Offset."} />
    {!enabled && <div className="cnc-checklist-locked"><LockKeyhole size={19} /><div><strong>Checklist chưa được mở</strong><p>Sinh viên phải hoàn thành và đạt cả hai bài Kiểm tra vận hành máy và Cài đặt dao {machine} để mở checklist thực hành.</p></div></div>}
    <div className="cnc-checklist-rules">
      <span><ClipboardCheck size={17} /><b>Ngưỡng đạt: 8/10 điểm</b></span>
      <span><AlertTriangle size={17} /><b>Không vi phạm mốc chặn</b></span>
      <p>Đánh dấu vào từng bước sau khi đã thực hiện chính xác, đúng kỹ thuật và an toàn. Bước không được đánh dấu nhận 0 điểm.</p>
    </div>
    <div className="cnc-operation-checklist">
      {sections.map((section) => <section key={section.id}>
        <header><h4>{section.title}</h4><b>{section.maxScore.toFixed(1)} điểm</b></header>
        {section.items.map((item) => {
          const critical = "critical" in item && item.critical;
          return <label key={item.id} className={`${checked[item.id] ? "checked" : ""} ${critical ? "critical" : ""}`}>
            <input type="checkbox" disabled={!enabled} checked={Boolean(checked[item.id])} onChange={(event) => setChecked((current) => ({ ...current, [item.id]: event.target.checked }))} />
            <i><Check size={14} /></i>
            <span><strong>{critical && <AlertTriangle size={14} />} {item.id}. {item.label}</strong><small>{item.note}</small></span>
            <b>+{item.score.toFixed(1)}</b>
          </label>;
        })}
      </section>)}
    </div>
    <section className="cnc-zero-tolerance">
      <header><AlertTriangle size={20} /><div><strong>Lỗi loại trực tiếp (Zero-tolerance)</strong><p>Phải xác nhận không vi phạm đầy đủ {zeroTolerance.length} điều kiện dưới đây.</p></div></header>
      {zeroTolerance.map((item, index) => <label key={item}>
        <input type="checkbox" disabled={!enabled} checked={Boolean(zeroToleranceClear[index])} onChange={(event) => setZeroToleranceClear((current) => ({ ...current, [index]: event.target.checked }))} />
        <i><Check size={13} /></i><span><b>{index + 1}</b>{item}</span>
      </label>)}
    </section>
    <div className={`cnc-checklist-score ${passed ? "passed" : ""}`}>
      <div><small>TỔNG ĐIỂM THỰC HÀNH</small><strong>{score.toFixed(1)}<span>/10.0</span></strong></div>
      <div className="cnc-checklist-status">
        <b>{passed ? "ĐẠT" : "CHƯA ĐẠT"}</b>
        <p>{!enabled ? "Checklist đang khóa." : score < 8 ? `Cần thêm ${(8 - score).toFixed(1)} điểm để đạt ngưỡng.` : !criticalPassed ? "Chưa đạt một hoặc nhiều bước an toàn trọng yếu." : !zeroTolerancePassed ? "Chưa xác nhận đầy đủ các mốc chặn Zero-tolerance." : "Đã đạt điểm và không vi phạm mốc chặn."}</p>
      </div>
    </div>
    {passed && <div className="cnc-checklist-congratulations"><Check size={25} /><p>Chúc mừng bạn đã vượt qua checklist cài đặt dao, phôi trên máy {machine} CNC.</p></div>}
  </>;
}

function Resources({ lesson, files }: { lesson: (typeof lessons)[number]; files: CncLessonFile[] }) {
  const resources = "resources" in lesson && lesson.resources ? lesson.resources : ["Giáo trình Gia công CNC", "Phiếu hướng dẫn thực hành", "Bản vẽ và dữ liệu bài tập"];
  return <>
    <SectionHeading icon={FileText} kicker="MỤC 05" title="Tài liệu học tập" description="Tài liệu bắt buộc và tài nguyên hỗ trợ cho bài học." />
    <div className="cnc-resources">
      {files.map((file) => <div key={file.id}><span className="doc">{file.file_name.split(".").pop()?.slice(0, 4).toUpperCase() || "FILE"}</span><div><strong>{file.title}</strong><small>{formatFileSize(file.size_bytes)} · Tài liệu tải lên</small></div><a href={file.file_url} target="_blank" rel="noreferrer" aria-label={`Tải ${file.title}`}><Download size={18} /></a></div>)}
      {resources.map((resource, i) => <div key={resource}><span className={i % 2 ? "doc" : "pdf"}>{i % 2 ? "DOC" : "PDF"}</span><div><strong>{resource}</strong><small>Tài liệu tham khảo</small></div><button aria-label={`Tải ${resource}`} disabled><Download size={18} /></button></div>)}
    </div>
  </>;
}

function SectionHeading({ icon: Icon, kicker, title, description }: { icon: typeof GraduationCap; kicker: string; title: string; description: string }) {
  return <div className="cnc-section-heading"><span><Icon size={21} /></span><div><small>{kicker}</small><h3>{title}</h3><p>{description}</p></div></div>;
}
