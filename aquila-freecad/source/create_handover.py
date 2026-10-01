"""Create the dimensioned GA drawing, handover PDF and downloadable archives."""
from pathlib import Path
import json, math, html, zipfile, hashlib, textwrap
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parent.parent
P=json.loads((ROOT/'parameters.json').read_text())
M=json.loads((ROOT/'manifest.json').read_text())
W,H=1190,842
C=canvas.Canvas(str(ROOT/'AQUILA_engineering.pdf'),pagesize=(W,H))
C.setTitle('AQUILA Rev A — General Arrangement and Engineering Handover')
SVG=[]
INK='#293e44'; MUTED='#7c8d92'; ORANGE='#dc683b'; LIGHT='#f1f4f2'

def line(x1,y1,x2,y2,color=INK,width=1,dash=False):
    C.setStrokeColor(color); C.setLineWidth(width); C.setDash(4,3) if dash else C.setDash()
    C.line(x1,H-y1,x2,H-y2)
    SVG.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="4 3"' if dash else '')+'/>')

def rect(x,y,w,h,fill=None):
    C.setStrokeColor(INK); C.setLineWidth(1); C.setDash()
    if fill: C.setFillColor(fill)
    C.rect(x,H-y-h,w,h,stroke=1,fill=int(bool(fill)))
    SVG.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill or "none"}" stroke="{INK}"/>')

def circle(x,y,r,fill=None):
    C.setStrokeColor(INK); C.setDash()
    if fill:C.setFillColor(fill)
    C.circle(x,H-y,r,stroke=1,fill=int(bool(fill)))
    SVG.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill or "none"}" stroke="{INK}"/>')

def text(x,y,t,size=11,color=INK):
    C.setFillColor(color); C.setFont('Helvetica',size); C.drawString(x,H-y,t)
    SVG.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}">{html.escape(t)}</text>')

def dim(x1,y1,x2,y2,t):
    line(x1,y1,x2,y2,MUTED)
    if y1==y2:
        for x in [x1,x2]:line(x,y1-5,x,y1+5,MUTED)
        text((x1+x2)/2-len(t)*2.8,y1-7,t,10)
    else:
        for y in [y1,y2]:line(x1-5,y,x1+5,y,MUTED)
        text(x1+8,(y1+y2)/2,t,10)

rect(25,25,W-50,H-50)
text(52,62,'AQUILA',28)
text(52,84,'ADAPTIVE SOFTWARE-DEFINED SONAR | TX PAYLOAD MODULE',10,MUTED)
text(815,58,'GENERAL ARRANGEMENT',17)
text(815,82,'REV A  /  mm  /  A3 landscape  /  NOT TO SCALE',10,MUTED)
line(25,104,1165,104)
text(55,132,'01 / SIDE ELEVATION',11)
S=1.7; X=110; Y=262
sx=lambda v:X+(v+165)*S
sy=lambda v:Y-v*S
rect(sx(-150),sy(55),300*S,110*S,LIGHT)
for x in [-150,132]:rect(sx(x),sy(60),18*S,120*S)
for x in [-158,150]:rect(sx(x),sy(60),8*S,120*S)
for x in [-165,158]:rect(sx(x),sy(22),7*S,44*S)
for x in [-97,85]:rect(sx(x),sy(58.5),12*S,117*S)
rect(sx(-110),sy(-64),220*S,5*S)
line(sx(-173),Y,sx(173),Y,MUTED,1,True)
line(sx(-142),sy(51),sx(142),sy(51),MUTED,1,True)
line(sx(-142),sy(-51),sx(142),sy(-51),MUTED,1,True)
rect(sx(-134),sy(-17),268*S,3*S)
for x,l,w in [(-118,28,50),(-35,130,80),(51,34,52),(102,60,68)]:
    rect(sx(x-l/2),sy(1),l*S,10*S)
rect(sx(-81),sy(56),114*S,4*S)
for a,b,y,t in [(-165,165,145,'330 OVERALL'),(-158,158,388,'316 CAP FACES'),(-150,150,414,'300 SHELL'),(-91,91,441,'182 SADDLE CENTERS')]:
    dim(sx(a),y,sx(b),y,t)
    line(sx(a),y-8,sx(a),y+8,MUTED);line(sx(b),y-8,sx(b),y+8,MUTED)
