# Tenzin Run

An endless runner starring Tenzin, a young monk, running along a stone path above the clouds. Change lanes to dodge woodpiles, jump the low beams, and collect butter lamps while the speed keeps rising.

**Status: v2, work in progress.** The previous game, *Tenzin Ascent* (a four-chapter platformer), is kept in the [v1.0 release](https://github.com/tenzin3/tenzin-game/releases/tag/v1.0).

## ▶ Play now

**https://tenzin3.github.io/tenzin-game/**

It runs right in your browser, on a computer or a phone. To play offline, download this repository and open `index.html`.

| Action | Keys |
|---|---|
| Change lane | ← → or A / D (swipe on a phone) |
| Jump | Space, ↑ or W (swipe up or tap on a phone) |

## Animation credit

Tenzin's run comes from an animation by **Arkizen Studio**: https://www.instagram.com/arkizen.studio/

It's a looped cut-out of the rope-bridge shot in their morning-run animation, where Tenzin runs straight away from the camera. The track, buildings and obstacles are built in 3D with [three.js](https://threejs.org/).

## Project structure

```
tenzin-game/
├── index.html                      The game (Tenzin's sprite sheet is embedded in it)
├── tools/run-loop/                 Scripts that make the running sprite sheet from the video
├── source-animations/
│   └── morning-gong.mp4            Arkizen Studio's original video the run is cut from
├── README.md
└── .gitignore
```

How the running animation is made is described in [`tools/run-loop/README.md`](tools/run-loop/README.md).

## Publishing

The game is hosted with GitHub Pages from the `main` branch, root folder (**Settings → Pages**). Anything pushed to `main` goes live at the link above within a minute or two.
