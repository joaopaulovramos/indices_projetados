from datetime import date
from dateutil import relativedelta

import pandas as pd
import numpy as np
from bcb_.focus import Focus

from indices.indice import IPEAData


pd.set_option("display.precision", 15)


class IndiceSimulado:
    
    def __init__(self, indice: str, data: date, pos_fix) -> None:
        self.indice = indice
        self.data = data
        self.pos_fix = pos_fix
        self.data_final = date(2050,12,31)       
        
    def future_frame(self):
        meses = relativedelta.relativedelta(self.data_final, self.data)
        meses = meses.years * 12 + meses.months + 1
        self.df_calculo = pd.DataFrame(
            {"data":pd.date_range(
                self.data, 
                periods=meses, 
                freq="M"
                )
            }
        )
        self.df_calculo["data"] = self.df_calculo['data'].dt.date
        
        self.df_calculo["acumulado"] = None
        self.df_calculo["variacao"] = None
    
    def simulacao_juros(self):
        indice = IPEAData(self.pos_fix)
        indice.time_series()
        focus = Focus(self.indice, self.data)
        self.focus = focus.dict_focus
        self.df = indice.df_series
        self.df["data"] = pd.to_datetime(self.df["data"])
        self.df["data"] = self.df["data"].dt.date
        self.df = self.df[
            (self.df["data"] < self.data) & 
            (pd.to_datetime(self.df["data"]).dt.year >= self.data.year - 1)
            ]
        self.future_frame()
        self.df = pd.concat([self.df, self.df_calculo], ignore_index=True)

    def valor_indice_ano(self):
        acumulado = np.prod(
            self.df[
                (self.df["data"] < self.data) & 
                (pd.to_datetime(self.df["data"]).dt.year >= self.data.year)
            ]["variacao"]
        )
        meses_restantes = 13 - self.data.month
        self.valor_indice = np.power(
            (self.focus[self.data.year] +1)/acumulado,1/meses_restantes)
    
    def simulacao(self) -> None:
        self.simulacao_juros()
        self.valor_indice_ano()
        
        def variacao_simulado(row):
            d = row["data"]
            if d.year > self.data.year:
                return np.power(self.focus[d.year] + 1, 1/12) 
            if d >= self.data and d.year == self.data.year:
                return self.valor_indice
            return row["variacao"]
        
        self.df["variacao"] = self.df.apply(variacao_simulado, axis=1)

        def acumulado_simulacao(row):
        
            if np.isnan(row["acumulado"]):
                return np.prod(
                    self.df[
                        (self.df["data"] <= row["data"]) & 
                        (self.df["data"] > 
                            (row["data"] - relativedelta.relativedelta(years=1)))
                        ]["variacao"].iloc[-12:]
                )
            return row["acumulado"]

        self.df["acumulado"] = self.df.apply(
            acumulado_simulacao, 
            axis=1
        )
    
    def simulacao_mes(self, mes):
        self.simulacao()
        self.df = self.df[
                pd.to_datetime(self.df["data"]).dt.month == mes
            ]
