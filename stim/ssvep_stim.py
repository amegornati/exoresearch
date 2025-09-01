#!/usr/bin/env python3
"""
SSVEP stimulus window with four flickering squares and LSL markers.

Run:
  python stim/ssvep_stim.py
Press ESC to quit.
"""
import pygame as pg
import math, time
from pylsl import local_clock
from utils.lsl_utils import make_marker_outlet, push_marker

FREQS = [10, 12, 15, 20]    # Hz
LABELS = ["A", "B", "C", "D"]
SCREEN_SIZE = (900, 700)
BG = (10, 10, 12)
FG = (230, 230, 240)
FPS = 120  # draw loop; approximates target Hz via toggling

def main():
    pg.init()
    pg.display.set_caption("SSVEP Stimulus")
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()

    # 2x2 layout
    rects = []
    w, h = SCREEN_SIZE
    pad = 40
    box_w, box_h = (w - 3*pad)//2, (h - 3*pad)//2
    positions = [
        (pad, pad), (2*pad + box_w, pad),
        (pad, 2*pad + box_h), (2*pad + box_w, 2*pad + box_h)
    ]
    for pos in positions:
        rects.append(pg.Rect(pos[0], pos[1], box_w, box_h))

    outlet = make_marker_outlet(name="markers")
    start_time = time.time()
    running = True
    font = pg.font.SysFont("Arial", 48, bold=True)

    while running:
        t = time.time() - start_time
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False

        screen.fill(BG)

        for i, r in enumerate(rects):
            freq = FREQS[i]
            phase = math.sin(2*math.pi*freq*t)
            on = 1 if phase >= 0 else 0
            c = (70, 70, 85) if on else (22, 22, 30)
            pg.draw.rect(screen, c, r, border_radius=18)

            text = font.render(f"{LABELS[i]}  {freq:.0f}Hz", True, FG)
            screen.blit(text, (r.x + 20, r.y + 20))

        # ~1 Hz heartbeat marker (helps you confirm markers are flowing)
        if int(t) != int(t - 1):
            push_marker(outlet, f"heartbeat:{local_clock():.3f}")

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()

if __name__ == "__main__":
    main()
