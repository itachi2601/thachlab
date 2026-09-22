-- Nội dung bài học CNC (thay cho mảng viết cứng CNC_COURSE_ITEMS trong services/cnc-lms.ts)
-- Chạy một lần trong Supabase SQL Editor. Giữ nguyên id dạng slug cũ ("lesson-1"…) vì
-- checklist, điều kiện mở bài (CncCourseWorkspace.tsx), CNC_ASSESSMENT_PLAN
-- (services/cnc-progress.ts) và cnc_lesson_videos.lesson_id đều tham chiếu theo đúng các id này.

create table if not exists public.cnc_lessons (
  id text primary key,
  title text not null,
  short_title text not null,
  duration_label text not null default '',
  emphasis text,
  body_html text not null default '',
  resources jsonb not null default '[]'::jsonb,
  sort_order integer not null default 0,
  created_at timestamptz not null default now()
);

create index if not exists cnc_lessons_sort_idx on public.cnc_lessons (sort_order);

alter table public.cnc_lessons enable row level security;

drop policy if exists "anyone reads cnc lessons" on public.cnc_lessons;
create policy "anyone reads cnc lessons" on public.cnc_lessons
  for select using (true);

drop policy if exists "admin manages cnc lessons" on public.cnc_lessons;
create policy "admin manages cnc lessons" on public.cnc_lessons
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- Dữ liệu 9 bài hiện có, chuyển từ CNC_COURSE_ITEMS (topics + lessonContent → body_html).
insert into public.cnc_lessons (id, title, short_title, duration_label, emphasis, body_html, resources, sort_order) values (
  'intro',
  'Phần mở đầu',
  'Thông tin chung',
  'Quy định xưởng',
  NULL,
  '<h3>Nội dung</h3><ul><li>Đề cương chi tiết học phần MĐ CNC.</li><li>Tiêu chí đánh giá và quy đổi điểm số.</li><li>Hướng dẫn an toàn lao động và quy trình 5S.</li></ul>',
  '["Đề cương chi tiết học phần MĐ CNC.","Tiêu chí đánh giá và quy đổi điểm số.","Hướng dẫn an toàn lao động và quy trình 5S."]'::jsonb,
  0
)
on conflict (id) do update set
  title = excluded.title,
  short_title = excluded.short_title,
  duration_label = excluded.duration_label,
  emphasis = excluded.emphasis,
  body_html = excluded.body_html,
  resources = excluded.resources,
  sort_order = excluded.sort_order;

