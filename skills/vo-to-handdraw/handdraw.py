from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from planner.auto_plan import plan
from runtime.qa import validate
from runtime.render import render


def ffprobe_duration(path:Path)->float:
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(path)],capture_output=True,text=True,check=True)
    return float(r.stdout.strip())


def mux_audio(video:Path,audio:Path,out:Path):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(video),'-i',str(audio),'-c:v','copy','-c:a','aac','-b:a','160k','-shortest',str(out)],check=True)


def main():
    ap=argparse.ArgumentParser(description='VO-to-Handdraw Layer 1 pipeline')
    ap.add_argument('input',help='.txt/.md script or .srt timing file')
    ap.add_argument('output',help='final .mp4')
    ap.add_argument('--audio',help='optional voice-over audio to mux')
    ap.add_argument('--plan',help='optional prebuilt Layer-1 scene spec; skips fallback planning')
    ap.add_argument('--plan-out',help='write normalized scene plan')
    ap.add_argument('--qa-out',help='write QA JSON report')
    ap.add_argument('--title')
    ap.add_argument('--audit',action='store_true')
    ap.add_argument('--production',action='store_true',help='requires SRT timing and strict QA')
    a=ap.parse_args()

    inp=Path(a.input).resolve(); out=Path(a.output).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    if a.plan:
        spec_path=Path(a.plan).resolve(); spec=json.loads(spec_path.read_text(encoding='utf-8'))
    else:
        spec=plan(inp,a.title,audit=a.audit)
        spec_path=out.with_suffix('.plan.json')
        spec_path.write_text(json.dumps(spec,indent=2,ensure_ascii=False),encoding='utf-8')
    if a.plan_out:
        po=Path(a.plan_out).resolve(); po.parent.mkdir(parents=True,exist_ok=True); po.write_text(json.dumps(spec,indent=2,ensure_ascii=False),encoding='utf-8')

    errors=validate(spec,production=a.production)
    report={'status':'PASS' if not errors else 'FAIL','production':a.production,'errors':errors,'timing_source':spec.get('meta',{}).get('timing_source'),'scene_count':len(spec.get('scenes',[]))}
    if a.audio:
        audio=Path(a.audio).resolve(); report['audio_duration_s']=round(ffprobe_duration(audio),3)
        video_expected=sum(float(s['duration_s']) for s in spec.get('scenes',[]))
        report['planned_video_duration_s']=round(video_expected,3)
        report['audio_plan_delta_s']=round(abs(report['audio_duration_s']-video_expected),3)
        if a.production and report['audio_plan_delta_s']>1.5:
            errors.append(f'audio/plan duration mismatch >1.5s ({report["audio_plan_delta_s"]}s)')
            report['status']='FAIL'; report['errors']=errors
    qpath=Path(a.qa_out).resolve() if a.qa_out else out.with_suffix('.qa.json')
    qpath.write_text(json.dumps(report,indent=2),encoding='utf-8')
    if errors:
        print('FAIL'); [print('-',e) for e in errors]; raise SystemExit(1)

    temp=out.with_name(out.stem+'.video-only.mp4') if a.audio else out
    normalized=out.with_suffix('.normalized-plan.json')
    normalized.write_text(json.dumps(spec,indent=2,ensure_ascii=False),encoding='utf-8')
    render(normalized,temp,audit_override=a.audit)
    if a.audio:
        mux_audio(temp,Path(a.audio).resolve(),out); temp.unlink(missing_ok=True)
    print(out)
    print(qpath)

if __name__=='__main__': main()
