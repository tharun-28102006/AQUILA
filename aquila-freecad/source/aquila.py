"""AQUILA rev A — parametric student demonstrator, dimensions in mm.
Requires Python 3.9+, cadquery==2.5.2. Run this file to regenerate exports.
STEP contains editable B-rep solids; this source preserves design parameters.
NOT pressure-rated. All PCB and connector placeholders require measurement.
"""
from pathlib import Path
import math
import json
import csv
import cadquery as cq
from cadquery import exporters

OUT = Path(__file__).resolve().parent.parent
PARTS = OUT / 'parts'
PARTS.mkdir(parents=True, exist_ok=True)
P = dict(shell_length=300.0, outer_diameter=110.0, wall=4.0,
         cap_thickness=8.0, collar_diameter=120.0, collar_length=18.0,
         lip_length=8.0, lip_diametral_clearance=0.6,
         oring_groove_width=3.2, oring_groove_depth=1.5, oring_section=2.0,
         cap_bolt_pcd=110.0, cap_hole=4.5, insert_pilot=4.6,
         tray_length=268.0, tray_width=84.0, tray_thickness=3.0,
         tray_bottom=-20.0, standoff_height=8.0, pcb_hole=3.4,
         fpga_length=130.0, fpga_width=80.0, fpga_mount_x=118.0, fpga_mount_y=70.0,
         rail_length=220.0, rail_width=16.0, rail_spacing=76.0,
         saddle_spacing=182.0, hull_slot_spacing=104.0,
         m5_slot_width=5.5, m5_slot_length=18.0,
         sensor_hole=16.2, debug_hole=12.2, status_hole=8.2,
         power_hole=12.2, analog_hole=12.2, transducer_hole=16.2,
         connector_projection=7.0)
P['inner_diameter'] = P['outer_diameter'] - 2 * P['wall']
P['overall_length'] = P['shell_length'] + 2 * P['cap_thickness'] + 2 * P['connector_projection']
L = P['shell_length'] / 2
R = P['outer_diameter'] / 2
RI = P['inner_diameter'] / 2
LIP = (P['inner_diameter'] - P['lip_diametral_clearance']) / 2


def box(l, w, h, x=0, y=0, z=0):
    return cq.Workplane('XY').box(l, w, h).translate((x, y, z))


def cyl(radius, length, x=0, y=0, z=0):
    return cq.Workplane('YZ', origin=(x, y, z)).circle(radius).extrude(length)


def zcyl(radius, height, x=0, y=0, z=0):
    return cq.Workplane('XY', origin=(x, y, z)).circle(radius).extrude(height)


def label(txt, size, x, y, z, depth=0.5):
    return cq.Workplane('XY', origin=(x, y, z)).text(txt, size, depth, font='DejaVu Sans', kind='bold', combine=False)


def cap_points():
    return [(P['cap_bolt_pcd']/2 * math.cos(math.radians(30 + 60*i)),
             P['cap_bolt_pcd']/2 * math.sin(math.radians(30 + 60*i))) for i in range(6)]


assembly = cq.Assembly(name='AQUILA_TX_PAYLOAD_REV_A')
manifest = []
shapes = {}
COLORS = {'shell':'#deded4', 'cap':'#263d43', 'orange':'#ec713e', 'tray':'#91a2a4',
          'metal':'#aab6bd', 'rubber':'#242e32', 'pcb':'#1d7163', 'chip':'#323e42', 'ink':'#24373b'}


def cad_color(color):
    return cq.Color(*(int(color[i:i+2],16)/255 for i in (1,3,5)))


