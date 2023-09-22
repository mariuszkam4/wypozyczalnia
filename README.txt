# Wypożyczalnia Samochodów

Projekt skupia się na zarządzaniu wypożyczalnią samochodów, umożliwiając użytkownikowi dodawanie, wypożyczanie oraz zwracanie pojazdów.

## Klasy

### Samochod
Reprezentuje samochód w wypożyczalni. Posiada atrybuty takie jak numer rejestracyjny, marka, model, rok produkcji oraz rodzaj paliwa. Klasa zawiera również metody do wypożyczenia, zwrotu i wyświetlenia pełnych danych o samochodzie.

### Wypozyczalnia
Zarządza bazą danych samochodów w wypożyczalni. Umożliwia wczytanie bazy z pliku JSON, zapis bazy do pliku, dodawanie nowego samochodu do bazy, wypożyczenie samochodu, zwrot samochodu oraz wyświetlenie informacji o wszystkich samochodach.

## Funkcje pomocnicze
* `wprowadzenie_samochodu()`: Pozwala użytkownikowi wprowadzić dane nowego samochodu.
* `wypozyczanie_samochodu()`: Umożliwia użytkownikowi wybór samochodu do wypożyczenia.
* `zwrot_samochodu()`: Umożliwia użytkownikowi zwrot wypożyczonego samochodu.

## Interfejs użytkownika
Po uruchomieniu programu użytkownik ma możliwość wyboru pomiędzy wypożyczeniem samochodu, zwrotem samochodu lub wyjściem z programu. Dodatkowo program oferuje opcję dodania nowego samochodu do bazy danych wypożyczalni.

## Jak uruchomić?
Upewnij się, że masz zainstalowane niezbędne biblioteki (`pandas` i `json`), a następnie uruchom główny skrypt programu.
