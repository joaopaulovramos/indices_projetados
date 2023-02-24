from pytest_mock import mocker

from indices_economico.indices.indice import IPEAData


IGPM = 'IGP12_IGPM12'
IPCA = 'PRECOS12_IPCA12'

def test_ipea_data():
    assert IPEAData(IGPM) is not None

def test_ipead_data():
    ipea_data = IPEAData(IGPM)
    assert ipea_data.nome == "IGPM"


def test_time_series(mocker, resultado):
    ipea_data = IPEAData(IGPM)
    mocker.patch.object(ipea_data, '_get_json', return_value=resultado)
    ipea_data.time_series()
    assert ipea_data.df_series is not None
    assert ipea_data.df_series['valor'].min() == 707.488
    assert ipea_data.df_series.iloc[0]['nome'] == 'IGPM'
    assert ipea_data.df_series['acumulado'].min() == 1.0378822817861568
    assert ipea_data.df_series['variacao'].min() == 0.9902861918583602
