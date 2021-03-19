import pygame
import sys
import random

# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Janela principal
screen_width = 1280  # largura
screen_height = 720  # altura

# cria a janela do jogo
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")  # titulo

score = 0

bg_color = pygame.Color("#020122")  # code de fundo
accent_color = (253, 255, 252)  # cor das letras e linha no meio
basic_font = pygame.font.Font("freesansbold.ttf", 32)  # carrega a fonte
hit_sound = pygame.mixer.Sound("sounds/pong.wav")  # carrega o som de hit
score_sound = pygame.mixer.Sound("sounds/score.wav")  # carrega o som de score
destroy_sound = pygame.mixer.Sound(
    "sounds/destroy.wav")  # carrega o som de score
button_sound = pygame.mixer.Sound(
    "sounds/button.wav")  # carrega o som de botão
# cria uma linha que será desenhada no meio da tela
middle_strip = pygame.Rect(screen_width/2 - 2, 0, 4, screen_height)
