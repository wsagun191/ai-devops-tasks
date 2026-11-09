Oto szczegółowe omówienie każdego elementu i etapu wspomnianego pliku `Jenkinsfile` oraz zestawienie najważniejszych dobrych praktyk przy tworzeniu rurociągów (pipelines) w Jenkinsie.

---

### Część 1: Co dzieje się w poszczególnych etapach Jenkinsfile?

1. **Konfiguracja globalna (`agent any` i `environment`)**
* `agent any` – Informuje Jenkinsa, że cały pipeline może wykonać się na **dowolnym dostępnym węźle (agencie)** roboczym, który ma odpowiednie narzędzia.
* `environment` – Definiuje zmienne globalne widoczne w całym pipeline (np. nazwę obrazu Docker oraz identyfikator bezpiecznych poświadczeń w Jenkinsie).


2. **Etap 1: Checkout (Pobranie kodu)**
* `checkout scm` – Pobiera najnowszą wersję kodu źródłowego z repozytorium (np. Git), z którego wywołano zadanie (job). Jenkins automatycznie wie, z którego brancha i commitu uruchomiono proces.


3. **Etap 2: Install Dependencies (Instalacja zależności)**
* `sh 'npm install'` – Uruchamia menedżer pakietów Node.js, który pobiera wszystkie biblioteki i zależności zdefiniowane w pliku `package.json` do katalogu `node_modules`.


4. **Etap 3: Run Tests (Uruchomienie testów)**
* `sh 'npm test'` – Wykonuje zestaw testów jednostkowych/integracyjnych aplikacji (np. napisanych w Jesten). Jeśli jakikolwiek test zakończy się błędem, cały pipeline natychmiast przerywa działanie.


5. **Etap 4: Build App (Budowanie aplikacji)**
* `sh 'npm run build'` – Przygotowuje aplikację do produkcji (np. transpiluje TypeScript do JavaScriptu, kompresuje pliki statyczne lub buduje paczkę dystrybucyjną).


6. **Etap 5: Build Docker Image (Budowanie obrazu kontenera)**
* `sh "docker build ..."` – Tworzy lokalny obraz Dockera na podstawie pliku `Dockerfile` znajdującego się w repozytorium. Obraz tagowany jest dwukrotnie: unikalnym numerem builda Jenkinsa (`${env.BUILD_NUMBER}`) oraz etykietą `latest`.


7. **Etap 6: Push Docker Image (Publikowanie w rejestrze)**
* `withCredentials(...)` – Pobiera z bezpiecznego magazynu Jenkinsa login i hasło do rejestru (np. Docker Hub) bez ujawniania ich w logach.
* `docker login` i `docker push` – Loguje się do rejestru i wysyła zbudowany obraz wraz z tagami na serwer zdalny, dzięki czemu gotowa aplikacja może zostać wdrożona na produkcję.


8. **Blok `post` (Czyszczenie i powiadomienia)**
* `cleanWs()` – Automatycznie czyści obszar roboczy (`workspace`) na agencie po zakończeniu pracy, oszczędzając miejsce na dysku.
* Bloki `success` / `failure` – Wypisują w konsoli status zakończenia całego procesu.



---

### Część 2: Najlepsze praktyki przy tworzeniu pipeline'ów Jenkins

1. **Stosuj deklaratywną składnię (Declarative Pipeline)**
* Zamiast starszej składni skryptowej (Groovy-heavy), używaj składni deklaratywnej (`pipeline { agent ... stages { ... } }`). Jest bardziej czytelna, łatwiejsza w utrzymaniu i zapewnia lepszą walidację struktury przed uruchomieniem.


2. **Nigdy nie przechowuj sekretów w kodzie (Credentials Management)**
* Hasła, klucze API, tokeny JWT czy dane logowania do rejestrów Docker nigdy nie powinny znajdować się w repozytorium Git ani wprost w pliku `Jenkinsfile`. Zawsze korzystaj z wbudowanego w Jenkinsa modułu **Credentials** i bloku `withCredentials`.


3. **Używaj unikalnego tagowania artefaktów (Avoid `latest` only)**
* Unikaj polegania wyłącznie na tagu `latest` przy budowaniu obrazów Docker w CI/CD. Zawsze znakuj obrazy unikalnymi identyfikatorami (np. numerem buildu `${env.BUILD_NUMBER}` lub wersją semantyczną/Commit SHA), aby zapewnić niezmienność (*immutability*) i możliwość odtworzenia wersji (rollback).


4. **Zasada "Fail Fast" (Szybkie wykrywanie błędów)**
* Układaj etupy w odpowiedniej kolejności: najpierw szybkie testy statyczne, linting i testy jednostkowe, a dopiero w dalszej kolejności czasochłonne operacje (takie jak budowanie obrazów Docker czy deploy). Pozwala to oszczędzać zasoby i szybko informować dewelopera o błędzie.


5. **Izolacja środowiska i czyszczenie przestrzeni**
* Zadbaj o to, aby buildy były powtarzalne i nie zależały od śmieci pozostałych po poprzednich uruchomieniach. Stosowanie `cleanWs()` na końcu lub uruchamianie etapów w dedykowanych kontenerach (np. z użyciem dyrektywy `agent { docker { ... } }`) gwarantuje czyste środowisko startowe.