dim(sx(165)+23,sy(60),sx(165)+23,sy(-69),'129')
text(111,469,'Shell OD110 / ID102 / wall 4.  Collar OD120.  End-cap face thickness 8.',11)

text(825,132,'02 / REAR INTERFACE',11)
CX,CY=981,265
circle(CX,CY,102,LIGHT);circle(CX,CY,93.5);circle(CX,CY,86.7)
line(CX-115,CY,CX+115,CY,MUTED,1,True);line(CX,CY-115,CX,CY+115,MUTED,1,True)
for i in range(6):
    a=math.radians(30+60*i);circle(CX+55*S*math.cos(a),CY-55*S*math.sin(a),2.25*S)
for title,y,z,d in [('POWER',-24,14,12.2),('ANALOG OUT',20,14,12.2),('TRANSDUCER',0,-23,16.2)]:
    circle(CX+y*S,CY-z*S,d*S/2);text(CX+y*S-len(title)*2.1,CY-z*S+24,title,7)
text(832,391,'6 x Ø4.5 on Ø110 PCD',11)
text(832,411,'POWER / ANALOG OUT: Ø12.2',10)
text(832,430,'TRANSDUCER: Ø16.2, future reserve',10)
text(832,451,'Front: SENSOR Ø16.2 / DEBUG Ø12.2',10)
text(832,469,'STATUS Ø8.2. Connector holes provisional.',10)
line(52,494,1137,494,MUTED)
text(55,521,'03 / REMOVABLE TRAY — PLAN',11)
TX,TY=95,576; scale=1.8
rect(TX,TY,268*scale,84*scale,LIGHT)
for name,x,l,w,mx,my in [('SENSOR',-118,28,50,20,42),('FPGA / DE10-Lite',-35,130,80,118,70),('POWER',51,34,52,26,44),('ANALOG TX',102,60,68,52,58)]:
    bx=TX+(x+134-l/2)*scale;by=TY+(84-w)*scale/2
    rect(bx,by,l*scale,w*scale)
    text(bx+5,by+w*scale/2,name,7.7)
    for dx in [-mx/2,mx/2]:
        for dy in [-my/2,my/2]:circle(TX+(x+134+dx)*scale,TY+(42+dy)*scale,1.7*scale)
dim(TX,TY-19,TX+268*scale,TY-19,'268')
dim(TX+268*scale+17,TY,TX+268*scale+17,TY+84*scale,'84')
text(95,752,'3 mm tray / 8 mm standoffs / M3 Ø3.4. All PCB patterns UNVERIFIED.',9)
text(705,521,'04 / SEAL + MOUNTING NOTES',11)
for i,t in enumerate(['Lip Ø101.4 x 8 long; bore Ø102.','Radial groove: 3.2 wide x 1.5 deep.','Illustrative O-ring section: 2.0.','Verify catalog seal, gland fill and compression.','','Two rails: 220 x 16 x 5; 76 center spacing.','M5 slots: 18 x 5.5; hull spacing 104 x 76.','Split clamp envelope width: 138.','110 mm shell diameter excludes brackets.']):text(705,548+i*20,t,10)
line(25,775,1165,775)
text(48,796,'STUDENT PROTOTYPE — NO PRESSURE / DEPTH RATING — VERIFY ALL HARDWARE FITS',10,ORANGE)
text(951,796,'AQUILA-GA-001  |  1',10)
(ROOT/'AQUILA_drawing.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1190" height="842" viewBox="0 0 1190 842"><rect width="1190" height="842" fill="white"/>'+''.join(SVG)+'</svg>')
C.showPage()

def heading(title,subtitle='AQUILA REV A | ENGINEERING HANDOVER'):
    C.setFillColor(INK);C.setFont('Helvetica-Bold',24);C.drawString(54,H-65,title)
    C.setFillColor(MUTED);C.setFont('Helvetica',10);C.drawString(54,H-87,subtitle)
    C.setStrokeColor(MUTED);C.line(54,H-103,W-54,H-103)

