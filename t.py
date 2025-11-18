class A:

    palavras : str

    def __init__(self):
        self.palavras = "Samuel"

    def __str__(self):
        txt = f"Nome: {self.palavras}"
        return txt

class B:

    palavras : str

    def __init__(self):
        self.palavras = "Meneses"

    def __str__(self):
        txt = f"Sobrenome: {self.palavras}"
        return txt

class C:

    frase : str 

    def __init__(self):
        self.frase = [A(), B()]

    def __str__(self):
        txt = f"a - {self.frase[0]} b - {self.frase[1]}"
        return txt
    
cd = C()

print(cd)