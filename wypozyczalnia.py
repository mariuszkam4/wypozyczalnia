import json
import pandas as pd

class Samochod:
    def __init__(self, nr_rej, marka, model, rok, paliwo):
        self.nr_rej = nr_rej
        self.marka = marka
        self.model = model
        self.rok = rok
        self.paliwo = paliwo
        self.wypozyczony = False

    def pelne_dane(self):
        return f"{self.nr_rej} {self.marka} {self.rok}"
    
    def __str__(self):
        return self.pelne_dane()
    
    def wypozycz(self):
        if not self.wypozyczony:
            self.wypozyczony = True
            return True
        return False
    
    def zwroc(self):
        if self.wypozyczony:
            self.wypozyczony = False
            return True
        return False
    
    def info(self):
        status = "wypożyczony" if self.wypozyczony else "dostępny"
        return f"Samochód o numerze rejestracyjnym {self.nr_rej}, marki {self.marka}, z roku {self.rok} jest {status}."
        
class Wypozyczalnia:
    def __init__ (self):
        self.df = pd.DataFrame(columns=["nr_rej", "marka", "model", "rok", "paliwo", "wypozyczony"])
    
    def wczytaj_baze(self, plik="baza_pojazdow.json"):
        with open(plik, 'r') as f:
            dane = json.load(f)
        self.df = pd.DataFrame(dane)
    
    def zapisz_baze(self, plik="baza_pojazdow.json"):
        self.df.to_json(plik)

    def dodaj_samochod (self, samochod):
        samochod_as_df = pd.DataFrame([vars(samochod)])
        self.df = pd.concat([self.df, samochod_as_df], ignore_index = True)
        self.zapisz_baze()
    
    def usun_samochod(self, nr_rej):
        samochod_idx = self.df[self.df['nr_rej'] == nr_rej].index
        if not samochod_idx.empty:
            self.df = self.df.drop(samochod_idx)
            self.zapisz_baze()
            print (f"Samochód o nr rejestracyjnym {nr_rej} został usunięty z bazy.")
        else:
            print (f"Samochód o nr rejestracyjnym {nr_rej} nie został usunięty z bazy.")

    
    def wyszukaj_po_paramterach (self, **kwargs):
        mask = pd.Series([True] * len(self.df))
        for k, v in kwargs.items():
            mask = mask & (self.df[k] == v)
        return self.df[mask]

    def wypozycz_samochod(self, nr_rej):
        samochod_idx = self.df[self.df['nr_rej'] == nr_rej].index
        if not samochod_idx.empty:
            print(f"Status wypożyczenia dla samochodu {nr_rej}: {self.df.loc[samochod_idx, 'wypozyczony'].values[0]}")
        
        #przeprowadzenie opercji wypożyczenia pojazdu
        if not samochod_idx.empty and self.df.loc[samochod_idx, 'wypozyczony'].values[0] == False:
            self.df.loc[samochod_idx, 'wypozyczony'] = True
            self.zapisz_baze()
            print (f"Samochód o nr rejestracyjnym {nr_rej} został wypożyczony.")
            return True
        else:
            print (f"Samochód o nr rejestracyjnym {nr_rej} jest niedostępny.")
            return False
            
    def zwroc_samochod (self, nr_rej):
        samochod_idx = self.df[self.df['nr_rej'] == nr_rej].index
        if not samochod_idx.empty and self.df.loc[samochod_idx, 'wypozyczony'].values[0]:
            self.df.loc[samochod_idx, 'wypozyczony'] = False
            self.zapisz_baze()
            print (f"Samochód o nr rejestracyjnym {nr_rej} został zwrócony.")
            return True
        return False
    
    def info(self):
        info_list = []
        for _, row in self.df.iterrows():
            status = "wypożyczony" if row['wypozyczony'] == True else 'dostępny'
            info_list.append(f"Samochód o numerze rejestracyjnym "
                f"{row['nr_rej']}, "
                f"marki {row['marka']}, "
                f"model {row['model']}, "
                f"z roku {row['rok']} ,"
                f"zasilany paliwem {row['paliwo']} jest {status}.")
        return info_list
            
