from __future__ import annotations
import json
from pathlib import Path

ALLOWED={'path_draw','asset_draw','actor_follow_path','text_write','hold'}
FORBIDDEN_KEYS={'mask','wipe','clip_path','clip-path','opacity_reveal','hidden_image','matte'}


def validate(spec:dict, production=False)->list[str]:
    errors=[]
    if 'meta' not in spec or 'scenes' not in spec: return ['missing meta/scenes']
    if not spec.get('scenes'): errors.append('no scenes')
    timing=spec.get('meta',{}).get('timing_source')
    if production and timing!='srt': errors.append('production requires SRT-verified timing_source')
    vo_ids={v.get('id') for v in spec.get('vo_segments',[]) if v.get('id')}
    covered=set()
    for si,scene in enumerate(spec.get('scenes',[])):
        sid=scene.get('id',f'#{si}')
        dur=float(scene.get('duration_s',0) or 0)
        if dur<=0: errors.append(f'{sid}: duration_s must be > 0')
        refs=set(scene.get('source_segment_ids',[])); covered|=refs
        if spec.get('vo_segments') and not refs: errors.append(f'{sid}: no source_segment_ids')
        path_ids={a.get('id') for a in scene.get('actions',[]) if a.get('type')=='path_draw'}
        for ai,a in enumerate(scene.get('actions',[])):
            typ=a.get('type'); label=f'{sid}.action[{ai}]'
            if typ not in ALLOWED: errors.append(f'{label}: unsupported type {typ}')
            for k in a:
                if str(k).lower() in FORBIDDEN_KEYS: errors.append(f'{label}: forbidden reveal key {k}')
            st=float(a.get('start',0) or 0); ad=float(a.get('duration',0) or 0)
            if st<0 or ad<0 or st+ad>dur+0.05: errors.append(f'{label}: timing outside scene')
            if typ=='path_draw' and (not a.get('id') or len(a.get('points',[]))<2): errors.append(f'{label}: invalid path')
            if typ=='actor_follow_path' and a.get('path_ref') not in path_ids: errors.append(f'{label}: missing path_ref')
    if vo_ids and covered!=vo_ids:
        missing=sorted(vo_ids-covered); extra=sorted(covered-vo_ids)
        if missing: errors.append('VO coverage missing: '+','.join(missing))
        if extra: errors.append('unknown VO refs: '+','.join(extra))
    return errors


def validate_file(path:Path,production=False):
    spec=json.loads(path.read_text(encoding='utf-8'))
    return validate(spec,production)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--production',action='store_true')
    a=ap.parse_args(); errs=validate_file(Path(a.spec),a.production)
    if errs:
        print('FAIL'); [print('-',e) for e in errs]; raise SystemExit(1)
    print('PASS')
