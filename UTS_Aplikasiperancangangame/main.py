import math
import random
import sys
import pygame

# Inisialisasi Pygame
pygame.init()

# Konfigurasi Layar (Ukuran Portrait / Layar HP)
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Meatball - Mobile View")

# Palet Warna (Tema Warung Kaki Lima Malam Hari)
NIGHT_DARK = (15, 15, 30)
STREET_ASPHALT = (40, 40, 50)
WARM_YELLOW = (255, 204, 0)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (230, 40, 40)
HEAVY_RED = (255, 75, 75)
HEART_EMPTY = (70, 70, 90)  # Warna hati saat nyawa hilang
SKIN_COLOR = (255, 220, 177)
BOWL_WHITE = (245, 245, 245)
BOWL_SHADOW = (180, 180, 180)
BROTH_COLOR = (210, 140, 60)
MEATBALL_COLOR = (230, 210, 180)
SHRIMP_PINK = (255, 150, 130)
CHILI_RED = (255, 0, 0)

# Warna Gerobak Hiasan Latar
CART_WOOD = (100, 60, 30)
CART_GLASS = (100, 140, 160)

# Clock untuk Framerate
clock = pygame.time.Clock()
FPS = 60

# Font Game
font_large = pygame.font.SysFont("Arial", 30, bold=True)
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 16)


# Fungsi untuk Menggambar Ikon Hati di UI
def draw_heart_icon(surf, x, y, active):
  color = HEAVY_RED if active else HEART_EMPTY
  pygame.draw.circle(surf, color, (x - 5, y), 6)
  pygame.draw.circle(surf, color, (x + 5, y), 6)
  points = [(x - 11, y + 2), (x + 11, y + 2), (x, y + 12)]
  pygame.draw.polygon(surf, color, points)


# Kelas Latar Belakang (Dilengkapi Hiasan Gerobak Kaki Lima)
class StreetFoodBackground:

  def __init__(self):
    self.lamps = [112, 225, 337]

  def draw(self, surf):
    # Langit Malam
    surf.fill(NIGHT_DARK)

    # Hiasan Gerobak Sisi Kiri
    cx1, cy1 = 60, SCREEN_HEIGHT - 170
    pygame.draw.rect(surf, CART_WOOD, (cx1, cy1, 70, 70))
    pygame.draw.rect(surf, CART_GLASS, (cx1 + 8, cy1 - 35, 54, 35))
    pygame.draw.circle(surf, BLACK, (cx1 + 35, cy1 + 70), 16)

    # Hiasan Gerobak Sisi Kanan
    cx2, cy2 = 330, SCREEN_HEIGHT - 190
    pygame.draw.rect(surf, (120, 70, 35), (cx2, cy2, 80, 80))
    pygame.draw.rect(surf, CART_GLASS, (cx2 + 10, cy2 - 40, 60, 40))
    pygame.draw.circle(surf, BLACK, (cx2 + 40, cy2 + 80), 18)

    # Jalan / Trotoar Bawah
    pygame.draw.rect(
        surf, STREET_ASPHALT, (0, SCREEN_HEIGHT - 90, SCREEN_WIDTH, 90)
    )
    pygame.draw.line(
        surf,
        (70, 70, 90),
        (0, SCREEN_HEIGHT - 90),
        (SCREEN_WIDTH, SCREEN_HEIGHT - 90),
        3,
    )

    # Lampu Gantung Warung
    for lx in self.lamps:
      pygame.draw.line(surf, BLACK, (lx, 0), (lx, 50), 2)
      pygame.draw.circle(surf, WARM_YELLOW, (lx, 55), 10)
      glow_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
      pygame.draw.circle(glow_surf, (255, 220, 100, 25), (30, 30), 25)
      surf.blit(glow_surf, (lx - 30, 55 - 30))


