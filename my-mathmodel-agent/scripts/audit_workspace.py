#!/usr/bin/env python3
"""Audit required artifacts and emit a human-readable final report."""
import argparse, json
from pathlib import Path

REQUIRED=['problem_files','planning','methods','code','data_cleaned','results','figures','paper','audit','state.json','project_manifest.json']
ap=argparse.ArgumentParser(); ap.add_argument('project',nargs='?',default='.'); args=ap.parse_args(); root=Path(args.project)
missing=[x for x in REQUIRED if not (root/x).exists()]
issues=[]
if not (root/'frozen_numbers.json').exists(): issues.append('缺少 frozen_numbers.json：结果尚未冻结')
if (root/'state.json').exists():
    try:
        state=json.loads((root/'state.json').read_text())
        if state.get('stage')=='READY' and missing: issues.append('状态为 READY，但仍缺少必需文件')
    except Exception as e: issues.append(f'state.json 无法解析：{e}')
status='PASS' if not missing and not issues else 'FAIL'
lines=[f'# Final Audit: {status}','',f'项目：{root.resolve()}','',f'缺失文件：{len(missing)}']
lines += [f'- {x}' for x in missing] or ['- 无']
lines += ['',f'问题：{len(issues)}']+[f'- {x}' for x in issues] or ['- 无']
lines += ['', '审计结论：只有在证据、冻结结果和格式检查均完成后，才能将 state.json 更新为 READY。']
(root/'audit').mkdir(exist_ok=True); (root/'audit'/'final_report.md').write_text('\n'.join(lines))
print('\n'.join(lines)); raise SystemExit(0 if status=='PASS' else 1)
