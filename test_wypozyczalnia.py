import pytest
import pandas as pd
import json
import tempfile
import os

from wypozyczalnia import Samochod, Wypozyczalnia 

@pytest.fixture
def wypozyczalnia():
    return Wypozyczalnia()

@pytest.fixture
def samochod():
    return Samochod ("XYZ 0013", "Toyota", "Yaris", 2020, "benzyna")

@pytest.fixture
def testowy_plik(wypozyczalnia):
    dane = [
        {"nr_rej": "XYZ 0013", "marka": "Toyota", "model": "Yaris", "rok": 2020, "paliwo": "benzyna", "wypozyczony": False},
        {"nr_rej": "ABC 456", "marka": "Ford", "model": "Focus", "rok": 2019, "paliwo": "diesel", "wypozyczony": True}
    ]
    wypozyczalnia.df = pd.DataFrame(dane)

    temp_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
    testowy_plik = temp_file.name
    temp_file.close()
    return testowy_plik

def test_samochod_pelne_dane(samochod):
    assert str(samochod) == "XYZ 0013 Toyota Yaris 2020 benzyna"

def test_samochod_wypozycz(samochod):
    assert samochod.wypozycz() == True
    assert samochod.wypozycz() == False
    assert samochod.wypozyczony == True

def test_zwroc_samochod(samochod):
    samochod.wypozycz()
    assert samochod.zwroc() == True
    assert samochod.wypozyczony == False

def test_info_samochod(samochod):
    assert samochod.info().startswith ("Samochód o numerze rejestracyjnym XYZ 0013, marki Toyota, z roku 2020 jest")

def test_wypozyczalnia_wczytaj_baze(wypozyczalnia, testowy_plik):
    wypozyczalnia.zapisz_baze(testowy_plik)
    
    wypozyczalnia.wczytaj_baze(testowy_plik)

    with open(testowy_plik, 'r') as f:
        dane = json.load(f)
    oczekiwana_df = pd.DataFrame(dane)

    assert wypozyczalnia.df.equals(oczekiwana_df)

    os.remove(testowy_plik)

def test_wypozyczalnia_zapisz_baze(wypozyczalnia, testowy_plik):
    wypozyczalnia.zapisz_baze(testowy_plik)
    with open(testowy_plik, 'r') as f:
        zapisane_dane = json.load(f)
    
    oczekiwane_dane = wypozyczalnia.df.to_dict(orient='records')
    assert zapisane_dane == oczekiwane_dane
    
    os.remove(testowy_plik)

def test_wypozyczalnia_dodaj_samochod(monkeypatch,wypozyczalnia, samochod):
    monkeypatch.setattr(wypozyczalnia, 'zapisz_baze', lambda: None)

    wypozyczalnia.dodaj_samochod(samochod)

    assert wypozyczalnia.df.iloc[-1]["nr_rej"] == "XYZ 0013"
    assert wypozyczalnia.df.iloc[-1]["marka"] == "Toyota"
    assert wypozyczalnia.df.iloc[-1]["model"] == "Yaris"
    assert wypozyczalnia.df.iloc[-1]["rok"] == 2020
    assert wypozyczalnia.df.iloc[-1]["paliwo"] == "benzyna"

def test_wypozyczalnia_usun_samochod(monkeypatch, wypozyczalnia, samochod):
    monkeypatch.setattr(wypozyczalnia, 'zapisz_baze', lambda: None)

    wypozyczalnia.dodaj_samochod(samochod)
    wypozyczalnia.usun_samochod('XYZ 0013')
    assert len(wypozyczalnia.df) == 0

def test_wypozyczalnia_wyszukaj_po_parametrach(wypozyczalnia):
    dane_testowe = [
        {"nr_rej": "XYZ 123", "marka": "Toyota", "model": "Yaris", "rok": 2020, "paliwo": "benzyna", "wypozyczony": False},
        {"nr_rej": "ABC 456", "marka": "Ford", "model": "Focus", "rok": 2019, "paliwo": "diesel", "wypozyczony": True},
        {"nr_rej": "GHI 789", "marka": "Toyota", "model": "Corolla", "rok": 2018, "paliwo": "benzyna", "wypozyczony": False}
    ]

    wypozyczalnia.df = pd.DataFrame(dane_testowe)

    wynik = wypozyczalnia.wyszukaj_po_parametrach(marka = "Toyota")
    assert len(wynik) == 2
    assert set(wynik['nr_rej']) == {"XYZ 123", "GHI 789"}

    wynik = wypozyczalnia.wyszukaj_po_parametrach(rok = 2019)
    assert len(wynik) == 1
    assert wynik.iloc[0]['nr_rej'] == "ABC 456"

    wynik = wypozyczalnia.wyszukaj_po_parametrach (marka = "Toyota", paliwo = "diesel")
    assert wynik.empty

    wynik = wypozyczalnia.wyszukaj_po_parametrach(paliwo = "benzyna", wypozyczony = False)
    assert len(wynik) == 2
    assert set(wynik["nr_rej"]) == {"XYZ 123", "GHI 789"}

