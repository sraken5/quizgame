#Uniwersalna gra-quiz, która pobiera pytania z zewnętrznego pliku .json (domyślnie dodałem bazę pytań egzaminu INF.03/EE.09/E.14)
#Program działać będzie także dla customowej bazy pytań, lecz trzeba mieć na uwadze, że bez żadnego pliku .json program nie będzie w pełni funkcjonował

import os 
import random
import json

def clear_console():
    # Czyści konsolę w zależności od systemu operacyjnego
    os.system('cls' if os.name == 'nt' else 'clear')



class BazaPytan(): #Klasa służy do zaimportowania bazy pytań z pliku .json oraz do zwracania losowego pytania z listy
    def __init__(self, title):
        self.title = title
        self.lista_pytan = []

    def import_json(self, plik):
        with open(plik, "r", encoding="utf-8") as file: #dodałem encoding, ponieważ baza pytań zawiera polskie znaki, co generowało błąd UnicodeDecodeError
            data = json.load(file)
        for element in data:
            pytanie = Pytanie(element[0], element[1], element[2]) #przypisuję klasie Pytanie() dane z jsona, generując pytanie
            self.lista_pytan.append(pytanie)

    def zwroc_losowe_pytanie(self):
        if self.lista_pytan: #sprawdzam, czy lista_pytan zawiera jakieś dane w środku
            return random.choice(self.lista_pytan)
        else:
            return False



class Pytanie(): #obsługa działania losowanych pytań
    def __init__(self, tresc, odp, correct_key):
        self.tresc = tresc # treść pytania
        self.odp = odp  # słownik z pytaniami
        self.correct_key = correct_key  # Poprawna odpowiedź - A, B, C lub D

    def __str__(self):
        tekst = self.tresc + "\n\n"
        for klucz in self.odp:
            tekst += klucz + ". " + self.odp[klucz] + "\n"
        return tekst

    def obsluga_pytania(self):
        print(self)
        wybor = input("Wybierz odpowiedź (A-D): ").upper().strip()
        while wybor not in self.odp:
            wybor = input("Nieprawidłowy wybór. Wybierz A, B, C lub D: ").upper().strip()
        if wybor == self.correct_key:
            clear_console()
            print("Poprawna odpowiedź!\n\n")
            return True
        else:
            clear_console()
            print(f"Błędna odpowiedź. Poprawna to: {self.correct_key}. {self.odp[self.correct_key]}\n\n")
            return False
        
        


class Game(): #wybór rodzaju gry, główna logika programu
    def __init__(self):
        self.baza_pytan = None

    def tryb_rozgrywki(self):
        wybor_trybu_rozgrywki = str(input("|   (P)ojedyncze pytania   |   (E)gzamin   |   ")).upper().strip()
        if wybor_trybu_rozgrywki not in ("P", "E"):
            print("Niepoprawny tryb.")
        elif wybor_trybu_rozgrywki == "P":
            self.__pojedyncze_pytania()
        elif wybor_trybu_rozgrywki == "E":
            self.__egzamin()

    def __pojedyncze_pytania(self):
        while True:
            pytanie = self.baza_pytan.zwroc_losowe_pytanie()
            pytanie.obsluga_pytania()
            wybor = str(input("|   (K)olejne pytanie   |   (E)xit   |   ")).upper().strip()
            if wybor not in ("K", "E"):
                print("Nieobsługiwana operacja.")
                break
            elif wybor == "K":
                continue
            elif wybor == "E":
                break

    def __egzamin(self):
        punkty = 0
        for i in range(1,41):
            pytanie = self.baza_pytan.zwroc_losowe_pytanie()
            
            if pytanie.obsluga_pytania():
                punkty += 1

        if punkty >= 20:
            print(f"Zdany egzamin\nUzyskana liczba punktów: {punkty}/40")
        else:
            print(f"Niezdany egzamin\nUzyskana liczba punktów {punkty}/40")
            
    def set_baza_pytan(self, baza): #metoda przypisuje do gry bazę pytań
        if isinstance(baza, BazaPytan): #sprawdzam tutaj, czy argument jest instancją klasy BazaPytan
            self.baza_pytan = baza
        else:
            print("Przekazana wartość nie jest instancją klasy BazaPytan!") 


#!!! Nie usuwać - służy to do zaimportowania bazy pytań z pliku .json
baza_pytan = BazaPytan("INF.03")
baza_pytan.import_json("informatyk.json")

gra = Game()
gra.set_baza_pytan(baza_pytan)
gra.tryb_rozgrywki()



