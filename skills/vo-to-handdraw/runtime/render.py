import json, math, hashlib, subprocess, sys
from pathlib import Path
import cv2, numpy as np
import cairosvg

DEFAULT_BG = "#F5EBD7"
DEFAULT_INK = "#303030"


def hex_to_bgr(hex_color: str):
    h = hex_color.lstrip('#')
    return (int(h[4:6],16), int(h[2:4],16), int(h[0:2],16))


def partial_poly(points, frac):
    p = np.array(points, dtype=float)
    if len(p) <= 1:
        return p
    if frac <= 0:
        return p[:1]
    if frac >= 1:
        return p
    seg = np.linalg.norm(np.diff(p, axis=0), axis=1)
    total = seg.sum()
    target = frac * total
    acc = 0.0
    out = [p[0]]
    for i, s in enumerate(seg):
        if acc + s < target:
            out.append(p[i+1])
            acc += s
        else:
            r = (target - acc) / max(s, 1e-9)
            out.append(p[i] + r*(p[i+1]-p[i]))
            break
    return np.array(out)


def path_length(points):
    p = np.array(points, dtype=float)
    if len(p) <= 1:
        return 0.0
    return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())


def draw_poly(frame, points, color, width=2, closed=False):
    p = np.array(points, dtype=float)
    if len(p) < 2:
        return
    cv2.polylines(frame, [np.round(p).astype(np.int32).reshape(-1,1,2)], closed, color, width, cv2.LINE_AA)


