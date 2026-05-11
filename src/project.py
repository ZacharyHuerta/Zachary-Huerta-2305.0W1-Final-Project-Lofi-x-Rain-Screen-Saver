import os
import random
import pygame
import math

AUDIO_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "audio")

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

ROOM_THEMES = [
    {"name": "neutral", "color": (0,   0,   0,   0)},
    {"name": "lofi",    "color": (255, 180, 80,  40)},
    {"name": "night",   "color": (30,  60,  180, 50)},
    {"name": "sunset",  "color": (255, 80,  120, 40)},
    {"name": "forest",  "color": (50,  180, 80,  40)},
    {"name": "neon",    "color": (180, 0,   255, 45)},
]

RAIN_STYLES = [
    {
        "name": "classic",
        "birth_rate": 3,
        "particle_size": 18,
        "speed_min": 0.8,
        "speed_max": 2.2,
        "shape": None,
        "angle": 0,
    },
    {
        "name": "chars",
        "birth_rate": 3,
        "particle_size": 18,
        "speed_min": 0.8,
        "speed_max": 2.2,
        "shape": "char",
        "angle": 0,
    },
    {
        "name": "shapes",
        "birth_rate": 3,
        "particle_size": 20,
        "speed_min": 0.8,
        "speed_max": 2.2,
        "shape": "square",
        "angle": 0,
    },
    {
        "name": "dense",
        "birth_rate": 8,
        "particle_size": 12,
        "speed_min": 2.0,
        "speed_max": 4.0,
        "shape": None,
        "angle": 0,
    },
    {
        "name": "sparse",
        "birth_rate": 1,
        "particle_size": 28,
        "speed_min": 0.3,
        "speed_max": 0.8,
        "shape": None,
        "angle": 0,
    },
    {
        "name": "glitch",
        "birth_rate": 5,
        "particle_size": 18,
        "speed_min": 0.5,
        "speed_max": 5.0,
        "shape": "char",
        "angle": 0,
    },
    {
        "name": "diagonal",
        "birth_rate": 3,
        "particle_size": 18,
        "speed_min": 0.8,
        "speed_max":2.2,
        "shape": None,
        "angle": 30,
    },
]

RAIN_STYLE_NAMES = [s["name"] for s in RAIN_STYLES]

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
        #Glow - background layer
        glow = self.surface.copy()
        glow_size = int(self.size * 1.8)
        glow = pygame.transform.scale(glow, (glow_size, glow_size))
        glow.set_alpha(int(self.alpha * 0.25))
        offset = (self.size - glow_size) // 2
        surface.blit(glow, (self.pos[0] + offset, self.pos[1] + offset))


        #Overlay
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)


class ParticleTrail():

    def __init__(self, pos, size, life, theme_name, font,
                 speed_min=0.8, speed_max=2.2, shape=None, angle=0):
        self.pos = pos
        self.size = size
        self.life = life
        self.theme_name = theme_name
        self.font = font
        self.particles = []
        self.speed = random.uniform(speed_min, speed_max)
        self.shape = shape
        self.angle = angle
        self.sub_pos = float(pos[1])
        self.step_acc = 0.0
    
    def update(self, dt):
        head = Particle(pos=self.pos, size=self.size, life=self.life,
                        theme_name=self.theme_name, is_head=True,
                        shape=self.shape, font=self.font)
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
        angle_rad = math.radians(self.angle)
        dx = int(pixels * math.sin(angle_rad))
        dy = int(pixels * math.cos(angle_rad))
        self.pos = (x + dx, y + dy)

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
        self.style_idx = 0
        self.current_shape = None
        self.angle = 0
        self.speed_min = 0.8
        self.speed_max = 2.2

    def apply_style(self, style):
        self.birth_rate = style["birth_rate"]
        self.particle_size = style["particle_size"]
        self.current_shape = style["shape"]
        self.angle = style["angle"]
        self.speed_min = style["speed_min"]
        self.speed_max = style["speed_max"]
        self.trails = []

    def next_style(self):
        self.style_idx = (self.style_idx + 1) % len(RAIN_STYLES)
        self.apply_style(RAIN_STYLES[self.style_idx])

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
            trail = ParticleTrail((x, 0), ps, life, t, self.font,
                                  self.speed_min, self.speed_max,
                                  self.current_shape, self.angle)
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

class Room:

    def __init__(self, image_path, window_coords, resolution):
        self.window_rect = pygame.Rect(*window_coords)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(base_dir, "..", "assets", "images", "room.png")

        # Load image and treat pure black as transparent
        raw = pygame.image.load(abs_path).convert()
        raw.set_colorkey((255, 255, 255))        # black becomes transparent
        self.image = pygame.transform.scale(raw, resolution)

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
    
