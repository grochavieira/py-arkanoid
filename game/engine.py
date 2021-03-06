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


# classe dos lasers que são atirados pela raquete/nave
class Laser(Block):
    def __init__(self, image_path, x_pos, y_pos, blocks):
        super().__init__(image_path, x_pos, y_pos)
        self.is_active = False
        self.speed = 5
        self.blocks = blocks

    def update(self):
        self.rect.y -= self.speed - 0.5
        self.collision()

    def collision(self):
        if self.rect.top <= 0:
            self.kill()

        if pygame.sprite.spritecollide(self, self.blocks, False):
            collision_blocks = pygame.sprite.spritecollide(
                self, self.blocks, False)

            settings.score += 100 * len(collision_blocks)
            pygame.mixer.Sound.play(settings.destroy_sound)

            for collision_block in collision_blocks:
                self.kill()
                if collision_block.life - 1 == 0:
                    settings.score += 100 * collision_block.initial_life

                collision_block.life -= 1


# classe dos poderes
class PowerUp(Block):
    def __init__(self, image_path, x_pos, y_pos, paddle, ball):
        super().__init__(image_path, x_pos, y_pos)
        self.powerup_type = settings.powerups[random.randint(0, 4)]
        self.is_active = False
        self.speed = 2
        self.paddle = paddle
        self.ball = ball
        self.spawn_value = random.randint(1, 100)

    def update(self):
        if self.spawn_value > 70:
            self.kill()
        if self.is_active:
            self.image = pygame.image.load(
                "images/powerups/" + self.powerup_type + ".png")
            self.rect.y += self.speed
            self.collision()

    def collision(self):

        if pygame.sprite.spritecollide(self, self.paddle, False):
            collision_paddle = pygame.sprite.spritecollide(
                self, self.paddle, False)[0]

            # raquete maior
            if(self.powerup_type == "grow_paddle"):
                pygame.mixer.Sound.play(settings.grow_power_sound)
                collision_paddle.image = pygame.image.load(
                    "images/paddle_grow.png")
                collision_paddle.rect = collision_paddle.image.get_rect(
                    center=(collision_paddle.rect.center))

            # raquete menor
            if(self.powerup_type == "shrink_paddle"):
                pygame.mixer.Sound.play(settings.grow_power_sound)
                collision_paddle.image = pygame.image.load(
                    "images/paddle_normal.png")
                collision_paddle.rect = collision_paddle.image.get_rect(
                    center=(collision_paddle.rect.center))

            # raquete mais rápida
            if(self.powerup_type == "increase_paddle_speed"):
                pygame.mixer.Sound.play(settings.speed_power_sound)
                if(collision_paddle.speed < collision_paddle.initial_speed):
                    if (collision_paddle.speed >= 0):
                        collision_paddle.speed += 1
                    elif (collision_paddle.speed < 0):
                        collision_paddle.speed -= 1

            # raquete atira
            if(self.powerup_type == "laser_ammunition"):
                collision_paddle.ammunition += 3
                pygame.mixer.Sound.play(settings.guns_power_sound)

            if(self.powerup_type == "plus_one_life"):
                if(collision_paddle.life < 5):
                    collision_paddle.life += 1
                pygame.mixer.Sound.play(settings.grow_power_sound)

            if(self.powerup_type == "ball_fire"):
                # carrega o sprite
                self.ball.sprite.image = pygame.image.load("images/balls/ball_fire.png")
                # desenha o retangulo em volta da imagem
                self.ball.sprite.rect = self.ball.sprite.image.get_rect(center=(self.ball.sprite.rect.center))

            self.kill()

        if self.rect.bottom >= settings.screen_height:
            self.kill()


# classe dos blocos quebráveis
class BreakableBlock(Block):
    def __init__(self, image_path, x_pos, y_pos, life, powerup):
        super().__init__(image_path, x_pos, y_pos)
        self.initial_life = life
        self.life = life
        self.powerup = powerup

    def update(self):
        if(self.life <= 0):
            self.powerup.is_active = True
            self.kill()
        if(self.life == 7):
            self.image = pygame.image.load("images/blocks/Block7.png")
        if(self.life == 6):
            self.image = pygame.image.load("images/blocks/Block6.png")
        if(self.life == 5):
            self.image = pygame.image.load("images/blocks/Block5.png")
        if(self.life == 4):
            self.image = pygame.image.load("images/blocks/Block4.png")
        if(self.life == 3):
            self.image = pygame.image.load("images/blocks/Block3.png")
        if(self.life == 2):
            self.image = pygame.image.load("images/blocks/Block2.png")
        if(self.life == 1):
            self.image = pygame.image.load("images/blocks/Block1.png")


