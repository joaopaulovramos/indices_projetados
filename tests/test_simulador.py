from datetime import date

from indices.simulacao_juros import IndiceSimulado


def test_simulador_is_not_none(indice):
    assert  indice is not None

def test_simulador_focus(indice):
    indice.simulacao(5)
    assert indice.focus[2022] == 0.133953
    assert indice.focus[2027] == 0.04

def test_simulador_df(indice):
    indice.simulacao(5)
    assert indice.df.iloc[2]['acumulado'] == 1.0886981403681075
