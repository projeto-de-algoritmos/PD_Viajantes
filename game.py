import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def carregar_imagem(arquivo, width, height):
    image = pygame.image.load(f'imagens/{arquivo}')
    image = pygame.transform.scale(image, (width, height))
    image_loc = image.get_rect()
    return image_loc, image

imagem_fundo = carregar_imagem("espaco.jpg",1280,720)

pygame.display.set_caption("Jogo de Navegação por Planetas")



# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Classe Planeta
class Planeta(pygame.sprite.Sprite):
    def __init__(self, nome, temperatura, x, y, n):
        super().__init__()
        self.rect ,self.image = carregar_imagem(f'p{n}.png', 200, 150)
        self.rect.x = x
        self.rect.y = y
        self.nome = nome
        self.temperatura = temperatura


# Classe Nave
class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect,self.image = carregar_imagem("starship_enterprise.png", 100, 100)
        self.rect.x = x
        self.rect.y = y
        self.temperatura_atual = 0

    def update(self, direcao_x, direcao_y):
        self.rect.x += direcao_x
        self.rect.y += direcao_y

# Criação dos planetas

def cria_planeta(n, planetas):
    if n%2 == 0:
        x = n * 100 
        y = n * 150
    else:
        x = SCREEN_WIDTH - (n *200)
        y = SCREEN_HEIGHT - (n * 150)

    planeta = Planeta(f'Planeta{n}', random.randint(0,100), x, y, n)
    planetas.add(planeta)


planetas = pygame.sprite.Group()
for i in range(1, 8):
    cria_planeta(i, planetas)

# Criação da nave
nave = Nave(700, 500)

# Fonte do texto
font = pygame.font.Font(None, 24)

# Grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(planetas)
all_sprites.add(nave)

# Variáveis do jogo

def game():
    ultimo_planeta_temperatura = 0
    game_over = False
    total_time = 30
    current_time = 0
    starting_time = pygame.time.get_ticks()
    
    
    while not game_over:
        current_time = (pygame.time.get_ticks() - starting_time) / 1000
        if current_time >= total_time:
            
            game_over = True

        time_text = font.render("Tempo: {:.1f}".format(current_time), True, RED)

        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    nave.update(-25, 0)
                elif event.key == pygame.K_RIGHT:
                    nave.update(25, 0)
                elif event.key == pygame.K_UP:
                    nave.update(0, -25)
                elif event.key == pygame.K_DOWN:
                    nave.update(0, 25)

        # Lógica do jogo

        # verifica se o planeta mais proximo da nave e mais quente que o anterior
        for planeta in planetas:
            if nave.rect.colliderect(planeta.rect):
                if planeta.temperatura < nave.temperatura_atual:
                    print("Nave Explodiu!")
                    game_over = True
                else:
                    nave.temperatura_atual = planeta.temperatura

        # Renderização do jogo
        screen.blit(imagem_fundo[1], (0,0))
        screen.blit(time_text, (100, 100))  # Desenhar o texto na tela
        # Renderização das temperaturas dos planetas
        for planeta in planetas:
            texto_temperatura = font.render(str(planeta.temperatura), True, WHITE)
            screen.blit(texto_temperatura, (planeta.rect.x + 50, planeta.rect.y + 50))
        all_sprites.draw(screen)

        pygame.display.flip()
    # Loop principal do jogo

game()
# Encerramento do Pygame


pygame.quit()
