#!/usr/bin/env python3
"""Kiểm logic tự chấm của các .tl-quiz trong theory.html — không cần trình duyệt.

CSS thật chỉ có hai rule quyết định phản hồi:
  .tl-quiz:has(input:checked + .tl-ok) > .tl-fb--ok { display: block }
  .tl-quiz:has(input:checked + .tl-no) > .tl-fb--no { display: block }
nên chỉ cần kiểm cấu trúc DOM: input đứng ngay trước label của nó, label và hai hộp
phản hồi là con TRỰC TIẾP của .tl-quiz, đúng một label .tl-ok.

Dùng: python3 check_quizzes.py <theory.html>
"""
import sys
from html.parser import HTMLParser


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children = []
        self.text = ""

    def cls(self):
        return (self.attrs.get("class") or "").split()

    def find_all(self, pred):
        out = []
        for c in self.children:
            if c.tag is not None:
                if pred(c):
                    out.append(c)
                out += c.find_all(pred)
        return out


VOID = {"input", "br", "img", "hr", "meta", "link", "source", "area", "base", "col"}


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node(None, [], None)
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].text += data


def main(path):
    p = Tree()
    p.feed(open(path, encoding="utf8").read())
    quizzes = [n for n in p.root.find_all(lambda n: "tl-quiz" in n.cls())]
    errors = []
    print(f"{len(quizzes)} quiz trong {path}")
    for i, q in enumerate(quizzes, 1):
        kids = [c for c in q.children if c.tag is not None]
        inputs = [c for c in kids if c.tag == "input"]
        labels = [c for c in kids if c.tag == "label"]
        names = {c.attrs.get("name") for c in inputs}
        n_ok = sum(1 for l in labels if "tl-ok" in l.cls())
        n_no = sum(1 for l in labels if "tl-no" in l.cls())
        if len(names) != 1 or None in names:
            errors.append(f"quiz {i}: số name khác nhau hoặc thiếu name ({names})")
        if n_ok != 1:
            errors.append(f"quiz {i}: có {n_ok} đáp án tl-ok (cần đúng 1)")
        if n_no < 1:
            errors.append(f"quiz {i}: không có đáp án tl-no")
        # input phải đứng NGAY TRƯỚC label của nó, trong cùng .tl-quiz
        pairs = [(kids[j], kids[j + 1]) for j in range(len(kids) - 1)
                 if kids[j].tag == "input" and kids[j + 1].tag == "label"]
        if len(pairs) != len(inputs):
            errors.append(f"quiz {i}: có input không đứng ngay trước label ({len(inputs)} input, {len(pairs)} cặp)")
        for inp, lab in pairs:
            if inp.attrs.get("id") != lab.attrs.get("for"):
                errors.append(f"quiz {i}: for/id không khớp ({inp.attrs.get('id')} vs {lab.attrs.get('for')})")
        ids = [c.attrs.get("id") for c in inputs]
        if len(set(ids)) != len(ids) or None in ids:
            errors.append(f"quiz {i}: id trùng hoặc thiếu ({ids})")
        fb = [c for c in kids if c.tag == "div" and any(x.startswith("tl-fb") for x in c.cls())]
        has_ok = any("tl-fb--ok" in c.cls() for c in fb)
        has_no = any("tl-fb--no" in c.cls() for c in fb)
        if not (has_ok and has_no):
            errors.append(f"quiz {i}: thiếu .tl-fb--ok/--no là con trực tiếp")
        # mỗi phản hồi phải có đúng một <p> để CSS .tl-fb p hiển thị đẹp
        for c in fb:
            if not c.find_all(lambda n: n.tag == "p"):
                errors.append(f"quiz {i}: hộp phản hồi không có <p>")
        mark = "✓" if n_ok == 1 and n_no >= 1 and len(pairs) == len(inputs) else "✗"
        print(f"  {mark} quiz {i}: {len(inputs)} đáp án · ok={n_ok} · no={n_no} · name={names.pop()}")
    for e in errors:
        print("✗", e)
    print("KẾT LUẬN:", "OK — mọi đáp án đúng hiện phản hồi xanh, đáp án sai hiện phản hồi đỏ" if not errors else f"{len(errors)} LỖI")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
