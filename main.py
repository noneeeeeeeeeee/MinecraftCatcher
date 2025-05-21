import pygame
import sys
import random

# Initialize Pygame
pygame.init()
try:
    pygame.mixer.init()
    AUDIO_ENABLED = True
except pygame.error:
    print("Audio initialization failed. Continuing without sound.")
    AUDIO_ENABLED = False

pygame.display.set_caption("Minecraft Catcher v3.0")

# Define default volumes globally
MUSIC_VOLUME = 0.1
SFX_VOLUME = 1

if AUDIO_ENABLED:
    pygame.mixer.music.set_volume(MUSIC_VOLUME)

# Load custom font
try:
    CUSTOM_FONT = "./font/Minecraft.ttf"
    FONT = lambda size: pygame.font.Font(CUSTOM_FONT, size)
except FileNotFoundError:
    print("Custom font not found. Falling back to default font.")
    FONT = lambda size: pygame.font.SysFont(None, size)

# ----------------------------
# VARIABLES FOR ASSETS & CONFIG
# ----------------------------

# Music Files
MUSIC_FRENZY = "./sounds/music/Steves Lava Chicken.mp3"
MUSIC_MAIN_MENU = "./sounds/music/Flint and Steel Wonka.mp3"
MUSIC_PLAYING = "./sounds/music/FLINT AND STEEL (Extended Version).mp3"

# Sound Effects
SFX_LAVA_BUCKET = "./sounds/sfx/Lava Bucket.mp3"
SFX_WATER_BUCKET = "./sounds/sfx/Water Bucket.mp3"
SFX_I_AM_STEVE = "./sounds/sfx/I am Steve.mp3"
SFX_STEVE_DROPPING = "./sounds/sfx/Coming in Hot.mp3"
SFX_STEVE_CATCH = "./sounds/sfx/Release.mp3"
SFX_CHICKEN_JOCKEY = "./sounds/sfx/Chicken Jockey.mp3"
SFX_DIAMOND_SWORD_READY = "./sounds/sfx/This is a Sweet Blade.mp3"
SFX_DIAMOND_SWORD_USED = "./sounds/sfx/And this is the only one I had, no biggie.mp3"
SFX_DIAMOND_SWORD_ACTIVATE = "./sounds/sfx/KABOOM.mp3"
SFX_ENDERPEARL_READY = "./sounds/sfx/This is an Ender Pearl.mp3"
SFX_ENDERPEARL_USED = "./sounds/sfx/And this is the only one I had, no biggie.mp3"
SFX_ENDERPEARL_ACTIVATE = "./sounds/sfx/KABOOM.mp3"
SFX_LUCKY_CLAIM = "./sounds/sfx/LuckyBlock.mp3"
SFX_TNT_EXPLODE = "./sounds/sfx/LuckyBlock.mp3"
SFX_ELYTRA_SAVE = "./sounds/sfx/LuckyBlock.mp3"

# Image assets
IMAGE_STEVE_STANDING = pygame.image.load("./img/Steve-Standing.png")
IMAGE_STEVE_FALLING = pygame.image.load("./img/Steve-Falling.png")
IMAGE_CHICKEN = pygame.image.load("./img/Raw-Chicken.png")
IMAGE_COOKED_CHICKEN = pygame.image.load("./img/Cooked-Chicken.png")
IMAGE_LAVA_BUCKET = pygame.image.load("./img/Lava-Bucket.png")
IMAGE_WATER_BUCKET = pygame.image.load("./img/Water-Bucket.png")
IMAGE_CHICKEN_JOCKEY = pygame.image.load("./img/Chicken-Jockey.png")
DIAMOND_SWORD_ICON = pygame.image.load("./img/Diamond-Sword.png")
DIAMOND_SWORD_ICON_GRAY = pygame.image.load("./img/DIamond Sword-Grayscale.png")
ENDER_PEARL_ICON = pygame.image.load("./img/Ender-Pearl.png")
ENDER_PEARL_ICON_GRAY = pygame.image.load("./img/Ender-Pearl-Grayscale.png")
LUCKY_BLOCK = pygame.image.load("./img/Lucky-Block.png")
IMAGE_LUCKY_BLOCK = pygame.image.load("./img/Lucky-Block.png")
IMAGE_BOOTS = pygame.image.load("./img/Sprint_Boots.png")
IMAGE_TNT = pygame.image.load("./img/TNT.png")
IMAGE_ELYTRA = pygame.image.load("./img/Elytra.png")
MAIN_MENU_BG = pygame.image.load("./img/Main_MenuBG.jpg")

# Splash text options
SPLASH_TEXTS = [
    "Catch 'em all!",
    "Steve's adventure awaits!",
    "Buckets of fun!",
    "Don't miss the chickens!",
    "Minecraft-inspired madness!",
    "Clucking good time!",
    "Chicken dinner winner!",
    "Steve needs help!",
    "Falling with style!",
    "Lava or water?",
    "Catch or perish!",
    "Bucket Brigade Champion!",
    "Crafting chicken catchers!",
    "Mob catching madness!",
    "Diamonds are forever!",
    "Actually just chickens!",
    "Ender pearls ready!",
    "Watch for jockeys!",
    "Frenzy mode activated!",
    "High score hunter!"
]

# Asset sizes
STEVE_SIZE = (100, 100)
CHICKEN_SIZE = (50, 50)
LAVA_BUCKET_SIZE = (50, 50)
WATER_BUCKET_SIZE = (55, 55)
DIAMOND_SWORD_SIZE = (50, 50)
DIAMOND_SWORD_STATUS_SIZE = (35, 35)
ENDER_PEARL_STATUS_SIZE = (35, 35)

# Screen parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (50, 150, 50)

LAVA_BUCKET_COLLISION_SIZE = (50, 50)
WATER_BUCKET_COLLISION_SIZE = (50, 50)

# Collision visibility
SHOW_COLLISION = False

# Frenzy Activation
FRENZY_ACTIVATE_STREAK = 15

