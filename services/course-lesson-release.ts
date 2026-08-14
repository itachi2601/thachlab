import { getSupabase } from "@/services/supabase";

export const CNC_LESSON_RELEASES=[
  {id:"lesson-1",label:"Bài 1 · An toàn"},{id:"lesson-2",label:"Bài 2 · Lập trình tiện"},{id:"lesson-3",label:"Bài 3 · Lập trình phay"},{id:"lesson-4-turn",label:"Bài 4T · Vận hành tiện"},{id:"lesson-4-mill",label:"Bài 4P · Vận hành phay"},{id:"lesson-5",label:"Bài 5 · Gia công tiện"},{id:"lesson-6",label:"Bài 6 · Gia công phay"},
] as const;

export async function fetchOpenCncLessons(courseId:number){const{data,error}=await getSupabase().from("course_offerings").select("open_lesson_ids").eq("id",courseId).single();if(error)throw error;return Array.isArray(data?.open_lesson_ids)?data.open_lesson_ids as string[]:[]}
export async function updateOpenCncLessons(courseId:number,lessonIds:string[]){const{error}=await getSupabase().from("course_offerings").update({open_lesson_ids:lessonIds}).eq("id",courseId);if(error)throw error}
