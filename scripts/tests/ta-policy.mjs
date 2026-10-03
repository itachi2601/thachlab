// Run with PGLITE_MODULE=/absolute/path/to/@electric-sql/pglite/dist/index.js node scripts/tests/ta-policy.mjs
import fs from 'node:fs';
import assert from 'node:assert/strict';
const {PGlite}=await import(process.env.PGLITE_MODULE || '@electric-sql/pglite');
const db=new PGlite();
const sql=async text=>db.exec(text);
const one=async(text,args=[]) => (await db.query(text,args)).rows[0];
const admin='00000000-0000-0000-0000-000000000001', user='00000000-0000-0000-0000-000000000002',other='00000000-0000-0000-0000-000000000003',ta='00000000-0000-0000-0000-000000000010';
await sql(`create role authenticated; create role anon; create role service_role; create schema auth;
 create table auth.users(id uuid primary key);
 create function auth.uid() returns uuid language sql stable as $$ select nullif(current_setting('test.user',true),'')::uuid $$;
 create function public.is_admin() returns boolean language sql stable as $$ select coalesce(auth.uid()='${admin}',false) $$;
 create table public.profiles(id uuid primary key);
 grant usage on schema public,auth to authenticated,anon;
 insert into auth.users values('${admin}'),('${user}'),('${other}');
 select set_config('test.user','${admin}',false);`);
await sql(fs.readFileSync('docs/supabase-migration-tro-giang.sql','utf8'));
await sql(fs.readFileSync('docs/supabase-migration-tro-giang-phudao-nhieu-em.sql','utf8'));
await sql(`insert into ta_assistants(id,user_id,full_name,short_name,tier,retained_rate) values('${ta}','${user}','Test','Test','B3',60000);
 insert into ta_sessions(assistant_id,work_date,session_type,start_time,end_time,error_note,student_touches,status) values('${ta}','2026-09-10','lop','17:00','18:30','lỗi',12,'approved');`);
const legacy=await one(`select row_to_json(t) v from ta_monthly_score('${ta}','2026-09-01') t`);
await sql(fs.readFileSync('docs/supabase-migration-ta-policy-oct2026.sql','utf8'));
await sql(fs.readFileSync('docs/supabase-migration-ta-policy-oct2026.sql','utf8'));
assert.deepEqual(await one(`select row_to_json(t) v from ta_monthly_score('${ta}','2026-09-01') t`),legacy);
// Stub tối giản của 3 bảng phụ đạo (docs/supabase-migration-tutoring-needs.sql +
// -tutoring-exit-quiz.sql) — chỉ đủ cột cho migration 20261003150000 chạy, không kéo cả migration
// thật vào (kéo theo question_topics/exam_question_results không có trong DB test này).
await sql(`create table public.tutoring_session_topics(id bigint generated always as identity primary key, session_id uuid not null, student_id uuid not null, topic_id bigint not null, created_at timestamptz not null default now());
 create table public.tutoring_needs(id bigint generated always as identity primary key, student_id uuid not null, topic_id bigint not null, form text not null default '', status text not null default 'open');
 create table public.tutoring_exit_attempts(id bigint generated always as identity primary key, tutoring_need_id bigint, student_id uuid not null, topic_id bigint, form text not null default '', question_ids bigint[] not null default '{}', total int not null default 10, correct int not null default 0, pct int not null default 0, passed boolean not null default false, created_at timestamptz not null default now());`);
