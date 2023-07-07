import pygame

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

imagem_fundo = carregar_imagem("espaco.jpg",528,810)
screen.blit(imagem_fundo[1], (SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("Jogo de Navegação por Planetas")



# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Classe Planeta
class Planeta(pygame.sprite.Sprite):
    def __init__(self, nome, temperatura, x, y):
        super().__init__()
        self.rect ,self.image = carregar_imagem("p1.png", 100, 100)
        self.rect.x = x
        self.rect.y = y
        self.nome = nome
        self.temperatura = temperatura

    def update(self):
        pass

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
planetas = pygame.sprite.Group()
planeta1 = Planeta("Planeta 1", 30, 100, 100)
planetas.add(planeta1)
planeta2 = Planeta("Planeta 2", 50, 300, 200)
planetas.add(planeta2)
planeta3 = Planeta("Planeta 3", 80, 500, 300)
planetas.add(planeta3)

# Criação da nave
nave = Nave(700, 500)

# Fonte do texto
font = pygame.font.Font(None, 24)

# Grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(planetas)
all_sprites.add(nave)

# Variáveis do jogo
game_over = False
ultimo_planeta_temperatura = 0

# Loop principal do jogo
while not game_over:
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
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Renderização das temperaturas dos planetas
    for planeta in planetas:
        texto_temperatura = font.render(str(planeta.temperatura), True, WHITE)
        screen.blit(texto_temperatura, (planeta.image.get_rect().x, planeta.image.get_rect().y - 20))

    pygame.display.flip()

# Encerramento do Pygame
pygame.quit()
