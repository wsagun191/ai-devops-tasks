Komunikat błędu: ERROR: for app Cannot start service app: driver failed programming external connectivity on endpoint app (172.18.0.2): Error starting userland proxy: listen tcp4 0.0.0.0:3000: bind: address already in use

wyjaśnienie gemini:
Ten błąd oznacza, że Docker próbuje uruchomić usługę i przypisać ją do portu **3000** na Twoim komputerze, ale ten port jest już zajęty przez inny działający proces, program lub inny kontener Docker. System operacyjny odrzuca żądanie ("address already in use").

Oto jak krok po kroku rozwiązać ten problem:

1. **Znajdź proces zajmujący port 3000:** Terminal.
Uruchom w terminalu polecenie, aby sprawdzić, co dokładnie blokuje port 3000:

```bash
sudo lsof -i :3000

```

*Weryfikacja:* W wynikach polecenia zobaczysz nazwę programu (np. `node`, `python`) oraz jego numer **PID** w drugiej kolumnie.


2. **Zatrzymaj konfliktowy proces:** Zarządzanie procesami.
Zabij proces blokujący port, wpisując (zastąp `<PID>` numerem uzyskanym w poprzednim kroku):

```bash
sudo kill -9 <PID>

```

*Weryfikacja:* Ponowne wpisanie `sudo lsof -i :3000` nie powinno już wyświetlić żadnego aktywnego procesu.


3. **Uruchom aplikację ponownie:** Docker Compose.
Gdy port jest wolny, uruchom swój projekt:

```bash
docker compose up

```

*Weryfikacja:* Kontener uruchomi się poprawnie bez komunikatu o błędzie binda.
