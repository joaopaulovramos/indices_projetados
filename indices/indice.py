from datetime import datetime, date
import calendar

import pandas as pd
import requests

from ifric.receita.models import Igpm, Ipca


pd.set_option("display.precision", 15)

class IPEAData:
    pox_fix = None
    nome = None
    def __init__(self) -> None:
        self.api = "http://www.ipeadata.gov.br/api/odata4/Metadados%s"
        self.df_series=  None
        self._time_series()

    def _time_series(self):
        api = self.api % (self.pos_fix)
        try:
            self.req = requests.get(api)
        except Exception as e:
            print(e)

        if self.req.status_code == requests.codes.OK:
            json_response = self.req.json()
            if 'value' in json_response:
                try:
                    self.df_series = pd.DataFrame(json_response['value'])
                    self.df_series["VALDATA"] = self.df_series["VALDATA"].apply(lambda x : datetime.fromisoformat(x).date())
                    self.df_series["VALDATA"] = pd.to_datetime(self.df_series["VALDATA"])
                    self.df_series = self.df_series[self.df_series["VALDATA"] >= datetime(2018, 1,1)]
                    self.df_series.columns = ["codigo", "data", "valor", "nome", "tercodigo"]
                    self.df_series = self.df_series.drop(["nome", "tercodigo", "codigo"], axis=1)
                    self.df_series["data"] = self.df_series["data"].apply(lambda x: x.replace(day=calendar.monthrange(x.year, x.month)[1]))
                    self.df_series["nome"] = self.nome
                except Exception as e:
                    print(e)


class GetIGPM(IPEAData):
    pos_fix = "('IGP12_IGPM12')/Valores"
    nome = "IGPM"
    
    def register(self):
        self.time_series()


class GetIPCA(IPEAData):
    pos_fix = "('PRECOS12_IPCA12')/Valores"
    nome = "IPCA"

    def register(self):
        self.time_series()
        