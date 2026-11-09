
### Krótkie omówienie poszczególnych etapów:

1. **Checkout kodu:** Pobranie aktualnego stanu kodu źródłowego z repozytorium (np. GitHub/GitLab) dla konkretnego brancha lub commita.
2. **Budowanie:** Instalacja zależności (`npm install`) oraz kompilacja / przygotowanie artefaktów aplikacji webowej.
3. **Testy jednostkowe:** Weryfikacja poszczególnych modułów logiki biznesowej pod kątem poprawności działania.
4. **Analiza statyczna kodu:** Sprawdzenie jakości kodu, wykrywanie zapachów kodu (*code smells*) oraz długu technologicznego za pomocą narzędzi takich jak SonarQube.
5. **Bezpieczeństwo:** Skanowanie zależności pod kątem znanych podatności (np. `npm audit` / Snyk) oraz analiza statyczna bezpieczeństwa kodu (SAST).
6. **Budowanie obrazu Docker:** Spakowanie aplikacji wraz z jej środowiskiem uruchomieniowym do niezależnego obrazu kontenera.
7. **Testy integracyjne:** Uruchomienie zbudowanego obrazu w izolowanym środowisku Jenkinsa w celu przetestowania interakcji z bazą danych lub zewnętrznymi serwisami.
8. **Wdrożenie na Staging:** Automatyczny deploy aplikacji na środowisko testowe przedprodukcyjne, gdzie mogą być przeprowadzane dodatkowe testy akceptacyjne.
9. **Zatwierdzenie ręczne (Gate):** Mechanizm bramki jakości (*Quality Gate* / *Manual Approval*), w którym właściciel projektu lub tester musi zatwierdzić przejście na produkcję.
10. **Produkcja:** Finalne wypuszczenie aplikacji webowej na live (np. za pomocą Kubernetes, Docker Swarm lub SSH na serwer produkcyjny).
