Konwersja danych z formatu **JSON** (który ma strukturę hierarchiczną, drzewiastą) do formatu **CSV** (który jest płaski i tabelaryczny) wymaga tzw. *spłaszczenia danych*.

Poniżej znajdziesz opis samego procesu oraz szczegółową analizę wyzwań, które się z nim wiążą (ze szczególnym uwzględnieniem reprezentacji tablic).

---

## 1. Proces konwersji krok po kroku

1. **Wczytanie i sparsowanie JSON-a:**
Program odczytuje ciąg tekstowy JSON i przekształca go w obiekt lub tablicę struktur zrozumiałą dla języka programowania (np. tablicę słowników/obiektów w Pythonie lub JS).
2. **Wyznaczenie nagłówków (Columns/Headers):**
Przegląda się klucze obiektów w tablici, aby ustalić nazwy kolumn przyszłego pliku CSV. W prostych przypadkach są to klucze poziomu głównego (`id`, `name`, `email`, `roles`).
3. **Przekształcenie pól złożonych (Serialization):**
Pola typu tablica (`roles`) lub zagnieżdżone obiekty są konwertowane na ciągi znaków (stringi), ponieważ CSV obsługuje w komórkach wyłącznie teksty lub liczby.
4. **Zapis do formatu tekstowego CSV:**
Wartości są rozdzielane separatorem (najczęściej przecinkiem `,` lub średnikiem `;`), a wiersze są oddzielane znakami nowej linii.

---

## 2. Potencjalne wyzwania i ich rozwiązania

### Wyzwanie 1: Reprezentacja tablicy w pojedynczej komórce (np. `roles`)

To jedno z głównych wyzwań. CSV to płaska tabela, w której komórka to zazwyczaj jedna wartość. Tablica `["admin", "user"]` nie ma bezpośredniego odpowiednika w tabeli.

* **Rozwiązanie A (Serializowanie do stringa z separatorem – najczęstsze):**
Elementy tablicy łączy się wybranym separatorem (np. przecinkiem lub spacji), a całą wartość zamyka się w cudzysłowach, aby parser CSV nie pomylił separatora elementów z separatorem kolumn.
* *Przyklad:* `"admin,user"`


* **Rozwiązanie B (JSON Stringification):**
Zapisanie całej tablicy jako zserializowanego JSON-a wewnątrz jednej komórki.
* *Przykład:* `"[\"admin\", \"user\"]"`


* **Rozwiązanie C (Normalizacja / Rozbicie na wiele wierszy lub kolumn):**
* Jeśli użytkownik ma wiele ról, można zduplikować wiersz użytkownika dla każdej roli (normalizacja relacyjna).
* Alternatywnie można utworzyć osobne kolumny: `role_1`, `role_2`, co jest jednak mało skalowalne przy dynamicznej liczbie elementów.



### Wyzwanie 2: Znak separatora i znaki specjalne (Escaping)

Wartości tekstowe w JSON-ie mogą zawierać przecinki, cudzysłowy lub znaki nowej linii (np. w adresach lub opisach). Jeśli w polu `name` znajdzie się przecinek (np. `Kowalski, Jan`), rozbije to kolumny w pliku CSV.

* **Rozwiązanie:**
Każde pole tekstowe zawierające separator, cudzysłów lub znak nowej linii **musi być ujęte w cudzysłowy (`"..."`)**. Jeśli wewnątrz tekstu znajduje się cudzysłów, należy go zdublować (np. `""`).

### Wyzwanie 3: Brakujące pola (Niejednorodny schemat)

W JSON-ie obiekty w tablicy mogą mieć różny zestaw pól (np. pierwszy użytkownik ma pole `phone`, a drugi nie).

* **Rozwiązanie:**
Przed konwersją należy przeskanować wszystkie obiekty, zebrać unikalny zestaw wszystkich występujących kluczy, a dla obiektów, które ich nie posiadają, wstawić puste wartości (`null` lub pusty string `""`).

### Wyzwanie 4: Kodowanie znaków (Encoding)

CSV otwierany np. w programie Microsoft Excel może niepoprawnie interpretować polskie znaki (ogonki), jeśli plik nie zostanie zapisany w odpowiednim kodowaniu.

* **Rozwiązanie:**
Zawsze należy zapisywać pliki CSV w kodowaniu **UTF-8 (najlepiej z tzw. BOM – Byte Order Mark)**, zwłaszcza jeśli plik ma być otwierany bezpośrednio w programach biurowych systemu Windows.