def test_wypozyczalnia_wypozycz_samochod_logika(monkeypatch, wypozyczalnia):
    monkeypatch.setattr(wypozyczalnia, 'zapisz_baze', lambda:None)
    dane_testowe = [
        {"nr_rej": "XYZ 123", "wypozyczony": False},
        {"nr_rej": "ABC 456", "wypozyczony": True},        
    ]
    wypozyczalnia.df = pd.DataFrame(dane_testowe)

    wynik = wypozyczalnia.wypozycz_samochod(nr_rej = 'XYZ 123')
    assert wynik == True

    wynik = wypozyczalnia.wypozycz_samochod(nr_rej = 'ABC 456')
    assert wynik == False

def test_wypozyczalnia_wypozycz_samochod_komunikaty(monkeypatch, wypozyczalnia, capsys):
    monkeypatch.setattr(wypozyczalnia, 'zapisz_baze', lambda:None)
    dane_testowe = [
        {"nr_rej": "XYZ 123", "wypozyczony": False},
        {"nr_rej": "ABC 456", "wypozyczony": True},        
    ]
    wypozyczalnia.df = pd.DataFrame(dane_testowe)

    wynik = wypozyczalnia.wypozycz_samochod(nr_rej = 'XYZ 123')
    assert wynik == True
    odpowiedz = capsys.readouterr()
    assert "Samochód o nr rejestracyjnym XYZ 123 został wypożyczony." in odpowiedz.out

    wynik = wypozyczalnia.wypozycz_samochod(nr_rej = 'ABC 456')
    assert wynik == False
    odpowiedz = capsys.readouterr()
    assert "Samochód o nr rejestracyjnym ABC 456 jest niedostępny." in odpowiedz.out

def test_wypozyczalnia_wypozycz_samochod_aktualizacja_bazy(monkeypatch, wypozyczalnia):
    monkeypatch.setattr(wypozyczalnia, 'zapisz_baze', lambda:None)
    dane_testowe = [
        {"nr_rej": "XYZ 123", "wypozyczony": False},
        {"nr_rej": "ABC 456", "wypozyczony": True},        
    ]
    wypozyczalnia.df = pd.DataFrame(dane_testowe)

    wynik = wypozyczalnia.wypozycz_samochod(nr_rej = 'XYZ 123')
    assert wynik == True
    assert wypozyczalnia.df.loc[wypozyczalnia.df['nr_rej'] == 'XYZ 123', 'wypozyczony'].all()

    wynik = wypozyczalnia.wypozycz_samochod(nr_rej = 'ABC 456')
    assert wynik == False
    assert wypozyczalnia.df.loc[wypozyczalnia.df['nr_rej'] == 'ABC 456', 'wypozyczony'].all()

def test_wypozyczalnia_zwroc_samochod(monkeypatch, wypozyczalnia, capsys):
    monkeypatch.setattr(wypozyczalnia, 'zapisz_baze', lambda:None)
    dane_testowe = [
        {"nr_rej": "XYZ 123", "wypozyczony": False},
        {"nr_rej": "ABC 456", "wypozyczony": True},        
    ]
    wypozyczalnia.df = pd.DataFrame(dane_testowe)

    wynik = wypozyczalnia.zwroc_samochod(nr_rej = 'XYZ 123')
    assert wynik == False

    wynik = wypozyczalnia.zwroc_samochod(nr_rej = 'ABC 456')
    assert wynik == True
    odpowiedz = capsys.readouterr()
    assert "Samochód o nr rejestracyjnym ABC 456 został zwrócony." in odpowiedz.out
    assert wypozyczalnia.df.loc[wypozyczalnia.df['nr_rej'] == 'ABC 456', 'wypozyczony'].eq(False).all()

