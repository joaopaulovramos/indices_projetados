from pytest_mock import mocker

from simulador_indices.indice import IPEAData




def test_ipea_data(ipea_data):
    assert ipea_data is not None

def test_ipead_data(ipea_data):
    assert ipea_data.nome == "IGPM"


def test_time_series(ipea_data):
    ipea_data.time_series()
    assert ipea_data.df_series is not None
    assert ipea_data.df_series['valor'].min() == 707.488
    assert ipea_data.df_series.iloc[0]['nome'] == 'IGPM'
    assert ipea_data.df_series['acumulado'].min() == 1.0378822817861568
    assert ipea_data.df_series['variacao'].min() == 0.9902861918583602
