"""Step 3: pack one stride into a sprite sheet.

Frames 34-62 are one full stride; frame 63 matches 34, so they loop without a
seam. They're packed 8 across, 4 down (29 frames used).

    python3 tools/run-loop/build_sheet.py --norm build/norm --out build/run_sheet.webp
"""
import argparse, os
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('--norm', default='build/norm')
ap.add_argument('--first', type=int, default=34)
ap.add_argument('--last', type=int, default=62)
ap.add_argument('--out', default='build/run_sheet.webp')
args = ap.parse_args()

frames = [Image.open(os.path.join(args.norm, f'f{i:03d}.png')).convert('RGBA') for i in range(args.first, args.last + 1)]
w, h = frames[0].size; cols = 8; rows = -(-len(frames) // cols)
sheet = Image.new('RGBA', (cols * w, rows * h), (0, 0, 0, 0))
for k, f in enumerate(frames):
    sheet.paste(f, ((k % cols) * w, (k // cols) * h))
os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
sheet.save(args.out, 'WEBP', quality=88, method=6)
print(f'{len(frames)} frames -> {args.out} ({os.path.getsize(args.out) // 1024} KB)')
