# -*- coding: utf-8 -*-
"""CĐ12 Nhiệt học nâng cao: cân bằng nhiệt và chuyển thể (lesson 153) — Bài tập tự luận (xếp từ dễ đến khó).
Xuất tu_luan() (dict label + body_html) và kiem_so() (assert mọi đáp số).
Tự soạn 16/10/2026, phỏng theo kiểu đề HSG 9 / tuyển sinh 10 chuyên phổ biến, không chép đề cụ thể nào.
Số liệu khác 6 dạng mẫu (153.json, nguon.md) và khác ví dụ trong docx nguồn (nguon.txt).
Hằng số theo quy ước nguon.md: c nước 4200, đá 2100, nhôm 880, đồng 380, thép 460; λ đá 3,4.10^5; L nước 2,3.10^6.
Không có dạng hao phí tỉ lệ thời gian / hiệu nhiệt độ (thuộc CĐ16)."""
from fractions import Fraction as F
from math import isclose, log, ceil

TL = [
 # ── Bài 1 · Dễ: pha nước tắm
 ("Dễ", r"""<p>Mẹ cần $30$ lít nước ấm ở $40\ ^\circ\text{C}$ để tắm cho em bé, pha từ nước sôi $100\ ^\circ\text{C}$ và nước lạnh $25\ ^\circ\text{C}$. Bỏ qua sự trao đổi nhiệt với chậu và môi trường; $1$ lít nước có khối lượng $1\ \text{kg}$.</p>
<p>a) Cần bao nhiêu lít nước sôi và bao nhiêu lít nước lạnh?</p>
<p>b) Trong phích chỉ còn $5$ lít nước sôi, nước lạnh có đủ. Pha được nhiều nhất bao nhiêu lít nước $40\ ^\circ\text{C}$?</p>
<p>c) Thực tế nước trong phích chỉ còn $90\ ^\circ\text{C}$. Muốn có đủ $30$ lít nước $40\ ^\circ\text{C}$ thì phải lấy bao nhiêu lít mỗi loại?</p>""",
  r"""<p>a) Gọi $m_1$, $m_2$ là khối lượng nước sôi và nước lạnh: $m_1+m_2=30\ \text{kg}$.</p>
<p>Nước sôi toả: $Q_{\text{toả}}=m_1c\,(100-40)=60\,m_1c$.</p>
<p>Nước lạnh thu: $Q_{\text{thu}}=m_2c\,(40-25)=15\,m_2c$.</p>
<p>$Q_{\text{toả}}=Q_{\text{thu}}$ nên $60m_1=15m_2$, tức $m_2=4m_1$.</p>
<p>Suy ra $5m_1=30$: $m_1=6\ \text{kg}$ (6 lít nước sôi), $m_2=24\ \text{kg}$ (24 lít nước lạnh).</p>
<p>b) Tỉ lệ vẫn là $m_2=4m_1$: với $m_1=5$ lít thì $m_2=20$ lít, pha được nhiều nhất $25$ lít.</p>
<p>c) $m_1(90-40)=m_2(40-25)$ nên $50m_1=15m_2$, tức $m_2=\dfrac{10}{3}m_1$.</p>
<p>$m_1+\dfrac{10}{3}m_1=30$ nên $m_1=\dfrac{90}{13}\approx6{,}9$ lít và $m_2\approx23{,}1$ lít.</p>
<p>Lỗi hay gặp: lấy trung bình cộng, nghĩ "nửa sôi nửa lạnh" — trộn $15$ lít mỗi loại được $62{,}5\ ^\circ\text{C}$, bỏng da em bé.</p>
<p>Lỗi hay gặp: viết $60m_1=15\cdot30$, quên $m_2=30-m_1$ chứ không phải $30$.</p>"""),

 # ── Bài 2 · Dễ: đo nhiệt dung riêng kim loại bằng nhiệt lượng kế
 ("Dễ", r"""<p>Để xác định nhiệt dung riêng của một kim loại, một nhóm học sinh dùng nhiệt lượng kế bằng đồng khối lượng $120\ \text{g}$ chứa $250\ \text{g}$ nước ở $18\ ^\circ\text{C}$. Thỏi kim loại $200\ \text{g}$ được ngâm lâu trong nồi nước đang sôi (coi là $100\ ^\circ\text{C}$) rồi thả nhanh vào nhiệt lượng kế. Khi cân bằng, nhiệt kế chỉ $24\ ^\circ\text{C}$. Coi như bỏ qua trao đổi nhiệt với môi trường. Cho $c_{\text{đồng}}=380$, $c_{\text{nước}}=4200\ \text{J/(kg·K)}$.</p>
<p>a) Tính nhiệt dung riêng của kim loại.</p>
<p>b) Kim loại đó gần với chất nào nhất trong ba chất: đồng ($380$), thép ($460$), nhôm ($880\ \text{J/(kg·K)}$)? Giả sử kim loại đúng là chất vừa nhận ra, nêu hai nguyên nhân làm kết quả đo nhỏ hơn giá trị trong bảng.</p>
<p>c) Một bạn quên tính nhiệt lượng kế. Bạn đó thu được kết quả bao nhiêu?</p>""",
  r"""<p>a) Nhiệt lượng kế và nước thu nhiệt, tăng từ $18$ lên $24\ ^\circ\text{C}$:</p>
<p>$Q_{\text{thu}}=(0{,}12\cdot380+0{,}25\cdot4200)(24-18)=1095{,}6\cdot6=6573{,}6\ \text{J}$.</p>
<p>Kim loại toả nhiệt, giảm từ $100$ xuống $24\ ^\circ\text{C}$: $Q_{\text{toả}}=0{,}2\cdot c\cdot76=15{,}2\,c$.</p>
<p>$15{,}2\,c=6573{,}6$ nên $c\approx432\ \text{J/(kg·K)}$.</p>
<p>b) $432$ gần $460$ nhất nên kim loại có thể là thép.</p>
<p>Kết quả nhỏ hơn bảng vì: thỏi kim loại nguội bớt trong lúc chuyển từ nồi sang nhiệt lượng kế (thực tế dưới $100\ ^\circ\text{C}$).</p>
<p>Và: một phần nhiệt toả ra không khí qua nắp, thành bình nên $Q_{\text{thu}}$ đo được nhỏ hơn nhiệt kim loại thật sự toả ra.</p>
<p>c) Quên nhiệt lượng kế: $c'=\dfrac{0{,}25\cdot4200\cdot6}{15{,}2}\approx414\ \text{J/(kg·K)}$, lệch thêm gần $4\,\%$.</p>
<p>Lỗi hay gặp: lấy $\Delta t$ của kim loại là $100-18$ (nhiệt độ ban đầu của nước) thay vì $100-24$.</p>"""),

 # ── Bài 3 · Trung bình: dẫn hơi nước vào cốc nước (ngưng tụ)
 ("Trung bình", r"""<p>Một cốc nhôm khối lượng $200\ \text{g}$ chứa $500\ \text{g}$ nước ở $15\ ^\circ\text{C}$. Dẫn hơi nước ở $100\ ^\circ\text{C}$ (áp suất chuẩn) vào cốc; toàn bộ hơi dẫn vào đều ngưng tụ trong cốc. Ngừng dẫn hơi khi nước trong cốc đạt $60\ ^\circ\text{C}$. Bỏ qua trao đổi nhiệt với môi trường. Cho $c_{\text{nhôm}}=880$, $c_{\text{nước}}=4200\ \text{J/(kg·K)}$, $L=2{,}3\cdot10^6\ \text{J/kg}$.</p>
<p>a) Tính khối lượng hơi nước đã dẫn vào.</p>
<p>b) Lúc đó trong cốc có bao nhiêu gam nước?</p>
<p>c) Muốn cốc nước tăng lên $60\ ^\circ\text{C}$ như trên bằng cách rót thêm nước sôi $100\ ^\circ\text{C}$ thì cần bao nhiêu gam? So sánh với câu a) và giải thích vì sao bỏng hơi nước thường nặng hơn bỏng nước sôi.</p>""",
  r"""<p>a) Cốc và nước thu nhiệt: $Q_{\text{thu}}=(0{,}2\cdot880+0{,}5\cdot4200)(60-15)=2276\cdot45=102\,420\ \text{J}$.</p>
<p>Hơi nước toả nhiệt qua hai giai đoạn: ngưng tụ ở $100\ ^\circ\text{C}$, rồi nước vừa ngưng nguội từ $100$ xuống $60\ ^\circ\text{C}$.</p>
<p>$Q_{\text{toả}}=m(L+4200\cdot40)=m\cdot2\,468\,000$.</p>
<p>$m=\dfrac{102\,420}{2\,468\,000}\approx0{,}0415\ \text{kg}\approx41{,}5\ \text{g}$.</p>
<p>b) Nước trong cốc: $500+41{,}5\approx541{,}5\ \text{g}$.</p>
<p>c) Nước sôi chỉ toả nhiệt khi nguội: $m'\cdot4200\cdot40=102\,420$ nên $m'\approx0{,}610\ \text{kg}=610\ \text{g}$.</p>
<p>Cần lượng nước sôi gấp khoảng $15$ lần lượng hơi. Mỗi gam hơi khi ngưng tụ trên da toả thêm nhiệt hoá hơi $L$ rất lớn, nên bỏng hơi nặng hơn.</p>
<p>Lỗi hay gặp: chỉ viết $Q_{\text{toả}}=mL$, quên phần nước ngưng tụ nguội tiếp xuống $60\ ^\circ\text{C}$ (ra $44{,}5\ \text{g}$).</p>
<p>Lỗi hay gặp: quên cốc nhôm.</p>"""),

 # ── Bài 4 · Trung bình: đá tan một phần, tìm khối lượng đá ban đầu
 ("Trung bình", r"""<p>Thả một cục nước đá ở $-20\ ^\circ\text{C}$ vào bình cách nhiệt chứa $1{,}4\ \text{kg}$ nước ở $28\ ^\circ\text{C}$ (áp suất chuẩn). Bỏ qua nhiệt dung của bình và trao đổi nhiệt với môi trường. Khi có cân bằng nhiệt, trong bình còn $100\ \text{g}$ nước đá chưa tan. Cho $c_{\text{nước}}=4200$, $c_{\text{đá}}=2100\ \text{J/(kg·K)}$, $\lambda=3{,}4\cdot10^5\ \text{J/kg}$.</p>
<p>a) Nhiệt độ cân bằng là bao nhiêu? Vì sao?</p>
<p>b) Tính khối lượng cục đá ban đầu.</p>
<p>c) Sau đó rót thêm nước $40\ ^\circ\text{C}$ vào bình. Cần rót ít nhất bao nhiêu gam để đá vừa tan hết?</p>""",
  r"""<p>a) Trong bình còn cả nước và đá nên nhiệt độ cân bằng bắt buộc là $0\ ^\circ\text{C}$.</p>
<p>b) Nước toả nhiệt khi hạ từ $28$ về $0\ ^\circ\text{C}$: $Q_{\text{toả}}=1{,}4\cdot4200\cdot28=164\,640\ \text{J}$.</p>
<p>Gọi $m$ là khối lượng đá ban đầu. Toàn bộ đá tăng từ $-20$ lên $0\ ^\circ\text{C}$: $Q_1=m\cdot2100\cdot20=42\,000\,m$.</p>
<p>Chỉ $(m-0{,}1)$ kg đá tan: $Q_2=(m-0{,}1)\cdot3{,}4\cdot10^5$.</p>
<p>$42\,000m+340\,000m-34\,000=164\,640$ nên $382\,000m=198\,640$.</p>
<p>$m=0{,}52\ \text{kg}=520\ \text{g}$.</p>
<p>c) Chỉ cần làm tan $100\ \text{g}$ đá còn lại, hệ vẫn ở $0\ ^\circ\text{C}$: $m'\cdot4200\cdot40=0{,}1\cdot3{,}4\cdot10^5=34\,000$.</p>
<p>$m'\approx0{,}202\ \text{kg}\approx202\ \text{g}$.</p>
<p>Lỗi hay gặp: viết $Q_2=m\lambda$ (cho cả cục đá tan) rồi mới trừ $100\ \text{g}$.</p>
<p>Lỗi hay gặp: chỉ cho phần đá tan được nóng lên từ $-20\ ^\circ\text{C}$ — thật ra cả $100\ \text{g}$ đá còn lại cũng đã lên $0\ ^\circ\text{C}$.</p>"""),

 # ── Bài 5 · Khó: đồ thị đông đặc khi làm lạnh
 ("Khó", r"""<p>Đổ $300\ \text{g}$ nước ở $20\ ^\circ\text{C}$ vào khay đá rồi đặt vào ngăn đá tủ lạnh. Coi như ngăn đá lấy nhiệt của khay nước đều đặn (công suất lấy nhiệt không đổi), bỏ qua nhiệt dung của khay; áp suất chuẩn, bỏ qua hiện tượng nước quá lạnh (nước bắt đầu đông đặc ngay khi tới $0\ ^\circ\text{C}$). Đồ thị nhiệt độ theo thời gian của nước gồm ba đoạn thẳng: đoạn AB đi từ $(0\ \text{min};\ 20\ ^\circ\text{C})$ đến $(4\ \text{min};\ 0\ ^\circ\text{C})$, đoạn BC nằm ngang ở $0\ ^\circ\text{C}$, đoạn CD đi xuống tới $-10\ ^\circ\text{C}$ tại điểm D. Cho $c_{\text{nước}}=4200$, $c_{\text{đá}}=2100\ \text{J/(kg·K)}$, $\lambda=3{,}4\cdot10^5\ \text{J/kg}$.</p>
<p>a) Tính công suất lấy nhiệt của ngăn đá.</p>
<p>b) Trên đoạn BC nước ở thể nào? Nhiệt độ không đổi thì nước có toả nhiệt không? Tính thời điểm $\tau_C$ kết thúc đoạn BC.</p>
<p>c) Tính thời điểm $\tau_D$.</p>
<p>d) So sánh độ dốc (số độ giảm mỗi phút) của đoạn AB và CD, giải thích.</p>""",
  r"""<p>a) Đoạn AB: nước lỏng nguội từ $20$ về $0\ ^\circ\text{C}$ trong $4\ \text{min}=240\ \text{s}$.</p>
<p>$P\cdot240=0{,}3\cdot4200\cdot20=25\,200$ nên $P=105\ \text{W}$.</p>
<p>b) Đoạn BC: nước đang đông đặc, trong khay có cả nước và đá.</p>
<p>Nhiệt độ không đổi nhưng nước vẫn toả nhiệt (nhiệt đông đặc), ngăn đá vẫn lấy nhiệt đều.</p>
<p>Thời gian đông đặc hết: $\Delta\tau=\dfrac{\lambda m}{P}=\dfrac{3{,}4\cdot10^5\cdot0{,}3}{105}\approx971\ \text{s}\approx16{,}2\ \text{min}$.</p>
<p>$\tau_C\approx4+16{,}2=20{,}2\ \text{min}$.</p>
<p>c) Đoạn CD: đá nguội từ $0$ xuống $-10\ ^\circ\text{C}$: $\Delta\tau'=\dfrac{0{,}3\cdot2100\cdot10}{105}=60\ \text{s}=1\ \text{min}$.</p>
<p>$\tau_D\approx21{,}2\ \text{min}$.</p>
<p>d) AB giảm $20:4=5\ ^\circ\text{C/min}$; CD giảm $10:1=10\ ^\circ\text{C/min}$, dốc gấp đôi.</p>
<p>Cùng khối lượng, cùng công suất lấy nhiệt thì độ giảm nhiệt độ mỗi phút $\dfrac{P}{mc}$ tỉ lệ nghịch với $c$; $c_{\text{đá}}=\tfrac12c_{\text{nước}}$ nên đoạn CD dốc gấp đôi.</p>
<p>Lỗi hay gặp: cho rằng trên đoạn BC "nhiệt độ không đổi nên nước không toả nhiệt".</p>
<p>Lỗi hay gặp: dùng $c_{\text{nước}}$ cho đoạn CD (ra $2\ \text{min}$).</p>"""),

 # ── Bài 6 · Khó: rót qua lại nhiều lần, tìm quy luật
 ("Khó", r"""<p>Hai bình cách nhiệt, mỗi bình chứa $1\ \text{kg}$ nước: bình 1 ở $80\ ^\circ\text{C}$, bình 2 ở $20\ ^\circ\text{C}$. Bỏ qua nhiệt dung của bình, của ca múc và trao đổi nhiệt với môi trường. Một <em>lượt</em> gồm: múc $250\ \text{g}$ nước từ bình 1 đổ sang bình 2, chờ cân bằng; rồi múc $250\ \text{g}$ nước từ bình 2 đổ về bình 1, chờ cân bằng.</p>
<p>a) Tính nhiệt độ mỗi bình sau lượt 1 và sau lượt 2.</p>
<p>b) Chứng minh sau mỗi lượt, hiệu nhiệt độ hai bình giảm theo cùng một tỉ số. Tìm tỉ số đó và nhiệt độ mà cả hai bình tiến tới.</p>
<p>c) Sau ít nhất bao nhiêu lượt thì hiệu nhiệt độ hai bình nhỏ hơn $1\ ^\circ\text{C}$?</p>""",
  r"""<p>a) Lượt 1, rót sang bình 2: $1\cdot(t_2'-20)=0{,}25\,(80-t_2')$ nên $t_2'=\dfrac{20+20}{1{,}25}=32\ ^\circ\text{C}$.</p>
<p>Rót về bình 1 (còn $0{,}75\ \text{kg}$ ở $80\ ^\circ\text{C}$): $t_1'=\dfrac{0{,}75\cdot80+0{,}25\cdot32}{1}=68\ ^\circ\text{C}$.</p>
<p>Lượt 2: $t_2''=\dfrac{1\cdot32+0{,}25\cdot68}{1{,}25}=39{,}2\ ^\circ\text{C}$.</p>
<p>$t_1''=0{,}75\cdot68+0{,}25\cdot39{,}2=60{,}8\ ^\circ\text{C}$.</p>
<p>b) Gọi $M=1\ \text{kg}$, $m=0{,}25\ \text{kg}$, đầu lượt hai bình ở $t_1$, $t_2$, hiệu $\Delta=t_1-t_2$.</p>
<p>Cuối lượt mỗi bình lại có $M$ kg và tổng nhiệt lượng không đổi, nên $t_1'+t_2'=t_1+t_2$: tổng (và trung bình $50\ ^\circ\text{C}$) giữ nguyên.</p>
<p>$t_2'=\dfrac{Mt_2+mt_1}{M+m}$, do đó $\Delta'=t_1'-t_2'=t_1+t_2-2t_2'=\dfrac{(M-m)(t_1-t_2)}{M+m}$.</p>
<p>Tỉ số $k=\dfrac{M-m}{M+m}=\dfrac{0{,}75}{1{,}25}=0{,}6$, không phụ thuộc lượt. Kiểm tra: $60\to36\to21{,}6$ ✓.</p>
<p>Sau $n$ lượt: $\Delta_n=60\cdot0{,}6^n$, $t_1=50+\tfrac{\Delta_n}{2}$, $t_2=50-\tfrac{\Delta_n}{2}$; cả hai tiến tới $50\ ^\circ\text{C}$.</p>
<p>c) Cần $60\cdot0{,}6^n\lt1$. Thử: $60\cdot0{,}6^8\approx1{,}008$ (chưa đạt), $60\cdot0{,}6^9\approx0{,}60$.</p>
<p>Vậy cần ít nhất $9$ lượt.</p>
<p>Lỗi hay gặp: nghĩ sau một lượt hai bình đã bằng nhau, hoặc nhiệt độ chung là trung bình có trọng số của lần rót đầu.</p>
<p>Lỗi hay gặp: khi rót về bình 1 vẫn dùng $1\ \text{kg}$ ở $80\ ^\circ\text{C}$, quên bình 1 chỉ còn $0{,}75\ \text{kg}$.</p>"""),

 # ── Bài 7 · Nâng cao: ba chất lỏng trộn từng đôi
 ("Nâng cao", r"""<p>Có ba chất lỏng không tác dụng hoá học với nhau, đựng trong ba bình: chất 1 ở $12\ ^\circ\text{C}$, chất 2 ở $36\ ^\circ\text{C}$, chất 3 ở $72\ ^\circ\text{C}$ (khối lượng và nhiệt dung riêng của chúng chưa biết, có thể khác nhau). Làm thí nghiệm với các lượng chất lỏng như trong ba bình: nếu đổ toàn bộ chất 1 với toàn bộ chất 2 vào một bình thì được $20\ ^\circ\text{C}$; nếu đổ toàn bộ chất 1 với toàn bộ chất 3 thì được $32\ ^\circ\text{C}$. Bỏ qua nhiệt dung của bình và trao đổi nhiệt với môi trường.</p>
<p>a) Đổ cả ba chất lỏng (toàn bộ lượng ban đầu) vào chung một bình thì nhiệt độ cân bằng là bao nhiêu?</p>
<p>b) Một bạn trả lời "$40\ ^\circ\text{C}$ vì là trung bình cộng của ba nhiệt độ". Chỉ ra chỗ sai.</p>
<p>c) Biết chất 1 là $0{,}4\ \text{kg}$ nước ($4200\ \text{J/(kg·K)}$), chất 3 là dầu có nhiệt dung riêng $2100\ \text{J/(kg·K)}$. Tính khối lượng dầu.</p>""",
  r"""<p>a) Đặt $C_i=m_ic_i$ là nhiệt dung của lượng chất $i$.</p>
<p>Trộn 1 với 2: $C_1(20-12)=C_2(36-20)$ nên $C_2=\dfrac{8}{16}C_1=\dfrac{C_1}{2}$.</p>
<p>Trộn 1 với 3: $C_1(32-12)=C_3(72-32)$ nên $C_3=\dfrac{20}{40}C_1=\dfrac{C_1}{2}$.</p>
<p>Trộn cả ba: $t=\dfrac{C_1t_1+C_2t_2+C_3t_3}{C_1+C_2+C_3}=\dfrac{12+\tfrac12\cdot36+\tfrac12\cdot72}{1+\tfrac12+\tfrac12}=\dfrac{66}{2}=33\ ^\circ\text{C}$.</p>
<p>b) Trung bình cộng chỉ đúng khi ba lượng chất lỏng có nhiệt dung $mc$ bằng nhau. Ở đây chất 1 có nhiệt dung gấp đôi mỗi chất còn lại nên kéo nhiệt độ chung xuống gần $12\ ^\circ\text{C}$ hơn.</p>
<p>c) $C_3=\dfrac{C_1}{2}=\dfrac{0{,}4\cdot4200}{2}=840\ \text{J/K}$, nên $m_3=\dfrac{840}{2100}=0{,}4\ \text{kg}$.</p>
<p>Lỗi hay gặp: cố đi tìm từng $m_i$ và $c_i$ — không đủ dữ kiện; chỉ cần tỉ số các nhiệt dung $C_i$.</p>
<p>Kiểm tra thêm: trộn 2 với 3 (nhiệt dung bằng nhau) được $\dfrac{36+72}{2}=54\ ^\circ\text{C}$.</p>"""),

 # ── Bài 8 · Nâng cao: tổng hợp đá + hơi nước + bình nhôm, biện luận
 ("Nâng cao", r"""<p>Một bình nhôm khối lượng $250\ \text{g}$ chứa $400\ \text{g}$ nước, bình và nước cùng ở $10\ ^\circ\text{C}$. Bỏ qua trao đổi nhiệt với môi trường; bình nhôm có tham gia trao đổi nhiệt. Cho $c_{\text{nhôm}}=880$, $c_{\text{nước}}=4200$, $c_{\text{đá}}=2100\ \text{J/(kg·K)}$; $\lambda=3{,}4\cdot10^5\ \text{J/kg}$; $L=2{,}3\cdot10^6\ \text{J/kg}$; áp suất chuẩn.</p>
<p>a) Thả vào bình $600\ \text{g}$ nước đá ở $-20\ ^\circ\text{C}$. Biện luận để xác định nhiệt độ cân bằng và khối lượng nước, nước đá trong bình khi cân bằng.</p>
<p>b) Sau đó dẫn hơi nước ở $100\ ^\circ\text{C}$ vào bình (hơi ngưng tụ hết trong bình) cho đến khi nhiệt độ cân bằng là $20\ ^\circ\text{C}$. Tính khối lượng hơi nước đã dẫn vào.</p>""",
  r"""<p>a) Bình và nước toả tối đa khi hạ từ $10$ về $0\ ^\circ\text{C}$: $Q_{\text{toả}}=(0{,}25\cdot880+0{,}4\cdot4200)\cdot10=1900\cdot10=19\,000\ \text{J}$.</p>
<p>Đưa đá từ $-20$ lên $0\ ^\circ\text{C}$ cần $Q_1=0{,}6\cdot2100\cdot20=25\,200\ \text{J}$.</p>
<p>$Q_{\text{toả}}\lt Q_1$: chưa đủ đưa đá lên $0\ ^\circ\text{C}$, nên đá không thể tan chút nào; phần nhiệt còn thiếu do một phần nước đông đặc toả ra.</p>
<p>Nhiệt còn thiếu: $25\,200-19\,000=6200\ \text{J}$; nếu cả $400\ \text{g}$ nước đông đặc sẽ toả $0{,}4\cdot3{,}4\cdot10^5=136\,000\ \text{J}\gt6200\ \text{J}$, nên chỉ một phần nước đông.</p>
<p>Khối lượng nước đông đặc: $\dfrac{6200}{3{,}4\cdot10^5}\approx0{,}0182\ \text{kg}=18{,}2\ \text{g}$.</p>
<p>Cân bằng ở $0\ ^\circ\text{C}$; nước đá $600+18{,}2\approx618{,}2\ \text{g}$; nước $400-18{,}2\approx381{,}8\ \text{g}$.</p>
<p>b) Để từ trạng thái ở câu a) lên $20\ ^\circ\text{C}$, cần làm tan toàn bộ $618{,}2\ \text{g}$ đá rồi đun $1\ \text{kg}$ nước cùng bình từ $0$ lên $20\ ^\circ\text{C}$.</p>
<p>Làm tan đá: $Q_2=0{,}6\cdot3{,}4\cdot10^5+6200=210\,200\ \text{J}$.</p>
<p>Đun nước và bình: $Q_3=(1\cdot4200+0{,}25\cdot880)\cdot20=4420\cdot20=88\,400\ \text{J}$.</p>
<p>$Q_{\text{thu}}=Q_2+Q_3=298\,600\ \text{J}$.</p>
<p>Hơi ngưng tụ rồi nguội từ $100$ xuống $20\ ^\circ\text{C}$: $Q_{\text{toả}}=m_h(2{,}3\cdot10^6+4200\cdot80)=2\,636\,000\,m_h$.</p>
<p>$m_h=\dfrac{298\,600}{2\,636\,000}\approx0{,}1133\ \text{kg}\approx113\ \text{g}$.</p>
<p>Lỗi hay gặp ở a): giả sử ngay đá tan một phần rồi tính khối lượng đá tan ra số âm; phải so $Q_{\text{toả}}$ với $Q_1$ trước.</p>
<p>Lỗi hay gặp ở b): chỉ làm tan $600\ \text{g}$ đá, quên $18{,}2\ \text{g}$ nước đã đông ở câu a); hoặc quên bình nhôm.</p>"""),
]