def asset_library():
    def pine_cluster():
        out=[]
        for x,y,s in [(0,0,1.0),(36,6,0.85),(74,2,1.08)]:
            out += [
                [[x,70*s+y],[x,25*s+y]],
                [[x-16*s,y+50*s],[x,y+20*s],[x+16*s,y+50*s]],
                [[x-13*s,y+39*s],[x,y+12*s],[x+13*s,y+39*s]],
                [[x-9*s,y+29*s],[x,y+6*s],[x+9*s,y+29*s]],
            ]
        return out

    def aspen_oak():
        return [
            [[0,80],[0,24]], [[18,82],[18,18]],
            [[-14,26],[-8,14],[0,8],[12,14],[16,28],[8,38],[-8,36],[-14,26]],
            [[48,84],[48,42]],
            [[24,46],[28,24],[40,16],[56,14],[74,22],[80,38],[76,54],[62,58],[42,58],[30,52],[24,46]],
        ]

    def juniper_scrub():
        return [
            [[0,60],[10,40],[18,46],[28,22],[38,44],[52,34],[60,60]],
            [[88,62],[98,42],[108,48],[116,24],[126,42],[138,32],[148,60]],
        ]

    def slickrock():
        xs = np.linspace(0, 160, 48)
        y1 = 42 - 22*np.sin(np.pi*np.linspace(0,1,48)) - 4*np.sin(3*np.pi*np.linspace(0,1,48))
        y2 = 62 - 9*np.sin(np.pi*np.linspace(0,1,48))
        return [list(map(list, np.c_[xs, y1])), list(map(list, np.c_[20+0.88*xs, y2]))]

    def canyon_river():
        t = np.linspace(0,1,60)
        rim1 = np.c_[220*t, 22 + 8*np.sin(2*np.pi*t) + 5*np.sin(5*np.pi*t)]
        rim2 = np.c_[220*t, 74 + 8*np.sin(1.8*np.pi*t + 0.4)]
        river = np.c_[120 + 60*np.sin(2.1*np.pi*t)*0.35 + 40*t, 140 - 105*t]
        return [list(map(list, rim1)), list(map(list, rim2)), list(map(list, river))]

    def map_frame():
        return [
            [[0,0],[240,0],[240,170],[0,170],[0,0]],
            [[12,12],[228,12],[228,158],[12,158],[12,12]],
            [[44,42],[82,70],[112,58],[136,90],[124,120],[160,130],[194,92]],
            [[38,120],[58,120]], [[182,38],[202,38]]
        ]

    def heart():
        t=np.linspace(0, np.pi, 28)
        left=np.c_[20+14*np.cos(t), 16+14*np.sin(t)]
        right=np.c_[44+14*np.cos(t), 16+14*np.sin(t)]
        bottom=np.array([[8,24],[32,54],[56,24]],float)
        return [list(map(list,left)), list(map(list,right)), list(map(list,bottom))]

    def location_pin():
        return [[[20,58],[12,32],[16,14],[26,6],[38,8],[46,18],[48,32],[20,58]], [[20,28],[25,23],[20,18],[15,23],[20,28]]]

    def ring():
        theta=np.linspace(0,2*np.pi,48)
        outer=np.c_[24+18*np.cos(theta), 24+18*np.sin(theta)]
        inner=np.c_[24+9*np.cos(theta), 24+9*np.sin(theta)]
        gem=np.array([[24,3],[18,12],[24,18],[30,12],[24,3]],float)
        return [list(map(list,outer)), list(map(list,inner)), list(map(list,gem))]

    def couple():
        return [
            [[0,18],[6,12],[12,18],[6,24],[0,18]], [[6,24],[6,54]], [[6,34],[-6,44]], [[6,34],[18,44]], [[6,54],[-2,70]], [[6,54],[14,70]],
            [[34,18],[40,12],[46,18],[40,24],[34,18]], [[40,24],[40,54]], [[40,34],[28,44]], [[40,34],[52,44]], [[40,54],[32,70]], [[40,54],[48,70]],
        ]

    def coffee_table():
        return [
            [[0,16],[74,16]], [[10,16],[10,46]], [[64,16],[64,46]],
            [[20,10],[28,10],[30,16],[18,16],[20,10]], [[42,10],[50,10],[52,16],[40,16],[42,10]],
        ]

    def house():
        return [
            [[0,34],[34,4],[68,34]], [[10,34],[10,74],[58,74],[58,34]], [[24,74],[24,52],[42,52],[42,74]],
        ]

    def bike_rider():
        theta=np.linspace(0,2*np.pi,40)
        w1=np.c_[0+16*np.cos(theta), 38+16*np.sin(theta)]
        w2=np.c_[56+16*np.cos(theta), 38+16*np.sin(theta)]
        return [
            list(map(list,w1)), list(map(list,w2)),
            [[0,38],[22,18],[40,38],[56,38]], [[22,18],[30,8]], [[30,8],[38,18]], [[22,18],[14,34]],
            [[30,8],[32,0],[38,6],[30,8]], [[36,18],[44,10],[48,34]], [[18,42],[28,56]],
        ]

    def mountain_ridge():
        return [[[0,78],[38,36],[72,66],[112,22],[158,70],[198,42],[240,82]],
                [[44,60],[70,42],[92,64]], [[126,52],[150,34],[174,61]]]

    def forest_cluster():
        return pine_cluster()

    def water_landscape():
        t=np.linspace(0,1,60)
        shore=np.c_[230*t, 70+14*np.sin(2*np.pi*t)]
        water=np.c_[230*t, 110+5*np.sin(5*np.pi*t)]
        return [list(map(list,shore)),list(map(list,water)),[[12,122],[220,122]]]

    def rock_landscape():
        return [[[0,92],[26,58],[52,60],[74,30],[100,34],[126,12],[158,52],[184,48],[214,82]],
                [[22,104],[54,88],[92,94],[126,72],[162,82],[206,64]]]

    def office_cue():
        return [[[0,70],[96,70]],[[12,70],[12,118]],[[84,70],[84,118]],
                [[28,52],[68,52],[68,70],[28,70],[28,52]],[[74,30],[74,70]],[[62,30],[86,30]]]

    def medical_cue():
        theta=np.linspace(0,2*np.pi,44)
        loop=np.c_[30+20*np.cos(theta),42+26*np.sin(theta)]
        return [list(map(list,loop)),[[30,68],[30,92],[64,92]],[[64,92],[72,84],[80,92],[88,84],[96,92]]]

    def travel_cue():
        return [[[0,25],[44,8],[78,22],[44,18],[44,34],[34,38],[28,21],[0,25]],
                [[4,48],[102,48]]]

    def celebration_cue():
        return [[[0,50],[8,22],[18,50],[0,50]],[[30,50],[38,16],[48,50],[30,50]],
                [[60,50],[68,25],[78,50],[60,50]],[[9,18],[14,8]],[[38,12],[38,2]],[[70,20],[76,10]]]

    def journey_line():
        return [[[0,70],[42,42],[88,62],[132,30],[178,48],[228,22]]]

    def landscape_accent():
        return [[[0,70],[42,36],[78,64],[118,26],[162,68],[214,42]],[[18,92],[210,92]]]

    return {
        'pine_cluster': pine_cluster(),
        'aspen_oak': aspen_oak(),
        'juniper_scrub': juniper_scrub(),
        'slickrock': slickrock(),
        'canyon_river': canyon_river(),
        'map_frame': map_frame(),
        'heart': heart(),
        'location_pin': location_pin(),
        'ring': ring(),
        'couple': couple(),
        'coffee_table': coffee_table(),
        'house': house(),
        'bike_rider': bike_rider(),
        'mountain_ridge': mountain_ridge(),
        'forest_cluster': forest_cluster(),
        'water_landscape': water_landscape(),
        'rock_landscape': rock_landscape(),
        'office_cue': office_cue(),
        'medical_cue': medical_cue(),
        'travel_cue': travel_cue(),
        'celebration_cue': celebration_cue(),
        'journey_line': journey_line(),
        'landscape_accent': landscape_accent(),
    }


