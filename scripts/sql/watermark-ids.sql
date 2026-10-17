-- id các câu question_bank còn dòng quảng cáo thukhoadaihoc.vn (chữ VNI vỡ "Taøi lieäu") — chỉ đọc
select coalesce(json_agg(id order by id), '[]') as ids, count(*) as n
from question_bank
where question::text ~* 'thukhoadaihoc|Ta[øo]i\s*lie[äa]u\s*[ñn][öo]' ;
