from __future__ import annotations
import hashlib, json, math, re
from dataclasses import asdict
from pathlib import Path
from .vo_ingest import Segment, ingest

CUE_RULES = [
    (('mountain','alpine','ridge','summit','peak'), 'mountain_ridge'),
    (('forest','pine','tree','woods','aspen','oak'), 'forest_cluster'),
    (('river','lake','ocean','water','coast','beach'), 'water_landscape'),
    (('desert','rock','slickrock','canyon','ledge','cliff'), 'rock_landscape'),
    (('bike','bicycle','ride','rider','cycling','trail'), 'bike_rider'),
    (('coffee','cafe','date'), 'coffee_table'),
    (('home','house','move','key'), 'house'),
    (('ring','proposal','marry','marriage','wedding'), 'ring'),
    (('love','together','couple','relationship'), 'couple'),
    (('office','career','work','leadership','team'), 'office_cue'),
    (('doctor','medical','hospital','care'), 'medical_cue'),
    (('travel','trip','flight','journey','adventure'), 'travel_cue'),
    (('celebrate','cheers','gratitude','thank'), 'celebration_cue'),
    (('map','keepsake','poster','personalize','product'), 'map_frame'),
]

GENERIC_CUES=['journey_line','landscape_accent']


def cues_for(text:str)->list[str]:
    s=text.lower(); out=[]
    for words,cue in CUE_RULES:
        if any(w in s for w in words): out.append(cue)
    if not out: out=GENERIC_CUES.copy()
    return out[:4]


def group_beats(segs:list[Segment], min_s=5.5, target_s=8.0, max_s=11.0, max_beats=6):
    groups=[]; cur=[]; start=None
    for seg in segs:
        if start is None: start=seg.start_s
        cur.append(seg)
        dur=cur[-1].end_s-start
        if dur>=min_s or dur>=max_s:
            groups.append(cur); cur=[]; start=None
    if cur:
        if groups and (cur[-1].end_s-cur[0].start_s)<min_s:
            groups[-1].extend(cur)
        else: groups.append(cur)
    while len(groups)>max_beats:
        pairs=[(groups[i+1][-1].end_s-groups[i][0].start_s,i) for i in range(len(groups)-1)]
        _,i=min(pairs)
        groups[i]=groups[i]+groups[i+1]; del groups[i+1]
    return groups


def seed_points(seed:str,w=960,h=540,kind='path'):
    n=int(hashlib.sha256(seed.encode()).hexdigest()[:12],16)
    y0=300+(n%75); pts=[]
    for i,x in enumerate([70,210,355,510,675,855]):
        phase=((n>>(i*5))&31)/31*2*math.pi
        y=y0+35*math.sin(phase+i*.8)
        pts.append([x,round(y,1)])
    return pts


def make_actions(beat_id:str,text:str,cues:list[str],duration:float):
    actions=[]
    path=seed_points(beat_id+text)
    actions.append({'type':'path_draw','id':beat_id+'_path','start':0.0,'duration':min(2.2,duration*.28),'points':path,'style':{'width':2}})
    if 'bike_rider' in cues:
        actions.append({'type':'actor_follow_path','asset':'bike_rider','path_ref':beat_id+'_path','start':2.0,'duration':max(2.0,duration-2.8),'scale':0.9})
    elif 'couple' in cues:
        actions.append({'type':'actor_follow_path','asset':'heart','path_ref':beat_id+'_path','start':2.0,'duration':max(2.0,duration-2.8),'scale':0.75,'offset_y':-8})
    elif 'travel_cue' in cues:
        actions.append({'type':'actor_follow_path','asset':'travel_cue','path_ref':beat_id+'_path','start':2.0,'duration':max(2.0,duration-2.8),'scale':0.8,'offset_y':-18})
    drawable=[c for c in cues if c not in {'bike_rider'}]
    for j,cue in enumerate(drawable[:3]):
        st=1.9+j*1.25
        actions.append({'type':'asset_draw','asset':cue,'start':st,'duration':max(1.1,min(2.8,duration-st-.5)),
                        'x':130+j*280,'y':180+(j%2)*85,'scale':1.0})
    return actions


def plan(input_path:Path, title:str|None=None, audit=True):
    segs=ingest(input_path); groups=group_beats(segs)
    scenes=[]
    for i,g in enumerate(groups,1):
        text=' '.join(x.text for x in g)
        dur=max(5.5,g[-1].end_s-g[0].start_s)
        beat_id=f'scene_{i:02d}'
        cues=cues_for(text)
        scenes.append({
            'id':beat_id,
            'source_segment_ids':[x.id for x in g],
            'subtitle':text,
            'duration_s':round(dur,3),
            'semantic_goal':text,
            'visual_cues':cues,
            'actions':make_actions(beat_id,text,cues,dur)
        })
    return {
        'meta':{'title':title or input_path.stem,'canvas':{'width':960,'height':540},'fps':15,
                'background':'#F5EBD7','ink':'#303030','show_audit_subtitles':audit,
                'timing_source':'srt' if input_path.suffix.lower()=='.srt' else 'estimated_script'},
        'vo_segments':[asdict(x) for x in segs],
        'scenes':scenes,
    }

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('output'); ap.add_argument('--title')
    a=ap.parse_args(); obj=plan(Path(a.input),a.title)
    Path(a.output).write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
    print(a.output)
