Stwórz prosty diagram ASCII Art przedstawiający połączenie klienta, serwera aplikacji i bazy danych.
ODPOWIEDŹ:

Oto prosty diagram ASCII Art przedstawiający architekturę trójwarstwową (klient, serwer aplikacji, baza danych):
+----------+           +-------------------+           +---------------+
|          |  HTTP/S   |                   |   SQL     |               |
|  Klient  | --------> | Serwer Aplikacji  | ------->  |  Baza Danych  |
| (Przeglą.)| <-------- |                   | <-------  |               |
+----------+           +-------------------+           +---------------+


Dodaj do diagramu opisy elementów i kierunki przepływu danych.
ODPOWIEDŹ:
+---------------------+
|      KLIENT         |
|  (np. Przeglądarka)  |
|                     |
| [PRZETWARZANIE UI]  |
+---------+-----------+
          |
          |
     (1) Żądanie HTTP/S: [Pobranie strony, Przesłanie danych]
          ---------------------->
          |
          v
+---------+-------------------------+
|      SERWER APLIKACJI           |
|      (np. Node.js, Python)       |
|                                 |
|   [LOGIKA BIZNESOWA & API]      |
+---------+-----------------+-------+
          |                 |
          |            (2) Zapytanie SQL/API: [Wstawienie, Odczyt, Aktualizacja]
          |                 ---------------------->
          |                 |
          v                 v
+---------+-------------+ +---------+-------------+
|     BAZA DANYCH       | |     BAZA DANYCH       |
|     (np. PostgreSQL)  | |     (np. PostgreSQL)  |
|                       | |                       |
| [TRWAŁE PRZECHOWYWANIE]| | [TRWAŁE PRZECHOWYWANIE]|
