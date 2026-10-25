"""Step 4: put the sprite sheet inside the game page.

The sheet is stored in index.html as a data URI (in the
<script id="sheetData"> tag) so the game also works when opened straight from
disk, where browsers block WebGL from loading image files.

    python3 tools/run-loop/embed.py --sheet build/run_sheet.webp --html index.html
"""
import argparse, base64, re

ap = argparse.ArgumentParser()
ap.add_argument('--sheet', default='build/run_sheet.webp')
ap.add_argument('--html', default='index.html')
args = ap.parse_args()

uri = 'data:image/webp;base64,' + base64.b64encode(open(args.sheet, 'rb').read()).decode()
html = open(args.html).read()
html, n = re.subn(r'(<script type="text/plain" id="sheetData">)[^<]*(</script>)', lambda m: m.group(1) + uri + m.group(2), html)
if n != 1:
    raise SystemExit('sheetData tag not found in ' + args.html)
open(args.html, 'w').write(html)
print(f'embedded {args.sheet} into {args.html}')
