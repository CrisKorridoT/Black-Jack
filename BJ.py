import random

class Carta:
    def __init__(self, palo, rango):
        self.palo = palo
        self.rango = rango

    def __str__(self):
        return f"{self.rango} de {self.palo}"


class Baraja:
    def __init__(self):
        palos = ["Corazones", "Diamantes", "Tréboles", "Picas"]
        rangos = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jota", "Reina", "Rey"]
        self.cartas = [Carta(palo, rango) for palo in palos for rango in rangos]
        random.shuffle(self.cartas)

    def repartir_carta(self):
        return self.cartas.pop()

    def __str__(self):
        return f"Baraja con {len(self.cartas)} cartas"


class Jugador:
    def __init__(self, nombre, dinero):
        self.nombre = nombre
        self.dinero = dinero
        self.mano = []

    def recibir_carta(self, carta):
        self.mano.append(carta)

    def obtener_valor_mano(self):
        valor = 0
        aces = 0
        for carta in self.mano:
            if carta.rango == "As":
                valor += 11
                aces += 1
            elif carta.rango in ["Jota", "Reina", "Rey"]:
                valor += 10
            else:
                valor += int(carta.rango)

        while valor > 21 and aces > 0:
            valor -= 10
            aces -= 1

        return valor

    def mostrar_mano(self):
        print(f"Mano de {self.nombre}:")
        for carta in self.mano:
            print(carta)

    def __str__(self):
        return f"{self.nombre} tiene {len(self.mano)} cartas con un valor total de {self.obtener_valor_mano()}"


class JuegoBlackjack:
    def __init__(self, nombre_jugador, dinero_inicial):
        self.baraja = Baraja()
        self.jugador = Jugador(nombre_jugador, dinero_inicial)
        self.dealer = Jugador("Dealer", 0)

    def obtener_apuesta(self):
        while True:
            apuesta = int(input("Ingrese la cantidad a apostar (mínimo 5000, máximo disponible): "))
            if apuesta < 5000:
                print("La apuesta mínima es de 5000.")
            elif apuesta > self.jugador.dinero:
                print("No tienes suficiente dinero.")
            else:
                return apuesta

    def iniciar_juego(self):
        print("¡Bienvenido a Blackjack!")
        apuesta = self.obtener_apuesta()

        self.jugador.dinero -= apuesta

        self.jugador.mano = []
        self.dealer.mano = []

        self.jugador.recibir_carta(self.baraja.repartir_carta())
        self.dealer.recibir_carta(self.baraja.repartir_carta())
        self.jugador.recibir_carta(self.baraja.repartir_carta())
        self.dealer.recibir_carta(self.baraja.repartir_carta())

        while True:
            print("\n" + "=" * 20)
            self.jugador.mostrar_mano()
            print("")

            print("Mano del dealer:")
            print(self.dealer.mano[0])
            print("Carta oculta")

            opcion = input("¿Qué deseas hacer? (1) Pedir carta o (2) Plantarse? ")
            if opcion == "1":
                self.jugador.recibir_carta(self.baraja.repartir_carta())
                if self.jugador.obtener_valor_mano() > 21:
                    print("\n" + "=" * 20)
                    self.jugador.mostrar_mano()
                    print("")
                    print("Mano del dealer:")
                    for carta in self.dealer.mano:
                        print(carta)
                    print("")
                    print("¡Te has pasado de 21! Has perdido.")
                    break
            elif opcion == "2":
                while self.dealer.obtener_valor_mano() < 17:
                    self.dealer.recibir_carta(self.baraja.repartir_carta())
                print("\n" + "=" * 20)
                self.jugador.mostrar_mano()
                print("")
                print("Mano del dealer:")
                for carta in self.dealer.mano:
                    print(carta)
                print("")
                if self.dealer.obtener_valor_mano() > 21:
                    print("¡El dealer se ha pasado de 21! Has ganado.")
                    self.jugador.dinero += apuesta * 2
                elif self.jugador.obtener_valor_mano() > self.dealer.obtener_valor_mano():
                    print("¡Has ganado!")
                    self.jugador.dinero += apuesta * 2
                elif self.jugador.obtener_valor_mano() < self.dealer.obtener_valor_mano():
                    print("Has perdido.")
                else:
                    print("¡Es un empate!")
                    self.jugador.dinero += apuesta
                break
            else:
                print("Opción inválida. Por favor, elige de nuevo.")

        print(f"\nTu saldo actual: {self.jugador.dinero}")


# Ejemplo de uso
nombre_jugador = input("Ingresa tu nombre: ")
dinero_inicial = int(input("Ingresa la cantidad de dinero inicial: "))
juego = JuegoBlackjack(nombre_jugador, dinero_inicial)
juego.iniciar_juego()