# Vẽ sơ đồ thí điểm cho câu động lực học L10 (nét currentColor, nhãn chữ). Chạy: python3 ve-so-do.py
import math,os
out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'svg')
A='#2563eb'; R='#dc2626'
def svg(i,body,w=440,h=240):
    m='<defs>'+''.join(f'<marker id="a{i}{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 z" fill="{c}" stroke="none"/></marker>' for k,c in (('',  'currentColor'),('b',A),('r',R)))+'</defs>'
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" font-family="system-ui,sans-serif" font-size="14" fill="none" stroke="currentColor" stroke-width="2">{m}{body}</svg>'
    open(os.path.join(out,f'{i}.svg'),'w').write(s)
def arrow(i,x1,y1,x2,y2,c=A,t='',tx=0,ty=0):
    k='r' if c==R else 'b'
    r=f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="2.5" marker-end="url(#a{i}{k})"/>'
    if t: r+=f'<text x="{x2+tx:.1f}" y="{y2+ty:.1f}" fill="{c}" stroke="none" font-style="italic">{t}</text>'
    return r
def txt(x,y,s,anchor='start',c='currentColor'): return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{c}" stroke="none">{s}</text>'
def hatch(x1,y,x2): 
    return ''.join(f'<line x1="{x}" y1="{y}" x2="{x-10}" y2="{y+10}" stroke-width="1" opacity=".5"/>' for x in range(int(x1)+12,int(x2),12))
def block(cx,cy,ang,w=56,h=34):
    # hình chữ nhật có đáy nằm trên mặt dốc; (cx,cy)=tâm đáy; ang: góc quay (độ, dương = xoay ngược chiều kim đồng hồ trên màn hình = đi lên bên phải)
    return f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({-ang})"><rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" rx="3" fill="#f59e0b" fill-opacity=".25"/></g>'

# 1) mặt phẳng nghiêng góc α, trọng lực P (3123, 682630)
for i,deg in (('3123',30),('682630',20)):
    a=math.radians(deg); x0,y0=60,200; L=300
    x1,y1=x0+L*math.cos(a),y0-L*math.sin(a)
    b=f'<polygon points="{x0},{y0} {x1+0:.1f},{y0} {x1:.1f},{y1:.1f}" fill="currentColor" fill-opacity=".06"/>'
    b+=hatch(x0,y0,x1)
    t=0.55; bx,by=x0+L*t*math.cos(a),y0-L*t*math.sin(a)
    b+=block(bx,by,deg)
    cx,cy=bx-(-0)+0,by-17
    b+=arrow(i,bx-17*math.sin(a),by-17*math.cos(a),bx-17*math.sin(a),by-17*math.cos(a)+80,R,'<tspan font-weight="600">P</tspan>',6,4)  # (không vẽ N, không vẽ thành phần)
    b+=f'<path d="M{x0+55},{y0} A55 55 0 0 0 {x0+55*math.cos(a):.1f} {y0-55*math.sin(a):.1f}" stroke-width="1.5"/>'+txt(x0+68,y0-8,'α' if i=='3123' else '20°')
    svg(i,b,w=380)
# 4) 1473157: m1 trên bàn nối dây qua ròng rọc mép bàn với m2 treo
b='<path d="M20,110 H300" stroke-width="2.5"/><path d="M300,110 V215" stroke-width="2.5"/>'+hatch(20,110,300).replace('y2="120"','y2="120"')
b+='<rect x="120" y="70" width="70" height="40" rx="3" fill="#f59e0b" fill-opacity=".25"/>'+txt(155,96,'m₁','middle')
b+='<circle cx="318" cy="98" r="14" fill="currentColor" fill-opacity=".08"/><circle cx="318" cy="98" r="2" fill="currentColor"/>'
b+='<line x1="190" y1="84" x2="318" y2="84"/><line x1="332" y1="98" x2="332" y2="150"/>'
b+='<rect x="304" y="150" width="56" height="40" rx="3" fill="#f59e0b" fill-opacity=".25"/>'+txt(332,176,'m₂','middle')
b+=arrow('1473157',215,50,280,50,A,'',0,0)+txt(247,40,'chiều dương','middle',A)
svg('1473157',b,w=400,h=230)
# 5) máng đệm khí: xe — dây — ròng rọc — quả nặng, cổng quang, cảm biến lực
b='<rect x="20" y="132" width="290" height="10" rx="2" fill="currentColor" fill-opacity=".15"/>'
b+='<rect x="70" y="102" width="62" height="30" rx="3" fill="#f59e0b" fill-opacity=".25"/><circle cx="82" cy="138" r="4" fill="currentColor"/><circle cx="120" cy="138" r="4" fill="currentColor"/>'+txt(101,122,'xe','middle')
b+='<rect x="132" y="108" width="22" height="16" rx="2" fill="currentColor" fill-opacity=".2"/>'+txt(120,92,'cảm biến lực','middle')
b+='<line x1="154" y1="116" x2="326" y2="116"/>'
b+='<circle cx="340" cy="116" r="14" fill="currentColor" fill-opacity=".08"/><circle cx="340" cy="116" r="2" fill="currentColor"/>'
b+='<line x1="354" y1="116" x2="354" y2="170"/><rect x="338" y="170" width="32" height="30" rx="3" fill="#f59e0b" fill-opacity=".25"/>'+txt(354,220,'quả nặng','middle')
for x,l in ((200,'cổng 1'),(260,'cổng 2')):
    b+=f'<path d="M{x-8},96 v-26 h16 v26" stroke-width="2"/><line x1="{x}" y1="70" x2="{x}" y2="62" stroke-width="1.5" stroke-dasharray="3 3"/>'+txt(x,56,l,'middle')
svg('1551590',b,w=420,h=230)
import shutil; shutil.copy(os.path.join(out,'1551590.svg'),os.path.join(out,'1553214.svg'))
print(sorted(os.listdir(out)))
