#!/usr/bin/env python3
"""mkweb.py — convert a print-built brief into the web version published to the team link.

    python3 mkweb.py DaybreakBrief_DBS_YYYYMMDD.html  ->  brief_web_YYYYMMDD.html

Then publish with the Artifact tool, passing the STORED URL from config/artifact.json.
Publishing WITHOUT that url creates a NEW artifact every day and the team's bookmark goes stale.
"""
import sys, os, json, re

SCREEN_EXTRA = """
  /* ---- screen presentation (the print block above is untouched) ---- */
  @media screen{
    body{background:#3c3a33;padding:0;margin:0;}
    #fit{display:block;overflow-x:hidden;}
    .page{box-shadow:0 3px 22px rgba(0,0,0,.38);margin:18px auto;}
    .viewnote{max-width:8.5in;margin:0 auto 2px;padding:9px 4px 0;color:#d8d2c0;
      font-family:"Source Sans 3",system-ui,sans-serif;font-size:12.5px;letter-spacing:.02em;}
    .viewnote b{color:#e8c96a;}
  }
  @media print{ .viewnote{display:none!important;} }
"""

FIT_OPEN = ('<div class="viewnote"><b>Daybreak Brief — one-page summary.</b> '
            'Internal; not for guest distribution. Printing gives exactly one page.</div>\n'
            '<div id="fit">\n')

SCALE_JS = """
<script>
/* scale the fixed 8.5in sheet to fit narrow screens so it is readable on a phone */
(function(){
  var pg=document.querySelector('.page'), fit=document.getElementById('fit');
  function go(){
    if(window.matchMedia('print').matches) return;
    var avail=document.documentElement.clientWidth, sheet=8.5*96;
    if(avail < sheet+24){
      var s=(avail-16)/sheet;
      pg.style.transformOrigin='top center';
      pg.style.transform='scale('+s+')';
      fit.style.height=(pg.offsetHeight*s+36)+'px';
    } else { pg.style.transform=''; fit.style.height=''; }
  }
  go(); window.addEventListener('resize',go);
})();
</script>
"""

def convert(src_path):
    s = open(src_path, encoding='utf-8').read()
    head = s[s.index('<title>'):s.index('</head>')]
    body = s[s.index('<body>') + len('<body>'):s.rindex('</body>')].strip()

    # TITLE MUST BE STABLE across daily republishes — no date, no edition number,
    # or the team sees what looks like a different page every morning.
    head = re.sub(r'<title>.*?</title>', '<title>Daybreak Brief</title>', head, flags=re.S)
    head = head.replace('</style>', SCREEN_EXTRA + '</style>')

    out = head + '\n' + FIT_OPEN + body + '\n</div>\n' + SCALE_JS

    for bad in ('<!DOCTYPE', '<html', '<body', '</html>'):
        assert bad not in out, f'document skeleton survived conversion: {bad}'
    assert out.count('<div') == out.count('</div>'), 'unbalanced divs'
    return out

if __name__ == '__main__':
    src = sys.argv[1]
    m = re.search(r'(\d{8})', os.path.basename(src))
    dst = f'brief_web_{m.group(1)}.html' if m else 'brief_web.html'
    open(dst, 'w', encoding='utf-8').write(convert(src))
    print('wrote', dst)
    cfg = os.path.join(os.path.dirname(src) or '.', 'config', 'artifact.json')
    if os.path.exists(cfg):
        print('republish to:', json.load(open(cfg)).get('artifact_url', '(missing artifact_url)'))
    else:
        print('WARNING: config/artifact.json not found — do NOT publish without the stored URL')
