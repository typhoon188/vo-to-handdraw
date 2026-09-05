from pathlib import Path
import hashlib, json, subprocess, sys

BASE=Path(__file__).resolve().parents[1]
OUTPUTS=BASE/'outputs'; OUTPUTS.mkdir(exist_ok=True)
sys.path.insert(0,str(BASE))
from planner.vo_ingest import parse_srt
from planner.auto_plan import plan
from runtime.qa import validate

srt=BASE/'examples/vo/generic_trail.srt'
segs=parse_srt(srt)
assert len(segs)==4
spec=plan(srt,'trail-test',audit=False)
assert 3 <= len(spec['scenes']) <= 6
assert validate(spec,production=True)==[]
covered={r for s in spec['scenes'] for r in s['source_segment_ids']}
assert covered=={x.id for x in segs}

txt=BASE/'examples/vo/draft.txt'
draft=plan(txt,'draft',audit=False)
errs=validate(draft,production=True)
assert any('SRT' in e for e in errs), errs

bad=json.loads(json.dumps(spec))
bad['scenes'][0]['actions'][0]['mask']='bad'
errs=validate(bad,production=False)
assert any('forbidden reveal' in e for e in errs), errs

hand=BASE/'assets/feminine-hand-fineline-v1.svg'
meta=json.loads((BASE/'assets/feminine-hand-fineline-v1.json').read_text())
assert hashlib.sha256(hand.read_bytes()).hexdigest()==meta['sha256']
ax,ay=meta['tip_anchor_viewbox']; vw,vh=meta['viewbox']; assert 0<=ax<=vw and 0<=ay<=vh

asset=BASE/'examples/vo/test_asset.json'; asset.write_text(json.dumps({'paths':[[[0,0],[60,20],[120,0]],[[20,30],[100,30]]]}))
ext_spec={
 'meta':{'title':'external','canvas':{'width':480,'height':270},'fps':10,'background':'#F5EBD7','ink':'#303030','show_audit_subtitles':False,'timing_source':'srt','asset_registry':{'external_shape':'test_asset.json'}},
 'vo_segments':[{'id':'vo_001','start_s':0,'end_s':2,'text':'draw'}],
 'scenes':[{'id':'scene_01','source_segment_ids':['vo_001'],'subtitle':'draw','duration_s':2,'semantic_goal':'draw','visual_cues':['external_shape'],'actions':[{'type':'asset_draw','asset':'external_shape','start':0,'duration':1.6,'x':160,'y':100,'scale':1}]}]
}
ext_plan=BASE/'examples/vo/external_asset_plan.json'; ext_plan.write_text(json.dumps(ext_spec,indent=2))
out=BASE/'outputs/test-external-asset.mp4'
subprocess.run([sys.executable,str(BASE/'runtime/render.py'),str(ext_plan),str(out),'--clean'],check=True)
assert out.exists() and out.stat().st_size>5000

one={
 'meta':{'title':'det','canvas':{'width':480,'height':270},'fps':10,'background':'#F5EBD7','ink':'#303030','show_audit_subtitles':False,'timing_source':'srt'},
 'vo_segments':[{'id':'vo_001','start_s':0,'end_s':2,'text':'journey'}],
 'scenes':[{'id':'scene_01','source_segment_ids':['vo_001'],'subtitle':'journey','duration_s':2,'semantic_goal':'journey','visual_cues':['journey_line'],'actions':[{'type':'asset_draw','asset':'journey_line','start':0,'duration':1.7,'x':100,'y':90,'scale':1}]}]
}
p=BASE/'examples/vo/deterministic_plan.json'; p.write_text(json.dumps(one,indent=2))
a=BASE/'outputs/det-a.mp4'; b=BASE/'outputs/det-b.mp4'
for o in (a,b): subprocess.run([sys.executable,str(BASE/'runtime/render.py'),str(p),str(o),'--clean'],check=True)
ha=hashlib.sha256(a.read_bytes()).hexdigest(); hb=hashlib.sha256(b.read_bytes()).hexdigest(); assert ha==hb

audio=OUTPUTS/'verify-silent.m4a'
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','anullsrc=r=44100:cl=mono','-t','24','-c:a','aac',str(audio)],check=True)
muxed=OUTPUTS/'verify-e2e-trail.mp4'
subprocess.run([sys.executable,str(BASE/'handdraw.py'),str(srt),str(muxed),'--audio',str(audio),'--production'],check=True)
assert muxed.exists() and muxed.stat().st_size>5000
r=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type','-of','csv=p=0',str(muxed)],capture_output=True,text=True,check=True)
streams=set(x.strip() for x in r.stdout.splitlines() if x.strip())
assert {'video','audio'} <= streams, streams
print('PASS')
print('scene_count',len(spec['scenes']))
print('deterministic_sha256',ha)
print('audio_video_streams',sorted(streams))
