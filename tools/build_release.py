# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Build a reproducible unsigned RBZ using only Python stdlib."""
from pathlib import Path
import ast,hashlib,re,zipfile
ROOT=Path(__file__).resolve().parents[1]
loader=ROOT/'yk_step_bridge.rb'
match=re.search(r"extension.version\s*=\s*'([0-9]+\.[0-9]+\.[0-9]+)'",loader.read_text(encoding='utf-8'))
if not match:raise SystemExit('Version not found')
paths=[loader]+[ROOT/'yk_step_bridge'/n for n in ('main.rb','convert.py','mesh_tools.py','metadata.py','LICENSE.txt','NOTICE.txt')]
for p in paths:
 if not p.is_file():raise SystemExit(f'Missing: {p.name}')
 if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
for name in ('LICENSE.txt','NOTICE.txt'):
 if (ROOT/name).read_bytes()!=(ROOT/'yk_step_bridge'/name).read_bytes():raise SystemExit(f'Copies differ: {name}')
output=ROOT/'dist';output.mkdir(exist_ok=True)
rbz=output/f'FreeCAD_Bridge_{match.group(1)}.rbz'
with zipfile.ZipFile(rbz,'w',compression=zipfile.ZIP_DEFLATED) as archive:
 for path in sorted(paths):
  info=zipfile.ZipInfo(path.relative_to(ROOT).as_posix(),(2026,1,1,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
  archive.writestr(info,path.read_bytes())
digest=hashlib.sha256(rbz.read_bytes()).hexdigest()
(output/'SHA256.txt').write_text(f'{digest}  {rbz.name}\n',encoding='utf-8')
print(f'Created {rbz.name} ({rbz.stat().st_size} bytes)')
print('Unsigned. This script does not test integration in the host applications.')
