from __future__ import annotations
import re
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Segment:
    id: str
    start_s: float
    end_s: float
    text: str


def _ts(s: str) -> float:
    s=s.replace(',', '.')
    h,m,sec=s.split(':')
    return int(h)*3600+int(m)*60+float(sec)


def parse_srt(path: Path) -> list[Segment]:
    raw=path.read_text(encoding='utf-8-sig').replace('\r\n','\n')
    blocks=re.split(r'\n\s*\n', raw.strip())
    out=[]
    for i,b in enumerate(blocks,1):
        lines=[x.strip() for x in b.splitlines() if x.strip()]
        if not lines: continue
        if re.fullmatch(r'\d+',lines[0]): lines=lines[1:]
        if not lines or '-->' not in lines[0]: continue
        a,z=[x.strip() for x in lines[0].split('-->',1)]
        text=' '.join(lines[1:]).strip()
        if text:
            out.append(Segment(f'vo_{len(out)+1:03d}',_ts(a),_ts(z),text))
    if not out: raise ValueError(f'No valid SRT segments in {path}')
    return out


def parse_text(path: Path, words_per_second: float=2.35) -> list[Segment]:
    raw=path.read_text(encoding='utf-8-sig').strip()
    chunks=[x.strip() for x in re.split(r'(?<=[.!?。！？])\s+|\n+',raw) if x.strip()]
    if not chunks: raise ValueError(f'No text in {path}')
    out=[]; t=0.0
    for c in chunks:
        wc=max(1,len(re.findall(r"\b[\w'-]+\b",c)))
        dur=max(1.4,wc/words_per_second)
        out.append(Segment(f'vo_{len(out)+1:03d}',t,t+dur,c)); t+=dur
    return out


def ingest(path: Path) -> list[Segment]:
    ext=path.suffix.lower()
    if ext=='.srt': return parse_srt(path)
    if ext in {'.txt','.md'}: return parse_text(path)
    raise ValueError('Layer 1 accepts .txt/.md scripts or .srt timing files. Audio can be muxed separately.')

if __name__=='__main__':
    import json,sys
    segs=ingest(Path(sys.argv[1]))
    print(json.dumps([asdict(s) for s in segs],indent=2,ensure_ascii=False))
