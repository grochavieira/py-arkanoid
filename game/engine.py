import pygame
import sys
import random
import settings

# classe base que será herdada pelas outras
# é utilizada para carregar a imagem e criar
# um retangulo ao redor dela, para que não sejá
# necessário repetir a mesma coisa nas outras por
# se tratar de elementos em comum


class Block(pygame.sprite.Sprite):
    def __init__(self, image_path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(image_path)  # carrega o sprite
        # desenha o retangulo em volta da imagem
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):  # Classe que define a raquete e suas funções
    def __init__(self, image_path, x_pos, y_pos, speed):
        super().__init__(image_path, x_pos, y_pos)
        self.speed = speed  # define a velocidade do jogador
        self.movement = 0  # define a movimentação do jogador

    # função para limitar até onde a raquete pode ir
    def screen_constrain(self):
        if self.rect.left <= 0:  # se a raquete chegou até o 'teto' da tela
            self.rect.left = 0
        if self.rect.right >= settings.screen_width:  # se a raquete chegou até o 'chão' da tela
            self.rect.right = settings.screen_width

    # função para atualizar a raquete
    def update(self, ball_group):
        self.rect.x += self.movement  # movimenta a raquete
        self.screen_constrain()  # chama a função impor limite até onde pode ir


class Ball(Block):  # classe que define a bola e sua funções
    def __init__(self, image_path, x_pos, y_pos, speed_x, speed_y, paddles, blocks):
        super().__init__(image_path, x_pos, y_pos)
        # randomiza a direção inicial que a bola ira começar
        self.initial_speed_x = speed_x
        self.initial_speed_y = speed_y
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.blocks = blocks
        self.active = False  # será usado para saber se a bola está movimentando
        self.score_time = 0

    # função para atualizar a bola
    def update(self):
        if self.active:  # se a bola está movimentando
            # atualiza sua posição
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()  # chama a função de colisões
        else:  # se não
            self.restart_counter()  # reseta o contador

    # função para definir as colisões da bola
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= settings.screen_height:
            # toca o som de hit quando a bola toca na parte
            # de cima ou de baixo da tela
            pygame.mixer.Sound.play(settings.hit_sound)
            self.speed_y *= -1  # joga a bola para outra posição

        if self.rect.left <= 0 or self.rect.right >= settings.screen_width:
            pygame.mixer.Sound.play(settings.hit_sound)
            self.speed_x *= -1  # joga a bola para outra posição

        # condicionais utilizadas para os blocos que aparecem na tela
        if pygame.sprite.spritecollide(self, self.blocks, False):
            collision_blocks = pygame.sprite.spritecollide(
                self, self.blocks, False)

            settings.score += 100 * len(collision_blocks)
            blockk = collision_blocks[len(collision_blocks) - 1]
            collision_block = collision_blocks[0].rect

            pygame.mixer.Sound.play(settings.destroy_sound)

            if abs(self.rect.right - collision_block.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1

            if abs(self.rect.left - collision_block.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1

            if abs(self.rect.top - collision_block.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_block.bottom
                self.speed_y *= -1

            if abs(self.rect.bottom - collision_block.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_block.top
                self.speed_y *= -1
            blockk.kill()

        # a função spritecollide é utilizada para fazer algo
        # quando dois objetos colidem, no caso a colisão das
        # raquetes (self.paddles) com a bola (self) e a terceiro
        # parâmetro se refere a eliminar todos os elementos que colidiram
        # com o elemento de referência se deixar como True, para False
        # apenas retorna uma lista dos elementos que colidiram
        if pygame.sprite.spritecollide(self, self.paddles, False):
            # toca o som de hit
            pygame.mixer.Sound.play(settings.hit_sound)
            # como retorna uma lista de elementos, é pego
            # somente o primeiro elemento, que pode ser a raquete
            # do jogador ou do oponente
            collision_paddle = pygame.sprite.spritecollide(
                self, self.paddles, False)[0].rect

            # agora que sabemos qual raquete está ocorrendo
            # a colisão, basta utilizar as condições a seguir
            # para mudar a posição da bola
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1

            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1

            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1

            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                # if collision_paddle.centerx >= self.rect.centerx:
                #     if self.speed_x < 0:
                #         self.speed_x = (self.initial_speed_x *
                #                         (((collision_paddle.centerx - self.rect.centerx) % 47)/47)) * -1
                #     else:
                #         self.speed_x = self.initial_speed_x * \
                #             (((collision_paddle.centerx - self.rect.centerx) % 47)/47)
                # else:
                #     if self.speed_x < 0:
                #         self.speed_x = (self.initial_speed_x *
                #                         (((collision_paddle.centerx - self.rect.centerx) % 47)/47)) * -1
                #     else:
                #         self.speed_x = self.initial_speed_x * \
                #             (((collision_paddle.centerx - self.rect.centerx) % 47)/47)

                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    # função para resetar a bola sempre que algúem marca
    # um ponto
    def reset_ball(self, start_game):
        self.active = False  # a bola não esta movimentando
        # define de forma aleatória a direção que irá iniciar
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        # pega o tempo quando a bola foi resetada
        self.score_time = pygame.time.get_ticks()
        # joga a bola para o centro da tela
        self.rect.center = (settings.screen_width/2, settings.screen_height/2)
        # ativa um som quando a bola sai pra fora da tela
        if(not start_game):
            pygame.mixer.Sound.play(settings.score_sound)

    # função para resetar o contador, que é chamado sempre
    # que alguém marca algum ponto, ou no inicio do jogo
    def restart_counter(self):
        current_time = pygame.time.get_ticks()  # pega o tempo atual
        countdown_number = 3  # contador que será renderizado na tela

        # basicamente essas condições são utilizadas
        # para contar 3 segundos antes da bola começar a se
        # movimentar, além de renderizar na tela um contador
        # para os jogadores saberem quando a bola voltar a se
        # movimentar
        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        # cria o texto que será renderizado
        time_counter = settings.basic_font.render(
            str(countdown_number), True, settings.accent_color)
        # cria um retangulo em volta do texto e define sua posição na tela
        time_counter_rect = time_counter.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 + 50))
        # desenha na tela o retangulo
        pygame.draw.rect(settings.screen, settings.bg_color, time_counter_rect)
        # coloca de fato na tela o contador
        settings.screen.blit(time_counter, time_counter_rect)


class GameManager:  # classe para gerenciar o jogo
    def __init__(self, ball_group, paddle_group, block_group):
        self.player_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.block_group = block_group

    def run_game(self):
        # Desenha os objetos do jogo
        self.paddle_group.draw(settings.screen)
        self.ball_group.draw(settings.screen)
        self.block_group.draw(settings.screen)

        # Atualiza os objetos do jogo
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    # função utilizada para verificar e chamar a função
    # de resetar a bola quando ocorrer colisão nas laterais
    def reset_ball(self):
        if self.ball_group.sprite.rect.bottom >= settings.screen_height:  # a bola saiu pela direita
            self.ball_group.sprite.reset_ball(False)  # reseta a bola

    # função para desenhar o score na tela
    def draw_score(self):
        # cria o texto para o score do jogador
        # e do oponente
        player_score = settings.basic_font.render(
            "SCORE: " + str(settings.score), True, settings.accent_color)

        # cria um objeto ao redor do texto dos scores
        # e também define a posição do texto
        player_score_rect = player_score.get_rect(
            midleft=(50, 50))

        # coloca os scores na tela
        settings.screen.blit(player_score, player_score_rect)


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([1, 1])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Button(pygame.sprite.Sprite):
    def __init__(self, base_images_path, number_of_images, pos_x, pos_y):
        super().__init__()
        self.sprites = []

        for i in range(number_of_images):
            image_path = base_images_path + str(i + 1) + ".png"
            self.sprites.append(pygame.image.load(image_path))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.07

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]


class Text(pygame.sprite.Sprite):
    def __init__(self, base_images_path, number_of_images, sprite_velocity, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprite_velocity = sprite_velocity

        for i in range(number_of_images):
            image_path = base_images_path + str(i + 1) + ".png"
            self.sprites.append(pygame.image.load(image_path))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += self.sprite_velocity

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]