class RoomOverlay:
    def __init__(self, resolution, exclude_rects):
        self.resolution = resolution
        self.exclude_rects = exclude_rects # list of rects to punch holes in
        self.themes = ROOM_THEMES
        self.current_idx = 0
        self.target_idx = 0
        self.fade_speed = 0.02
        self.blend = 0.0
        self.auto_cycle = False
        self.auto_timer = 0
        self.auto_interval = 4000 #cycle every 4 seconds

    def next_theme(self):
        self.target_idx = (self.current_idx + 1) % len(self.themes)
        self.blend = 0.0

    def update(self, dt):
        if self.blend < 1.0:
            self.blend = min(1.0, self.blend + self.fade_speed)
            if self.blend >= 1.0:
                self.current_idx = self.target_idx

        if self.auto_cycle:
            self.auto_timer += dt
            if self.auto_timer >= self.auto_interval:
                self.auto_timer = 0
                self.next_theme()

    def draw(self, surface):
        cur = self.themes[self.current_idx]["color"]
        tgt = self.themes[self.target_idx]["color"]

        # Switching RGBA between current and target
        r = int(cur[0] + (tgt[0] - cur[0]) * self.blend)
        g = int(cur[1] + (tgt[1] - cur[1]) * self.blend)
        b = int(cur[2] + (tgt[2] - cur[2]) * self.blend)
        a = int(cur[3] + (tgt[3] - cur[3]) * self.blend)

        # Drawing Overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((r, g, b, a))

        #Punching holes in monitor and window
        for rect in self.exclude_rects:
            overlay.fill((0, 0, 0, 0), rect)

        surface.blit(overlay, (0,0))

class MusicPlayer:
    def __init__(self, audio_folder):
        pygame.mixer.init()
        self.tracks = [
            f for f in os.listdir(audio_folder)
            if f.endswith((".mp3", ".wav"))
        ]
        self.tracks.sort()
        self.audio_folder = audio_folder
        self.current_idx = 0
        self.playing = False
        self.auto_cycle = False
        self.auto_timer = 0 
        self.auto_interval = 30000
        self.on_track_change = None

    def play(self):
        if not self.tracks:
            return
        
        path = os.path.join(self.audio_folder, self.tracks[self.current_idx])
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        self.playing = True

    def next_track(self):
        self.current_idx = (self.current_idx + 1) % len(self.tracks)
        self.play()
        if self.on_track_change:
            self.on_track_change(self.current_track_name())

    def current_track_name(self):
        if not self.tracks:
            return "No tracks found"
        name = self.tracks[self.current_idx]
        return os.path.splitext(name)[0] #strips file extension
    
    def update(self, dt):
        if self.auto_cycle:
            self.auto_timer += dt
            if self.auto_timer >= self.auto_interval:
                self.auto_timer = 0
                self.next_track()

class MonitorDisplay:
    def __init__(self, monitor_rect, font):
        self.rect = monitor_rect
        self.font = font
        self.text = ""
        self.x = float(monitor_rect.right)
        self.speed = 80
        self.bg_color = (10, 10, 30)

    def set_track(self, name):
        self.text = f"  ♪  Now Playing: {name}  ♪  "
        self.x = float(self.rect.right)

    def update(self, dt):
        self.x -= self.speed * (dt / 1000)
        text_width = self.font.size(self.text)[0]
        if self.x < self.rect.left - text_width:
            self.x = float(self.rect.right)

    def draw(self, surface, rain_theme_name):
        # Draws monitor dark background
        pygame.draw.rect(surface, self.bg_color, self.rect)

        # Subtle glow - slightly lighter rect layered on top
        glow_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        glow_surf.fill((40, 60, 80, 30))
        surface.blit(glow_surf, self.rect.topleft)

        # Get current rain color for text
        theme = COLOR_THEMES.get(rain_theme_name, COLOR_THEMES["matrix"])
        text_color = theme["body"]

        # Glow effect - render text slightly transparent behind main text
        old_clip = surface.get_clip()
        surface.set_clip(self.rect)

        glow_text = self.font.render(self.text, True, text_color)
        glow_text.set_alpha(60)
        text_y = self.rect.y + (self.rect.height - glow_text.get_height()) // 2
        for offset in [-2, 2]:
            surface.blit(glow_text, (int(self.x) + offset, text_y))
            surface.blit(glow_text, (int(self.x), text_y + offset))

        # Main text overlay
        text_surf = self.font.render(self.text, True, text_color)
        surface.blit(text_surf, (int(self.x), text_y))

        surface.set_clip(old_clip)