# Kelas Karakter (Mangkok Lebih Cekung / Melengkung di Bawah)
class NoodleBowlPlayer:

  def __init__(self):
    self.width = 110
    self.height = 65
    self.x = SCREEN_WIDTH // 2 - self.width // 2
    self.y = SCREEN_HEIGHT - 110
    self.speed = 7

  def move(self, direction):
    if direction == "LEFT":
      self.x -= self.speed
    elif direction == "RIGHT":
      self.x += self.speed

    if self.x < 0:
      self.x = 0
    elif self.x > SCREEN_WIDTH - self.width:
      self.x = SCREEN_WIDTH - self.width

  def draw(self, surf):
    # Tangan Kiri & Kanan Pemegang Mangkok
    pygame.draw.circle(
        surf, SKIN_COLOR, (int(self.x) + 5, int(self.y) + 35), 16
    )
    pygame.draw.circle(
        surf, SKIN_COLOR, (int(self.x) + self.width - 5, int(self.y) + 35), 16
    )

    # Bagian Luar Mangkok (Bentuk Cekung ke Bawah)
    bowl_outer_points = [
        (self.x, self.y + 15),
        (self.x + self.width, self.y + 15),
        (self.x + self.width - 15, self.y + 60),
        (self.x + 15, self.y + 60),
    ]
    pygame.draw.polygon(surf, BOWL_SHADOW, bowl_outer_points)

    bowl_inner_points = [
        (self.x + 3, self.y + 15),
        (self.x + self.width - 3, self.y + 15),
        (self.x + self.width - 18, self.y + 57),
        (self.x + 18, self.y + 57),
    ]
    pygame.draw.polygon(surf, BOWL_WHITE, bowl_inner_points)

    # Bibir Mangkok Atas
    rim_rect = pygame.Rect(self.x, self.y + 5, self.width, 22)
    pygame.draw.ellipse(surf, BOWL_WHITE, rim_rect)
    pygame.draw.ellipse(surf, BOWL_SHADOW, rim_rect, 2)

    # Isi Mangkok (Kuah & Mie)
    content_rect = pygame.Rect(
        self.x + 10, self.y + 14, self.width - 20, 24
    )
    pygame.draw.ellipse(surf, BROTH_COLOR, content_rect)
    pygame.draw.arc(
        surf,
        (255, 230, 120),
        (self.x + 22, self.y + 17, self.width - 44, 16),
        0,
        3.14,
        4,
    )


# Kelas Objek Jatuh (Topping, Cabai Pedas, & Hati)
class FallingItem:

  def __init__(self, score, existing_objects):
    self.radius = 16

    valid_x = False
    while not valid_x:
      self.x = random.randint(self.radius + 15, SCREEN_WIDTH - self.radius - 15)
      valid_x = True
      for obj in existing_objects:
        if abs(self.x - obj.x) < 60 and obj.y < 140:
          valid_x = False
          break

    self.y = -self.radius

    rand_val = random.random()
    if rand_val < 0.15:
      self.item_type = "heart"
      self.is_hazard = False
      self.is_healing = True
    elif rand_val < 0.35:
      self.item_type = "chili"
      self.is_hazard = True
      self.is_healing = False
    else:
      self.item_type = random.choice(["meatball", "siomay", "wonton"])
      self.is_hazard = False
      self.is_healing = False

    base_speed = random.uniform(1.2, 2.0)
    multiplier = score // 10
    self.speed = base_speed + (multiplier * 0.5)

  def fall(self):
    self.y += self.speed

  def draw(self, surf):
    if self.item_type == "meatball":
      pygame.draw.circle(
          surf, MEATBALL_COLOR, (int(self.x), int(self.y)), self.radius
      )
      pygame.draw.circle(
          surf, (180, 160, 130), (int(self.x) - 3, int(self.y) - 3), 3
      )
    elif self.item_type == "siomay":
      pygame.draw.circle(
          surf, SHRIMP_PINK, (int(self.x), int(self.y)), self.radius
      )
      pygame.draw.circle(
          surf, (255, 200, 100), (int(self.x), int(self.y) - 2), 5
      )
    elif self.item_type == "wonton":
      wonton_rect = pygame.Rect(
          int(self.x) - 13, int(self.y) - 11, 26, 22
      )
      pygame.draw.ellipse(surf, (210, 140, 60), wonton_rect)
    elif self.item_type == "chili":
      pygame.draw.ellipse(
          surf, CHILI_RED, (int(self.x) - 5, int(self.y) - 12, 10, 24)
      )
      pygame.draw.line(
          surf,
          (34, 139, 34),
          (int(self.x), int(self.y) - 12),
          (int(self.x) + 3, int(self.y) - 18),
          2,
      )
    elif self.item_type == "heart":
      hx, hy = int(self.x), int(self.y)
      pygame.draw.circle(surf, HEAVY_RED, (hx - 5, hy - 2), 7)
      pygame.draw.circle(surf, HEAVY_RED, (hx + 5, hy - 2), 7)
      points = [(hx - 12, hy), (hx + 12, hy), (hx, hy + 12)]
      pygame.draw.polygon(surf, HEAVY_RED, points)


