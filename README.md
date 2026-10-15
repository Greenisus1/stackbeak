# Stackbeak

A fullscreen, offline stack-and-dash bird runner for Raspberry Pi and Linux terminals. Your bird sprints to the right on its own; every tap drops another block under it, building a living tower. Walls slide in from the right at heights 1-5. If your stack is at least as tall as the wall, the wall shaves the matching blocks off your stack and you score its height. Too short and the bird bonks. Chain clean shaves to build fever, which doubles pass bonuses.

Original name, art, and code, in the spirit of one-tap stack runners like Square Bird. This is a simplified terminal tribute: it shares no assets or code with any commercial game and does not claim to be a port.

## Run

```
python3 stackbeak.py
```

Python 3 with curses. No other dependencies, no network, no install. Saves your best score to `~/.local/share/stackbeak/best.json`.

## Controls

- **Space / W / Up** - stack a block (max 8)
- **P** - pause
- **R** - restart
- **Q / Esc** - quit

## Scoring

- Shave a wall: + wall height, spends that many blocks
- Wall fully passed: +5
- Fever active: +5 extra per pass

## Install from the Pi App Store

Search for `stackbeak` in the games category, or use `app-store.sh` directly:

```
bash app-store.sh INSTALL
bash app-store.sh StAtUs
bash app-store.sh RUN
```

## Tests

```
python3 test_stackbeak.py   # 14 unit tests
python3 test_terminal.py    # real PTY controls/resize/restore check
```

## Scope

Local unit and PTY tests cover stacking rules, the 8-block cap, wall spawning and heights, shave/bonk collision outcomes, scoring, fever bonuses and decay, off-screen cleanup, deterministic seeds, best-score saves, resizing and clean terminal exit. Before publication, all 14 unit tests and the PTY control/resize/exit checks passed on a real aarch64 Raspberry Pi.

MIT licensed (Greenisus1).
