Dane wyjściowe:
Metryki serwera API (ostatnie 24h):

Średni czas odpowiedzi: 230ms
95 percentyl czasu odpowiedzi: 450ms
99 percentyl czasu odpowiedzi: 1200ms
Liczba zapytań: 15,000
Liczba błędów 5xx: 120
Użycie CPU: średnio 45%, max 80%
Użycie pamięci: średnio 2.1GB, max 3.5GB (z 4GB dostępnych)

Analiza przez gemini:
Na podstawie przedstawionych metryk można zauważyć kilka istotnych sygnałów ostrzegawczych. Co szczególnie zwraca uwagę, to **stosunkowo niski ruch** (15 000 zapytań przez 24 godziny to średnio ok. 0.17 zapytania na sekundę) przy **stosunkowo wysokim zużyciu zasobów**.

Oto szczegółowa interpretacja danych, identyfikacja problemów oraz rekomendacje usprawnień.

---

### 1. Interpretacja i zidentyfikowane problemy

* **Krytyczne zużycie pamięci (Zagrożenie OOM):**
Zużycie pamięci na poziomie średnio 2.1 GB, z pikami do **3.5 GB z dostępnych 4 GB**, to główny powód do natychmiastowego niepokoju. Oznacza to zaledwie 500 MB zapasu. Jeśli obciążenie wzrośnie lub wystąpi wyciek pamięci (*memory leak*), proces zostanie natychmiast ubity przez system operacyjny (OOM Killer), powodując całkowity przestój serwera.
* **Wysoki „długi ogon” opóźnień (P99 = 1.2s):**
Podczas gdy średni czas odpowiedzi (230ms) i P95 (450ms) wyglądają w miarę poprawnie, **1% najwolniejszych zapytań zajmuje ponad 1.2 sekundy**. Dla użytkowników doświadczających tych opóźnień aplikacja wydaje się powolna lub niesprawna.
* **Wysoki wskaźnik błędów 5xx:**
120 błędów serwera przy 15 000 zapytań daje wskaźnik awaryjności na poziomie ok. **0.8%**. Standardowo dąży się do wartości poniżej 0.1%. Oznacza to, że co 125. zapytanie kończy się awarią po stronie serwera.
* **Niska efektywność zasobów (CPU max 80%):**
Osiąganie 80% użycia CPU przy tak niskim ruchu sugeruje, że w kodzie aplikacji znajdują się ciężkie operacje, nieoptymalne algorytmy lub zapytania do bazy danych, które nadmiernie obciążają procesor.

---

### 2. Sugerowane działania naprawcze

#### A. Natychmiastowe (Stabilizacja i bezpieczeństwo)

1. **Analiza wycieków pamięci i profilowanie:** Sprawdź logi pod kątem błędów `JavaScript heap out of memory` (jeśli to Node.js) lub odpowiedników dla innych środowisk. Wykonaj profilowanie pamięci (np. *heap snapshot*), aby ustalić, co zatrzymuje tyle RAM-u.
2. **Zwiększenie zasobów (Tymczasowe):** Jeśli to możliwe, skaluj pionowo zasoby RAM (np. z 4 GB do 8 GB), aby kupić czas na dokładniejszą analizę kodu i zapobiec awariom OOM.
3. **Konfiguracja alertów:** Ustaw powiadomienia (np. w Prometheus/Grafana czy Datadog), gdy zużycie pamięci przekroczy 85% oraz gdy wskaźnik błędów 5xx nagle wzrośnie.

#### B. Średnioterminowe (Optymalizacja wydajności i P99)

1. **Optymalizacja bazy danych (DB Profiling):** Piki opóźnień (P99) oraz wysokie użycie CPU najczęściej wynikają z braku indeksów w bazie danych lub problemów typu *N+1 queries*. Przeanalizuj najwolniejsze zapytania SQL/NoSQL.
2. **Wdrożenie cachowania (Redis/Memcached):** Jeśli te same dane są często odpytywane z bazy, wprowadzenie warstwy pamięci podręcznej drastycznie odciąży CPU i zmniejszy czas odpowiedzi.
3. **Identyfikacja błędów 5xx:** Przeanalizuj stack trace zebrany przez system monitorowania błędów (np. Sentry, Logstash), aby dowiedzieć się, które dokładnie endpointy generują te 120 błędów i dlaczego (np. timeouty połączeń z bazą danych, niedostępne zewnętrzne API).
