#!/usr/bin/env python3
"""Dựng bài 'Ôn thì & nối câu' (AVCN) -> theory.html + bundle.json. Nội dung nằm ngay trong file này."""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
TOPIC = "AVCN: Ôn thì & nối câu"
L = "abcd"


def speak(t):
    return f'<button type="button" class="tl-speak" data-tl-speak="{html.escape(t, quote=True)}" aria-label="Nghe">🔊</button>'


def quiz(name, opts, ans, ok, no, say=True):
    """Radio quiz kiểu tl-quiz; phương án tiếng Anh có data-tl-say để bấm là nghe."""
    s = '<div class="tl-quiz">'
    for i, o in enumerate(opts):
        cls = "tl-ok" if i == ans else "tl-no"
        sy = ' data-tl-say="1"' if say else ""
        s += (f'<input type="radio" name="{name}" id="{name}{L[i]}"><label for="{name}{L[i]}" '
              f'class="tl-opt {cls}"{sy}>{L[i]}. {o}</label>')
    s += (f'<div class="tl-fb tl-fb--ok"><p><strong>Đúng.</strong> {ok}</p></div>'
          f'<div class="tl-fb tl-fb--no"><p><strong>Chưa đúng.</strong> {no}</p></div></div>')
    return s


def box(kind, label, inner):
    return f'<div class="tl-box tl-box--{kind}"><p class="tl-label">{label}</p>{inner}</div>'


def ul(items):
    return '<ul class="avcn-list">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ex(en, vi):
    return f'{en} {speak(en)}<br><span class="avcn-trans">{vi}</span>'


class N:  # bộ đếm id quiz
    def __init__(s, p): s.p, s.n = p, 0
    def __call__(s): s.n += 1; return f"{s.p}-q{s.n}"


