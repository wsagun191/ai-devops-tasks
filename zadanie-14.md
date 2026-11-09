May 19 10:15:32 server dockerd[1234]: time="2025-05-19T10:15:32.123456789Z" level=info msg="Container 78a2b3c4 health status changed from starting to healthy"
May 19 10:16:45 server dockerd[1234]: time="2025-05-19T10:16:45.987654321Z" level=info msg="Container 78a2b3c4 failed to connect to 172.17.0.3:5432: connection refused"
May 19 10:16:47 server dockerd[1234]: time="2025-05-19T10:16:47.246813579Z" level=warning msg="Container 78a2b3c4 health status changed from healthy to unhealthy"

Co się dzieje w tych logach? Jakie problemy można zidentyfikować?

ODPOWIEDŹ:
Na podstawie przedstawionych logów systemowych Dockera można prześledzić sekwencję zdarzeń dotyczącą pracy kontenera o ID `78a2b3c4`.

Oto szczegółowa analiza tego, co się dzieje:

### 1. Przebieg zdarzeń krok po kroku

* **Godzina 10:15:32 – Start i gotowość:**
Kontener przechodzi pomyślnie testy wstępne (healthcheck). Jego status zmienia się z `starting` (uruchamianie) na `healthy` (zdrowy/gotowy do pracy). Oznacza to, że aplikacja wewnątrz kontenera poprawnie się zainicjalizowała.
* **Godzina 10:16:45 – Błąd połączenia sieciowego:**
Niecałą minutę później aplikacja w kontenerze próbuje nawiązać połączenie sieciowe pod adres `172.17.0.3` na port `5432` (standardowy port dla bazy danych **PostgreSQL**). Próba ta kończy się niepowodzeniem z komunikatem `connection refused` (połączenie odrzucone). Oznacza to, że pod wskazanym adresem IP i portem nikt nie nasłuchuje lub usługa docelowa jest wyłączona/niedostępna.
* **Godzina 10:16:47 – Zmiana statusu na niezdrowy:**
W wyniku problemów z połączeniem (prawdopodobnie mechanizm healthcheck weryfikuje łączność z bazą danych lub aplikacja zgłasza awarię po utracie zależności), status kontenera zmienia się z `healthy` z powrotem na `unhealthy` (niezdrowy).

---

### 2. Jakie problemy można zidentyfikować?

1. **Awaria lub brak uruchomionej bazy danych:**
Port `5432` wskazuje na bazę PostgreSQL. Błąd `connection refused` oznacza, że kontener bazy danych (lub usługa zewnętrzna pod tym adresem IP) nie działa, uległ awarii, jeszcze się nie uruchomił albo ma błędnie skonfigurowaną sieć.
2. **Problem z komunikacją między kontenerami (Docker Networking):**
Adres `172.17.0.3` to wewnętrzny adres IP w sieci Dockera. Jeśli aplikacja próbuje połączyć się z innym kontenerem po surowym adresie IP, może to prowadzić do błędów, ponieważ adresy IP wewnątrz sieci dockerowych mogą się zmieniać przy restarcie kontenerów. Lepiej używać **nazw hostów / nazw serwisów** (szczególnie w Docker Compose).
3. **Zależności usług (Brak `depends_on` / mechanizmu ponawiania prób):**
Aplikacja prawdopodobnie wystartowała szybciej niż baza danych (stąd status `healthy` samego kontenera aplikacji, ale brak gotowości bazy). Aplikacja nie poradziła sobie z chwilową niedostępnością bazy i nie ma zaimplementowanego mechanizmu ponawiania prób połączenia (*retry policy*), przez co od razu uznała stan za krytyczny.
