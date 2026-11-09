### 👍 Mocne strony (Zalety)

1. **Przejrzysta struktura:** Podział na logiczne sekcje (Opis, Instalacja, Użycie, Endpointy) sprawia, że dokumentacja jest intuicyjna. Użytkownik od razu wie, gdzie szukać informacji o uruchomieniu, a gdzie o samym API.
2. **Gotowe przykłady konfiguracji:** Umieszczenie wzoru pliku `.env` z domyślnymi wartościami (port, URI bazy danych, klucz JWT) bardzo ułatwia pierwszym krokom z projektem.
3. **Zrozumienie kontekstu autoryzacji:** Informacja o tym, że endpointy wymagają nagłówka `Authorization: Bearer <token>`, zapobiega frustracji deweloperów próbujących odpytań API bez zalogowania.
4. **Estetyczne tablice:** Użycie tabel Markdown dla endpointów jest czytelniejsze i bardziej kompaktowe niż długa lista wypunktowana.

---

### 🔍 Obszary do poprawy (Co można dodać w przyszłości)

1. **Brak przykładów requestów i response'ów dla zadań:** Choć tabela endpointów (`/api/tasks`) mówi, co robi dany adres, brakuje przykładowego ciała żądania (`body` dla `POST / PUT`) oraz struktury zwracanego JSON-a. Deweloper musiałby zgadywać, jakie pola są wymagane (np. czy `title` jest obowiązkowe, jakie wartości może przyjmować `priority`).
2. **Brak wymagań wstępnych (Prerequisites):** W sekcji instalacji warto byłłoby dopisać informację o wymaganych wersjach oprogramowania (np. *Node.js >= 18* oraz *MongoDB w wersji 6+*).
3. **Brak sekcji o testowaniu:** Skoro w projekcie poruszaliśmy kwestię testów jednostkowych (np. w Jesto), dobrym zwyczajem byłoby dodanie w pliku `README.md` wzmianki o poleceniu `npm test` w sekcji Użycie.
4. **Brak opisu obsługi błędów / kodów statusu:** Dokumentacja nie wspomina, jakie kody HTTP są zwracane w sytuacjach awaryjnych (np. `401 Unauthorized` przy braku tokena, `404 Not Found` gdy zadanie o danym ID nie istnieje).
