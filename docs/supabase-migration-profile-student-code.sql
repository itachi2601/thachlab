-- Mã số sinh viên do sinh viên tự khai báo trong hồ sơ; không cho phép trùng mã.
alter table public.profiles add column if not exists student_code text;

create unique index if not exists profiles_student_code_unique_idx
  on public.profiles(upper(student_code))
  where student_code is not null and trim(student_code) <> '';

alter table public.profiles drop constraint if exists profiles_student_code_format_check;
alter table public.profiles add constraint profiles_student_code_format_check
  check (student_code is null or (char_length(trim(student_code)) between 2 and 30));
