from cartas_baralho import *
from jogador import *
from banco import *

class Jogo:
    num_jogador : int

    def __init__(self):
        self.banco = Banco()
        self.baralho = Baralho()
        self.jogadores = []
        self.iniciar_jogadores()

    def iniciar_jogadores(self):
        n = int(input("Digite o numero de jogadores: "))
        for i in range(n):
            nome = input(f"Nome do jogador {i}: ")
            self.jogadores.append(Jogador(nome, self.baralho))
            print(f"--------------------------------------------")

        print(f"Jogadores criados com sucesso!")
        for j in self.jogadores:
            print(f"Nome: {j.nome}")
        print(f"\n")

    def remover_carta(self):
        pass

    def sacar(self):
        pass

    def depositar(self):
        pass

    def __str__(self):
        txt =  f"Jogadores -\n"
        for j in self.jogadores:
            txt += f"{j}\n"
        txt += f"\n"
        txt += f"Baralho -\n{self.baralho}\n"
        txt += f"Banco -\n{self.banco}"
        return txt
    

