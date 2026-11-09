
### Jakie zmiany zaszły?

1. **Wzorzec Słownikowy (Lookup Map / Configuration Object):** Usunięto długą i powtarzalną strukturę warunkową `if-else if` na rzecz obiektu `CONFIGS`, który przechowuje mapowanie nazw środowisk na odpowiednie konfiguracje.
2. **Parametr domyślny:** Wykorzystano domyślną wartość parametru w funkcji (`env = DEFAULT_ENV`), co upraszcza obsługę sytuacji, gdy argument nie zostanie przekazany.
3. **Bezpieczne pobieranie wartości i fallback:** Użyto operatora logicznego `||`, który w przypadku podania nieznanego środowiska (nieznanego klucza w obiekcie) automatycznie zwraca konfigurację domyślną (zamiast rzucać błędem).

---

### Korzyści z wprowadionych zmian

* **Lepsza czytelność (Readability):** Kod jest krótszy, bardziej płaski (brak zagnieżdżeń) i od razu widać strukturę danych dla wszystkich środowisk w jednym miejscu.
* **Łatwiejsza rozszerzalność (Maintainability):** Dodanie nowego środowiska (np. `qa` czy `ci`) wymaga jedynie dopisania jednej linii w obiekcie `CONFIGS`, bez modyfikowania logiki warunkowej w samej funkcji.
* **DRY (Don't Repeat Yourself):** Wyeliminowano powielanie słowa kluczowego `return` oraz powtarzalną strukturę zwracanych obiektów.
* **Wydajność:** Wyszukiwanie klucza w obiekcie stałym w JS ma złożoność $O(1)$, co jest bardziej eleganckie niż wielokrotne sprawdzanie warunków tekstowych w bloku `if-else`.
