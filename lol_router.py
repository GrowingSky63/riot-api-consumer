from fastapi import APIRouter
from riot_api_consumer import (
  get_PUUID,
  get_entries,
  select_entry,
  list_queue_types,
  RANK_TRANSLATION
)


lol_router = APIRouter(
  prefix='/lol'
)
"""
[
    {
        "queueType": "RANKED_SOLO_5x5",
        "tier": "GOLD",
        "rank": "IV",
        "puuid": "0KjC1H7Rdxwa_M7NRJkOsDi1EkA_OohCL-SGTGsxU0DWC0j9Irja7rQpd5JDpyHNkl07JwfbuniRew",
        "leaguePoints": 72,
        "wins": 37,
        "losses": 48,
        "veteran": false,
        "inactive": false,
        "freshBlood": false,
        "hotStreak": false
    },
    {
        "queueType": "RANKED_FLEX_SR",
        "tier": "GOLD",
        "rank": "IV",
        "puuid": "0KjC1H7Rdxwa_M7NRJkOsDi1EkA_OohCL-SGTGsxU0DWC0j9Irja7rQpd5JDpyHNkl07JwfbuniRew",
        "leaguePoints": 50,
        "wins": 10,
        "losses": 13,
        "veteran": false,
        "inactive": false,
        "freshBlood": false,
        "hotStreak": false
    }
]
"""
@lol_router.get('/elo')
def get_elo(
  username: str,
  tag_line: str | None = None,
  queue_type: str = 'RANKED_SOLO_5x5'
) -> str:
  entries = get_entries(get_PUUID(username, tag_line))

  available_queue_types = list_queue_types(entries)

  if queue_type not in available_queue_types:
    raise ValueError(f'Fila não encontrada. Fila solicitada: {queue_type}. Filas disponíveis: {available_queue_types}')

  queue_entry = select_entry(entries, 'RANKED_SOLO_5x5')

  if not 'rank' in queue_entry or not 'tier' in queue_entry:
    queue_entry['rank'] = 'Unranked'
    queue_entry['tier'] = ''

  return f"{RANK_TRANSLATION[queue_entry['tier']]} {queue_entry['rank']}"