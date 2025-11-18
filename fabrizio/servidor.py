import socket
import threading
import time

# --- Configurações de Rede ---
HOST = '127.0.0.1'
PORT = 12345
NUM_JOGADORES = 4

# --- Dicionário de Conexões ---
# Armazena as conexões ativas no formato {player_id: socket}
# Usamos um dicionário para 'enviar_privado' ser mais fácil
rede_conexoes = {}
rede_lock = threading.Lock() # Trava para proteger o dicionário

#
# =======================================================================
# == (A SUA CLASSE 'Jogo' VAI AQUI) ==
#
# Você vai criar sua classe Jogo e todo o seu sistema de lógica.
# Ela precisa ser "encaixada" abaixo.
#
# Exemplo de como sua classe Jogo será:
#
# class Jogo:
#     def __init__(self, enviar_privado_func, broadcast_func):
#         self.enviar_privado = enviar_privado_func
#         self.broadcast = broadcast_func
#         self.jogadores = {} # Seus objetos de jogador
#         self.estado = "AGUARDANDO"
#
#     def adicionar_jogador(self, player_id):
#         # (Sua lógica para criar um jogador)
#         self.enviar_privado(player_id, "Você foi registrado no jogo.")
#
#     def remover_jogador(self, player_id):
#         # (Sua lógica para remover um jogador)
#         self.broadcast(f"Jogador {player_id} saiu.")
#
#     def processar_comando(self, player_id, comando):
#         # (AQUI ENTRA TODA A SUA LÓGICA DE TURNOS, AÇÕES, ETC.)
#         self.broadcast(f"O Jogo recebeu '{comando}' do Jogador {player_id}")
#
# =======================================================================
#

# --- Funções "API" de Rede ---
# Estas são as funções que sua classe Jogo vai chamar.

def enviar_privado(player_id, mensagem):
    """Envia uma mensagem para um jogador específico."""
    try:
        with rede_lock:
            if player_id in rede_conexoes:
                socket_jogador = rede_conexoes[player_id]
                socket_jogador.send(mensagem.encode('utf-8'))
    except Exception as e:
        print(f"[REDE] Falha ao enviar privado para {player_id}: {e}")

def broadcast(mensagem):
    """Envia uma mensagem para todos os jogadores conectados."""
    try:
        with rede_lock:
            for socket_jogador in rede_conexoes.values():
                socket_jogador.send(mensagem.encode('utf-8'))
    except Exception as e:
        print(f"[REDE] Falha no broadcast: {e}")

# --- (COLOQUE SUA CLASSE 'Jogo' AQUI) ---
# ...
# ... (Por favor, cole sua classe Jogo aqui)
# ...

# --- (CRIAÇÃO DA INSTÂNCIA DO JOGO) ---
# Crie a instância única do seu jogo, passando as funções de rede.
# Exemplo (descomente quando sua classe Jogo estiver pronta):
#
# meu_jogo = Jogo(
#     enviar_privado_func=enviar_privado_rede,
#     broadcast_func=broadcast_rede
# )
#
# --- (FIM DA SEÇÃO DA SUA CLASSE) ---


def handle_client(client_socket, player_id):
    try:
    
        client_socket.send(f"Qual o seu nome, Jogador {player_id}?".encode('utf-8'))
        nome = client_socket.recv(1024).decode('utf-8').strip()
        
        
        meu_jogo.adicionar_jogador(player_id, nome)
        
        
        meu_jogo.enviar_privado(player_id, f"Bem-vindo, {nome}!")
    """
    Esta é a "orelha" de cada jogador.
    Ela roda em uma thread separada por jogador.
    """
    print(f"[REDE] Thread de escuta iniciada para Jogador {player_id}.")
    try:
        while True:
            # 1. Recebe a resposta
            mensagem_bytes = client_socket.recv(2048)
            if not mensagem_bytes:
                break # Cliente desconectou
            
            comando = mensagem_bytes.decode('utf-8').strip()
            if not comando:
                continue
            
            # 2. Entrega a resposta para a Lógica do Jogo
            
            meu_jogo.processar_comando(player_id, comando)
            
            # Linha temporária para teste (remove_depois):
            print(f"[REDE] Recebido de {player_id}: {comando}")
            broadcast_rede(f"[ECO] Jogador {player_id} disse: {comando}")


    except (ConnectionResetError, BrokenPipeError, EOFError):
        print(f"[REDE] Conexão com Jogador {player_id} perdida.")
        meu_jogo.remover_jogador(player_id)
    finally:
        # Limpa a conexão
        print(f"[REDE] Encerrando thread e limpando Jogador {player_id}.")
        with rede_lock:
            if player_id in rede_conexoes:
                del rede_conexoes[player_id]
            meu_jogo.remover_jogador(player_id)
        
        client_socket.close()
        
        # Avisa a Lógica do Jogo que o jogador saiu
        # (Descomente a linha abaixo quando 'meu_jogo' existir)
        # meu_jogo.remover_jogador(player_id)

def iniciar_servidor_rede():
    """Função principal que abre o servidor e gerencia o lobby."""
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
    except OSError:
        print(f"!!! ERRO: A porta {PORT} já está em uso.")
        return
        
    server_socket.listen(NUM_JOGADORES)
    print(f"[REDE] Servidor de rede escutando em {HOST}:{PORT}...")

    try:
        while True:
            num_atual = len(rede_conexoes)
            
            # --- (A SUA CLASSE 'Jogo' controlará se o jogo está em andamento) ---
            # Ex: if not meu_jogo.esta_em_andamento and num_atual < NUM_JOGADORES:
            
            if num_atual < NUM_JOGADORES: # Lógica de lobby simplificada
                
                client_socket, client_address = server_socket.accept()
                
                # Encontra um ID vago (1, 2, 3 ou 4)
                player_id = -1
                with rede_lock:
                    ids_ocupados = set(rede_conexoes.keys())
                    for i in range(1, NUM_JOGADORES + 1):
                        if i not in ids_ocupados:
                            player_id = i
                            break
                
                if player_id == -1:
                    client_socket.send("[ERRO] Servidor cheio.".encode('utf-8'))
                    client_socket.close()
                    continue

                # Adiciona o novo jogador ao dicionário de rede
                with rede_lock:
                    rede_conexoes[player_id] = client_socket
                
                print(f"[REDE] Jogador {player_id} ({client_address}) conectou.")
                
            
                

                # Inicia a thread de escuta para este jogador
                thread = threading.Thread(target=handle_client, args=(client_socket, player_id))
                thread.daemon = True
                thread.start()
            
            time.sleep(0.1) # Impede o loop de consumir 100% da CPU
            
    except KeyboardInterrupt:
        print("\n[REDE] Desligando...")
    finally:
        with rede_lock:
            for s in rede_conexoes.values():
                s.close()
        server_socket.close()
        print("[REDE] Servidor desligado.")

if __name__ == "__main__":
    # --- (Você precisa descomentar a criação da instância 'meu_jogo' acima) ---
    # if 'meu_jogo' not in locals():
    #    print("!!! ERRO: A classe 'Jogo' não foi definida ou instanciada.")
    #    print("!!! Edite o script e adicione sua classe 'Jogo'.")
    # else:
    #    iniciar_servidor_rede()
    
    # Linha temporária para teste (remova quando 'meu_jogo' estiver pronto):
    print("[AVISO] Rodando em modo de 'ECO'. A Lógica do Jogo não está conectada.")
    iniciar_servidor_rede()