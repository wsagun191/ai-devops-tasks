Oto szczegółowe wyjaśnienie działania przedstawionego wcześniej skryptu w Pythonie, użytych w nim bibliotek oraz sposobu jego uruchamiania i wykorzystania.

---

### 1. Jakich bibliotek używa skrypt?

Skrypt opiera się na jednej zewnętrznej, potężnej i standardowej bibliotece w ekosystemie Pythona do obsługi zapytań HTTP:

* **`requests`** – Najpopularniejsza biblioteka HTTP w Pythonie. Umożliwia łatwe wysyłanie żądań GET i POST, obsługę ciasteczek, nagłówków oraz uwierzytelniania.
* **`requests.Session()`** – Obiekt sesji, który pozwala zachować parametry połączenia (np. nagłówki, mechanizmy autoryzacji) między wieloma zapytaniami, co poprawia wydajność i upraszcza kod.
* **`requests.auth.HTTPBasicAuth`** – Klasa służąca do przekazywania danych uwierzytelniających w formacie Basic Auth (nazwa użytkownika i token API) w nagłówku HTTP.



*(Uwaga: Skrypt korzysta również z wbudowanych w Pythona modułów, takich jak obsługa wyjątków i struktur danych, więc nie wymaga instalowania dodatkowych pakietów poza `requests`).*

---

### 2. Jak działa ten skrypt? (Architektura krok po kroku)

Skrypt został zaprojektowany z użyciem programowania obiektowego – główną logikę zamyka klasa **`JenkinsClient`**.

1. **Inicjalizacja i Uwierzytelnianie (`__init__`)**
Klient przyjmuje adres URL serwera Jenkins oraz dane dostępowe. Tworzy instancję `requests.Session()` i na stałe podpina pod nią uwierzytelnianie `HTTPBasicAuth`. Dzięki temu każde kolejne zapytanie automatycznie przesyła poświadczenia.
2. **Obejście zabezpieczeń CSRF (`_get_crumb`)**
Nowoczesne instancje Jenkinsa chronią operacje modyfikujące stan (np. uruchamianie buildów metodą `POST`) za pomocą tokenów CSRF zwanych *crumbami*. Metoda ta odpytuje endpoint `/crumbIssuer/api/json` i pobiera unikalny nagłówek zabezpieczający, który jest doklejaony do żądań typu POST.
3. **Pobieranie listy zadań (`list_jobs`)**
Wysyła zapytanie `GET` na adres główny Jenkinsa z filtrem optymalizacyjnym `?tree=jobs[name,url,color]`. Ten filtr to kluczowa optymalizacja API Jenkinsa – zamiast zwracać ogromne pliki XML/JSON z pełną konfiguracją każdego projektu, pobiera wyłącznie podstawowe metadane (nazwę, adres i status w postaci koloru).
4. **Sprawdzanie statusu buildów (`get_job_build_status`)**
Odpytuje konkretne zadanie (`/job/{job_name}/api/json`) również z użyciem filtra `tree`, wyciągając informacje o ostatnim, ostatnim udanym oraz ostatnim nieudanym buildzie.
5. **Uruchamianie zadania (`trigger_job`)**
Wysyła żądanie `POST` na endpoint `/job/{job_name}/build`, dołączając wcześniej pobranie zabezpieczenie CSRF (*crumb*). Skutkuje to zainicjowaniem nowego buildu na serwerze Jenkins.

---

### 3. Jak używać tego skryptu? (Przykładowe polecenia)

#### Krok 1: Instalacja wymaganej biblioteki

Upewnij się, że masz zainstalowanego Pythona oraz zainstaluj pakiet `requests` za pomocą terminala:

```bash
pip install requests

```

#### Krok 2: Przygotowanie tokena w Jenkinsie

Zamiast używać głównego hasła, w Jenkinsie zaleca się generowanie Tokenu API:

1. Zaloguj się do Jenkinsa.
2. Kliknij na swoją nazwę użytkownika w prawym górnym rogu $\rightarrow$ **Configure** (Konfiguracja).
3. Znajdź sekcję **API Token** i kliknij **Add new Token** (Dodaj nowy token). Skopiuj wygenerowaną wartość.

#### Krok 3: Uruchomienie i modyfikacja skryptu

Zapisz kod do pliku np. `jenkins_manager.py`, uzupełnij dane konfiguracyjne na końcu pliku, a następnie uruchom go w terminalu:

```bash
python jenkins_manager.py

```

##### Przykładowe modyfikacje kodu (co możesz zrobić w bloku `if __name__ == "__main__":`):

* **Tylko wypisanie wszystkich zadań:**
```python
jenkins = JenkinsClient("http://localhost:8080", "admin", "twoj_token_api")
for job in jenkins.list_jobs():
    print(f"Projekt: {job['name']} [Stan: {job['color']}]")

```


* **Bezpośrednie uruchomienie wybranego zadania:**
```python
jenkins = JenkinsClient("http://localhost:8080", "admin", "twoj_token_api")

# Uruchomienie joba o nazwie "web-app-deploy"
jenkins.trigger_job("web-app-deploy")

```


* **Sprawdzenie statusu konkretnego zadania:**
```python
jenkins = JenkinsClient("http://localhost:8080", "admin", "twoj_token_api")
status = jenkins.get_job_build_status("web-app-deploy")
print(status)

```
