# Atividade-Pratica---Programa-o-Orientada-a-Objeto

## Identificação do Grupo
* **Nome:** Fabrizio Jacinto  | **E-mail:** fabrizio.j@unisantos.br
* **Nome:** Samuel Meneses | **E-mail:** samuel.meneses@unisnatos.br

* **Link do Repositório:** 
https://github.com/Sam-fall/Atividade-Pratica---Programa-o-Orientada-a-Objeto.git

## Sobre o Projeto
Este projeto consiste na implementação do jogo de cartas **Coup** utilizando a linguagem Python. O objetivo principal é demonstrar a aplicação prática de conceitos fundamentais e avançados de **Programação Orientada a Objetos (POO)**.

Destaques da implementação:
* **Herança e Abstração:** Utilização da classe abstrata `Carta(ABC)` como base para todas as cartas do jogo, garantindo que todas as subclasses (`Capitao`, `Assassino`, `Duque`, etc.) implementem os métodos obrigatórios.
* **Polimorfismo:** Cada carta possui sua própria implementação dos métodos `acao()` e `bloqueio()`, permitindo comportamentos distintos para uma mesma chamada de método.
* **Gerenciamento de Estado:** A classe `Jogo` gerencia o fluxo de turnos, contestações e o estado de vida dos jogadores.

> **Nota sobre o desenvolvimento:** O projeto encontra-se em estágio de desenvolvimento. As mecânicas centrais de influência, renda e ações de personagens estão implementadas, mas funcionalidades como o loop de rede e finalização de partida podem apresentar limitações nesta versão.

## Configurações e Como Executar

### Pré-requisitos
Para executar este software, você precisará de:
* **Python 3.13.3** instalado.
* Bibliotecas padrão do Python (`abc`, `random`, `threading`, `time`, `typing`). Não é necessária a instalação de pacotes externos.

### Executando o Jogo
1. Certifique-se de que todos os arquivos do código fonte (`Classe_jogo.py`, `cartas_baralho.py`, `jogador.py`, `banco.py`) estão no mesmo diretório.
2. Abra o terminal na pasta do projeto.
3. Execute o arquivo principal do jogo:

```bash
python Classe_jogo.py
```
Implementação do jogo de carta Coup desenvolvida em Python. O projeto demonstra a aplicação prática de conceitos avançados de POO (herança, polimorfismo, encapsulamento) e documentação de software através de diagramas de classe UML (PlantUML/Mermaid).

---
 
# Coup
**Regras:** 

2-6 jogadores

No seu turno, você pode escolher uma ação para jogar. A ação que você escolhe pode ou não corresponder às influências que você possui. Para a ação que você escolher, outros jogadores podem potencialmente bloqueá-la ou desafiá-la.

Desafio: Quando um jogador declara uma ação ele está declarando para o resto dos jogadores que eles têm uma certa influência, e qualquer outro jogador pode desafiá-la. Quando um jogador é desafiado, o jogador desafiado deve revelar a influência correta associada à sua ação. Se revelarem a influência correta, o desafiante perderá uma influência. No entanto, se não conseguir revelar a influência correta, o jogador desafiado perderá sua influência revelada incorretamente.

Bloqueio: Quando qualquer uma das ações "Ajuda Estrangeira", "Roubar" e "Assasinar" são usadas, elas podem ser bloqueadas. Mais uma vez, qualquer jogador pode alegar ter a influência correta para bloquear. No entanto, os bloqueios também podem ser desafiados por qualquer jogador. Se um bloco falhar, a ação original ocorrerá.

Se um jogador perde todas as suas influências, está fora do jogo. O último jogador em pé ganha!

Neste momento, se um jogador se desconectar, o jogo deve ser recriado.

### **Ações Gerais:**
ROUBAR - ASSASSINAR - TRIBUTARIO - TROCA-CARTA - RENDA - AJUDA EXTERNA - GOLPE


## **Imfluências** 

### **Class Abstract -**
```python
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
```

### **Capitão -** 

**Ação:** ***ROUBAR*** 2 moedas do alvo.

**Bloqueado por:**  Capitão ou Embaixador.

**Bloqueio:** Bloqueia ***ROUBAR***.

```python
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
```

### **Assassino -**

**Ação:** ***ASSASSINAR*** Paga 3 moedas ao banco para assassinar uma influência do alvo.

**Bloqueado por:** Condessa.

**Bloqueio:** Não possui.

```python
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
```

### **Duque -**

**Ação:** ***TRIBUTARIO*** Pega 3 moedas do banco.

**Bloqueado por:** Não bloqueável.

**Bloqueio:** Bloqueia ***AJUDA EXTERNA***.

```python
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
```

### **Embaixador -**

**Ação:** ***TROCA-CARTA***  Pega duas cartas do deck e devolve duas.

**Bloqueado por:** Não bloqueável.

**Bloqueio:** Bloqueia ***ROUBAR***.

```python
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
```

### **Condessa -**

**Ação:** Não possui ação

**Bloqueado por:** Não bloqueável.

**Bloqueio:** Bloqueia ***ASSASSINAR***.

```python
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
```

## **Outras Ações**

### **Renda -**

**Ação:** ***RENDA*** Pega 1 modeda do banco

**Bloqueado por:** Não bloqueável

```python
    def renda(self, banco : Banco):
        banco.remove(self, 1)

```

### **Ajuda Externa -**

**Ação:** ***AJUDA EXTERNA*** Pega 2 moedas do banco

**Bloqueado por:** Duque

```python
    def ajuda_externa(self, banco : Banco):
            banco.remove(self, 2)
```

### **Golpe -**

**Ação:** ***GOLPE*** Paga 7 moedas para um alvo perde 1 influencia, caso comece o turno com 10 ou mais moedas é obrigatorio dar um golpe

**Bloqueado por:** Não bloqueável

```python
    def golpe(self, banco : Banco, j_alvo : "Jogador", c : Carta):
        banco.add_moedas(self, 7)
        j_alvo.perder_influencia(c)
```
