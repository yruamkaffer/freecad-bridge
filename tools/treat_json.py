# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Apply the extension's mesh treatment to a JSON without FreeCAD or extra packages."""
from pathlib import Path
import argparse,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'yk_step_bridge'))
from conversion import run_json

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--mode',choices=['strict','visualization','solids_only'],default='strict')
    parser.add_argument('--treatment',choices=['complete','conservative','none'],default='complete')
    args=parser.parse_args()
    if args.source.resolve()==args.output.resolve():parser.error('Choose a different output path to preserve the source.')
    result=run_json(dict(source=str(args.source),policy=args.mode,mesh_treatment=args.treatment))
    args.output.write_text(json.dumps(result,ensure_ascii=False,allow_nan=False,separators=(',',':')),encoding='utf-8')
    print(f"{len(result['parts'])} parts; {len(result['skipped_parts'])} omitted; output: {args.output}")
    for p in result['parts']:
        print(f"{p['name']}: closed={p['mesh_closed']}; repairs={len(p.get('repairs',[]))}")
if __name__=='__main__':main()
