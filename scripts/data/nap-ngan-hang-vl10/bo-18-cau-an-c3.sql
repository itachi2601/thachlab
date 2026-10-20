begin;
select count(*) as se_xoa from public.question_bank where note = 'nap-vl10-c3-20261020' and archived;
delete from public.question_bank where note = 'nap-vl10-c3-20261020' and archived;
select count(*) filter (where archived) an, count(*) filter (where not archived) hien, count(*) tong from public.question_bank where note = 'nap-vl10-c3-20261020';
commit;
