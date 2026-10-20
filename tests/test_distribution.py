# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Offline distribution checks. No SketchUp UI simulation."""
from pathlib import Path
import importlib.util,json,math,re,struct,unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build_release',ROOT/'tools/build_release.py')
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)

class DistributionTests(unittest.TestCase):
    def test_installer_matches_sources(self):
        build.validate(ROOT/'dist'/f'FreeCAD_Bridge_{build.version()}.rbz',build.sources())

    def test_png_dimensions_and_svg_sources(self):
        for name in ('step','json','settings','diagnostics','about'):
            for size in (24,32):
                data=(ROOT/f'yk_step_bridge/icons/{name}_{size}.png').read_bytes()
                self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n')
                self.assertEqual(struct.unpack('>II',data[16:24]),(size,size))
            self.assertIn('<svg',(ROOT/f'yk_step_bridge/icons/{name}.svg').read_text())

    def test_internal_documentation_links(self):
        for p in ROOT.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
                if '://' in target or target.startswith('#'):continue
                self.assertTrue((p.parent/target.split('#')[0]).exists(),f'{p.name}: {target}')

    def test_synthetic_example_closed_positive_volume(self):
        import sys
        sys.path.insert(0,str(ROOT/'yk_step_bridge'))
        from mesh_tools import prepare
        data=json.loads((ROOT/'examples/tetraedro_vermelho.json').read_text())
        self.assertEqual(data['format'],'yk-step-bridge-1')
        p=data['parts'][0];vertices,triangles,check=prepare(p['vertices'],p['triangles'])
        self.assertTrue(check['closed'])
        volume=0.0
        for t in triangles:
            a,b,c=[vertices[i] for i in t]
            volume+=sum(a[k]*(b[(k+1)%3]*c[(k+2)%3]-b[(k+2)%3]*c[(k+1)%3]) for k in range(3))/6
        self.assertTrue(math.isclose(volume,1000/6))

if __name__=='__main__':unittest.main()
