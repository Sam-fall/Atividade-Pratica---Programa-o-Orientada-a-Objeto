import threading
import time
from typing import Callable, Dict, List

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
    def __init__(self, enviar_privado, broadcast):
        self.estado = "aguardando_ação"
        self.lock = threading.Lock()
        self.jogadores = {}
        self.banco = Banco()
        self.baralho = Baralho()
        self.acao_pendente = {}
        self.enviar_privado = enviar_privado
        self.broadcast = broadcast
        self.jogador_turno = 0
        self.janela_de_tempo = 30.0
        self.tempo_inicio_contestacao = 0.0

        self.cartas_modelo = {
            "taxa": Duque(),
            "roubar": Capitao(),
            "assassinar": Assassino(),
            "trocar": Embaixador()
        }

        self.regras_bloqueio = {
            "ajuda externa": [Duque()],
            "roubar": [Capitao(), Embaixador()],
            "assassinar": [Condessa()]
        }

    def adicionar_jogador(self, player_id, nome):
        if player_id not in self.jogadores:
            self.jogadores[player_id] = Jogador(player_id, nome)
            self.broadcast(f"{nome} (ID {player_id}) entrou.")

    def remover_jogador(self, player_id):
        if player_id in self.jogadores:
            del self.jogadores[player_id]
            self.broadcast(f"Jogador {player_id} saiu.")
            self.verificar_vencedor()

    def iniciar_jogo(self):
        if len(self.jogadores) < 2: return
        self.baralho = Baralho()
        
        ids = sorted(self.jogadores.keys())
        self.jogador_turno = ids[0]

        for pid, jogador in self.jogadores.items():
            jogador.moedas = 2
            jogador.deck = [self.baralho.remove(), self.baralho.remove()]
            jogador.vivo = True
            cartas_str = ", ".join([c.nome for c in jogador.deck])
            self.enviar_privado(pid, f"Cartas: {cartas_str} | Moedas: 2")

        self.estado = "aguardando_ação"
        self.broadcast(f"Jogo iniciado. Turno do Jogador {self.jogador_turno}.")

    def passar_turno(self):
        ids = sorted(self.jogadores.keys())
        if not ids: return
        try:
            idx = ids.index(self.jogador_turno)
        except ValueError:
            idx = 0

        for _ in range(len(ids)):
            idx = (idx + 1) % len(ids)
            prox_id = ids[idx]
            if self.jogadores[prox_id].vivo:
                self.jogador_turno = prox_id
                self.broadcast(f"--- Vez do Jogador {self.jogador_turno} ---")
                self.enviar_privado(self.jogador_turno, "Sua vez.")
                return

    def verificar_vencedor(self):
        vivos = [j for j in self.jogadores.values() if j.vivo]
        if len(vivos) == 1:
            self.broadcast(f"VENCEDOR: {vivos[0].nome}!")
            self.estado = "fim de jogo"

    def escolher_perda_carta(self, player_id):
        if player_id not in self.jogadores: return
        jogador = self.jogadores[player_id]
        
        if not jogador.deck:
            jogador.vivo = False
            self.verificar_vencedor()
            return

        if len(jogador.deck) == 1:
            self.perder_carta(player_id, jogador.deck[0].nome)
        else:
            self.estado = "aguardando_ESCOLHA_PERDA_CARTA"
            self.acao_pendente["vitima"] = player_id
            self.tempo_inicio_contestacao = time.time()
            self.enviar_privado(player_id, "Escolha uma carta para perder.")

    def perder_carta(self, player_id, nome_carta):
        jogador = self.jogadores[player_id]
        carta_removida = None
        for i, c in enumerate(jogador.deck):
            if c.nome.lower() == nome_carta.lower():
                carta_removida = jogador.deck.pop(i)
                break
        
        if not carta_removida and jogador.deck:
            carta_removida = jogador.deck.pop(0)

        if carta_removida:
            self.broadcast(f"{jogador.nome} perdeu: {carta_removida.nome}")

        if not jogador.deck:
            jogador.vivo = False
            self.broadcast(f"{jogador.nome} foi eliminado.")
            self.verificar_vencedor()

        if self.estado != "fim de jogo":
            self.estado = "aguardando_ação"
            self.passar_turno()

    def trocar_carta_revelada(self, player_id, nome_carta):
        jogador = self.jogadores[player_id]
        for i, c in enumerate(jogador.deck):
            if c.nome == nome_carta:
                velha = jogador.deck.pop(i)
                self.baralho.insert(velha)
                self.baralho.embaralhar()
                jogador.deck.append(self.baralho.remove())
                self.enviar_privado(player_id, f"Nova carta: {jogador.deck[-1].nome}")
                break

    def processar_comando(self, player_id, comando):
        with self.lock:
            if self.estado == "fim de jogo": return
            if player_id not in self.jogadores: return
            if self.estado != "aguardando_ESCOLHA_PERDA_CARTA" and not self.jogadores[player_id].vivo: return

            cmd_parts = comando.strip().lower().split()
            cmd_base = cmd_parts[0] if cmd_parts else ""

            if self.estado == "aguardando_ação":
                if player_id != self.jogador_turno: return

                self.acao_pendente = {"autor_acao": player_id, "acao": cmd_base}
                if len(cmd_parts) > 1 and cmd_parts[1].isdigit():
                    self.acao_pendente["alvo"] = int(cmd_parts[1])

                if cmd_base in ["taxa", "trocar"]:
                    self.estado = f"aguardando_CONTESTACAO_{cmd_base}"
                    self.broadcast(f"{player_id} declarou {cmd_base}. Contestar?")
                    self.tempo_inicio_contestacao = time.time()

                elif cmd_base in ["roubar", "assassinar"]:
                    if cmd_base == "assassinar" and self.jogadores[player_id].moedas < 3:
                        self.enviar_privado(player_id, "Moedas insuficientes.")
                        return
                    self.estado = f"aguardando_REACAO_{cmd_base}"
                    self.broadcast(f"{player_id} declarou {cmd_base}. Bloquear/Contestar?")
                    self.tempo_inicio_contestacao = time.time()

                elif cmd_base == "ajuda externa":
                    self.estado = "aguardando_BLOQUEIO_ajuda_externa"
                    self.broadcast(f"{player_id} pede Ajuda Externa. Bloquear?")
                    self.tempo_inicio_contestacao = time.time()

                elif cmd_base in ["renda", "golpe"]:
                    self.executar_acao_pendente(self.acao_pendente)

            elif self.estado == "aguardando_ESCOLHA_PERDA_CARTA":
                if player_id == self.acao_pendente.get("vitima"):
                    self.perder_carta(player_id, cmd_base)

            elif self.estado == "aguardando_ESCOLHA_TROCA":
                if player_id == self.acao_pendente["autor_acao"]:
                    nomes = comando.strip().split()
                    if len(nomes) == 2:
                        jogador = self.jogadores[player_id]
                        temp_mao = [c.nome.lower() for c in jogador.deck]
                        valido = True
                        for n in nomes:
                            if n.lower() in temp_mao:
                                temp_mao.remove(n.lower())
                            else:
                                valido = False
                        
                        if valido:
                            kwargs = {
                                "j_atk": jogador,
                                "baralho": self.baralho,
                                "cartas_devolver": nomes
                            }
                            carta = self.cartas_modelo["trocar"]
                            msg = carta.acao(**kwargs)
                            self.broadcast(msg)
                            self.estado = "aguardando_ação"
                            self.passar_turno()
                        else:
                            self.enviar_privado(player_id, "Cartas inválidas.")

            elif self.estado == "aguardando_REACAO_roubo":
                if cmd_base == "contestar":
                    self.resolver_contestacao_de_acao(player_id, self.acao_pendente["autor_acao"], "Capitao")
                elif cmd_base == "bloquear":
                    if player_id == self.acao_pendente["alvo"]:
                        self.estado = "aguardando_ESCOLHA_BLOQUEIO_ROUBO"
                        self.acao_pendente["bloqueador"] = player_id
                        self.tempo_inicio_contestacao = time.time()
                        self.enviar_privado(player_id, "Qual carta? (capitao/embaixador)")
                elif time.time() - self.tempo_inicio_contestacao > self.janela_de_tempo:
                    self.executar_acao_pendente(self.acao_pendente)

            elif self.estado == "aguardando_ESCOLHA_BLOQUEIO_ROUBO":
                if player_id == self.acao_pendente["bloqueador"]:
                    if cmd_base in ["capitao", "embaixador"]:
                        self.acao_pendente["carta_reivindicada"] = cmd_base
                        self.estado = "aguardando_CONTESTACAO_do_bloqueio"
                        self.tempo_inicio_contestacao = time.time()
                        self.broadcast(f"{player_id} bloqueia com {cmd_base}. Contestar?")
                    elif time.time() - self.tempo_inicio_contestacao > self.janela_de_tempo:
                        self.executar_acao_pendente(self.acao_pendente)

            elif self.estado == "aguardando_CONTESTACAO_do_bloqueio":
                if cmd_base == "contestar":
                    self.resolver_contestacao_de_bloqueio(player_id, self.acao_pendente["bloqueador"])
                elif time.time() - self.tempo_inicio_contestacao > self.janela_de_tempo:
                    self.broadcast("Bloqueio aceito.")
                    self.estado = "aguardando_ação"
                    self.passar_turno()

            elif self.estado in ["aguardando_CONTESTACAO_taxa", "aguardando_CONTESTACAO_troca"]:
                if cmd_base == "contestar":
                    carta = "Duque" if "taxa" in self.estado else "Embaixador"
                    self.resolver_contestacao_de_acao(player_id, self.acao_pendente["autor_acao"], carta)
                elif time.time() - self.tempo_inicio_contestacao > self.janela_de_tempo:
                    self.executar_acao_pendente(self.acao_pendente)

            elif self.estado in ["aguardando_BLOQUEIO_ajuda_externa", "aguardando_REACAO_assassinato"]:
                if cmd_base == "contestar" and "assassinato" in self.estado:
                    self.resolver_contestacao_de_acao(player_id, self.acao_pendente["autor_acao"], "Assassino")
                elif cmd_base == "bloquear":
                    self.estado = "aguardando_CONTESTACAO_do_bloqueio"
                    self.acao_pendente["bloqueador"] = player_id
                    self.tempo_inicio_contestacao = time.time()
                    self.broadcast(f"{player_id} bloqueou. Contestar?")
                elif time.time() - self.tempo_inicio_contestacao > self.janela_de_tempo:
                    self.executar_acao_pendente(self.acao_pendente)

    def resolver_contestacao_de_bloqueio(self, contestador_id, bloqueador_id):
        bloqueador = self.jogadores[bloqueador_id]
        contestador = self.jogadores[contestador_id]
        acao_original = self.acao_pendente["acao"]
        
        carta_ref = None
        if acao_original == "roubar":
            nome_escolhido = self.acao_pendente.get("carta_reivindicada", "").lower()
            for c in self.regras_bloqueio["roubar"]:
                if c.nome.lower() == nome_escolhido:
                    carta_ref = c
                    break
        elif acao_original in self.regras_bloqueio:
            carta_ref = self.regras_bloqueio[acao_original][0]

        if not carta_ref: return

        vencedor_id = carta_ref.bloqueio(bloqueador, contestador)

        if vencedor_id == bloqueador_id:
            self.broadcast(f"Bloqueio válido. {bloqueador.nome} tem {carta_ref.nome}.")
            self.trocar_carta_revelada(bloqueador_id, carta_ref.nome)
            self.escolher_perda_carta(contestador_id)
        else:
            self.broadcast(f"Bloqueio falhou. {bloqueador.nome} blefou.")
            self.escolher_perda_carta(bloqueador_id)
            self.executar_acao_pendente(self.acao_pendente)

    def resolver_contestacao_de_acao(self, contestador_id, autor_id, carta_necessaria):
        autor = self.jogadores[autor_id]
        contestador = self.jogadores[contestador_id]
        
        tem_carta = any(c.nome == carta_necessaria for c in autor.deck)
        
        if tem_carta:
            self.broadcast(f"Contestação falhou. {autor.nome} tem {carta_necessaria}.")
            self.trocar_carta_revelada(autor_id, carta_necessaria)
            self.escolher_perda_carta(contestador_id)
            self.executar_acao_pendente(self.acao_pendente)
        else:
            self.broadcast(f"Contestação sucesso. {autor.nome} blefou.")
            self.escolher_perda_carta(autor_id)

    def executar_acao_pendente(self, acao_dict):
        if not acao_dict: return
        autor_id = acao_dict["autor_acao"]
        autor = self.jogadores[autor_id]
        tipo = acao_dict["acao"]
        alvo_id = acao_dict.get("alvo")
        alvo = self.jogadores.get(alvo_id) if alvo_id else None

        if tipo == "trocar":
            try:
                c1 = self.baralho.remove()
                c2 = self.baralho.remove()
                autor.deck.append(c1)
                autor.deck.append(c2)
                cartas_str = " ".join([c.nome for c in autor.deck])
                self.estado = "aguardando_ESCOLHA_TROCA"
                self.enviar_privado(autor_id, f"Suas cartas: {cartas_str}. Digite as 2 para devolver.")
                return
            except:
                self.estado = "aguardando_ação"
                self.passar_turno()
                return

        kwargs = {
            "j_atk": autor,
            "j_alvo": alvo,
            "banco": self.banco,
            "baralho": self.baralho,
            "jogo_ref": self
        }

        if tipo in self.cartas_modelo:
            carta = self.cartas_modelo[tipo]
            msg = carta.acao(**kwargs)
            if msg: self.broadcast(msg)

        elif tipo == "ajuda externa":
            self.banco.remove(autor, 2)
            self.broadcast(f"{autor.nome} recebeu Ajuda Externa.")

        elif tipo == "renda":
            self.banco.remove(autor, 1)
            self.broadcast(f"{autor.nome} pegou Renda.")

        elif tipo == "golpe":
            self.banco.add_moedas(autor, 7)
            self.broadcast(f"Golpe em {alvo.nome}!")
            self.escolher_perda_carta(alvo_id)
            return

        if tipo != "assassinar":
            self.estado = "aguardando_ação"
            self.passar_turno()