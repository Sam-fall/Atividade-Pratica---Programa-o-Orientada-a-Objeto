from cartas_baralho import *
from banco import *

class Jogador:
    nome : str
    moedas : int
    deck : list
    esta_vivo : bool

    def __init__(self, nome : str, baralho : Baralho):
        self.nome = nome
        self.moedas = 2
        self.deck = [baralho.remove(), baralho.remove()]
        self.esta_vivo = True

    def perder_influencia(self, c : "Carta"):
        self.deck.remove(c)
        num_carta = len(self.deck)
        if num_carta == 0:
            self.esta_vivo = False

    def renda(self, banco : Banco):
        banco.remove(self, 1)

    def ajuda_externa(self, banco : Banco):
        banco.remove(self, 2)

    def golpe(self, banco : Banco, j_alvo : "Jogador", c : Carta):
        banco.add_moedas(self, 7)
        j_alvo.perder_influencia(c)

    def __str__(self):
         num_carta = len(self.deck)
         txt = f"Nome: {self.nome}\nNumero de cartas: {num_carta}\nMoedas: {self.moedas}\nEsta vivo: {self.esta_vivo}\n"
         return txt


