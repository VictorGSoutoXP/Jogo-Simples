import random

def jogar():
    opcoes = ["pedra", "papel", "tesoura"]
    print("\n🎮 Bem-vindo ao Pedra, Papel e Tesoura!")
    
    while True:
        jogador = input("Escolha [pedra, papel, tesoura] ou 'sair' para encerrar: ").lower()
        
        if jogador == "sair":
            print("👋 Até a próxima!")
            break
        if jogador not in opcoes:
            print("❌ Escolha inválida. Tente novamente.")
            continue
        
        computador = random.choice(opcoes)
        print(f"🤖 Computador escolheu: {computador}")
        
        if jogador == computador:
            print("⚖️ Empate!")
        elif (jogador == "pedra" and computador == "tesoura") or \
             (jogador == "papel" and computador == "pedra") or \
             (jogador == "tesoura" and computador == "papel"):
            print("✅ Você venceu!")
        else:
            print("❌ Você perdeu!")

# Iniciar o jogo
jogar()
