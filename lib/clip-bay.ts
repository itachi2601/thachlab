// Clip "bẫy hay sai" 20–30 s cho phụ đạo theo chủ đề (chặng C, docs/KE-HOACH-MOTION-GRAPHIC.md, thí điểm L12 Ch.3).
// Kho: content/phu-dao/clip-bay/<id>.json — `video` do scripts/tai-clip-len-storage.mts --kho-dir ghi khi tải lên bucket.
// Dữ liệu tĩnh trong bundle, không thêm round-trip Supabase. Clip chưa có `video.mp4` thì không hiện.
import c01 from "@/content/phu-dao/clip-bay/bay-l12-ch3-01.json";
import c02 from "@/content/phu-dao/clip-bay/bay-l12-ch3-02.json";
import c03 from "@/content/phu-dao/clip-bay/bay-l12-ch3-03.json";
import c04 from "@/content/phu-dao/clip-bay/bay-l12-ch3-04.json";
import c05 from "@/content/phu-dao/clip-bay/bay-l12-ch3-05.json";

export type ClipBay = {
  id: string;
  topicId: number;
  lessonTopicId: number;
  nhan: string;
  nhinVao: string;
  mp4: string;
  poster: string;
  giay: number;
};

type Kho = {
  id: string;
  topic_id: number;
  lesson_topic_id: number;
  nhan: string;
  nhin_vao: string;
  video?: { mp4?: string; poster?: string; giay?: number };
};

const ALL: ClipBay[] = ([c01, c02, c03, c04, c05] as Kho[]).flatMap((k) =>
  k.video?.mp4 && k.video.poster
    ? [{
        id: k.id, topicId: k.topic_id, lessonTopicId: k.lesson_topic_id, nhan: k.nhan, nhinVao: k.nhin_vao,
        mp4: k.video.mp4, poster: k.video.poster, giay: k.video.giay ?? 30,
      }]
    : [],
);

/** Clip cho một mục phụ đạo (tầng bài): ưu tiên đúng các YCCĐ em đang sai, theo thứ tự sai nhiều → ít; tối đa `max`. */
export function clipsForNeed(lessonTopicId: number, outcomeTopicIds: number[], max = 2): ClipBay[] {
  const ofLesson = ALL.filter((c) => c.lessonTopicId === lessonTopicId);
  const hit = outcomeTopicIds.flatMap((id) => ofLesson.filter((c) => c.topicId === id));
  return (hit.length ? hit : ofLesson).slice(0, max);
}
