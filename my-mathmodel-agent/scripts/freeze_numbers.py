#!/usr/bin/env python3
"""Freeze a JSON-compatible results file with provenance metadata."""
import argparse, hashlib, json, csv
from datetime import datetime, timezone
from pathlib import Path

def sha256(path):
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

ap=argparse.ArgumentParser(); ap.add_argument('results'); ap.add_argument('--output',default='frozen_numbers.json'); args=ap.parse_args()
src=Path(args.results); out=Path(args.output)
if src.suffix.lower()=='.json': data=json.loads(src.read_text())
elif src.suffix.lower()=='.csv':
    with src.open(newline='') as f: data=list(csv.DictReader(f))
else: raise SystemExit('results must be .json or .csv')
payload={"frozen_at":datetime.now(timezone.utc).isoformat(),"source_file":str(src.resolve()),"source_sha256":sha256(src),"values":data}
out.write_text(json.dumps(payload,ensure_ascii=False,indent=2))
print(f'Frozen {src} -> {out}')
