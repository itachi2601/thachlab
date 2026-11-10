# Sơ đồ tay cho câu chương 4 L12 (nét currentColor). Chạy: python3 ve-so-do.py
import os
out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'svg')
def txt(x,y,s,anchor='middle',size=14): return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="currentColor" stroke="none">{s}</text>'
# 458568: cảm biến báo khói ion hoá — hai bản kim loại song song nối pin, nguồn Am-241 ở giữa, chuông nối tiếp.
# Không vẽ đường đi của hạt α (đề hỏi chính điều đó).
b='<rect x="60" y="40" width="240" height="12" rx="2" fill="currentColor" fill-opacity=".25"/>'+txt(318,51,'+','start',18)
b+='<rect x="60" y="148" width="240" height="12" rx="2" fill="currentColor" fill-opacity=".25"/>'+txt(318,159,'−','start',18)
b+='<rect x="66" y="88" width="28" height="24" rx="3" fill="#f59e0b" fill-opacity=".35"/>'+txt(80,132,'nguồn α','middle',12)+txt(80,146,'²⁴¹Am','middle',12)
b+='<path d="M180,40 V20 H380 V80"/><path d="M180,160 V190 H380 V140"/>'
b+='<line x1="366" y1="80" x2="394" y2="80" stroke-width="3"/><line x1="372" y1="90" x2="388" y2="90" stroke-width="5"/>'+txt(402,90,'pin','start',13)
b+='<path d="M380,90 V108"/><circle cx="380" cy="124" r="16" fill="currentColor" fill-opacity=".06"/>'+txt(402,129,'chuông','start',13)
b+=txt(180,105,'không khí','middle',12)
s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 470 210" role="img" aria-label="Sơ đồ cảm biến báo khói ion hoá" font-family="system-ui,sans-serif" fill="none" stroke="currentColor" stroke-width="2">{b}</svg>'
open(os.path.join(out,'458568.svg'),'w').write(s)
