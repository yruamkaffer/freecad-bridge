# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""FreeCADCmd entry point. No external Python dependencies are required."""
import os,sys,json,traceback
import FreeCAD as App
import Part,MeshPart
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from conversion import run

output=None
try:
    config=json.load(open(os.environ['YK_STEP_JOB'],encoding='utf-8'));output=config['output']
    data=run(config,App,Part,MeshPart)
    with open(output+'.tmp','w',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,allow_nan=False)
    os.replace(output+'.tmp',output)
except Exception:
    if output:
        with open(output+'.error','w',encoding='utf-8') as f:f.write(traceback.format_exc())
    else:traceback.print_exc()
os._exit(0 if output and os.path.isfile(output) else 1)
