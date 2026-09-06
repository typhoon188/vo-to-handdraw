from pathlib import Path
import json, subprocess, sys
import cv2, numpy as np

BASE=Path(__file__).resolve().parents[1]
TMP=BASE/'outputs'/'hand-override-test'
TMP.mkdir(parents=True,exist_ok=True)

# Build a tiny deterministic RGBA fixture. Product layers may supply a real approved PNG/WebP.
img=np.zeros((80,120,4),np.uint8)
cv2.line(img,(8,65),(82,16),(20,20,20,255),5,cv2.LINE_AA)
cv2.circle(img,(90,28),18,(230,230,230,255),-1,cv2.LINE_AA)
hand=TMP/'approved-hand.png'
cv2.imwrite(str(hand),img)
(hand.with_suffix('.json')).write_text(json.dumps({
    'asset_id':'test-approved-hand',
    'native_size':[120,80],
    'tip_anchor_px':[8,65],
    'status':'test-fixture'
},indent=2))

spec={
  'meta':{
    'title':'hand-override',
    'canvas':{'width':480,'height':270},
    'fps':10,
    'background':'#F4F7F8',
    'ink':'#25343C',
    'show_audit_subtitles':False,
    'timing_source':'srt',
    'hand_asset':'outputs/hand-override-test/approved-hand.png',
    'hand_width':120
  },
  'vo_segments':[{'id':'vo_001','start_s':0,'end_s':2,'text':'draw'}],
  'scenes':[{
    'id':'scene_01',
    'source_segment_ids':['vo_001'],
    'subtitle':'draw',
    'duration_s':2,
    'semantic_goal':'draw',
    'visual_cues':[],
    'actions':[{
      'type':'path_draw','id':'p','start':0,'duration':1.5,
      'points':[[80,180],[180,130],[300,160],[400,100]],
      'style':{'width':3}
    }]
  }]
}
plan=BASE/'hand-override-test-plan.json'
plan.write_text(json.dumps(spec,indent=2))
out=TMP/'hand-override.mp4'
subprocess.run([sys.executable,str(BASE/'runtime/render.py'),str(plan),str(out),'--clean'],check=True)
assert out.exists() and out.stat().st_size>3000
print('PASS')
print(out)
