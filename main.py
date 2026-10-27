import json
import time
import requests

BASE_URL = "https://api.hevyapp.com/user_workouts_paged"
USERNAME = "<your-user-here>"
AUTH_TOKEN = "Bearer <your-token-here>"
PAGE_SIZE = 5  # Valor seguro aceite pela web app (podes testar 3 se persistir)
OUTPUT_FILE = "workouts_backup.json"

BASE_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "pt-PT,pt;q=0.9,en;q=0.8",
    "authorization": AUTH_TOKEN,
    "dnt": "1",
    "hevy-platform": "web",
    "origin": "https://hevy.com",
    "priority": "u=1, i",
    "referer": "https://hevy.com/",
    "sec-ch-ua": '"Chromium";v="148", "Microsoft Edge";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",
    "x-api-key": "shelobs_hevy_web",
}

def fetch_all_workouts():
    offset = 0
    all_workouts = []

    print(f"A iniciar extração de treinos para o utilizador: {USERNAME}")

    session = requests.Session()
    session.headers.update(BASE_HEADERS)

    while True:
        params = {
            "username": USERNAME,
            "limit": PAGE_SIZE,
            "offset": offset,
        }

        # Atualiza o timestamp Unix com milissegundos a cada chamada
        session.headers["x-client-time"] = f"{time.time():.3f}"

        response = session.get(BASE_URL, params=params, timeout=15)

        if response.status_code != 200:
            print(f"[ERRO] Status {response.status_code} no offset {offset}:")
            print(f"Detalhe: {response.text}")
            break

        data = response.json()
        workouts = data.get("workouts", [])

        if not workouts:
            print("Nenhum treino adicional encontrado. Fim da paginação.")
            break

        all_workouts.extend(workouts)
        print(f"Offset {offset:3d}: recolhidos {len(workouts)} treinos (Total acumulado: {len(all_workouts)})")

        offset += len(workouts)
        time.sleep(0.5)

    if all_workouts:
        result_payload = {"workouts": all_workouts}
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(result_payload, file, ensure_ascii=False, indent=2)
        print(f"\nConcluído com sucesso! {len(all_workouts)} treinos guardados em '{OUTPUT_FILE}'.")
    else:
        print("\nNenhum dado foi guardado.")

if __name__ == "__main__":
    fetch_all_workouts()