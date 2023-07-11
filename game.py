import pygame
import random
import time

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
GREEN = (124,252,0)

# Classe Planeta
class Planeta(pygame.sprite.Sprite):
    def __init__(self, nome, temperatura, x, y, n):
        super().__init__()
        self.rect ,self.image = carregar_imagem(f'p{n}.png', 150, 100)
        self.rect.x = x
        self.rect.y = y
        self.nome = nome
        self.temperatura = temperatura
        self.selecionado = False
    
    def destacar(self):
        if self.selecionado:
            # Desenha a borda do retângulo com a cor especificada
            pygame.draw.rect(screen, RED, self.rect, 2)

        # Copia a imagem do planeta na superfície
        screen.blit(self.image, self.rect.topleft)

# Classe Nave
class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect,self.image = carregar_imagem("starship_enterprise.png", 100, 100)
        self.rect.x = x
        self.rect.y = y
        self.temperatura_atual = 0
        self.planetas_selecionados = []

    def update(self):
        if not self.planetas_selecionados:
            return True
        
        planeta_atual = self.planetas_selecionados[0]
        self.rect.x += (planeta_atual.rect.x - self.rect.x)
        self.rect.y += (planeta_atual.rect.y - self.rect.y)

        if self.rect.colliderect(planeta_atual.rect):
            if planeta_atual.temperatura < self.temperatura_atual:
                self.rect,self.image = carregar_imagem("explosao.png", 150, 100)
                self.rect.x += (planeta_atual.rect.x - self.rect.x)
                self.rect.y += (planeta_atual.rect.y - self.rect.y)
                self.planetas_selecionados = []
            else:
                self.temperatura_atual = planeta_atual.temperatura
                self.planetas_selecionados.pop(0)

        return False 


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
    parte_width = SCREEN_WIDTH // 16
    parte_height = SCREEN_HEIGHT // 2
    
    x = parte_width + ((n-1) * 150)
    if (n % 2 == 0):
       y = parte_height + 110
    else:
        y = parte_height
    
    planeta = Planeta(f'Planeta{n}', random.randint(0,100), x, y, n)
    planetas.add(planeta)

# Função para verificar os cliques nos planetas
def verificar_cliques(event, planetas):
    if event.button == 1:  # Botão esquerdo do mouse
        pos = pygame.mouse.get_pos()
        for planeta in planetas:
            if planeta.rect.collidepoint(pos):
                planeta.selecionado = not planeta.selecionado
    
def destacar_planetas_selecionados(planetas):
    

    for planeta in planetas:
        if planeta.selecionado:
            planeta.destacar()

def monta_rota(planetas, nave):
    planetas_lista = list(planetas)
    nave.planetas_selecionados = [i for i in planetas_lista if i.selecionado]
    nave.planetas_selecionados.sort(key=lambda x: x.nome)

def desenha_planetas(planetas, fim_de_jogo):
        # Colocando imagem de fundo
        screen.blit(imagem_fundo[1], (0,0))
        all_sprites.draw(screen)
        if fim_de_jogo == True:
            mensagem = pygame.Rect((SCREEN_WIDTH/3), (SCREEN_HEIGHT/3), 300, 50)
            texto = font.render("Esta é a solução ideal", True, GREEN)
            mensagem_texto = texto.get_rect(center=mensagem.center)

            # texto = font.render("Esta é a solução ideal", True, RED)
            # mensagem = texto.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2))
            pygame.draw.rect(screen, BLACK, mensagem)
            screen.blit(texto, mensagem_texto)
        
        for planeta in planetas:
            planeta.destacar()
            retangulo_texto = pygame.Surface((80, 30))
            retangulo_texto.fill(BLACK)
            
            texto_temperatura = font.render(str(f'{planeta.temperatura} °C'), True, WHITE)
           
            posicao_texto = (28, 10)
            retangulo_texto.blit(texto_temperatura, posicao_texto)
            
            screen.blit(retangulo_texto, (planeta.rect.center))

# Fonte do texto
font = pygame.font.Font(None, 24)

# Grupo de sprites
all_sprites = pygame.sprite.Group()


def game():
    # Variáveis do jogo
    game_over = False
    total_time = 10
    current_time = 0
    starting_time = pygame.time.get_ticks()
    nave = Nave(0, 0) 

    # Criação dos planetas
    planetas = pygame.sprite.Group()
    for i in range(1, 8):
        cria_planeta(i, planetas)
    
    while not game_over:
        current_time = (pygame.time.get_ticks() - starting_time) / 1000
        if current_time >= total_time:
            
            game_over = True
            viagem(nave, planetas)
            melhor_rota(planetas)

        time_text = font.render("Tempo: {:.1f}".format(current_time), True, RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                verificar_cliques(event, planetas)

        
        
        destacar_planetas_selecionados(planetas)
        
        # Renderização das temperaturas dos planetas
        desenha_planetas(planetas, False)

        # Colocando o tempo e o retangulo de fundo
        retangulo_tempo = pygame.Surface((120, 30))
        retangulo_tempo.fill(BLACK)
        posicao_texto_tempo = (26, 8)
        retangulo_tempo.blit(time_text, posicao_texto_tempo)
        screen.blit(retangulo_tempo, (100, 100))  

        pygame.display.flip()

def viagem(nave, planetas):
    game_over = False

    monta_rota(planetas, nave)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        game_over = nave.update()
        time.sleep(2)
        desenha_planetas(planetas, False)
        screen.blit(nave.image, nave.rect.topleft)
        pygame.display.flip()

def melhor_rota(planetas):
    
    planetas = maior_subsequencia_crescente(list(planetas))

    desenha_planetas(planetas, True)
    pygame.display.flip()
    
    time.sleep(10)
    

game()
# Encerramento do Pygame


pygame.quit()
