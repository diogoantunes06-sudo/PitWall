"""
PitWall — Script de atualização automática de dados
Roda via GitHub Actions semanalmente.
Atualiza: F1 (via Ergast/OpenF1), Fórmula E (via FIA API pública)
F2, F3, F4 Brasil: atualizados manualmente via JSON
"""

import json
import urllib.request
import urllib.error
from datetime import date, datetime
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PitWall/1.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"Erro ao buscar {url}: {e}")
        return None

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {filename}")

def update_f1():
    print("Atualizando F1...")
    today = date.today().isoformat()

    # Classificação de pilotos via Ergast
    drivers_url = "https://ergast.com/api/f1/current/driverStandings.json"
    drivers_data = fetch_json(drivers_url)

    # Classificação de construtores via Ergast
    ctors_url = "https://ergast.com/api/f1/current/constructorStandings.json"
    ctors_data = fetch_json(ctors_url)

    # Calendário via Ergast
    cal_url = "https://ergast.com/api/f1/current.json"
    cal_data = fetch_json(cal_url)

    # Carrega JSON atual como fallback
    current_path = os.path.join(DATA_DIR, 'f1.json')
    with open(current_path, encoding='utf-8') as f:
        current = json.load(f)

    if drivers_data:
        try:
            standings = drivers_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            current['drivers'] = [
                {
                    "pos": int(s['position']),
                    "name": f"{s['Driver']['givenName']} {s['Driver']['familyName']}",
                    "team": s['Constructors'][0]['name'] if s['Constructors'] else "—",
                    "points": float(s['points']),
                    "nationality": s['Driver']['nationality']
                }
                for s in standings
            ]
            print(f"  Pilotos F1: {len(current['drivers'])} registros")
        except (KeyError, IndexError) as e:
            print(f"  Erro parsing pilotos F1: {e}")

    if ctors_data:
        try:
            standings = ctors_data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
            current['constructors'] = [
                {
                    "pos": int(s['position']),
                    "team": s['Constructor']['name'],
                    "points": float(s['points'])
                }
                for s in standings
            ]
            print(f"  Construtores F1: {len(current['constructors'])} registros")
        except (KeyError, IndexError) as e:
            print(f"  Erro parsing construtores F1: {e}")

    if cal_data:
        try:
            races = cal_data['MRData']['RaceTable']['Races']
            today_dt = date.today()
            current['calendar'] = [
                {
                    "round": int(r['round']),
                    "name": r['raceName'],
                    "circuit": r['Circuit']['circuitName'],
                    "date": r['date'],
                    "status": "done" if date.fromisoformat(r['date']) < today_dt else "upcoming"
                }
                for r in races
            ]
            print(f"  Calendário F1: {len(current['calendar'])} etapas")
        except (KeyError, IndexError) as e:
            print(f"  Erro parsing calendário F1: {e}")

    current['last_updated'] = today
    save_json('f1.json', current)

def update_fe():
    """
    Fórmula E não tem API pública estável.
    Por ora mantém os dados do JSON e só atualiza a data.
    Futuramente: scraping do site oficial ou parceria com API paga.
    """
    print("Fórmula E: sem API pública disponível — mantendo dados manuais.")
    current_path = os.path.join(DATA_DIR, 'fe.json')
    with open(current_path, encoding='utf-8') as f:
        current = json.load(f)
    current['last_updated'] = date.today().isoformat()
    save_json('fe.json', current)

def check_manual_files():
    """Verifica se os JSONs manuais existem e estão válidos."""
    for fname in ['f2.json', 'f3.json', 'f4brasil.json']:
        path = os.path.join(DATA_DIR, fname)
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
            print(f"{fname}: OK — última atualização: {data.get('last_updated','?')}")
        else:
            print(f"AVISO: {fname} não encontrado!")

if __name__ == '__main__':
    print(f"=== PitWall Update — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    update_f1()
    update_fe()
    check_manual_files()
    print("=== Concluído ===")
