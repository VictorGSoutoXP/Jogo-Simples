import random

TAMANHO = 5
NUM_MINAS = 3

def criar_tabuleiro():
    return [["_" for _ in range(TAMANHO)] for _ in range(TAMANHO)]

def gerar_minas():
    minas = set()
    while len(minas) < NUM_MINAS:
        mina = (random.randint(0, TAMANHO-1), random.randint(0, TAMANHO-1))
        minas.add(mina)
    return minas

def contar_minas_vizinhas(linha, coluna, minas):
    vizinhos = [
        (linha-1, coluna-1), (linha-1, coluna), (linha-1, coluna+1),
        (linha, coluna-1),                   (linha, coluna+1),
        (linha+1, coluna-1), (linha+1, coluna), (linha+1, coluna+1)
    ]
    return sum((v in minas) for v in vizinhos if 0 <= v[0] < TAMANHO and 0 <= v[1] < TAMANHO)

def exibir_tabuleiro(tabuleiro):
    print("   " + " ".join(str(i) for i in range(TAMANHO)))
    for i, linha in enumerate(tabuleiro):
        print(f"{i}  " + " ".join(linha))
    print()

def jogar():
    tabuleiro = criar_tabuleiro()
    minas = gerar_minas()
    reveladas = set()

    while True:
        exibir_tabuleiro(tabuleiro)
        try:
            linha = int(input("Digite a linha (0 a 4): "))
            coluna = int(input("Digite a coluna (0 a 4): "))
        except ValueError:
            print("❌ Entrada inválida. Digite números válidos.")
            continue

        if not (0 <= linha < TAMANHO and 0 <= coluna < TAMANHO):
            print("❌ Coordenadas fora do tabuleiro.")
            continue

        if (linha, coluna) in reveladas:
            print("⚠️ Essa posição já foi revelada.")
            continue

        if (linha, coluna) in minas:
            print("💥 BOOM! Você pisou numa mina!")
            break

        minas_ao_redor = contar_minas_vizinhas(linha, coluna, minas)
        tabuleiro[linha][coluna] = str(minas_ao_redor)
        reveladas.add((linha, coluna))

        if len(reveladas) == TAMANHO*TAMANHO - NUM_MINAS:
            exibir_tabuleiro(tabuleiro)
            print("🎉 Parabéns! Você venceu o Campo Minado!")
            break

# Iniciar o jogo
jogar()