def load_hand(asset_path: Path, size=160):
    if not asset_path.exists():
        return None, (0,0)
    png = cairosvg.svg2png(bytestring=asset_path.read_bytes(), output_width=size)
    arr = np.frombuffer(png, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    meta_path = asset_path.with_suffix('.json')
    if meta_path.exists():
        meta=json.loads(meta_path.read_text(encoding='utf-8'))
        vb=meta.get('viewbox',[320,220]); anchor=meta.get('tip_anchor_viewbox',[29,176])
        scale=img.shape[1]/float(vb[0])
        return img,(int(anchor[0]*scale),int(anchor[1]*scale))
    return img,(0,int(img.shape[0]*0.8))


def overlay_rgba(dst, src, x, y):
    h,w = src.shape[:2]
    x0=max(0,x); y0=max(0,y); x1=min(dst.shape[1],x+w); y1=min(dst.shape[0],y+h)
    if x0>=x1 or y0>=y1: return
    sx0=x0-x; sy0=y0-y; sx1=sx0+(x1-x0); sy1=sy0+(y1-y0)
    patch=src[sy0:sy1,sx0:sx1]
    a=patch[:,:,3:4]/255.0
    dst[y0:y1,x0:x1]=(patch[:,:,:3]*a + dst[y0:y1,x0:x1]*(1-a)).astype(np.uint8)


def transform_paths(paths, x=0, y=0, scale=1.0):
    out=[]
    for p in paths:
        arr=np.array(p, dtype=float)*scale + np.array([x,y])
        out.append(arr)
    return out


def render(spec_path: Path, out_path: Path, audit_override=None):
    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    meta = spec['meta']
    W = meta.get('canvas',{}).get('width',960)
    H = meta.get('canvas',{}).get('height',540)
    FPS = meta.get('fps',15)
    bg = np.array(hex_to_bgr(meta.get('background', DEFAULT_BG)), dtype=np.uint8)
    ink = hex_to_bgr(meta.get('ink', DEFAULT_INK))
    show_audit = meta.get('show_audit_subtitles', False) if audit_override is None else audit_override
    assets = asset_library()
    for name, rel in meta.get('asset_registry', {}).items():
        ap = (spec_path.parent / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
        obj = json.loads(ap.read_text(encoding='utf-8'))
        paths = obj.get('paths', obj)
        if not isinstance(paths, list):
            raise ValueError(f'invalid asset registry entry {name}: expected list of paths')
        assets[name] = paths
    hand_img, hand_anchor = load_hand(Path(__file__).resolve().parents[1]/'assets'/'feminine-hand-fineline-v1.svg')

    raw_path = out_path.with_suffix('.raw.mp4')
    vw = cv2.VideoWriter(str(raw_path), cv2.VideoWriter_fourcc(*'mp4v'), FPS, (W,H))

    for scene in spec['scenes']:
        scene_dur = float(scene['duration_s'])
        frame_count = int(round(scene_dur * FPS))
        path_cache = {}
        for a in scene['actions']:
            if a['type'] == 'path_draw':
                path_cache[a['id']] = np.array(a['points'], dtype=float)
        for fi in range(frame_count):
            t = fi / FPS
            frame = np.empty((H,W,3), np.uint8); frame[:] = bg
            hand_tip = None
            for a in scene['actions']:
                typ = a['type']
                start = float(a.get('start',0))
                dur = max(0.001, float(a.get('duration',0.001)))
                progress = (t-start)/dur
                if typ == 'path_draw':
                    if progress <= 0: continue
                    pts = np.array(a['points'], dtype=float)
                    q = partial_poly(pts, min(1.0, progress))
                    draw_poly(frame, q, ink, int(a.get('style',{}).get('width',2)), False)
                    if 0 < progress < 1: hand_tip = q[-1]
                elif typ == 'asset_draw':
                    if progress <= 0: continue
                    paths = transform_paths(assets[a['asset']], a.get('x',0), a.get('y',0), a.get('scale',1.0))
                    lengths = np.array([max(1e-6, path_length(p)) for p in paths], dtype=float)
                    total = lengths.sum(); target = min(1.0, progress) * total; acc=0.0
                    for p,L in zip(paths, lengths):
                        if target >= acc + L:
                            draw_poly(frame, p, ink, int(a.get('width',2)), False)
                        elif target > acc:
                            q = partial_poly(p, (target-acc)/L)
                            draw_poly(frame, q, ink, int(a.get('width',2)), False)
                            hand_tip = q[-1]
                            break
                        acc += L
                elif typ == 'text_write':
                    if progress <= 0: continue
                    text = a['text']
                    n = min(len(text), max(1, int(math.ceil(min(1.0,progress)*len(text)))))
                    txt = text[:n]
                    font = getattr(cv2, a.get('font','FONT_HERSHEY_SCRIPT_SIMPLEX')) if isinstance(a.get('font'), str) else cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
                    fs = float(a.get('font_scale',0.8)); th = int(a.get('thickness',1))
                    cv2.putText(frame, txt, (int(a['x']), int(a['y'])), font, fs, ink, th, cv2.LINE_AA)
                    if n < len(text):
                        size = cv2.getTextSize(txt, font, fs, th)[0]
                        hand_tip = (int(a['x'])+size[0]+2, int(a['y']))
                elif typ == 'actor_follow_path':
                    if progress <= 0: continue
                    base_path = path_cache[a['path_ref']]
                    pos = max(0.0, min(1.0, progress))
                    idx = min(len(base_path)-2, max(0, int(pos*(len(base_path)-1))))
                    pt = base_path[idx]
                    d = base_path[min(len(base_path)-1, idx+1)] - base_path[idx]
                    ang = math.degrees(math.atan2(d[1], d[0])) if np.linalg.norm(d) > 1e-9 else 0.0
                    ang = max(-24, min(24, ang))
                    actor_paths = []
                    for p in assets[a['asset']]:
                        arr = np.array(p, dtype=float)
                        arr = arr - arr.mean(axis=0)
                        arr *= float(a.get('scale',1.0))
                        rad = math.radians(ang)
                        rot = np.array([[math.cos(rad), -math.sin(rad)],[math.sin(rad), math.cos(rad)]])
                        arr = arr @ rot.T + np.array([pt[0], pt[1] + float(a.get('offset_y', -24))])
                        actor_paths.append(arr)
                    for p in actor_paths:
                        draw_poly(frame, p, ink, int(a.get('width',2)), False)
                elif typ == 'hold':
                    continue
            if hand_tip is not None and hand_img is not None:
                x = int(hand_tip[0]-hand_anchor[0]); y = int(hand_tip[1]-hand_anchor[1])
                overlay_rgba(frame, hand_img, x, y)
            if show_audit and scene.get('subtitle'):
                cv2.rectangle(frame, (0,H-92), (W,H), (226,240,245), -1)
                words=scene['subtitle'].split(); lines=[]; cur=''
                for word in words:
                    test=(cur+' '+word).strip()
                    if cv2.getTextSize(test,cv2.FONT_HERSHEY_SIMPLEX,0.48,1)[0][0] > W-48 and cur:
                        lines.append(cur); cur=word
                    else: cur=test
                if cur: lines.append(cur)
                lines=lines[:2]
                for li,line in enumerate(lines):
                    cv2.putText(frame,line,(24,H-56+li*22),cv2.FONT_HERSHEY_SIMPLEX,0.48,(55,55,55),1,cv2.LINE_AA)
                cv2.putText(frame, scene['id'], (24,H-10), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (90,90,90), 1, cv2.LINE_AA)
            vw.write(frame)
    vw.release()
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(raw_path),'-c:v','libx264','-pix_fmt','yuv420p','-crf','21',str(out_path)], check=True)
    raw_path.unlink(missing_ok=True)
    return out_path


def main():
    if len(sys.argv) < 3:
        print('usage: python3 runtime/render.py input.json output.mp4 [--audit|--clean]')
        raise SystemExit(2)
    spec = Path(sys.argv[1])
    out = Path(sys.argv[2])
    audit_override = None
    if '--audit' in sys.argv:
        audit_override = True
    elif '--clean' in sys.argv:
        audit_override = False
    render(spec, out, audit_override)
    print(out)
    print(hashlib.sha256(out.read_bytes()).hexdigest())

if __name__ == '__main__':
    main()
