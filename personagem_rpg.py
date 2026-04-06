from abc import ABC, abstractmethod

# =========================
# CLASSE ABSTRATA (Heroi)
# =========================
class Heroi(ABC):
    def __init__(self, nome, hp):
        self._nome = nome  # encapsulado (protegido)
        self._hp = hp      # encapsulado (protegido)

    @abstractmethod
    def receber_dano(self, dano):
        pass

    def mostrar_status(self):
        print(f"{self._nome} | HP: {self._hp}")

    # Getter para provar encapsulamento (LSP)
    def get_hp(self):
        return self._hp


# =========================
# INTERFACE (Curavel)
# =========================
class Curavel(ABC):
    @abstractmethod
    def receber_cura(self, valor):
        pass


# =========================
# CLASSE GUERREIRO
# =========================
class Guerreiro(Heroi, Curavel):
    def __init__(self, nome, hp, armadura):
        super().__init__(nome, hp)
        self._armadura = armadura

    def receber_dano(self, dano):
        dano_reduzido = dano - self._armadura

        if dano_reduzido < 0:
            dano_reduzido = 0

        hp_antes = self._hp
        self._hp -= dano_reduzido

        if self._hp < 0:
            self._hp = 0

        print(f"{self._nome} (Guerreiro) | Armadura: {self._armadura}")
        print(f"   Dano original: {dano} -> Reduzido para: {dano_reduzido}")
        print(f"   HP: {hp_antes} -> {self._hp}\n")

    def receber_cura(self, valor):
        hp_antes = self._hp
        self._hp += valor
        print(f"{self._nome} (Guerreiro) | HP: {hp_antes} -> {self._hp} (+{valor})\n")


# =========================
# CLASSE MAGO
# =========================
class Mago(Heroi, Curavel):
    def __init__(self, nome, hp, mana):
        super().__init__(nome, hp)
        self._mana = mana

    def receber_dano(self, dano):
        hp_antes = self._hp
        mana_antes = self._mana
        
        if self._mana >= dano:
            self._mana -= dano
            print(f"{self._nome} (Mago) | Mana: {mana_antes} -> {self._mana}")
            print(f"   Dano {dano} completamente ABSORVIDO pela mana!")
            print(f"   HP permanece: {self._hp}\n")
        else:
            dano_restante = dano - self._mana
            self._mana = 0
            self._hp -= dano_restante

            if self._hp < 0:
                self._hp = 0

            print(f"{self._nome} (Mago) | Mana: {mana_antes} -> 0 (esgotou)")
            print(f"   Dano original: {dano} | Dano que passou: {dano_restante}")
            print(f"   HP: {hp_antes} -> {self._hp}\n")

    def receber_cura(self, valor):
        hp_antes = self._hp
        mana_antes = self._mana
        
        self._hp += valor
        self._mana += valor * 0.5
        
        print(f"{self._nome} (Mago) | HP: {hp_antes} -> {self._hp} (+{valor})")
        print(f"   Mana: {mana_antes} -> {self._mana} (+{valor*0.5})\n")


# =========================
# CLASSE BATALHA (POLIMORFISMO)
# =========================
class Batalha:
    def __init__(self, herois):
        self.herois = herois

    def bola_de_fogo(self, dano):
        print("\n" + "="*50)
        print(f"MESTRE LANCA BOLA DE FOGO! Dano: {dano}")
        print("="*50 + "\n")

        # POLIMORFISMO: cada herói reage de forma diferente
        for h in self.herois:
            h.receber_dano(dano)

    def aplicar_cura_todos(self, valor):
        print("\n" + "="*50)
        print(f"CURA EM AREA APLICADA! Valor: {valor}")
        print("="*50 + "\n")
        
        for h in self.herois:
            h.receber_cura(valor)

    def mostrar_todos(self):
        print("\n" + "="*50)
        print("STATUS FINAL DOS HEROIS")
        print("="*50)
        for h in self.herois:
            if isinstance(h, Mago):
                print(f"{h._nome} | HP: {h._hp} | Mana: {h._mana}")
            else:
                print(f"{h._nome} | HP: {h._hp}")
        print("="*50 + "\n")