# ============================================================ TAB HỌC
def theory():
    nid = N("tl11")
    h = []
    # I. Tình huống
    h.append("<h3>I. Ba dòng trên bảng thông báo ở xưởng</h3>")
    h.append(box("think", "🔧 Tình huống ở xưởng",
        "<p>Em đi ngang bảng thông báo của xưởng cơ khí. Có ba dòng tiếng Anh, ba dòng nói về <strong>ba thời điểm khác nhau</strong>:</p>"
        + ul([ex("The <strong>lathe</strong> <strong>is running</strong> now.", "Máy tiện đang chạy.") ,
              ex("Yesterday the operator <strong>changed</strong> the cutting tool.", "Hôm qua thợ vận hành đã thay dao cắt."),
              ex("Tomorrow the technician <strong>will lubricate</strong> the spindle.", "Ngày mai kỹ thuật viên sẽ tra dầu trục chính.")])
        + "<p>Từ vựng em đã học rồi. Cái làm em lúng túng là <strong>động từ đổi hình</strong>: is running, changed, will lubricate.</p>"))
    qa = nid()
    h.append("<h3>II. Đoán trước khi học</h3>")
    h.append(box("think", "🤔 Dự đoán",
        "<p>Dòng nào trong ba dòng ở mục I nói về việc <strong>đã xảy ra rồi</strong>?</p>"
        + quiz(qa, ["The lathe is running now.", "Yesterday the operator changed the cutting tool.", "Tomorrow the technician will lubricate the spindle."], 1,
               "<em>Yesterday</em> (hôm qua) là dấu hiệu quá khứ, và <em>changed</em> là động từ quá khứ.",
               "Tìm từ chỉ thời gian trong mỗi dòng. Từ nào đặt việc đó ở phía sau lưng em?")))

    h.append("<p><strong>Hôm nay em sẽ:</strong> chọn đúng thì của động từ nhờ dấu hiệu thời gian, và nối hai câu ngắn thành một câu bằng and, but, so, because, although, who, which.</p>")
    h.append('<details class="tl-details"><summary>Chuẩn đầu ra của bài</summary><p>Sau bài này, em hiểu và nắm được:</p>'
        + ul(["Nhìn dấu hiệu thời gian (now, every day, yesterday, since, tomorrow) để chọn đúng thì: hiện tại đơn, hiện tại tiếp diễn, quá khứ đơn, hiện tại hoàn thành, tương lai.",
              "Nhận ra câu bị động <em>be + V3</em> rất hay gặp trong văn kỹ thuật (is made, was cut, are tightened).",
              "Nối hai câu bằng <em>and, but, so, because, although</em> đúng quan hệ: thêm ý, trái ngược, kết quả, lý do, nhượng bộ.",
              "Gộp hai câu bằng <em>who, which, that</em> để nói rõ một người hay một máy đang được nhắc tới."])
        + "</details>")

    # III. Năm thì
    h.append("<h3>III. Năm thì thợ cơ khí gặp mỗi ngày: nhìn dấu hiệu, chọn thì</h3>")
    h.append("<p>Không cần học thuộc cả sách ngữ pháp. Đề chỉ hỏi những thì dưới đây, và <strong>dấu hiệu thời gian</strong> thường nằm ngay trong câu.</p>")
    h.append(box("rule", "📘 Bảng tra nhanh: dấu hiệu → thì → công thức",
        ul(["<strong>every day, always, usually</strong><br>→ hiện tại đơn: <strong>V / V-s</strong>",
            "<strong>now, at the moment</strong><br>→ hiện tại tiếp diễn: <strong>is/are + V-ing</strong>",
            "<strong>yesterday, ago, last week</strong><br>→ quá khứ đơn: <strong>V-ed</strong>",
            "<strong>since, for, yet, just</strong><br>→ hiện tại hoàn thành: <strong>have/has + V3</strong>",
            "<strong>tomorrow, next week</strong><br>→ tương lai: <strong>will + V</strong>"])))

    h.append("<h4>1. Hiện tại đơn và hiện tại tiếp diễn: thói quen hay đang xảy ra?</h4>")
    h.append(box("rule", "📘 Hiện tại đơn: sự thật, quy trình, việc lặp lại",
        ul([ex("A drill <strong>makes</strong> round holes.", "Máy khoan tạo lỗ tròn. (sự thật)"),
            ex("The operator <strong>checks</strong> the coolant every morning.", "Thợ vận hành kiểm tra dung dịch làm mát mỗi sáng. (thói quen)")])
        + ul(["Chủ ngữ <em>he / she / it / một máy / một người</em> thì động từ thêm <strong>-s</strong>: the lathe rotate<strong>s</strong>."])))
    h.append(box("rule", "📘 Hiện tại tiếp diễn: việc đang xảy ra ngay lúc nói",
        ul([ex("The CNC machine <strong>is cutting</strong> the plate now.", "Máy CNC đang cắt tấm kim loại."),
            ex("Two welders <strong>are working</strong> at the moment.", "Lúc này hai thợ hàn đang làm việc.")])
        + ul(["Công thức: <strong>am / is / are + V-ing</strong>. Có <em>now, at the moment, Look!, Listen!</em> là nghĩ ngay tới thì này."])))
    h.append("<p><strong>Thử ngay:</strong></p>")
    h.append(box("think", "✏️ Câu 1", "<p>The grinder ______ the metal surface. (sự thật về chức năng của máy)</p>"
        + quiz(nid(), ["smooths", "is smoothing", "smoothed", "will smooth"], 0,
               "Không có dấu hiệu thời gian, nói về chức năng nên dùng hiện tại đơn. Chủ ngữ <em>the grinder</em> là số ít nên thêm <em>-s</em>.",
               "Câu không có now hay yesterday. Nó nói máy mài <em>nói chung</em> làm gì.")))
    h.append(box("think", "✏️ Câu 2", "<p>Listen! The press ______ a loud noise at the moment.</p>"
        + quiz(nid(), ["makes", "made", "is making", "has made"], 2,
               "<em>Listen!</em> và <em>at the moment</em> báo việc đang xảy ra: <em>is making</em>.",
               "Có hai dấu hiệu trong câu. Chúng báo việc xảy ra vào lúc nào?")))
    h.append(box("think", "✏️ Câu 3", "<p>The apprentice ______ the floor every afternoon.</p>"
        + quiz(nid(), ["is cleaning", "cleans", "cleaned", "has cleaned"], 1,
               "<em>Every afternoon</em> là thói quen lặp lại: hiện tại đơn, chủ ngữ số ít nên <em>cleans</em>.",
               "<em>Every afternoon</em> là việc xảy ra một lần hay lặp đi lặp lại?")))

    h.append("<h4>2. Quá khứ đơn và hiện tại hoàn thành: đã xong hẳn hay còn liên quan tới bây giờ?</h4>")
    h.append(box("rule", "📘 Quá khứ đơn: có mốc thời gian đã qua",
        ul([ex("The technician <strong>replaced</strong> the bearing yesterday.", "Hôm qua kỹ thuật viên đã thay vòng bi."),
            ex("We <strong>measured</strong> the shaft two hours ago.", "Hai giờ trước chúng tôi đã đo trục.")])
        + ul(["Dấu hiệu: <em>yesterday, ago, last week, in 2024</em>. Động từ thêm <strong>-ed</strong> (cut, made, ran là động từ bất quy tắc)."])))
    h.append(box("rule", "📘 Hiện tại hoàn thành: từ lúc đó đến nay, hoặc vừa xong",
        ul([ex("This workshop <strong>has used</strong> this lathe since 2020.", "Xưởng này dùng chiếc máy tiện này từ năm 2020."),
            ex("We <strong>have</strong> not <strong>finished</strong> the assembly yet.", "Chúng tôi chưa lắp xong.")])
        + ul(["Công thức: <strong>have / has + V3</strong> (he, she, it dùng <em>has</em>).",
              "Dấu hiệu: <em>since 2020, for three years, just, yet</em>.",
              "Có <em>yesterday</em> hoặc <em>ago</em> thì <strong>không</strong> dùng thì này."])))
    h.append(box("think", "✏️ Câu 4", "<p>The mechanic ______ the old filter last week.</p>"
        + quiz(nid(), ["removes", "removed", "has removed", "is removing"], 1,
               "<em>Last week</em> là mốc thời gian đã qua: quá khứ đơn <em>removed</em>.",
               "Mốc <em>last week</em> đã kết thúc hay còn kéo tới bây giờ?")))
    h.append(box("think", "✏️ Câu 5", "<p>The factory ______ this robot arm since 2022.</p>"
        + quiz(nid(), ["has bought", "buys", "bought", "is buying"], 0,
               "<em>Since 2022</em> (từ năm 2022 đến nay) đi với hiện tại hoàn thành, chủ ngữ <em>the factory</em> dùng <em>has</em>.",
               "<em>Since</em> nối một mốc trong quá khứ với hiện tại. Thì nào có nhiệm vụ đó?", say=True)))
    h.append(box("think", "✏️ Câu 6", "<p>We ______ not tested the new valve yet.</p>"
        + quiz(nid(), ["do", "have", "are", "will"], 1,
               "<em>Yet</em> đi với hiện tại hoàn thành: have not tested.",
               "Nhìn <em>yet</em> và <em>not</em>: câu nói việc đã xong hay chưa xong tính tới bây giờ?")))

    h.append("<h4>3. Tương lai và bị động: sẽ làm gì, vật được làm gì</h4>")
    h.append(box("rule", "📘 Tương lai: will + động từ nguyên mẫu",
        ul([ex("Tomorrow the technician <strong>will lubricate</strong> the spindle.", "Ngày mai kỹ thuật viên sẽ tra dầu trục chính."),
            ex("Next week we <strong>will install</strong> a new CNC machine.", "Tuần sau chúng tôi sẽ lắp một máy CNC mới.")])
        + ul(["Sau <em>will</em> là động từ <strong>nguyên mẫu</strong>, không thêm -s, -ed, -ing."])))
    h.append(box("rule", "📘 Bị động: be + V3 (vật bị tác động đứng đầu câu)",
        ul([ex("The workpiece <strong>is clamped</strong> to the chuck.", "Phôi được kẹp vào mâm cặp."),
            ex("Gears <strong>are made</strong> from hardened steel.", "Bánh răng được làm từ thép tôi."),
            ex("The bolts <strong>were tightened</strong> yesterday.", "Các bu lông đã được siết hôm qua.")])
        + ul(["Hiện tại: <strong>is / are + V3</strong>. Quá khứ: <strong>was / were + V3</strong>.",
              "Văn kỹ thuật ít nói ai làm, mà nói <em>vật được làm gì</em>. Thấy <em>is / are / was / were</em> + một từ -ed là nghĩ ngay tới bị động."])))
    h.append(box("think", "✏️ Câu 7", "<p>Next month the workshop ______ two new drill presses.</p>"
        + quiz(nid(), ["buys", "bought", "will buy", "has bought"], 2,
               "<em>Next month</em> chỉ tương lai: <em>will buy</em>.",
               "<em>Next month</em> nằm trước hay sau hôm nay?")))
    h.append(box("think", "✏️ Câu 8", "<p>Engine blocks ______ from cast iron.</p>"
        + quiz(nid(), ["make", "are made", "is making", "made"], 1,
               "Khối động cơ <em>được làm</em> từ gang: bị động <em>are made</em> (chủ ngữ số nhiều).",
               "Khối động cơ có tự làm ra chính nó không? Ai hoặc cái gì tác động lên nó?")))
    h.append(box("think", "✏️ Câu 9", "<p>The shaft ______ by an experienced operator last Friday.</p>"
        + quiz(nid(), ["is machined", "machines", "was machined", "will machine"], 2,
               "Trục <em>được gia công</em> (bị động) và <em>last Friday</em> là quá khứ: <em>was machined</em>.",
               "Có hai thứ cần đúng cùng lúc: ai tác động lên trục, và mốc thời gian <em>last Friday</em>.")))

    h.append("<h3>IV. Quy trình 3 bước chọn thì</h3>")
    h.append(box("rule", "🎯 Làm theo thứ tự này",
        ul(["<strong>Bước 1</strong>: gạch chân dấu hiệu thời gian (now, yesterday, tomorrow, since, every day…).",
            "<strong>Bước 2</strong>: không có dấu hiệu mà câu nói về sự thật, chức năng, quy trình → hiện tại đơn.",
            "<strong>Bước 3</strong>: chủ ngữ là một vật bị tác động (workpiece, bolts, gears) và sau <em>is/are/was/were</em> là một từ V3 → bị động."])))
    h.append(box("trap", "⚠️ Bốn cái bẫy hay mất điểm",
        ul(["Quên -s: <em>The machine cut</em> ✗ → The machine cut<strong>s</strong> ✓ (chủ ngữ số ít, hiện tại).",
            "Dấu hiệu <em>yesterday / ago</em> mà chọn <em>have + V3</em> ✗. Hai thứ này không đi cùng nhau.",
            "Sau <em>will</em> thêm -s hoặc -ed: <em>will lubricates</em> ✗ → will lubricate ✓.",
            "Có <em>now</em> mà chọn hiện tại đơn ✗ → <em>is / are + V-ing</em> ✓."])))

    # V. Nối câu: liên từ
    h.append("<h3>V. Nối hai câu bằng liên từ: and, but, so, because, although</h3>")
    h.append("<p>Hai câu ngắn đứng cạnh nhau thường có một quan hệ. Hỏi mình: <strong>ý thứ hai là thêm vào, trái ngược, kết quả hay lý do?</strong></p>")
    h.append(box("rule", "📘 Năm liên từ, năm quan hệ",
        ul([ex("The lathe turns the workpiece, <strong>and</strong> the tool cuts it.", "<strong>and</strong> = và (thêm ý cùng hướng)"),
            ex("The drill is small, <strong>but</strong> it is powerful.", "<strong>but</strong> = nhưng (hai ý trái nhau)"),
            ex("The floor was oily, <strong>so</strong> he wore safety boots.", "<strong>so</strong> = nên (<em>kết quả</em> đứng sau so)"),
            ex("He wore safety boots <strong>because</strong> the floor was oily.", "<strong>because</strong> = vì (<em>lý do</em> đứng sau because)"),
            ex("<strong>Although</strong> the lathe is old, it cuts accurately.", "<strong>although</strong> = mặc dù (không dùng thêm <em>but</em> ở vế sau)")])))
    h.append(box("rule", "🧠 Mẹo nhớ so và because",
        ul(["Cùng một chuyện, hai cách nói: <em>sàn dầu → đi ủng</em>.",
            "<strong>so</strong> đi theo mũi tên: nguyên nhân <strong>so</strong> kết quả.",
            "<strong>because</strong> đi ngược mũi tên: kết quả <strong>because</strong> nguyên nhân."])))
    h.append(box("think", "✏️ Câu 10", "<p>The saw is old, ______ it still cuts well.</p>"
        + quiz(nid(), ["so", "because", "but", "or"], 2,
               "Cưa cũ nhưng vẫn cắt tốt: hai ý trái nhau nên dùng <em>but</em>.",
               "Cưa cũ và cắt tốt có cùng chiều không?")))
    h.append(box("think", "✏️ Câu 11", "<p>The blade broke, ______ the operator stopped the machine.</p>"
        + quiz(nid(), ["but", "so", "because", "although"], 1,
               "Lưỡi cưa gãy là nguyên nhân, dừng máy là kết quả: dùng <em>so</em>.",
               "Việc nào xảy ra trước, việc nào là hệ quả của nó?")))
    h.append(box("think", "✏️ Câu 12", "<p>The technician cleaned the filter ______ it was blocked.</p>"
        + quiz(nid(), ["so", "because", "but", "and"], 1,
               "Phần sau chỗ trống nói <em>lý do</em> (bộ lọc bị tắc): dùng <em>because</em>.",
               "Bộ lọc bị tắc xảy ra trước hay sau khi kỹ thuật viên lau?")))
    h.append(box("think", "✏️ Câu 13", "<p>______ the bolt was very tight, it came loose.</p>"
        + quiz(nid(), ["Because", "So", "Although", "And"], 2,
               "Siết chặt mà vẫn lỏng ra: hai ý trái kỳ vọng nên dùng <em>Although</em> đứng đầu câu.",
               "Bu lông siết chặt thì ta kỳ vọng nó thế nào? Kết quả có đúng kỳ vọng không?")))

    # VI. who / which / that
    h.append("<h3>VI. Gộp hai câu bằng who, which, that</h3>")
    h.append("<p>Trong Article của Chapter 8 em đã gặp: <em>a machine called a lathe, <strong>which</strong> rotates the workpiece</em>. Từ <strong>which</strong> thay cho “a lathe” ở câu thứ hai.</p>")
    h.append(box("rule", "📘 Hai câu → một câu",
        ul([ex("A lathe is a machine. <strong>It</strong> rotates the workpiece.<br>→ A lathe is a machine <strong>which</strong> rotates the workpiece.", "Máy tiện là máy làm phôi quay."),
            ex("An operator is a person. <strong>He</strong> runs the machine.<br>→ An operator is a person <strong>who</strong> runs the machine.", "Thợ vận hành là người điều khiển máy.")])
        + ul(["<strong>who</strong> thay cho <em>người</em> (operator, welder, engineer).",
              "<strong>which</strong> thay cho <em>vật, máy, dụng cụ</em> (lathe, drill, caliper).",
              "<strong>that</strong> thay được cho cả hai: a machine <em>that</em> rotates…, a person <em>that</em> runs… Đề hay dùng who và which, nên nhớ hai từ này trước.",
              "Hai từ này <strong>đứng thay cho chủ ngữ</strong>, nên sau đó không viết thêm <em>it / he</em>."])))
    h.append(box("think", "✏️ Câu 14", "<p>A welder is a person ______ joins metal parts.</p>"
        + quiz(nid(), ["which", "who", "where", "what"], 1, "Welder là người nên dùng <em>who</em>.", "Thợ hàn là người hay vật?")))
    h.append(box("think", "✏️ Câu 15", "<p>A micrometer is a tool ______ measures very small thicknesses.</p>"
        + quiz(nid(), ["who", "which", "when", "whose"], 1, "Micrometer là dụng cụ (vật) nên dùng <em>which</em>.", "Panme là người hay vật?")))
    h.append(box("think", "✏️ Câu 16", "<p>Nối hai câu: <em>I use a wrench. It tightens nuts.</em></p>"
        + quiz(nid(), ["I use a wrench who tightens nuts.", "I use a wrench which tightens nuts.", "I use a wrench it tightens nuts.", "I use a wrench, and which tightens nuts."], 1,
               "Wrench là vật nên dùng <em>which</em>, và <em>which</em> thay luôn cho <em>it</em>.",
               "Có hai chỗ cần soát: vật hay người, và còn dư <em>it</em> không?")))
    h.append(box("think", "✏️ Câu 17", "<p>Nối hai câu: <em>The tool was blunt. The cut was rough.</em></p>"
        + quiz(nid(), ["The tool was blunt because the cut was rough.", "The tool was blunt, so the cut was rough.", "The tool was blunt although the cut was rough.", "The tool was blunt but the cut was rough."], 1,
               "Dao cùn là nguyên nhân, đường cắt xấu là kết quả: <em>so</em>.",
               "Hỏi: cái nào gây ra cái nào?")))

    # VII. Trả bài
    h.append("<h3>VII. Trả bài: gấp sách lại, trả lời 8 câu</h3>")
    h.append("<p>Nhớ lại được là nhớ lâu. Với mỗi câu: <strong>nói đáp án ra trước</strong>, rồi mới bấm mở. Câu nào chưa trả lời được thì quay lên mục tương ứng, rồi sang tab <strong>Đề mẫu</strong>.</p>")
    tb = [("Thấy <em>now</em> hoặc <em>at the moment</em> thì chia thì gì? Công thức?", "Hiện tại tiếp diễn: am / is / are + V-ing."),
          ("Thấy <em>yesterday</em> hoặc <em>ago</em> thì chia thì gì?", "Quá khứ đơn: V-ed (hoặc dạng bất quy tắc). Không dùng have + V3."),
          ("Thấy <em>since</em>, <em>for</em>, <em>yet</em> thì chia thì gì? Công thức?", "Hiện tại hoàn thành: have / has + V3."),
          ("Thấy <em>tomorrow</em> hoặc <em>next week</em> thì chia thế nào?", "will + động từ nguyên mẫu."),
          ("Câu bị động có công thức gì? Khi nào dùng?", "be + V3. Dùng khi nói vật được làm gì, ví dụ: The workpiece is clamped to the chuck."),
          ("Khác nhau giữa <em>so</em> và <em>because</em>?", "So đứng trước kết quả, because đứng trước lý do."),
          ("<em>who</em> và <em>which</em> dùng cho gì?", "who cho người, which cho vật; that dùng được cho cả hai."),
          ("Dịch sang tiếng Anh: <em>Máy tiện làm phôi quay.</em> Rồi dịch: <em>Gears are made from steel.</em>", "The lathe rotates the workpiece. / Bánh răng được làm từ thép.")]
    h.append('<div class="tl-box tl-box--think"><p class="tl-label">🎤 Trả bài</p>'
             + "".join(f'<details class="tl-details"><summary>{q}</summary><p>{a}</p></details>' for q, a in tb) + "</div>")
    h.append("<p><strong>Quay lại ba dòng đầu bài:</strong> giờ em nói được vì sao <em>is running</em>, <em>changed</em>, <em>will lubricate</em> lại có ba hình dạng khác nhau chưa?</p>")
    return "".join(h)


