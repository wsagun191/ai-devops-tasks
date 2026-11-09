Standardowym i najnowocześniejszym sposobem na zarządzanie konfiguracją Jenkinsa za pomocą plików (tzw. *Infrastructure as Code*) jest mechanizm **Jenkins Configuration as Code (JCasC)**. Pozwala on zdefiniować całe środowisko – od liczby wykonawców, przez narzędzia, aż po zadania – w jednym pliku konfiguracyjnym w formacie YAML (`jenkins.yaml`).

Poniżej znajdziesz kompletny plik konfiguracyjny, listę wtyczek oraz instrukcję, jak uruchomić Jenkinsa z tym szablonem.

---

### 1. Plik konfiguracyjny JCasC (`jenkins.yaml`)

Ten plik definiuje podstawowe ustawienia, globalne narzędzia oraz przykładowe zadanie typu Pipeline.

```yaml
jenkins:
  # Podstawowe ustawienia (liczba wykonawców)
  numExecutors: 4
  quietPeriod: 5
  scmCheckoutRetryCount: 2
  
  # Globalne właściwości systemowe / timeouty (np. timeout sesji lub globalne timeouty buildów)
  globalNodeProperties:
    - envVars:
        env:
          - key: "DEFAULT_TIMEOUT_MINUTES"
            value: "60"

unclassified:
  # Konfiguracja globalna (np. lokalizacja Jenkinsa)
  location:
    url: "http://localhost:8080/"

# Globalny katalog narzędzi (Maven, Node.js)
tool:
  maven:
    installations:
      - name: "Maven 3.8.8"
        properties:
          - installSource:
              installers:
                - maven:
                    id: "3.8.8"
                    
  nodejs:
    installations:
      - name: "NodeJS 18"
        properties:
          - installSource:
              installers:
                - nodeJS:
                    id: "18.16.0"

# Definicja zadań (w tym przykładowy Pipeline)
jobs:
  - script: >
      pipeline {
          agent any
          tools {
              nodejs "NodeJS 18"
              maven "Maven 3.8.8"
          }
          stages {
              stage('Weryfukj Środowisko') {
                  steps {
                      echo 'Sprawdzanie wersji narzędzi...'
                      sh 'node -v'
                      sh 'npm -v'
                      sh 'mvn -version'
                  }
              }
              stage('Przykładowy Krok') {
                  steps {
                      echo 'Pipeline JCasC działa poprawnie!'
                  }
              }
          }
      }

```

---

### 2. Lista wymaganych wtyczek (`plugins.txt`)

Aby JCasC oraz narzędzia działały poprawnie, Jenkins potrzebuje odpowiednich wtyczek. Utwórz plik `plugins.txt`:

```text
configuration-as-code:latest
git:latest
workflow-aggregator:latest
nodejs:latest
maven-plugin:latest
docker-workflow:latest

```

---

### 3. Kroki instalacji i uruchomienia Jenkinsa z tym szablonem

Najprostszym i najbardziej powtarzalnym sposobem na uruchomienie Jenkinsa z gotową konfiguracją jest użycie **Dockera**.

#### Krok 1: Przygotowanie struktur katalogów

Stwórz na dysku lokalny katalog, np. `jenkins-config`, a w nim umieść:

1. Plik konfiguracyjny o nazwie **`jenkins.yaml`** (zawierający kod z punktu 1).
2. Plik z wtyczkami o nazwie **`plugins.txt`** (zawierający listę z punktu 2).

#### Krok 2: Uruchomienie kontenera Docker

Uruchom poniższe polecenie w terminalu w katalogu, gdzie znajdują się Twoje pliki. Automatycznie pobierze ono obraz Jenkinsa, zainstaluje wtyczki z pliku `plugins.txt` oraz wgra konfigurację JCasC:

```bash
docker run -d \
  --name jenkins-server \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/jenkins.yaml:/var/jenkins_home/jenkins.yaml \
  -v $(pwd)/plugins.txt:/var/jenkins_home/plugins.txt \
  -e CASC_JENKINS_CONFIG=/var/jenkins_home/jenkins.yaml \
  --user root \
  jenkins/jenkins:lts

```

*Wyjaśnienie kluczowych flag:*

* `-v $(pwd)/jenkins.yaml:/var/jenkins_home/jenkins.yaml` – Montuje Twój plik JCasC do kontenera.
* `-e CASC_JENKINS_CONFIG=...` – Wskazuje Jenkinsowi ścieżkę do pliku konfiguracyjnego przy starcie.
* `--user root` oraz `-v /var/run/docker.sock:...` – Pozwalają na uruchamianie poleceń Dockera bezpośrednio z wnętrza pipeline'ów Jenkinsa (Docker-in-Docker / Docker socket binding).

#### Krok 3: Automatyczna instalacja wtyczek

Aby Jenkins automatycznie zainstalował wtyczki z pliku `plugins.txt` przy pierwszym uruchomieniu, możesz skorzystać ze standardowego skryptu inicjalizacyjnego Jenkinsa lub wtyczki *Plugin Manager*. W nowoczesnych obrazach LTS można to zrobić, uruchamiając w tle narzędzie CLI lub korzystając z gotowego skryptu instalatora wtyczek (`jenkins-plugin-cli`).

#### Krok 4: Pierwsze logowanie

1. Otwórz przeglądarkę i wejdź pod adres: `http://localhost:8080`.
2. Pobierz początkowe hasło administratora z logów kontenera, wpisując w terminalu:
```bash
docker logs jenkins-server

```


3. Wklej hasło w interfejsie, pomiń domyślny kreator instalacji wtyczek (ponieważ JCasC i Twoje pliki zajmą się konfiguracją) i ciesz się w pełni gotowym, automatycznie skonfigurowanym środowiskiem z predefiniowanym pipeline'em!
