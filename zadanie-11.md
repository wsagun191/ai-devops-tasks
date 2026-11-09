Oto kompleksowy przewodnik, jak napisać test jednostkowy dla podanej funkcji za pomocą **Jesta**.

---

### ## 1. Czym jest Jest?

**Jest** to popularny, wszechstronny framework do testowania kodu w języku JavaScript, stworzony i rozwijany przez firmę Meta (Facebook). Jest ceniony za to, że działa „od razu po wyjęciu z pudełka” (zero-config dla wielu projektów), oferuje szybkie testowanie (dzięki równoległemu uruchamianiu), wbudowany mechanizm sprawdzania pokrycia kodu (*code coverage*) oraz łatwe w użyciu funkcje do mockowania (symulowania) obiektów i funkcji.

---

### ## 2. Struktura plików projektu

Aby projekt poprawnie współpracował z Jestem, jego struktura powinna wyglądać następująco:

```text
mój-projekt/
├── node_modules/       # Katalog z zainstalowanymi pakietami npm
├── package.json        # Konfiguracja projektu i zależności
├── package-lock.json   # Dokładne wersje zainstalowanych pakietów
├── sum.js              # Plik z testowaną funkcją
└── sum.test.js         # Plik z testami jednostkowymi

```

---

### ## 3. Instalacja Jesta w projekcie

1. **Inicjalizacja projektu Node.js:** Krok 1.
Jeśli jeszcze tego nie zrobiłeś, otwórz terminal w folderze projektu i zainicjuj nowy projekt Node.js:

```bash
npm init -y

```


2. **Instalacja Jesta:** Krok 2.
Zainstaluj Jesta jako zależność deweloperską (`--save-dev`), ponieważ jest on potrzebny głównie w procesie pisania i uruchamiania testów, a nie na produkcji:

```bash
npm install --save-dev jest

```


3. **Konfiguracja skryptu testowego:** Krok 3.
Otwórz plik `package.json` i w sekcji `"scripts"` zmień linię `"test"` na wywołanie Jesta:

```json
"scripts": {
  "test": "jest"
}

```


---

### ## 4. Kod funkcji i testu

#### Plik z funkcją: `sum.js`

Musimy wyeksportować funkcję, aby test mógł ją zaimportować (w środowisku CommonJS używamy `module.exports`):

```javascript
function sum(a, b) {
  return a + b;
}

module.exports = sum;

```

#### Plik z testem: `sum.test.js`

Standardowo pliki testowe dla Jesta nazywają się tak samo jak pliki źródłowe, ale z rozszerzeniem `.test.js` (lub `.spec.js`).

```javascript
const sum = require('./sum');

test('poprawnie dodaje dwie liczby (1 + 2 = 3)', () => {
  expect(sum(1, 2)).toBe(3);
});

test('poprawnie obsługuje liczby ujemne (-1 + -2 = -3)', () => {
  expect(sum(-1, -2)).toBe(-3);
});

```

---

### ## 5. Jak uruchomić test?

Aby uruchomić przygotowany test, wpisz w terminalu polecenie:

```bash
npm test

```

Lub bezpośrednio za pomocą narzędzia npx:

```bash
npx jest

```

Po uruchomieniu zobaczysz w terminalu zielony komunikat oznaczający, że wszystkie testy przeszły pomyślnie!