insert into public.cnc_lessons (id, title, short_title, duration_label, emphasis, body_html, resources, sort_order) values (
  'lesson-1',
  'Bài 1: Giới thiệu chung về máy tiện phay CNC',
  'Giới thiệu CNC',
  '2 tiết',
  NULL,
  '<h3>1. Quá trình phát triển của máy CNC</h3><p>Máy công cụ phát triển từ máy vạn năng lên máy NC. Khi máy NC được bổ sung cụm vi tính, bộ xử lý và phương pháp điều khiển theo đường biên, máy NC (Numerical Control) phát triển thành máy CNC (Computer Numerical Control).</p><ul><li>Máy vạn năng: người vận hành trực tiếp điều khiển các chuyển động gia công.</li><li>Máy NC: hoạt động theo chương trình điều khiển số đã được thiết lập.</li><li>Máy CNC: sử dụng máy tính và bộ xử lý để điều khiển, lưu trữ và hiệu chỉnh chương trình linh hoạt.</li></ul><h3>2. Cấu tạo chung của máy CNC</h3><p>Máy CNC gồm hai phần chính: phần điều khiển và phần chấp hành. Hai phần trao đổi tín hiệu về chuyển động, vận tốc, vị trí và trạng thái lỗi trong suốt quá trình gia công.</p><ul><li>Phần điều khiển: chương trình điều khiển, bàn phím, màn hình và các cơ cấu điều khiển bằng tay hoặc tự động.</li><li>Phần chấp hành: máy cắt kim loại và các cơ cấu tự động hóa như tay máy, ổ chứa dao, hệ thống cấp phôi và hút phoi.</li><li>Đầu vào là phôi và chương trình; đầu ra là chi tiết được gia công theo yêu cầu kỹ thuật.</li></ul><h3>3. Các bộ phận chính của máy tiện và máy phay CNC</h3><p>Phần chấp hành của máy tiện CNC và máy phay CNC có kết cấu khác nhau để phù hợp với chuyển động tạo hình đặc trưng của từng loại máy.</p><ul><li>Máy tiện CNC: băng máy, trục chính, mâm dao, động cơ bàn dao ngang, động cơ xoay dao, động cơ bàn dao dọc, bộ truyền trục chính, bàn dao ngang và ụ động.</li><li>Máy phay CNC: trục chính, ổ tích dao, cơ cấu thay dao, bảng điều khiển, bàn máy, động cơ dẫn động và đế máy.</li></ul><h3>4. Đặc tính kỹ thuật của máy CNC</h3><p>Máy tiện và máy phay CNC có khả năng tự động hóa và tập trung nguyên công cao, phù hợp với sản xuất chính xác và các biên dạng phức tạp.</p><ul><li>Tự động hóa cao và giảm sự phụ thuộc vào thao tác trực tiếp của người vận hành.</li><li>Linh hoạt khi thay đổi sản phẩm thông qua việc thay đổi chương trình.</li><li>Tập trung nhiều nguyên công trên một lần gá đặt.</li><li>Đảm bảo độ chính xác và chất lượng bề mặt cao.</li><li>Gia công được các biên dạng phức tạp.</li><li>Mang lại hiệu quả kinh tế và kỹ thuật khi tổ chức sản xuất phù hợp.</li></ul><h3>5. Hệ trục tọa độ trên máy CNC</h3><p>Vị trí và chuyển động trên máy CNC được mô tả chủ yếu bằng hệ tọa độ Đề-các X, Y, Z. Chiều dương của các trục được xác định theo quy tắc bàn tay phải và quy ước dụng cụ cắt chuyển động tương đối so với chi tiết.</p><p>Máy CNC hiện đại cũng cho phép lập trình theo tọa độ cực, trong đó vị trí được xác định bằng bán kính và góc quay; cách biểu diễn này thuận tiện cho các chi tiết có vị trí phân bố theo vòng tròn.</p><ul><li>Trục Z trùng với trục chính của máy.</li><li>Máy tiện: chiều +Z hướng ra xa mâm cặp; trục X biểu diễn chuyển động theo phương đường kính; máy tiện cơ bản không có trục Y.</li><li>Máy phay: các trục X, Y nằm trên mặt bàn máy; trục Z theo phương trục chính.</li><li>Ví dụ tọa độ cực: P1 (R100, 30°), P2 (R100, 150°), P3 (R100, 270°).</li></ul><h3>6. Các điểm chuẩn trên máy CNC</h3><p>Để điều khiển quỹ đạo chạy dao, cần xác lập quan hệ tọa độ giữa máy, phôi và mũi dao. Máy tiện và máy phay CNC cùng sử dụng các điểm chuẩn M, W, R, N/T và P.</p><ul><li>M — Machine zero point: điểm gốc tọa độ máy, do nhà sản xuất xác định và không thay đổi.</li><li>W — Workpiece zero point: điểm gốc tọa độ chi tiết/phôi, thay đổi theo cách gá và yêu cầu lập trình.</li><li>R — Reference point: điểm chuẩn tham chiếu, là vị trí chuẩn cố định để máy xác lập tọa độ.</li><li>N/T — Tool reference point: điểm chuẩn dao, nằm tại vị trí chuẩn của ổ hoặc cơ cấu gá dao.</li><li>P — Cutter point: điểm đỉnh mũi dao trực tiếp tạo hình bề mặt, thay đổi theo dụng cụ.</li></ul><h3>7. Lắp đặt, bảo quản và bảo dưỡng máy CNC</h3><p>Sinh viên phải bảo quản máy, phụ tùng và vật tư trong toàn bộ thời gian thực tập, đồng thời thực hiện đúng quy định vệ sinh và bảo dưỡng của xưởng.</p><ul><li>Kiểm tra máy và phụ tùng thiết bị ngay khi được phân máy.</li><li>Bảo quản vật tư, thiết bị trong suốt quá trình thực tập.</li><li>Cuối ca thực hiện vệ sinh và tra dầu nhớt; cuối tuần tổng vệ sinh máy và xưởng.</li></ul><h3>8. Bài tập củng cố</h3><p>Hoàn thành các câu hỏi sau để hệ thống hóa kiến thức của Bài 1.</p><ul><li>So sánh những điểm giống và khác nhau cơ bản giữa máy tiện vạn năng và máy tiện CNC.</li><li>Trình bày và phân tích các điểm chuẩn trên máy tiện CNC.</li><li>Xác định tọa độ các điểm P1–P7 trên biên dạng chi tiết tiện theo bản vẽ bài tập.</li></ul><h3>Hướng dẫn giảng dạy</h3><p>Sinh viên đã được học kiến thức cơ bản ở học phần Máy cắt kim loại và Điều khiển chương trình số. Giảng viên trình bày nhanh, khái quát phần lý thuyết để chuyển trọng tâm sang các nội dung thực hành tiếp theo.</p><h3>Đánh giá</h3><p>Sinh viên thảo luận và viết bài thu hoạch theo nhóm tại nhà, nộp vào ngày hôm sau.</p><ul><li>Trình bày các đặc tính kỹ thuật cơ bản của máy tiện CNC Turn 55 và máy phay CNC Mill 55.</li><li>So sánh những điểm giống và khác nhau cơ bản giữa máy tiện, máy phay truyền thống tại xưởng trường với máy tiện CNC Turn 55 và máy phay CNC Mill 55.</li></ul><p>Chấm như một bài tự luận theo thang điểm 10.</p>',
  '[]'::jsonb,
  1
)
on conflict (id) do update set
  title = excluded.title,
  short_title = excluded.short_title,
  duration_label = excluded.duration_label,
  emphasis = excluded.emphasis,
  body_html = excluded.body_html,
  resources = excluded.resources,
  sort_order = excluded.sort_order;

