"""Bài tập mẫu bài 3 "Nội năng. Định luật 1 của nhiệt động lực học" (Vật lí 12) — lesson_id 4.
5 dạng (quét ở scripts/logs/batch-ra-soat/ket-qua/4.quet-dang.json): cấp 1, 2, 2, 3, 4.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-4.py   (idempotent)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_4 import *

J = os.path.join(HERE, "4.json")
T199 = "Nội năng và hai cách làm biến đổi nội năng"
T200 = "Vận dụng ΔU = A + Q"

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Nhận ra cách biến đổi nội năng: thực hiện công hay truyền nhiệt", topic=T199,
      problem_html=r"""<p>Một đĩa phanh bằng nhôm có khối lượng $m=0{,}25\ \text{kg}$, nhiệt độ ban đầu $25{,}0\ ^\circ\text{C}$. Khi phanh gấp, lực ma sát của má phanh thực hiện công $4400\ \text{J}$ lên đĩa. Thời gian phanh rất ngắn nên coi đĩa chưa kịp truyền nhiệt ra ngoài. Sau đó xe dừng, đĩa đang ở $45{,}0\ ^\circ\text{C}$ nguội dần về $25{,}0\ ^\circ\text{C}$ trong không khí. Nhiệt dung riêng của nhôm là $c=880\ \text{J/(kg·K)}$.</p><ol type="a"><li>Lúc phanh, nội năng của đĩa biến đổi bằng cách nào? Tính độ biến thiên nội năng $\Delta U_1$ của đĩa lúc phanh.</li><li>Lúc nguội, nội năng của đĩa biến đổi bằng cách nào? Tính nhiệt lượng $Q$ của đĩa và độ biến thiên nội năng $\Delta U_2$ lúc nguội.</li><li>Tính độ biến thiên nội năng của đĩa từ trước lúc phanh đến khi nguội hẳn.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Đặt dấu A, Q khi khí vừa nhận vừa mất năng lượng", topic=T200,
      problem_html=r"""<p>Khí trong xilanh của một bơm tay được nén rồi giãn ra. Giai đoạn 1: nén nhanh, pit-tông thực hiện công $180\ \text{J}$ lên khí, đồng thời khí toả ra ngoài $70\ \text{J}$ nhiệt lượng qua thành xilanh. Giai đoạn 2: pit-tông được thả ra, khí giãn nở, nhận $130\ \text{J}$ nhiệt lượng từ không khí xung quanh và sinh công $150\ \text{J}$ đẩy pit-tông.</p><ol type="a"><li>Tính độ biến thiên nội năng $\Delta U_1$ của khí ở giai đoạn 1.</li><li>Tính độ biến thiên nội năng $\Delta U_2$ của khí ở giai đoạn 2.</li><li>Sau hai giai đoạn, nội năng của khí tăng hay giảm, và bằng bao nhiêu?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Bài ngược: biết ΔU và một đại lượng, tìm công hoặc nhiệt lượng còn lại", topic=T200,
      problem_html=r"""<p>Một khối khí trong xilanh trải qua hai quá trình liên tiếp. Quá trình 1: nén khí, khí nhận công $25\ \text{J}$ và nội năng của khí giảm $35\ \text{J}$. Quá trình 2: hơ nóng khí, khí nhận nhiệt lượng $100\ \text{J}$ và nội năng của khí tăng $20\ \text{J}$.</p><ol type="a"><li>Ở quá trình 1, khí toả hay thu nhiệt? Nhiệt lượng bao nhiêu?</li><li>Ở quá trình 2, khí nhận hay sinh công? Công bao nhiêu?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Công làm nóng vật rồi nhiệt truyền sang nước: đặt dấu riêng cho từng vật", topic=T199,
      problem_html=r"""<p>Một thợ khoan lỗ trên khối đồng khối lượng $0{,}300\ \text{kg}$ đặt trong cốc cách nhiệt chứa $0{,}250\ \text{kg}$ nước ở $24{,}0\ ^\circ\text{C}$. Trong một lượt khoan, mũi khoan thực hiện công $5400\ \text{J}$ lên khối đồng. Cuối lượt khoan, nước ở $27{,}0\ ^\circ\text{C}$. Coi nước chỉ nhận nhiệt từ khối đồng (bỏ qua trao đổi nhiệt với cốc và không khí) và nước không nhận công. Nhiệt dung riêng của nước là $c=4200\ \text{J/(kg·K)}$.</p><ol type="a"><li>Tính nhiệt lượng nước nhận được.</li><li>Khối đồng toả hay thu nhiệt? Tính nhiệt lượng $Q$ của khối đồng.</li><li>Tính độ biến thiên nội năng của khối đồng. Nội năng khối đồng tăng hay giảm?</li></ol>"""),
 dict(label="Dạng 5 · Nâng cao · Cả chu trình: ΔU = 0 trong tủ lạnh", topic=T200,
      problem_html=r"""<p>Trong tủ lạnh, gas (môi chất) tuần hoàn qua máy nén, dàn nóng, van tiết lưu và dàn lạnh rồi trở về đúng trạng thái lúc đầu chu trình. Trong mỗi chu trình, máy nén thực hiện công $150\ \text{J}$ lên gas; ở dàn nóng gas toả ra môi trường $450\ \text{J}$ nhiệt lượng. Van tiết lưu không nhận công, không sinh công và không trao đổi nhiệt; gas chỉ thu nhiệt ở dàn lạnh.</p><ol type="a"><li>Tính nhiệt lượng gas thu vào ở dàn lạnh trong một chu trình.</li><li>Cần lấy $54\ \text{kJ}$ nhiệt từ ngăn lạnh. Tủ phải chạy bao nhiêu chu trình?</li><li>Tính tổng công máy nén thực hiện trong số chu trình đó.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 [(r'"lực ma sát của má phanh thực hiện công $4400$ J lên đĩa"', r"$A=4400\ \text{J}$ (đĩa nhận công)", r"Thực hiện công: có lực làm vật dịch chuyển · quy ước dấu: nhận vào thì $+$"),
  (r'"thời gian phanh rất ngắn nên coi đĩa chưa kịp truyền nhiệt"', r"Lúc phanh: không truyền nhiệt", r"⚠ Chỉ khi bỏ qua truyền nhiệt thì lúc phanh mới chỉ còn một cách tác động"),
  (r'"nhôm $m=0{,}25$ kg, $c=880$ J/(kg·K)"', r"$m=0{,}25\ \text{kg}$ ; $c=880\ \text{J/(kg·K)}$", r"Nhiệt lượng $Q=mc\,\Delta t$"),
  (r'"đĩa $45{,}0\ ^\circ$C nguội dần về $25{,}0\ ^\circ$C"', r"$t_{\text{đầu}}=45{,}0\ ^\circ\text{C}$ ; $t_{\text{cuối}}=25{,}0\ ^\circ\text{C}$", r"Hai cách đổi nội năng: công (lực làm dịch chuyển) · truyền nhiệt (chênh nhiệt độ) ; $\Delta t$ lấy cuối trừ đầu"),
  (r'"tính $\Delta U_1$, $\Delta U_2$"', r"Cần $\Delta U$ của từng giai đoạn", r"$\Delta U=A+Q$"),
  (r'"từ trước lúc phanh đến khi nguội hẳn"', r"Cần $\Delta U$ toàn bộ", r"Cộng độ biến thiên nội năng của hai giai đoạn")],
 [(r'"giai đoạn 1: pit-tông thực hiện công $180$ J lên khí"', r"công $180\ \text{J}$, đi vào khí", r"Quy ước dấu định luật I: nhận vào thì $+$, mất đi thì $-$"),
  (r'"khí toả ra ngoài $70$ J nhiệt lượng"', r"nhiệt $70\ \text{J}$, đi ra khỏi khí", r"Quy ước dấu như trên"),
  (r'"giai đoạn 2: khí nhận $130$ J nhiệt lượng"', r"nhiệt $130\ \text{J}$, đi vào khí", r"Quy ước dấu như trên"),
  (r'"khí giãn nở … sinh công $150$ J"', r"công $150\ \text{J}$, đi ra khỏi khí", r"⚠ Hệ đang xét là khí: công khí sinh ra là năng lượng khí mất đi"),
  (r'"tính $\Delta U_1$, $\Delta U_2$"', r"Cần $\Delta U_1$, $\Delta U_2$", r"$\Delta U=A+Q$ viết riêng cho từng giai đoạn"),
  (r'"sau hai giai đoạn"', r"Cần $\Delta U$ cả hai giai đoạn", r"Cộng đại số $\Delta U_1+\Delta U_2$")],
 [(r'"quá trình 1: khí nhận công $25$ J"', r"công $25\ \text{J}$, đi vào khí", r"Quy ước dấu: nhận vào thì $+$, mất đi thì $-$"),
  (r'"nội năng của khí giảm $35$ J"', r"nội năng bớt $35\ \text{J}$", r"$\Delta U$ là độ biến thiên (cuối trừ đầu)"),
  (r'"toả hay thu nhiệt? Nhiệt lượng bao nhiêu?"', r"Cần $Q_1$", r"⚠ Đặt dấu hai số đề cho trước (kể cả dấu) rồi mới tìm ẩn"),
  (r'"quá trình 2: khí nhận nhiệt lượng $100$ J"', r"nhiệt $100\ \text{J}$, đi vào khí", r"Quy ước dấu như trên"),
  (r'"nội năng của khí tăng $20$ J"', r"nội năng thêm $20\ \text{J}$", r"$\Delta U$ là độ biến thiên (cuối trừ đầu)"),
  (r'"khí nhận hay sinh công? Công bao nhiêu?"', r"Cần $A_2$", r"⚠ Cả ba đại lượng cùng tính cho khối khí")],
 [(r'"mũi khoan thực hiện công $5400$ J lên khối đồng"', r"$A=5400\ \text{J}$, đi vào khối đồng", r"Thực hiện công · quy ước dấu: nhận vào thì $+$"),
  (r'"$0{,}250$ kg nước ở $24{,}0\ ^\circ$C … cuối lượt khoan $27{,}0\ ^\circ$C"', r"$m=0{,}250\ \text{kg}$ ; $t_{\text{đầu}}=24{,}0\ ^\circ\text{C}$ ; $t_{\text{cuối}}=27{,}0\ ^\circ\text{C}$ ; $c=4200\ \text{J/(kg·K)}$", r"$Q=mc\,\Delta t$ ; $\Delta t$ lấy cuối trừ đầu"),
  (r'"nước chỉ nhận nhiệt từ khối đồng … không nhận công"', r"Nước: $A=0$ ; nhiệt nước thu là nhiệt đồng mất", r"⚠ Điều kiện: không mất nhiệt ra cốc và không khí · mỗi vật đặt dấu riêng"),
  (r'"tính nhiệt lượng nước nhận được"', r"Cần $Q_{\text{nước}}$", r"$Q=mc\,\Delta t$"),
  (r'"khối đồng toả hay thu nhiệt? Tính $Q$"', r"Cần $Q_{\text{đồng}}$", r"Một vật thu bao nhiêu thì vật kia toả bấy nhiêu"),
  (r'"độ biến thiên nội năng của khối đồng"', r"Cần $\Delta U_{\text{đồng}}$", r"$\Delta U=A+Q$ viết cho khối đồng")],
 [(r'"trở về đúng trạng thái lúc đầu chu trình"', r"Hết chu trình: cùng nhiệt độ, cùng thể tích", r"⚠ Nội năng phụ thuộc nhiệt độ và thể tích"),
  (r'"máy nén thực hiện công $150$ J lên gas"', r"công $150\ \text{J}$, đi vào gas", r"Quy ước dấu: nhận vào thì $+$, mất đi thì $-$"),
  (r'"ở dàn nóng gas toả ra $450$ J"', r"nhiệt $450\ \text{J}$, đi ra khỏi gas", r"Quy ước dấu như trên"),
  (r'"van tiết lưu không công, không nhiệt"', r"Van: $A=0$ ; $Q=0$", r"Chỉ máy nén có công · chỉ dàn nóng và dàn lạnh có nhiệt"),
  (r'"nhiệt lượng gas thu vào ở dàn lạnh"', r"Cần $Q_{\text{lạnh}}$", r"Định luật I, viết cho cả chu trình"),
  (r'"lấy $54$ kJ nhiệt từ ngăn lạnh … bao nhiêu chu trình"', r"$54\ \text{kJ}=54\,000\ \text{J}$", r"Số chu trình $=$ nhiệt cần lấy $\div$ nhiệt thu mỗi chu trình"),
  (r'"tổng công máy nén"', r"Cần $A_{\text{tổng}}$", r"Công mỗi chu trình $\times$ số chu trình")],
]

# ═════════════ LỜI GIẢI (mỗi bước một khối, mỗi công thức một dòng) ═════════════
R1 = [r"<strong>Khái niệm:</strong> nội năng $U$ là tổng động năng và thế năng của các phân tử ; đổi bằng hai cách: thực hiện công (có lực làm vật dịch chuyển) và truyền nhiệt (có chênh nhiệt độ).",
      r"<strong>Định luật I:</strong> $\Delta U=A+Q$ ; nhận vào thì dương, mất đi thì âm.",
      r"<strong>Nhiệt lượng:</strong> $Q=mc\,\Delta t$ với $\Delta t=t_{\text{cuối}}-t_{\text{đầu}}$.",
      r"⚠ <strong>Điều kiện:</strong> lúc phanh bỏ qua truyền nhiệt ($Q=0$) ; lúc nguội không còn lực làm đĩa dịch chuyển ($A=0$)."]
R2 = [r"<strong>Khái niệm:</strong> hệ đang xét là khối khí ; $A\gt0$ khi khí bị nén (nhận công), $A\lt0$ khi khí giãn (sinh công).",
      r"$Q\gt0$ khi khí thu nhiệt, $Q\lt0$ khi khí toả nhiệt.",
      r"<strong>Định luật I:</strong> $\Delta U=A+Q$ (cộng đại số, mang theo dấu).",
      r"⚠ <strong>Điều kiện:</strong> $A$, $Q$ đều tính cho cùng một hệ (khối khí) ; mỗi giai đoạn đặt dấu riêng rồi mới cộng."]
R3 = [r"<strong>Định luật I:</strong> $\Delta U=A+Q$, rút ra $Q=\Delta U-A$ hoặc $A=\Delta U-Q$.",
      r"<strong>Đặt dấu trước:</strong> nội năng giảm thì $\Delta U\lt0$ ; nhận công thì $A\gt0$ ; nhận nhiệt thì $Q\gt0$.",
      r"<strong>Đọc kết quả:</strong> $Q\lt0$ là toả nhiệt ; $A\lt0$ là sinh công.",
      r"⚠ <strong>Điều kiện:</strong> $\Delta U$, $A$, $Q$ cùng tính cho một hệ (khối khí) ; đặt dấu hai số đề cho rồi mới rút ẩn."]
R4 = [r"<strong>Khái niệm:</strong> khối đồng vừa nhận công (mũi khoan) vừa toả nhiệt (cho nước) ; nước chỉ thu nhiệt.",
      r"<strong>Nhiệt lượng:</strong> $Q=mc\,\Delta t$ với $\Delta t=t_{\text{cuối}}-t_{\text{đầu}}$.",
      r"<strong>Định luật I</strong> cho từng vật: $\Delta U=A+Q$ ; nhiệt vật này thu bằng nhiệt vật kia toả.",
      r"⚠ <strong>Điều kiện:</strong> không mất nhiệt ra cốc và không khí ; nước và khối đồng đặt dấu riêng, không lẫn."]
R5 = [r"<strong>Khái niệm:</strong> nội năng phụ thuộc nhiệt độ và thể tích ; hết một chu trình gas về đúng trạng thái đầu nên $\Delta U=0$.",
      r"<strong>Định luật I</strong> cho cả chu trình: $0=A+Q_{\text{tổng}}$ với $Q_{\text{tổng}}=Q_{\text{nóng}}+Q_{\text{lạnh}}$.",
      r"<strong>Dấu:</strong> máy nén cho gas công ($A\gt0$) ; dàn nóng gas toả nhiệt ($Q_{\text{nóng}}\lt0$) ; dàn lạnh gas thu nhiệt ($Q_{\text{lạnh}}\gt0$).",
      r"⚠ <strong>Điều kiện:</strong> van tiết lưu không công, không nhiệt ; đổi kJ ra J trước khi chia."]

SOLS = [
 sol(R1, [
  ("Nhận ra cách biến đổi lúc phanh", [P("Có lực ma sát làm bề mặt đĩa dịch chuyển, còn đề bỏ qua truyền nhiệt:"),
     A(r"T:Cách biến đổi: <strong>thực hiện công</strong>, nhiệt lượng $Q=0$")]),
  ("Độ biến thiên nội năng lúc phanh", [P(r"Đĩa nhận công nên $A\gt0$:"), M(r"\Delta U_1=A+Q=4400+0"), A(r"\Delta U_1=+4400\ \text{J}")]),
  ("Lúc nguội: truyền nhiệt", [P(r"Đĩa ($45{,}0\ ^\circ\text{C}$) nóng hơn không khí ($25{,}0\ ^\circ\text{C}$), không có lực làm đĩa dịch chuyển: <strong>truyền nhiệt</strong>, $A=0$."),
     P("Độ biến thiên nhiệt độ lấy cuối trừ đầu:"), M(r"\Delta t=25{,}0-45{,}0=-20{,}0\ \text{K}"),
     M(r"Q=mc\,\Delta t=0{,}25\cdot880\cdot(-20{,}0)"), A(r"Q=-4400\ \text{J}"),
     P(r"Đĩa toả nhiệt nên $Q\lt0$. Vì $A=0$:"), M(r"\Delta U_2=A+Q=0+(-4400)"), A(r"\Delta U_2=-4400\ \text{J}")]),
  ("Kiểm tra: cả quá trình", [P("Cộng hai giai đoạn:"), M(r"\Delta U=\Delta U_1+\Delta U_2=4400+(-4400)"), A(r"\Delta U=0"),
     P(r"Đĩa về đúng $25{,}0\ ^\circ\text{C}$, thể tích gần như không đổi nên nội năng như lúc đầu ✓."),
     P(r"Kiểm tra giai đoạn phanh: $mc\,\Delta t=0{,}25\cdot880\cdot20{,}0=4400\ \text{J}$, đúng bằng công đĩa nhận ✓.")])],
  [r"a) Thực hiện công · $\Delta U_1=+4400\ \text{J}$", r"b) Truyền nhiệt · $Q=-4400\ \text{J}$ · $\Delta U_2=-4400\ \text{J}$", r"c) $\Delta U=0$"],
  r"Nhận dạng: có <strong>lực làm vật dịch chuyển</strong> → thực hiện công ; có <strong>chênh nhiệt độ</strong> → truyền nhiệt. Rồi đặt dấu theo “nhận thì cộng, mất thì trừ”."),
 sol(R2, [
  ("Giai đoạn 1: khí bị nén, toả nhiệt", [P(r"Khí bị nén nên nhận công: $A_1=+180\ \text{J}$. Khí toả nhiệt: $Q_1=-70\ \text{J}$."),
     M(r"\Delta U_1=A_1+Q_1=180+(-70)"), A(r"\Delta U_1=+110\ \text{J}")]),
  ("Giai đoạn 2: khí giãn, thu nhiệt", [P(r"Khí thu nhiệt: $Q_2=+130\ \text{J}$. Khí sinh công (năng lượng mất đi): $A_2=-150\ \text{J}$."),
     M(r"\Delta U_2=A_2+Q_2=-150+130"), A(r"\Delta U_2=-20\ \text{J}"),
     P("Nội năng giảm vì khí sinh ra nhiều công hơn nhiệt nhận vào.")]),
  ("Cộng hai giai đoạn", [M(r"\Delta U=\Delta U_1+\Delta U_2=110+(-20)"), A(r"\Delta U=+90\ \text{J}"), P("Nội năng của khí tăng $90\ \text{J}$.")]),
  ("Kiểm tra", [P("Cộng riêng công và nhiệt của cả hai giai đoạn:"), M(r"A=180+(-150)=+30\ \text{J}"), M(r"Q=(-70)+130=+60\ \text{J}"),
     M(r"\Delta U=A+Q=30+60=90\ \text{J}"), P(r"✓ Khớp. Ghi nhầm $Q_1=+70$ sẽ ra $250\ \text{J}$ ở giai đoạn 1 — sai, vì khí đang toả nhiệt.")])],
  [r"a) $\Delta U_1=+110\ \text{J}$", r"b) $\Delta U_2=-20\ \text{J}$", r"c) Tăng $90\ \text{J}$"],
  r"Nhận dạng: khí <strong>vừa nhận vừa mất</strong> năng lượng → đặt dấu từng số theo chiều đi vào hay ra khỏi khí, rồi cộng đại số."),
 sol(R3, [
  ("Quá trình 1: tìm nhiệt lượng", [P(r"Nội năng giảm: $\Delta U_1=-35\ \text{J}$. Khí nhận công: $A_1=+25\ \text{J}$."), P("Rút $Q_1$ từ định luật I:"),
     M(r"\Delta U_1=A_1+Q_1"), M(r"Q_1=\Delta U_1-A_1=-35-25"), A(r"Q_1=-60\ \text{J}"), P(r"$Q_1\lt0$ nên khí <strong>toả</strong> $60\ \text{J}$ nhiệt lượng.")]),
  ("Quá trình 2: tìm công", [P(r"Khí nhận nhiệt: $Q_2=+100\ \text{J}$. Nội năng tăng: $\Delta U_2=+20\ \text{J}$."), P("Rút $A_2$ từ định luật I:"),
     M(r"A_2=\Delta U_2-Q_2=20-100"), A(r"A_2=-80\ \text{J}"), P(r"$A_2\lt0$ nên khí <strong>sinh công</strong> $80\ \text{J}$ (giãn nở đẩy pit-tông).")]),
  ("Kiểm tra", [P("Thay ngược vào định luật I:"), M(r"\Delta U_1=25+(-60)=-35\ \text{J}"), M(r"\Delta U_2=-80+100=+20\ \text{J}"), P("✓ Khớp với đề."),
     P(r"Nếu coi nội năng giảm là $\Delta U_1=+35$ sẽ ra $Q_1=+10\ \text{J}$: nén mà thu nhiệt và nội năng tăng, trái với đề.")])],
  [r"a) Khí toả nhiệt $60\ \text{J}$ ($Q_1=-60\ \text{J}$)", r"b) Khí sinh công $80\ \text{J}$ ($A_2=-80\ \text{J}$)"],
  r"Nhận dạng: đề cho <strong>ΔU</strong> và <strong>một trong hai</strong> công / nhiệt, hỏi đại lượng còn lại → đặt dấu hai số đề cho rồi rút từ $\Delta U=A+Q$."),
 sol(R4, [
  ("Nhiệt lượng nước nhận", [P("Độ tăng nhiệt độ của nước:"), M(r"\Delta t=27{,}0-24{,}0=3{,}0\ \text{K}"), M(r"Q_n=m\,c\,\Delta t=0{,}250\cdot4200\cdot3{,}0"), A(r"Q_n=+3150\ \text{J}")]),
  ("Nhiệt lượng của khối đồng", [P("Nước chỉ nhận nhiệt từ khối đồng, nên khối đồng toả đúng lượng đó:"), M(r"Q_đ=-Q_n"), A(r"Q_đ=-3150\ \text{J}")]),
  ("Độ biến thiên nội năng của khối đồng", [P(r"Hệ là khối đồng: nhận công của mũi khoan ($A=+5400\ \text{J}$) và toả nhiệt ($Q_đ=-3150\ \text{J}$)."),
     M(r"\Delta U_đ=A+Q_đ=5400+(-3150)"), A(r"\Delta U_đ=+2250\ \text{J}"), P(r"$\Delta U_đ\gt0$ nên nội năng khối đồng <strong>tăng</strong>.")]),
  ("Kiểm tra", [P(r"Nước không nhận công: $\Delta U_n=A_n+Q_n=0+3150=3150\ \text{J}$."), P("Cộng nội năng tăng của cả hai vật:"),
     M(r"\Delta U_đ+\Delta U_n=2250+3150=5400\ \text{J}"), P("✓ Đúng bằng công mũi khoan: năng lượng không mất đi, chỉ chia cho đồng và nước.")])],
  [r"a) $Q_n=3150\ \text{J}$", r"b) Khối đồng toả nhiệt · $Q_đ=-3150\ \text{J}$", r"c) $\Delta U_đ=+2250\ \text{J}$ · nội năng tăng"],
  r"Nhận dạng: <strong>hai vật trao đổi nhiệt</strong>, một vật <strong>nhận công</strong> → đặt dấu riêng cho từng vật ; nhiệt vật này thu là nhiệt vật kia toả."),
 sol(R5, [
  ("ΔU của gas sau một chu trình", [P("Gas ra khỏi chu trình ở đúng trạng thái lúc vào, cùng nhiệt độ và thể tích, nên nội năng như cũ:"), A(r"\Delta U=0")]),
  ("Nhiệt thu ở dàn lạnh", [P(r"Công: $A=+150\ \text{J}$. Nhiệt toả ở dàn nóng: $Q_{\text{nóng}}=-450\ \text{J}$. Van tiết lưu không có công, không có nhiệt."),
     M(r"\Delta U=A+Q_{\text{nóng}}+Q_{\text{lạnh}}"), M(r"0=150+(-450)+Q_{\text{lạnh}}"), M(r"Q_{\text{lạnh}}=450-150"), A(r"Q_{\text{lạnh}}=+300\ \text{J}")]),
  ("Số chu trình", [P(r"Đổi $54\ \text{kJ}=54\,000\ \text{J}$. Mỗi chu trình lấy $300\ \text{J}$ từ ngăn lạnh:"), M(r"n=\dfrac{54\,000}{300}"), A(r"n=180\ \text{chu trình}")]),
  ("Tổng công của máy nén", [M(r"A_{\text{tổng}}=n\cdot150=180\cdot150=27\,000\ \text{J}"), A(r"A_{\text{tổng}}=27\ \text{kJ}")]),
  ("Kiểm tra", [P(r"Nhiệt toả ở dàn nóng trong $180$ chu trình:"), M(r"180\cdot450=81\,000\ \text{J}=81\ \text{kJ}"),
     P(r"Bằng nhiệt lấy từ ngăn lạnh cộng công: $54+27=81\ \text{kJ}$ ✓."),
     P("Mỗi $1\ \text{J}$ công lấy đi $2\ \text{J}$ nhiệt từ ngăn lạnh — hợp lí với tủ lạnh thực.")])],
  [r"a) $Q_{\text{lạnh}}=300\ \text{J}$", r"b) $n=180$ chu trình", r"c) $A_{\text{tổng}}=27\ \text{kJ}$"],
  r"Nhận dạng: <strong>một chu trình</strong>, gas <strong>về trạng thái đầu</strong> → $\Delta U=0$, nên công nhận vào cộng nhiệt tổng bằng 0."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>lực làm vật dịch chuyển</b> hay <b>chênh nhiệt độ</b> → nghĩ tới <b>công hay truyền nhiệt</b>, rồi ΔU = A + Q.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhận ra cách biến đổi lúc phanh", "Lúc phanh gấp, nội năng của đĩa biến đổi bằng cách nào?",
       lua_chon=[("Thực hiện công: lực ma sát làm bề mặt đĩa dịch chuyển, không truyền nhiệt", True),
                 ("Truyền nhiệt, vì đĩa nóng lên", "Nóng lên là kết quả, chưa phải cách. Phải xem có lực làm dịch chuyển hay có chênh nhiệt độ ; ở đây là lực ma sát, còn đề đã bỏ qua truyền nhiệt."),
                 ("Cả hai cách như nhau", "Đề coi đĩa chưa kịp truyền nhiệt ra ngoài, nên lúc phanh chỉ còn thực hiện công.")],
       loi="Nhầm “nóng lên” với “truyền nhiệt”. Cách phân biệt: có lực làm vật dịch chuyển (công) hay có chênh nhiệt độ (truyền nhiệt)."),
  buoc("Độ biến thiên nội năng lúc phanh", r"$\Delta U_1$ của đĩa lúc phanh bằng bao nhiêu?", 4400, "J", 5,
       loi=r"Ghi ngược dấu vì nghĩ ma sát là lực cản, nên “mất công”. Hệ là đĩa: đĩa nhận công nên $A\gt0$.",
       ke=[(r"Chỉ có công nên $\Delta U=A$, với $A$ dương vì đĩa nhận công", True),
           (r"$\Delta U=A+Q$ rồi tính $Q=mc\,\Delta t$ với $\Delta t=20$", r"Lúc phanh đề đã bỏ qua truyền nhiệt ($Q=0$) ; thêm $mc\,\Delta t$ là đếm cùng một năng lượng hai lần."),
           (r"$\Delta U=-A$ vì lực ma sát là lực cản", r"Lực ma sát cản xe nhưng với đĩa nó truyền năng lượng vào ; đĩa nhận công nên $A\gt0$.")]),
  buoc("Lúc nguội: truyền nhiệt", r"Nhiệt lượng $Q$ của đĩa lúc nguội bằng bao nhiêu (kể cả dấu)?", -4400, "J", 5,
       loi=r"Lấy $\Delta t$ là đầu trừ cuối nên ra $Q\gt0$. Đĩa toả nhiệt phải ra $Q\lt0$ ; $\Delta t$ luôn là cuối trừ đầu.",
       ke=[(r"$Q=mc\,\Delta t$ với $\Delta t=25-45$ (cuối trừ đầu), được số âm", True),
           (r"$Q=mc\,\Delta t$ với $\Delta t=45-25$", r"$\Delta t$ là cuối trừ đầu ; đĩa nguội nên $\Delta t\lt0$ và đĩa toả nhiệt ($Q\lt0$)."),
           (r"$Q=0$ vì không có lực nào làm đĩa dịch chuyển", r"Không có công không có nghĩa là không có nhiệt ; đĩa nóng hơn không khí vẫn toả nhiệt.")]),
  buoc("Kiểm tra: cả quá trình")]),
 dict(nhan_dang=r"Thấy khí <b>vừa nhận vừa mất</b> năng lượng → đặt dấu theo <b>vào / ra</b>, rồi ΔU = A + Q.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Giai đoạn 1: khí bị nén, toả nhiệt", r"$\Delta U_1$ của khí ở giai đoạn 1 bằng bao nhiêu (kể cả dấu)?", 110, "J", 0.5,
       loi=r"Ra $250\ \text{J}$ vì cộng cả hai con số ; khí toả nhiệt phải mang $Q_1=-70$."),
  buoc("Giai đoạn 2: khí giãn, thu nhiệt", r"$\Delta U_2$ của khí ở giai đoạn 2 bằng bao nhiêu (kể cả dấu)?", -20, "J", 0.5,
       loi=r"Ra $+280\ \text{J}$ vì để $A_2=+150$ ; hoặc ra $+20\ \text{J}$ vì lấy lớn trừ nhỏ mà quên nội năng giảm. Khí sinh công thì $A_2=-150$.",
       ke=[(r"Khí thu nhiệt $Q_2=+130$, khí sinh công $A_2=-150$, rồi cộng đại số", True),
           (r"$A_2=+150$ vì có công 150 J xuất hiện", r"Khí là hệ đang xét : công do khí sinh ra là năng lượng khí mất đi nên $A_2=-150$."),
           (r"Lấy $150-130$ rồi ghi dương", r"Nhiệt nhận vào nhỏ hơn công sinh ra, phần thiếu lấy từ nội năng nên $\Delta U_2$ phải âm.")]),
  buoc("Cộng hai giai đoạn", "Nội năng khí sau hai giai đoạn thay đổi bao nhiêu (kể cả dấu)?", 90, "J", 0.5,
       loi=r"Cộng độ lớn $110+20=130\ \text{J}$ (bỏ dấu âm của giai đoạn 2), hoặc chỉ lấy giai đoạn sau.",
       ke=[(r"Cộng đại số $\Delta U_1+\Delta U_2$", True),
           (r"Chỉ lấy giai đoạn sau vì đó là trạng thái cuối", r"Giai đoạn 1 đã làm nội năng khí đổi ; độ biến thiên tổng phải cộng cả hai phần."),
           (r"Cộng độ lớn của hai độ biến thiên", r"Cộng độ lớn bỏ mất dấu âm của giai đoạn 2 ; phải cộng đại số.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy đề cho <b>ΔU</b> và <b>một trong hai</b> công / nhiệt → đặt dấu rồi <b>rút ẩn</b> từ ΔU = A + Q.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Quá trình 1: tìm nhiệt lượng", r"$Q_1$ của khí ở quá trình 1 bằng bao nhiêu (kể cả dấu)?", -60, "J", 0.5,
       loi=r"Ra $+10\ \text{J}$ vì coi “nội năng giảm 35” là $\Delta U=+35$ ; hoặc ra $-10\ \text{J}$ vì đặt $A_1=-25$ khi nhầm “nén” với “sinh công”."),
  buoc("Quá trình 2: tìm công", r"$A_2$ của khí ở quá trình 2 bằng bao nhiêu (kể cả dấu)?", -80, "J", 0.5,
       loi=r"Đảo dấu vì lấy $Q-\Delta U$ (đảo hai số) ; hoặc kết luận “khí nhận công” từ chữ “nhận nhiệt”.",
       ke=[(r"$A_2=\Delta U_2-Q_2$ với $\Delta U_2=+20$ và $Q_2=+100$", True),
           (r"$A_2=Q_2-\Delta U_2$", r"Định luật I là $\Delta U=A+Q$ nên $A=\Delta U-Q$ ; đảo hai số sẽ đổi dấu kết quả."),
           (r"$A_2=\Delta U_2+Q_2$", r"Cộng là sai phép rút : chuyển $Q$ sang vế kia phải đổi dấu thành $-Q$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hai vật trao đổi nhiệt</b> và <b>một vật nhận công</b> → đặt dấu <b>riêng</b> cho từng vật rồi dùng ΔU = A + Q.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhiệt lượng nước nhận", r"Nhiệt lượng $Q_n$ nước nhận được bằng bao nhiêu?", 3150, "J", 5,
       loi=r"Lấy $\Delta t=24$ hoặc $27$ thay vì $27-24=3\ \text{K}$ ; hoặc quên nhân khối lượng nước."),
  buoc("Nhiệt lượng của khối đồng", r"Nhiệt lượng $Q_đ$ của khối đồng bằng bao nhiêu (kể cả dấu)?", -3150, "J", 5,
       loi=r"Ghi $+3150\ \text{J}$ vì thấy hai nhiệt lượng cùng độ lớn. Với hệ là khối đồng, nhiệt mất đi mang dấu âm.",
       ke=[(r"Nước thu bao nhiêu thì đồng toả bấy nhiêu: $Q_đ=-Q_n$", True),
           (r"$Q_đ=+Q_n$ vì hai nhiệt lượng cùng độ lớn", r"Đồng mất năng lượng cho nước ; với hệ là khối đồng, nhiệt mất đi mang dấu âm."),
           (r"$Q_đ=m_đ\,c_đ\,\Delta t$ của đồng", r"Đề không cho nhiệt độ cuối và nhiệt dung riêng của đồng ; chỉ cần dùng quan hệ với nhiệt nước thu.")]),
  buoc("Độ biến thiên nội năng của khối đồng", r"$\Delta U$ của khối đồng bằng bao nhiêu (kể cả dấu)?", 2250, "J", 5,
       loi=r"Ghi $\Delta U=A=5400\ \text{J}$ vì quên khối đồng đang toả nhiệt cho nước ; hoặc lấy $Q$ của nước làm $Q$ của đồng nên ra $8550\ \text{J}$.",
       ke=[(r"Hệ là khối đồng: $\Delta U=A+Q_đ$ với $A$ dương, $Q_đ$ âm", True),
           (r"$\Delta U=A$ vì khối đồng nóng lên", r"Khối đồng còn toả nhiệt cho nước nên $Q_đ\ne0$ ; chỉ lấy công là bỏ sót phần năng lượng đã mất."),
           (r"$\Delta U=A+Q_n$ với $Q_n$ là nhiệt nước nhận", r"$Q_n$ thuộc hệ nước ; với hệ khối đồng phải dùng nhiệt của chính khối đồng ($Q_đ$ âm).")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>một chu trình</b>, gas <b>về trạng thái đầu</b> → nghĩ tới <b>ΔU = 0</b> nên A + Q tổng = 0.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("ΔU của gas sau một chu trình", r"Sau một chu trình, $\Delta U$ của gas bằng bao nhiêu?",
       lua_chon=[("Bằng 0, vì gas trở về đúng trạng thái đầu nên nội năng như cũ", True),
                 ("Bằng công máy nén, vì chỉ máy nén cấp năng lượng cho gas", "Gas còn toả nhiệt ở dàn nóng và thu nhiệt ở dàn lạnh ; cộng tất cả lại thì nội năng không đổi sau chu trình."),
                 ("Bằng nhiệt toả ở dàn nóng, vì đó là phần lớn nhất", "Độ lớn một phần không quyết định ΔU ; ΔU là tổng đại số của mọi công và nhiệt, mà gas về trạng thái đầu thì tổng ấy là 0.")],
       loi="Cho rằng gas “nhận công thì nội năng tăng” mà quên gas đã trở về đúng trạng thái đầu ; nội năng phụ thuộc nhiệt độ và thể tích."),
  buoc("Nhiệt thu ở dàn lạnh", r"$Q_{\text{lạnh}}$ gas thu vào ở dàn lạnh trong một chu trình bằng bao nhiêu?", 300, "J", 0.5,
       loi=r"Ra $600\ \text{J}$ vì cộng $150+450$ (quên nhiệt toả mang dấu âm) ; hoặc ra $450\ \text{J}$ vì coi gas thu lại đúng nhiệt đã toả.",
       ke=[(r"Viết $0=A+Q_{\text{nóng}}+Q_{\text{lạnh}}$ với $Q_{\text{nóng}}$ âm rồi rút $Q_{\text{lạnh}}$", True),
           (r"$Q_{\text{lạnh}}=150+450$", r"Nhiệt toả ở dàn nóng mang dấu âm ; cộng hai số dương là quên dấu."),
           (r"$Q_{\text{lạnh}}=450$ vì gas thu lại đúng nhiệt đã toả", r"Gas còn nhận công 150 J ở máy nén ; thu 450 J rồi toả 450 J thì $\Delta U=150\ne0$.")]),
  buoc("Số chu trình", r"Tủ phải chạy bao nhiêu chu trình để lấy $54\ \text{kJ}$ từ ngăn lạnh?", 180, "chu trình", 0.5,
       loi=r"Chia $54$ cho $300$ mà không đổi kJ ra J nên ra $0{,}18$ ; hoặc chia cho nhiệt toả ở dàn nóng ($450\ \text{J}$) thay vì nhiệt thu ở dàn lạnh.",
       ke=[(r"$n=$ nhiệt cần lấy $\div$ nhiệt thu mỗi chu trình, sau khi đổi kJ ra J", True),
           (r"$n=\dfrac{54}{300}$ (giữ nguyên kJ)", r"kJ và J khác đơn vị : $54\ \text{kJ}=54\,000\ \text{J}$ rồi mới chia cho nhiệt thu mỗi chu trình."),
           (r"$n=\dfrac{54\,000}{450}$", r"$450\ \text{J}$ là nhiệt toả ở dàn nóng ; nhiệt lấy từ ngăn lạnh là nhiệt thu ở dàn lạnh.")]),
  buoc("Tổng công của máy nén", r"Tổng công máy nén thực hiện bằng bao nhiêu kJ?", 27, "kJ", 0.1,
       loi=r"Ra $54\ \text{kJ}$ vì lấy số chu trình nhân nhiệt thu mỗi chu trình ; hoặc ra $81\ \text{kJ}$ vì lấy nhiệt toả ở dàn nóng.",
       ke=[(r"$A_{\text{tổng}}=n\times$ công của máy nén trong một chu trình", True),
           (r"$A_{\text{tổng}}=n\times$ nhiệt thu mỗi chu trình", r"Đó là nhiệt lấy từ ngăn lạnh, không phải công máy nén bỏ ra."),
           (r"$A_{\text{tổng}}=n\times$ nhiệt toả ở dàn nóng", r"Nhiệt toả ở dàn nóng bằng công cộng nhiệt thu ; không phải riêng công.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 4, "Bài 3. Nội năng. Định luật 1 của nhiệt động lực học", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code) — đã tự giải lại bằng Python"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
