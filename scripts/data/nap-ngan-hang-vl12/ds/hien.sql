begin;
update public.question_bank set archived = false where note = 'nap-vl12-ds-20261024' and archived = true;
select count(*) filter (where archived) as an, count(*) filter (where not archived) as hien, count(*) as tong from public.question_bank where note = 'nap-vl12-ds-20261024';
commit;
-- Hoàn tác: update public.question_bank set archived = true where note = 'nap-vl12-ds-20261024';