# ============================================================ TAB BÀI MẪU + LUYỆN TẬP
def qa_list(prefix, items, start=1):
    out = []
    for i, (q, opts, ans, why) in enumerate(items, start):
        n = f"{prefix}-q{i}"
        out.append('<div class="tl-box tl-box--think">' + f"<p><strong>{i}.</strong> {q}</p>" + quiz(n, opts, ans, why, "Đọc lại dấu hiệu trong câu, loại hai đáp án chắc chắn sai rồi chọn.") + "</div>")
    return "".join(out)


A = [("Every day the apprentice ______ the workshop floor before class.", ["cleans", "is cleaning", "cleaned", "will clean"], 0, "<em>Every day</em> = thói quen: hiện tại đơn, chủ ngữ số ít nên thêm -s."),
     ("Look at the screen! The robot arm ______ a car door now.", ["welds", "welded", "is welding", "has welded"], 2, "<em>Look!</em> và <em>now</em>: hiện tại tiếp diễn."),
     ("The press ______ the metal sheet ten minutes ago.", ["cuts", "cut", "is cutting", "will cut"], 1, "<em>Ago</em> = quá khứ; cut là dạng quá khứ của cut."),
     ("She ______ in this workshop for three years.", ["works", "worked", "has worked", "is working"], 2, "<em>For three years</em> (đến nay): hiện tại hoàn thành, chủ ngữ she dùng has."),
     ("The parts ______ by a robot in this factory.", ["assemble", "are assembled", "is assembling", "assembled"], 1, "Các chi tiết <em>được lắp</em>: bị động, chủ ngữ số nhiều dùng are.")]
