from datetime import date
from dateutil import relativedelta

import pandas as pd
import numpy as np

from indices_economicos.indices.indice import GetIGPM, GetIPCA


pd.set_option("display.precision", 15)


class IndiceSimulado:
    
    def __init__(self, indice: str, data: date) -> None:
        self.indice = indice
        self.data = data
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
        indice =  GetIGPM() if self.indice == "IGP-M" else Ipca
        self.df = pd.DataFrame.from_records(
            list(indice.objects.all().values(
                'data', 'variacao', 'acumulado'
                )
            )
        )
        competencia = Focus.objects.filter(
            competencia__lte=self.data
            ).aggregate(maximo=Max('competencia'))['maximo']

        self.focus = create_dict_values(list(
                Focus.objects.filter(
                    competencia=competencia,
                    focus = self.indice
                    ).values_list('ano', 'valor')
                )
            )
        
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
    
    def simulacao(self, mes:int) -> None:
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
        self.df = self.df[
                pd.to_datetime(self.df["data"]).dt.month == mes
            ]