insert into public.cnc_lessons (id, title, short_title, duration_label, emphasis, body_html, resources, sort_order) values (
  'lesson-2',
  'Bài 2: Lập trình tiện CNC với Win-NC32 / FANUC 21T',
  'Lập trình tiện',
  '8 tiết',
  NULL,
  '<h3>1. Các điểm chuẩn trên máy tiện CNC</h3><p>Việc lập trình và cài đặt máy tiện CNC dựa trên mối quan hệ giữa hệ tọa độ máy, hệ tọa độ phôi và vị trí thực của mũi dao.</p><ul><li>M — Machine zero point: điểm gốc tọa độ máy, cố định và không thay đổi.</li><li>W — Workpiece zero point: điểm gốc tọa độ chi tiết/phôi, thay đổi theo cách gá và yêu cầu lập trình.</li><li>R — Reference point: điểm chuẩn tham chiếu của máy, không thay đổi.</li><li>T/N — Tool reference point: điểm chuẩn dao, không thay đổi.</li><li>P — Cutter point: điểm đỉnh mũi dao trực tiếp tạo hình, thay đổi theo dụng cụ.</li></ul><h3>2. Cấu trúc chương trình tiện NC — FANUC 21T</h3><p>Chương trình NC gồm chương trình chính và chương trình con. Các khối lệnh được thực hiện tuần tự; chương trình chính có thể gọi chương trình con để tổ chức các phần gia công lặp lại.</p><p>Tên chương trình gồm chữ O và bốn chữ số, ví dụ O1601. Khối lệnh tổng quát có dạng N_G_X_Y_Z_M_S_F_T_; và kết thúc bằng dấu chấm phẩy.</p><ul><li>N: số thứ tự câu lệnh; G: chức năng chuẩn bị.</li><li>X, Y, Z: vị trí tọa độ; trên máy tiện chủ yếu sử dụng X và Z.</li><li>M: lệnh phụ; S: tốc độ trục chính; F: lượng chạy dao; T: chọn dụng cụ cắt.</li><li>G90 lập trình tọa độ tuyệt đối; G91 lập trình tọa độ tương đối so với điểm trước đó.</li></ul><h3>3. Mặt phẳng, đơn vị và các lệnh dịch chuyển cơ bản</h3><p>Hệ tọa độ gia công gồm ba trục X, Y, Z và các mặt phẳng XOY, XOZ, YOZ. Khi tiện, mặt phẳng làm việc chính là XOZ (G18).</p><ul><li>G17/G18/G19: chọn lần lượt mặt phẳng XOY, XOZ và YOZ.</li><li>G70: đơn vị inch; G71: đơn vị hệ mét.</li><li>G94: lượng chạy dao mm/phút; G95: lượng chạy dao mm/vòng, thường dùng khi tiện.</li><li>G00 X(U)… Z(W)…: chạy dao nhanh không cắt; X, Z là tọa độ tuyệt đối, U, W là tọa độ tương đối.</li><li>G01 X(U)… Z(W)… F…: nội suy đường thẳng, dùng để tiện mặt đầu, trụ, côn, rãnh, khoan và doa; có thể dùng R để bo góc hoặc C để vát góc.</li><li>G02/G03 X(U)… Z(W)… I… K… F… hoặc dùng R: nội suy cung tròn cùng/ngược chiều kim đồng hồ.</li></ul><h3>4. Bù trừ bán kính mũi dao</h3><p>Bù trừ bán kính mũi dao giúp đường tâm dao được hiệu chỉnh để biên dạng thực đạt đúng kích thước yêu cầu khi tiện ngoài, tiện trong và gia công cung tròn.</p><ul><li>G40: hủy bù trừ bán kính dao.</li><li>G41: bù trừ bán kính dao về bên trái quỹ đạo lập trình.</li><li>G42: bù trừ bán kính dao về bên phải quỹ đạo lập trình.</li><li>Phải chọn đúng G41/G42 theo hướng chạy dao và vị trí mũi dao; hủy bù bằng G40 trước khi rút dao.</li></ul><h3>5. Các chu trình tiện cơ bản</h3><p>Chu trình giúp rút gọn chương trình và tổ chức tự động các lượt cắt thô, cắt tinh, cắt rãnh và tiện ren.</p><ul><li>G73: chu trình tiện thô dọc trục, bóc hết lượng dư theo biên dạng từ khối P đến Q; khai báo chiều sâu cắt U, khoảng rút dao R và lượng dư tinh U/W.</li><li>G72 P… Q…: chu trình tiện tinh dọc trục theo biên dạng đã được xác định trong khối P–Q.</li><li>G77: chu trình cắt rãnh theo phương X; khai báo điểm cuối X(U), Z(W), chiều sâu cắt P, bước dịch theo Z là Q và lượng dịch ngang R.</li><li>G78: chu trình tiện ren ngoài, ren lỗ hoặc ren côn; khai báo số lần cắt tinh, góc ren, chiều sâu lát cắt nhỏ nhất, chiều sâu ren và bước ren F.</li><li>Khi dùng G73, khối bắt đầu và kết thúc vùng biên dạng phải được tổ chức đúng, đồng thời bố trí G00 an toàn trước và sau chu trình.</li></ul><h3>6. Chu trình khoan trên máy tiện</h3><p>Các lệnh khoan quy định mặt phẳng lùi dao, chiều sâu, lượng ăn dao từng bước và thời gian dừng ở đáy lỗ.</p><ul><li>G98: sau khi khoan, dao trở về mặt phẳng ban đầu.</li><li>G99: sau khi khoan, dao trở về mặt phẳng tham chiếu R.</li><li>G83 X(U)… Z(W)… R… Q… P… F… M… K…: chu trình khoan lỗ sâu; Q là chiều sâu mỗi lần cắt, P là thời gian dừng đáy lỗ và K là số lần lặp.</li><li>G80: hủy chu trình khoan đang hoạt động.</li></ul><h3>7. Mã lệnh M dùng trong chương trình tiện</h3><p>Mã M điều khiển các chức năng phụ của máy, trục chính, dung dịch làm mát, mâm cặp, ụ động và luồng thực hiện chương trình.</p><ul><li>M00 dừng vô điều kiện; M01 dừng có điều kiện; M30 kết thúc và trở về đầu chương trình.</li><li>M03/M04/M05: quay thuận, quay nghịch và dừng trục chính; M06: thay dao.</li><li>M08/M09: bật/tắt dung dịch tưới nguội; M71/M72: bật/tắt thổi phoi.</li><li>M20/M21: lùi/đẩy nòng ụ động; M25/M26: mở/đóng chấu mâm cặp.</li><li>M98 gọi chương trình con; M99 kết thúc chương trình con.</li></ul><h3>8. Bài tập lập trình tiện</h3><p>Bài tập 1 và 2 yêu cầu viết chương trình gia công hoàn chỉnh từ bản vẽ biên dạng, lựa chọn dao, chế độ cắt và kiểm tra quỹ đạo trên phần mềm mô phỏng.</p><ul><li>Bài tập 1: tiện thô bằng dao T0202, n = 800 vòng/phút, F = 0,2 mm/vòng, chiều sâu cắt 1 mm; tiện tinh bằng dao T0404, n = 1000 vòng/phút, F = 0,1 mm/vòng, chiều sâu cắt 0,5 mm.</li><li>Chương trình mẫu sử dụng G90, G71, G18, G95; tiện mặt đầu; chu trình G73; biên dạng G01; bù dao G41/G40; chu trình tiện tinh G72 và kết thúc M30.</li><li>Bài tập 2: lập trình biên dạng có vát và hai cung chuyển tiếp bằng G02/G03; sử dụng cùng bộ thông số dao thô–dao tinh, lượng dư tinh U0.5/W0.5.</li><li>Yêu cầu kiểm tra: đúng gốc W, đúng thứ tự dao, đúng chiều trục chính, không va chạm, mô phỏng đạt trước khi xuất file .NC.</li></ul>',
  '["Link tải phần mềm Win-NC32.","Video lập trình mẫu."]'::jsonb,
  2
)
on conflict (id) do update set
  title = excluded.title,
  short_title = excluded.short_title,
  duration_label = excluded.duration_label,
  emphasis = excluded.emphasis,
  body_html = excluded.body_html,
  resources = excluded.resources,
  sort_order = excluded.sort_order;