# Diamond Sword feature
DIAMOND_SWORD_DURATION = 0.5
DIAMOND_SWORD_COOLDOWN = 10.0
diamond_sword_timer = 0
diamond_sword_cooldown = 0

# Ender Pearl feature
ENDER_PEARL_COOLDOWN = 35.0
ender_pearl_timer = 0

# Global settings for Perfect Chicken feature
PERFECT_CHICKEN_SPAWN_CHANCE = 0.25
PERFECT_CHICKEN_STREAK_THRESHOLD = 15
PERFECT_CHICKEN_MULTIPLIER_INCREMENT = 0.5
PERFECT_CHICKEN_MULTIPLIER = 1.0
PERFECT_CHICKEN_STREAK = 0

# Default keybinds
KEYBINDS = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "switch_bucket": pygame.K_w,
    "diamond_sword": pygame.K_q,
    "ender_pearl": pygame.K_e,
    "sprint": pygame.K_LSHIFT,
}

# Ability configuration
ABILITY_BOOT_DURATION = 30.0
ABILITY_TNT_DURATION = 60.0
ABILITY_ELYTRA_DURATION = 60.0
active_ability = None
ability_timer = 0.0

# ----------------------------
# GAME CLASSES AND FUNCTIONS
# ----------------------------


def play_sound(path, volume=1.0):
    # Plays a sound effect from the given file path at the specified volume.
    # Checks if audio is enabled before attempting to play the sound.
    if AUDIO_ENABLED:
        s = pygame.mixer.Sound(path)  # Load the sound file.
        s.set_volume(volume)  # Set the volume for the sound.
        s.play()  # Play the sound.


# Catcher class to represent the player
class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        # Initializes the Catcher object, representing the player-controlled bucket.
        # Sets the default bucket to "lava" and initializes movement and sprinting attributes.
        super().__init__()
        self.equipped = "lava"  # Default bucket type.
        self.image = pygame.transform.scale(IMAGE_LAVA_BUCKET, LAVA_BUCKET_SIZE)  # Bucket image.
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))  # Position on screen.
        self.switch_cooldown = 0  # Cooldown timer for switching buckets.
        self.sprint_timer = 8.0  # Sprint stamina timer.
        self.sprinting = False  # Whether the player is sprinting.
        self.sprint_refill_delay = 0  # Delay before stamina starts refilling.

    def update(self, dt):
        # Updates the Catcher's position, sprinting state, and bucket image based on player input.
        base_speed = 200  # Normal movement speed.
        sprint_speed = base_speed * 2.5  # Sprinting speed.
        speed = sprint_speed if self.sprinting else base_speed  # Determine current speed.

        keys = pygame.key.get_pressed()  # Get the current state of keyboard keys.
        if keys[pygame.K_LSHIFT] and self.sprint_timer > 0:
            # Sprinting logic: reduce stamina while sprinting.
            self.sprinting = True
            self.sprint_timer -= dt
            self.sprint_refill_delay = 0
        else:
            # Stop sprinting and refill stamina over time.
            self.sprinting = False
            if self.sprint_timer <= 0:
                self.sprint_refill_delay += dt
                if self.sprint_refill_delay >= 0.5:
                    self.sprint_timer = min(self.sprint_timer + dt * 1.5, 5.0)
            else:
                self.sprint_refill_delay += dt
                if self.sprint_refill_delay >= 0.2:
                    self.sprint_timer = min(self.sprint_timer + dt * 1.5, 5.0)

        # Movement logic: move left or right based on key input.
        if keys[KEYBINDS["left"]]:
            self.rect.x -= speed * dt
        if keys[KEYBINDS["right"]]:
            self.rect.x += speed * dt

        # Prevent the Catcher from moving outside the screen boundaries.
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Handle bucket switching cooldown.
        if self.switch_cooldown > 0:
            self.switch_cooldown -= dt

        # Update the bucket image based on the equipped bucket type.
        if self.equipped == "lava":
            self.image = pygame.transform.scale(IMAGE_LAVA_BUCKET, LAVA_BUCKET_SIZE)
            self.rect.size = LAVA_BUCKET_COLLISION_SIZE
        elif self.equipped == "water":
            self.image = pygame.transform.scale(IMAGE_WATER_BUCKET, WATER_BUCKET_SIZE)
            self.rect.size = WATER_BUCKET_COLLISION_SIZE
        elif self.equipped == "sword":
            self.image = pygame.transform.scale(DIAMOND_SWORD_ICON, DIAMOND_SWORD_SIZE)

    def switch_bucket(self):
        # Switches between "lava" and "water" buckets, with a cooldown to prevent rapid switching.
        if self.switch_cooldown <= 0:
            if self.equipped == "lava":
                self.equipped = "water"
                play_sound(SFX_WATER_BUCKET, SFX_VOLUME)  # Play water bucket sound.
            else:
                self.equipped = "lava"
                play_sound(SFX_LAVA_BUCKET, SFX_VOLUME)  # Play lava bucket sound.
            self.switch_cooldown = 0.5  # Set cooldown duration.


# Falling object – can be a chicken drop
class Chicken(pygame.sprite.Sprite):
    def __init__(self):
        # Initializes a falling chicken object with random position and speed.
        super().__init__()
        self.image = pygame.transform.scale(IMAGE_CHICKEN, CHICKEN_SIZE)  # Chicken image.
        self.rect = self.image.get_rect(midtop=(random.randint(50, SCREEN_WIDTH - 50), -50))  # Random spawn position.
        self.base_speed = 200  # Base falling speed.
        self.speed = self.base_speed * (1.5 if random.uniform(0, 1) < 0.2 else 1)  # Random speed multiplier.

    def update(self, dt):
        # Updates the chicken's position, making it fall down the screen.
        self.rect.y += self.speed * dt


