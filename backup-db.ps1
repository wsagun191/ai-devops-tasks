# Prosty skrypt do backupu bazy danych

$DB_NAME = "app_database"
$BACKUP_DIR = "C:\var\backups\db"
$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
$FILENAME = "$BACKUP_DIR\${DB_NAME}_${DATE}.sql"
$ZIP_FILENAME = "$FILENAME.zip"

# Sprawdź czy katalog istnieje
if (-not (Test-Path -Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Force -Path $BACKUP_DIR | Out-Null
    Write-Host "Utworzono katalog $BACKUP_DIR"
}

# Wykonaj backup
Write-Host "Rozpoczynam backup bazy $DB_NAME..."

# W PowerShell przekierowanie potoku (pipe) dla zewnętrznych narzędzi takich jak mysqldump 
# bywa specyficzne, dlatego najbezpieczniej zapisać plik SQL, a następnie go spakować:
mysqldump -u root -p "$DB_NAME" --result-file="$FILENAME"

if ($LASTEXITCODE -eq 0) {
    # Kompresja pliku do formatu zip (alternatywa dla gzip w Windows)
    Compress-Archive -Path "$FILENAME" -DestinationPath "$ZIP_FILENAME" -Force
    Remove-Item "$FILENAME" # Usunięcie nieskompresowanego pliku SQL
    
    Write-Host "Backup zakończony sukcesem: $ZIP_FILENAME"
} else {
    Write-Host "Błąd podczas wykonywania backupu!" -ForegroundColor Red
    exit 1
}
