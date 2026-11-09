Przyjrzyjmy się bliżej zaawansowanemu wyrażeniu regularnemu służącemu do walidacji adresu IPv4:

```regex
^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$

```

---

### Jak działa to wyrażenie regularne? (Krok po kroku)

Wyrażenie to dzieli adres IP na dwie główne części: **trzy pierwsze oktety z kropkami** oraz **czwarty (ostatni) oktet**. Każdy oktet musi spełniać rygorystyczny warunek bycia liczbą z zakresu od **0 do 255**.

1. **Kotwice początku i końca (`^` oraz `$`)**:
* `^` – Oznacza początek linii/ciągu znaków.
* `$` – Oznacza koniec linii/ciągu znaków. Gwarantują one, że sprawdzany jest *cały* ciąg, a nie tylko jego fragment.


2. **Blok pierwszych trzech oktetów `(?: ... ){3}**`:
* Cała sekcja wewnątrz nawiasów zewnętrznych jest powtórzona dokładnie **3 razy** `{3}`. Obejmuje ona liczbę oraz następującą po niej kropkę (`\.`).


3. **Logika sprawdzania liczby 0–255 (powtarzana w każdym oktecie)**:
Wewnątrz każdego oktetu znajduje się alternatywa (`|`), która dopasowuje liczby w trzech wariantach:
* `25[0-5]` – Dopasowuje liczby od **250 do 255**.
* `2[0-4][0-9]` – Dopasowuje liczby od **200 do 249** (cyfra `2`, po której następuje cyfra od `0` do `4`, a na końcu dowolna cyfra od `0` do `9`).
* `[01]?[0-9][0-9]?` – Dopasowuje liczby od **0 do 199** (opcjonalna cyfra setek `0` lub `1`, po której następuje cyfra dziesiątek i opcjonalna cyfra jedności).


4. **Czwarty oktet `(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)**`:
* To dokładnie taka sama reguła walidacji liczby 0–255, ale **bez kropki na końcu**, ponieważ adres IPv4 kończy się na czwartej liczbie.



---

### Testowanie na przykładach

Poniższa tabela pokazuje, jak wyrażenie zachowuje się dla różnych ciągów znaków:

| Testowany ciąg | Wynik | Wyjaśnienie |
| --- | --- | --- |
| `192.168.1.1` | **Poprawny** (`true`) | Standardowy, poprawny adres sieciowy. Każdy oktet mieszcząc się w zakresie 0-255. |
| `0.0.0.0` | **Poprawny** (`true`) | Minimalny poprawny adres IPv4 (skrajny przypadek). |
| `255.255.255.255` | **Poprawny** (`true`) | Maksymalny poprawny adres IPv4 (adres rozgłoszeniowy). |
| `10.0.254.1` | **Poprawny** (`true`) | Prawidłowy adres z różnymi zakresami cyfr w oknach. |
| `256.100.50.25` | **Niepoprawny** (`false`) | Pierwszy oktet (`256`) wykracza poza dozwolony zakres (maksymalnie 255). |
| `192.168.1.300` | **Niepoprawny** (`false`) | Czwarty oktet (`300`) jest za duży. |
| `192.168.1` | **Niepoprawny** (`false`) | Brakuje czwartego oktetu (wymagane są dokładnie 3 kropki i 4 liczby). |
| `192.168.1.1.1` | **Niepoprawny** (`false`) | Za dużo oktetów (podano 5 segmentów zamiast 4). |
| `abc.def.ghi.jkl` | **Niepoprawny** (`false`) | Zamiast cyfr podano litery. |
