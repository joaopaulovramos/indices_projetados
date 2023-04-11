from datetime import date

import pytest
from pytest_mock import mocker

from simulador_indices.simulacao_juros import IndiceSimulado
from simulador_indices.indice import IPEAData


RESULTADO = {
  "@odata.context":"http://ipeadata.gov.br/api/odata4/$metadata#Valores","value":[
      {
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-01-01T00:00:00-02:00","VALVALOR":707.488,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-02-01T00:00:00-02:00","VALVALOR":713.747,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-03-01T00:00:00-03:00","VALVALOR":722.707,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-04-01T00:00:00-03:00","VALVALOR":729.346,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-05-01T00:00:00-03:00","VALVALOR":732.595,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-06-01T00:00:00-03:00","VALVALOR":738.421,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-07-01T00:00:00-03:00","VALVALOR":741.346,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-08-01T00:00:00-03:00","VALVALOR":736.402,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-09-01T00:00:00-03:00","VALVALOR":736.362,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-10-01T00:00:00-03:00","VALVALOR":741.333,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-11-01T00:00:00-03:00","VALVALOR":743.558,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2019-12-01T00:00:00-03:00","VALVALOR":759.112,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-01-01T00:00:00-03:00","VALVALOR":762.733,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-02-01T00:00:00-03:00","VALVALOR":762.423,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-03-01T00:00:00-03:00","VALVALOR":771.908,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-04-01T00:00:00-03:00","VALVALOR":778.101,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-05-01T00:00:00-03:00","VALVALOR":780.28,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-06-01T00:00:00-03:00","VALVALOR":792.429,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-07-01T00:00:00-03:00","VALVALOR":810.083,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-08-01T00:00:00-03:00","VALVALOR":832.313,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-09-01T00:00:00-03:00","VALVALOR":868.442,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-10-01T00:00:00-03:00","VALVALOR":896.505,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-11-01T00:00:00-03:00","VALVALOR":925.887,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2020-12-01T00:00:00-03:00","VALVALOR":934.758,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-01-01T00:00:00-03:00","VALVALOR":958.844,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-02-01T00:00:00-03:00","VALVALOR":983.063,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-03-01T00:00:00-03:00","VALVALOR":1011.948,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-04-01T00:00:00-03:00","VALVALOR":1027.211,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-05-01T00:00:00-03:00","VALVALOR":1069.289,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-06-01T00:00:00-03:00","VALVALOR":1075.733,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-07-01T00:00:00-03:00","VALVALOR":1084.095,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-08-01T00:00:00-03:00","VALVALOR":1091.29,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-09-01T00:00:00-03:00","VALVALOR":1084.312,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-10-01T00:00:00-03:00","VALVALOR":1091.283,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-11-01T00:00:00-03:00","VALVALOR":1091.483,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2021-12-01T00:00:00-03:00","VALVALOR":1100.988,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-01-01T00:00:00-03:00","VALVALOR":1120.999,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-02-01T00:00:00-03:00","VALVALOR":1141.546,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-03-01T00:00:00-03:00","VALVALOR":1161.418,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-04-01T00:00:00-03:00","VALVALOR":1177.809,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-05-01T00:00:00-03:00","VALVALOR":1183.953,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-06-01T00:00:00-03:00","VALVALOR":1190.882,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-07-01T00:00:00-03:00","VALVALOR":1193.337,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-08-01T00:00:00-03:00","VALVALOR":1185.004,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-09-01T00:00:00-03:00","VALVALOR":1173.793,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-10-01T00:00:00-03:00","VALVALOR":1162.391,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-11-01T00:00:00-03:00","VALVALOR":1155.829,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2022-12-01T00:00:00-03:00","VALVALOR":1161.006,"NIVNOME":"","TERCODIGO":""
    },{
      "SERCODIGO":"IGP12_IGPM12","VALDATA":"2023-01-01T00:00:00-03:00","VALVALOR":1163.465,"NIVNOME":"","TERCODIGO":""
    }
  ]
}


IGPM = 'IGP12_IGPM12'
IPCA = 'PRECOS12_IPCA12'


@pytest.fixture()
def ipea_data(mocker):
    ipea = IPEAData(IGPM)
    mocker.patch.object(ipea, '_get_json', return_value=RESULTADO)
    return ipea

@pytest.fixture(scope="session")
def indice():
    return IndiceSimulado('IGP-M', date(2022,3,31), IGPM)
