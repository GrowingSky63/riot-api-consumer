from fastapi import APIRouter
from riot_api_consumer import get_PUUID, get_entries, select_entry, RANK_TRANSLATION


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
def get_elo(username: str) -> dict:
  entries = get_entries(get_PUUID(username))
  
  soloq_entry = select_entry(entries, 'RANKED_SOLO_5x5')
  flex_entry = select_entry(entries, 'RANKED_FLEX_SR')

  return {
    'Solo/Duo': f"{RANK_TRANSLATION[soloq_entry['tier']]} {soloq_entry['rank']}",
    'Flex': f"{RANK_TRANSLATION[flex_entry['tier']]} {flex_entry['rank']}"
    }