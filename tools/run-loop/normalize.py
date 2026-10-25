"""Step 2: make the cut-out frames steady.

Keeps only Tenzin (drops bridge-rope fragments), scales every frame by a
smoothed body height so he doesn't pulse in size with each stride, and anchors
his head and torso to the same spot on a 220x300 canvas.

    python3 tools/run-loop/normalize.py --cut build/cut --out build/norm \
        --first 30 --last 66 --hold 47=46 48=49

--hold replaces a bad frame with a copy of a neighbour (47 and 48 had a blurred
rope next to his head).
"""
import argparse, os, shutil
import cv2, numpy as np
from scipy.ndimage import median_filter

ap = argparse.ArgumentParser()
ap.add_argument('--cut', default='build/cut')
ap.add_argument('--out', default='build/norm')
ap.add_argument('--first', type=int, default=30)
ap.add_argument('--last', type=int, default=66)
ap.add_argument('--hold', nargs='*', default=['47=46', '48=49'])
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)

CW, CH, BODY_H, HEAD_Y = 220, 300, 250, 22
frames = list(range(args.first, args.last + 1))
boxes = {l.split()[0]: list(map(int, l.split()[1:])) for l in open(os.path.join(args.cut, 'boxes.txt'))}

data = {}
for i in frames:
    name = f'f{i:03d}.png'
    im = cv2.imread(os.path.join(args.cut, name), cv2.IMREAD_UNCHANGED)
    a = im[:, :, 3]
    n, lab, stats, _ = cv2.connectedComponentsWithStats((a > 100).astype(np.uint8))
    biggest = 1 + np.argmax(stats[1:, 4])
    keep = cv2.dilate((lab == biggest).astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    a = np.where(keep, a, 0)
    rows = (a > 100).sum(1); top = int(np.argmax(rows > 0))
    while top < len(rows) and rows[top] < 16:      # thin strands above the head
        a[top] = 0; top += 1
    im[:, :, 3] = a
    data[i] = dict(im=im, top=top, oy=boxes[name][1])

# clip anything sticking up well above where his head is in nearby frames
tops = np.array([data[i]['top'] + data[i]['oy'] for i in frames], float)
usual = median_filter(tops, size=7, mode='nearest')
for k, i in enumerate(frames):
    d = data[i]
    if d['top'] + d['oy'] < usual[k] - 8:
        d['im'][:int(usual[k] - 6 - d['oy']), :, 3] = 0

for i in frames:
    d = data[i]; a = d['im'][:, :, 3]
    ys = np.where(a > 100)[0]; d['top'], d['bot'] = ys.min(), ys.max()
    upper = a[d['top']: d['top'] + int((d['bot'] - d['top']) * 0.55)] > 100
    d['cx'] = np.where(upper)[1].mean()

def smooth(v, k):
    return np.convolve(np.pad(v, k // 2, mode='edge'), np.ones(k) / k, mode='valid')
heights = smooth(np.array([data[i]['bot'] - data[i]['top'] for i in frames], float), 15)
centres = smooth(np.array([data[i]['cx'] for i in frames], float), 5)

for k, i in enumerate(frames):
    d = data[i]; s = BODY_H / heights[k]
    im = cv2.resize(d['im'], None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    can = np.zeros((CH, CW, 4), np.uint8)
    ox, oy = int(round(CW / 2 - centres[k] * s)), int(round(HEAD_Y - d['top'] * s))
    h, w = im.shape[:2]
    ya, yb, xa, xb = max(0, oy), min(CH, oy + h), max(0, ox), min(CW, ox + w)
    can[ya:yb, xa:xb] = im[ya - oy:yb - oy, xa - ox:xb - ox]
    cv2.imwrite(os.path.join(args.out, f'f{i:03d}.png'), can)

for pair in args.hold:
    bad, good = pair.split('=')
    shutil.copy(os.path.join(args.out, f'f{int(good):03d}.png'), os.path.join(args.out, f'f{int(bad):03d}.png'))
print(f'normalized frames {args.first}-{args.last}')
