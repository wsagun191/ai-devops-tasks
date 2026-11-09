Oto profesjonalna dokumentacja dla podanego endpointu API w formacie Markdown oraz refleksja na temat jej jakości.

---

## Dokumentacja API

### `GET /api/users`

Pobiera paginowaną listę użytkowników zarejestrowanych w systemie. Endpoint pozwala na filtrowanie wyników według roli użytkownika.

#### Parametry zapytania (Query Parameters)

| Nazwa | Typ | Wymagany | Domyślna wartość | Opis |
| --- | --- | --- | --- | --- |
| `page` | Integer | Nie | `1` | Numer strony wyników do pobrania. |
| `limit` | Integer | Nie | `10` | Liczba wyników na stronę (maksymalnie `100`). |
| `role` | String | Nie | *brak* | Opcjonalny filtr pozwalający zwrócić użytkowników o określonej roli (np. `admin`, `user`). |

---

#### Przykładowe żądanie

Pobranie drugiej strony użytkowników z limitem 5 elementów na stronę, posiadających rolę `user`:

```http
GET /api/users?page=2&limit=5&role=user HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
Accept: application/json

```

---

#### Przykładowa odpowiedź

**Kod statusu:** `200 OK`

```json
{
  "success": true,
  "data": [
    {
      "id": 6,
      "name": "Anna Nowak",
      "email": "anna.nowak@example.com",
      "role": "user",
      "createdAt": "2026-03-10T14:22:00Z"
    },
    {
      "id": 7,
      "name": "Piotr Zieliński",
      "email": "piotr.zielinski@example.com",
      "role": "user",
      "createdAt": "2026-03-11T09:15:00Z"
    }
  ],
  "pagination": {
    "currentPage": 2,
    "totalPages": 5,
    "totalItems": 24,
    "limit": 5
  }
}

```