def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
                          + "".join(parts))


def kiem_so():
    cn, cd, cal, ccu, lam, L = 4200, 2100, 880, 380, 340000, 2300000
    # Bài 1
    m1 = F(30 * 15, 60 + 15); assert m1 == 6 and 30 - m1 == 24 and 5 * 4 + 5 == 25
    assert (15 * 100 + 15 * 25) / 30 == 62.5
    m1c = F(30 * 15, 50 + 15); assert m1c == F(90, 13) and round(float(m1c), 1) == 6.9 and round(float(30 - m1c), 1) == 23.1
    # Bài 2
    qthu = (F(12, 100) * ccu + F(25, 100) * cn) * 6; assert qthu == F(65736, 10)
    c = qthu / (F(2, 10) * 76); assert round(float(c)) == 432 and abs(float(c) - 460) < abs(float(c) - 380)
    c2 = F(25, 100) * cn * 6 / (F(2, 10) * 76); assert round(float(c2)) == 414 and 0.035 < float((c - c2) / c) < 0.045
    # Bài 3
    q3 = (F(2, 10) * cal + F(5, 10) * cn) * 45; assert q3 == 102420
    mh = q3 / (L + cn * 40); assert L + cn * 40 == 2468000 and round(float(mh) * 1000, 1) == 41.5
    assert round(float(q3 / L) * 1000, 1) == 44.5
    mn = q3 / (cn * 40); assert round(float(mn), 3) == 0.610 and round(float(mn / mh)) == 15
    # Bài 4
    qw = F(14, 10) * cn * 28; assert qw == 164640
    m = (qw + F(1, 10) * lam) / (cd * 20 + lam); assert m == F(52, 100)
    assert m * cd * 20 + (m - F(1, 10)) * lam == qw
    mp = F(1, 10) * lam / (cn * 40); assert round(float(mp) * 1000) == 202
    # Bài 5
    P = F(3, 10) * cn * 20 / 240; assert P == 105
    tf = F(3, 10) * lam / P; assert round(float(tf)) == 971 and round(float(tf) / 60, 1) == 16.2
    assert round(4 + float(tf) / 60, 1) == 20.2
    tcd = F(3, 10) * cd * 10 / P; assert tcd == 60 and round(4 + float(tf) / 60 + 1, 1) == 21.2
    assert F(3, 10) * cn * 10 / P == 120
    # Bài 6
    M, mm = F(1), F(1, 4)
    t1, t2 = F(80), F(20); hist = []
    for _ in range(2):
        t2 = (M * t2 + mm * t1) / (M + mm)
        t1 = ((M - mm) * t1 + mm * t2) / M
        hist.append((t1, t2))
    assert hist[0] == (68, 32) and hist[1] == (F(608, 10), F(392, 10))
    k = (M - mm) / (M + mm); assert k == F(3, 5)
    assert hist[0][0] - hist[0][1] == 60 * k and hist[1][0] - hist[1][1] == 60 * k ** 2 and sum(hist[1]) == 100
    n = ceil(log(60) / log(1 / 0.6)); assert n == 9 and 60 * 0.6 ** 8 > 1 > 60 * 0.6 ** 9
    assert round(60 * 0.6 ** 8, 3) == 1.008 and round(60 * 0.6 ** 9, 2) == 0.60
    # Bài 7
    C1 = F(1); C2 = C1 * (20 - 12) / (36 - 20); C3 = C1 * (32 - 12) / (72 - 32)
    assert C2 == C3 == F(1, 2)
    t = (C1 * 12 + C2 * 36 + C3 * 72) / (C1 + C2 + C3); assert t == 33 and (12 + 36 + 72) / 3 == 40
    assert (C1 * 12 + C2 * 36) / (C1 + C2) == 20 and (C1 * 12 + C3 * 72) / (C1 + C3) == 32
    assert F(4, 10) * cn / 2 / 2100 == F(4, 10) and (C2 * 36 + C3 * 72) / (C2 + C3) == 54
    # Bài 8
    Cb = F(25, 100) * cal + F(4, 10) * cn; assert Cb == 1900
    qt = Cb * 10; q1 = F(6, 10) * cd * 20; assert qt == 19000 and q1 == 25200 and qt < q1
    assert qt + F(4, 10) * lam > q1
    mdd = (q1 - qt) / lam; assert round(float(mdd) * 1000, 1) == 18.2
    assert round(600 + float(mdd) * 1000, 1) == 618.2 and round(400 - float(mdd) * 1000, 1) == 381.8
    q2 = (F(6, 10) + mdd) * lam; assert q2 == 210200
    q3b = (1 * cn + F(25, 100) * cal) * 20; assert q3b == 88400
    mh8 = (q2 + q3b) / (L + cn * 80); assert L + cn * 80 == 2636000 and round(float(mh8) * 1000, 1) == 113.3
    print("kiểm số liệu tự luận 153: đạt")


if __name__ == "__main__":
    kiem_so()
    print(len(tu_luan()["body_html"]))