def footer():
    C.setFillColor(MUTED);C.setFont('Helvetica',9);C.drawString(54,32,'PROVISIONAL DESIGN — FIT / SEAL / THERMAL VALIDATION REQUIRED');C.drawRightString(W-54,32,str(C.getPageNumber()))

heading('Parameter schedule')
y=126
for i,(k,v) in enumerate(P.items()):
    if y>H-75:footer();C.showPage();heading('Parameter schedule / continued');y=126
    C.setFillColor(INK);C.setFont('Helvetica',11);C.drawString(60,H-y,k.replace('_',' '));C.drawString(490,H-y,f'{v:g} mm')
    C.setStrokeColor('#e0e6e3');C.line(60,H-y-8,650,H-y-8);y+=24
footer();C.showPage()
heading('Custom parts and purchased hardware')
y=136
for p in M:
    if not p['printable']:continue
    C.setFont('Helvetica-Bold',12);C.setFillColor(INK);C.drawString(60,H-y,p['name']);y+=20
    C.setFont('Helvetica',10)
    for t in textwrap.wrap(p['note'],145):C.drawString(60,H-y,t);y+=15
    y+=12
C.setFont('Helvetica',11)
for t in ['Reference geometry: four PCBs, component/header envelopes, six bulkheads, connector inserts,',
          'two O-rings, two alignment pins, twelve M4 cap screws, heat spreader and thermal pad.',
          'Buy real connectors, seals, fasteners and thermal materials; do not print the reference geometry.',
          'M3 tray/PCB, M4 clamp and M5 mounting hardware must be selected and added during fit review.']:
    C.drawString(60,H-y,t);y+=19
footer();C.showPage()
heading('Manufacturing, assembly and assumptions')
y=125
notes=(ROOT/'BUILD_NOTES.md').read_text().splitlines()
for raw in notes:
    if raw.startswith('# '):continue
    if raw.startswith('## '):
        if y>H-120:footer();C.showPage();heading('Engineering handover / continued');y=125
        y+=12;C.setFont('Helvetica-Bold',13);C.setFillColor(INK);C.drawString(60,H-y,raw[3:]);y+=23
    elif raw:
        C.setFont('Helvetica',10.5);C.setFillColor(INK)
        for t in textwrap.wrap(raw,165):
            if y>H-65:footer();C.showPage();heading('Engineering handover / continued');y=125;C.setFont('Helvetica',10.5);C.setFillColor(INK)
            C.drawString(60,H-y,t.encode('latin-1','replace').decode('latin-1'));y+=15
        y+=8
footer();C.save()
with zipfile.ZipFile(ROOT/'AQUILA_printable_parts.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in M:
        if p['printable']:z.write(ROOT/'parts'/(p['id']+'.stl'),p['id']+'.stl')
    z.write(ROOT/'BUILD_NOTES.md','BUILD_NOTES.md')
checksums=[]
for f in sorted(ROOT.rglob('*')):
    if f.is_file() and f.suffix in ['.step','.stl','.pdf','.py','.svg']:
        checksums.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(ROOT)))
(ROOT/'SHA256SUMS.txt').write_text('\n'.join(checksums)+'\n')
with zipfile.ZipFile(ROOT/'AQUILA_complete_package.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(ROOT.rglob('*')):
        if f.is_file() and f.name not in ['AQUILA_complete_package.zip','downloads.json'] and '__pycache__' not in str(f):z.write(f, str(f.relative_to(ROOT)))
files=['AQUILA_assembly.step','AQUILA_exploded.step','AQUILA_printable_parts.zip','AQUILA_engineering.pdf','AQUILA_complete_package.zip']
(ROOT/'downloads.json').write_text(json.dumps({f:dict(bytes=(ROOT/f).stat().st_size,megabytes=round((ROOT/f).stat().st_size/1048576,2)) for f in files},indent=2))
print('Created dimensioned SVG, multi-page PDF, printable ZIP and complete CAD package.')
