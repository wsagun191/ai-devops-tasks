 Główne różnice między skryptami Bash i PowerShell zaobserwowane w tym przykładzie

1. **Zmienne:**
* **Bash:** Używa symbolu `$` do odczytu zmiennej (np. `$DB_NAME`), a przy przypisaniu podaje się samą nazwę bez `$` (np. `DB_NAME="app_database"`). Do łączenia ze ścieżkami często stosuje się klamry, np. `${BACKUP_DIR}/...`.
* **PowerShell:** Zawsze używa symbolu `$` zarówno przy przypisaniu, jak i odczycie (np. `$DB_NAME = "app_database"`). Nazwy zmiennych mogą też zawierać nawiasy klamrowe przy interpolacji w stringach dwucudzysłowowych (np. `"${DB_NAME}_${DATE}.sql"`).


2. **Podstawianie wyniku poleceń (Command Substitution):**
* **Bash:** Używa konstrukcji z backtickami lub dolarem i nawiasami, np. `DATE=$(date +%Y%m%d_%H%M%S)`.
* **PowerShell:** Wywołuje polecenia cmdlet bezpośrednio lub w nawiasach, np. `Get-Date -Format "yyyyMMdd_HHmmss"`.


3. **Operacje na systemie plików i katalogach:**
* **Bash:** Wykorzystuje tradycyjne narzędzia powłoki i uniksowe flagi, np. `[ ! -d "$DIR" ]` do sprawdzenia istnienia oraz `mkdir -p` do utworzenia.
* **PowerShell:** Koroczysta z dedykowanych poleceń (cmdletów) z obiektowym podejściem, takich jak `Test-Path` (sprawdzanie istnienia) oraz `New-Item -ItemType Directory` (tworzenie katalogu).


4. **Kody wyjścia (Exit codes):**
* **Bash:** Sprawdza status ostatniej operacji za pomocą specjalnej zmiennej `$?` (`if [ $? -eq 0 ]`).
* **PowerShell:** Używa automatycznej zmiennej `$LASTEXITCODE` do sprawdzania kodów powrotu zewnętrznych aplikacji konsolowych (takich jak `mysqldump`).


5. **Kompresja i obsługa potoków (Pipes):**
* **Bash:** Standardowo wspiera strumieniowe potokowanie za pomocą operatora `|` (np. `mysqldump ... | gzip > file`), ponieważ uniksowe narzędzia operują na surowych bajtach/strumieniach tekstowych.
* **PowerShell:** Jest potokiem **obiektowym**, co czasami komplikuje bezpośrednie przekierowanie strumieni binarnych z zewnętrznych programów (`mysqldump`) do narzędzi kompresujących w locie tak gładko jak w Bashu. Dlatego w PowerShell bezpieczniej jest zapisać najpierw plik przez argument `--result-file`, a następnie użyć dedykowanego polecenia kompresującego `Compress-Archive`.
