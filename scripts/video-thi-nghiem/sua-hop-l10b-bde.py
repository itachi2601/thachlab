# Cổng mới L10b nhóm B–E (thầy duyệt 28/11 "Duyệt, sửa hộp"): sửa tối thiểu hộp exp lộ đáp án Dự đoán/chốt 22 clip mới — ghi theory.src.html, theory.html, bundle.json.
import json, sys
E = [
 ("l10-luc-ma-sat",
  "<strong>Rút ra:</strong> ma sát trượt tỉ lệ với $N$, và nhỏ hơn ma sát nghỉ cực đại.",
  "<strong>Rút ra:</strong> ma sát trượt phụ thuộc $N$ thế nào? So với ma sát nghỉ cực đại thì lớn hơn hay nhỏ hơn?"),
 ("l10-giai-bai-toan-dong-luc-hoc",
  "<strong>Quan sát:</strong> hai hộp tới chân ván gần như cùng lúc.",
  "<strong>Quan sát:</strong> so lúc hai hộp tới chân ván (video bên dưới)."),
 ("l10-giai-bai-toan-dong-luc-hoc",
  "<strong>Rút ra:</strong> gia tốc trượt không phụ thuộc khối lượng — đúng câu dự đoán ở mục I.",
  "<strong>Rút ra:</strong> gia tốc trượt có phụ thuộc khối lượng không? Đối chiếu với câu dự đoán ở mục I."),
 ("l10-giai-bai-toan-dong-luc-hoc",
  "rồi cộng lại, $T$ triệt tiêu, được $a = \\dfrac{m_2 g}{m_1 + m_2} = 2{,}0\\ \\text{m/s}^2$; đem so với $a$ đo.",
  "rồi cộng lại, $T$ triệt tiêu: tìm $a$ theo $m_1$, $m_2$, $g$ rồi đem so với $a$ đo."),
 ("l10-moment-luc",
  "<strong>Quan sát:</strong> thước quay tại chỗ quanh vạch $15$ cm (trọng tâm), không trượt đi.",
  "<strong>Quan sát:</strong> thước trượt đi hay quay tại chỗ? Nếu quay, quanh vạch nào (video bên dưới)?"),
 ("l10-moment-luc",
  "<strong>Rút ra:</strong> ngẫu lực chỉ làm quay; vật tự do quay quanh trọng tâm.",
  "<strong>Rút ra:</strong> ngẫu lực làm vật trượt đi hay chỉ làm quay? Vật tự do quay quanh điểm nào?"),
 ("l10-chuyen-dong-tron-deu",
  "<strong>Quan sát:</strong> góc AOB đo bằng thước đo độ được khoảng $57^\\circ$, nắp to hay nhỏ đều vậy.",
  "<strong>Quan sát:</strong> đo góc AOB bằng thước đo độ ở nắp to và nắp nhỏ, so các số đo (video bên dưới)."),
 ("l10-chuyen-dong-tron-deu",
  "<strong>Rút ra:</strong> 1 rad là góc chắn cung dài bằng bán kính, không phụ thuộc cỡ đường tròn. Cả vòng dài $2\\pi r$ nên ứng với $2\\pi\\ \\text{rad}$.",
  "<strong>Rút ra:</strong> 1 rad là góc chắn cung dài bằng bán kính. Góc ấy có phụ thuộc cỡ đường tròn không? Cả vòng dài $2\\pi r$ thì ứng với bao nhiêu rad?"),
 ("l10-luc-huong-tam",
  "<strong>Quan sát:</strong> quả nặng càng lớn, phải quay càng nhanh thì kẹp mới đứng yên sát miệng ống, tức $r$ giữ đúng $0{,}50\\ \\text{m}$.",
  "<strong>Quan sát:</strong> so tốc độ quay cần có ở ba quả nặng để kẹp đứng yên sát miệng ống, tức $r$ giữ đúng $0{,}50\\ \\text{m}$ (video bên dưới)."),
 ("l10-luc-huong-tam",
  "<strong>Rút ra:</strong> quả nặng đứng yên nên lực căng dây bằng $Mg$, và lực căng ấy đóng vai lực hướng tâm; so $Mg$",
  "<strong>Rút ra:</strong> quả nặng đứng yên thì lực căng dây bằng bao nhiêu? Lực căng ấy đóng vai lực gì với nút? So $Mg$"),
 ("l10-luc-huong-tam",
  "<strong>Quan sát:</strong> tới chỗ hở, bi lăn <strong>thẳng</strong> theo tiếp tuyến, không bật ra theo bán kính.",
  "<strong>Quan sát:</strong> tới chỗ hở, bi đi theo đường nào? Búng nhanh và búng chậm có khác không (video bên dưới)?"),
 ("l10-luc-huong-tam",
  "Mất lực đó, bi đi thẳng theo quán tính.",
  "Mất lực đó, bi đi theo hướng nào, vì sao?"),
 ("l10-bien-dang-vat-ran",
  "<strong>Quan sát:</strong> lò xo dây to dãn ít, lò xo dây mảnh dãn nhiều.",
  "<strong>Quan sát:</strong> so độ dãn của hai lò xo (video bên dưới)."),
 ("l10-khoi-luong-rieng-ap-suat",
  "<strong>Rút ra:</strong> bút đứng yên nên hai ngón chịu áp lực bằng nhau; đầu nhọn có $S$ nhỏ nên áp suất lớn hơn nhiều.",
  "<strong>Rút ra:</strong> bút đứng yên thì áp lực lên hai ngón so với nhau thế nào? Đầu nhọn có $S$ nhỏ thì áp suất ra sao?"),
]
ap = "--apply" in sys.argv; loi = 0
for bai, cu, moi in E:
    for f, a, b in [("theory.src.html", cu, moi), ("theory.html", cu, moi), ("bundle.json", json.dumps(cu, ensure_ascii=False)[1:-1], json.dumps(moi, ensure_ascii=False)[1:-1])]:
        p = f"content/lesson-samples/{bai}/{f}"; s = open(p, encoding="utf-8").read(); n = s.count(a)
        if n != 1: print(f"LOI {p}: {n} lần — {cu[:50]}"); loi += 1; continue
        if ap: open(p, "w", encoding="utf-8").write(s.replace(a, b))
print("LOI", loi, "| apply" if ap else "| dry-run")
