#!/bin/bash

# Nazwa usługi
SERVICE="docker"

echo "Sprawdzanie statusu usługi $SERVICE..."

# Sprawdzamy, czy usługa jest aktywna
if systemctl is-active --quiet "$SERVICE"; then
    echo "Usługa $SERVICE działa poprawnie."
else
    echo "Usługa $SERVICE nie działa. Próba uruchomienia..."
    
    # Próba uruchomienia usługi (wymaga uprawnień roota)
    sudo systemctl start "$SERVICE"
    
    # Weryfikacja po próbie uruchomienia
    if systemctl is-active --quiet "$SERVICE"; then
        echo "Usługa $SERVICE została pomyślnie uruchomiona."
    else
        echo "BŁĄD: Nie udało się uruchomić usługi $SERVICE." >&2
        exit 1
    fi
fi
