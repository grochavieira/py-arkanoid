import pygame
import sys
import random
import settings
import engine
import level_1
import level_2


def start():  # menu principal do jogo
    # botão para iniciar o jogo
    start_button = engine.Button(
        "images/btn_start/start_game", 0, settings.screen_width/2 - 20, 400)

    button_group = pygame.sprite.Group()
    button_group.add(start_button)

    # titulo e texto de informação do jogo
    title = engine.Text("images/title/arkanoid_title", 8, 0.07,
                        settings.screen_width/2 - 20, 100)
    # info = engine.Text("images/info/info", 2, 0.02,
    #                    settings.screen_width/2 - 20, 250)
    text_group = pygame.sprite.Group()
    text_group.add(title)
    # text_group.add(info)

    # mouse element
    mouse = engine.Mouse()
    mouse_group = pygame.sprite.Group()
    mouse_group.add(mouse)
    while True:

        settings.screen.fill(settings.bg_color)

        if pygame.sprite.spritecollide(mouse, button_group, False):
            collision_button = pygame.sprite.spritecollide(
                mouse, button_group, False)[0]
            collision_button.image = pygame.image.load(
                "images/btn_start/start_game_hover.png")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollide(mouse, button_group, False):
                    collision_button = pygame.sprite.spritecollide(
                        mouse, button_group, False)[0].rect
                    if collision_button.bottom <= 460:
                        settings.button_sound.play()
                        level_1.start()
                        if(settings.is_winning):
                            level_2.start()

        button_group.draw(settings.screen)
        mouse_group.draw(settings.screen)
        text_group.draw(settings.screen)
        button_group.update()
        mouse_group.update()
        text_group.update()
        pygame.display.update()
        settings.clock.tick(120)
