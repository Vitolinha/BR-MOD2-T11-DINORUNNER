import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, GAME_OVER
from dino_runner.components.player import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

FONT_STYLE = 'dino_runner/assets/Other/pixelated.ttf'


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('dino_runner/assets/Sounds/game_song.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.score = 0
        self.high_score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager() ## importar o update
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.high_score = 0
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self, self.player)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 2 ## troca da lógica
        if self.score > self.high_score: ## implementação do high score
            self.high_score = self.score
        if self.score % 1000 == 0: #1000
            pygame.mixer.music.load('dino_runner/assets/Sounds/point.wav')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.text_pattern(FONT_STYLE, 20,
                 f"{self.player.type.capitalize()} enabled!!",
                  (0, 0, 0), 500, 40)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
    
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.game_speed = 20 ## RESET SPEED
                self.score = 0 ## RESET SCORE
                self.run()
                
    def text_pattern(self, font, size, message: str, color, position_x, position_y): ## método para a montagem do texto
        font = pygame.font.Font(font, size)
        text = font.render(message, True, (color))
        text_rect = text.get_rect()
        text_rect.center = (position_x, position_y)
        self.screen.blit(text, text_rect)

    def draw_score(self):
        self.text_pattern(FONT_STYLE, 22,
         f"Score: {self.score}", 
         (0, 0, 0), 1000, 50)

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0: ## TELA DE TÍTULO
            self.text_pattern(FONT_STYLE, 44,
            f"DINO RUNNER",
            (0, 0, 0), half_screen_width, half_screen_height - 150)
            self.text_pattern(FONT_STYLE, 22,
            f"Press any key to start",
            (0, 0, 0), half_screen_width, half_screen_height)
        else: ## MENU DE RESTART
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 140))
            self.screen.blit(GAME_OVER, (half_screen_width - 180, half_screen_height - 200))
            self.text_pattern(FONT_STYLE, 22,
             f"Press any key to continue",
             (0, 0, 0), half_screen_width, half_screen_height)
            self.text_pattern(FONT_STYLE, 22,
             f"Score: {self.score}",
             (0, 0, 0), half_screen_width, half_screen_height + 50)
            self.text_pattern(FONT_STYLE, 22,
             f"High Score: {self.high_score}",
             (0, 0, 0), half_screen_width, half_screen_height + 100)
            self.text_pattern(FONT_STYLE, 22,
             f"Deaths: {self.death_count}",
             (0, 0, 0), half_screen_width, half_screen_height + 150)


        pygame.display.update()
        self.handle_events_on_menu()