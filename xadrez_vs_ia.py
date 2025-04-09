import pygame
import chess
import chess.engine
import sys

# --- CONFIGURACOES ---
TAMANHO_CASA = 80
TAMANHO_TABULEIRO = TAMANHO_CASA * 8
BRANCO = (240, 217, 181)
PRETO = (181, 136, 99)
SELECIONADO = (255, 255, 0)

# Caminho do Stockfish (ajuste se necessário)
CAMINHO_STOCKFISH = r"C:\\Users\\victor.goncalves\\Documents\\Xadrez\\stockfish-windows-x86-64-avx2\\stockfish\\stockfish-windows-x86-64-avx2.exe"

# Inicializacao
pygame.init()
tela = pygame.display.set_mode((TAMANHO_TABULEIRO, TAMANHO_TABULEIRO + 100))
pygame.display.set_caption("Xadrez vs IA")
fonte = pygame.font.SysFont(None, 32)
fonte_grande = pygame.font.SysFont(None, 40)

# --- FUNCOES ---
def desenhar_tabuleiro(screen, board, cor_jogador, selecao=None):
    for linha in range(8):
        for coluna in range(8):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            x = coluna * TAMANHO_CASA
            y = linha * TAMANHO_CASA
            pygame.draw.rect(screen, cor, (x, y, TAMANHO_CASA, TAMANHO_CASA))

            if selecao == (linha, coluna):
                pygame.draw.rect(screen, SELECIONADO, (x, y, TAMANHO_CASA, TAMANHO_CASA), 4)

            peca = board.piece_at(posicao_para_peca(coluna, linha, cor_jogador))
            if peca:
                cor_texto = (0, 0, 0) if peca.color == chess.WHITE else (255, 255, 255)
                texto = fonte.render(peca.symbol().upper(), True, cor_texto)
                screen.blit(texto, (x + 25, y + 25))

def posicao_para_peca(coluna, linha, cor_jogador):
    if cor_jogador == chess.BLACK:
        coluna = 7 - coluna
        linha = 7 - linha
    return chess.square(coluna, 7 - linha)

def coordenada_para_linha_coluna(x, y, cor_jogador):
    coluna = x // TAMANHO_CASA
    linha = y // TAMANHO_CASA
    if cor_jogador == chess.BLACK:
        coluna = 7 - coluna
        linha = 7 - linha
    return linha, coluna

def menu():
    clock = pygame.time.Clock()
    cor = chess.WHITE
    dificuldade = 0.1
    escolhendo = True

    while escolhendo:
        tela.fill((20, 20, 20))
        
        # Título
        titulo = fonte_grande.render("Xadrez vs IA", True, (255, 255, 255))
        tela.blit(titulo, (TAMANHO_TABULEIRO // 2 - titulo.get_width() // 2, 40))

        # Configurações de botão
        largura_botao = 240
        altura_botao = 60
        espacamento = 40
        centro_x = TAMANHO_TABULEIRO // 2

        # Botões
        botao_brancas = pygame.Rect(centro_x - largura_botao - espacamento // 2, 120, largura_botao, altura_botao)
        botao_pretas = pygame.Rect(centro_x + espacamento // 2, 120, largura_botao, altura_botao)

        mouse_pos = pygame.mouse.get_pos()

        # Desenhar botão BRANCAS com efeito hover
        if botao_brancas.collidepoint(mouse_pos):
            pygame.draw.rect(tela, (90, 90, 255), botao_brancas, border_radius=10)
        else:
            pygame.draw.rect(tela, (70, 70, 240), botao_brancas, border_radius=10)

        # Desenhar botão PRETAS com efeito hover
        if botao_pretas.collidepoint(mouse_pos):
            pygame.draw.rect(tela, (240, 70, 70), botao_pretas, border_radius=10)
        else:
            pygame.draw.rect(tela, (220, 60, 60), botao_pretas, border_radius=10)

        # Textos dos botões com ▶
        texto_brancas = fonte.render("▶ Jogar como BRANCAS", True, (255, 255, 255))
        texto_pretas = fonte.render("▶ Jogar como PRETAS", True, (255, 255, 255))

        tela.blit(texto_brancas, (botao_brancas.centerx - texto_brancas.get_width() // 2, botao_brancas.centery - texto_brancas.get_height() // 2))
        tela.blit(texto_pretas, (botao_pretas.centerx - texto_pretas.get_width() // 2, botao_pretas.centery - texto_pretas.get_height() // 2))

        # Texto de dificuldade
        texto_dificuldade = fonte.render("Dificuldade: 1 - Fácil | 2 - Médio | 3 - Difícil", True, (200, 200, 200))
        tela.blit(texto_dificuldade, (TAMANHO_TABULEIRO // 2 - texto_dificuldade.get_width() // 2, 210))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if botao_brancas.collidepoint(x, y):
                    cor = chess.WHITE
                    escolhendo = False
                elif botao_pretas.collidepoint(x, y):
                    cor = chess.BLACK
                    escolhendo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    dificuldade = 0.01
                elif event.key == pygame.K_2:
                    dificuldade = 0.1
                elif event.key == pygame.K_3:
                    dificuldade = 1.0

        clock.tick(30)

    return cor, dificuldade



# --- JOGO ---
def main():
    cor_jogador, tempo_ia = menu()
    board = chess.Board()
    selecionado = None
    engine = chess.engine.SimpleEngine.popen_uci(CAMINHO_STOCKFISH)

    rodando = True
    while rodando:
        tela.fill((0, 0, 0))
        desenhar_tabuleiro(tela, board, cor_jogador, selecionado)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < TAMANHO_TABULEIRO and board.turn == cor_jogador:
                    linha, coluna = coordenada_para_linha_coluna(x, y, cor_jogador)
                    pos = posicao_para_peca(coluna, linha, cor_jogador)
                    peca = board.piece_at(pos)

                    if selecionado is None:
                        if peca and peca.color == cor_jogador:
                            selecionado = (linha, coluna)
                    else:
                        destino = posicao_para_peca(coluna, linha, cor_jogador)
                        move = chess.Move(posicao_para_peca(selecionado[1], selecionado[0], cor_jogador), destino)
                        if move in board.legal_moves:
                            board.push(move)
                            selecionado = None

                            # Movimento IA
                            if not board.is_game_over():
                                resultado = engine.play(board, chess.engine.Limit(time=tempo_ia))
                                board.push(resultado.move)
                        else:
                            selecionado = None

    engine.quit()
    pygame.quit()

if __name__ == '__main__':
    main()
