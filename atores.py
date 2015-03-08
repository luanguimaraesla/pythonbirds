# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import math

DESTRUIDO = 'Destruido'
ATIVO = 'Ativo'
GRAVIDADE = 10  # m/s^2


class Ator():
    """
    Classe que representa um ator. Ele representa um ponto cartesiano na tela.
    """
    _caracter_ativo = 'A'
    _caracter_destruido = ' '

    def __init__(self, x=0, y=0):
        """
        Método de inicialização da classe. Deve inicializar os parâmetros x, y, caracter e status

        :param x: Posição horizontal inicial do ator
        :param y: Posição vertical inicial do ator
        """
        self.y = y
        self.x = x
        self.status = ATIVO

    def caracter(self):
        return self._caracter_ativo if self.status == ATIVO else self._caracter_destruido

    def calcular_posicao(self, tempo):
        """
        Método que calcula a posição do ator em determinado tempo.
        Deve-se imaginar que o tempo começa em 0 e avança de 0,01 segundos

        :param tempo: o tempo do jogo
        :return: posição x, y do ator
        """
        #Lógica não compreendida, há a necessidade de mais informações além do tempo para se verificar a posição em 4 dimensões
        return self.x, self.y

    def colidir(self, outro_ator, intervalo=1):
        """
        Método que executa lógica de colisão entre dois atores.
        Só deve haver colisão se os dois atores tiverem seus status ativos.
        Para colisão, é considerado um quadrado, com lado igual ao parâmetro intervalo, em volta do ponto onde se
        encontra o ator. Se os atores estiverem dentro desse mesmo quadrado, seus status devem ser alterados para
        destruido, seus caracteres para destruido também.

        :param outro_ator: Ator a ser considerado na colisão
        :param intervalo: Intervalo a ser considerado
        :return:
        """
        if abs(self.x - outro_ator.x)<= intervalo and abs(self.y - outro_ator.y) <= intervalo and\
                self.caracter() != self._caracter_destruido and\
                outro_ator.caracter() != outro_ator._caracter_destruido:
            self.status = DESTRUIDO
            outro_ator.status = DESTRUIDO



class Obstaculo(Ator):
    #correção de caracter
    _caracter_ativo = 'O'


class Porco(Ator):
    _caracter_ativo = '@'
    _caracter_destruido = '+'


class Passaro(Ator):
    velocidade_escalar = 10.0

    def __init__(self, x=0, y=0):
        """
        Método de inicialização de pássaro.

        Deve chamar a inicialização de ator. Além disso, deve armazenar a posição inicial e incializar o tempo de
        lançamento e angulo de lançamento

        :param x:
        :param y:
        """
        super().__init__(x, y)
        self._x_inicial = x
        self._y_inicial = y
        self._tempo_de_lancamento = None
        self._angulo_de_lancamento = None  # radianos

    def foi_lancado(self):
        """
        Método que retorna verdaeira se o pássaro já foi lançado e falso caso contrário

        :return: booleano
        """
        if self._tempo_de_lancamento == None:
            return False
        else:
            return True

    def colidir_com_chao(self):
        """
        Método que executa lógica de colisão com o chão. Toda vez que y for menor ou igual a 0,
        o status dos Passaro deve ser alterado para destruido, bem como o seu caracter

        """
        if self.y <= 0:
            self.status = DESTRUIDO

    def calcular_posicao(self, tempo):
        """
        Método que cálcula a posição do passaro de acordo com o tempo.

        Antes do lançamento o pássaro deve retornar o valor de sua posição inicial

        Depois do lançamento o pássaro deve calcular de acordo com sua posição inicial, velocidade escalar,
        ângulo de lancamento, gravidade (constante GRAVIDADE) e o tempo do jogo.

        Após a colisão, ou seja, ter seus status destruido, o pássaro deve apenas retornar a última posição calculada.

        :param tempo: tempo de jogo a ser calculada a posição
        :return: posição x, y
        """
        if not self.foi_lancado():
            return self._x_inicial, self._y_inicial
        elif self.status == DESTRUIDO:
            pass
        else:
            tempo = tempo - self._tempo_de_lancamento
            vel_x = self.velocidade_escalar * math.cos(self._angulo_de_lancamento)
            vel_y = self.velocidade_escalar * math.sin(self._angulo_de_lancamento)
            self.x = self._x_inicial + tempo * vel_x
            self.y = self._y_inicial + vel_y * tempo - (GRAVIDADE*(tempo**2)/2)

        return self.x , self.y


    def lancar(self, angulo, tempo_de_lancamento):
        """
        Lógica que lança o pássaro. Deve armazenar o ângulo e o tempo de lançamento para posteriores cálculo.
        O ângulo é passado em graus e deve ser transformado em radianos

        :param angulo:
        :param tempo_de_lancamento:
        :return:
        """
        self._tempo_de_lancamento = tempo_de_lancamento
        self._angulo_de_lancamento = math.radians(angulo)


class PassaroAmarelo(Passaro):
    velocidade_escalar = 30.0
    _caracter_ativo = 'A'
    _caracter_destruido = 'a'

    def __init__(self, x=0, y=0):
        Passaro.__init__(self,x,y)


class PassaroVermelho(Passaro):
    _caracter_ativo = 'V'
    _caracter_destruido = 'v'
    velocidade_escalar = 20.0

    def __init__(self, x=0, y=0):
        super().__init__(x,y)