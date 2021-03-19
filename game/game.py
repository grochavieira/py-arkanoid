import pygame
import sys
import random
import settings
import engine


def start():

    # instância as classes de player e opponent
    player = engine.Player(
        "images/Paddle.png", settings.screen_width/2, settings.screen_height - 20, 7)

    # os objetos player e opponent são adicionados a um sprite group
    # para que todos sejam renderizados ao mesmo tempo na tela ou atualizados
    # assim não existe a necessidade de fazer um por um
    singleplayer_paddle_group = pygame.sprite.Group()
    singleplayer_paddle_group.add(player)

    singleplayer_block_group = pygame.sprite.Group()

    for i in range(11):
        for j in range(3):
            new_block = engine.Block(
                "images/Block1.png", i * 100 + 140, 100 + j * 50)
            new_block2 = engine.Block(
                "images/Block2.png", i * 100 + 140, 100 + j * 50)
            new_block3 = engine.Block(
                "images/Block3.png", i * 100 + 140, 100 + j * 50)
            new_block4 = engine.Block(
                "images/Block3.png", i * 100 + 140, 100 + j * 50)

            singleplayer_block_group.add(new_block)
            singleplayer_block_group.add(new_block2)
            singleplayer_block_group.add(new_block3)

    # O mesmo que foi feito para o player e opponent é feito para a bola (ball)
    ball = engine.Ball("images/Ball.png", settings.screen_width/2,
                       settings.screen_height/2, 4, 4, singleplayer_paddle_group, singleplayer_block_group)
    ball_group = pygame.sprite.GroupSingle()
    ball_group.add(ball)

    ball.reset_ball(True)
    # instancia a classe GameManager, para ser usada no loop do jogo
    singleplayer_game_manager = engine.GameManager(
        ball_group, singleplayer_paddle_group, singleplayer_block_group)

    game_start_time = pygame.time.get_ticks()
    previous_player_score = 0

    running = True
    while running:
        # checa os eventos do teclado e mouse
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
                    player.movement -= player.speed
                # apertou a tecla para baixo
                if event.key == pygame.K_RIGHT:
                    # move o jogador para baixo
                    player.movement += player.speed
                if event.key == pygame.K_ESCAPE:
                    running = False

            # se soltou alguma tecla
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    # reseta o movimento do jogador para 0
                    player.movement += player.speed
                if event.key == pygame.K_RIGHT:
                    # reseta o movimento do jogador para 0
                    player.movement -= player.speed

        # Desenha a tela de fundo
        settings.screen.fill(settings.bg_color)
        pygame.draw.rect(settings.screen, settings.accent_color,
                         settings.middle_strip)
        singleplayer_block_group.draw(settings.screen)

        # Cuida da renderização e alteração dos objetos do jogo
        singleplayer_game_manager.run_game()

        # Atualiza todo o conteúdo da tela
        pygame.display.flip()
        # define a velocidade do jogo
        settings.clock.tick(120)
