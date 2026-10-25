# How Tenzin's run loop was made

The endless-runner test uses a looped cut-out of Tenzin from Arkizen Studio's morning-run animation (`source-animations/morning-gong.mp4`), during the rope-bridge shot where he runs straight away from the camera.

1. **Extract frames** (about 9.4s to 11.8s, 72 frames at 30fps):
   `ffmpeg -ss 9.4 -i source-animations/morning-gong.mp4 -t 2.4 -q:v 2 frames/f%03d.jpg`
2. **Cut out Tenzin** with the `u2net_human_seg.onnx` model from https://github.com/danielgatis/rembg/releases (needs `onnxruntime`, `opencv-python`, `numpy`):
   `python3 1_segment.py u2net_human_seg.onnx frames cut`
3. **Normalize**: `python3 2_normalize.py`. It scales frames by a smoothed body height, so he doesn't pulse in size with each stride, anchors his head and torso, and trims bridge-rope strands.
   Frames 47 and 48 still showed a blurred rope next to his head, so they were replaced by copies of 46 and 49.
4. **Build the sheet**: `python3 3_build_sheet.py`. It packs frames 34–62 (one full stride, which loops seamlessly) into `run_sheet.png`, which was then converted to `assets/run_sheet.webp`.

`index.html` has the sheet embedded as a data URI, so the game also works when opened straight from disk.