B = [("The tool is cheap, ______ it is very strong.", ["so", "because", "but", "or"], 2, "Rẻ nhưng bền: hai ý trái nhau nên dùng <em>but</em>."),
     ("He cleaned the machine ______ it was covered with oil.", ["so", "because", "but", "although"], 1, "Phần sau là lý do: <em>because</em>."),
     ("The valve leaked, ______ the technician replaced it.", ["so", "because", "but", "although"], 0, "Van rò là nguyên nhân, thay van là kết quả: <em>so</em>."),
     ("A bolt is a fastener ______ holds two parts together.", ["who", "which", "what", "whom"], 1, "Bolt là vật nên dùng <em>which</em>."),
     ("The technician ______ fixed the pump is my teacher.", ["who", "which", "whose", "where"], 0, "Technician là người nên dùng <em>who</em>.")]


def worked():
    chienthuat_a = box("rule", "🎯 Chiến thuật", ul([
        "Gạch dấu hiệu thời gian trước: now, every day, ago, since, tomorrow.",
        "Có dấu hiệu thì theo bảng; không có thì nghĩ tới sự thật hoặc quy trình (hiện tại đơn).",
        "Thấy is / are / was / were + V3 thì nghĩ tới bị động.",
        "Loại ngay đáp án sai dạng (will + -s, have + yesterday)."]))
    chienthuat_b = box("rule", "🎯 Chiến thuật", ul([
        "Hỏi: ý thứ hai là thêm vào, trái ngược, kết quả hay lý do?",
        "Có <em>nhưng</em> trong đầu → but. Có <em>nên</em> → so. Có <em>vì</em> → because. Có <em>mặc dù</em> → although.",
        "Phía sau chỗ trống là người → who; là vật → which.",
        "Câu có although thì vế sau không cần thêm but."]))
    return [
        {"label": "Phần A · Chọn thì đúng",
         "body_html": "<p><strong>Part A: Choose the correct answer.</strong> (chọn thì của động từ)</p>" + chienthuat_a + qa_list("tl11m", A)},
        {"label": "Phần B · Nối câu",
         "body_html": "<p><strong>Part B: Choose the correct answer.</strong> (and, but, so, because, although, who, which)</p>" + chienthuat_b + qa_list("tl11m", B, start=6)},
    ]