# =========================
# TESTE DO SISTEMA COM PROVAS DO LSP
# =========================

print("\n" + "-"*50)
print("SISTEMA DE GUILDA - RPG")
print("-"*50 + "\n")

# Criando heróis
print("CRIANDO HEROIS:")
g1 = Guerreiro("Thor", 100, 10)
m1 = Mago("Merlin", 80, 50)
m2 = Mago("Gandalf", 90, 30)

print(f"OK {g1._nome} (Guerreiro) | HP: 100 | Armadura: 10")
print(f"OK {m1._nome} (Mago) | HP: 80 | Mana: 50")
print(f"OK {m2._nome} (Mago) | HP: 90 | Mana: 30\n")

# Grupo de heróis (todos são tratados como Heroi)
grupo = [g1, m1, m2]

# Criando batalha
batalha = Batalha(grupo)

# Ataque em área (POLIMORFISMO)
batalha.bola_de_fogo(30)

# Aplicando cura
batalha.aplicar_cura_todos(20)

# Mostrar status final
batalha.mostrar_todos()


# =========================
# PROVA DO PRINCIPIO DA SUBSTITUICAO DE LISKOV (LSP)
# =========================

print("\n" + "-"*50)

print(" TESTE DE SUBSTITUICAO:")
def testar_heroi_generico(heroi: Heroi, dano_teste: int):
    """Esta funcao aceita QUALQUER Heroi (Guerreiro ou Mago)"""
    hp_antes = heroi.get_hp()
    print(f"   Testando: {heroi._nome}")
    print(f"   HP antes: {hp_antes}")
    heroi.receber_dano(dano_teste)
    print(f"   HP depois: {heroi.get_hp()}")
    print(f"   OK! {heroi._nome} se comportou como Heroi\n")

# Criando heróis diferentes
heroi_teste_1 = Guerreiro("TesteGuerreiro", 100, 15)
heroi_teste_2 = Mago("TesteMago", 100, 40)

# Ambos funcionam na mesma funcao!
testar_heroi_generico(heroi_teste_1, 25)
testar_heroi_generico(heroi_teste_2, 25)

#A evolução do sistema proposto foi realizada com base nos princípios da Programação Orientada a Objetos, com o objetivo de garantir escalabilidade, reutilização e segurança. Inicialmente, foi criada a classe abstrata Heroi, que define a estrutura comum a todos os personagens do jogo, incluindo atributos encapsulados, como nome e pontos de vida (HP), além do método abstrato receber_dano(). Essa abordagem garante que todas as subclasses implementem seu próprio comportamento de dano, respeitando um contrato comum.
# Além disso, foi definida a interface Curavel, por meio de uma classe abstrata com o método receber_cura(), assegurando que todas as classes que implementam esse contrato possuam comportamento de cura. As classes Guerreiro e Mago foram implementadas como especializações de Heroi, utilizando herança para reaproveitar estrutura e polimorfismo para modificar comportamentos específicos. O Guerreiro reduz o dano recebido com base em sua armadura, enquanto o Mago utiliza sua mana para absorver o dano antes que ele afete sua vida.
# O polimorfismo foi aplicado na classe Batalha, onde um conjunto genérico de objetos do tipo Heroi é manipulado de forma uniforme. Durante a execução do ataque em área (bola de fogo), cada herói reage de maneira distinta ao mesmo estímulo, demonstrando a flexibilidade do sistema. Esse comportamento também é observado no método de cura em grupo, onde cada classe implementa sua própria lógica de recuperação.
# Por fim, o Princípio da Substituição de Liskov foi respeitado, uma vez que objetos das subclasses Guerreiro e Mago podem ser utilizados no lugar da classe base Heroi sem comprometer o funcionamento do sistema. Isso é evidenciado pela função de teste que recebe qualquer objeto do tipo Heroi e executa operações de dano de forma consistente, mantendo as regras de negócio, como a impossibilidade de valores negativos de HP. Dessa forma, o sistema permanece robusto, extensível e alinhado às boas práticas da engenharia de software.