insert into public.cnc_lessons (id, title, short_title, duration_label, emphasis, body_html, resources, sort_order) values (
  'lesson-3',
  'Bài 3: Lập trình phay CNC với Win-NC32 / FANUC 21M',
  'Lập trình phay',
  '8 tiết',
  NULL,
  '<h3>1. Các điểm chuẩn trên máy phay CNC</h3><p>Lập trình phay CNC yêu cầu xác định rõ hệ tọa độ máy, hệ tọa độ phôi và điểm chuẩn của từng dụng cụ trước khi tạo quỹ đạo cắt.</p><ul><li>M — Machine zero point: gốc tọa độ máy, cố định.</li><li>W — Workpiece zero point: gốc tọa độ phôi, thay đổi theo cách gá và chương trình.</li><li>R — Reference point: điểm tham chiếu cố định của máy.</li><li>T/N — Tool reference point: điểm chuẩn dao, không thay đổi.</li><li>P — Cutter point: điểm đỉnh mũi dao thực hiện cắt gọt, thay đổi theo dụng cụ.</li></ul><h3>2. Cấu trúc chương trình phay NC — FANUC 21M</h3><p>Chương trình phay gồm chương trình chính và chương trình con, được thực hiện theo thứ tự các khối lệnh. Tên chương trình có dạng Oxxxx, ví dụ O1601.</p><p>Khối lệnh tổng quát có dạng N_G_X_Y_Z_M_S_F_T_; và kết thúc bằng dấu chấm phẩy.</p><ul><li>N: số thứ tự; G: chức năng chuẩn bị; X/Y/Z: tọa độ vị trí.</li><li>M: chức năng phụ; S: tốc độ trục chính; F: tốc độ chạy dao; T: chọn dụng cụ.</li><li>G90: lập trình tọa độ tuyệt đối so với chuẩn phôi; G91: lập trình lượng dịch chuyển tương đối so với điểm trước.</li><li>Khi chuẩn W đặt tại tâm, phải xác định đúng dấu của X, Y và chiều sâu Z cho từng điểm biên dạng.</li></ul><h3>3. Mặt phẳng, đơn vị và lệnh dịch chuyển</h3><p>Máy phay sử dụng đầy đủ ba trục X, Y, Z. Việc chọn đúng mặt phẳng nội suy quyết định ý nghĩa của tọa độ cung tròn và hướng chuyển động.</p><ul><li>G17/G18/G19: chọn mặt phẳng XOY, XOZ và YOZ; phay biên dạng thông dụng thường dùng G17.</li><li>G70: đơn vị inch; G71: đơn vị hệ mét.</li><li>G94: lượng chạy dao mm/phút, thường dùng khi phay; G95: lượng chạy dao mm/vòng.</li><li>G00 X… Y… Z…: chạy dao nhanh không cắt.</li><li>G01 X… Y… Z… F…: nội suy đường thẳng; có thể dùng R để bo góc hoặc C để vát góc.</li><li>G02/G03 X… Y… Z… I… J… K… F… hoặc dùng R: nội suy cung tròn cùng/ngược chiều kim đồng hồ.</li></ul><h3>4. Bù bán kính và bù chiều dài dao</h3><p>Bù dao cho phép chương trình mô tả biên dạng chi tiết trong khi bộ điều khiển tự hiệu chỉnh theo kích thước và chiều dài thực của dụng cụ.</p><ul><li>G40: hủy bù bán kính; G41/G42: bù bán kính dao trái/phải theo hướng chạy dao.</li><li>G41, G42 đi kèm địa chỉ H để chọn ô dữ liệu bù bán kính, ví dụ G41 H2.</li><li>G43: bù chiều dài dao theo hướng dương; G44: bù theo hướng âm; G49: hủy bù chiều dài.</li><li>G43/G44 đi kèm H để chọn ô dữ liệu chiều dài dao, ví dụ G43 H12.</li><li>Phải gọi bù tại vị trí tiếp cận an toàn và hủy bù trước khi kết thúc/rút dao khỏi biên dạng.</li></ul><h3>5. Chu trình khoan G81, G83 và G73</h3><p>Các chu trình khoan cố định giúp lập trình nhiều lỗ bằng cách khai báo một lần các thông số chiều sâu, mặt phẳng an toàn và lượng tiến dao.</p><ul><li>G98: trở về mặt phẳng ban đầu; G99: trở về mặt phẳng tham chiếu R sau mỗi lỗ.</li><li>G81 X… Y… Z… R… F…: khoan hết chiều sâu trong một lần tiến dao.</li><li>G83 X… Y… Z… R… P… Q… F… K…: khoan lỗ sâu; Q là chiều sâu mỗi lát cắt, P là thời gian dừng đáy lỗ, K là số lần lặp.</li><li>G73 X… Y… Z… R… P… Q… F…: chu trình khoan cao tốc, rút dao ngắn để bẻ và thoát phoi.</li><li>X/Y xác định tâm lỗ; Z xác định chiều sâu; R là khoảng an toàn tính từ mặt phôi.</li></ul><h3>6. Chu trình tarô và doa</h3><p>Chu trình tarô và doa sử dụng cùng cấu trúc vị trí lỗ, chiều sâu và mặt phẳng an toàn nhưng khác phương thức chuyển động của trục chính và dụng cụ.</p><ul><li>G84: tarô ren phải; G74: tarô ren trái; cấu trúc gồm X, Y, Z, R, P, F và K.</li><li>Khi tarô, tốc độ tiến dao phải đồng bộ với tốc độ trục chính và bước ren.</li><li>G89 X… Y… Z… R… P… F… K…: chu trình doa, có dừng P tại đáy lỗ trước khi rút dao.</li><li>Kết thúc nhóm chu trình cố định phải hủy chu trình trước khi chuyển sang chuyển động khác.</li></ul><h3>7. Mã lệnh M dùng trong chương trình phay</h3><p>Mã M điều khiển trục chính, thay dao, làm mát, cơ cấu kẹp phôi, đầu phân độ và kết thúc chương trình.</p><ul><li>M00 dừng vô điều kiện; M01 dừng có điều kiện; M30 kết thúc chương trình.</li><li>M03/M04/M05: quay thuận, quay nghịch và dừng trục chính; M06: thay dao.</li><li>M08/M09: bật/tắt dung dịch tưới nguội; M71/M72: bật/tắt thổi phoi.</li><li>M10/M11: khóa/mở khóa đầu phân độ; M19: xác định vị trí dừng trục chính.</li><li>M25/M26: mở ê-tô và siết ê-tô kẹp phôi.</li></ul><h3>8. Bài tập lập trình phay</h3><p>Bài tập yêu cầu phay biên dạng ngoài sâu 2 mm và khoan bốn lỗ sâu 6 mm theo bản vẽ, sử dụng hai dụng cụ và kiểm tra toàn bộ chương trình bằng mô phỏng.</p><ul><li>Chương trình O0005 chọn G17, G90; gọi dao T02, bù chiều dài G43 H02, trục chính S1000 M03 và tiếp cận từ vị trí an toàn.</li><li>Phay biên dạng dùng G01 kết hợp G02, bù bán kính G41 H12 và hủy bù bằng G40 sau khi hoàn thành đường bao.</li><li>Khoan bốn lỗ dùng dao T04, bù chiều dài G43 H04 và chu trình G99 G73 với Z-6, R5, P1000, Q3, F100.</li><li>Các tâm lỗ lần lượt tại X12 Y25, X25 Y38, X38 Y25 và X25 Y12; chương trình kết thúc bằng M30.</li><li>Yêu cầu nộp file .NC và ảnh chụp mô phỏng 3D sau khi kiểm tra không còn va chạm hoặc lỗi quỹ đạo.</li></ul>',
  '[]'::jsonb,
  3
)
on conflict (id) do update set
  title = excluded.title,
  short_title = excluded.short_title,
  duration_label = excluded.duration_label,
  emphasis = excluded.emphasis,
  body_html = excluded.body_html,
  resources = excluded.resources,
  sort_order = excluded.sort_order;

