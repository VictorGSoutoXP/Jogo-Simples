import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("PONG vs IA")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Sons
pong_sound = pygame.mixer.Sound("blip.mp3")
score_sound = pygame.mixer.Sound("score.mp3")

# Fonte
fonte = pygame.font.SysFont(None, 50)
fonte_grande = pygame.font.SysFont(None, 80)

# Objetos
raquete_largura = 10
raquete_altura = 100
bola_tamanho = 15

def desenhar_texto(texto, fonte, cor, y):
    render = fonte.render(texto, True, cor)
    rect = render.get_rect(center=(LARGURA//2, y))
    tela.blit(render, rect)

def menu():
    while True:
        tela.fill(PRETO)
        desenhar_texto("PONG vs IA", fonte_grande, BRANCO, ALTURA//3)
        desenhar_texto("Pressione ENTER para jogar", fonte, BRANCO, ALTURA//2)
        desenhar_texto("Pressione ESC para sair", fonte, BRANCO, ALTURA//2 + 40)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def jogar():
    raquete_jogador = pygame.Rect(10, ALTURA//2 - 50, raquete_largura, raquete_altura)
    raquete_ia = pygame.Rect(LARGURA - 20, ALTURA//2 - 50, raquete_largura, raquete_altura)
    bola = pygame.Rect(LARGURA//2, ALTURA//2, bola_tamanho, bola_tamanho)

    vel_bola_x = 5 * random.choice((1, -1))
    vel_bola_y = 5 * random.choice((1, -1))
    vel_raquete = 6
    vel_ia = 4

    pontos_jogador = 0
    pontos_ia = 0
    max_pontos = 5

    relogio = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and raquete_jogador.top > 0:
            raquete_jogador.y -= vel_raquete
        if teclas[pygame.K_s] and raquete_jogador.bottom < ALTURA:
            raquete_jogador.y += vel_raquete

        # Movimento da IA
        if raquete_ia.centery < bola.centery and raquete_ia.bottom < ALTURA:
            raquete_ia.y += vel_ia
        elif raquete_ia.centery > bola.centery and raquete_ia.top > 0:
            raquete_ia.y -= vel_ia

        # Movimento da bola
        bola.x += vel_bola_x
        bola.y += vel_bola_y

        # Colisão com topo/fundo
        if bola.top <= 0 or bola.bottom >= ALTURA:
            vel_bola_y *= -1

        # Colisão com raquetes
        if bola.colliderect(raquete_jogador) or bola.colliderect(raquete_ia):
            vel_bola_x *= -1
            pong_sound.play()

        # Pontuação
        if bola.left <= 0:
            pontos_ia += 1
            score_sound.play()
            bola.center = (LARGURA//2, ALTURA//2)
            vel_bola_x *= -1
        if bola.right >= LARGURA:
            pontos_jogador += 1
            score_sound.play()
            bola.center = (LARGURA//2, ALTURA//2)
            vel_bola_x *= -1

        # Fim do jogo
        if pontos_jogador == max_pontos or pontos_ia == max_pontos:
            vencedor = "Você venceu!" if pontos_jogador > pontos_ia else "A IA venceu!"
            tela.fill(PRETO)
            desenhar_texto(vencedor, fonte_grande, BRANCO, ALTURA//2)
            pygame.display.flip()
            pygame.time.wait(3000)
            return

        # Desenho
        tela.fill(PRETO)
        pygame.draw.rect(tela, BRANCO, raquete_jogador)
        pygame.draw.rect(tela, BRANCO, raquete_ia)
        pygame.draw.ellipse(tela, BRANCO, bola)
        pygame.draw.aaline(tela, BRANCO, (LARGURA//2, 0), (LARGURA//2, ALTURA))

        texto1 = fonte.render(str(pontos_jogador), True, BRANCO)
        texto2 = fonte.render(str(pontos_ia), True, BRANCO)
        tela.blit(texto1, (LARGURA//4, 20))
        tela.blit(texto2, (LARGURA*3//4, 20))

        pygame.display.flip()
        relogio.tick(60)

# Executar jogo
menu()
jogar()
