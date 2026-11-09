Ignorowanie plików wymienionych w pliku `.gitignore` jest kluczowe dla zachowania bezpieczeństwa, wydajności oraz porządku w projekcie. Oto dlaczego poszczególne grupy plików powinny być pomijane w systemie kontroli wersji (Git):

### 1. Zależności (`node_modules/`)

* **Dlaczego:** Katalog `node_modules` potrafi zawierać dziesiątki tysięcy małych plików i ważyć setki megabajtów.
* **Korzyść:** Zamiast przesyłać je do repozytorium, każdy programista pobiera je lokalnie za pomocą polecenia `npm install`. Dzięki temu repozytorium jest małe, a jego klonowanie trwa sekundy, a nie minuty.

### 2. Pliki konfiguracyjne ze sekretami (`.env`, `.env.local`)

* **Dlaczego:** **To kwestia bezpieczeństwa.** Pliki te zawierają poufne dane: hasła do baz danych, klucze API, tajne tokeny czy dane dostępowe do serwerów.
* **Korzyść:** Zapobiega to przypadkowemu wyciekowi wrażliwych danych (szczególnie w publicznych repozytoriach na GitHubie), co mogłoby doprowadzić do przejęcia aplikacji lub usług zewnętrznych.

### 3. Pliki wynikowe kompilacji (`dist/`, `build/`)

* **Dlaczego:** Są to pliki generowane *automatycznie* przez kompilator lub bundler na podstawie kodu źródłowego.
* **Korzyść:** Committowanie gotowych plików builda prowadzi do ciągłych konfliktów przy mergowaniu kodu (merge conflicts) i niepotrzebnie powiększa historię repozytorium o rzeczy, które można w każdej chwili wygenerować na nowo poleceniem `npm run build`.

### 4. Pliki bazy danych (`data/`, `db/`, `mongodb_data/`)

* **Dlaczego:** Baza danych przechowuje dynamiczne dane stanu aplikacji, które stale się zmieniają i często mają postać dużych plików binarnych.
* **Korzyść:** Git nie radzi sobie dobrze z wersjonowaniem dużych, zmieniających się plików binarnych. Ponadto każdy programista powinien pracować na własnej, niezależnej instancji bazy danych (np. uruchamianej w kontenerze Docker), a nie dzielić ten sam stan bazy z innymi.

### 5. Pliki systemowe i edytorów (`.DS_Store`, `.vscode/`, `Thumbs.db`)

* **Dlaczego:** Są to śmieci tworzone automatycznie przez system operacyjny (np. macOS, Windows) lub Twój edytor kodu (np. VS Code).
* **Korzyść:** Różni programistów używają różnych systemów i edytorów. Pliki te nie wnoszą nic do kodu aplikacji, a ich brak zapobiega niepotrzebnemu "zaśmiecaniu" historii commitów prywatnymi preferencjami deweloperów.

### 6. Pliki logów (`*.log`)

* **Dlaczego:** Logi to tymczasowe zapisy zdarzeń z działania aplikacji, które dynamicznie rosną i zmieniają się z każdą sekundą.
* **Korzyść:** Dodawanie ich do Gita powodowałoby, że każdy commit zawierałby tysiące nieistotnych zmian w plikach tekstowych z błędami czy historią zapytań.
