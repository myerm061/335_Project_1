# visualizer.py
# pip install pygame

import random
import pygame
from typing import Generator, List, Tuple, Optional, Callable, Dict
import time

from sorting_steps import (
    bubble_sort_steps,
    quick_sort_steps,
    merge_sort_steps,
    radix_sort_steps,
)

Step = Tuple[List[int], List[int], str]

ALGOS: Dict[str, Callable[[List[int]], Generator[Step, None, None]]] = {
    "Bubble": bubble_sort_steps,
    "Quick": quick_sort_steps,
    "Merge": merge_sort_steps,
    "Radix": radix_sort_steps,
}
ORDER = ["Bubble", "Quick", "Merge", "Radix"]

WIDTH, HEIGHT = 1200, 700
MARGIN = 20
TOP_UI_H = 110

MIN_VAL, MAX_VAL = 5, 3000
N_MIN, N_MAX, N_STEP = 20, 200, 10


def make_base_array(n: int, mode: str) -> List[int]:
    arr = [random.randint(0, MAX_VAL) for _ in range(n)]  # Radix safe: >=0
    if mode == "sorted":
        arr.sort()
    elif mode == "reverse":
        arr.sort(reverse=True)
    return arr


# -------------------------
# Button
# -------------------------
class Button:
    def __init__(self, rect: pygame.Rect, text: str, on_click: Callable[[], None]):
        self.rect = rect
        self.text = text
        self.on_click = on_click

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        mouse = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse)
        bg = (70, 70, 85) if hovered else (45, 48, 60)
        pygame.draw.rect(screen, bg, self.rect, border_radius=8)
        pygame.draw.rect(screen, (120, 120, 140), self.rect, width=1, border_radius=8)

        txt = font.render(self.text, True, (240, 240, 240))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def handle(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()


def draw_bars_in_rect(
    screen: pygame.Surface,
    rect: pygame.Rect,
    arr: List[int],
    highlights: List[int],
    title: str,
    info: str,
    font: pygame.font.Font,
    elapsed_sec: Optional[float],
):
    # background for each quadrant
    pygame.draw.rect(screen, (22, 26, 36), rect, border_radius=12)
    pygame.draw.rect(screen, (70, 70, 90), rect, width=1, border_radius=12)

    # title
    screen.blit(font.render(title, True, (235, 235, 235)), (rect.x + 10, rect.y + 8))
    # small info (trim)
    small = info[:52] + ("..." if len(info) > 52 else "")
    screen.blit(font.render(small, True, (185, 185, 185)), (rect.x + 10, rect.y + 30))
    t_text = "time: --" if elapsed_sec is None else f"time: {elapsed_sec:.3f}s"
    screen.blit(font.render(t_text, True, (185, 185, 185)), (rect.x + 10, rect.y + 48))
    size_text = f"n = {len(arr)}"
    screen.blit(font.render(size_text, True, (180, 180, 180)), (rect.x + rect.w - 80, rect.y + 8))


    # bars area inside rect
    pad = 10
    bars_top = rect.y + 55
    bars_bottom = rect.y + rect.h - pad
    bars_h = max(1, bars_bottom - bars_top)
    bars_w = rect.w - 2 * pad

    if not arr:
        return
    max_v = max(arr) if max(arr) != 0 else 1
    bar_w = max(1, bars_w // len(arr))

    for i, v in enumerate(arr):
        x = rect.x + pad + i * bar_w
        h = int((v / max_v) * bars_h)
        y = bars_bottom - h
        color = (255, 165, 0) if i in highlights else (90, 170, 255)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, bar_w - 1, h))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sorting Visualizer (Pygame) - 4-up Compare")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 18)
    font_small = pygame.font.SysFont("arial", 16)

    mode = "random"
    n = 80
    steps_per_second = 180
    running = False

    # per-quadrant states
    arrays: Dict[str, List[int]] = {}
    gens: Dict[str, Optional[Generator[Step, None, None]]] = {}
    highlights: Dict[str, List[int]] = {}
    infos: Dict[str, str] = {}
    done = {}
    start_ts: Dict[str, Optional[float]] = {}
    elapsed: Dict[str, Optional[float]] = {}

    def init_all():
        nonlocal arrays, gens, highlights, infos, running, done, start_ts, elapsed
        base = make_base_array(n, mode)
        arrays = {name: base.copy() for name in ORDER}
        gens = {name: None for name in ORDER}
        highlights = {name: [] for name in ORDER}
        infos = {name: "Ready" for name in ORDER}
        done = {name: False for name in ORDER}
        start_ts = {name: None for name in ORDER}
        elapsed = {name: None for name in ORDER}
        running = False

    def start_pause():
        nonlocal running
        running = not running
        # lazily create generators on run
        if running:
            for name in ORDER:
                if (gens[name] is None) and (not done[name]):
                    gens[name] = ALGOS[name](arrays[name])
                    if start_ts[name] is None:
                        start_ts[name] = time.perf_counter()


    def reset():
        init_all()

    def set_mode(new_mode: str):
        nonlocal mode
        mode = new_mode
        init_all()

    def change_n(delta: int):
        nonlocal n
        n2 = max(N_MIN, min(N_MAX, n + delta))
        if n2 != n:
            n = n2
            init_all()

    def speed_up():
        nonlocal steps_per_second
        steps_per_second = min(2000, steps_per_second + 40)

    def speed_down():
        nonlocal steps_per_second
        steps_per_second = max(1, steps_per_second - 40)

    # UI buttons
    buttons: List[Button] = []
    x, y = MARGIN, MARGIN
    buttons.append(Button(pygame.Rect(x, y, 140, 40), "Start / Pause", start_pause))
    buttons.append(Button(pygame.Rect(x + 155, y, 100, 40), "Reset", reset))
    buttons.append(Button(pygame.Rect(x + 270, y, 60, 40), f"{N_STEP} -", lambda: change_n(-N_STEP)))
    buttons.append(Button(pygame.Rect(x + 340, y, 60, 40), f"{N_STEP} +", lambda: change_n(+N_STEP)))
    buttons.append(Button(pygame.Rect(x + 420, y, 70, 40), "Speed-", speed_down))
    buttons.append(Button(pygame.Rect(x + 500, y, 70, 40), "Speed+", speed_up))

    # mode buttons
    buttons.append(Button(pygame.Rect(x + 590, y, 110, 40), "Random", lambda: set_mode("random")))
    buttons.append(Button(pygame.Rect(x + 710, y, 110, 40), "Sorted", lambda: set_mode("sorted")))
    buttons.append(Button(pygame.Rect(x + 830, y, 110, 40), "Reverse", lambda: set_mode("reverse")))

    init_all()

    # Quadrant rectangles (2x2) below UI
    area = pygame.Rect(MARGIN, TOP_UI_H, WIDTH - 2 * MARGIN, HEIGHT - TOP_UI_H - MARGIN)
    gap = 14
    w2 = (area.w - gap) // 2
    h2 = (area.h - gap) // 2

    rects = {
        "Bubble": pygame.Rect(area.x, area.y, w2, h2),
        "Quick": pygame.Rect(area.x + w2 + gap, area.y, w2, h2),
        "Merge": pygame.Rect(area.x, area.y + h2 + gap, w2, h2),
        "Radix": pygame.Rect(area.x + w2 + gap, area.y + h2 + gap, w2, h2),
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            for b in buttons:
                b.handle(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_SPACE:
                    start_pause()
                if event.key == pygame.K_r:
                    reset()

        # advance steps
        if running:
            # steps per frame
            steps = max(1, steps_per_second // 60)
            steps = min(400, steps)

            for name in ORDER:
                if (gens[name] is None) and (not done[name]):
                    gens[name] = ALGOS[name](arrays[name])
                else:
                    if gens[name] is None:  
                        continue   

                for _ in range(steps):
                    try:
                        arr_state, hi, inf = next(gens[name])  # type: ignore
                        highlights[name] = hi
                        infos[name] = inf
                    except StopIteration:
                        gens[name] = None
                        done[name] = True
                        highlights[name] = []
                        infos[name] = f"{name}: finished"

                        if start_ts[name] is not None and elapsed[name] is None:
                            elapsed[name] = time.perf_counter() - start_ts[name]

                        break
            if all(done[name] for name in ORDER):
                running = False

        # draw
        screen.fill((15, 18, 25))

        header = f"4-up Compare | mode={mode} | {'RUN' if running else 'PAUSE'} | speed={steps_per_second} steps/s | n={n}"
        screen.blit(font.render(header, True, (235, 235, 235)), (MARGIN, 62))

        # UI panel
        ui_rect = pygame.Rect(MARGIN - 10, MARGIN - 8, WIDTH - 2 * (MARGIN - 10), 92)
        pygame.draw.rect(screen, (22, 26, 36), ui_rect, border_radius=12)
        pygame.draw.rect(screen, (70, 70, 90), ui_rect, width=1, border_radius=12)

        for b in buttons:
            b.draw(screen, font_small)

        # quadrants
        for name in ORDER:
            draw_bars_in_rect(
                screen=screen,
                rect=rects[name],
                arr=arrays[name],
                highlights=highlights[name],
                title=name,
                info=infos[name],
                font=font_small,
                elapsed_sec=elapsed[name],
            )

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
