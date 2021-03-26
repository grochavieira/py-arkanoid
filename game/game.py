import pygame
import sys
import random
import settings
import engine


class GameState():
    def __init__(self):
        self.state = "menu"
        self.is_running = True
        self.paddle_group = pygame.sprite.GroupSingle()
        self.block_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()
        self.ball_group = pygame.sprite.GroupSingle()
        self.laser_group = pygame.sprite.Group()
        self.game_manager = engine.GameManager(
            self.ball_group, self.paddle_group, self.block_group, self.powerup_group, self.laser_group)

        self.player = engine.Player(
            "images/paddle_normal.png", settings.screen_width/2, settings.screen_height - 20, 7)
        self.paddle_group.add(self.player)

        self.ball = engine.Ball("images/balls/ball_night.png", self.player.rect.x + 25,
                                settings.screen_height/2, 4, 4, self.paddle_group, self.block_group)
        self.ball_group.add(self.ball)

    def game_events(self, next_stage):
        if not self.game_manager.is_winning:
            self.state = "lost_level"
            self.game_manager.reset_game()
            self.is_running = False

        if(self.game_manager.has_finished_level):
            self.game_manager.soft_reset()
            self.state = next_stage
            self.is_running = False

        for event in pygame.event.get():
            # se clicou no X da tela
            if event.type == pygame.QUIT:
                # sai do jogo
                pygame.quit()
                sys.exit()
            # se apertou alguma tecla
            if event.type == pygame.KEYDOWN:
                # apertou a tecla para cima
                if event.key == pygame.K_LEFT:
                    # move o jogador para cima
                    self.player.movement -= self.player.speed
                # apertou a tecla para baixo
                if event.key == pygame.K_RIGHT:
                    # move o jogador para baixo
                    self.player.movement += self.player.speed
                if event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                    self.game_manager.reset_game()
                    self.is_running = False
                if event.key == pygame.K_SPACE:
                    if(self.player.can_shoot and self.player.ammunition > 0):
                        pygame.mixer.Sound.play(settings.laser_sound)
                        new_laser1 = engine.Laser(
                            "images/Laser.png", self.player.rect.left + 10, self.player.rect.top, self.block_group)
                        new_laser2 = engine.Laser(
                            "images/Laser.png", self.player.rect.right - 10, self.player.rect.top, self.block_group)
                        self.laser_group.add(new_laser1)
                        self.laser_group.add(new_laser2)
                        self.player.shoot_laser()

            # se soltou alguma tecla
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    # reseta o movimento do jogador para 0
                    self.player.movement += self.player.speed
                if event.key == pygame.K_RIGHT:
                    # reseta o movimento do jogador para 0
                    self.player.movement -= self.player.speed

    def menu(self):
        settings.score = 0
        self.is_running = True
        pygame.mixer.Sound.play(settings.main_theme)  # toca fireflies

        start_button_text = settings.bigger_basic_font.render(
            "START GAME", True, settings.accent_color)
        start_button_text_rect = start_button_text.get_rect(
            center=(settings.screen_width/2, 395))
        start_button = engine.Button(
            "images/btn_start/start_game", 9, settings.screen_width/2, 400)

        randomizer_button_text = settings.bigger_basic_font.render(
            "RANDOMIZER", True, settings.accent_color)
        randomizer_button_text_rect = randomizer_button_text.get_rect(
            center=(settings.screen_width/2, 595))
        randomizer_button = engine.Button(
            "images/btn_start/start_game", 9, settings.screen_width/2, 600)

        # botão para iniciar o jogo
        button_group = pygame.sprite.Group()
        button_group.add(start_button)
        button_group.add(randomizer_button)

        # titulo e texto de informação do jogo
        title = engine.Text("images/title/arkanoid_title", 9, 0.07,
                            settings.screen_width/2, 100)

        text_group = pygame.sprite.Group()
        text_group.add(title)

        # mouse element
        mouse = engine.Mouse()
        mouse_group = pygame.sprite.Group()
        mouse_group.add(mouse)

        while self.is_running:
            settings.screen.fill(settings.bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.sprite.spritecollide(mouse, button_group, False):
                        collision_button = pygame.sprite.spritecollide(
                            mouse, button_group, False)[0].rect
                        print(collision_button.bottom)
                        if collision_button.bottom <= 600:
                            settings.button_sound.play()
                            self.state = "level_1"
                            self.is_running = False
                        elif collision_button.bottom <= 800:
                            settings.button_sound.play()
                            self.state = "randomizer"
                            self.is_running = False

            bg_image = pygame.image.load('images/background.jpg')
            bg_scaled = pygame.transform.scale(
                bg_image, (settings.screen_width, settings.screen_height))
            settings.screen.blit(bg_scaled, (0, 0))

            button_group.draw(settings.screen)
            mouse_group.draw(settings.screen)
            text_group.draw(settings.screen)
            button_group.update()
            settings.screen.blit(start_button_text, start_button_text_rect)
            settings.screen.blit(randomizer_button_text,
                                 randomizer_button_text_rect)
            mouse_group.update()
            text_group.update()
            pygame.display.update()
            settings.clock.tick(120)

    def passed_level(self):
        self.is_running = True

        passed_level_text = settings.bigger_basic_font.render(
            "You passed level " + str(self.game_manager.current_stage), True, settings.accent_color)
        passed_level_text_rect = passed_level_text.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 - 50))

        press_space_text = settings.basic_font.render(
            "Press space to proceed no next level", True, settings.accent_color)
        press_space_text_rect = press_space_text.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 + 50))

        while self.is_running:
            settings.screen.fill(settings.bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = "level_" + \
                            str(self.game_manager.current_stage + 1)
                        self.is_running = False

            settings.screen.fill(settings.bg_color)

            settings.screen.blit(passed_level_text, passed_level_text_rect)
            settings.screen.blit(press_space_text, press_space_text_rect)
            pygame.display.update()
            settings.clock.tick(120)

    def lost_level(self):
        self.is_running = True

        lost_level_text = settings.bigger_basic_font.render(
            "Your total score is " + str(settings.score), True, settings.accent_color)
        lost_level_text_rect = lost_level_text.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 - 50))

        press_space_text = settings.basic_font.render(
            "Press space to return to the menu", True, settings.accent_color)
        press_space_text_rect = press_space_text.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 + 50))

        while self.is_running:
            settings.screen.fill(settings.bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = "menu"
                        self.is_running = False

            settings.screen.fill(settings.bg_color)

            settings.screen.blit(lost_level_text, lost_level_text_rect)
            settings.screen.blit(press_space_text, press_space_text_rect)
            pygame.display.update()
            settings.clock.tick(120)

    def win_game(self):
        self.is_running = True

        win_text = settings.bigger_basic_font.render(
            "You WIN ", True, settings.accent_color)
        win_text_rect = win_text.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 - 150))

        score_text = settings.bigger_basic_font.render(
            "Your total score is " + str(settings.score), True, settings.accent_color)
        score_text_rect = score_text.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 - 50))

        press_space_text = settings.basic_font.render(
            "Press space to return to the menu", True, settings.accent_color)
        press_space_text_rect = press_space_text.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 + 50))

        while self.is_running:
            settings.screen.fill(settings.bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = "menu"
                        self.is_running = False

            settings.screen.fill(settings.bg_color)

            settings.screen.blit(win_text, win_text_rect)
            settings.screen.blit(score_text, score_text_rect)
            settings.screen.blit(press_space_text, press_space_text_rect)
            pygame.display.update()
            settings.clock.tick(120)

    def randomizer(self):
        pygame.mixer.Sound.stop(settings.main_theme)
        self.is_running = True
        self.game_manager.current_stage = 0
        self.game_manager.has_finished_level = False

        for i in range(11):
            for j in range(10):
                if random.randint(1, 100) <= 50:
                    new_powerup = engine.PowerUp(
                        "images/powerups/invisible.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, self.paddle_group)
                    new_breakable_block = engine.BreakableBlock(
                        "images/blocks/Block1.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, random.randint(1, 7), new_powerup)

                    self.block_group.add(new_breakable_block)
                    self.powerup_group.add(new_powerup)

        self.ball.reset_ball(True)

        game_start_time = pygame.time.get_ticks()
        previous_player_score = 0

        while self.is_running:
            self.game_events("randomizer")

            settings.screen.fill(settings.bg_color)
            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.left_strip)
            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.right_strip)
            self.block_group.draw(settings.screen)

            # Cuida da renderização e alteração dos objetos do jogo
            self.game_manager.run_game()

            # Atualiza todo o conteúdo da tela
            pygame.display.flip()
            # define a velocidade do jogo
            settings.clock.tick(120)

    def level_1(self):
        pygame.mixer.Sound.stop(settings.main_theme)
        self.is_running = True
        self.game_manager.current_stage = 1
        self.game_manager.has_finished_level = False

        for i in range(11):
            for j in range(3):
                new_powerup = engine.PowerUp(
                    "images/powerups/invisible.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, self.paddle_group)
                new_breakable_block = engine.BreakableBlock(
                    "images/blocks/Block1.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, 1, new_powerup)

                self.block_group.add(new_breakable_block)
                self.powerup_group.add(new_powerup)

        self.ball.reset_ball(True)

        game_start_time = pygame.time.get_ticks()

        while self.is_running:

            self.game_events("passed_level")

            settings.screen.fill(settings.bg_color)

            bg_image = pygame.image.load('images/levels/city.png')
            bg_scaled = pygame.transform.scale(bg_image, (640, 720))
            settings.screen.blit(bg_scaled, (320, 0))

            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.left_strip)
            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.right_strip)
            self.block_group.draw(settings.screen)

            self.game_manager.run_game()

            pygame.display.flip()
            settings.clock.tick(120)

    def level_2(self):
        self.is_running = True
        self.game_manager.current_stage = 2
        self.game_manager.has_finished_level = False

        powerup_group = pygame.sprite.Group()

        for i in range(11):
            for j in range(5):
                new_powerup = engine.PowerUp(
                    "images/powerups/invisible.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, self.paddle_group)
                new_breakable_block = engine.BreakableBlock(
                    "images/blocks/Block1.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, 1, new_powerup)

                self.block_group.add(new_breakable_block)
                self.powerup_group.add(new_powerup)

        self.ball.reset_ball(True)

        game_start_time = pygame.time.get_ticks()

        while self.is_running:
            self.game_events("passed_level")

            settings.screen.fill(settings.bg_color)

            bg_image = pygame.image.load('images/levels/sky.png')
            bg_scaled = pygame.transform.scale(bg_image, (640, 720))
            settings.screen.blit(bg_scaled, (320, 0))

            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.left_strip)
            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.right_strip)
            self.block_group.draw(settings.screen)

            self.game_manager.run_game()

            pygame.display.flip()
            settings.clock.tick(120)

    def level_3(self):
        self.is_running = True
        self.game_manager.current_stage = 3
        self.game_manager.has_finished_level = False

        powerup_group = pygame.sprite.Group()

        for i in range(11):
            for j in range(5):
                new_powerup = engine.PowerUp(
                    "images/powerups/invisible.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, self.paddle_group)
                new_breakable_block = engine.BreakableBlock(
                    "images/blocks/Block1.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, 1, new_powerup)

                self.block_group.add(new_breakable_block)
                self.powerup_group.add(new_powerup)

        self.ball.reset_ball(True)

        game_start_time = pygame.time.get_ticks()

        while self.is_running:
            self.game_events("passed_level")

            settings.screen.fill(settings.bg_color)

            bg_image = pygame.image.load('images/levels/spooky.png')
            bg_scaled = pygame.transform.scale(bg_image, (640, 720))
            settings.screen.blit(bg_scaled, (320, 0))

            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.left_strip)
            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.right_strip)
            self.block_group.draw(settings.screen)

            self.game_manager.run_game()

            pygame.display.flip()
            settings.clock.tick(120)

    def level_4(self):
        self.is_running = True
        self.game_manager.current_stage = 4
        self.game_manager.has_finished_level = False

        powerup_group = pygame.sprite.Group()

        for i in range(11):
            for j in range(5):
                new_powerup = engine.PowerUp(
                    "images/powerups/invisible.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, self.paddle_group)
                new_breakable_block = engine.BreakableBlock(
                    "images/blocks/Block1.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, 1, new_powerup)

                self.block_group.add(new_breakable_block)
                self.powerup_group.add(new_powerup)

        self.ball.reset_ball(True)

        game_start_time = pygame.time.get_ticks()

        while self.is_running:
            self.game_events("passed_level")

            settings.screen.fill(settings.bg_color)

            bg_image = pygame.image.load('images/levels/grass.png')
            bg_scaled = pygame.transform.scale(bg_image, (640, 720))
            settings.screen.blit(bg_scaled, (320, 0))

            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.left_strip)
            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.right_strip)
            self.block_group.draw(settings.screen)

            self.game_manager.run_game()

            pygame.display.flip()
            settings.clock.tick(120)

    def level_5(self):
        self.is_running = True
        self.game_manager.current_stage = 5
        self.game_manager.has_finished_level = False

        powerup_group = pygame.sprite.Group()

        for i in range(11):
            for j in range(5):
                new_powerup = engine.PowerUp(
                    "images/powerups/invisible.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, self.paddle_group)
                new_breakable_block = engine.BreakableBlock(
                    "images/blocks/Block1.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, 1, new_powerup)

                self.block_group.add(new_breakable_block)
                self.powerup_group.add(new_powerup)

        self.ball.reset_ball(True)

        game_start_time = pygame.time.get_ticks()

        while self.is_running:
            self.game_events("win_game")

            settings.screen.fill(settings.bg_color)

            bg_image = pygame.image.load('images/levels/city.png')
            bg_scaled = pygame.transform.scale(bg_image, (640, 720))
            settings.screen.blit(bg_scaled, (320, 0))

            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.left_strip)
            pygame.draw.rect(settings.screen, settings.accent_color,
                             settings.right_strip)
            self.block_group.draw(settings.screen)

            self.game_manager.run_game()

            pygame.display.flip()
            settings.clock.tick(120)

    def state_manager(self):
        if self.state == "menu":
            self.menu()
        if self.state == "passed_level":
            self.passed_level()
        if self.state == "lost_level":
            self.lost_level()
        if self.state == "win_game":
            self.win_game()
        if self.state == "randomizer":
            self.randomizer()
        if self.state == "level_1":
            self.level_5()
        if self.state == "level_2":
            self.level_2()
        if self.state == "level_3":
            self.level_3()
        if self.state == "level_4":
            self.level_4()
        if self.state == "level_5":
            self.level_5()
