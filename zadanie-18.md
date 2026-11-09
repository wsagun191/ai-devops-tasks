Odpowiedź do pierwszego pytania: 

Oto 5 kluczowych praktyk bezpieczeństwa, które należy wdrożyć dla aplikacji Dockerowych w środowisku produkcyjnym:

1. **Uruchamianie jako użytkownik niebędący rootem (Non-root User)**
* **Na czym polega:** Domyślnie kontenery Dockera uruchamiają procesy z uprawnieniami użytkownika `root` wewnątrz kontenera. Jeśli napastnik przełamie zabezpieczenia aplikacji, zyskuje pełną kontrolę nad kontenerem jako root.
* **Jak wdrożyć:** W pliku `Dockerfile` zdefiniuj dedykowanego użytkownika za pomocą instrukcji `USER` (np. `USER appuser`) przed uruchomieniem aplikacji, upewniając się wcześniej, że pliki aplikacji mają odpowiednie uprawnienia odczytu.


2. **Minimalizacja obrazów bazowych (Minimal Base Images)**
* **Na czym polega:** Im większy i bardziej rozbudowany obraz bazowy (np. pełny Ubuntu czy Debian), tym więcej zawiera zbędnych pakietów, narzędzi i potencjalnych dziur w zabezpieczeniach (podatności CVE).
* **Jak wdrożyć:** Korzystaj z minimalnych obrazów oficjalnych, takich jak `Alpine Linux` lub dystrybucje typu *distroless*, które zawierają wyłącznie środowisko uruchomieniowe języka i absolutnie niezbędne biblioteki, drastycznie zmniejszając tzw. powierzchnię ataku.


3. **Skanowanie obrazów pod kątem podatności (Vulnerability Scanning)**
* **Na czym polega:** Kod i biblioteki zewnętrzne (np. zależności z npm, pip) mogą zawierać znane luki bezpieczeństwa. Skanowanie pozwala wykryć je przed wdrożeniem na produkcję.
* **Jak wdrożyć:** Włącz automatyczne skanowanie obrazów w swoim procesie CI/CD za pomocą narzędzi takich jak `Trivy`, `Docker Scout`, `Clair` czy `Snyk`. Blokuj budowanie lub wdrażanie obrazów, które zawierają krytyczne podatności.


4. **Bezpieczne zarządzanie sekretami (Secrets Management)**
* **Na czym polega:** Hasła, klucze API, tokeny JWT czy certyfikaty nigdy nie powinny być "zaszyte" na stałe w kodzie aplikacji ani w plikach `Dockerfile` czy plain-textowych plikach konfiguracyjnych (np. `docker-compose.yml`), ponieważ łatwo je wtedy wycieknąć.
* **Jak wdrożyć:** Używaj dedykowanych mechanizmów zarządzania sekretami, takich jak *Docker Secrets* (w trybie Swarm), *Kubernetes Secrets*, HashiCorp Vault lub bezpiecznego wstrzykiwania zmiennych środowiskowych podczas uruchamiania kontenera z zewnętrznego, szyfrowanego magazynu.


5. **Ograniczanie uprawnień i zasobów kontenera (Resource & Capability Restrictions)**
* **Na czym polega:** Kontenery powinny mieć dostęp tylko do tych zasobów systemowych, które są im absolutnie niezbędne do działania, zgodnie z zasadą najmniejszego uprzywilejowania.
* **Jak wdrożyć:**
* Uruchamiaj kontenery w trybie tylko do odczytu systemu plików (`--read-only`), jeśli aplikacja nie musi zapisywać danych lokalnie (a jeśli musi – montuj dedykowane wolumeny).
* Ograniczaj zasoby sprzętowe (CPU, pamięć RAM) za pomocą flag `--memory` i `--cpus`, aby zapobiec atakom typu Denial of Service (DoS) poprzez wyczerpanie zasobów hosta.
* Odrzucaj niepotrzebne uprawnienia jądra Linuksa za pomocą flagi `--cap-drop=ALL` i dodawaj tylko te wymagane (`--cap-add`).

Odpowiedź do uzupełnienia:

Aby wdrożyć **pierwszą praktykę** (uruchamianie kontenera jako użytkownik niebędący rootem) w swojej aplikacji, musisz wykonać dwa kroki: zmodyfikować `Dockerfile` (aby utworzyć użytkownika i przekazać mu uprawnienia do plików) oraz odpowiednio skonfigurować plik `docker-compose.yml`.

Oto jak to zrobić krok po kroku:

---

### 1. Zmiany w `Dockerfile`

W pliku `Dockerfile` musisz utworzyć dedykowanego użytkownika oraz grupę, zmienić właściciela plików aplikacji, a na samym końcu przełączyć kontekst za pomocą instrukcji `USER`.

Poniżej znajduje się przykład dla aplikacji opartej na Node.js (na bazie Alpine Linux):

```dockerfile
FROM node:18-alpine

# 1. Utworzenie dedykowanej grupy i użytkownika (specyficzne dla Alpine)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 2. Ustawienie katalogu roboczego
WORKDIR /app

# 3. Kopiowanie plików zależności
COPY package*.json ./
RUN npm install

# 4. Kopiowanie reszty kodu aplikacji
COPY . .

# 5. Zmiana właściciela katalogu /app na naszego nowego użytkownika
# (Ważne, aby użytkownik miał prawo odczytu/zapisu tam, gdzie tego potrzebuje)
RUN chown -R appuser:appgroup /app

# 6. Przełączenie na użytkownika niebędącego rootem (od tego momentu wszystkie polecenia i procesy działają jako appuser)
USER appuser

# 7. Uruchomienie aplikacji
EXPOSE 3000
CMD ["npm", "start"]

```

> **Wskazówka dla innych systemów:** Jeśli Twoim obrazem bazowym jest Ubuntu/Debian, zamiast `addgroup` i `adduser` używasz standardowych poleceń:
> `RUN groupadd -r appgroup && useradd -r -g appgroup appuser`

---

### 2. Zmiany w `docker-compose.yml`

W pliku `docker-compose.yml` możesz dodatkowo wymusić lub upewnić się, że kontener uruchomi się z odpowiednimi uprawnieniami. Możesz to zrobić na dwa sposoby:

#### Sposób A: Poleganie na ustawieniu z Dockerfile (rekomendowane)

Jeśli w `Dockerfile` poprawnie zdefiniowałeś instrukcję `USER appuser`, `docker-compose` automatycznie ją odczyta i zastosuje. Twój plik może wyglądać tak:

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production

```

#### Sposób B: Wymuszenie użytkownika w `docker-compose.yml`

Możesz również zdefiniować użytkownika bezpośrednio w pliku compose (podając np. ID użytkownika i grupy, co zapobiega problemom z uprawnieniami do montowanych wolumenów):

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    # Wymuszenie uruchomienia jako konkretny UID:GID (np. użytkownik 1000)
    user: "1000:1000"

```

---

### Dlaczego to ważne i na co uważać?

* **Ochrona hosta:** Jeśli napastnik zdobędzie zdalną kontrolę nad aplikacją wewnątrz kontenera, nie uzyska uprawnień `root` na hoście ani w innych kontenerach.
* **Uprawnienia do plików (Volumes):** Jeśli montujesz wolumeny (np. na logi lub bazę danych), upewnij się, że nowo utworzony użytkownik (`appuser`) ma prawa do zapisu w tych katalogach. W przeciwnym razie aplikacja może zgłosić błąd `EACCES: permission denied`.
