# Step 3: pack the 29-frame loop (frames 34-62) into an 8x4 sprite sheet.
import cv2, numpy as np
fr = [cv2.imread(f'norm2/f{i:03d}.png', cv2.IMREAD_UNCHANGED) for i in range(34, 63)]
# light temporal smoothing of horizontal anchor: already centred. Build sheet 8 cols
cols = 8; rows = (len(fr)+cols-1)//cols; h, w = fr[0].shape[:2]
sheet = np.zeros((rows*h, cols*w, 4), np.uint8)
for k, f in enumerate(fr): sheet[(k//cols)*h:(k//cols+1)*h, (k%cols)*w:(k%cols+1)*w] = f
cv2.imwrite('run_sheet.png', sheet, [cv2.IMWRITE_PNG_COMPRESSION, 9])
# preview frames on a backdrop (2 loops)
import os; os.makedirs('prev', exist_ok=True)
for t in range(len(fr)*2):
    bg = np.full((h, w, 3), (200, 170, 140), np.uint8); f = fr[t % len(fr)]; a = f[:,:,3:]/255.
    out = (f[:,:,:3]*a + bg*(1-a)).astype(np.uint8); cv2.imwrite(f'prev/p{t:03d}.png', out)
print(len(fr), sheet.shape)
