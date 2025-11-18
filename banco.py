
class Banco:
    dinheirinhos_brasileiros : int

    def __init__(self) -> None:
        self.dinheirinhos_brasileiros = 54

    def add_moedas(self, j : "Jogador", n_moedas : int) -> None:
        if j.moedas >= n_moedas:
            j.moedas -= n_moedas
            self.dinheirinhos_brasileiros += n_moedas
        else:
            print(f"{j.nome} não possui moedas suficientes para transferir {n_moedas}.")

    def remove(self, j : "Jogador", n_moedas : int) -> None:
        if self.dinheirinhos_brasileiros >= n_moedas:
            j.moedas += n_moedas
            self.dinheirinhos_brasileiros -= n_moedas
        else:
            retirado = self.dinheirinhos_brasileiros
            j.moedas += self.dinheirinhos_brasileiros
            self.dinheirinhos_brasileiros = 0
            print(f"Banco sem dinheiro suficiente. Valor solicitado: {n_moedas}, valor retirado: {retirado}")
        
    def __str__(self):
        txt = f"Saldo: {self.dinheirinhos_brasileiros}"
        return txt
        