await sql(fs.readFileSync('supabase/migrations/20261003150000_phu_dao_kiem_tra_cuoi_buoi.sql','utf8'));
await sql(fs.readFileSync('supabase/migrations/20261003150000_phu_dao_kiem_tra_cuoi_buoi.sql','utf8'));
await sql(`create or replace function public.ta_policy_today() returns date language sql stable as $$ select date '2026-12-31' $$; grant select,insert,update on ta_sessions to authenticated; grant select on ta_assistants to authenticated;`);
const base={attendance:'on_time',arrived_early:true,homework_checked:true,homework_missing:0,walked_tables:true,reported_students:true,attention_note:'',teaching_minutes:45,teaching_note:'Chữa bài 1',prepared:true,recalled:true,asked_each:true,followups:[]};
const setUser=async id=>sql(`select set_config('test.user','${id}',false)`);
async function add(date,type='lop',patch={}){const fields={assistant_id:ta,work_date:date,session_type:type,class_label:'12A',start_time:'17:00',end_time:'18:30',student_touches:type==='lop'?12:null,error_note:'Lỗi lớp',policy:base,status:'approved',...patch};const keys=Object.keys(fields);return one(`insert into ta_sessions(${keys.join(',')}) values(${keys.map((_,i)=>'$'+(i+1)).join(',')}) returning id`,Object.values(fields));}
const month=async m=>(await one('select ta_monthly_policy($1,$2) v',[ta,m])).v;
const save=async(m,scores,close=false)=> (await one('select ta_save_month_review($1,$2,$3,$4,$5,$6) v',[ta,m,scores,60000,'Kiểm thử',close])).v;
let count=0;async function test(name,fn){await fn();count++;console.log('PASS',name)}
await test('October trial: 45 min teaching within 90 min; low score still 1.0',async()=>{await add('2026-10-01');let s=await save('2026-10-01',{touches:0,phudao:0,homework:0,attendance:0,observation:0});assert.equal(s.class_factor,1);assert.equal(s.class_pay,45000);assert.equal(s.teaching_pay,72000);assert.equal(s.total_pay,117000)});
await test('November threshold 69.99 vs 70; teaching factor never stacked',async()=>{await add('2026-11-01');let s=await save('2026-11-01',{touches:30,phudao:20,homework:10,attendance:5,observation:4.99});assert.equal(s.class_factor,.9);assert.equal(s.class_pay,40500);assert.equal(s.teaching_pay,72000);s=await save('2026-11-01',{touches:30,phudao:20,homework:10,attendance:5,observation:5});assert.equal(s.class_factor,1)});
await test('Tutoring 1–2 students x1.2, 3–4 x1.4, no class penalty',async()=>{for(let n=1;n<=4;n++){const names=Array.from({length:n},(_,i)=>'Em '+i);await add('2026-11-02','phudao',{phudao_students:names,policy:{...base,teaching_minutes:0,followups:names.map(student=>({student,lesson:'Bài 1',difficulty:'Đã làm được'}))}})}let s=await month('2026-11-01');assert.equal(s.tutoring_weighted_hours,7.8);assert.equal(s.tutoring_pay,468000);assert.equal(s.phudao,20)});
await test('5 students rejected; too many teaching minutes rejected',async()=>{await assert.rejects(()=>add('2026-11-02','phudao',{phudao_students:['a','b','c','d','e']}));await assert.rejects(()=>add('2026-11-02','lop',{policy:{...base,teaching_minutes:91}}))});
await test('No tutoring requires teacher score; observation mandatory',async()=>{await add('2026-12-01');const s=await month('2026-12-01');assert.equal(s.phudao,null);assert.equal(s.observation,null);await assert.rejects(()=>save('2026-12-01',{},true))});
await test('No administrative work in October; pre-policy results unchanged',async()=>{await assert.rejects(()=>add('2026-10-02','hanhchinh'));assert.deepEqual(await one(`select row_to_json(t) v from ta_monthly_score('${ta}','2026-09-01') t`),legacy)});
await test('Other assistants cannot view payroll or close a month',async()=>{await setUser(other);await assert.rejects(()=>month('2026-10-01'));await setUser(user);await assert.rejects(()=>save('2026-10-01',{},true));await setUser(admin)});
await test('Pending work blocks closure',async()=>{const r=await add('2026-10-03','lop',{status:'submitted'});await assert.rejects(()=>save('2026-10-01',{phudao:25,observation:10},true));await sql(`update ta_sessions set status='approved' where id='${r.id}'`)});
await test('Close stores snapshot; student cannot insert or edit closed month',async()=>{const s=await save('2026-10-01',{phudao:25,observation:10},true);assert.ok(s.closed_at);await setUser(user);await sql('set role authenticated');await assert.rejects(()=>add('2026-10-04','lop',{status:'submitted'}));await sql('reset role');await setUser(admin)});
await test('Admin edit reopens month; teacher can reclose; audit preserved',async()=>{const row=await one(`select id from ta_sessions where work_date='2026-10-01'`);await sql(`update ta_sessions set student_touches=6 where id='${row.id}'`);assert.equal((await month('2026-10-01')).closed_at,null);assert.ok((await save('2026-10-01',{phudao:25,observation:10},true)).closed_at);assert.ok(Number((await one(`select count(*) n from ta_policy_audit where action='reopen_after_session_edit'`)).n)>0)});
await test('Per-session touches cap stops one busy session offsetting another',async()=>{await add('2026-12-02','lop',{student_touches:0,policy:{...base,teaching_minutes:0}});await add('2026-12-03','lop',{student_touches:24,policy:{...base,teaching_minutes:0}});const s=await save('2026-12-01',{phudao:25,observation:10});assert.equal(s.touches,20)});
await test('Marks outside their ranges rejected; future month cannot close',async()=>{await assert.rejects(()=>save('2026-12-01',{observation:11}));await assert.rejects(()=>save('2027-01-01',{phudao:25,observation:10},true))});
await sql(`create or replace function public.ta_policy_today() returns date language sql stable as $$ select date '2027-01-31' $$;`);
const e=i=>`00000000-0000-0000-0000-0000000000e${i}`;
const T1=901,T2=902;
const followup=names=>names.map(student=>({student,lesson:'Bài 1',difficulty:'Đã làm được'}));
const attempt=(i,topic,passed,windowId,at)=>sql(`insert into tutoring_exit_attempts(tutoring_need_id,student_id,topic_id,passed,pct,window_id,created_at) select id,'${e(i)}',${topic},${passed},${passed?80:40},${windowId?`'${windowId}'`:'null'},'${at}' from tutoring_needs where student_id='${e(i)}' and topic_id=${topic}`);
const mkWindow=async(students,topics,openedAt)=>{const w=await one(`insert into tutoring_exit_windows(assistant_id,student_ids,topic_ids) values('${ta}',array[${students.map(i=>`'${e(i)}'`).join(',')}]::uuid[],array[${topics.join(',')}]::bigint[]) returning id,extract(epoch from closes_at-opened_at)/60 as len`);assert.equal(Number(w.len),20);await sql(`update tutoring_exit_windows set opened_at='${openedAt}',closes_at='${openedAt}'::timestamptz+interval '20 minutes' where id='${w.id}'`);return w.id};
await test('Phụ đạo 25đ theo tỉ lệ nhóm đạt: ≥60% đủ, 40–59% nửa, <40% không',async()=>{
 // buổi 5/1/2027: 3 em x 1 chủ đề = 3 cặp; cửa sổ mở 10:00 UTC (17:00 VN) cùng ngày
 const s=await add('2027-01-05','phudao',{phudao_students:['A','B','C'],policy:{...base,teaching_minutes:0,followups:followup(['A','B','C'])}});
 for(const i of [1,2,3]){await sql(`insert into tutoring_needs(student_id,topic_id) values('${e(i)}',${T1})`);await sql(`insert into tutoring_session_topics(session_id,student_id,topic_id) values('${s.id}','${e(i)}',${T1})`)}
 // chủ đề dạy thêm ngoài danh sách hổng không có bài để làm -> không được làm tụt mẫu số
 await sql(`insert into tutoring_session_topics(session_id,student_id,topic_id) values('${s.id}','${e(1)}',${T2})`);
 const w=await mkWindow([1,2,3],[T1],'2027-01-05T10:00:00Z');
 assert.equal((await month('2027-01-01')).phudao,0); // chưa ai làm
 await attempt(1,T1,true,w,'2027-01-05T10:10:00Z');
 assert.equal((await month('2027-01-01')).phudao,0); // 1/3 = 33% < 40%
 await attempt(2,T1,false,w,'2027-01-05T10:11:00Z');
 await attempt(3,T1,true,w,'2027-01-05T10:12:00Z');
 assert.equal((await month('2027-01-01')).phudao,25); // 2/3 = 67% >= 60%
 // buổi 6/1: 2 cặp, 1 đạt = 50% -> 12,5đ cho buổi đó; trung bình tháng (25+12,5)/2
 const s2=await add('2027-01-06','phudao',{phudao_students:['A','B'],policy:{...base,teaching_minutes:0,followups:followup(['A','B'])}});
 for(const i of [1,2]) await sql(`insert into tutoring_session_topics(session_id,student_id,topic_id) values('${s2.id}','${e(i)}',${T1})`);
 const w2=await mkWindow([1,2],[T1],'2027-01-06T10:00:00Z');
 await attempt(1,T1,true,w2,'2027-01-06T10:10:00Z');
 await attempt(2,T1,false,w2,'2027-01-06T10:11:00Z');
 assert.equal(Number((await one('select ta_tutoring_pass_ratio($1) v',[s2.id])).v),0.5);
 assert.equal((await month('2027-01-01')).phudao,18.75);
});
await test('Lượt tự ôn ngoài cửa sổ và cửa sổ sai ngày không được tính vào điểm trợ giảng',async()=>{
 const s=await add('2027-01-07','phudao',{phudao_students:['A'],policy:{...base,teaching_minutes:0,followups:followup(['A'])}});
 await sql(`insert into tutoring_session_topics(session_id,student_id,topic_id) values('${s.id}','${e(1)}',${T1})`);
 await attempt(1,T1,true,null,'2027-01-07T10:10:00Z'); // tự ôn đạt, không có window_id
 assert.equal(Number((await one('select ta_tutoring_pass_ratio($1) v',[s.id])).v),0);
 const wrongDay=await mkWindow([1],[T1],'2027-01-08T10:00:00Z'); // cửa sổ mở ngày khác
 await attempt(1,T1,true,wrongDay,'2027-01-08T10:05:00Z');
 assert.equal(Number((await one('select ta_tutoring_pass_ratio($1) v',[s.id])).v),0);
});
await test('Guard DB: cửa sổ 10 câu đạt từ 70%, mỗi em/chủ đề một lượt, đúng em và chủ đề, quá hạn bị chặn',async()=>{
 await sql(`create trigger trg_tutoring_exit_attempt_guard before insert on public.tutoring_exit_attempts for each row execute function public.tutoring_exit_attempt_guard()`);
 const ins=(i,topic,correct,windowId,total=10)=>one(`insert into tutoring_exit_attempts(tutoring_need_id,student_id,total,correct,window_id) select id,'${e(i)}',${total},${correct},${windowId?`'${windowId}'`:'null'} from tutoring_needs where student_id='${e(i)}' and topic_id=${topic} returning pct,passed`);
 await sql(`insert into tutoring_needs(student_id,topic_id) values('${e(4)}',${T1}),('${e(5)}',${T2})`);
 const fresh=await one(`insert into tutoring_exit_windows(assistant_id,student_ids,topic_ids) values('${ta}',array['${e(4)}']::uuid[],array[${T1}]::bigint[]) returning id`);
 assert.deepEqual(await ins(4,T1,7,fresh.id),{pct:70,passed:true});
 await assert.rejects(()=>ins(4,T1,9,fresh.id)); // lượt thứ hai trong cùng cửa sổ
 await assert.rejects(()=>ins(5,T2,10,fresh.id)); // em không thuộc cửa sổ / chủ đề không thuộc cửa sổ
 const expired=await mkWindow([4],[T1],'2026-01-01T00:00:00Z');
 await sql(`insert into tutoring_needs(student_id,topic_id) values('${e(6)}',${T1})`);
 await assert.rejects(()=>ins(4,T1,10,expired));
 const f2=await one(`insert into tutoring_exit_windows(assistant_id,student_ids,topic_ids) values('${ta}',array['${e(6)}']::uuid[],array[${T1}]::bigint[]) returning id`);
 assert.deepEqual(await ins(6,T1,6,f2.id),{pct:60,passed:false}); // 6/10 < 70%
 // ngoài cửa sổ: vẫn 80% (7/10 trượt)
 await sql(`insert into tutoring_needs(student_id,topic_id) values('${e(7)}',${T1})`);
 assert.deepEqual(await ins(7,T1,7,null),{pct:70,passed:false});
});
console.log(`${count} policy checks passed; migration applied twice; legacy payroll preserved.`);await db.close();
