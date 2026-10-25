# Tenzin Ascent

A four-chapter rooftop platformer about Tenzin, a young monk running, climbing and leaping across a Himalayan monastery. Each chapter opens with a cinematic, then you take control of Tenzin.

## ▶ Play now

**https://tenzin3.github.io/tenzin-game/**

The game runs right in your browser, on a computer or a phone. Nothing to download or install.

## Animation credit

All cinematics, the trailer and the still images in this game (title screen, Tenzin's portrait, chapter cards) come from animations by **Arkizen Studio**: https://www.instagram.com/arkizen.studio/

The playable Tenzin, the monkey, Gen-la and the levels are drawn in code to match the look of those animations.

## How to play

Play online at the link above, or download this repository and open `index.html` in a web browser (Chrome, Safari, Edge or Firefox) to play offline.

| Action | Keys |
|---|---|
| Run | ← → or A / D |
| Jump (hold for higher) | Space (also Z, K, ↑ or W away from ladders) |
| Climb ladders | ↑ / ↓ |
| Drop through a wooden plank | ↓ + Space |
| Wall-jump | Slide down a wall, then press Space |
| Pause | P or Esc |
| Mute | M |
| Skip a cinematic | Enter, Space or the Skip button |

On phones and tablets, on-screen buttons appear. Turn the phone sideways for a wider view.

## Chapters

1. **The Morning Gong**: race across the rooftops and ring the gong before the 2-minute timer runs out.
2. **The Monkey Thief**: a langur has stolen the gong striker. Chase it over the golden roofs and catch it on the rope bridge.
3. **Pages on the Wind**: gusts have scattered the pages. Collect all ten and bring them to Gen-la on the balcony.
4. **The Leap**: moving planks, a climb between two walls, then the big jump across the gap to Gen-la.

Butter lamps are optional collectibles in every chapter. Prayer wheels are checkpoints: touch one and that's where you'll come back after a fall. Finished chapters unlock on the title screen, and the full trailer plays from there and after the last chapter.

## Files

- `index.html`: the whole game (HTML, CSS and JavaScript in one file).
- `assets/intro1.mp4` to `intro4.mp4`: chapter cinematics (Arkizen Studio).
- `assets/trailer.mp4`: the Tenzin Ascent trailer (Arkizen Studio).
- `assets/title.jpg`, `portrait.jpg`, `card1.jpg` to `card4.jpg`: stills taken from the animations (Arkizen Studio).
- `source-animations/`: the original full-quality animations by Arkizen Studio (`morning-gong.mp4`, `monkey-thief.mp4`, `pages-on-the-wind.mp4`, `the-leap.mp4`, `trailer.mp4`). The game itself uses the smaller copies in `assets/`.

## Publishing

The game is hosted with GitHub Pages from the `main` branch, root folder (**Settings → Pages**). Anything pushed to `main` goes live at the link above within a minute or two.
