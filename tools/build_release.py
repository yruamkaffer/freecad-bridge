# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Build/check an unsigned RBZ, including the toolbar resources. Python stdlib only."""
from pathlib import Path
import argparse,ast,hashlib,re,zipfile
ROOT=Path(__file__).resolve().parents[1]

def version():
    match=re.search(r"extension.version\s*=\s*'([0-9]+\.[0-9]+\.[0-9]+)'",(ROOT/'yk_step_bridge.rb').read_text(encoding='utf-8'))
    if not match:raise ValueError('Version not found in loader')
    return match.group(1)

def sources():
    paths=[ROOT/'yk_step_bridge.rb']+[ROOT/'yk_step_bridge'/n for n in ('main.rb','convert.py','mesh_tools.py','metadata.py','cad_tools.py','conversion.py','LICENSE.txt','NOTICE.txt','AJUDA.txt')]
    for name in ('step','json','settings','diagnostics','about'):
        paths += [ROOT/'yk_step_bridge/icons'/f'{name}{suffix}' for suffix in ('.svg','_24.png','_32.png')]
    for p in paths:
        if not p.is_file():raise ValueError(f'Missing required file: {p.relative_to(ROOT)}')
        if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    for name in ('LICENSE.txt','NOTICE.txt'):
        if (ROOT/name).read_bytes()!=(ROOT/'yk_step_bridge'/name).read_bytes():raise ValueError(f'Copies differ: {name}')
    return sorted(paths)

def validate(rbz,paths):
    with zipfile.ZipFile(rbz) as archive:
        expected={p.relative_to(ROOT).as_posix():p for p in paths}
        if len(archive.namelist())!=len(expected) or set(archive.namelist())!=set(expected):raise ValueError('Package file set differs from sources')
        if archive.testzip() is not None:raise ValueError('ZIP integrity check failed')
        for name,p in expected.items():
            if archive.read(name)!=p.read_bytes():raise ValueError(f'Package source mismatch: {name}')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Validate existing installer and SHA256 without rebuilding')
    args=parser.parse_args()
    paths=sources();output=ROOT/'dist';output.mkdir(exist_ok=True)
    rbz=output/f'FreeCAD_Bridge_{version()}.rbz'
    if not args.check:
        with zipfile.ZipFile(rbz,'w',compression=zipfile.ZIP_DEFLATED) as archive:
            for path in paths:
                info=zipfile.ZipInfo(path.relative_to(ROOT).as_posix(),(2026,1,1,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                archive.writestr(info,path.read_bytes())
        (output/'SHA256.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in sorted(output.glob('*.rbz'))),encoding='utf-8')
    validate(rbz,paths)
    expected=f'{hashlib.sha256(rbz.read_bytes()).hexdigest()}  {rbz.name}'
    if expected not in (output/'SHA256.txt').read_text().splitlines():raise ValueError('SHA256 mismatch or missing current installer')
    print(f'Validated {rbz.name}: {len(paths)} files; SHA256 OK')
    print('Unsigned. This command does not test Ruby syntax or integration in host applications.')

if __name__=='__main__':main()
