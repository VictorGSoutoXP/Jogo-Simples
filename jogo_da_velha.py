def exibir_tabuleiro(tab):
    print("\n")
    print(f" {tab[0]} | {tab[1]} | {tab[2]} ")
    print("---|---|---")
    print(f" {tab[3]} | {tab[4]} | {tab[5]} ")
    print("---|---|---")
    print(f" {tab[6]} | {tab[7]} | {tab[8]} ")
    print("\n")


def verificar_vencedor(tab, jogador):
    combinacoes = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]              # Diagonais
    ]
    for c in combinacoes:
        if tab[c[0]] == tab[c[1]] == tab[c[2]] == jogador:
            return True
    return False


def jogo_da_velha():
    tabuleiro = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    jogador_atual = "X"
    jogadas = 0

    while True:
        exibir_tabuleiro(tabuleiro)
        escolha = input(f"Jogador {jogador_atual}, escolha uma posição (1-9): ")

        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > 9:
            print("Escolha inválida. Tente novamente.")
            continue

        posicao = int(escolha) - 1

        if tabuleiro[posicao] in ["X", "O"]:
            print("Essa posição já está ocupada. Tente outra.")
            continue

        tabuleiro[posicao] = jogador_atual
        jogadas += 1

        if verificar_vencedor(tabuleiro, jogador_atual):
            exibir_tabuleiro(tabuleiro)
            print(f"🏆 Jogador {jogador_atual} venceu!")
            break

        if jogadas == 9:
            exibir_tabuleiro(tabuleiro)
            print("⚖️ Deu velha! Empate!")
            break

        jogador_atual = "O" if jogador_atual == "X" else "X"


# Iniciar o jogo
jogo_da_velha()