def add(name, shape, category, color, printable=False, explode=(0,0,0), note=''):
    solid = shape.val() if isinstance(shape, cq.Workplane) else shape
    assert solid.isValid(), 'Invalid B-rep: ' + name
    assert solid.Volume() > 0, 'Empty solid: ' + name
    shapes[name] = solid
    assembly.add(solid, name=name, color=cad_color(color))
    exporters.export(solid, str(PARTS / (name + '.step')))
    exporters.export(solid, str(PARTS / (name + '.stl')), tolerance=0.14, angularTolerance=0.15)
    bounds = solid.BoundingBox()
    manifest.append(dict(id=name, name=name.replace('_',' '), category=category,
                         color=color, printable=printable, explode=list(explode), note=note,
                         bounds=[round(bounds.xlen,2),round(bounds.ylen,2),round(bounds.zlen,2)],
                         volume_mm3=round(solid.Volume(),2), valid=True,
                         solids=len(solid.Solids()), file='/cad/parts/'+name+'.stl'))
    print('Exported', name, flush=True)


shell = cyl(R, 2*L, -L).cut(cyl(RI, 2*L+2, -L-1))
for side in [-1, 1]:
    start = -L if side == -1 else L-P['collar_length']
    collar = cyl(P['collar_diameter']/2, P['collar_length'], start).cut(cyl(RI, P['collar_length']+2, start-1))
    collar = collar.edges('%Circle').fillet(0.7)
    shell = shell.union(collar)
    for y,z in cap_points():
        start_hole = -L-0.2 if side == -1 else L-9
        shell = shell.cut(cyl(P['insert_pilot']/2, 9.2, start_hole, y, z))
    shell = shell.cut(cyl(1.7, 5.2, -L-0.1 if side == -1 else L-5.1, 56, 0))
for y in [-42.5,42.5]:
    shell = shell.union(box(P['tray_length'], 10, 4, y=y, z=-22))
for x in [-124,124]:
    for y in [-40,40]:
        shell = shell.cut(zcyl(1.7, 9, x,y,-27))
add('01_Main_enclosure', shell, 'housing', COLORS['shell'], True, (0,0,50), '110 OD / 102 ID; integral collars and tray runners; blind M4 insert pilots.')

