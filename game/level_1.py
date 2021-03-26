import pygame
import sys
import random
import settings
import engine




def start():
    settings.current_stage = 1
    settings.finished_level = False
    laser_group = pygame.sprite.Group()

    # instância as classes de player e opponent
    player = engine.Player(
        "images/Paddle.png", settings.screen_width/2, settings.screen_height - 20, 7, laser_group)

    # os objetos player e opponent são adicionados a um sprite group
    # para que todos sejam renderizados ao mesmo tempo na tela ou atualizados
    # assim não existe a necessidade de fazer um por um
    paddle_group = pygame.sprite.GroupSingle()
    paddle_group.add(player)

    block_group = pygame.sprite.Group()

    powerup_group = pygame.sprite.Group()

    for i in range(11):
        for j in range(3):
            new_powerup = engine.PowerUp( #1o parametro define o powerup
                random.randint(0, 2), "images/powerups/invisible.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, paddle_group)
            new_breakable_block = engine.BreakableBlock(
                "images/blocks/Block1.png", settings.left_boundary + i * 51 + 60, 50 + j * 26, 1, new_powerup)

            block_group.add(new_breakable_block)
            powerup_group.add(new_powerup)



    # O mesmo que foi feito para o player e opponent é feito para a bola (ball)
    ball = engine.Ball("images/Ball.png", player.rect.x + 25,
                       settings.screen_height/2, 4, 4, paddle_group, block_group)
    ball_group = pygame.sprite.GroupSingle()
    ball_group.add(ball)

    ball.reset_ball(True)
    # instancia a classe GameManager, para ser usada no loop do jogo
    game_manager = engine.GameManager(
        ball_group, paddle_group, block_group, powerup_group, laser_group)

    game_start_time = pygame.time.get_ticks()
    previous_player_score = 0

    running = True
    while running:
        # checa os eventos do teclado e mouse

        if(settings.finished_level):
            running = False

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
                if event.key == pygame.K_SPACE:
                    if(player.can_shoot and player.ammunition > 0):
                        pygame.mixer.Sound.play(settings.laser_sound)
                        new_laser1 = engine.Laser(
                            "images/Laser.png", player.rect.left + 10, player.rect.top, block_group)
                        new_laser2 = engine.Laser(
                            "images/Laser.png", player.rect.right - 10, player.rect.top, block_group)
                        laser_group.add(new_laser1)
                        laser_group.add(new_laser2)
                        player.shoot_laser()

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
        bgImg = pygame.image.load('images/640x720/city.png')
        bgScaled = pygame.transform.scale(bgImg, (640, 720))
        settings.screen.blit(bgScaled,(320,0))
        
        pygame.draw.rect(settings.screen, settings.accent_color,
                         settings.left_strip)
        pygame.draw.rect(settings.screen, settings.accent_color,
                         settings.right_strip)
        block_group.draw(settings.screen)

        # Cuida da renderização e alteração dos objetos do jogo
        game_manager.run_game()

        # Atualiza todo o conteúdo da tela
        pygame.display.flip()
        # define a velocidade do jogo
        settings.clock.tick(120)
