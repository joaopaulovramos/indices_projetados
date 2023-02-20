from datetime import date

import pandas as pd
from bcb import Expectativas
from bizdays import Calendar


class Focus:
    def __init__(self, indice: str, data: date) -> None:
        self.indice = indice
        self.data = date
        self._get_values()

    def _last_bizday(self):
        cal = Calendar.load(filename='ANBIMA.cal')
        if self.data < date(self.data.year, 3,31):
            return cal.getbizdays(self.data.year-1, 12)[-1]

        elif self.data < date(self.data.year, 6,30):
            return cal.getbizdays(self.data.year, 3)[-1]

        elif self.data < date(self.data.year, 9,30):
            return cal.getbizdays(self.data.year, 6)[-1]
        return cal.getbizdays(self.data.year, 9)[-1]
    
    def _get_values(self):
        em = Expectativas()
        ep = em.get_endpoint('ExpectativasMercadoTop5Anuais')
        last_bizday = self._last_bizday()
        return (ep.query()
            .filter(ep.Indicador == self.indice)
            .filter(ep.Data >= last_bizday, ep.Data <= last_bizday)
            .orderby(ep.Data.asc())
            .select(ep.Data, ep.DataReferencia, ep.Mediana)
            .collect())
