Przykład użycia

```javascript
// Przykładowa tablica zadań
const myTasks = [
  { id: 3, title: 'Naprawić błąd w formularzu', status: 'pending' },
  { id: 1, title: 'Stworzyć strukturę bazy danych', status: 'completed' },
  { id: 4, title: 'Napisać testy jednostkowe', status: 'completed' },
  { id: 2, title: 'Zaprojektować interfejs użytkownika', status: 'completed' }
];

// Wywołanie funkcji
const result = getCompletedTaskTitles(myTasks);

console.log(result);
// Wynik w konsoli:
// [ 'Stworzyć strukturę bazy danych', 'Zaprojektować interfejs użytkownika', 'Napisać testy jednostkowe' ]

```

---

### Opis działania (krok po kroku)

1. **`filter(task => task.status === 'completed')`**
Metoda przechodzi przez każdy element tablice i zostawia tylko te obiekty, w których pole `status` ma dokładnie wartość `"completed"`. Zadania w statusie np. `"pending"` zostają odrzucone.
2. **`sort((a, b) => a.id - b.id)`**
Przefiltrowane zadania są sortowane według ich unikalnego identyfikatora (`id`). Wyrażenie `a.id - b.id` zapewnia sortowanie **rosnące** (jeśli wynik jest ujemny, `a` będzie przed `b`; jeśli dodatni – odwrotnie).
3. **`map(task => task.title)`**
Na sam koniec metoda `map` przekształca tablicę obiektów w nową tablicę zawierającą wyłącznie wartości pola `title` z każdego przefiltrowanego i posortowanego elementu.

Zastosowanie tzw. **łańcucha metod (method chaining)** sprawia, że kod jest bardzo czytelny, deklaratywny i wydajny.
