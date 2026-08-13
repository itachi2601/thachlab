import type { CncLearningRecord } from "@/services/cnc-learning-records";
import type { AttendanceStatus } from "@/services/course-attendance";
import { CNC_TOTAL_ASSESSMENTS } from "@/services/cnc-progress";

export type CncAchievement={id:string;group:"assessment"|"attendance";icon:string;name:string;description:string;earned:boolean;progress?:string};

export function cncAchievements(records:CncLearningRecord[],attendance:AttendanceStatus[]):CncAchievement[]{
  const passed=records.filter(row=>row.completed);
  const firstTry=records.filter(row=>row.completed&&row.attempt_count===1).toSorted((a,b)=>Date.parse(a.last_activity_at)-Date.parse(b.last_activity_at));
  const hasThreeStreak=firstTry.some((_,index)=>index>=2);
  const attended=attendance.filter(status=>status==="present"||status==="late");
  const hasFiveStreak=attendance.reduce((best,status)=>status==="present"||status==="late"?best+1:0,0)>=5||attendance.some((_,start)=>attendance.slice(start,start+5).length===5&&attendance.slice(start,start+5).every(status=>status==="present"||status==="late"));
  return[
    {id:"first-unlock",group:"assessment",icon:"🔓",name:"Người mở khoá",description:"Đạt bài kiểm tra đầu tiên",earned:passed.length>=1,progress:`${Math.min(passed.length,1)}/1`},
    {id:"streak-3",group:"assessment",icon:"🔥",name:"Chuỗi 3",description:"Đạt 3 bài ngay lần đầu, không trượt",earned:hasThreeStreak,progress:`${Math.min(firstTry.length,3)}/3`},
    {id:"perfect-first",group:"assessment",icon:"🎯",name:"Ăn điểm tuyệt đối",description:"Điểm tối đa ngay lần làm đầu tiên",earned:records.some(row=>row.attempt_count===1&&row.total_questions!==null&&row.latest_score===row.total_questions)},
    {id:"comeback",group:"assessment",icon:"💪",name:"Không bỏ cuộc",description:"Vượt qua một bài sau ít nhất 3 lần thử",earned:records.some(row=>row.completed&&row.attempt_count>=3)},
    {id:"graduate",group:"assessment",icon:"🏆",name:"Tốt nghiệp CNC",description:"Đạt đủ 17/17 bài kiểm tra toàn khoá",earned:passed.length>=CNC_TOTAL_ASSESSMENTS,progress:`${Math.min(passed.length,CNC_TOTAL_ASSESSMENTS)}/${CNC_TOTAL_ASSESSMENTS}`},
    {id:"halfway",group:"assessment",icon:"⭐",name:"Nửa chặng đường",description:"Đạt ít nhất 50% số bài toàn khoá",earned:passed.length>=Math.ceil(CNC_TOTAL_ASSESSMENTS/2),progress:`${Math.min(passed.length,Math.ceil(CNC_TOTAL_ASSESSMENTS/2))}/${Math.ceil(CNC_TOTAL_ASSESSMENTS/2)}`},
    {id:"attendance-perfect",group:"attendance",icon:"🟢",name:"Chuyên cần",description:"Có mặt đầy đủ mọi buổi đã ghi nhận",earned:attendance.length>0&&attendance.every(status=>status==="present"),progress:`${attendance.filter(status=>status==="present").length}/${attendance.length||1}`},
    {id:"always-on-time",group:"attendance",icon:"⏰",name:"Đúng giờ tuyệt đối",description:"Chưa từng bị ghi nhận đi muộn",earned:attendance.length>0&&!attendance.includes("late")},
    {id:"attendance-streak",group:"attendance",icon:"📅",name:"Bền bỉ",description:"Tham dự liên tục ít nhất 5 buổi không vắng",earned:hasFiveStreak,progress:`${Math.min(attended.length,5)}/5`},
  ];
}
