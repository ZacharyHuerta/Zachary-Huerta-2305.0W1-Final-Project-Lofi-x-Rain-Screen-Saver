import random
import pygame
import math


# Katakana + ASCII char pool
KATAKANA = [chr(c) for c in range(0x30A0, 0x30FF)]
ASCII_CHARS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%&")
SYMBOLS = list("!?><|/\\[]}{~^")
ALL_CHARS = KATAKANA + ASCII_CHARS + SYMBOLS

# Color Themes
COLOR_THEMES = {
    "matrix": {"head": (220, 255, 220), "body": (0, 255, 70), "tail": (0, 100, 30)},
    "cyber": {"head": (255, 255, 255), "body": (0, 200, 255), "tail": (0, 60, 120)},
    "blood": {"head": (255, 220, 220), "body": (220, 0, 50), "tail": (80, 0, 20)},
    "gold": {"head": (255, 255, 200), "body": (255, 180, 0), "tail": (100, 60, 0)},
    "purple": {"head": (240, 220, 255), "body": (160, 0, 255), "tail": (60, 0, 100)},
    "ice": {"head": (230, 245, 255), "body": (80, 200, 255), "tail": (20, 60, 120)},
    "toxic": {"head": (240, 255, 150), "body": (140, 255, 0), "tail": (40, 80, 0)},
    "fire": {"head": (255, 255, 200), "body": (255, 100, 0), "tail": (100, 20, 0)},
}

THEME_NAMES = list(COLOR_THEMES.keys())