class CookedChicken(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(IMAGE_COOKED_CHICKEN, CHICKEN_SIZE)
        self.rect = self.image.get_rect(
            midtop=(random.randint(50, SCREEN_WIDTH - 50), -50)
        )
        self.base_speed = 200
        self.speed = self.base_speed

    def update(self, dt):
        self.rect.y += self.speed * dt


class ChickenJockey(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        scale = random.uniform(1.7, 2.0)
        w = int(CHICKEN_SIZE[0] * scale)
        h = int(CHICKEN_SIZE[1] * scale)
        self.image = pygame.transform.scale(IMAGE_CHICKEN_JOCKEY, (w, h))
        self.rect = self.image.get_rect(
            midtop=(random.randint(50, SCREEN_WIDTH - 50), -50)
        )
        self.speed = 200 * scale

    def update(self, dt):
        self.rect.y += self.speed * dt


# Steve character
class Steve(pygame.sprite.Sprite):
    def __init__(self):
        # Initializes the Steve character, which moves horizontally and occasionally drops.
        super().__init__()
        self.image = pygame.transform.scale(IMAGE_STEVE_STANDING, STEVE_SIZE)  # Steve's standing image.
        self.rect = self.image.get_rect(midtop=(SCREEN_WIDTH // 2, 10))  # Initial position.
        self.direction = 1  # Movement direction (1 = right, -1 = left).
        self.move_speed = random.uniform(140, 200)  # Random horizontal speed.
        self.drop_chance = 5  # Initial chance of dropping.
        self.talk_timer = random.uniform(15, 30)  # Timer for Steve to "talk."
        self.drop_timer = random.uniform(10, 15)  # Timer for Steve to drop.
        self.is_dropping = False  # Whether Steve is currently dropping.

    def update(self, dt):
        # Updates Steve's position, drop logic, and "talking" behavior.
        if not self.is_dropping:
            # Move horizontally and bounce off screen edges.
            self.rect.x += self.direction * self.move_speed * dt
            if self.rect.left < 0:
                self.rect.left = 0
                self.direction = 1
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                self.direction = -1

            # Handle "talking" timer.
            self.talk_timer -= dt
            if self.talk_timer <= 0:
                play_sound(SFX_I_AM_STEVE, SFX_VOLUME)  # Play Steve's voice line.
                self.drop_chance += 30  # Increase drop chance.
                self.talk_timer = random.uniform(15, 30)  # Reset timer.

            # Handle drop timer.
            self.drop_timer -= dt
            if self.drop_timer <= 0:
                roll = random.uniform(0, 100)  # Random chance roll.
                if roll < self.drop_chance:
                    self.drop()  # Trigger drop.
                else:
                    self.drop_chance += 15  # Increase drop chance.
                self.drop_timer = random.uniform(10, 15)  # Reset timer.
        else:
            # If Steve is dropping, move him downward.
            self.rect.y += self.move_speed * random.uniform(1.4, 2.0) * dt

    def drop(self):
        # Initiates Steve's dropping behavior.
        self.is_dropping = True
        self.image = pygame.transform.scale(IMAGE_STEVE_FALLING, STEVE_SIZE)  # Change to falling image.
        play_sound(SFX_STEVE_DROPPING, SFX_VOLUME)  # Play dropping sound.

    def reset_after_drop(self):
        # Resets Steve's state after he has dropped.
        self.is_dropping = False
        self.image = pygame.transform.scale(IMAGE_STEVE_STANDING, STEVE_SIZE)  # Reset to standing image.
        self.rect.y = 10  # Reset position.
        self.drop_chance = 5  # Reset drop chance.


# Lucky block sprite
class LuckyBlock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(IMAGE_LUCKY_BLOCK, CHICKEN_SIZE)
        self.rect = self.image.get_rect(
            midtop=(random.randint(50, SCREEN_WIDTH - 50), -50)
        )
        self.speed = random.randint(300, 800)

    def update(self, dt):
        self.rect.y += self.speed * dt


# UI Drawing Functions
score_feed = []


def draw_ui(
    screen,
    score,
    lives,
    frenzy_multi,
    steve_multi,
    frenzy_active,
    frenzy_timer,
    frenzy_cooldown,
    streak,
    frenzy_chicken_count,
    steve_multiplier_timer,
    catcher,
):
    """
    Draws the game's user interface (UI) elements on the screen.

    Parameters:
    - screen: The Pygame surface where the UI will be drawn.
    - score: The player's current score.
    - lives: The player's remaining lives.
    - frenzy_multi: The current frenzy multiplier.
    - steve_multi: The current multiplier for catching Steve.
    - frenzy_active: Boolean indicating if frenzy mode is active.
    - frenzy_timer: Remaining time for frenzy mode.
    - frenzy_cooldown: Cooldown time before frenzy can be activated again.
    - streak: Current streak of successful catches.
    - frenzy_chicken_count: Number of chickens caught during frenzy mode.
    - steve_multiplier_timer: Remaining time for Steve's multiplier effect.
    - catcher: The Catcher object, used to display sprint-related UI.
    """
    font = FONT(30)  # Font for rendering text.
    
    # Display the current score.
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display active effects (e.g., multipliers).
    active_effects = []
    if steve_multiplier_timer > 0:
        active_effects.append(f"x{steve_multi:.1f} ({int(steve_multiplier_timer)}s)")
    if frenzy_active:
        active_effects.append(f"x{frenzy_multi:.1f}")
    if PERFECT_CHICKEN_MULTIPLIER > 1.0:
        active_effects.append(f"x{PERFECT_CHICKEN_MULTIPLIER:.1f}")

    active_effects_text = "Active Effects: " + ", ".join(active_effects)
    effects_font = FONT(30)
    effects_render = effects_font.render(active_effects_text, True, WHITE)
    screen.blit(effects_render, (10, 40))

    # Display the score feed (recent score changes).
    feed_y = 100
    current_time = pygame.time.get_ticks()
    global score_feed
    score_feed = [feed for feed in score_feed if current_time - feed[1] < 1000]  # Keep only recent entries.
    for feed, _ in score_feed[-5:]:  # Display the last 5 entries.
        feed_text = font.render(feed, True, WHITE)
        screen.blit(feed_text, (10, feed_y))
        feed_y += 20

    # Draw the frenzy bar (progress or cooldown).
    frenzy_bar_width = 200
    frenzy_bar_height = 20
    bar_x = SCREEN_WIDTH - frenzy_bar_width - 30
    bar_y = 10
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, frenzy_bar_width, frenzy_bar_height), 2)  # Bar outline.

    if frenzy_active:
        # Show remaining frenzy time as a red bar.
        inner_width = int(frenzy_bar_width * (frenzy_timer / 20))
        counter_text = f"{int(frenzy_timer)}s"
    elif frenzy_cooldown > 0:
        # Show cooldown progress as a red bar.
        inner_width = int(frenzy_bar_width * (1 - frenzy_cooldown / 60))
        counter_text = f"{int(frenzy_cooldown)}s"
    else:
        # Show streak progress toward activating frenzy.
        inner_width = int(frenzy_bar_width * min(streak / FRENZY_ACTIVATE_STREAK, 1.0))
        counter_text = f"{streak}"

    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, inner_width, frenzy_bar_height))  # Fill the bar.

    # Display the counter text next to the frenzy bar.
    counter_font = FONT(30)
    counter_render = counter_font.render(counter_text, True, WHITE)
    screen.blit(counter_render, (bar_x + frenzy_bar_width + 10, bar_y))

    # Display the player's remaining lives.
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 150, bar_y + frenzy_bar_height + 10))

    # Draw the sprint bar (stamina).
    sprint_bar_width = 200
    sprint_bar_height = 20
    sprint_bar_x = SCREEN_WIDTH - sprint_bar_width - 10
    sprint_bar_y = SCREEN_HEIGHT - sprint_bar_height - 10
    pygame.draw.rect(screen, WHITE, (sprint_bar_x, sprint_bar_y, sprint_bar_width, sprint_bar_height), 2)  # Outline.

    # Fill the sprint bar based on the Catcher's remaining stamina.
    sprint_inner_width = int(sprint_bar_width * (catcher.sprint_timer / 5.0))
    pygame.draw.rect(screen, (0, 0, 255), (sprint_bar_x, sprint_bar_y, sprint_inner_width, sprint_bar_height))

    # Display the Diamond Sword icon and cooldown.
    scaled_icon = pygame.transform.scale(DIAMOND_SWORD_ICON, DIAMOND_SWORD_STATUS_SIZE)
    scaled_icon_gray = pygame.transform.scale(DIAMOND_SWORD_ICON_GRAY, DIAMOND_SWORD_STATUS_SIZE)
    icon_pos = (10, SCREEN_HEIGHT - DIAMOND_SWORD_STATUS_SIZE[1] - 10)
    if diamond_sword_cooldown <= 0 and diamond_sword_timer <= 0:
        screen.blit(scaled_icon, icon_pos)  # Active icon.
    else:
        screen.blit(scaled_icon_gray, icon_pos)  # Grayed-out icon.
        cd = int(diamond_sword_cooldown) if diamond_sword_cooldown > 0 else int(diamond_sword_timer)
        cd_text = counter_font.render(f"{cd}s", True, WHITE)
        screen.blit(cd_text, (icon_pos[0] + DIAMOND_SWORD_STATUS_SIZE[0] + 5, icon_pos[1]))

    # Display the Ender Pearl icon and cooldown.
    ender_icon_pos = (icon_pos[0] + ENDER_PEARL_STATUS_SIZE[0] + 15, icon_pos[1])
    if ender_pearl_timer <= 0:
        ender_icon = pygame.transform.scale(ENDER_PEARL_ICON, ENDER_PEARL_STATUS_SIZE)
        screen.blit(ender_icon, ender_icon_pos)  # Active icon.
    else:
        ender_icon_gray = pygame.transform.scale(ENDER_PEARL_ICON_GRAY, ENDER_PEARL_STATUS_SIZE)
        screen.blit(ender_icon_gray, ender_icon_pos)  # Grayed-out icon.
        cd_text2 = counter_font.render(f"{int(ender_pearl_timer)}s", True, WHITE)
        screen.blit(cd_text2, (ender_icon_pos[0] + ENDER_PEARL_STATUS_SIZE[0] + 5, ender_icon_pos[1]))

    # Display the active ability icon and timer (if any).
    if active_ability:
        iconsize = 35
        if active_ability == "boots":
            icon = pygame.transform.scale(IMAGE_BOOTS, (iconsize, iconsize))
        elif active_ability == "tnt":
            icon = pygame.transform.scale(IMAGE_TNT, (iconsize, iconsize))
        else:
            icon = pygame.transform.scale(IMAGE_ELYTRA, (iconsize, iconsize))
        xpos = SCREEN_WIDTH - 150
        ypos = 70
        screen.blit(icon, (xpos, ypos))  # Display the ability icon.
        timer_text = FONT(20).render(f"{int(ability_timer)}s", True, WHITE)
        screen.blit(timer_text, (xpos + iconsize + 5, ypos))  # Display the remaining time for the ability.


