"""Step 1: cut Tenzin out of each video frame.

Runs the u2net_human_seg person-segmentation model on every frame and saves a
transparent PNG crop of the runner, plus where that crop sat in the frame.

    python3 tools/run-loop/segment.py --model u2net_human_seg.onnx \
        --frames build/frames --out build/cut
"""
import argparse, glob, os
import cv2, numpy as np, onnxruntime as ort

ap = argparse.ArgumentParser()
ap.add_argument('--model', required=True)
ap.add_argument('--frames', default='build/frames')
ap.add_argument('--out', default='build/cut')
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)

sess = ort.InferenceSession(args.model, providers=['CPUExecutionProvider'])
inp = sess.get_inputs()[0]
SIZE = 320
MEAN, STD = np.array([0.485, 0.456, 0.406]), np.array([0.229, 0.224, 0.225])

def mask(img):
    h, w = img.shape[:2]
    x = cv2.resize(img, (SIZE, SIZE), interpolation=cv2.INTER_LANCZOS4)[:, :, ::-1].astype(np.float32) / 255
    x = ((x / max(x.max(), 1e-6) - MEAN) / STD).transpose(2, 0, 1)[None].astype(np.float32)
    m = sess.run(None, {inp.name: x})[0][0, 0]
    m = (m - m.min()) / (m.max() - m.min() + 1e-8)
    return cv2.resize(m, (w, h))

with open(os.path.join(args.out, 'boxes.txt'), 'w') as boxes:
    for f in sorted(glob.glob(os.path.join(args.frames, '*.jpg'))):
        img = cv2.imread(f); H, W = img.shape[:2]
        # pass 1: the centre of the frame, where the runner is
        x0, y0 = int(W * 0.3), int(H * 0.15)
        crop = img[y0:H, x0:int(W * 0.7)]
        ys, xs = np.where(mask(crop) > 0.5)
        if not len(xs):
            continue
        # pass 2: a tight crop around him, for a sharper mask
        pad = 30
        cx0, cy0 = max(0, xs.min() - pad), max(0, ys.min() - pad)
        cx1, cy1 = min(crop.shape[1], xs.max() + pad), min(crop.shape[0], ys.max() + pad)
        tight = crop[cy0:cy1, cx0:cx1]
        rgba = np.dstack([tight, (np.clip(mask(tight), 0, 1) * 255).astype(np.uint8)])
        name = os.path.basename(f).replace('.jpg', '.png')
        cv2.imwrite(os.path.join(args.out, name), rgba)
        boxes.write(f'{name} {x0 + cx0} {y0 + cy0} {cx1 - cx0} {cy1 - cy0}\n')
        print(name)
