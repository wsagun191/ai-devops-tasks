Oto prosty diagram w formacie **Mermaid**, który przedstawia standardowy proces CI/CD (Continuous Integration / Continuous Deployment):

```mermaid
graph LR
    A[Commit] --> B[Build]
    B --> C[Test]
    C --> D[Deploy]

```

### Opis poszczególnych kroków:

* **Commit:** Programista wysyła (pushuje) swój kod do zdalnego repozytorium (np. Git).
* **Build:** System CI pobiera kod i buduje aplikację (kompilacja, przygotowanie artefaktów).
* **Test:** Automatyczne uruchamianie testów jednostkowych i integracyjnych w celu wykrycia błędów.
* **Deploy:** Automatyczne wdrożenie przetestowanej aplikacji na środowisko testowe lub produkcyjne.


<img width="1278" height="818" alt="Zrzut ekranu 2026-11-09 152130" src="https://github.com/user-attachments/assets/3f1a509a-c28e-43d8-807f-900f9533dcc7" />
