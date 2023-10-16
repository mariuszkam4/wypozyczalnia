import pytest
import pandas as pd
import json
import tempfile
import os

from wypozyczalnia import Samochod, Wypozyczalnia 

def test_samochod_pelne_dane():
    samochod = Samochod ('XYZ 123', 'Toyota', "Yaris", 2020, 'benzyna')
    assert str(samochod) == "XYZ 123 Toyota Yaris 2020 benzyna"

def test_samochod_wypozycz():
    samochod = Samochod ("XYZ 123", "Toyota", "Yaris", 2020, "benzyna")
    assert samochod.wypozycz() == True
    assert samochod.wypozycz() == False
    assert samochod.wypozyczony == True

def test_zwroc_samochod():
    samochod = Samochod ("XYZ 123", "Toyota", "Yaris", 2020, "benzyna")
    samochod.wypozycz()
    assert samochod.zwroc() == True
    assert samochod.wypozyczony == False

def test_info_samochod():
    samochod = Samochod ("XYZ 123", "Toyota", "Yaris", 2020, "benzyna")
    assert samochod.info().startswith ("Samochód o numerze rejestracyjnym XYZ 123, marki Toyota, z roku 2020 jest")

def test_wypozyczalnia_dodaj_samochod():
    wypozyczalnia = Wypozyczalnia()
    samochod = Samochod ("XYZ 123", "Toyota", "Yaris", 2020, "benzyna")
    wypozyczalnia.dodaj_samochod(samochod)
    assert len(wypozyczalnia.df) == 1
    assert wypozyczalnia.df['marka'].iloc[0] == 'Toyota'

def test_wypozyczalnia_usun_samochod():
    wypozyczalnia = Wypozyczalnia()
    samochod = Samochod ("XYZ 123", "Toyota", "Yaris", 2020, "benzyna")
    wypozyczalnia.dodaj_samochod(samochod)
    wypozyczalnia.usun_samochod('XYZ 123')
    assert len(wypozyczalnia.df) == 0

def test_wypozyczalnia_wczytaj_baze():
    wypozyczalnia = Wypozyczalnia()
    wypozyczalnia.wczytaj_baze('baza_pojazdow.json')

    with open('baza_pojazdow.json', 'r') as f:
        dane = json.load(f)
    oczekiwana_df = pd.DataFrame(dane)

    assert wypozyczalnia.df.equals(oczekiwana_df)

def test_wypozyczalnia_zapisz_baze():
    wypozyczalnia = Wypozyczalnia()
    dane = [
        {"nr_rej": "XYZ 123", "marka": "Toyota", "model": "Yaris", "rok": 2020, "paliwo": "benzyna", "wypozyczony": False},
        {"nr_rej": "ABC 456", "marka": "Ford", "model": "Focus", "rok": 2019, "paliwo": "diesel", "wypozyczony": True}
    ]
    wypozyczalnia.df = pd.DataFrame(dane)

    with tempfile.NamedTemporaryFile(suffix='.json', delete=True) as temp_file:
        testowy_plik = temp_file.name
    wypozyczalnia.zapisz_baze(testowy_plik)

    with open(testowy_plik, 'r') as f:
        zapisane_dane = json.load(f)
    
    oczekiwane_dane = wypozyczalnia.df.to_dict(orient='records')
    assert zapisane_dane == oczekiwane_dane
    
    os.remove(testowy_plik)

# def test_wypozyczalnia_dodaj_samochod():
#     wypozyczalnia = Wypozyczalnia()
#     samochod = {"nr_rej": "XYZ 123", "marka": "Toyota", "model": "Yaris", "rok": 2020, "paliwo": "benzyna", "wypozyczony": False}
#     wypozyczalnia.df = pd.DataFrame(samochod)

#     testowy_plik = 'test_baza_pojazdow.json'
#     wypozyczalnia.dodaj_samochod(testowy_plik)
#     oczekiwane_dane = wypozyczalnia.df.to_json()

#     assert oczekiwane_dane == wypozyczalnia.df


