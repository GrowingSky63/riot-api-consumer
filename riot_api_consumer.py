import requests, dotenv, json, fastapi

HEADERS = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
  "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,nl;q=0.6",
  "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
  "Origin": "https://developer.riotgames.com",
  "X-Riot-Token": dotenv.get_key('.env', 'RIOT_KEY')
}

ACCOUTS_V1_URL = 'https://americas.api.riotgames.com/riot/account/v1/'
LEAGUE_V4_URL = 'https://br1.api.riotgames.com/lol/league/v4/'

RANK_TRANSLATION = {
  'IRON': 'Ferro',
  'BRONZE': 'Bronze',
  'SILVER': 'Prata',
  'GOLD': 'Ouro',
  'PLATINUM': 'Platina',
  'EMERALD': 'Esmeralda',
  'DIAMOND': 'Diamante',
  'MASTER': 'Mestre'
}

def get_PUUID(username: str, tag_line: str | None = None) -> str:
  if tag_line is not None:
    game_name = username

  elif tag_line is None:
    if '#' not in username:
      raise ValueError('tag_line precisa estar no username, ou ser passada separadamente como tag_line')
    game_name, tag_line = username.split('#')
  
  url = f'{ACCOUTS_V1_URL}accounts/by-riot-id/{game_name}/{tag_line}'

  response = requests.get(url, headers=HEADERS)

  try:
    response_dict = json.loads(response.content)
  except:
    raise ValueError(f'PUUID não encontrado. [{response.status_code}] {response.content}')

  if not 'puuid' in response_dict:
    raise ValueError(f'PUUID não encontrado. [{response.status_code}] {response.content}')
  
  return response_dict['puuid']

def get_entries(PUUID: str) -> list[dict]:
  url = f'{LEAGUE_V4_URL}entries/by-puuid/{PUUID}'

  response = requests.get(url, headers=HEADERS)
  
  try:
    response_dict = json.loads(response.content)
  except:
    raise ValueError(f'PUUID não encontrado. [{response.status_code}] {response.content}')
  
  return response_dict

def list_queue_types(entries: list[dict]) -> list:
  return [entry['queueType'] for entry in entries if 'queueType' in entry]

def select_entry(entries: list[dict], queue_type: str) -> dict:
  for entry in entries:
    if entry['queueType'] == queue_type:
      return entry
  return {}