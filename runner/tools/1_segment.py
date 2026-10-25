# Step 1: cut Tenzin out of each video frame with the u2net_human_seg model.
# Usage: python3 1_segment.py u2net_human_seg.onnx frames/ cut/
import onnxruntime as ort, numpy as np, cv2, sys, glob, os
model = sys.argv[1]; src = sys.argv[2]; out = sys.argv[3]; os.makedirs(out, exist_ok=True)
sess = ort.InferenceSession(model, providers=['CPUExecutionProvider'])
inp = sess.get_inputs()[0]; S = inp.shape[2] if isinstance(inp.shape[2], int) else 320
isnet = 'isnet' in model
mean = np.array([0.485,0.456,0.406]) if not isnet else np.array([0.5,0.5,0.5])
std = np.array([0.229,0.224,0.225]) if not isnet else np.array([1.0,1.0,1.0])
def run(img):
    h,w = img.shape[:2]
    x = cv2.resize(img, (S,S), interpolation=cv2.INTER_LANCZOS4)[:,:,::-1].astype(np.float32)/255.
    x = (x/ max(x.max(),1e-6) - mean)/std
    x = x.transpose(2,0,1)[None].astype(np.float32)
    m = sess.run(None, {inp.name: x})[0][0,0]
    m = (m - m.min())/(m.max()-m.min()+1e-8)
    return cv2.resize(m, (w,h), interpolation=cv2.INTER_LINEAR)
for f in sorted(glob.glob(src+'/*.jpg')):
    img = cv2.imread(f); H,W = img.shape[:2]
    # pass 1: center crop where the runner is
    x0,x1,y0,y1 = int(W*0.3), int(W*0.7), int(H*0.15), H
    crop = img[y0:y1, x0:x1]
    m = run(crop)
    ys,xs = np.where(m>0.5)
    if len(xs)==0: continue
    bx0,bx1,by0,by1 = xs.min(),xs.max(),ys.min(),ys.max()
    pad = 30
    cx0,cx1 = max(0,bx0-pad), min(crop.shape[1],bx1+pad); cy0,cy1 = max(0,by0-pad), min(crop.shape[0],by1+pad)
    c2 = crop[cy0:cy1, cx0:cx1]; m2 = run(c2)
    rgba = np.dstack([c2, (np.clip(m2,0,1)*255).astype(np.uint8)])
    name = os.path.basename(f).replace('.jpg','.png')
    cv2.imwrite(os.path.join(out,name), rgba)
    with open(os.path.join(out,'boxes.txt'),'a') as bf: bf.write(f"{name} {x0+cx0} {y0+cy0} {cx1-cx0} {cy1-cy0}\n")