LT = [  # (câu, opts, đáp án, giải thích)
    ("A lathe ______ the workpiece while the tool stays fixed. (chức năng của máy)", ["rotates", "is rotating", "rotated", "will rotate"], 0, "Chức năng của máy: hiện tại đơn."),
    ("Listen! The grinder ______ a strange noise now.", ["makes", "made", "is making", "has made"], 2, "Listen! và now: hiện tại tiếp diễn."),
    ("The technician ______ the faulty sensor last Monday.", ["replaces", "replaced", "has replaced", "is replacing"], 1, "Last Monday: quá khứ đơn."),
    ("We ______ this CNC machine since January.", ["use", "used", "are using", "have used"], 3, "Since: hiện tại hoàn thành."),
    ("Next week the company ______ two new milling machines.", ["buys", "bought", "will buy", "has bought"], 2, "Next week: will + V."),
    ("The metal sheets ______ into small parts by a press every month.", ["cut", "are cut", "is cutting", "cuts"], 1, "Tấm kim loại bị cắt: bị động are cut."),
    ("The shaft ______ yesterday by a skilled operator.", ["is machined", "was machined", "machines", "has machined"], 1, "Yesterday + bị động: was machined."),
    ("He ______ safety goggles every time he uses the grinder.", ["wears", "is wearing", "wore", "will wear"], 0, "Every time: thói quen, hiện tại đơn."),
    ("Be careful! The welder ______ a steel pipe at the moment.", ["welds", "is welding", "welded", "has welded"], 1, "At the moment: hiện tại tiếp diễn."),
    ("We have not finished the assembly ______.", ["yesterday", "ago", "yet", "last week"], 2, "Yet đi với hiện tại hoàn thành phủ định."),
    ("Two hours ago, the operator ______ the machine and left.", ["stops", "is stopping", "stopped", "will stop"], 2, "Ago: quá khứ đơn."),
    ("Tomorrow the technician ______ the spindle.", ["lubricated", "has lubricated", "will lubricate", "is lubricated"], 2, "Tomorrow: will + V."),
    ("Last year the workshop ______ a new safety rule.", ["introduces", "introduced", "has introduced", "will introduce"], 1, "Last year: quá khứ đơn."),
    ("Bolts ______ with a wrench.", ["tighten", "are tightened", "is tightening", "tightened"], 1, "Bu lông được siết: bị động."),
    ("The drill is very small, ______ it can make deep holes.", ["because", "so", "but", "or"], 2, "Nhỏ nhưng khoan sâu: but."),
    ("The oil was spilled on the floor, ______ the worker slipped.", ["but", "so", "or", "although"], 1, "Dầu đổ là nguyên nhân, trượt chân là kết quả: so."),
    ("The operator stopped the machine ______ he heard a strange noise.", ["so", "but", "because", "although"], 2, "Phần sau là lý do: because."),
    ("______ the part was expensive, the factory bought it.", ["Because", "So", "But", "Although"], 3, "Đắt mà vẫn mua: Although."),
    ("The welder wore a mask ______ the light can damage his eyes.", ["so", "because", "but", "although"], 1, "Phần sau là lý do: because."),
    ("A caliper is a tool ______ measures length.", ["who", "which", "where", "when"], 1, "Caliper là vật: which."),
    ("A mechanic is a person ______ repairs engines.", ["who", "which", "what", "where"], 0, "Mechanic là người: who."),
    ("The machine ______ stands near the door is a drill press.", ["who", "what", "that", "whose"], 2, "That dùng được cho vật."),
    ("Choose the best sentence: <em>The wheel was damaged. The machine stopped.</em>",
     ["The wheel was damaged, so the machine stopped.", "The wheel was damaged because the machine stopped.", "The wheel was damaged but the machine stopped.", "The wheel was damaged although the machine stopped."], 0, "Bánh bị hỏng → máy dừng: so."),
    ("Choose the best sentence: <em>A grinder is a machine. It smooths metal surfaces.</em>",
     ["A grinder is a machine who smooths metal surfaces.", "A grinder is a machine which smooths metal surfaces.", "A grinder is a machine it smooths metal surfaces.", "A grinder is a machine so smooths metal surfaces."], 1, "Machine là vật: which (thay cho it)."),
]


