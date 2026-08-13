import { getSupabase } from "@/services/supabase";

export type CompetencyId="turn-operation"|"turn-tool-setup"|"mill-operation"|"mill-tool-setup";
export type CompetencyPermissionStatus="approved"|"revoked";
export interface CompetencyPermission{course_id:number;student_id:string;competency_id:CompetencyId;status:CompetencyPermissionStatus;note:string;approved_at:string|null;updated_at:string;approved_by:string|null}

export const CNC_COMPETENCIES=[
  {id:"turn-operation" as const,title:"Vận hành máy tiện",lessonId:"lesson-4-turn",assessmentId:"machine-operation",permission:"Thao tác bảng điều khiển máy tiện"},
  {id:"turn-tool-setup" as const,title:"Cài đặt dao tiện",lessonId:"lesson-4-turn",assessmentId:"tool-setup",permission:"Rà dao và nhập offset máy tiện"},
  {id:"mill-operation" as const,title:"Vận hành máy phay",lessonId:"lesson-4-mill",assessmentId:"machine-operation",permission:"Thao tác bảng điều khiển máy phay"},
  {id:"mill-tool-setup" as const,title:"Cài đặt dao phay",lessonId:"lesson-4-mill",assessmentId:"tool-setup",permission:"Cài G54, H và D trên máy phay"},
];

export async function fetchCourseCompetencyPermissions(courseId:number,studentId?:string){let query=getSupabase().from("cnc_competency_permissions").select("course_id, student_id, competency_id, status, note, approved_at, updated_at, approved_by").eq("course_id",courseId);if(studentId)query=query.eq("student_id",studentId);const{data,error}=await query;if(error)throw error;return(data??[])as CompetencyPermission[]}
export async function setCompetencyPermission(courseId:number,studentId:string,competencyId:CompetencyId,status:CompetencyPermissionStatus,note=""){const supabase=getSupabase();const{data:auth}=await supabase.auth.getUser();const{error}=await supabase.from("cnc_competency_permissions").upsert({course_id:courseId,student_id:studentId,competency_id:competencyId,status,note,approved_by:auth.user?.id,approved_at:status==="approved"?new Date().toISOString():null,updated_at:new Date().toISOString()},{onConflict:"course_id,student_id,competency_id"});if(error)throw error}