front_ports = [('SENSOR INPUT',-20,16,P['sensor_hole']),('DEBUG',20,16,P['debug_hole']),('STATUS',0,-23,P['status_hole'])]
rear_ports = [('POWER',-24,14,P['power_hole']),('ANALOG OUT',20,14,P['analog_hole']),('TRANSDUCER',0,-23,P['transducer_hole'])]
for side, title, ports, num in [(-1,'Front_service_cap',front_ports,'02'),(1,'Rear_interface_cap',rear_ports,'03')]:
    face_x = -L-P['cap_thickness'] if side == -1 else L
    cap = cyl(P['collar_diameter']/2,P['cap_thickness'],face_x).edges('%Circle').fillet(0.8)
    lip_x = -L if side == -1 else L-P['lip_length']
    cap = cap.union(cyl(LIP,P['lip_length'],lip_x).cut(cyl(LIP-6.5,P['lip_length']+0.2,lip_x-0.1)))
    groove_x = lip_x + (P['lip_length']-P['oring_groove_width'])/2
    groove = cyl(LIP+0.2,P['oring_groove_width'],groove_x).cut(cyl(LIP-P['oring_groove_depth'],P['oring_groove_width']+0.2,groove_x-0.1))
    cap = cap.cut(groove)
    for y,z in cap_points():
        cap = cap.cut(cyl(P['cap_hole']/2, P['cap_thickness']+2, face_x-1,y,z))
    for text,y,z,d in ports:
        cap = cap.cut(cyl(d/2, 20, -L-9 if side == -1 else L-9,y,z))
        recess_x = -L-P['cap_thickness']-0.1 if side == -1 else L+P['cap_thickness']-1
        cap = cap.cut(cyl(d/2+3,1.1,recess_x,y,z))
        plane = cq.Plane(origin=(-L-P['cap_thickness']-0.01 if side == -1 else L+P['cap_thickness']+0.01,y,z-13), xDir=(0,side,0), normal=(side,0,0))
        letters = cq.Workplane(plane).text(text,2.7,-0.5,font='DejaVu Sans',kind='bold',combine=False)
        cap = cap.cut(letters)
    pin_x = -L-0.1 if side == -1 else L-3
    cap = cap.cut(cyl(1.7,3.1,pin_x,56,0))
    add(num+'_'+title,cap,'front' if side==-1 else 'rear',COLORS['cap'],True,(side*52,0,0), 'Radial O-ring gland; six M4 clearance holes; alignment pin socket; engraved port labels.')
    ring = cq.Solid.makeTorus(LIP-P['oring_groove_depth']+P['oring_section']/2,P['oring_section']/2,
                             cq.Vector(groove_x+P['oring_groove_width']/2,0,0),cq.Vector(1,0,0))
    add('Seal_'+title,ring,'front' if side==-1 else 'rear',COLORS['orange'],False,(side*30,0,0),'Illustrative installed 2 mm O-ring; select catalog seal and calculate gland fill/stretch before manufacture.')
    pin = cyl(1.5,6,-L-3 if side==-1 else L-3,56,0)
    add('Alignment_pin_'+title,pin,'front' if side==-1 else 'rear',COLORS['metal'],False,(side*42,0,0))
    for i,(y,z) in enumerate(cap_points()):
        shaft = cyl(2,16,-L-8 if side==-1 else L-8,y,z)
        head_x = -L-P['cap_thickness']-3 if side==-1 else L+P['cap_thickness']
        bolt = shaft.union(cyl(3.7,3,head_x,y,z))
        bolt = bolt.cut(cq.Workplane('YZ',origin=(head_x-0.1,y,z)).polygon(6,3.2).extrude(3.2))
        add('M4_'+title+'_'+str(i+1),bolt,'front' if side==-1 else 'rear',COLORS['metal'],False,(side*62,0,0),'Simplified fastener; unthreaded CAD shank; select final lengths and inserts.')
    for i,(text,y,z,d) in enumerate(ports):
        outside = -L-P['cap_thickness'] if side==-1 else L+P['cap_thickness']
        stem_start = outside-2 if side==-1 else outside-10
        connector = cyl(d/2-0.2,12,stem_start,y,z)
        flange_start = outside-2 if side==-1 else outside
        connector = connector.union(cq.Workplane('YZ',origin=(flange_start,y,z)).polygon(6,d+6).extrude(2))
        nose_start = outside-P['connector_projection'] if side==-1 else outside+2
        connector = connector.union(cyl(d/2-0.6,5,nose_start,y,z))
        connector = connector.cut(cyl(max(1,d/2-2.2),2.8,nose_start-0.1 if side==-1 else nose_start+2.4,y,z))
        add('Connector_'+text.replace(' ','_'),connector,'front' if side==-1 else 'rear',COLORS['metal'],False,(side*75,0,0),'Generic sealed bulkhead placeholder; not a purchasable connector definition.')
        plug = cyl(d/2-2.3,1.2,nose_start+1.4 if side==-1 else nose_start+2.4,y,z)
        add('Insert_'+text.replace(' ','_'),plug,'front' if side==-1 else 'rear',COLORS['rubber'],False,(side*75,0,0),'Protected connector insert / blanking plug.')

zones = [dict(key='Sensor_interface',x=-118,l=28,w=50,mx=20,my=42,label='SENSORS'),
         dict(key='FPGA_DE10_Lite',x=-35,l=P['fpga_length'],w=P['fpga_width'],mx=P['fpga_mount_x'],my=P['fpga_mount_y'],label='MAX 10 / FPGA'),
         dict(key='Power_regulation',x=51,l=34,w=52,mx=26,my=44,label='POWER'),
         dict(key='Analog_TX_PCB',x=102,l=60,w=68,mx=52,my=58,label='ANALOG TX')]
tray = box(P['tray_length'],P['tray_width'],P['tray_thickness'],z=P['tray_bottom']+P['tray_thickness']/2).edges('|Z').fillet(2)
for x in [-105,32,70]:
    tray = tray.union(box(2,68,5,x=x,z=-14.5))
for z in zones:
    for dx in [-z['mx']/2,z['mx']/2]:
        for y in [-z['my']/2,z['my']/2]:
            x = z['x']+dx
            tray = tray.union(zcyl(3.2,P['standoff_height'],x,y,-17))
            tray = tray.cut(zcyl(P['pcb_hole']/2,13,x,y,-21))
