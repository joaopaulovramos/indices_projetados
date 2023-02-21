from datetime import date

import pandas as pd
import pytest

from indices_economico.bcb_.focus import Focus


@pytest.fixture
def focus():
    data =  date(2023,2,21)
    return Focus('IPCA', data)
    

def test_focus(focus):
    assert focus is not None
    assert focus.data == date(2023,2,21)
    assert focus.indice == 'IPCA'
    assert focus.df_focus is not None
    assert focus.dict_focus[2023] == 5.4384
