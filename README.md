W celu uruchomienia programu należy:

1. Utworzyc venv'a python3 -m venv venv
2. Zainstalowac zaleznosci pip install -r requirements.txt
3. Uruchomienie postgresa cd src && docker compose up -d
4. Ustawienie odpowiednich zmiennych srodowiskowych (domyslnie skonfigurowane modele to gemini i openai (oba uzywane na raz!))
  Zmienne wymagane do uruchomienia bez jakichkolwiek zmian:

export GEMINI_API_KEY=xxx
export OPENAI_API_KEY=xxx 
export EMAIL=xxx@gmail.com
export PASSWORD="xxx" --- klucz do api gmail'a 
export POSTGRES_DB=xxx
export POSTGRES_USER=xxx
export POSTGRES_PASSWORD=xxx
export POSTGRES_HOST=xxx
export POSTGRES_PORT=xxx

5. Upewnienie sie ze na koncie gmail jest wlaczona obsluga IPAM oraz SMTP
6. uruchomienie funkcji main -- python3 src/nai/main.py
