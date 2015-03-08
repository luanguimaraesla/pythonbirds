# -*- coding: utf-8 -*-
from itertools import chain
from atores import ATIVO


VITORIA = 'VITORIA'
DERROTA = 'DERROTA'
EM_ANDAMENTO = 'EM_ANDAMENTO'


class Ponto():
    def __init__(self, x, y, caracter):
        self.caracter = caracter
        self.x = round(x)
        self.y = round(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.caracter == other.caracter

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self, *args, **kwargs):
        return "Ponto(%s,%s,'%s')" % (self.x, self.y, self.caracter)

class Fase():
    def __init__(self, intervalo_de_colisao=1):
        """
        Método que inicializa uma fase.

        :param intervalo_de_colisao:
        """
        self.intervalo_de_colisao = intervalo_de_colisao
        self._passaros = []
        self._porcos = []
        self._obstaculos = []


    def adicionar_obstaculo(self, *obstaculos):
        """
        Adiciona obstáculos em uma fase

        :param obstaculos:
        """

        for cada_obstaculo in obstaculos:
            self._obstaculos.append(cada_obstaculo)

    def adicionar_porco(self, *porcos):
        """
        Adiciona porcos em uma fase

        :param porcos:
        """
        for cada_porco in porcos:
            self._porcos.append(cada_porco)

    def adicionar_passaro(self, *passaros):
        """
        Adiciona pássaros em uma fase

        :param passaros:
        """
        for cada_passaro in passaros:
            self._passaros.append(cada_passaro)

    def status(self):
        """
        Método que indica com mensagem o status do jogo

        Se o jogo está em andamento (ainda tem porco ativo e pássaro ativo), retorna essa mensagem.

        Se o jogo acabou com derrota (ainda existe porco ativo), retorna essa mensagem

        Se o jogo acabou com vitória (não existe porco ativo), retorna essa mensagem

        :return:
        """
        tem_porco = ATIVO in [cada_porco.status for cada_porco in self._porcos]
        tem_passaro = ATIVO in [cada_passaro.status for cada_passaro in self._passaros]

        if tem_porco and tem_passaro:
            return EM_ANDAMENTO
        elif tem_porco and not tem_passaro:
            return DERROTA
        else:
            return VITORIA

    def lancar(self, angulo, tempo):
        """
        Método que executa lógica de lançamento.

        Deve escolher o primeiro pássaro não lançado da lista e chamar seu método lançar

        Se não houver esse tipo de pássaro, não deve fazer nada

        :param angulo: ângulo de lançamento
        :param tempo: Tempo de lançamento
        """
        for cada_passaro in self._passaros:
            if not cada_passaro.foi_lancado():
                cada_passaro.lancar(angulo, tempo)
                break

    def calcular_pontos(self, tempo):
        """
        Lógica que retorna os pontos a serem exibidos na tela.

        Cada ator deve ser transformado em um Ponto.

        :param tempo: tempo para o qual devem ser calculados os pontos
        :return: objeto do tipo Ponto
        """

        pontos = []

        for cada_passaro in self._passaros:
                cada_passaro.calcular_posicao(tempo)
                for cada_possivel_alvo in self._porcos + self._obstaculos:
                    cada_passaro.colidir(cada_possivel_alvo, self.intervalo_de_colisao)

        pontos.extend([self._transformar_em_ponto(cada_ator) for cada_ator in self._passaros])
        pontos.extend([self._transformar_em_ponto(cada_ator) for cada_ator in self._porcos])
        pontos.extend([self._transformar_em_ponto(cada_ator) for cada_ator in self._obstaculos])

        return pontos

    def _transformar_em_ponto(self, ator):
        return Ponto(ator.x, ator.y, ator.caracter())

