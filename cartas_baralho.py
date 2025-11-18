from abc import ABC, abstractmethod
from random import shuffle

class Carta(ABC):
    nome : str
    tipo_acao : str
    bloqueia : list

    @abstractmethod
    def acao(self, **kwargs):
        pass

    @abstractmethod
    def bloqueio(self, c : "Carta"):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return f"Carta: {self.nome}"

class Capitao(Carta):

    def __init__(self) -> None:
        self.nome = "Capitão"
        self.tipo_acao = "ROUBAR"
        self.bloqueia = ["ROUBAR"]

    def acao(self, **kwargs) -> None:
        # entrada: j_alvo = jogador alvo, j_atk = jogador atacante
        alvo = kwargs['j_alvo']
        atk = kwargs['j_atk']
        if alvo.moedas >= 2:
            alvo.moedas -= 2
            atk.moedas += 2
        else:
            atk.moedas += alvo.moedas
            alvo.moedas = 0

    def bloqueio(self, c : "Carta") -> bool:
        # True bloqueia, False não bloqueia
        return c.tipo_acao in self.bloqueia
    
    def __str__(self) -> str:
        bloqueia_str = ", " .join(self.bloqueia)
        txt = f"Nome: {self.nome}\nAção: {self.tipo_acao}\nBloqueia: {bloqueia_str}"
        return txt 
    
class Assassino(Carta):

    def __init__(self) -> None:
        self.nome = "Assassino"
        self.tipo_acao = "ASSASSINAR"
        self.bloqueia = []

    def acao(self, **kwargs) -> None:
        # entrada: j_alvo = jogador alvo, j_atk = jogador atacante, carta_rm = cartas remover, banco = banco
        alvo = kwargs['j_alvo']
        atk = kwargs['j_atk']
        banco = kwargs['banco']
        carta_rm = kwargs['carta']

        banco.add_moedas(atk, 3)
        alvo.deck.remove(carta_rm)      

    def bloqueio(self, c) -> bool:
        return False 

    def __str__(self) -> str:
        txt = f"Nome: {self.nome}\nAção: {self.tipo_acao}\nBloqueia: Não possui bloqueio"
        return txt

class Duque(Carta):

    def __init__(self) -> None:
        self.nome = "Duque"
        self.tipo_acao = "TRIBUTARIO"
        self.bloqueia = ["AJUDA EXTERNA"]

    def acao(self, **kwargs) -> None:
        # entrada: j_atk = jogador atacante, banco = banco
        atk = kwargs['j_atk']
        banco = kwargs['banco']
        banco.remove(atk, 3)

    def bloqueio(self, c : "Carta") -> bool:
        # True bloqueia, False não bloqueia
        return c.tipo_acao in self.bloqueia

    def __str__(self) -> str:
        bloqueia_str = ", " .join(self.bloqueia)
        txt = f"Nome: {self.nome}\nAção: {self.tipo_acao}\nBloqueia: {bloqueia_str}"
        return txt

class Embaixador(Carta):

    def __init__(self) -> None:
        self.nome = "Embaixador"
        self.tipo_acao = "TROCA-CARTA"
        self.bloqueia = ["ROUBAR"]

    def acao(self, **kwargs) -> None:
        # entrada: j_atk = jogador atacante, baralho = baralho
        atk = kwargs['j_atk']
        baralho = kwargs['baralho']
        atk.deck.append(baralho.remove())
        atk.deck.append(baralho.remove())
        num_cartas = len(atk.deck)

        print("Deck atual -")
        for i in range(num_cartas):
            print(f"{i+1}")
            print(f"{atk.deck[i]}\n")
        
        while True:
            try:
                cartas_rm = input("Digite o numero das duas carta que seja devolver para o baralho: ").split()
                a = int(cartas_rm[0])
                b = int(cartas_rm[1])

                if 1 <= a <= (num_cartas) and 1 <= b <= (num_cartas) and a != b:
                    if(a < b):
                        baralho.insert(atk.deck[b-1])
                        del atk.deck[b-1]
                        baralho.insert(atk.deck[a-1])
                        del atk.deck[a-1]
                    else:
                        baralho.insert(atk.deck[a-1])
                        del atk.deck[a-1]
                        baralho.insert(atk.deck[b-1])
                        del atk.deck[b-1]

                    print(f"Baralho atual: \n")
                    for i in atk.deck:
                        print(f"{i}\n") 
                    
                    break
                else:
                    print("--------------------------------------------------------------------------------------------------------------")
                    print("Erro! Digite dois numeros diferentes, cada um correspondete a uma carta e sepadoros por espaço, ex.: num1 num2")
                    print("--------------------------------------------------------------------------------------------------------------")

            except ValueError:
                print("--------------------------------------------------------------------------------------------------------------")
                print("Erro! Digite dois numeros diferentes, cada um correspondete a uma carta e sepadoros por espaço, ex.: num1 num2")
                print("--------------------------------------------------------------------------------------------------------------")


    def bloqueio(self, c : "Carta") -> bool:
        # True bloqueia, False não bloqueia
        return c.tipo_acao in self.bloqueia

    def __str__(self):
        bloqueia_str = ", " .join(self.bloqueia)
        txt = f"Nome: {self.nome}\nAção: {self.tipo_acao}\nBloqueia: {bloqueia_str}"
        return txt
    
class Condessa(Carta):
    
    def __init__(self) -> None:
        self.nome = "Condessa"
        self.tipo_acao = "Não Possui"
        self.bloqueia = ["ASSASSINAR"]

    def acao(self, **kwargs) -> None:
        print("Não possui ação")


    def bloqueio(self, c : "Carta") -> bool:
        # True bloqueia, False não bloqueia
        return c.tipo_acao in self.bloqueia

    def __str__(self):
        bloqueia_str = ", " .join(self.bloqueia)
        txt = f"Nome: {self.nome}\nAção: {self.tipo_acao}\nBloqueia: {bloqueia_str}"
        return txt

class Baralho:

    def __init__(self):
        self.cartas = []
        for i in range(3):
            self.cartas.append(Capitao())
            self.cartas.append(Assassino())
            self.cartas.append(Duque())
            self.cartas.append(Embaixador())
            self.cartas.append(Condessa())          
            self.embaralhar()  

    def remove(self):
        return self.cartas.pop(0)
    
    def insert(self, carta : Carta):
        self.cartas.append(carta)

    def embaralhar(self):
        shuffle(self.cartas)

    def __repr__(self):
        num_cartas = len(self.cartas)
        txt = f"Numero de cartas: {num_cartas}\n"
        for c in self.cartas:
            txt += f"{c.nome}\n"
        return txt
    
    def __str__(self):
        tam_baralho = len(self.cartas)
        txt = f"Numero de cartas: {tam_baralho}"
        return txt