class Particle():
    SHAPE_SQUARE = "square"
    SHAPE_CIRCLE = "circle"
    SHAPE_DIAMOND = "diamond"
    SHAPE_CHAR = "char"

    def __init__(self, pos=(0, 0), size=15, life=1000,
                 theme_name="matrix", is_head=False, shape=None, font=None):
        self.pos = pos
        self.size = size
        self.age = 0 # age in milliseconds
        self.life = life # life in milliseconds
        self.dead = False
        self.alpha = 255
        self.is_head = is_head
        self.font = font

        # picks shape or char
        if shape is None:
            r = random.random()
            if r < 0.55:
                self.shape = self.SHAPE_CHAR
            elif r < 0.72:
                self.shape = self.SHAPE_SQUARE
            elif r < 0.86:
                self.shape = self.SHAPE_CIRCLE
            else:
                self.shape = self.SHAPE_DIAMOND
        else:
            self.shape = shape

        self.char = random.choice(ALL_CHARS)
        # self.surface = self.update_surface()

        # glitch timer
        self.glitch_interval = random.randint(80, 350)
        self.glitch_timer = 0

        # pick color from theme
        theme = COLOR_THEMES.get(theme_name, COLOR_THEMES["matrix"])
        if is_head:
            self.color = pygame.Color(*theme["head"])
        else:
            self.color = pygame.Color(*theme["body"])
        self.tail_color = pygame.Color(*theme["tail"])

        self.surface = self._make_surface()

    # rendering section

    def _make_surface(self):
        s = self.size
        surf = pygame.Surface((s, s), pygame.SRCALPHA)
        col = self.color

        if self.shape == self.SHAPE_SQUARE:
            inner = max(4, int(s * 0.75))
            off = (s - inner) // 2
            pygame.draw.rect(surf, col, (off, off, inner, inner))

        elif self.shape == self.SHAPE_CIRCLE:
            pygame.draw.circle(surf, col, (s // 2, s // 2), max(3, s // 2 - 2))

        elif self.shape == self.SHAPE_DIAMOND:
            cx, cy = s // 2, s // 2
            r = max(4, s // 2 - 1)
            pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
            pygame.draw.polygon(surf, col, pts)

        elif self.shape == self.SHAPE_CHAR and self.font:
            text_surf = self.font.render(self.char, True, col)
            tw, th = text_surf.get_size()
            surf.blit(text_surf, ((s - tw) // 2, (s - th) // 2))

        return surf


    def update(self, dt):
        self.age += dt
        if self.age > self.life:
            #print("Particle is dead")
            self.dead = True
            self.alpha = 0
            return
        
        frac = self.age / self.life
        
        self.alpha = int(255 * max(0, 1 - frac * 1.6))

        self.glitch_timer += dt
        if self.shape == self.SHAPE_CHAR and self.glitch_timer >= self.glitch_interval:
            self.glitch_timer = 0
            if random.random() < 0.5:
                self.char = random.choice(ALL_CHARS)
                self.surface = self._make_surface()
        
    def draw(self, surface):
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)


class ParticleTrail():

    def __init__(self, pos, size, life, theme_name, font):
        self.pos = pos
        self.size = size
        self.life = life
        self.theme_name = theme_name
        self.font = font
        self.particles = []
        self.speed = random.uniform(0.8, 2.2)
        self.sub_pos = float(pos[1])
        self.step_acc = 0.0
    
    def update(self, dt):
        head = Particle(pos=self.pos, size=self.size, life=self.life,
                        theme_name=self.theme_name, is_head=True, font=self.font)
        self.particles.insert(0, head)

        for p in self.particles[1:]:
            p.is_head = False
        
        self._update_particles(dt)
        self._advance(dt)

    def _update_particles(self, dt):
        alive = []
        for p in self.particles:
            p.update(dt)
            if not p.dead:
                alive.append(p)
            self.particles = alive

    def _advance(self, dt):
        pixels = self.speed * self.size
        x, y = self.pos
        self.pos = (x, y + int(pixels))

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class Rain():

    def __init__(self, screen_res, font):
        self.screen_res = screen_res
        self.particle_size = 18
        self.birth_rate = 3 #trails per frame
        self.trails = []
        self.font = font
        self.theme_name = random.choice(THEME_NAMES)
        self.theme_timer = 0
        self.theme_cycle = False

    def set_theme(self, name):
        self.theme_name = name

    def update(self, dt):
        if self.theme_cycle:
            self.theme_timer += dt
            if self.theme_timer > 8000:
                self.theme_timer = 0
                idx = THEME_NAMES.index(self.theme_name)
                self.theme_name = THEME_NAMES[(idx + 1) % len(THEME_NAMES)]

        self._birth_new_trails()
        self._update_trails(dt)

    def _update_trails(self, dt):
        alive = []
        for trail in self.trails:
            trail.update(dt)
            if not self._trail_offscreen(trail):
                alive.append(trail)
        self.trails = alive

    def _trail_offscreen(self, trail):
        if not trail.particles:
            return trail.pos[1] > self.screen_res[1]
        return trail.particles[-1].pos[1] > self.screen_res[1] + 50

    def _birth_new_trails(self):
        sw = self.screen_res[0]
        ps = self.particle_size
        for _ in range(self.birth_rate):
            x = random.randrange(0, sw, ps)
            life = random.randint(400, 2800)
            t = self.theme_name if random.random() < 0.75 else random.choice(THEME_NAMES)
            trail = ParticleTrail((x, 0), ps, life, t, self.font)
            self.trails.insert(0, trail)

    def spawn_burst(self, pos, count=12):
        #Spawn in extra trails with a mouse click
        ps = self.particle_size
        for _ in range(count):
            ox = random.randint(-4, 4) * ps
            x = max(0, min(self.screen_res[0] - ps, pos[0] + ox))
            life = random.randint(500, 2000)
            t = self.theme_name
            trail = ParticleTrail((x, 0), ps, life, t, self.font)
            self.trails.insert(0, trail)

    def draw(self, surface):
        for trail in self.trails:
            trail.draw(surface)

class Room():
    

def draw_hud(surface, font_small, rain, fps):
    lines = [
        f"FPS: {fps:.0f}",
        f"Theme: {rain.theme_name.upper()} [T] next [C] auto cycle {'On' if rain.theme_cycle else 'OFF'}",
        f"Trails: {len(rain.trails)}",
        "[F] fullscreen [+/-] speed [CLICK] burst [ESC] quit"
    ]
    y = 6
    for line in lines:
        shadow = font_small.render(line, True, (0, 0, 0))
        text = font_small.render(line, True, (0, 200, 80))
        surface.blit(shadow, (11, y +1))
        surface.blit(text, (10, y))
        y += font_small.get_height() + 2

def main():
    pygame.init()
    pygame.font.init()

    CANDIDATE_FONTS = [
        "notosansmono", "couriernew", "lucidaconsole",
        "dejavusanmono", "liberationmono", "consolas", "monospace",
    ]
    rain_font = None
    for name in CANDIDATE_FONTS:
        try:
            f = pygame.font.SysFont(name, 16)
            f.render("ア", True, (0, 255, 0))
            rain_font = f
            break
        except Exception:
            continue
    if rain_font is None:
        rain_font = pygame.font.Font(None, 18)

    hud_font = pygame.font.SysFont("couriernew,monospace,dejavusansmono", 14)

    flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    info = pygame.display.Info()
    resolution = (max(info.current_w, 1920), max(info.current_h, 1080))
    screen = pygame.display.set_mode(resolution, flags)
    pygame.display.set_caption("Digital Rain")

    clock = pygame.time.Clock()
    dt = 0
    fps_cap = 18
    show_hud = True

    rain = Rain(resolution, rain_font)

    overlay = pygame.Surface(resolution, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 60))

    running = True
    while running:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_t:
                    idx = THEME_NAMES.index(rain.theme_name)
                    rain.theme_name = THEME_NAMES[(idx + 1) % len(THEME_NAMES)]
                elif event.key == pygame.K_c:
                    rain.theme_cycle = not rain.theme_cycle
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    rain.birth_rate = min(rain.birth_rate + 1, 20)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    rain.birth_rate = max(rain.birth_rate - 1, 1)
                elif event.key == pygame.K_h:
                    show_hud = not show_hud
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                rain.spawn_burst(event.pos, count=14)
        # some game logic
        rain.update(dt)
        # render and display
        screen.blit(overlay, (0,0))
        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        rain.draw(screen)

        if show_hud:
            draw_hud(screen, hud_font, rain, clock.get_fps())

        pygame.display.flip()
        dt = clock.tick(fps_cap)

    pygame.quit()

#ENJOY THE RAIN
if __name__ == "__main__":
    main()