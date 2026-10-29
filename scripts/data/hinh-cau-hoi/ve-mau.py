# Khuôn vẽ có tham số cho câu động lực học L10: dốc, lực kéo xiên, vật treo hai dây. Chạy: python3 ve-mau.py
# Tham số lấy tay từ đề từng câu (bảng INCLINE / PULL); hình chỉ nêu dữ kiện ĐỀ CHO, không vẽ phản lực/thành phần (đó là đáp án).
import math,os
out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'svg')
A='#2563eb'; R='#dc2626'; BOX='<rect {p} rx="3" fill="#f59e0b" fill-opacity=".25"/>'
def svg(i,body,w,h):
    m='<defs>'+''.join(f'<marker id="a{i}{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 z" fill="{c}" stroke="none"/></marker>' for k,c in (('','currentColor'),('b',A),('r',R)))+'</defs>'
    open(os.path.join(out,f'{i}.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" font-family="system-ui,sans-serif" font-size="14" fill="none" stroke="currentColor" stroke-width="2">{m}{body}</svg>')
def T(x,y,s,anchor='start',c='currentColor',rot=None):
    r=f' transform="rotate({rot} {x} {y})"' if rot is not None else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{c}" stroke="none"{r}>{s}</text>'
def arrow(i,x1,y1,x2,y2,c=A,both=False,w=2.5):
    k='r' if c==R else ('b' if c==A else '')
    ms=f' marker-start="url(#a{i}{k})"' if both else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{ms} marker-end="url(#a{i}{k})"/>'
def hatch(x1,y,x2): return ''.join(f'<line x1="{x}" y1="{y}" x2="{x-10}" y2="{y+10}" stroke-width="1" opacity=".5"/>' for x in range(int(x1)+12,int(x2),12))

def incline(i,a=30,lab=None,L=None,h=None,m=None,start='mid',x=None,P=False,rope=False,F=None,floor=False):
    r=math.radians(a); x0,y0=40,205; Ls=260; xr,yt=x0+Ls*math.cos(r),y0-Ls*math.sin(r)
    xe=xr+(110 if floor else 0)
    b=f'<polygon points="{x0},{y0} {xr:.1f},{y0} {xr:.1f},{yt:.1f}" fill="currentColor" fill-opacity=".06"/>'
    b+=f'<line x1="{xr:.1f}" y1="{y0}" x2="{xe:.1f}" y2="{y0}"/>' if floor else ''
    b+=hatch(x0,y0,xe)
    t={'top':.8,'mid':.5,'foot':.25}[start]
    bx,by=x0+Ls*t*math.cos(r),y0-Ls*t*math.sin(r)
    wd,ht=56,34
    b+=f'<g transform="translate({bx:.1f},{by:.1f}) rotate({-a})">'+BOX.format(p=f'x="{-wd/2}" y="{-ht}" width="{wd}" height="{ht}"')+(f'<text x="0" y="{-ht/2+5}" text-anchor="middle" fill="currentColor" stroke="none" font-size="13">{m}</text>' if m else '')+'</g>'
    cx,cy=bx-ht/2*math.sin(r),by-ht/2*math.cos(r)
    if P: b+=arrow(i,cx,cy,cx,cy+78,R)+T(cx+8,cy+78,'<tspan font-weight="600">P</tspan>','start',R)
    if rope:  # dây song song mặt dốc, buộc vào tường ở đỉnh
        ex,ey=bx+wd/2*math.cos(r)-ht/2*math.sin(r),by-wd/2*math.sin(r)-ht/2*math.cos(r)
        tx,ty=xr-6,yt-ht/2*math.cos(r)+2
        b+=f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{tx+0:.1f}" y2="{ey-(tx-ex)*math.tan(r):.1f}" stroke-dasharray="0"/>'
        b+=f'<line x1="{xr:.1f}" y1="{yt-40:.1f}" x2="{xr:.1f}" y2="{yt+8:.1f}" stroke-width="5"/>'
    if F:
        ex,ey=bx+wd/2*math.cos(r)-ht/2*math.sin(r),by-wd/2*math.sin(r)-ht/2*math.cos(r)
        b+=arrow(i,ex,ey,ex+55*math.cos(r),ey-55*math.sin(r),A)+T(ex+55*math.cos(r)+6,ey-55*math.sin(r)-6,F,'start',A)
    if x:
        s=-1 if x=='down' else 1
        ox,oy=bx-(ht+16)*math.sin(r),by-(ht+16)*math.cos(r)
        b+=arrow(i,ox,oy,ox+s*60*math.cos(r),oy-s*60*math.sin(r),A)+T(ox+s*60*math.cos(r)+(-4 if s<0 else 6),oy-s*60*math.sin(r)-8,'x','start',A)
    # góc
    b+=f'<path d="M{x0+52},{y0} A52 52 0 0 0 {x0+52*math.cos(r):.1f} {y0-52*math.sin(r):.1f}" stroke-width="1.5"/>'+T(x0+62,y0-8,lab or f'{a}°')
    if L:
        nx,ny=-math.sin(r),-math.cos(r); mx,my=x0+Ls/2*math.cos(r)+nx*-1,y0-Ls/2*math.sin(r)
        b+=T(mx-26,my-10-(0),L,'middle',rot=-a) if False else T(x0+Ls*0.45*math.cos(r)+22*math.sin(r),y0-Ls*0.45*math.sin(r)+22*math.cos(r)+5,L,'middle',rot=-a)
    if h:
        b+=arrow(i,xr+16,yt,xr+16,y0,'currentColor',both=True,w=1.5)+T(xr+24,(yt+y0)/2+5,h)
    W=max(xe+90,400)
    svg(i,b,W,235)

def pull(i,a=30,lab=None,F=None,m=None):
    b='<line x1="30" y1="170" x2="380" y2="170"/>'+hatch(30,170,380)
    b+=BOX.format(p='x="140" y="116" width="90" height="54"')+(T(185,148,m,'middle') if m else '')
    r=math.radians(a); sx,sy=230,143; L=120
    b+=arrow(i,sx,sy,sx+L*math.cos(r),sy-L*math.sin(r),R)+T(sx+L*math.cos(r)+6,sy-L*math.sin(r)+4,F or 'F','start',R)
    b+=f'<line x1="{sx}" y1="{sy}" x2="{sx+135}" y2="{sy}" stroke-dasharray="4 4" stroke-width="1.2" opacity=".7"/>'
    b+=f'<path d="M{sx+60},{sy} A60 60 0 0 0 {sx+60*math.cos(r):.1f},{sy-60*math.sin(r):.1f}" stroke-width="1.5"/>'+T(sx+68,sy-10,lab or f'{a}°')
    svg(i,b,420,200)

def hung(i,a=45,m=None):
    r=math.radians(a); b='<line x1="30" y1="30" x2="390" y2="30" stroke-width="3"/>'+''.join(f'<line x1="{x}" y1="30" x2="{x-10}" y2="20" stroke-width="1" opacity=".5"/>' for x in range(42,390,12))
    cx,by=210,150; dx=110; ty=by-dx*math.tan(r)*0+0
    ty=by-dx*math.tan(r)
    ty=max(ty,30)
    # hai dây từ hai điểm trên trần tới đỉnh khối; điểm trên trần cách theo tan
    h=by-30; dxx=h/math.tan(r)
    for s in (-1,1):
        b+=f'<line x1="{cx+s*dxx:.1f}" y1="30" x2="{cx}" y2="{by}"/>'
    b+=f'<line x1="{cx-dxx:.1f}" y1="{by}" x2="{cx+dxx:.1f}" y2="{by}" stroke-dasharray="4 4" stroke-width="1.2" opacity=".6"/>'
    b+=BOX.format(p=f'x="{cx-34}" y="{by}" width="68" height="44"')+(T(cx,by+28,m,'middle') if m else '')
    for s in (-1,1):
        b+=f'<path d="M{cx+s*46},{by} A46 46 0 0 {1 if s>0 else 0} {cx+s*46*math.cos(r):.1f},{by-46*math.sin(r):.1f}" stroke-width="1.5"/>'+T(cx+s*(62 if s>0 else 62)+(0 if s>0 else -34),by-8,f'{a}°')
    svg(i,b,420,215)

# ---- bảng tham số: id → thông số lấy từ đề ----
INCLINE={
 3123:dict(lab='α',P=True),
 682630:dict(a=20,P=True,m='5 kg'),
 1474150:dict(h='h = 1 m',start='top',m='m',x='down'),
 1473156:dict(m='hộp',x='down'),
 1539214:dict(start='top',x='down'),
 339255:dict(L='L = 2 m',start='top',x='down'),
 683669:dict(L='L = 5 m',start='top',m='m',x='down'),
 1511600:dict(lab=' ',L='L = 10 m',h='h = 5 m',floor=True,start='top',x='down'),
 1531862:dict(a=60,m='4 kg',P=True),
 1531675:dict(m='4 kg',P=True),
 1531934:dict(start='top',x='down'),
 1531869:dict(x='down'),
 339483:dict(L='BC = 50 cm',start='top',x='down'),
 339825:dict(L='L = 5 m',start='top',x='down'),
 1551642:dict(lab='α',m='m',P=True),
 1551546:dict(lab='α',P=True),
 1543921:dict(F='F = 20 N'),
 1538687:dict(a=37,lab=' ',L='50 cm',h='30 cm',x='down'),
 1544028:dict(m='xe'),
 1544048:dict(L='L = 10 m',m='1 kg',start='top',x='down'),
 1544049:dict(L='L = 10 m',m='1 kg',start='top',x='down'),
 1544061:dict(a=37,lab=' ',h='h = 1,5 m',start='top',x='down'),
 1539719:dict(m='10 kg'),
 683216:dict(m='ô tô'),
 1544705:dict(L='L = 2 m',m='2 kg',start='top',x='down'),
 1544666:dict(L='L = 8 m',m='1,5 kg',start='top',x='down'),
 683905:dict(a=40,start='top',x='down'),
 1531937:dict(a=37,x='up'),
 1531926:dict(lab='α',x='up'),
 1473160:dict(lab='α',x='up'),
 1531866:dict(lab='α',x='down'),
 1531863:dict(lab='α',x='down'),
 1551645:dict(lab='α',x='down'),
 1551651:dict(lab='α',m='m',x='down'),
 1553275:dict(lab='α',m='m',x='down'),
 1543999:dict(m='30 kg',rope=True),
 685496:dict(m='P = 80 N',rope=True),
}
PULL={
 681370:dict(a=60,F='F = 50 N',m='4 kg'),
 680922:dict(a=30,F='F = 10 N',m='2 kg'),
 681784:dict(a=30,F='F = 0,8 N',m='400 g'),
 682598:dict(a=30,F='F = 5 N',m='3 kg'),
 1512557:dict(a=30,F='F = 150 N',m='thùng'),
 1531668:dict(a=60,F='F = 20 N'),
 1531674:dict(a=37,F='F = 50 N'),
 1531861:dict(lab='α',F='F',m='m'),
 1551643:dict(lab='α',F='F',m='m'),
 680351:dict(a=60,F='F',m='20 kg'),
 1544044:dict(a=45,F='F = 48 N',m='m'),
 1544047:dict(a=45,F='F = 2√2 N',m='1 kg'),
 1551652:dict(lab='α',F='F',m='m'),
 1553276:dict(lab='α',F='F',m='m'),
 680381:dict(lab='α',F='F',m='12 kg'),
}
for i,p in INCLINE.items(): incline(i,**p)
for i,p in PULL.items(): pull(i,**p)
hung(1544000,45,'10 kg')
print(len(INCLINE)+len(PULL)+1,'hình')
