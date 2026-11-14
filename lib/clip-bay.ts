// Clip "bẫy hay sai" 20–30 s cho phụ đạo theo chủ đề (chặng C, docs/KE-HOACH-MOTION-GRAPHIC.md, thí điểm L12 Ch.3; thêm Ch.1, 2, 4 ngày 14/11/2026).
// Kho: content/phu-dao/clip-bay/<id>.json — `video` do scripts/tai-clip-len-storage.mts --kho-dir ghi khi tải lên bucket.
// Dữ liệu tĩnh trong bundle, không thêm round-trip Supabase. Clip chưa có `video.mp4` thì không hiện.
import c01 from "@/content/phu-dao/clip-bay/bay-l12-ch3-01.json";
import c02 from "@/content/phu-dao/clip-bay/bay-l12-ch3-02.json";
import c03 from "@/content/phu-dao/clip-bay/bay-l12-ch3-03.json";
import c04 from "@/content/phu-dao/clip-bay/bay-l12-ch3-04.json";
import c05 from "@/content/phu-dao/clip-bay/bay-l12-ch3-05.json";
import bch1_01 from "@/content/phu-dao/clip-bay/bay-l12-ch1-01.json";
import bch1_02 from "@/content/phu-dao/clip-bay/bay-l12-ch1-02.json";
import bch1_03 from "@/content/phu-dao/clip-bay/bay-l12-ch1-03.json";
import bch1_04 from "@/content/phu-dao/clip-bay/bay-l12-ch1-04.json";
import bch2_01 from "@/content/phu-dao/clip-bay/bay-l12-ch2-01.json";
import bch2_02 from "@/content/phu-dao/clip-bay/bay-l12-ch2-02.json";
import bch2_03 from "@/content/phu-dao/clip-bay/bay-l12-ch2-03.json";
import bch2_04 from "@/content/phu-dao/clip-bay/bay-l12-ch2-04.json";
import bch4_01 from "@/content/phu-dao/clip-bay/bay-l12-ch4-01.json";
import bch4_02 from "@/content/phu-dao/clip-bay/bay-l12-ch4-02.json";
import bch4_03 from "@/content/phu-dao/clip-bay/bay-l12-ch4-03.json";
import bch4_04 from "@/content/phu-dao/clip-bay/bay-l12-ch4-04.json";

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

const ALL: ClipBay[] = ([
  c01, c02, c03, c04, c05,
  bch1_01, bch1_02, bch1_03, bch1_04, bch2_01, bch2_02, bch2_03, bch2_04, bch4_01, bch4_02, bch4_03, bch4_04,
] as Kho[]).flatMap((k) =>
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