for x in [-124,124]:
    for y in [-40,40]:
        tray = tray.cut(zcyl(1.7,5,x,y,-21))
for y in [-39,39]:
    tray = tray.cut(box(220,3,1.2,x=0,y=y,z=-17.4))
for x in [-108,32,70]:
    for y in [-37,37]:
        tray = tray.cut(box(4,2,5,x=x,y=y,z=-19))
add('04_Electronics_tray',tray,'tray',COLORS['tray'],True,(0,0,-50),'Parameterized M3 standoffs; cable channels and tie slots; M3 runner retention. Nominal holes, not verified PCB patterns.')

for i,z in enumerate(zones):
    pcb = box(z['l'],z['w'],1.6,x=z['x'],z=-8.2)
    for dx in [-z['mx']/2,z['mx']/2]:
        for y in [-z['my']/2,z['my']/2]:
            pcb = pcb.cut(zcyl(1.7,3,z['x']+dx,y,-9.5))
    pcb = pcb.union(label(z['label'],3,z['x'],-z['w']/2+8,-7.4,0.35))
    add('PCB_'+z['key'],pcb,'electronics',COLORS['pcb'],False,(0,0,25+i*5),'UNVERIFIED placeholder envelope and mounting pattern. Replace with measured board + components + connectors.')
    if z['key']=='Analog_TX_PCB':
        for j,(text,l,w) in enumerate([('DAC',12,16),('LPF',12,16),('AMP',14,20)]):
            x=z['x']-20+j*19
            chip=box(l,w,5,x=x,y=4,z=-4.9).union(label(text,2.5,x,4,-2.4,0.3))
            add('Signal_'+text,chip,'electronics',COLORS['chip'],False,(0,0,40))
    else:
        chip=box(22 if i==1 else 12,22 if i==1 else 15,7,x=z['x'],z=-3.9)
        add('Component_'+z['key'],chip,'electronics',COLORS['chip'],False,(0,0,35+i*5))
    for y in [-z['w']/2+4,z['w']/2-4]:
        header=box(min(z['l']-12,40),3,6,x=z['x'],y=y,z=-4.4)
        add('Header_'+z['key']+('_A' if y<0 else '_B'),header,'electronics',COLORS['rubber'],False,(0,0,40))
heat=box(116,58,2,x=-35,z=-16)
add('Heat_spreader',heat,'tray',COLORS['metal'],False,(0,0,-28),'Aluminum contact plate, isolate electrically; thermal path depends on real component location.')
add('Thermal_interface_pad',box(20,20,6,x=-35,z=-12),'tray','#699c9a',False,(0,0,-18),'Placeholder pad to underside FPGA region; confirm contact and allowable compression.')

for side in [-1,1]:
    x=side*P['saddle_spacing']/2
    ring=cyl(58.5,12,x-6).cut(cyl(55.3,14,x-7))
    lower=ring.intersect(box(16,140,65,x=x,z=-32.5))
    lower=lower.union(box(12,108,9,x=x,z=-59.5))
    upper=ring.intersect(box(16,140,62,x=x,z=31))
    for y in [-61,61]:
        lower=lower.union(box(12,16,6,x=x,y=y,z=-3))
        upper=upper.union(box(12,16,6,x=x,y=y,z=3))
        lower=lower.cut(zcyl(2.25,8,x,y,-7))
        upper=upper.cut(zcyl(2.25,8,x,y,-1))
    lower=lower.cut(cyl(55.3,14,x-7))
    upper=upper.cut(cyl(55.3,14,x-7))
    for y in [-P['rail_spacing']/2,P['rail_spacing']/2]:
        lower=lower.cut(zcyl(2.75,16,x,y,-66))
    add('05_Saddle_'+('front' if side<0 else 'rear'),lower,'mounting',COLORS['cap'],True,(0,0,-35),'Split saddle; 0.3 mm radial liner allowance; M4 clamp / M5 rail attachment.')
    add('06_Clamp_'+('front' if side<0 else 'rear'),upper,'mounting',COLORS['cap'],True,(0,0,40),'Removable upper clamp; 138 mm maximum mounting width across ears.')