def exam():
    qs = [{"type": "multiple_choice", "question": q, "options": o, "answer": a, "explanation": e,
           "topic": TOPIC, "form": "ly_thuyet", "difficulty": "de"} for q, o, a, e in LT]
    return {"title": "Luyện tập: Ôn thì & nối câu", "topic": TOPIC, "difficulty": "de", "duration_minutes": 20,
            "subject_code": "avcn", "questions": qs, "new_topics": [TOPIC]}


if __name__ == "__main__":
    th = theory()
    open(os.path.join(HERE, "theory.html"), "w", encoding="utf-8").write(th)
    bundle = {"schema": "thachlab.lesson-bundle/v1",
              "target": {"class_name": "Anh văn chuyên ngành Cơ khí", "chapter_title": "Ôn thì và nối câu",
                         "lesson_title": "Ôn tập: Thì và nối câu (Tenses & Joining Sentences)"},
              "theory_title": "Học", "theory_subtitle": "25 phút · 5 thì · nối câu",
              "theory_html": th, "worked_examples": worked(), "exam": exam(), "raster_images": []}
    json.dump(bundle, open(os.path.join(HERE, "bundle.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", len(th), "bytes;", th.count('class="tl-quiz"'), "quiz Học;", len(LT), "câu luyện tập")