class Player(Block):  # Classe que define a raquete e suas funções
    def __init__(self, image_path, x_pos, y_pos, speed):
        super().__init__(image_path, x_pos, y_pos)
        self.life = 3
        self.initial_speed = speed
        self.speed = speed  # define a velocidade do jogador
        self.movement = 0  # define a movimentação do jogador
        self.can_shoot = False
        self.ammunition = 0

    # função para limitar até onde a raquete pode ir
    def screen_constrain(self):
        if self.rect.left <= settings.left_boundary:  # se a raquete chegou até o 'teto' da tela
            self.rect.left = settings.left_boundary
        if self.rect.right >= settings.right_boundary:  # se a raquete chegou até o 'chão' da tela
            self.rect.right = settings.right_boundary

    # função para atualizar a raquete
    def update(self, ball_group):
        self.rect.x += self.movement  # movimenta a raquete
        self.screen_constrain()  # chama a função impor limite até onde pode ir

    def shoot_laser(self):
        self.ammunition -= 1

    def reset(self):
        self.life = 3
        self.speed = self.initial_speed
        self.movement = 0
        self.can_shoot = False
        self.ammunition = 0
        self.image = pygame.image.load(
                    "images/paddle_normal.png")
        self.rect.center = (settings.screen_width/2, settings.screen_height - 20)


