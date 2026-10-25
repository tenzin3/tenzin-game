# Run-loop tools

These scripts turn a shot from Arkizen Studio's morning-run animation into the looping sprite sheet that Tenzin Run uses. The shot is the rope bridge, where Tenzin runs straight away from the camera.

Run them from the repository root. Intermediate files go in `build/`, which git ignores.

You need Python 3 with `opencv-python`, `numpy`, `scipy`, `pillow` and `onnxruntime`, the `u2net_human_seg.onnx` model from https://github.com/danielgatis/rembg/releases, and `ffmpeg`.

```bash
# 0. Pull 2.4 seconds of frames from the rope-bridge shot
mkdir -p build/frames
ffmpeg -ss 9.4 -i source-animations/morning-gong.mp4 -t 2.4 -q:v 2 build/frames/f%03d.jpg

# 1. Cut Tenzin out of every frame
python3 tools/run-loop/segment.py --model u2net_human_seg.onnx

# 2. Steady the frames: same size, same position, rope strands removed
python3 tools/run-loop/normalize.py

# 3. Pack one stride (frames 34-62) into an 8x4 sprite sheet
python3 tools/run-loop/build_sheet.py

# 4. Put the sheet inside the game page
python3 tools/run-loop/embed.py
```

| Script | What it does |
|---|---|
| `segment.py` | Runs the person-segmentation model and saves transparent PNG crops plus their positions in the frame (`boxes.txt`). |
| `normalize.py` | Keeps only Tenzin, trims rope strands, scales by a smoothed body height so he doesn't pulse with each stride, and anchors head and torso. Frames 47 and 48 are replaced by their neighbours because of rope blur next to his head. |
| `build_sheet.py` | Packs frames 34–62 into `build/run_sheet.webp`. Frame 63 matches 34, so the loop has no seam. |
| `embed.py` | Writes the sheet into `games/runner/index.html` as a data URI, so the game also works when opened from disk. |
