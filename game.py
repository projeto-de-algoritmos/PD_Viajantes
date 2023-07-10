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
        self.rect ,self.image = carregar_imagem(f'p{n}.png', 300, 225)
        self.rect.x = x
        self.rect.y = y
        self.nome = nome
        self.temperatura = temperatura
        self.selecionado = False
    
    def selecionar(self, surface):
        if self.selecionado:
            # Desenha a borda do retângulo com a cor especificada
            pygame.draw.rect(surface, RED, self.rect, 2)

        # Copia a imagem do planeta na superfície
        surface.blit(self.image, self.rect.topleft)


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



def maior_subsequencia_crescente(planetas):
    if not planetas:
        return []

    tamanho_lista = len(planetas)
    vetor = [1] * tamanho_lista  # Inicializa uma lista com todos os elementos como 1

    for i in range(1, tamanho_lista):
        for j in range(i):
            if planetas[i].temperatura > planetas[j].temperatura and vetor[i] < vetor[j] + 1:
                vetor[i] = vetor[j] + 1

    tam_maior_sub = max(vetor)  # Comprimento da maior subsequência crescente
    indice_maior_elem = vetor.index(tam_maior_sub)  # Índice do maior elemento na lista vetor

    subsequencia = [planetas[indice_maior_elem]]  # Inicializa a subsequência com o maior elemento
    tam_maior_sub -= 1

    for i in range(indice_maior_elem - 1, -1, -1):
        if planetas[i].temperatura < subsequencia[-1].temperatura and vetor[i] == tam_maior_sub:
            subsequencia.append(planetas[i])
            tam_maior_sub -= 1

    subsequencia.reverse()  # Inverte a sequência para retornar em ordem crescente
    return subsequencia
# Criação dos planetas

def cria_planeta(n, planetas):
    # parte_width = SCREEN_WIDTH // 3
    # parte_height = SCREEN_HEIGHT // 2
    parte_width = SCREEN_WIDTH // 16
    parte_height = SCREEN_HEIGHT // 2
    # coluna = i % 3
    # linha = i // 3
    

    # x = coluna * parte_width + parte_width // 2 - 150  # 25 é a metade da largura do planeta
    # y = linha * parte_height + parte_height // 2 - 25  # 25 é a metade da altura do planeta
    x = parte_width + ((i-1) * 150)
    if (n % 2 == 0):
       y = parte_height + 110
    else:
        y = parte_height
    
    planeta = Planeta(f'Planeta{n}', random.randint(0,100), x, y, n)
    planetas.add(planeta)


planetas = pygame.sprite.Group()
for i in range(1, 8):
    cria_planeta(i, planetas)

# Criação da nave
nave = Nave(200, 200)

# Fonte do texto
font = pygame.font.Font(None, 24)

# Grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(planetas)
all_sprites.add(nave)

# Variáveis do jogo

def game():
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

        # verifica se o planeta mais proximo da nave e mais quente que o anterior
        for planeta in planetas:
            if nave.rect.colliderect(planeta.rect):
                if planeta.temperatura < nave.temperatura_atual:
                    print("Nave Explodiu!")
                    game_over = True
                else:
                    nave.temperatura_atual = planeta.temperatura
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if planeta.rect.collidepoint(event.pos):
                        planeta.selecionado = not planeta.selecionado
                        planeta.desenhar(screen)

        # Colocando imagem de fundo
        screen.blit(imagem_fundo[1], (0,0))

        # Colocando o tempo e o retangulo de fundo
        retangulo_tempo = pygame.Surface((120, 30))
        retangulo_tempo.fill(BLACK)
        posicao_texto_tempo = (26, 8)
        retangulo_tempo.blit(time_text, posicao_texto_tempo)
        screen.blit(retangulo_tempo, (100, 100))  

        # Renderização das temperaturas dos planetas
        all_sprites.draw(screen)
        for planeta in planetas:
            retangulo_texto = pygame.Surface((80, 30))
            retangulo_texto.fill(BLACK)
            
            texto_temperatura = font.render(str(f'{planeta.temperatura} °C'), True, WHITE)
           
            posicao_texto = (28, 10)
            retangulo_texto.blit(texto_temperatura, posicao_texto)
            
            screen.blit(retangulo_texto, (planeta.rect.center))

        pygame.display.flip()

game()
# Encerramento do Pygame


pygame.quit()