insert into public.cnc_lessons (id, title, short_title, duration_label, emphasis, body_html, resources, sort_order) values (
  'lesson-4-turn',
  'Bài 4: Vận hành và cài đặt máy tiện CNC EMCO TURN 55',
  'Vận hành máy tiện',
  '9 tiết',
  'Trọng tâm cài đặt dao tiện, mâm cặp và gốc phôi',
  '<h3>1. Cấu tạo máy tiện CNC EMCO TURN 55</h3><p>Máy tiện CNC gồm hai phần chính: phần điều khiển tiếp nhận chương trình và lệnh của người vận hành; phần chấp hành thực hiện các chuyển động cắt gọt để tạo thành chi tiết.</p><ul><li>Phần điều khiển: tủ điều khiển, màn hình, bàn phím máy CNC, bàn phím máy tính và thùng CPU.</li><li>Phần chấp hành: băng máy, trục chính, mâm dao, động cơ bàn dao ngang, động cơ xoay dao, động cơ bàn dao dọc, cơ cấu phân độ trục chính, động cơ trục chính, bàn dao ngang và ụ động.</li><li>Dụng cụ, phụ kiện và thiết bị đo phải được đặt đúng vị trí trong tủ dụng cụ sau khi sử dụng.</li></ul><h3>2. Kiểm tra máy trước khi cấp điện</h3><p>Trước khi đóng điện, người vận hành phải quan sát toàn bộ máy và khu vực làm việc để phát hiện vật cản, hư hỏng hoặc trạng thái không an toàn.</p><ul><li>Kiểm tra tủ điện, thân máy tiện CNC và khu vực băng máy.</li><li>Kiểm tra mâm cặp, chấu cặp, ổ gá dao/mâm dao và ụ động.</li><li>Kiểm tra nút dừng khẩn cấp, cửa che chắn và vùng hành trình dao.</li><li>Kiểm tra màn hình, bàn phím CNC, bàn phím máy tính và thùng CPU.</li><li>Bảo đảm không còn chìa khóa mâm cặp, dụng cụ hoặc vật lạ trong vùng quay.</li></ul><h3>3. Mở máy, về chuẩn tham chiếu và di chuyển JOG</h3><p>Máy chỉ được thao tác sau khi mở đúng trình tự và hoàn thành việc đưa các trục về chuẩn tham chiếu Reference.</p><ul><li>Đóng CP của máy tiện CNC; nhấn Power của máy tính; mở phần mềm WinNC FANUC 21T.</li><li>Chọn chế độ Reference, đặt phần trăm bước tiến phù hợp và nhấn phím Reference để đưa máy về chuẩn.</li><li>Chuyển sang JOG; điều chỉnh phần trăm bước tiến; dùng +X, -X, +Z, -Z để di chuyển dao theo hai trục.</li><li>Luôn quan sát khoảng cách giữa dao, phôi, mâm cặp và ụ động khi di chuyển bằng tay.</li></ul><h3>4. Trục chính, mâm dao và thao tác MDI</h3><p>Chế độ MDI được dùng để gọi dao, thay dao và ra lệnh quay trục chính trước khi thực hiện các thao tác cài đặt hoặc gia công bằng tay.</p><ul><li>M03: trục chính quay cùng chiều kim đồng hồ; M04: quay ngược chiều kim đồng hồ; kiểm tra chiều quay trước khi tiếp cận phôi.</li><li>Dùng phím quay dao để kiểm tra vị trí và số lượng dao trên mâm dao.</li><li>Chọn MDI, mở Program MDI, nhập T0202 M6; và M3 S500; rồi chạy từng câu lệnh.</li><li>Sau khi gọi đúng dao và xác nhận trục chính quay đúng chiều, chuyển sang JOG để thao tác X, Z bằng tay.</li></ul><h3>5. Gá phôi và gá dao tiện</h3><p>Phôi và dao phải được gá chắc chắn, đúng tâm và không gây cản trở hành trình máy trước khi cho trục chính quay.</p><ul><li>Dùng chấu thuận để kẹp phôi nhỏ; dùng chấu ngược để kẹp phôi lớn; lựa chọn chiều dài nhô ra phù hợp.</li><li>Mâm dao có thể gá tám dao, gồm dao tiện ngoài, dao cắt rãnh, dao tiện ren ngoài, dao tiện lỗ, dao ren lỗ và mũi khoan.</li><li>Gá đúng chiều dao, siết chặt bằng lục giác và dùng căn chêm để canh tâm mũi dao.</li><li>Quay thử mâm cặp ở tốc độ thấp và kiểm tra khoảng hở trước khi gia công.</li></ul><h3>6. Bài tập vận hành tiện bằng tay</h3><p>Sinh viên vận hành máy ở chế độ JOG/MDI, căn cứ tọa độ hiển thị để tiện chi tiết và đo kiểm sau gia công.</p><ul><li>Vạt mặt đầu để đạt chiều dài 60 ± 0,1 mm.</li><li>Tiện trụ đạt đường kính Ø18 ± 0,1 mm trên chiều dài 20 ± 0,1 mm.</li><li>Theo dõi tọa độ X, Z trong suốt quá trình, sử dụng bước tiến nhỏ khi dao gần phôi.</li><li>Đo kiểm chiều dài và đường kính bằng dụng cụ đo phù hợp; ghi nhận sai lệch và hiệu chỉnh thao tác.</li></ul><h3>7. Điểm chuẩn và xóa dữ liệu cài đặt cũ</h3><p>Trước khi cài đặt cho phôi và bộ dao mới, phải xác định đúng các điểm M, W, R, N/T, P và xóa các giá trị cũ để tránh dùng nhầm dữ liệu của lần gá trước.</p><ul><li>M: gốc máy; W: gốc phôi; R: điểm tham chiếu; N/T: chuẩn dao; P: đỉnh mũi dao.</li><li>Vào Offset Setting → Work Shift để xóa dữ liệu X, Z của phôi.</li><li>Vào Offset Setting → Offset Geometry để xóa dữ liệu X, Z, R, T của dao.</li><li>Chỉ xóa và nhập dữ liệu khi đã xác nhận đúng trang, đúng hàng dao và đúng đơn vị.</li></ul><h3>8. Cài đặt gốc phôi W trên máy tiện</h3><p>Cài đặt phôi là dịch hệ tọa độ từ gốc máy M sang gốc chi tiết W. Tài liệu hướng dẫn hai phương pháp xác lập giá trị Z của Work Shift.</p><ul><li>Cách 1 — đo trực tiếp: xác định kích thước mâm cặp MA và khoảng cách từ mâm cặp đến mặt đầu phôi AW; nhập Zphôi = MW = MA + AW với đúng dấu tọa độ.</li><li>Cách 2 — chạm dao: vào MDI cho phôi quay, chuyển JOG, đưa dao chạm nhẹ mặt đầu phôi theo Z.</li><li>Nhấn POS để đọc Zmachine, đổi dấu theo quy ước rồi nhập vào giá trị Z của Shift Value.</li><li>Sau khi nhập, rút dao về vị trí an toàn và kiểm tra lại gốc W trên màn hình Position.</li></ul><h3>9. Cài đặt Geometry Offset dao theo Z và X</h3><p>Mỗi dao phải được đo riêng để dịch từ điểm chuẩn dao N đến đỉnh mũi dao P. Ví dụ dùng dao số 2 và lưu dữ liệu tại hàng Geometry số 2.</p><ul><li>Gọi dao trong MDI bằng T0202 M6; cho trục chính quay M3 hoặc M4 S500; sau đó chuyển JOG.</li><li>Theo Z: cho dao chạm mặt đầu phôi, tại hàng 2 nhập Z0 và nhấn Measure; quan hệ Zdao2 = Zmachine2 − Zphôi.</li><li>Theo X: cho dao chạm nhẹ đường kính đã biết của phôi, tại hàng 2 nhập giá trị X và nhấn Measure; quan hệ Xdao2 = Xmachine2 − Xphôi.</li><li>Nhập đúng bán kính và hướng mũi dao nếu chương trình sử dụng bù bán kính mũi dao.</li></ul><h3>10. Kiểm tra cài đặt trước khi chạy máy tiện</h3><p>Sau khi cài đặt, phải kiểm tra ở chế độ MDI và chạy từng khối với bước tiến thấp; không chuyển sang gia công tự động nếu vị trí thực không trùng với tọa độ dự kiến.</p><ul><li>Gọi đúng dao: T0202 M6; và quay trục chính M3 S500;.</li><li>Tiếp cận thử: G0 X20 Z5; sau đó G1 X20 Z0 F0.2;.</li><li>Quan sát khoảng cách dao–phôi–mâm cặp, tọa độ Position và chiều chuyển động của từng trục.</li><li>Nếu có sai lệch hoặc nguy cơ va chạm, dừng ngay, rút dao và kiểm tra lại Work Shift/Geometry Offset.</li></ul>',
  '["Video giáo viên thị phạm quy trình mở máy tiện và cài đặt dao, phôi."]'::jsonb,
  4
)
on conflict (id) do update set
  title = excluded.title,
  short_title = excluded.short_title,
  duration_label = excluded.duration_label,
  emphasis = excluded.emphasis,
  body_html = excluded.body_html,
  resources = excluded.resources,
  sort_order = excluded.sort_order;

