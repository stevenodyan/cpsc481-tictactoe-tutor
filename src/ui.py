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
            {"label": "Win Length (k)",   "val": "4", "active": False},
        ]
        self._player = "X"
        self._error  = ""
        self._rects  = {}   # keyed by name → pygame.Rect

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._on_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            self._on_key(event)

    def _on_click(self, pos):
        self._error = ""
        # Field boxes
        for i, f in enumerate(self._fields):
            if self._rects.get(f"field_{i}") and self._rects[f"field_{i}"].collidepoint(pos):
                for j, g in enumerate(self._fields):
                    g["active"] = (i == j)
                return
        # Deactivate fields if clicking elsewhere
        for f in self._fields:
            f["active"] = False
        # Player radio
        for val in ("X", "O"):
            if self._rects.get(f"radio_{val}") and self._rects[f"radio_{val}"].collidepoint(pos):
                self._player = val
                return
        # Start button
        if self._rects.get("start") and self._rects["start"].collidepoint(pos):
            self._submit()

    def _on_key(self, event):
        for f in self._fields:
            if not f["active"]:
                continue
            if event.key == pygame.K_BACKSPACE:
                f["val"] = f["val"][:-1]
            elif event.unicode.isdigit() and len(f["val"]) < 2:
                f["val"] += event.unicode
            elif event.key == pygame.K_TAB:
                idx = self._fields.index(f)
                f["active"] = False
                self._fields[(idx + 1) % len(self._fields)]["active"] = True

    def _submit(self):
        try:
            m = int(self._fields[0]["val"])
            n = int(self._fields[1]["val"])
            k = int(self._fields[2]["val"])
        except ValueError:
            self._error = "All fields must be numbers."
            return
        if not (3 <= m <= 10 and 3 <= n <= 10):
            self._error = "m and n must be between 3 and 10."
            return
        if k > min(m, n) or k < 3:
            self._error = f"Win length must be 3–{min(m, n)}."
            return
        self.result = {"m": m, "n": n, "k": k, "player": self._player}

    def draw(self):
        s = self.screen
        s.fill(BG)

        title_f = _font(26, bold=True)
        label_f = _font(13)
        input_f = _font(15)
        btn_f   = _font(14, bold=True)
        err_f   = _font(12)

        cx = self.W // 2
        y  = 44

        # Title
        t = title_f.render("New Game", True, WHITE)
        s.blit(t, t.get_rect(centerx=cx, top=y)); y += 52

        # --- 1. Side-by-side Width & Height ---
        f0 = self._fields[0] # Width
        lbl0 = label_f.render(f0["label"], True, SUBTLE)
        s.blit(lbl0, (40, y))
        r0 = pygame.Rect(40, y + 22, (self.W - 90) // 2, 40)
        self._rects["field_0"] = r0

        f1 = self._fields[1] # Height
        lbl1 = label_f.render(f1["label"], True, SUBTLE)
        s.blit(lbl1, (cx + 5, y))
        r1 = pygame.Rect(cx + 5, y + 22, (self.W - 90) // 2, 40)
        self._rects["field_1"] = r1

        # Draw the Width and Height boxes
        for i, rect, f in [(0, r0, f0), (1, r1, f1)]:
            border_col = ACCENT if f["active"] else BORDER
            pygame.draw.rect(s, PANEL, rect, border_radius=8)
            pygame.draw.rect(s, border_col, rect, 2, border_radius=8)
            val_surf = input_f.render(f["val"], True, WHITE)
            s.blit(val_surf, val_surf.get_rect(midleft=(rect.x + 12, rect.centery)))

        y += 74

        # --- 2. Win Length (k) ---
        f2 = self._fields[2]
        lbl2 = label_f.render(f2["label"], True, SUBTLE)
        s.blit(lbl2, (40, y)); y += 22
        r2 = pygame.Rect(40, y, self.W - 80, 40)
        self._rects["field_2"] = r2
        border_col = ACCENT if f2["active"] else BORDER
        pygame.draw.rect(s, PANEL, r2, border_radius=8)
        pygame.draw.rect(s, border_col, r2, 2, border_radius=8)
        val2 = input_f.render(f2["val"], True, WHITE)
        s.blit(val2, val2.get_rect(midleft=(r2.x + 12, r2.centery)))
        
        y += 52

        # --- 3. Player radio (Segmented Button Style) ---
        lbl = label_f.render("Play as", True, SUBTLE)
        s.blit(lbl, (40, y)); y += 24

        bw = (self.W - 80) // 2  # Button width (half the screen width)
        for i, (val, col) in enumerate((("X", X_CLR), ("O", O_CLR))):
            r = pygame.Rect(40 + i*bw, y, bw, 36)
            self._rects[f"radio_{val}"] = r
            active = self._player == val
            fill = col if active else PANEL
            
            # Round the outer corners to make it look like a single pill
            rad_kwargs = {'border_top_left_radius': 8, 'border_bottom_left_radius': 8} if i == 0 else \
                         {'border_top_right_radius': 8, 'border_bottom_right_radius': 8}
            
            pygame.draw.rect(s, fill, r, **rad_kwargs)
            pygame.draw.rect(s, col, r, 2, **rad_kwargs)
            txt = btn_f.render(val, True, BG if active else col)
            s.blit(txt, txt.get_rect(center=r.center))
        y += 56

        # Error text
        if self._error:
            err = err_f.render(self._error, True, O_CLR)
            s.blit(err, err.get_rect(centerx=cx, top=y))

        # --- 4. Start button (Anchored near the bottom) ---
        btn = pygame.Rect(40, self.H - 80, self.W - 80, 46) 
        self._rects["start"] = btn
        mx, my = pygame.mouse.get_pos()
        hover = btn.collidepoint(mx, my)
        pygame.draw.rect(s, tuple(min(c+20,255) for c in ACCENT) if hover else ACCENT,
                         btn, border_radius=10)
        bt = btn_f.render("Start Game", True, WHITE)
        s.blit(bt, bt.get_rect(center=btn.center))

        pygame.display.flip()


# ── Game Screen ─────────────────────────────────────────────────────────────

CELL  = 80
TOP   = 70
BOT   = 110
SIDE  = 40

class GameScreen:
    def __init__(self, screen, game, tutor, player_side):
        self.screen      = screen
        self.game        = game
        self.tutor       = tutor
        self.player_side = player_side
        self.state       = game.initial
        self._hint_move  = None
        self._hint_text  = ""
        self._feedback_text = ""
        self._hovered    = None
        self._ai_pending = False
        self._ai_delay   = 0
        self._thinking   = False
        self._new_game   = False   # signal to caller to restart

        # Resize window to fit board
        W = game.h * CELL + SIDE * 2
        H = game.v * CELL + TOP + BOT
        self.W, self.H = W, H
        pygame.display.set_mode((W, H))

        # Pre-compute stable button rects
        self._rects = {
            "hint": pygame.Rect(SIDE, H - BOT + 14, 90, 34),
            "new":  pygame.Rect(W - SIDE - 110, H - BOT + 14, 110, 34),
        }

        # If human is O, AI (X) goes first
        if self.state.to_move != self.player_side:
            self._schedule_ai()

    # ── Event handling ──────────────────────────────────────────────────────

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._on_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self._hovered = self._cell_at(event.pos)

    def update(self):
        if self._ai_pending and pygame.time.get_ticks() >= self._ai_delay:
            self._ai_pending = False
            self._do_ai_move()

    def _on_click(self, pos):
        # New Game is always clickable
        if self._rects["new"].collidepoint(pos):
            self._new_game = True
            return

        if self._ai_pending or self._thinking:
            return
        if self.tutor.is_terminal(self.state):
            return

        # Hint button
        if self._rects["hint"].collidepoint(pos):
            self._get_hint()
            return

        # Board cell
        if self.state.to_move != self.player_side:
            return
        cell = self._cell_at(pos)
        if cell and cell in self.state.moves:
            # 1. Get Tutor feedback BEFORE applying the move
            evaluation = self.tutor.evaluate_player_move(self.state, cell)
            self._feedback_text = f"Tutor: {evaluation}"
            
            # 2. Apply the move normally
            self._hint_move = None
            self._hint_text = ""
            self.state = self.tutor.apply_move(self.state, cell)
            if not self.tutor.is_terminal(self.state):
                self._schedule_ai()

    def _schedule_ai(self):
        self._ai_pending = True
        self._ai_delay   = pygame.time.get_ticks() + 600

    def _do_ai_move(self):
        self._thinking = True
        def run_ai():
            move, _ = self.tutor.recommend(self.state)
            self._pending_move = move
            self._thinking = False
        t = threading.Thread(target=run_ai, daemon=True)
        t.start()
        t.join()  # small board — fast enough; keeps code simple
        self.state = self.tutor.apply_move(self.state, self._pending_move)
        self._hint_move = None
        self._hint_text = ""

    def _get_hint(self):
        if self.tutor.is_terminal(self.state):
            return
        if self.state.to_move != self.player_side:
            return
        move, _ = self.tutor.recommend(self.state)
        self._hint_move = move
        self._hint_text = f"Hint → col {move[0]}, row {move[1]}"

    # ── Coordinate helpers ──────────────────────────────────────────────────

    def _cell_rect(self, x, y):
        x0 = SIDE + (x - 1) * CELL
        y0 = TOP  + (y - 1) * CELL
        return pygame.Rect(x0, y0, CELL, CELL)

    def _cell_at(self, pos):
        mx, my = pos
        x = (mx - SIDE) // CELL + 1
        y = (my - TOP)  // CELL + 1
        if 1 <= x <= self.game.h and 1 <= y <= self.game.v:
            return (x, y)
        return None

    # ── Drawing ─────────────────────────────────────────────────────────────

    def draw(self):
        s = self.screen
        s.fill(BG)
        self._draw_board()
        self._draw_status()
        self._draw_controls()
        pygame.display.flip()

    def _draw_board(self):
        s = self.screen
        board = self.state.board

        for y in range(1, self.game.v + 1):
            for x in range(1, self.game.h + 1):
                cell = (x, y)
                r    = self._cell_rect(x, y)
                inner = r.inflate(-6, -6)
                mark  = board.get(cell)

                # Cell background
                if mark:
                    fill = PANEL
                elif cell == self._hint_move:
                    fill = (45, 38, 15)   # dark gold tint
                elif cell == self._hovered and cell in self.state.moves:
                    fill = CELL_HOVER
                else:
                    fill = CELL_BG

                pygame.draw.rect(s, fill, inner, border_radius=10)

                # Hint ring
                if cell == self._hint_move and not mark:
                    pygame.draw.rect(s, HINT_CLR, inner, 2, border_radius=10)

                # Mark
                if mark:
                    color = X_CLR if mark == "X" else O_CLR
                    f = _font(int(CELL * 0.52), bold=True)
                    t = f.render(mark, True, color)
                    s.blit(t, t.get_rect(center=inner.center))

        # Grid lines
        for x in range(self.game.h + 1):
            px = SIDE + x * CELL
            pygame.draw.line(s, BORDER,
                             (px, TOP), (px, TOP + self.game.v * CELL), 1)
        for y in range(self.game.v + 1):
            py = TOP + y * CELL
            pygame.draw.line(s, BORDER,
                             (SIDE, py), (SIDE + self.game.h * CELL, py), 1)

    def _draw_status(self):
        s  = self.screen
        sf = _font(15, bold=True)
        hf = _font(12)

        if self.tutor.is_terminal(self.state):
            msg = self.tutor.result_message(self.state)
            col = X_CLR if "X" in msg else (O_CLR if "O" in msg else SUBTLE)
        elif self._ai_pending:
            msg, col = "AI is thinking…", SUBTLE
        elif self.state.to_move == self.player_side:
            msg = f"Your turn  ({self.player_side})"
            col = X_CLR if self.player_side == "X" else O_CLR
        else:
            msg = f"AI's turn  ({self.state.to_move})"
            col = X_CLR if self.state.to_move == "X" else O_CLR

        t = sf.render(msg, True, col)
        s.blit(t, t.get_rect(centerx=self.W // 2, centery=TOP // 2))

        # Show Hint if it exists, otherwise show Tutor Feedback
        if self._hint_text:
            ht = hf.render(self._hint_text, True, HINT_CLR)
            s.blit(ht, ht.get_rect(centerx=self.W // 2,
                                   centery=self.H - BOT // 2 + 14))
        elif self._feedback_text:
            ft = hf.render(self._feedback_text, True, SUCCESS)
            s.blit(ft, ft.get_rect(centerx=self.W // 2,
                                   centery=self.H - BOT // 2 + 14))

    def _draw_controls(self):
        s   = self.screen
        bf  = _font(12, bold=True)
        mx, my = pygame.mouse.get_pos()

        # Hint button (bottom-left)
        hint_r = self._rects["hint"]
        terminal = self.tutor.is_terminal(self.state)
        can_hint = (not terminal and not self._ai_pending
                    and self.state.to_move == self.player_side)
        hov = hint_r.collidepoint(mx, my) and can_hint
        col = ACCENT if can_hint else BORDER
        pygame.draw.rect(s, tuple(min(c+25,255) for c in col) if hov else col,
                         hint_r, border_radius=8)
        ht = bf.render("💡 Hint", True, WHITE if can_hint else SUBTLE)
        s.blit(ht, ht.get_rect(center=hint_r.center))

        # New Game button (bottom-right)
        new_r = self._rects["new"]
        nhov = new_r.collidepoint(mx, my)
        pygame.draw.rect(s, tuple(min(c+25,255) for c in PANEL) if nhov else PANEL,
                         new_r, border_radius=8)
        pygame.draw.rect(s, BORDER, new_r, 1, border_radius=8)
        nt = bf.render("New Game", True, WHITE)
        s.blit(nt, nt.get_rect(center=new_r.center))


# ── App entry point ─────────────────────────────────────────────────────────

def run():
    pygame.init()
    pygame.display.set_caption("Tic-Tac-Toe Tutor")

    screen = pygame.display.set_mode((ConfigScreen.W, ConfigScreen.H))
    clock  = pygame.time.Clock()

    while True:
        # ── Config phase ──
        cfg_screen = ConfigScreen(screen)
        pygame.display.set_mode((ConfigScreen.W, ConfigScreen.H))
        while cfg_screen.result is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); return
                cfg_screen.handle(event)
            cfg_screen.draw()
            clock.tick(FPS)

        # ── Game phase ──
        from src.board import TicTacToe
        from src.tutor import Tutor
        cfg  = cfg_screen.result
        game = TicTacToe(h=cfg["m"], v=cfg["n"], k=cfg["k"])
        tutor = Tutor(game)
        gs   = GameScreen(screen, game, tutor, cfg["player"])

        while not gs._new_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); return
                gs.handle(event)
            gs.update()
            gs.draw()
            clock.tick(FPS)