# Main menu screen
def main_menu(screen):
    # Displays the main menu, allowing the player to start the game, view instructions, or adjust settings.
    # Handles button interactions and settings adjustments.
    global SFX_VOLUME  # Declare SFX_VOLUME as global
    clock = pygame.time.Clock()
    font = FONT(60)
    small_font = FONT(30)
    splash_base_font_size = 20  
    splash_font = lambda size: FONT(size)

    if AUDIO_ENABLED:
        pygame.mixer.music.load(MUSIC_MAIN_MENU)
        pygame.mixer.music.play(-1)

    # Random splash text
    splash_text = random.choice(SPLASH_TEXTS)

    # Scale the background image proportionally
    bg_width, bg_height = MAIN_MENU_BG.get_size()
    scale_factor = max(SCREEN_WIDTH / bg_width, SCREEN_HEIGHT / bg_height)
    scaled_bg = pygame.transform.scale(
        MAIN_MENU_BG, (int(bg_width * scale_factor), int(bg_height * scale_factor))
    )

    play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    info_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
    settings_button = pygame.Rect(
        SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 140, 200, 50
    )

    settings_margin = 50
    back_button = pygame.Rect(settings_margin, SCREEN_HEIGHT - 100, 100, 50)
    scroll_offset = 0
    scroll_speed = 20

    slider_width = 200
    slider_height = 10
    music_slider = pygame.Rect(settings_margin + 100, 150, slider_width, slider_height)
    sfx_slider = pygame.Rect(settings_margin + 100, 250, slider_width, slider_height)

    keybinds_rects = {
        "left": pygame.Rect(settings_margin + 115, 365, 50, 30),
        "right": pygame.Rect(settings_margin + 115, 415, 50, 30),
        "switch_bucket": pygame.Rect(settings_margin + 115, 465, 50, 30),
        "sprint": pygame.Rect(settings_margin + 315, 465, 50, 30),
        "diamond_sword": pygame.Rect(settings_margin + 315, 365, 50, 30),
        "ender_pearl": pygame.Rect(settings_margin + 315, 415, 50, 30),
    }

    keybind_labels = {
        "left": "Move Left",
        "right": "Move Right",
        "switch_bucket": "Switch Bucket",
        "sprint": "Sprint",
        "diamond_sword": "Diamond Sword",
        "ender_pearl": "Ender Pearl",
    }

    show_instructions = False
    show_settings = False
    music_volume = MUSIC_VOLUME
    sfx_volume = SFX_VOLUME
    active_keybind = None

    # Variables for splash text pulsing animation
    pulse_direction = 2 
    pulse_speed = 0.3  
    splash_font_size = splash_base_font_size

    while True:
        screen.blit(scaled_bg, (0, 0))

        # Title
        title_text = font.render("Minecraft Catcher", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Splash text with pulsing animation
        splash_font_size += pulse_direction * pulse_speed
        if splash_font_size >= splash_base_font_size + 5:
            pulse_direction = -1
        elif splash_font_size <= splash_base_font_size:
            pulse_direction = 1

        splash_render = splash_font(int(splash_font_size)).render(
            splash_text, True, (255, 255, 0)
        )
        splash_render = pygame.transform.rotate(splash_render, 40)  # Tilted text
        splash_x = SCREEN_WIDTH // 2 + title_text.get_width() // 2 - 100
        splash_y = 65
        screen.blit(splash_render, (splash_x, splash_y))

        # Buttons
        pygame.draw.rect(screen, BLACK, play_button)
        play_text = small_font.render("Play", True, WHITE)
        screen.blit(
            play_text,
            (
                play_button.centerx - play_text.get_width() // 2,
                play_button.centery - play_text.get_height() // 2,
            ),
        )

        pygame.draw.rect(screen, BLACK, info_button)
        info_text = small_font.render("How to Play", True, WHITE)
        screen.blit(
            info_text,
            (
                info_button.centerx - info_text.get_width() // 2,
                info_button.centery - info_text.get_height() // 2,
            ),
        )

        pygame.draw.rect(screen, BLACK, settings_button)
        settings_text = small_font.render("Settings", True, WHITE)
        screen.blit(
            settings_text,
            (
                settings_button.centerx - settings_text.get_width() // 2,
                settings_button.centery - settings_text.get_height() // 2,
            ),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [4, 5]:
                    if show_instructions:
                        if event.button == 4:
                            scroll_offset = max(scroll_offset - scroll_speed, 0)
                        elif event.button == 5:
                            max_scroll = max(
                                0,
                                120
                                + len(instructions_text) * 30
                                - (SCREEN_HEIGHT - 200),
                            )
                            scroll_offset = min(
                                scroll_offset + scroll_speed, max_scroll
                            )
                    continue
                if show_instructions:
                    if back_button.collidepoint(event.pos):
                        show_instructions = False

                elif show_settings:
                    if back_button.collidepoint(event.pos):
                        show_settings = False
                        active_keybind = None
                        scroll_offset = 0
                    elif AUDIO_ENABLED and music_slider.collidepoint(event.pos):
                        music_volume = (event.pos[0] - music_slider.x) / slider_width
                        music_volume = max(0.0, min(1.0, music_volume))
                        pygame.mixer.music.set_volume(music_volume)
                    elif AUDIO_ENABLED and sfx_slider.collidepoint(event.pos):
                        sfx_volume = (event.pos[0] - sfx_slider.x) / slider_width
                        sfx_volume = max(0.0, min(1.0, sfx_volume))
                        SFX_VOLUME = sfx_volume 
                    else:
                        for action, rect in keybinds_rects.items():
                            if rect.collidepoint(event.pos):
                                active_keybind = action
                                break

                else:
                    if play_button.collidepoint(event.pos):
                        return
                    if info_button.collidepoint(event.pos):
                        show_instructions = True
                    if settings_button.collidepoint(event.pos):
                        show_settings = True

            if event.type == pygame.KEYDOWN and active_keybind:
                KEYBINDS[active_keybind] = event.key
                active_keybind = None

        if show_settings:
            settings_surf = pygame.Surface(
                (
                    SCREEN_WIDTH - 2 * settings_margin,
                    SCREEN_HEIGHT - 2 * settings_margin,
                )
            )
            settings_surf.set_alpha(230)
            settings_surf.fill((30, 30, 30))
            screen.blit(settings_surf, (settings_margin, settings_margin))

            sounds_label = small_font.render("Sounds", True, WHITE)
            screen.blit(sounds_label, (settings_margin + 50, 110))
            keybinds_label = small_font.render("Keybinds", True, WHITE)
            screen.blit(keybinds_label, (settings_margin + 50, 310))

            if AUDIO_ENABLED:
                pygame.draw.rect(screen, WHITE, music_slider)
                music_knob_x = music_slider.x + int(music_volume * slider_width)
                pygame.draw.circle(
                    screen, BLACK, (music_knob_x, music_slider.centery), 10
                )
                music_text = small_font.render("Music Volume", True, WHITE)
                screen.blit(music_text, (settings_margin + 50, music_slider.y - 20))

                pygame.draw.rect(screen, WHITE, sfx_slider)
                sfx_knob_x = sfx_slider.x + int(sfx_volume * slider_width)
                pygame.draw.circle(screen, BLACK, (sfx_knob_x, sfx_slider.centery), 10)
                sfx_text = small_font.render("SFX Volume", True, WHITE)
                screen.blit(sfx_text, (settings_margin + 50, sfx_slider.y - 20))
            else:
                audio_disabled_text = small_font.render(
                    "Audio is disabled", True, WHITE
                )
                screen.blit(audio_disabled_text, (settings_margin + 50, 150))

            for action, rect in keybinds_rects.items():
                action_text = small_font.render(keybind_labels[action], True, WHITE)
                key_text = small_font.render(
                    pygame.key.name(KEYBINDS[action]), True, BLACK
                )
                screen.blit(action_text, (rect.x - 90, rect.y + 5))
                pygame.draw.rect(screen, WHITE, rect)
                screen.blit(key_text, (rect.x + 5, rect.y + 5))

            pygame.draw.rect(screen, BLACK, back_button)
            back_text = small_font.render("Back", True, WHITE)
            screen.blit(
                back_text,
                (
                    back_button.centerx - back_text.get_width() // 2,
                    back_button.centery - back_text.get_height() // 2,
                ),
            )

        if show_instructions:
            instructions_surf = pygame.Surface(
                (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
            )
            instructions_surf.set_alpha(230)
            instructions_surf.fill((30, 30, 30))
            screen.blit(instructions_surf, (50, 50))

            instructions_font = FONT(30)
            instructions_title_font = FONT(40)

            # Title
            title_text = instructions_title_font.render("How to Play", True, WHITE)
            screen.blit(
                title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 70)
            )

            # Instructions
            instructions_text = [
                "Controls:",
                "- Use 'A' and 'D' to move left and right.",
                "- Press 'W' to switch between Lava and Water buckets.",
                "- Press 'Q' to activate the Diamond Sword.",
                "- Press 'E' to use the Ender Pearl.",
                "- Hold 'Shift' to sprint (limited stamina).",
                "",
                "Gameplay:",
                "- Catch falling items with the correct bucket.",
                "- Lava bucket catches raw chickens.",
                "- Water bucket catches Steve when he falls.",
                "- Avoid missing items or catching with the wrong bucket.",
                "- Use the Diamond Sword to defeat Chicken Jockeys.",
                "- Use the Ender Pearl to teleport to the center of the screen.",
                "- Catch Lucky Blocks to gain special abilities.",
                "",
                "Scoring:",
                "- Catching items correctly increases your score.",
                "- Missing items or using the wrong bucket decreases your score.",
                "- Catching Steve grants a large score bonus.",
                "- Perfect Chicken streaks increase your multiplier.",
                "",
                "Tips:",
                "- Keep an eye on your sprint bar to move faster when needed.",
                "- Use the Diamond Sword and Ender Pearl strategically.",
                "- Watch out for Chicken Jockeys—they're dangerous!",
                "- Lucky Block abilities can turn the tide of the game!",
            ]

            scroll_area = pygame.Rect(70, 120, SCREEN_WIDTH - 140, SCREEN_HEIGHT - 200)
            pygame.draw.rect(screen, BG_COLOR, scroll_area)
            clip_surface = pygame.Surface(scroll_area.size)
            clip_surface.set_colorkey(BG_COLOR)
            clip_surface.fill(BG_COLOR)
            screen.set_clip(scroll_area)

            y_offset = 120 - scroll_offset
            for line in instructions_text:
                text_render = instructions_font.render(line, True, WHITE)
                screen.blit(text_render, (70, y_offset))
                y_offset += 30

            screen.set_clip(None)

            pygame.draw.rect(screen, BLACK, back_button)
            back_text = small_font.render("Back", True, WHITE)
            screen.blit(
                back_text,
                (
                    back_button.centerx - back_text.get_width() // 2,
                    back_button.centery - back_text.get_height() // 2,
                ),
            )

        pygame.display.update()
        clock.tick(FPS)


# ----------------------------
# MAIN GAME LOOP
# ----------------------------
def game_loop(screen):
    # The main game loop where gameplay occurs.
    # Handles spawning, collisions, scoring, and updating all game objects.
    clock = pygame.time.Clock()
    if AUDIO_ENABLED:
        pygame.mixer.music.load(MUSIC_PLAYING)
        pygame.mixer.music.play(-1)

    catcher = Catcher()
    catcher_group = pygame.sprite.GroupSingle(catcher)
    chicken_group = pygame.sprite.Group()
    steve = Steve()
    steve_group = pygame.sprite.GroupSingle(steve)
    jockey_group = pygame.sprite.Group()
    lucky_group = pygame.sprite.Group()

    score = 0
    lives = 5
    frenzy_multi = 1.0
    steve_multi = 1.0
    frenzy_active = False
    frenzy_timer = 0
    frenzy_cooldown = 0
    frenzy_chicken_count = 0
    streak = 0

    chicken_spawn_timer = 0
    spawn_interval = 1.0

    steve_multiplier_timer = 0

    jockey_spawn_timer = 0
    jockey_spawn_interval = random.uniform(25, 45)
    jockey_spawn_chance = 15

    lucky_spawn_timer = 0.0

    global diamond_sword_timer, diamond_sword_cooldown, ender_pearl_timer, active_ability, ability_timer

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        # Update ability timer
        if active_ability:
            ability_timer -= dt
            if ability_timer <= 0:
                active_ability = None

        # Enforce sprint boots infinite stamina
        if active_ability == "boots":
            catcher.sprint_timer = 5.0

        # Update diamond sword timer
        if diamond_sword_timer > 0:
            diamond_sword_timer -= dt
            if diamond_sword_timer <= 0:
                catcher.equipped = "lava"
                diamond_sword_cooldown = DIAMOND_SWORD_COOLDOWN
                play_sound(SFX_DIAMOND_SWORD_USED, SFX_VOLUME)
        elif diamond_sword_cooldown > 0:
            diamond_sword_cooldown -= dt
            if diamond_sword_cooldown <= 0:
                play_sound(SFX_DIAMOND_SWORD_READY, SFX_VOLUME)

        # Update ender pearl timer
        if ender_pearl_timer > 0:
            ender_pearl_timer -= dt
            if ender_pearl_timer <= 0:
                play_sound(SFX_ENDERPEARL_READY, SFX_VOLUME)

        # Spawn logic for Lucky Block
        lucky_spawn_timer += dt
        if lucky_spawn_timer >= spawn_interval and not active_ability:
            lucky_spawn_timer = 0
            if random.randint(1, 25) == 1:
                lucky_group.add(LuckyBlock())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == KEYBINDS["diamond_sword"]
                    and diamond_sword_cooldown <= 0
                ):
                    diamond_sword_timer = DIAMOND_SWORD_DURATION
                    catcher.equipped = "sword"
                    play_sound(SFX_DIAMOND_SWORD_ACTIVATE, SFX_VOLUME)
                if event.key == KEYBINDS["switch_bucket"]:
                    catcher.switch_bucket()
                if event.key == KEYBINDS["ender_pearl"] and ender_pearl_timer <= 0:
                    rel_x = catcher.rect.centerx - SCREEN_WIDTH / 2
                    new_center = SCREEN_WIDTH / 2 - rel_x
                    catcher.rect.centerx = new_center
                    play_sound(SFX_ENDERPEARL_ACTIVATE, SFX_VOLUME)
                    ender_pearl_timer = ENDER_PEARL_COOLDOWN
                    play_sound(SFX_ENDERPEARL_USED, SFX_VOLUME)

        # Jockey spawn logic
        jockey_spawn_timer += dt
        if jockey_spawn_timer >= jockey_spawn_interval:
            if random.uniform(0, 100) < jockey_spawn_chance:
                play_sound(SFX_CHICKEN_JOCKEY, SFX_VOLUME)
                jockey_group.add(ChickenJockey())
                jockey_spawn_timer = 0
                jockey_spawn_interval = random.uniform(10, 20)
                jockey_spawn_chance = 15
            else:
                jockey_spawn_chance = min(jockey_spawn_chance + 35, 100)
                jockey_spawn_timer = 0
                jockey_spawn_interval = random.uniform(10, 20)

        chicken_spawn_timer += dt
        if chicken_spawn_timer >= spawn_interval:
            chicken_spawn_timer = 0
            if not frenzy_active:
                if random.random() < PERFECT_CHICKEN_SPAWN_CHANCE:
                    chicken_group.add(CookedChicken())
                else:
                    chicken_group.add(Chicken())
            else:
                # During frenzy, spawn chickens with varied speeds
                for _ in range(random.randint(15, 500)):
                    speed_multiplier = random.uniform(0.8, 3) 
                    
                    if random.random() < PERFECT_CHICKEN_SPAWN_CHANCE:
                        chicken = CookedChicken()
                        chicken.speed = chicken.base_speed * speed_multiplier
                    else:
                        chicken = Chicken()
                        chicken.speed = chicken.base_speed * speed_multiplier
                    
                    chicken.rect.x = random.randint(20, SCREEN_WIDTH - 70)
                    chicken_group.add(chicken)

        catcher_group.update(dt)
        chicken_group.update(dt)
        steve_group.update(dt)
        jockey_group.update(dt)
        lucky_group.update(dt)

        # Collision: Lucky Block catch
        for lb in lucky_group:
            if catcher.rect.colliderect(lb.rect):
                choice = random.choice(["boots", "tnt", "elytra"])
                active_ability = choice
                if choice == "boots":
                    ability_timer = ABILITY_BOOT_DURATION
                elif choice == "tnt":
                    ability_timer = ABILITY_TNT_DURATION
                elif choice == "elytra":
                    ability_timer = ABILITY_ELYTRA_DURATION
                play_sound(SFX_LUCKY_CLAIM, SFX_VOLUME)
                lucky_group.empty()

        # Collision: Chicken
        for chicken in chicken_group:
            if catcher.rect.colliderect(chicken.rect):
                if isinstance(chicken, CookedChicken):
                    global PERFECT_CHICKEN_STREAK, PERFECT_CHICKEN_MULTIPLIER
                    PERFECT_CHICKEN_STREAK = 0
                    PERFECT_CHICKEN_MULTIPLIER = 1.0
                    score_feed.append(
                        ("Perfect Chicken Streak Reset", pygame.time.get_ticks())
                    )
                else:
                    if catcher.equipped == "lava":
                        if frenzy_active:
                            points = int(
                                2
                                * frenzy_multi
                                * steve_multi
                                * PERFECT_CHICKEN_MULTIPLIER
                            )
                            score_feed.append(
                                (f"+{points} (Frenzy)", pygame.time.get_ticks())
                            )
                        else:
                            points = int(2 * steve_multi * PERFECT_CHICKEN_MULTIPLIER)
                            score_feed.append((f"+{points}", pygame.time.get_ticks()))
                        score += points
                        streak += 1
                        frenzy_chicken_count += 1
                    else:
                        if not frenzy_active:
                            score_feed.append(
                                ("-5 (Wrong Bucket)", pygame.time.get_ticks())
                            )
                            score -= 5
                            streak = 0
                chicken.kill()

        # Collision: Chicken missed
        for chicken in chicken_group:
            if chicken.rect.top >= SCREEN_HEIGHT:
                if isinstance(chicken, CookedChicken):
                    PERFECT_CHICKEN_STREAK += 1
                    score_feed.append(
                        (
                            f"Perfect Chicken Streak: {PERFECT_CHICKEN_STREAK}",
                            pygame.time.get_ticks(),
                        )
                    )
                    if PERFECT_CHICKEN_STREAK % PERFECT_CHICKEN_STREAK_THRESHOLD == 0:
                        PERFECT_CHICKEN_MULTIPLIER += (
                            PERFECT_CHICKEN_MULTIPLIER_INCREMENT
                        )
                    chicken.kill()
                else:
                    if not frenzy_active:
                        score_feed.append(("-2 (Missed)", pygame.time.get_ticks()))
                        score -= 2
                        streak = 0
                    chicken.kill()

        # Frenzy activation
        if (
            not frenzy_active
            and streak >= FRENZY_ACTIVATE_STREAK
            and frenzy_cooldown <= 0
        ):
            frenzy_active = True
            frenzy_timer = 20
            frenzy_multi = 5.0
            frenzy_chicken_count = 0
            if AUDIO_ENABLED:
                pygame.mixer.music.load(MUSIC_FRENZY)
                pygame.mixer.music.play(-1)
            streak = 0

        # Frenzy timer
        if frenzy_active:
            frenzy_timer -= dt
            frenzy_multi = max(1.5, 5.0 - (frenzy_chicken_count // 10) * 0.5)
            if frenzy_timer <= 0:
                frenzy_active = False
                frenzy_cooldown = 60
                frenzy_multi = 1.0
                if AUDIO_ENABLED:
                    pygame.mixer.music.load(MUSIC_PLAYING)
                    pygame.mixer.music.play(-1)

        if frenzy_cooldown > 0:
            frenzy_cooldown -= dt

        # Steve dropping
        if steve.is_dropping:
            if catcher.rect.colliderect(steve.rect):
                if catcher.equipped == "water":
                    play_sound(SFX_STEVE_CATCH, SFX_VOLUME)
                    score += int(100 * frenzy_multi * steve_multi)
                    steve_multi = 5.0
                    steve_multiplier_timer = 30
                    score_feed.append(("+100 (Steve Caught)", pygame.time.get_ticks()))
                    score += 100
                    steve.reset_after_drop()
                else:
                    score_feed.append(("-500 (Wrong Bucket)", pygame.time.get_ticks()))
                    score -= 500
                    lives -= 1
                    steve.reset_after_drop()
            elif steve.rect.top > SCREEN_HEIGHT:
                if active_ability == "elytra":
                    play_sound(SFX_ELYTRA_SAVE, SFX_VOLUME)
                    active_ability = None
                    steve.reset_after_drop()
                else:
                    score_feed.append(("-500 (Missed Steve)", pygame.time.get_ticks()))
                    score -= 500
                    lives -= 1
                    steve.reset_after_drop()

        # Jockey collision
        for jockey in jockey_group:
            if jockey.rect.top >= SCREEN_HEIGHT:
                if active_ability == "tnt":
                    play_sound(SFX_TNT_EXPLODE, SFX_VOLUME)
                    # Award points for all chickens
                    pts = len(chicken_group) * 2
                    score += pts
                    chicken_group.empty()
                    active_ability = None
                else:
                    lives -= 3
                jockey.kill()
            elif catcher.rect.colliderect(jockey.rect):
                if active_ability == "tnt":
                    play_sound(SFX_TNT_EXPLODE, SFX_VOLUME)
                    # Award points for all chickens
                    pts = len(chicken_group) * 2
                    score += pts
                    chicken_group.empty()
                    active_ability = None
                elif catcher.equipped == "lava":
                    score -= 1000
                    lives -= 1
                    score_feed.append(
                        ("-1000 (Jockey Missed)", pygame.time.get_ticks())
                    )
                    jockey.kill()
                elif catcher.equipped == "water":
                    lives -= 3
                    jockey.kill()
                elif catcher.equipped == "sword":
                    score += 500
                    score_feed.append(("+500 (Jockey Killed)", pygame.time.get_ticks()))
                    jockey.kill()

        # Steve multiplier timer
        if steve_multiplier_timer > 0:
            steve_multiplier_timer -= dt
        else:
            steve_multi = 1.0

        # Draw everything
        screen.fill(BG_COLOR)
        chicken_group.draw(screen)
        catcher_group.draw(screen)
        steve_group.draw(screen)
        jockey_group.draw(screen)
        lucky_group.draw(screen)
        draw_ui(
            screen,
            score,
            lives,
            frenzy_multi,
            steve_multi,
            frenzy_active,
            frenzy_timer,
            frenzy_cooldown,
            streak,
            frenzy_chicken_count,
            steve_multiplier_timer,
            catcher,
        )

        if SHOW_COLLISION:
            pygame.draw.rect(screen, (0, 255, 0), catcher.rect, 2)
            for chicken in chicken_group:
                pygame.draw.rect(screen, (255, 0, 0), chicken.rect, 2)
            for jockey in jockey_group:
                pygame.draw.rect(screen, (255, 0, 0), jockey.rect, 2)

        pygame.display.update()

        if lives <= 0:
            end_screen(screen, score)
            return


def end_screen(screen, score):
    # Displays the game over screen with the player's final score.
    # Allows the player to return to the main menu.
    clock = pygame.time.Clock()
    font = FONT(60)
    small_font = FONT(30)
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    while True:
        screen.fill(BG_COLOR)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Your Score: {score}", True, WHITE)
        screen.blit(
            game_over_text,
            (
                SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - 100,
            ),
        )
        screen.blit(
            score_text,
            (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20),
        )
        pygame.draw.rect(screen, BLACK, button_rect)
        button_text = small_font.render("Main Menu", True, WHITE)
        screen.blit(
            button_text,
            (
                button_rect.centerx - button_text.get_width() // 2,
                button_rect.centery - button_text.get_height() // 2,
            ),
        )
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return
        clock.tick(FPS)


def reset_globals():
    # Resets global variables to their initial states for a new game session.
    global diamond_sword_timer, diamond_sword_cooldown, PERFECT_CHICKEN_STREAK, PERFECT_CHICKEN_MULTIPLIER, score_feed, ender_pearl_timer, active_ability, ability_timer
    diamond_sword_timer = 0
    diamond_sword_cooldown = 0
    PERFECT_CHICKEN_STREAK = 0
    PERFECT_CHICKEN_MULTIPLIER = 1.0
    score_feed = []
    ender_pearl_timer = 0
    active_ability = None
    ability_timer = 0.0


# ----------------------------
# MAIN FUNCTION
# ----------------------------
def main():
    # The main function that initializes the game and manages the transition between the main menu and game loop.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        main_menu(screen)
        game_loop(screen)
        reset_globals()


if __name__ == "__main__":
    main()
