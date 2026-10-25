# Tenzin Games

Browser games starring Tenzin, a young monk in a Himalayan monastery, built around animations by **Arkizen Studio**.

## ▶ Play now

**https://tenzin3.github.io/tenzin-game/**

The link opens a menu with both games. They run right in your browser, on a computer or a phone, with nothing to download or install.

| Game | Status | Direct link |
|---|---|---|
| **Tenzin Ascent**: four-chapter rooftop platformer | v1, playable | https://tenzin3.github.io/tenzin-game/games/ascent/ |
| **Tenzin Run**: endless runner | v2, work in progress | https://tenzin3.github.io/tenzin-game/games/runner/ |

## Animation credit

All cinematics, the trailer and the still images come from animations by **Arkizen Studio**: https://www.instagram.com/arkizen.studio/

- In **Tenzin Ascent**, the cinematics play before each chapter. The playable Tenzin, the monkey, Gen-la and the levels are drawn in code to match the animations' look.
- In **Tenzin Run**, Tenzin's run is a looped cut-out taken straight from the animation's rope-bridge shot.

## Project structure

```
tenzin-game/
├── index.html                 Menu page (what the Play now link opens)
├── games/
│   ├── ascent/                Tenzin Ascent (v1)
│   │   ├── index.html         The whole game: HTML, CSS and JavaScript
│   │   └── assets/            Cinematics, trailer and stills used by the game
│   └── runner/                Tenzin Run (v2, work in progress)
│       ├── index.html         The game, with Tenzin's sprite sheet embedded
│       └── preview.jpg        Screenshot for the menu page
├── tools/
│   └── run-loop/              Scripts that make Tenzin's running sprite sheet
├── source-animations/         Arkizen Studio's original full-quality videos
├── README.md
└── .gitignore
```

## Tenzin Ascent (v1)

Each chapter opens with a cinematic, then you take control of Tenzin.

1. **The Morning Gong**: race across the rooftops and ring the gong before the 2-minute timer runs out.
2. **The Monkey Thief**: a langur has stolen the gong striker. Chase it over the golden roofs and catch it on the rope bridge.
3. **Pages on the Wind**: gusts have scattered the pages. Collect all ten and bring them to Gen-la on the balcony.
4. **The Leap**: moving planks, a climb between two walls, then the big jump across the gap to Gen-la.

Butter lamps are optional collectibles in every chapter. Prayer wheels are checkpoints: touch one and that's where you'll come back after a fall. Finished chapters unlock on the title screen, and the full trailer plays from there and after the last chapter.

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

## Tenzin Run (v2, work in progress)

Tenzin runs along a stone path above the clouds. Change lanes to dodge woodpiles, jump the low beams, and collect butter lamps while the speed keeps rising.

| Action | Keys |
|---|---|
| Change lane | ← → or A / D (swipe on a phone) |
| Jump | Space, ↑ or W (swipe up or tap on a phone) |

How the running animation is made from the video is described in [`tools/run-loop/README.md`](tools/run-loop/README.md).

## Playing offline

Download this repository and open `index.html` in a web browser (Chrome, Safari, Edge or Firefox). You can also open a game's own `index.html` inside `games/` directly.

## Publishing

The site is hosted with GitHub Pages from the `main` branch, root folder (**Settings → Pages**). Anything pushed to `main` goes live at the link above within a minute or two.
