"""
Pygame-based UI for m×n Tic-Tac-Toe Tutor.
Two screens: ConfigScreen → GameScreen.
"""
import threading
import pygame

# ── Palette ────────────────────────────────────────────────────────────────
BG          = (15,  23,  42)   # #0F172A
PANEL       = (30,  41,  59)   # #1E293B
BORDER      = (71,  85, 105)   # #475569
WHITE       = (248, 250, 252)  # #F8FAFC
SUBTLE      = (148, 163, 184)  # #94A3B8
X_CLR       = (96, 165, 250)   # #60A5FA  blue
O_CLR       = (248, 113, 113)  # #F87171  red
ACCENT      = (99, 102, 241)   # #6366F1  indigo
HINT_CLR    = (251, 191,  36)  # #FBBF24  gold
HOVER_CLR   = (30,  58, 138)   # dark blue tint
SUCCESS     = (74, 222, 128)   # #4ADE80  green
CELL_BG     = (30,  41,  59)
CELL_HOVER  = (44,  63,  92)

FONT_NAME = "Helvetica"
FPS = 60

def _font(size, bold=False):
    return pygame.font.SysFont(FONT_NAME, size, bold=bold)


# ── Config Screen ───────────────────────────────────────────────────────────

class ConfigScreen:
    W, H = 420, 460

    def __init__(self, screen):
        self.screen = screen
        self.result = None
        self._fields = [
            {"label": "Board Width (m)",  "val": "5", "active": False},
            {"label": "Board Height (n)", "val": "5", "active": False},
            {"label
