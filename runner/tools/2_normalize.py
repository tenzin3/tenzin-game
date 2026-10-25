# Step 2: crop, scale to a steady size, anchor head and torso, trim rope strands.
# Reads cut/ (from step 1), writes norm2/. Frames 30-66 of the rope-bridge shot.
import cv2, numpy as np, os
src='cut_u2'; out='norm2'; os.makedirs(out, exist_ok=True)
CW, CH = 220, 300
R = list(range(30, 67))
data = {}
for i in R:
    im = cv2.imread(f'{src}/f{i:03d}.png', cv2.IMREAD_UNCHANGED); a = im[:,:,3]
    n, lab, st, _ = cv2.connectedComponentsWithStats((a>100).astype(np.uint8))
    k = 1 + np.argmax(st[1:,4]); keep = cv2.dilate((lab==k).astype(np.uint8), np.ones((7,7),np.uint8))>0
    a = np.where(keep, a, 0)
    # trim thin stuff above the head (rope strands)
    rows = (a>100).sum(1); top = np.argmax(rows>0)
    while top < len(rows) and rows[top] < 16: a[top,:] = 0; top += 1
    im[:,:,3] = a
    ys, xs = np.where(a>100)
    up = a[top: top + int((ys.max()-top)*0.55)] > 100
    cx = np.where(up)[1].mean()
    data[i] = dict(im=im, top=top, bot=ys.max(), h=ys.max()-top, cx=cx)
boxes = {l.split()[0]: list(map(int, l.split()[1:])) for l in open(src+'/boxes.txt')}
for i in R: data[i]['oy'] = boxes[f'f{i:03d}.png'][1]
tops = np.array([data[i]['top'] + data[i]['oy'] for i in R], float)
from scipy.ndimage import median_filter
mt = median_filter(tops, size=7, mode='nearest')
for n,i in enumerate(R):
    d = data[i]
    if d['top'] + d['oy'] < mt[n] - 8:
        cut = int(mt[n] - 6 - d['oy']); d['im'][:cut,:,3] = 0; d['top'] = cut
        ys = np.where(d['im'][:,:,3]>100)[0]; d['top'] = ys.min(); d['h'] = d['bot'] - d['top']
        print('clipped', i)
hs = np.array([data[i]['h'] for i in R], float)
# smooth height with wide window (removes stride pulsing, keeps camera zoom trend)
k = 15; pad = np.pad(hs, k//2, mode='edge'); sm = np.convolve(pad, np.ones(k)/k, mode='valid')
cxs = np.array([data[i]['cx'] for i in R]); pad = np.pad(cxs, 2, mode='edge'); cxsm = np.convolve(pad, np.ones(5)/5, 'valid')
TH = 250
for n,i in enumerate(R):
    d = data[i]; s = TH / sm[n]
    im = cv2.resize(d['im'], None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    can = np.zeros((CH, CW, 4), np.uint8)
    ox = int(round(CW/2 - cxsm[n]*s)); oy = int(round(22 - d['top']*s))   # anchor head-top at y=22
    h, w = im.shape[:2]
    ya, yb = max(0,oy), min(CH, oy+h); xa, xb = max(0,ox), min(CW, ox+w)
    can[ya:yb, xa:xb] = im[ya-oy:yb-oy, xa-ox:xb-ox]
    cv2.imwrite(f'{out}/f{i:03d}.png', can)

