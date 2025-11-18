from typing import Callable
import time

class Banco:
    moedas : int


    def __init__(self) -> None:
        self.moedas = 54

    def add_moedas(self, j: int, n_moedas : int) -> None:
        if j.moedas >= n_moedas:
            j.moedas -= n_moedas
            self.moedas += n_moedas
        else:
            raise ValueError("Saldo insuficiente...") 

    def remove(self, j : "Jogador", n_moedas : int) -> None:
        if self.moedas >= n_moedas:
            j.moeda += n_moedas
            self.moedas -= n_moedas
        else:
            j.moedas += self.moedas
            self.moedas = 0
            raise ValueError(f"Banco sem dinheiro suficiente...\nValor retirado: {self.moedas}")



class Jogo:
    banco: Banco
    enviar_privado: Callable
    broadcast: Callable
    jogadores = {}
    jogador_turno: int
    acao_pendente = {}
    jogador_alvo: int
    estado: str
    janela_de_tempo: float
    tempo_inicio_contestacao: float
    jogador_turno: int

    def __init__(self,enviar_privado, broadcast):
        self.enviar_privado = enviar_privado
        self.broadcast = broadcast
        self.jogadores = {}
        self.estado = "aguardando_ação"
        self.banco = Banco()
        self.janela_tempo = 20.0
        self.tempo_inicio_contestacao = 0.0
        self.lock = threading.lock()
        self.jogador_turno = 1

    def adicionar_jogador(self,player_id,nome):
        novo_jogador = jogador(nome)
        self.jogadores[player_id] = novo_jogador
        self.broadcast(f"{nome} (jogador{player_id}) entrou")

        

    def remover_jogador(self,player_id):
        # Remove a chave se ela existir, caso contrario retorna None
        nome_removido = self.jogadores.pop(player_id, None)

        if nome_removido is not None:
            self.broadcast(f"jogador {player_id} ({nome_removido}) foi eliminado.")
        verificar_vencedor()


            
    



def processar_comando(self, player_id, comando):
    

    with self.lock:
        
        comando_limpo = comando.strip().lower() 

        if self.estado == "aguardando_ação":
            
            if player_id != self.jogador_turno:
                self.enviar_privado(player_id, "Não é a sua vez de jogar ESPERTINHO")
                return

            #  Ação RENDA 
            if comando_limpo == "renda":
                
                self.banco.remover_moedas(self.jogadores[player_id], 1)
                self.jogadores[player_id].moedas += 1
            
                self.broadcast(f"Jogador {player_id} pegou 1 moeda (Renda).")
                self.passar_turno() 

            #  Ação AJUDA EXTERNA 
            elif comando_limpo == "ajuda externa":
                
                self.estado = "aguardando_BLOQUEIO_ajuda_externa"
                self.tempo_inicio_contestacao = time.time()

                self.broadcast(f"jogador {player_id} quer pegar Ajuda Externa (2 moedas).")
                self.broadcast("Alguém bloqueia com o Duque? (20s para digitar 'bloquear')")
            
            # Adicionar outras ações aqui: elif comando_limpo == "assassinar"/"roubar" e por ai vai...)

        
        elif self.estado == "aguardando_BLOQUEIO_ajuda_externa":
            
            # se alguem bloquear:
            if comando_limpo == "bloquear":
                
                self.broadcast(f"Jogador {player_id} bloqueou a Ajuda Externa com o Duque!")
                self.broadcast("Alguém contesta o Duque dele? (20s para 'contestar')")

                # muda o estado e espera para ver se algum jogador contesta o bloqueio
                self.estado = "aguardando_CONTESTACAO_do_bloqueio"
                
                # Salvo a ação em um dicionario para que a função resolver.bloqueio() resolva
                self.acao_pendente = {"autor_acao": self.jogador_turno,"acao": "ajuda externa","bloqueador": player_id}
                
                # reinicia o timer 
                self.tempo_inicio_contestacao = time.time()
                
            
            else:
                tempo_passado = time.time() - self.tempo_inicio_contestacao
                
                if tempo_passado > self.janela_de_tempo:
                    # se ninguém fizer nada:
                    self.broadcast(f"Tempo acabou. Ninguém bloqueou.")
                    
                    self.estado = "aguardando_ação"
                    self.executar_acao(self.acao_turno)
                    self.passar_turno()
                    
                    
        elif self.estado == "aguardando_CONTESTACAO_do_bloqueio":
            
            #  se alguém contestar o bloqueio:
            if comando_limpo == "contestar":
                self.broadcast(f"Jogador {player_id} contestou o bloqueio!")

                self.resolver_contestacao_de_bloqueio(player_id,self.acao_pendente["bloqueador"])
                
                # self.duque.bloqueio (instância do jogador contestado, instância do jogador que esta contestando)
                self.estado = "aguardando_ação"
                self.passar_turno()

            # Se ninguém contestar o bloqueio:
            else:
                tempo_passado = time.time() - self.tempo_inicio_contestacao
                
                if tempo_passado > self.janela_de_tempo:
                    self.broadcast(f"Tempo acabou. Ninguém contestou o bloqueio.")
                    self.broadcast("O bloqueio foi bem-sucedido. A Ajuda Externa falhou.")
                    
                    self.estado = "aguardando_ação"
                    self.passar_turno()
             
            

                
                    

    # avisa que o jogo começou e pergunta para o jogador do turno o que ele quer fazer        
    def iniciar_jogo(self)


    def verificar_vencedor(self):
        if Len(jogadores) == 1:
           vencedor = list(self.jogadores.values())[0]
           self.broadcast(f"o jogo acabou {vencedor.nome.upper()} é o vencedor!!!!")
           self.estado = "fim de jogo"


        