import subprocess, os, sys, glob
import importlib
def pages(kind):
    subprocess.run(['rm','-rf','dchk'],check=False)
    os.makedirs('dchk',exist_ok=True)
    subprocess.run(['soffice','--headless','--convert-to','pdf','--outdir','dchk',
                    f'DaybreakBrief_{kind}_20260905.docx'],capture_output=True)
    out=subprocess.run(['pdfinfo',f'dchk/DaybreakBrief_{kind}_20260905.pdf'],capture_output=True,text=True).stdout
    for line in out.splitlines():
        if line.startswith('Pages:'): return int(line.split()[1])
    return 999
def build(kind,scale):
    r=subprocess.run(['python3','mkdocx.py',kind,str(round(scale,4))],capture_output=True,text=True)
    return r.stdout.strip()
for kind,target in [('DBS',1),('FULL',6)]:
    lo,hi=0.60,1.30
    best=None
    for i in range(9):
        mid=(lo+hi)/2
        info=build(kind,mid); pg=pages(kind)
        print(f'{kind} scale={mid:.4f} pages={pg}  {info}')
        if pg<=target:
            best=mid; lo=mid   # can afford bigger type
        else:
            hi=mid
        if hi-lo<0.004: break
    if best is None:
        print(f'!! {kind} never reached {target}pp'); sys.exit(1)
    print(build(kind,best), '-> pages', pages(kind))
