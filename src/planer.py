from typing import Dict
import datetime

class Kwadrans:
    StudentID: int
    Id: int
    przydzielony: bool
    dataPrzydzialu: datetime.date


def upchnij_godziny(kwadranse:dict[int: Kwadrans], plan):
    for key, val in kwadranse.items():
        if val.przydzielony is True:
            continue