def draw_hud(surface, font_small, rain, room_overlay, music_player, fps):
    lines = [
        f"FPS: {fps:.0f}",
        f"Rain: {rain.theme_name.upper()} | [T] next | [C] auto cycle rain|{'On' if rain.theme_cycle else 'OFF'} | Style: {RAIN_STYLE_NAMES[rain.style_idx].upper()} [S] next Rain Style",
        f"Room: {ROOM_THEMES[room_overlay.current_idx]['name'].upper()} | [R] next | [B] auto cycle room theme {'On' if room_overlay.auto_cycle else 'OFF'} | ",
        f"Now Playing: {music_player.current_track_name()} | [M] next music track | [N] 30 sec auto cycle {'On' if music_player.auto_cycle else 'OFF'} ",
        f"Rain Trails: {len(rain.trails)}",
        "| [+/-] rain speed | [CLICK] rain burst | [ESC] quit"
    ]
    y = 6
    for line in lines:
        shadow = font_small.render(line, True, (0, 0, 0))
        text = font_small.render(line, True, (0, 200, 80))
        surface.blit(shadow, (11, y +1))
        surface.blit(text, (10, y))
        y += font_small.get_height() + 6

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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, "..", "assets", "fonts", "VT323-Regular.ttf")
    monitor_font = pygame.Font(font_path, 36)

    flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    info = pygame.display.Info()
    resolution = (info.current_w, info.current_h)          # match PNG canvas size
    screen = pygame.display.set_mode(resolution, flags)

    orig_w, orig_h = 1281, 721
    scale_x = resolution[0] / orig_w
    scale_y = resolution[1] / orig_h

    win_x = 944
    win_y = 160
    win_w = 660
    win_h = 517

    monitor_rect = pygame.Rect(
        int(235 * scale_x),
        int(245 * scale_y),
        int(233 * scale_x),
        int(149 * scale_y)
    )
    pygame.display.set_caption("Study Room")

    clock = pygame.time.Clock()
    fps_cap = 30
    dt = 0
    show_hud = True

    # Window hole coords (x, y, w, h) — corrected for pygame origin compared to illustrators
    room = Room("../assets/images/room.png", (win_x, win_y, win_w, win_h), resolution)
    room_overlay = RoomOverlay(resolution, [room.window_rect, monitor_rect])

    music_player = MusicPlayer(AUDIO_FOLDER)
    music_player.play()

    monitor_display = MonitorDisplay(monitor_rect, monitor_font)
    monitor_display.set_track(music_player.current_track_name())

    music_player.on_track_change = monitor_display.set_track

    rain = Rain((room.window_rect.width, room.window_rect.height), rain_font)
    rain_surface = pygame.Surface(
        (room.window_rect.width, room.window_rect.height)
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
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
                elif event.key == pygame.K_r:
                    room_overlay.next_theme()
                elif event.key == pygame.K_m:
                    music_player.next_track()
                    monitor_display.set_track(music_player.current_track_name())
                elif event.key == pygame.K_b:
                    room_overlay.auto_cycle = not room_overlay.auto_cycle
                elif event.key == pygame.K_n:
                    music_player.auto_cycle = not music_player.auto_cycle
                elif event.key == pygame.K_s:
                    rain.next_style()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if room.window_rect.collidepoint(event.pos):
                    local = (event.pos[0] - room.window_rect.x,
                             event.pos[1] - room.window_rect.y)
                    rain.spawn_burst(local, count=14)
            elif event.type == pygame.USEREVENT + 1:
                music_player.next_track()
                monitor_display.set_track(music_player.current_track_name())

        # --- Update ---
        rain.update(dt)
        music_player.update(dt)

        # --- Draw layers ---
        screen.fill((255, 255, 255))           # 1. dark background / night sky color

        rain_surface.fill((10, 10, 30))     # 2. fill rain surface dark
        rain.draw(rain_surface)
        screen.blit(rain_surface,           # 3. blit rain into window position
                    room.window_rect.topleft)

        room.draw(screen)                   # 4. room drawn on top (black hole = transparent)
        
        # pygame.draw.rect(screen, (255, 255, 255), monitor_rect) # 5. clear monitor area to white before overlay so no color bleeds through
        
        room_overlay.update(dt)
        room_overlay.draw(screen)

        monitor_display.update(dt)
        monitor_display.draw(screen, rain.theme_name)

        if show_hud:
            draw_hud(screen, hud_font, rain, room_overlay, music_player, clock.get_fps())

        pygame.display.flip()
        dt = clock.tick(fps_cap)

    pygame.quit()

#ENJOY THE RAIN
if __name__ == "__main__":
    main()