from jogo import *



###############################################################################
################################# Perguntas ###################################
###############################################################################

###############################################################################
################################ teste Banco ##################################
###############################################################################
"""
ban = Banco()
b = Baralho()
j = Jogador("Samuel", b)
print("Inicio")
print(ban)
print(f"")
print(j)

print("----------------------------")
print("Remove banco")
ban.remove(j, 10)
print(ban)
print(f"")
print(j)

print("----------------------------")
print("Remove banco, valor > saldo banco")
ban.remove(j, 45)
print(ban)
print(f"")
print(j)

print("----------------------------")
print("Add banco")
ban.add_moedas(j, 10)
print(ban)
print(f"")
print(j)

print("----------------------------")
print("Add banco, valor > saldo jogador")
ban.add_moedas(j, 47)
print(ban)
print(f"")
print(j)
"""

###############################################################################
############################### teste Baralho #################################
###############################################################################
"""
b = Baralho()
em = Embaixador()
print("----------------------------")
print(b)
print("----------------------------")
print(repr(b))

print("----------------------------")
print("Embaralhar")
b.embaralhar()
print(repr(b))

print("----------------------------")
print("Remover")
b.remove()
b.remove()
b.remove()
print(repr(b))

print("----------------------------")
print("Inserir")
b.insert(em)
b.insert(em)
b.insert(em)
print(repr(b))
"""

###############################################################################
################################ teste Cartas #################################
###############################################################################
"""
ca = Capitao()
ass = Assassino()
du = Duque()
em = Embaixador()
com = Condessa()
ba = Baralho()
ban = Banco()

print(f"\n\n----------------------------")
print(ca)
print("----------------------------")
print(ass)
print("----------------------------")
print(du)
print("----------------------------")
print(em)
print("----------------------------")
print(com)
print(f"----------------------------\n\n")
j1 = Jogador("Samuel", ba)
j2 = Jogador("Vitoria", ba)

print("Inicio")
print(j1)
print(j2)

print("----------------------------")
print("Capitão")
ca.acao( j_alvo = j2, j_atk = j1)
print(j1)
print(j2)

print("----------------------------")
print("Assassino")
c = j2.deck[0]
ass.acao(j_alvo = j2, j_atk = j1, banco = ban, carta = c)
print(j1)
print(j2)

print("----------------------------")
print("Duque")
du.acao(j_atk = j2, banco = ban)
print(j1)
print(j2)

print("----------------------------")
print("Embaixador")
em.acao(j_atk = j2, baralho = ba)
print(j1)
print(j2)

print("----------------------------")
print("Condessa")
com.acao()
print(j1)
print(j2)
"""

###############################################################################
############################### teste Jogador #################################
###############################################################################
"""
b = Baralho()
ban = Banco()
j1 = Jogador("Samuel", b)
j2 = Jogador("Vitoria", b)

print("Inicio")
print(j1)
print(j2)

print("----------------------------")
print("Perder influencia")
c = j1.deck[0]
j1.perder_influencia(c)
print(j1)
print(j2)

print("----------------------------")
print("Renda")
j1.renda(ban)
j2.renda(ban)
print(j1)
print(j2)

print("----------------------------")
print("Ajuda Externa")
j1.ajuda_externa(ban)
j1.ajuda_externa(ban)
j2.ajuda_externa(ban)
print(j1)
print(j2)

print("----------------------------")
print("Glope")
j1.golpe(ban, j2, j2.deck[0])
print(j1)
print(j2)
"""

###############################################################################
################################# teste Jogo ##################################
###############################################################################
"""
jogo = Jogo()
print(jogo)
"""

