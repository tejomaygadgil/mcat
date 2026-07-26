import re, json, sys, markdown, subprocess
import numpy as np
from weasyprint import HTML
from pdf2image import convert_from_bytes, convert_from_path

def set_font(fs):
    s=open('build_pdf.py').read()
    s=re.sub(r'\.page \{ font-size: [\d.]+pt', f'.page {{ font-size: {fs}pt', s)
    s=re.sub(r'\.page h2 \{ font-size: [\d.]+pt', f'.page h2 {{ font-size: {fs*1.22:.2f}pt', s)
    s=re.sub(r'\.page h4 \{ font-size: [\d.]+pt', f'.page h4 {{ font-size: {fs*1.04:.2f}pt', s)
    open('build_pdf.py','w').write(s)

def measure(boxes, CSS, inject):
    COLW=(8.5-0.6-0.16)/2
    hs=[]
    for b in boxes:
        body=markdown.markdown(inject(b),extensions=["tables","sane_lists","md_in_html"])
        html=(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}\n'
              f'@page{{size:{COLW}in 40in !important;margin:0 !important}}</style></head>'
              f'<body><div class="page"><div class="cols"><div class="col">{body}</div>'
              f'</div></div></body></html>')
    	# render and measure ink height
        a=np.array(convert_from_bytes(HTML(string=html,base_url=".").write_pdf(),dpi=72)[0].convert('L'))
        r=np.where((a<200).sum(axis=1)>0)[0]
        hs.append(int(r.max()-r.min()+1) if len(r) else 0)
    return hs

def partition(hs,k):
    n=len(hs); INF=float('inf'); pre=[0]
    for h in hs: pre.append(pre[-1]+h)
    dp=[[INF]*(k+1) for _ in range(n+1)]; cut=[[0]*(k+1) for _ in range(n+1)]
    dp[0][0]=0
    for i in range(1,n+1):
        for j in range(1,k+1):
            for m in range(j-1,i):
                v=max(dp[m][j-1],pre[i]-pre[m])
                if v<dp[i][j]: dp[i][j]=v; cut[i][j]=m
    g=[]; i,j=n,k
    while j>0: m=cut[i][j]; g.append((m,i)); i,j=m,j-1
    return dp[n][k], g[::-1]
