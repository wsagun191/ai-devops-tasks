wyjaśnienie kodu z pliku check_docker.sh

Jasne! Rozbierzmy ten skrypt na części pierwsze. Wyjaśnię Ci każdą linię tak, abyś dokładnie zrozumiał, co robi i dlaczego tak została napisana.

---

### Krok po kroku:

```bash
#!/bin/bash

```

* **Co to znaczy:** To tzw. *shebang*. Mówi systemowi operacyjnemu (Linux/macOS), za pomocą jakiego interpreter ten plik ma zostać uruchomiony – w tym przypadku jest to powłoka **bash**.

---

```bash
# Nazwa usługi
SERVICE="docker"

```

* **Co to znaczy:**
* Linie zaczynające się od `#` to **komentarze** – komputer je ignoruje, służą one tylko do wyjaśnienia kodu dla Ciebie.
* `SERVICE="docker"` tworzy zmienną o nazwie `SERVICE` i przypisuje jej wartość `"docker"`. Dzięki temu w dalszej części skryptu zamiast pisać słowo "docker", możemy odwołać się do tej zmiennej.



---

```bash
echo "Sprawdzanie statusu usługi $SERVICE..."

```

* **Co to znaczy:** Polecenie `echo` wypisuje tekst na ekranie terminala. Zauważ, że zamiast napisać dosłownie "docker", używamy `$SERVICE`. Komputer automatycznie podstawi w tym miejscu wartość zmiennej (czyli słowo `docker`). Na ekranie zobaczysz więc: *Sprawdzanie statusu usługi docker...*

---

```bash
if systemctl is-active --quiet "$SERVICE"; then

```

* **Co to znaczy:** To początek instrukcji warunkowej **if** (jeśli). Sprawdzamy stan usługi za pomocą menedżera systemowego `systemctl`:
* `is-active` – sprawdza, czy usługa aktualnie działa.
* `--quiet` – sprawia, że `systemctl` nie wypisuje żadnych dodatkowych komunikatów na ekranie, tylko zwraca tzw. kod wyjścia (status sukcesu lub błędu).
* `"$SERVICE"` – sprawdza usługę zapisaną w zmiennej (czyli `docker`).
* `; then` – oznacza: „jeśli powyższe sprawdzenie zwróci sukces (usługa działa), wykonaj to, co jest poniżej”.



---

```bash
    echo "Usługa $SERVICE działa poprawnie."

```

* **Co to znaczy:** Jeśli warunek w `if` okazał się prawdziwy (Docker działa), skrypt wypisze na ekranie komunikat o tym, że usługa działa poprawnie. *(Wcięcie na początku to tylko dobra praktyka robienia porządku w kodzie).*

---

```bash
else

```

* **Co to znaczy:** Słowo kluczowe `else` oznacza: **„w przeciwnym razie”** (czyli jeśli usługa **nie** działa i pierwsze sprawdzenie zwróciło błąd).

---

```bash
    echo "Usługa $SERVICE nie działa. Próba uruchomienia..."

```

* **Co to znaczy:** Skrypt informuje użytkownika na ekranie, że Docker jest wyłączony i próbuje go uruchomić.

---

```bash
    sudo systemctl start "$SERVICE"

```

* **Co to znaczy:** Tutaj następuje właściwa próba naprawy:
* `sudo` – wykonuje polecenie z uprawnieniami administratora (root), ponieważ uruchamianie usług systemowych wymaga wyższych uprawnień.
* `systemctl start` – polecenie włączające wskazaną usługę.
* `"$SERVICE"` – wskazuje, którą usługę chcemy uruchomić (w tym przypadku `docker`).



---

```bash
    if systemctl is-active --quiet "$SERVICE"; then

```

* **Co to znaczy:** Mamy tu zagnieżdżony kolejny `if` (instrukcję w instrukcji). Skrypt chce sprawdzić, czy **próba uruchomienia się powiodła**. Ponownie pytamy system: „Czy Docker teraz działa?”.

---

```bash
        echo "Usługa $SERVICE została pomyślnie uruchomiona."

```

* **Co to znaczy:** Jeśli drugie sprawdzenie potwierdziło, że Docker w końcu działa, skrypt wypisuje radosny komunikat o sukcesie.

---

```bash
    else

```

* **Co to znaczy:** Jeśli jednak próba uruchomienia zawiodła i usługa nadal nie działa...

---

```bash
        echo "BŁĄD: Nie udało się uruchomić usługi $SERVICE." >&2
        exit 1
    fi

```

* **Co to znaczy:**
* `echo ... >&2` – wypisuje komunikat o błędzie, ale kieruje go do specjalnego strumienia błędów (`stderr`), a nie standardowego wyjścia. To dobra praktyka przy pisaniu skryptów systemowych.
* `exit 1` – przerywa działanie całego skryptu i zwraca kod `1` (co w świecie Linuksa oznacza, że wystąpił błąd).
* `fi` – zamyka wewnętrzną instrukcję warunkową `if`.



---

```bash
fi

```

* **Co to znaczy:** Zamyka główną (pierwszą) instrukcję warunkową `if`.