insert into public.cnc_lessons (id, title, short_title, duration_label, emphasis, body_html, resources, sort_order) values (
  'lesson-4-mill',
  'Bài 5: Vận hành và cài đặt máy phay CNC EMCO MILL 55',
  'Vận hành máy phay',
  '9 tiết',
  'Trọng tâm cài đặt dao phay, ê-tô và gốc phôi G54',
  '<h3>1. Cấu tạo máy phay CNC EMCO MILL 55</h3><p>Máy phay CNC gồm phần điều khiển và phần chấp hành. Phần điều khiển xử lý chương trình; phần chấp hành tạo chuyển động tương đối giữa dao và phôi.</p><ul><li>Phần điều khiển: tủ điều khiển, màn hình, bàn phím CNC, bàn phím máy tính và thùng CPU.</li><li>Phần chấp hành: trục chính, ổ tích dao, cơ cấu thay dao, bảng điều khiển, bàn máy, động cơ dẫn động và đế máy.</li><li>Dụng cụ, collet, thiết bị đo và phụ kiện phải được vệ sinh, kiểm đếm và đặt đúng vị trí trong tủ.</li></ul><h3>2. Kiểm tra máy phay trước khi cấp điện</h3><p>Trước khi mở máy, người vận hành phải quan sát khu vực làm việc và xác nhận các bộ phận ở trạng thái an toàn.</p><ul><li>Kiểm tra nút dừng khẩn cấp, cửa bảo vệ và không gian hành trình các trục.</li><li>Kiểm tra trục chính, ổ gá dao/ổ tích dao và cơ cấu thay dao.</li><li>Kiểm tra ê-tô, bàn máy, phôi, đồ gá và vật cản trong vùng gia công.</li><li>Kiểm tra màn hình, bàn phím CNC, bàn phím máy tính, chuột và thùng CPU.</li><li>Bảo đảm dao được kẹp chắc, đúng chiều dài và không có người/vật trong vùng chuyển động.</li></ul><h3>3. Mở máy, về Reference và di chuyển JOG</h3><p>Máy phải được mở đúng trình tự và đưa về điểm tham chiếu trước khi gọi dao, cài đặt phôi hoặc chạy chương trình.</p><ul><li>Đóng CP của máy; nhấn Power máy tính; mở phần mềm WinNC FANUC 21M.</li><li>Chọn Reference, đặt phần trăm bước tiến phù hợp và nhấn phím Reference.</li><li>Chuyển sang JOG; dùng +X, -X, +Y, -Y, +Z, -Z để di chuyển dao theo ba trục.</li><li>Khi dao gần phôi, ê-tô hoặc đồng hồ đo, giảm bước tiến và thao tác từng bước có kiểm soát.</li></ul><h3>4. Trục chính, thay dao và thao tác MDI</h3><p>Chế độ MDI cho phép gọi dao, thay dao và chạy trục chính bằng từng câu lệnh để chuẩn bị cài đặt hoặc gia công bằng tay.</p><ul><li>M03/M04 điều khiển trục chính quay thuận/nghịch; xác nhận đúng chiều quay của dụng cụ.</li><li>Dùng nút tháo dao theo đúng quy trình, giữ chắc chuôi dao và tránh đứng dưới dụng cụ.</li><li>Chọn MDI, mở Program MDI, nhập T02 M6; và M3 S500; rồi chạy câu lệnh.</li><li>Sau khi gọi đúng dao, có thể chuyển sang JOG để di chuyển X, Y, Z bằng tay.</li></ul><h3>5. Gá phôi và gá dao phay</h3><p>Gá đặt phải bảo đảm định vị đúng, kẹp chặt và tạo khoảng hở an toàn cho dao, trục chính và ê-tô trong toàn bộ hành trình.</p><ul><li>Vệ sinh ê-tô và phôi; định vị phôi đủ sáu bậc tự do; siết ê-tô chắc chắn.</li><li>Ổ dao có tám vị trí, có thể gá dao phay mặt đầu, dao phay ngón, mũi khoan và mũi tarô.</li><li>Chọn đúng collet/chấu kẹp, kiểm tra chiều dài nhô dao và siết đúng lực.</li><li>Kiểm tra đường kính, chiều dài dao và nguy cơ va chạm khi thay dao tự động.</li></ul><h3>6. Bài tập vận hành phay bằng tay</h3><p>Sinh viên vận hành máy để phay mặt phẳng theo tọa độ, sau đó đo kiểm kích thước và chất lượng bề mặt.</p><ul><li>Phay mặt đầu đạt kích thước 60 ± 0,1 mm.</li><li>Bề mặt sau phay đạt yêu cầu nhám Rz20.</li><li>Theo dõi tọa độ X, Y, Z và điều chỉnh bước tiến phù hợp khi dao vào/ra phôi.</li><li>Đo kiểm sản phẩm, đối chiếu bản vẽ và ghi nhận nguyên nhân sai lệch nếu chưa đạt.</li></ul><h3>7. Điểm chuẩn và xóa dữ liệu cài đặt cũ</h3><p>Trước khi thiết lập bộ dao và phôi mới, phải xác định các điểm M, W, R, N, P và xóa giá trị cũ để tránh sai lệch hệ tọa độ.</p><ul><li>M: gốc máy; W: gốc phôi; R: điểm tham chiếu; N: chuẩn dao; P: đỉnh mũi dao.</li><li>Vào Offset Setting → Work Shift/Work Coordinates để xóa thông số X, Y, Z của phôi.</li><li>Vào Offset Setting → Offset để xóa thông số chiều dài và bán kính dao.</li><li>Xác nhận đúng hàng dao và hệ tọa độ phôi trước khi nhập số liệu mới.</li></ul><h3>8. Cài đặt chiều dài và bán kính dao số 2</h3><p>Tài liệu sử dụng đồng hồ chuẩn cao 50 mm để đo chiều dài dao. Gốc Z tạm thời được thiết lập theo chiều cao đồng hồ trước khi chạm dao.</p><ul><li>Nhập Zphôi = ZMA + ZAW1 = 50 + 0 = 50 vào Work Shift.</li><li>Trong MDI gọi T2 M6; nhấn POS để theo dõi tọa độ Machine; chuyển JOG và đưa dao vào tâm đồng hồ.</li><li>Giảm bước tiến, cho dao chạm nhẹ mặt trên đồng hồ; tính Zdao2 = Zmachine2 − Zphôi.</li><li>Nhập bù chiều dài dao số 2 tại hàng 2 và nhập bù bán kính Rdao2 tại hàng 12.</li><li>Rút dao và đưa máy về Reference sau khi hoàn tất.</li></ul><h3>9. Cài đặt chiều dài và bán kính dao số 4</h3><p>Dao số 4 được đo độc lập theo cùng phương pháp để bảo đảm mỗi dụng cụ có giá trị chiều dài và bán kính riêng.</p><ul><li>Trong MDI gọi T4 M6; theo dõi tọa độ Machine trên màn hình POS.</li><li>Chuyển JOG, đưa dao vào tâm đồng hồ, giảm bước tiến và chạm nhẹ mặt đồng hồ.</li><li>Tính Zdao4 = Zmachine4 − Zphôi.</li><li>Nhập chiều dài dao tại hàng 4 và bán kính Rdao4 tại hàng 14; sau đó rút dao và về Reference.</li></ul><h3>10. Cài đặt gốc phôi theo Z, X và Y</h3><p>Gốc phôi W được xác lập lần lượt theo ba phương. Khi dò cạnh X/Y bằng dao, phải cộng bán kính dao để chuyển từ tâm dao về bề mặt chuẩn của phôi.</p><ul><li>Theo Z: nhập Zphôi = ZMA + ZAW1; ví dụ máy MILL 55 có ZMA = 28 mm và chiều cao phôi ZAW1 = 50 mm.</li><li>Theo X: gọi T02 M6; M3 S800; chuyển JOG, chạm cạnh trái phôi và tính Xphôi = Xmachine + Rdao.</li><li>Theo Y: chạm cạnh trước phôi, giảm bước tiến và tính Yphôi = Ymachine + Rdao.</li><li>Nhập Xphôi, Yphôi, Zphôi vào Work Shift/Work Coordinates và đưa máy về Reference.</li></ul><h3>11. Kiểm tra cài đặt trước khi chạy máy phay</h3><p>Sau khi cài đặt, phải kiểm tra từng dao tại gốc phôi trong MDI với bù chiều dài tương ứng và tốc độ tiến dao thấp.</p><ul><li>Dao số 2: T02 M6; M3 S500; G43 H2; G0 X0 Y0 Z50; G1 Z0 F200;.</li><li>Dao số 4: T04 M6; M3 S500; G43 H4; G0 X0 Y0 Z50; G1 Z0 F200;.</li><li>Theo dõi Position, kiểm tra đúng dao, đúng H, đúng chiều trục chính và đúng gốc X0 Y0 Z0.</li><li>Nếu dao không đến đúng vị trí hoặc có nguy cơ va chạm, dừng máy và kiểm tra lại Work Shift, chiều dài và bán kính dao.</li></ul>',
  '["Video giáo viên thị phạm quy trình mở máy phay và cài đặt dao, phôi."]'::jsonb,
  5
)
on conflict (id) do update set
  title = excluded.title,
  short_title = excluded.short_title,
  duration_label = excluded.duration_label,
  emphasis = excluded.emphasis,
  body_html = excluded.body_html,
  resources = excluded.resources,
  sort_order = excluded.sort_order;

