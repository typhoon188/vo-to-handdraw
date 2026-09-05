import hashlib, json, subprocess, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'outputs'
OUT.mkdir(exist_ok=True)

def validate_spec(path: Path):
    obj = json.loads(path.read_text(encoding='utf-8'))
    assert 'meta' in obj and 'scenes' in obj
    assert isinstance(obj['scenes'], list) and len(obj['scenes']) >= 2
    for scene in obj['scenes']:
        assert 'id' in scene and 'duration_s' in scene and 'actions' in scene
        for a in scene['actions']:
            assert a['type'] in {'path_draw','asset_draw','actor_follow_path','text_write','hold'}
            if a['type'] == 'path_draw':
                assert 'id' in a and 'points' in a and len(a['points']) >= 2
            if a['type'] == 'actor_follow_path':
                assert 'path_ref' in a and 'asset' in a

specs = [BASE/'examples'/'trail_demo.json', BASE/'examples'/'love_story_demo.json', BASE/'examples'/'retirement_demo.json']
for s in specs:
    validate_spec(s)
    out = OUT / (s.stem + '.mp4')
    subprocess.run([sys.executable, str(BASE/'runtime'/'render.py'), str(s), str(out), '--clean'], check=True)
    assert out.exists() and out.stat().st_size > 20000

trail = BASE/'examples'/'trail_demo.json'
out1 = OUT/'trail_demo_a.mp4'
out2 = OUT/'trail_demo_b.mp4'
subprocess.run([sys.executable, str(BASE/'runtime'/'render.py'), str(trail), str(out1), '--clean'], check=True)
subprocess.run([sys.executable, str(BASE/'runtime'/'render.py'), str(trail), str(out2), '--clean'], check=True)
h1 = hashlib.sha256(out1.read_bytes()).hexdigest()
h2 = hashlib.sha256(out2.read_bytes()).hexdigest()
assert h1 == h2
print('PASS')
print('trail_demo_sha256', h1)
print('validated_specs', len(specs))