if __name__ == "__main__":

    wypozyczalnia = Wypozyczalnia()
    wypozyczalnia.wczytaj_baze()

    def wprowadzenie_samochodu():
        nr_rej = input ("Podaj nr rejestracyjny pojazdu który chcesz wprowadzić: \n")
        marka = input ("Wprowadź markę: \n")
        model = input ("Wprowadź model samochodu: \n")
        rok = int(input ("Wprowadź rok produkcji: \n"))
        paliwo = input ("Wprowadź rodzaj paliwa (ON, benzyna, LPG, EV): \n")
        return Samochod(nr_rej, marka, model, rok, paliwo)

    def wypozyczanie_samochodu():
        while True:
            decyzja = input("Czy chcesz skorzystać z filtrów wyszukiwania? Tak/Nie \n")
            if decyzja.lower() == "tak":
                wynik = filtruj()
                if wynik.empty:
                    print ("Brak samochodów spełniających podane kryteria.")
                    return None
                for _, samochod in wynik.iterrows():
                    print (f"{samochod['nr_rej']} - {samochod['marka']} {samochod['model']} {samochod['rok']} {samochod['paliwo']}")
                break
            elif decyzja.lower() == "nie":
                for samochod_info in wypozyczalnia.info():
                    print (samochod_info)
                break
            else:
                print ("Wprowadzono niepoprawną komendę.")

        nr_rej = input ("Wprowadź nr rejestracyjny samochodu który chcesz wypożyczyć: \n")
        return nr_rej
    def zwrot_samochodu():
        nr_rej = input("Wprowadź nr rejestracyjny samochodu, który chcesz zwrócic: \n")
        return nr_rej

    def usuniecie_samochodu():
        for samochod_info in wypozyczalnia.info():
            print (samochod_info)
        nr_rej = input ("Wprowdź nr rejestracyjny pojazdu który chcesz usunąć z bazy:\n")
        return nr_rej 

    def filtruj():
        parametry = {}
        dostepne_pojazdy = wypozyczalnia.df[wypozyczalnia.df['wypozyczony'] == False]
        
        def wybor_paramteru(lista_opcji):
            while True:
                for i, opcja in enumerate(lista_opcji, 1):
                    print (f"{i}. {opcja}")
                try:
                    wybor = int(input("Wybierz numer paramteru:\n"))
                    if 1<= wybor <= len(lista_opcji):
                        return lista_opcji[wybor - 1]
                    else:
                        print ("Wybrano niepoprawny numer. Spróbuj ponownie.")
                except ValueError:
                    print ("Proszę wporwadzić poprawny numer. Spróbuj ponownie.")

        kolumny = ['marka', 'model', 'rok', 'paliwo']

        for kolumna in kolumny:
            decyzja = input (f"Czy chcesz sprawdzić dostępne pojazdy wg paramtru: {kolumna}? Tak/Nie\n")
            
            if decyzja.lower() == "tak":
                
                dostepne_opcje = dostepne_pojazdy[kolumna].unique().tolist()

                if not dostepne_opcje:
                    print (f"Brak dostępnych pojazdów dla wybranego kryterium.")
                    continue

                print (f"Dostępne pojazdy wg kryterium {kolumna}:")
                wybrana_opcja = wybor_paramteru(dostepne_opcje)
                parametry[kolumna] = wybrana_opcja

                dostepne_pojazdy = dostepne_pojazdy[dostepne_pojazdy[kolumna] == wybrana_opcja]

                if dostepne_pojazdy.empty:
                    print ("Brak dostępnych pojazdów spełniających podane wymagania.")
                    return pd.DataFrame()
        
        return dostepne_pojazdy

    # obsługa klienta - wypożycz/zwróc
    while True:
        pytanie1 = input ("Chcesz wypożyczyć lub zwrócić pojazd? \n"
                        "Wprowadź nr komendy:\n"
                        "1. Wypożyczam samochód\n"
                        "2. Zwracam samochód\n"
                        "3. Żadna z powyższych\n")
        if pytanie1 == "1":
            nr_rej = wypozyczanie_samochodu()
            wypozyczalnia.wypozycz_samochod(nr_rej)
        elif pytanie1 == "2":
            nr_rej = zwrot_samochodu()
            wypozyczalnia.zwroc_samochod(nr_rej)
        elif pytanie1 == "3":
            break
        else:
            print ("Wprowadzono nieprawidłową komendę. Proszę wybrać z listy.")

    # wprowadzanie nowego samochodu do bazy
    while True:
        pytanie2 = input ("Czy chcesz wprowadzić nowy samochód do bazy? Odpowiedz Tak lub Nie\n")
        if pytanie2.lower() == "tak":
            samochod = wprowadzenie_samochodu()
            wypozyczalnia.dodaj_samochod(samochod)
        else:
            print ("Nie zdecydowano się dodać samochodu")
            break
    # usunięcie samochodu z bazy
    while True:
        pytanie3 = input ("Czy chcesz usunąć pojazd z bazy? Odpowiedz Tak lub Nie\n")
        if pytanie3.lower() == "tak":
            nr_rej = usuniecie_samochodu()
            wypozyczalnia.usun_samochod(nr_rej)
            usunac_kolejny = input ("Czy chcesz usunąć kolejny samochód: Odpowiedz Tak lub Nie:\n")
            if usunac_kolejny.lower() == "tak":
                continue
            elif usunac_kolejny.lower() == "nie":
                break
            else:
                print ("Nieprawidłowa komenda, odpowiedz Tak lub Nie\n")
        if pytanie3.lower() == "nie":
            break
        else:
            print ("Nieprawidłowa komenda, odpowiedz Tak lub Nie.")
