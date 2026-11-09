Oryginalna wersja:
```python
def find_duplicates(list_of_items):
    duplicates = []
    for i in range(len(list_of_items)):
        for j in range(i+1, len(list_of_items)):
            if list_of_items[i] == list_of_items[j] and list_of_items[i] not in duplicates:
                duplicates.append(list_of_items[i])
    return duplicates
```
Ulepszona przez gemini:
**Tak, ten kod można bardzo mocno zoptymalizować.**

Obecna wersja ma złożoność obliczeniową **$O(n^2)$** ze względu na zagnieżdżone pętle oraz dodatkowe sprawdzanie `in duplicates`, co przy dużych listach powoduje gwałtowny spadek wydajności.

Możemy skrócić czas działania do **$O(n)$**, wykorzystując **zbiory (`set`)**, które oferują wyszukiwanie elementów w czasie $O(1)$.

### Optymalne rozwiązanie z użyciem zbiorów (`set`)

Oto najwydajniejsze i bardzo czytelne podejście:

```python
def find_duplicates(list_of_items):
  seen = set()
  duplicates = set()

  for item in list_of_items:
    if item in seen:
      duplicates.add(item)
    else:
      seen.add(item)

  return list(duplicates)

```

### Alternatywne rozwiązanie (Pythoniczne z `Counter`)

Jeśli zależy Ci na jak najkrótszym kodzie, możesz użyć klasy `Counter` z wbudowanego modułu `collections`:

```python
from collections import Counter


def find_duplicates(list_of_items):
  counts = Counter(list_of_items)
  return [item for item, count in counts.items() if count > 1]

```

### Dlaczego te wersje są lepsze?

1. **Złożoność czasowa ($O(n)$):** Zamiast porównywać każdy element z każdym ($O(n^2)$), przechodzimy przez listę tylko **raz** ($O(n)$). Operacje na zbiorach i słownikach w Pythonie są uśredniając błyskawiczne.
2. **Brak zbędnych powtórzeń:** Użycie zbioru `duplicates` (lub komprehension z `Counter`) gwarantuje, że dany duplikat pojawi się na liście wynikowej dokładnie raz, bez potrzeby kosztownego sprawdzania `item not in duplicates`.