for y in [-P['rail_spacing']/2,P['rail_spacing']/2]:
    rail=box(P['rail_length'],P['rail_width'],5,y=y,z=-66.5).edges('|Z').fillet(2)
    for x in [-91,-52,52,91]:
        slot=cq.Workplane('XY',origin=(x,y,-70)).slot2D(P['m5_slot_length'],P['m5_slot_width']).extrude(8)
        rail=rail.cut(slot)
    add('07_Mounting_rail_'+('left' if y<0 else 'right'),rail,'mounting',COLORS['metal'],True,(0,y*0.5,-50),'M5 slots: 18 x 5.5; hull attachment centers 104 x 76. Prefer machined aluminum.')

plate=box(114,32,6,x=-24,z=53).edges('|Z').fillet(2).cut(cyl(R,116,-82))
plate=plate.cut(label('AQUILA',10,-24,6,55.5,1))
plate=plate.cut(label('ADAPTIVE SONAR TX',3.0,-24,-5,55.5,1))
plate=plate.cut(label('MoES PROTOTYPE / TX PAYLOAD',2.5,-24,-11,55.5,1))
add('08_Identification_plate',plate,'housing',COLORS['orange'],True,(0,0,65),'Conformal adhesive-bonded ID plate; engraved AQUILA / ADAPTIVE SONAR TX / MoES Prototype.')

print('Exporting complete STEP assembly...',flush=True)
assembly.save(str(OUT/'AQUILA_assembly.step'))
exploded=cq.Assembly(name='AQUILA_EXPLODED_REV_A')
for part in manifest:
    exploded.add(shapes[part['id']],name=part['id'],color=cad_color(part['color']),loc=cq.Location(cq.Vector(*part['explode'])))
exploded.save(str(OUT/'AQUILA_exploded.step'))
(OUT/'parameters.json').write_text(json.dumps(P,indent=2))
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
with (OUT/'parameters.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['Parameter','Value','Units']); w.writerows((k,v,'mm') for k,v in P.items())

checks=[]
for name in ['01_Main_enclosure','02_Front_service_cap','03_Rear_interface_cap','04_Electronics_tray']:
    imported=cq.importers.importStep(str(PARTS/(name+'.step'))).val()
    checks.append(dict(test='STEP round trip: '+name,passed=imported.isValid() and abs(imported.Volume()-shapes[name].Volume())<0.1))
for a,b in [('01_Main_enclosure','02_Front_service_cap'),('01_Main_enclosure','03_Rear_interface_cap'),('01_Main_enclosure','04_Electronics_tray'),('04_Electronics_tray','PCB_FPGA_DE10_Lite'),('01_Main_enclosure','05_Saddle_front'),('01_Main_enclosure','06_Clamp_front')]:
    overlap=shapes[a].intersect(shapes[b]).Volume()
    checks.append(dict(test='Nominal clearance: '+a+' / '+b,passed=overlap<0.1,overlap_mm3=round(overlap,4)))
combined=cq.Compound.makeCompound(list(shapes.values())).BoundingBox()
report=dict(revision='A',units='mm',part_count=len(manifest),printable_parts=sum(p['printable'] for p in manifest),
            all_breps_valid=all(p['valid'] for p in manifest),assembly_bounds=[round(combined.xlen,2),round(combined.ylen,2),round(combined.zlen,2)],
            checks=checks,limitations=['No pressure, stress, waterproofing, thermal or manufacturing validation.','PCB envelopes and all PCB mounting patterns are provisional.','Connector models are placeholders, not supplier parts.','Interference checks cover listed structural pairs, not every fastener or cable.'])
(OUT/'validation.json').write_text(json.dumps(report,indent=2))
assert all(c['passed'] for c in checks),json.dumps(report,indent=2)
print(json.dumps(report,indent=2),flush=True)
