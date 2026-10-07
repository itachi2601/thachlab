import sys, subprocess, glob, os
from PIL import Image
pdf, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
dpi = sys.argv[4] if len(sys.argv) > 4 else '55'
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 4
for f in glob.glob('out/_s-*.png'): os.remove(f)
subprocess.run(['pdftoppm','-r',dpi,'-f',str(a),'-l',str(b),'-png',pdf,'out/_s'],check=True)
fs = sorted(glob.glob('out/_s-*.png'))
ims = [Image.open(f) for f in fs]; w, h = ims[0].size
rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (cols*w, rows*h), 'white')
for i, im in enumerate(ims): S.paste(im, ((i % cols)*w, (i // cols)*h))
S.save('out/sheet.png'); print(len(ims), S.size)