class Ball(Block):  # classe que define a bola e sua funções
    def __init__(self, image_path, x_pos, y_pos, speed_x, speed_y, paddle, blocks):
        super().__init__(image_path, x_pos, y_pos)
        # randomiza a direção inicial que a bola ira começar
        self.initial_speed_x = speed_x
        self.initial_speed_y = speed_y
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddle = paddle
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
            self.rect.x = self.paddle.sprite.rect.x + \
                (self.paddle.sprite.rect.width // 2) - 10
            self.restart_counter()  # reseta o contador

    # função para definir as colisões da bola
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= settings.screen_height:
            # toca o som de hit quando a bola toca na parte
            # de cima ou de baixo da tela
            pygame.mixer.Sound.play(settings.hit_sound)
            self.speed_y *= -1  # joga a bola para outra posição

        if self.rect.left <= settings.left_boundary or self.rect.right >= settings.right_boundary:
            pygame.mixer.Sound.play(settings.hit_sound)
            self.speed_x *= -1  # joga a bola para outra posição

        # condicionais utilizadas para os blocos que aparecem na tela
        if pygame.sprite.spritecollide(self, self.blocks, False):
            collision_blocks = pygame.sprite.spritecollide(
                self, self.blocks, False)

            settings.score += 100 * len(collision_blocks)
            pygame.mixer.Sound.play(settings.destroy_sound)

            for collision_block in collision_blocks:

                if abs(self.rect.right - collision_block.rect.left) < 10 and self.speed_x > 0:
                    self.speed_x *= -1

                if abs(self.rect.left - collision_block.rect.right) < 10 and self.speed_x < 0:
                    self.speed_x *= -1

                if abs(self.rect.top - collision_block.rect.bottom) < 10 and self.speed_y < 0:
                    self.rect.top = collision_block.rect.bottom
                    self.speed_y *= -1

                if abs(self.rect.bottom - collision_block.rect.top) < 10 and self.speed_y > 0:
                    self.rect.bottom = collision_block.rect.top
                    self.speed_y *= -1

                if collision_block.life - 1 == 0:
                    settings.score += 100 * collision_block.initial_life

                collision_block.life -= 1

        # a função spritecollide é utilizada para fazer algo
        # quando dois objetos colidem, no caso a colisão das
        # raquetes (self.paddle) com a bola (self) e a terceiro
        # parâmetro se refere a eliminar todos os elementos que colidiram
        # com o elemento de referência se deixar como True, para False
        # apenas retorna uma lista dos elementos que colidiram
        if pygame.sprite.spritecollide(self, self.paddle, False):
            # toca o som de hit
            pygame.mixer.Sound.play(settings.hit_sound)
            # como retorna uma lista de elementos, é pego
            # somente o primeiro elemento, que pode ser a raquete
            # do jogador ou do oponente
            collision_paddle = pygame.sprite.spritecollide(
                self, self.paddle, False)[0].rect

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
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    # função para resetar a bola sempre que algúem marca
    # um ponto
    def reset_ball(self, start_game):
        self.paddle.sprite.can_shoot = False
        self.active = False  # a bola não esta movimentando
        # define de forma aleatória a direção que irá iniciar
        self.speed_x *= random.choice((-1, 1))
        self.speed_y = abs(self.speed_y) * -1
        # pega o tempo quando a bola foi resetada
        self.score_time = pygame.time.get_ticks()
        # joga a bola para o centro da tela
        self.rect.center = (self.paddle.sprite.rect.x +
                            (self.paddle.sprite.rect.width // 2), self.paddle.sprite.rect.y - self.paddle.sprite.rect.height + 10)
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
            countdown_number = 0
            self.paddle.sprite.can_shoot = True
            self.active = True

        # cria o texto que será renderizado
        time_counter = settings.basic_font.render(
            str(countdown_number), True, settings.accent_color)
        # cria um retangulo em volta do texto e define sua posição na tela
        time_counter_rect = time_counter.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 + 50))
        # desenha na tela o retangulo
        # pygame.draw.rect(settings.screen, settings.bg_color, time_counter_rect)
        # coloca de fato na tela o contador
        settings.screen.blit(time_counter, time_counter_rect)


class GameManager:  # classe para gerenciar o jogo
    def __init__(self, ball_group, paddle_group, block_group, powerup_group, laser_group):
        self.player_score = 0
        self.current_stage = 0
        self.is_winning = True
        self.has_finished_level = False
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.block_group = block_group
        self.powerup_group = powerup_group
        self.laser_group = laser_group

    def run_game(self):
        if(self.paddle_group.sprite.life <= 0):
            self.is_winning = False

        # Desenha os objetos do jogo
        self.paddle_group.draw(settings.screen)
        self.ball_group.draw(settings.screen)
        self.block_group.draw(settings.screen)
        self.powerup_group.draw(settings.screen)
        self.laser_group.draw(settings.screen)

        # Atualiza os objetos do jogo
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.block_group.update()
        self.powerup_group.update()
        self.laser_group.update()
        self.reset_ball()
        self.draw_score()
        self.draw_ammunition()
        self.draw_life()
        self.stage_level()

        if(len(self.block_group) == 0):
            self.has_finished_level = True

    # função utilizada para verificar e chamar a função
    # de resetar a bola quando ocorrer colisão nas laterais
    def reset_ball(self):
        if self.ball_group.sprite.rect.bottom >= settings.screen_height:  # a bola saiu pela direita
            self.paddle_group.sprite.life -= 1
            self.ball_group.sprite.reset_ball(False)  # reseta a bola
            for powerup in self.powerup_group.sprites():
                if(powerup.is_active):
                    powerup.kill()

            for laser in self.laser_group.sprites():
                laser.kill()

    def reset_game(self):
        self.paddle_group.sprite.reset()
        self.is_winning = True
        self.has_finished_level = False
        for block in self.block_group.sprites():
            block.kill()

        for powerup in self.powerup_group.sprites():
            powerup.kill()

        for laser in self.laser_group.sprites():
            laser.kill()

    def soft_reset(self):
        self.paddle_group.sprite.rect.center = (
            settings.screen_width/2, settings.screen_height - 20)
        for powerup in self.powerup_group.sprites():
            powerup.kill()

        for laser in self.laser_group.sprites():
            laser.kill()

    def draw_score(self):
        player_score = settings.basic_font.render(
            "SCORE " + str(settings.score), True, settings.accent_color)

        player_score_rect = player_score.get_rect(
            midleft=(10, 70))

        settings.screen.blit(player_score, player_score_rect)

    def draw_ammunition(self):
        ammunition_text = settings.basic_font.render(
            "AMMUNITION " + str(self.paddle_group.sprite.ammunition), True, settings.accent_color)
        bullet = pygame.image.load('images/bullet.png')
        bulletScaled = pygame.transform.scale(bullet, (40, 35))
        settings.screen.blit(bulletScaled, (260, 103))

        ammunition_text_rect = ammunition_text.get_rect(
            midleft=(10, 120))

        settings.screen.blit(ammunition_text, ammunition_text_rect)

    def draw_heart(self, life):
        heart = pygame.image.load('images/life.png')
        heartScaled = pygame.transform.scale(heart, (40, 35))
        if (life >= 5):
            settings.screen.blit(heartScaled, (270, 155))
        if (life >= 4):
            settings.screen.blit(heartScaled, (230, 155))
        if (life >= 3):
            settings.screen.blit(heartScaled, (190, 155))
        if (life >= 2):
            settings.screen.blit(heartScaled, (150, 155))
        if (life >= 1):
            settings.screen.blit(heartScaled, (110, 155))

    def draw_life(self):
        lifes_text = settings.basic_font.render(
            "LIFES ", True, settings.accent_color)

        self.draw_heart(self.paddle_group.sprite.life)

        lifes_text_rect = lifes_text.get_rect(
            midleft=(10, 170))

        settings.screen.blit(lifes_text, lifes_text_rect)

    def stage_level(self):
        if(self.current_stage == 0):
            level_text = settings.basic_font.render(
                "RANDOMIZER", True, settings.accent_color)
        else:
            level_text = settings.basic_font.render(
                "LEVEL " + str(self.current_stage), True, settings.accent_color)

        level_text_rect = level_text.get_rect(
            midleft=(10, 20))

        settings.screen.blit(level_text, level_text_rect)


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

        if number_of_images > 0:
            for i in range(number_of_images):
                image_path = base_images_path + str(i) + ".png"
                self.sprites.append(pygame.image.load(image_path))
        else:
            image_path = base_images_path + ".png"
            self.sprites.append(pygame.image.load(image_path))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

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
            image_path = base_images_path + str(i) + ".png"
            self.sprites.append(pygame.image.load(image_path))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self):
        self.current_sprite += self.sprite_velocity

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]