insert into public.cnc_lessons (id, title, short_title, duration_label, emphasis, body_html, resources, sort_order) values (
  'lesson-5',
  'Bài 6: Gia công tiện CNC',
  'Gia công tiện',
  '17 tiết',
  NULL,
  '<h3>Nội dung</h3><ol><li>Tiện mặt đầu.</li><li>Tiện trụ ngắn, bậc, bo cung vạt cạnh.</li><li>Tiện côn, ren.</li><li>Bài tập tổng hợp.</li></ol>',
  '["Tài liệu: Bản vẽ phôi."]'::jsonb,
  6
)
on conflict (id) do update set
  title = excluded.title,
  short_title = excluded.short_title,
  duration_label = excluded.duration_label,
  emphasis = excluded.emphasis,
  body_html = excluded.body_html,
  resources = excluded.resources,
  sort_order = excluded.sort_order;

insert into public.cnc_lessons (id, title, short_title, duration_label, emphasis, body_html, resources, sort_order) values (
  'lesson-6',
  'Bài 7: Gia công phay CNC',
  'Gia công phay',
  '17 tiết',
  NULL,
  '<h3>Nội dung</h3><ol><li>Phay mặt phẳng.</li><li>Phay bậc, cong, cung.</li><li>Phay theo biên dạng profile.</li><li>Khoan lỗ, Tarô.</li><li>Bài tập tổng hợp.</li></ol>',
  '[]'::jsonb,
  7
)
on conflict (id) do update set
  title = excluded.title,
  short_title = excluded.short_title,
  duration_label = excluded.duration_label,
  emphasis = excluded.emphasis,
  body_html = excluded.body_html,
  resources = excluded.resources,
  sort_order = excluded.sort_order;