def main():
  bg = StreetFoodBackground()
  player = NoodleBowlPlayer()
  objects = []

  score = 0
  max_lives = 5
  lives = 5
  game_over = False

  spawn_timer = 0
  flash_timer = 0

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      player.move("LEFT")
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      player.move("RIGHT")

    if not game_over:
      spawn_timer += 1
      if spawn_timer > 50:
        objects.append(FallingItem(score, objects))
        spawn_timer = 0

      if flash_timer > 0:
        flash_timer -= 1

      for obj in objects[:]:
        obj.fall()

        if (
            player.x <= obj.x <= player.x + player.width
            and player.y <= obj.y + obj.radius
            <= player.y + player.height + obj.radius
        ):
          if obj.is_hazard:
            lives -= 1
            flash_timer = 15
            if lives <= 0:
              game_over = True
          elif obj.is_healing:
            if lives < max_lives:
              lives += 1
            score += 2
          else:
            score += 1
          objects.remove(obj)

        elif obj.y > SCREEN_HEIGHT + obj.radius:
          objects.remove(obj)
          if not obj.is_hazard and not obj.is_healing:
            lives -= 1
            if lives <= 0:
              game_over = True

    bg.draw(screen)

    if flash_timer > 0:
      red_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
      red_overlay.set_alpha(100)
      red_overlay.fill((255, 0, 0))
      screen.blit(red_overlay, (0, 0))

    player.draw(screen)

    for obj in objects:
      obj.draw(screen)

    # Tampilkan UI Skor di Kiri dan 5 Ikon Hati di Kanan Atas
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (15, 15))

    # Render Ikon Hati Nyawa
    for i in range(max_lives):
      heart_x = SCREEN_WIDTH - 25 - (i * 30)
      heart_y = 25
      is_active = i < lives
      draw_heart_icon(screen, heart_x, heart_y, is_active)

    if game_over:
      overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
      overlay.set_alpha(210)
      overlay.fill(BLACK)
      screen.blit(overlay, (0, 0))

      game_over_surf = font_large.render("GAME OVER", True, RED)
      final_score_surf = font_medium.render(
          f"Final Score: {score}", True, WHITE
      )
      restart_surf = font_small.render(
          "Close window to exit.", True, WARM_YELLOW
      )

      screen.blit(
          game_over_surf,
          (SCREEN_WIDTH // 2 - game_over_surf.get_width() // 2, 250),
      )
      screen.blit(
          final_score_surf,
          (SCREEN_WIDTH // 2 - final_score_surf.get_width() // 2, 310),
      )
      screen.blit(
          restart_surf,
          (SCREEN_WIDTH // 2 - restart_surf.get_width() // 2, 360),
      )

    pygame.display.flip()
    clock.tick(FPS)


if __name__ == "__main__":
  main()