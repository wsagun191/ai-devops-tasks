import requests
from requests.auth import HTTPBasicAuth

class JenkinsClient:
    def __init__(self, base_url, username, api_token):
        """
        Inicjalizacja klienta API Jenkinsa.
        :param base_url: Adres URL serwera Jenkins (np. http://localhost:8080)
        :param username: Nazwa użytkownika Jenkins
        :param api_token: Token API użytkownika (rekomendowany zamiast hasła)
        """
        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, api_token)
        self.session = requests.Session()
        self.session.auth = self.auth

    def _get_crumb(self):
        """
        Pobiera token CSRF (crumb) wymagany przez Jenkinsa do zapytań typu POST/PUT/DELETE.
        Zwraca słownik z nagłówkiem zabezpieczającym lub pusty słownik, jeśli CSRF jest wyłączone.
        """
        try:
            response = self.session.get(f"{self.base_url}/crumbIssuer/api/json")
            if response.status_code == 200:
                data = response.json()
                return {data['crumbRequestField']: data['crumb']}
        except requests.exceptions.RequestException:
            # Jeśli endpoint crumb nie istnieje lub wystąpił błąd, kontynuujemy bez niego
            pass
        return {}

    def list_jobs(self):
        """
        Pobiera listę wszystkich zadań (jobs) w Jenkinsie.
        Wykorzystuje parametr tree, aby ograniczyć pobierane dane do najważniejszych pól.
        """
        try:
            url = f"{self.base_url}/api/json?tree=jobs[name,url,color]"
            response = self.session.get(url)
            response.raise_for_status()
            
            jobs = response.json().get('jobs', [])
            return jobs
        except requests.exceptions.HTTPError as e:
            print(f"[Błąd HTTP] Nie udało się pobrać listy zadań: {e.response.status_code} - {e.response.reason}")
        except requests.exceptions.RequestException as e:
            print(f"[Błąd Sieci] Problem z połączeniem z Jenkinsem: {e}")
        return []

    def get_job_build_status(self, job_name):
        """
        Sprawdza status ostatnich buildów dla wskazanego zadania.
        """
        try:
            # Pobieramy informacje o ostatnim buildzie, ostatnim udanym i ostatnim nieudanym
            url = f"{self.base_url}/job/{job_name}/api/json?tree=lastBuild[number,result,timestamp,duration],lastSuccessfulBuild[number],lastFailedBuild[number]"
            response = self.session.get(url)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"[Błąd 404] Zadanie '{job_name}' nie zostało znalezione.")
            else:
                print(f"[Błąd HTTP] Nie udało się pobrać statusu zadania: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[Błąd Sieci]: {e}")
        return None

    def trigger_job(self, job_name):
        """
        Uruchamia wybrane zadanie w Jenkinsie (wysyła żądanie POST).
        """
        try:
            url = f"{self.base_url}/job/{job_name}/build"
            headers = self._get_crumb()  # Pobranie zabezpieczenia CSRF
            
            response = self.session.post(url, headers=headers)
            response.raise_for_status()
            
            # Jenkins zazwyczaj zwraca kod 201 Created lub 200 OK przy pomyślnym uruchomieniu
            if response.status_code in [200, 201]:
                print(f"[Sukces] Zadanie '{job_name}' zostało pomyślnie zlecone do wykonania!")
                return True
        except requests.exceptions.HTTPError as e:
            print(f"[Błąd HTTP] Nie udało się uruchomić zadania '{job_name}': {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            print(f"[Błąd Sieci] Nie udało się wysłać żądania uruchomienia: {e}")
        return False

# ==========================================
# PRZYKŁAD UŻYCIA SKRYPTU
# ==========================================
if __name__ == "__main__":
    # Konfiguracja połączenia (dostosuj do swojego środowiska)
    JENKINS_URL = "http://localhost:8080"
    USERNAME = "admin"
    API_TOKEN = "twoj_token_api_wygenerowany_w_jenkinsie"

    # Inicjalizacja klienta
    jenkins = JenkinsClient(JENKINS_URL, USERNAME, API_TOKEN)

    # 1. Listowanie zadań
    print("--- 1. Pobieranie listy zadań ---")
    jobs = jenkins.list_jobs()
    
    if jobs:
        for job in jobs:
            print(f"• Zadanie: {job['name']} | Status koloru (np. blue=sukces): {job['color']}")
        
        # Wybieramy pierwsze zadanie z listy do dalszych testów
        selected_job = jobs[0]['name']

        # 2. Sprawdzanie statusu ostatnich buildów
        print(f"\n--- 2. Status buildów dla zadania: '{selected_job}' ---")
        status_data = jenkins.get_job_build_status(selected_job)
        
        if status_data:
            last_build = status_data.get('lastBuild')
            if last_build:
                print(f"  - Ostatni numer buildu: #{last_build.get('number')}")
                print(f"  - Wynik ostatniego buildu: {last_build.get('result') or 'W toku (w ejecución)'}")
            else:
                print("  - Zadanie nie ma jeszcze żadnych historii buildów.")
            
            print(f"  - Ostatni udany build: #{status_data.get('lastSuccessfulBuild', {}).get('number', 'Brak')}")
            print(f"  - Ostatni nieudany build: #{status_data.get('lastFailedBuild', {}).get('number', 'Brak')}")

        # 3. Uruchamianie wybranego zadania (odkomentuj poniższe linie, aby przetestować trigger)
        # print(f"\n--- 3. Uruchamianie zadania: '{selected_job}' ---")
        # jenkins.trigger_job(selected_job)
    else:
        print("Brak zadań do wyświetlenia lub wystąpił problem z połączeniem.")
