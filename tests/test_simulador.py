from datetime import date

from  simulador_indices.simulacao_juros import IndiceSimulado


def test_simulador_is_not_none(indice):
    assert  indice is not None

def test_simulador_focus(indice):
    indice.simulacao_mes(5)
    assert indice.focus[2022] == 0.133953
    assert indice.focus[2027] == 0.04
    assert indice.df.iloc[2]['acumulado'] == 1.0886981403681075
