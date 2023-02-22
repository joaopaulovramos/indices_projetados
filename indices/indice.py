import re
from datetime import datetime, date
import calendar

import pandas as pd
import requests


pd.set_option("display.precision", 15)

class IPEAData:
    def __init__(self, pos_fix) -> None:
        self.pos_fix = pos_fix
        self.api = "http://www.ipeadata.gov.br/api/odata4/Metadados('%s')/Valores"
        self.df_series=  None
        self._get_name()
        #self._time_series()

    def _get_name(self):
        final = self.pos_fix.split('_')[-1]
        self.nome =  re.sub(r'\d+', '', final)

    def _get_json(self):
        api = self.api % (self.pos_fix)
        try:
            self.req = requests.get(api)
        except Exception as e:
            print(e)

        if self.req.status_code == requests.codes.OK:
            json_response = self.req.json()
            return json_response
        return None
    
    def time_series(self):
        json_response = self._get_json()
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
