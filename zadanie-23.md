Oto szczegółowa analiza złożoności oraz kompleksowy opis optymalizacji dla algorytmu wyszukiwania par liczb, które sumują się do określonej wartości (`targetSum`).

---

## 1. Analiza Algorytmu Wyjściowego (Brute Force)

Pierwotna wersja algorytmu sprawdza każdą możliwą kombinację dwóch elementów w tablicy za pomocą dwóch zagnieżdżonych pętli.

* **Złożoność czasowa: $\mathcal{O}(n^2)$**
Dla tablicy o rozmiarze $n$ liczba iteracji pętli wewnętrznej maleje, ale średnia liczba operacji wynosi $\frac{n(n-1)}{2}$. Oznacza to, że podwojenie rozmiaru tablicy czterokrotnie wydłuża czas wykonania. Przy dużych zbiorach danych (np. $n = 100\,000$) algorytm staje się nieakceptowalnie wolny.
* **Złożoność pamięciowa: $\mathcal{O}(1)$ dodatkowej pamięci** (pomijając tablicę wynikową)
Algorytm nie tworzy dodatkowych struktur danych w trakcie działania, operując bezpośrednio na wskaźnikach tablicy wejściowej.

---

## 2. Opis Ścieżek Optymalizacji

W zależności od tego, czy priorytetem jest **czas wykonania** (minimalizacja liczby operacji), czy **zużycie pamięci**, możemy zastosować jedno z dwóch podejść optymalizacyjnych.

### Strategia A: Podejście z użyciem Hash Set (Optymalizacja Czasowa)

* **Idea:** Zamiast szukać drugiej liczby za pomocą pętli, możemy "zapamiętywać" odwiedzone elementy w strukturze typu `Set` (która oferuje czas wyszukiwania $\mathcal{O}(1)$). Dla każdego elementu obliczamy jego dopełnienie (`complement = targetSum - num`) i sprawdzamy, czy już wcześniej je spotkaliśmy.
* **Złożoność czasowa:** $\mathcal{O}(n)$ – przechodzimy przez tablicę tylko raz, a operacje na zbiorze (wstawianie i sprawdzanie) są średnio w czasie stałym.
* **Złożoność pamięciowa:** $\mathcal{O}(n)$ – konieczność alokacji pamięci na struktury przechowujące odwiedzone elementy oraz unikalne pary wyników.

### Strategia B: Podejście z Dwoma Wskaźnikami (Optymalizacja Pamięciowa)

* **Idea:** Jeśli najpierw posortujemy tablicę, możemy ustawić dwa wskaźniki – jeden na początku (`left = 0`), a drugi na końcu (`right = n - 1`). Sumując elementy pod tymi wskaźnikami, decydujemy, który wskaźnik przesunąć: jeśli suma jest za mała, zwiększamy `left`; jeśli za duża, zmniejszamy `right`.
* **Złożoność czasowa:** $\mathcal{O}(n \log n)$ – dominującym kosztem jest operacja sortowania tablicy.
* **Złożoność pamięciowa:** $\mathcal{O}(1)$ – algorytm nie wymaga dodatkowych struktur danych poza miejscem na sortowanie (w zależności od silnika JS sortowanie w miejscu lub kopia).

---

## 3. Podsumowanie i Porównanie Podejść

| Podejście | Złożoność czasowa | Złożoność pamięciowa | Zalety | Wady |
| --- | --- | --- | --- | --- |
| **Brute Force** | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Prostota implementacji, brak dodatkowej pamięci. | Katastrofalna skalowalność przy dużych zbiorach danych. |
| **Hash Set** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Najwyższa wydajność czasowa (przejście liniowe). | Wyższe zużycie pamięci na dodatkową strukturę. |
| **Dwa Wskaźniki** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(1)$ | Minimalne zużycie pamięci, brak potrzebnych struktur skrótu. | Wymaga modyfikacji / sortowania danych wejściowych. |
