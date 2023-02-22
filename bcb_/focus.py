from datetime import date

from dateutil.relativedelta import relativedelta
import pandas as pd
from bcb import Expectativas
from bizdays import Calendar
from indices_economico.bcb_.metas import METAS


def get_date(data):
    cal = Calendar.load(filename='ANBIMA.cal')   
    return data if cal.isbizday(data) else cal.preceding(data)

class Focus:
    def __init__(self, indice, data) -> None:
        self.indice = indice
        self.data = data
        self._get_values()

    def _last_bizday(self):
        
        if self.data < date(self.data.year, 3,31):
            return get_date(date(self.data.year-1, 12,31))        

        elif self.data < date(self.data.year, 6,30):
            return get_date(self.data.year, 3, 31)
        
        elif self.data < date(self.data.year, 9,30):
            return get_date(self.data.year, 6, 30)
        return get_date(self.data.year, 9,30)
    
    def __conection_bcb(self):
        endpoint = ('ExpectativasMercadoTop5Selic' 
                    if self.indice == 'SELIC' 
                    else 'ExpectativasMercadoTop5Anuais'
        )
        em = Expectativas()
        ep = em.get_endpoint(endpoint)
        self.last_bizday = self._last_bizday()
        df_focus =(ep.query()
            .filter(ep.Indicador == self.indice)
            .filter(ep.Data >= self.last_bizday+relativedelta(days=-3), ep.Data <= self.last_bizday)
            .filter(ep.tipoCalculo=='L')
            .orderby(ep.Data.asc())
            .select(ep.Data, ep.DataReferencia, ep.Mediana)
            .collect())
        df_focus = df_focus.loc[df_focus['Data'] == self.last_bizday.isoformat()]
        df_focus.columns = ['data', 'ano', 'valor']
        df_focus['ano'] = df_focus['ano'].astype(int)
        return df_focus
    
    def _get_values(self):
        self.df_focus = self.__conection_bcb()
        max_ano = self.df_focus['ano'].max()
        competencia = self.last_bizday.year
        self._dict_values(max_ano, competencia)

    def _dict_values(self, max_ano, competencia):

        dict_focus = self.df_focus.to_dict('records')
        self.dict_focus = {
            x['ano']:x['valor'] for x in dict_focus
        }
        meta = METAS[competencia][self.indice]
        for ano in range(max_ano+1, 2051):
            self.dict_focus[ano] = meta
