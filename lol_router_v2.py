from typing import Literal
from fastapi import APIRouter, HTTPException
from riot_api_consumer import (
  get_PUUID,
  get_entries,
  select_entry,
  list_queue_types,
  RANK_TRANSLATION
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


lol_router = APIRouter(
  prefix='/league/v2'
)


def get_queue_info(
  username: str,
  tag_line: str | None = None,
  queue_type: str = 'RANKED_SOLO_5x5',
  lang: Literal['pt-br'] = 'pt-br'
):
  try:
    entries = get_entries(get_PUUID(username, tag_line))
  except ValueError as e:
    raise HTTPException(
      status_code=500,
      detail=f'{e}'
    )

  available_queue_types = list_queue_types(entries)

  if queue_type not in available_queue_types:
    raise HTTPException(
      status_code=400,
      detail=f'Fila não encontrada. Fila solicitada: {queue_type}. Filas disponíveis: {available_queue_types}'
    )
  
  queue_info = select_entry(entries, queue_type)
  
  if 'tier' not in queue_info or queue_info['tier'] == '':
    queue_info['tier'] = 'UNRANCKED'

  if lang not in RANK_TRANSLATION:
    lang = 'pt-br'
  
  queue_info['tier'] = RANK_TRANSLATION[lang][queue_info['tier']]

  return queue_info


@lol_router.get('/{rank_format}')
def get_tier_rank_string(
  rank_format: str,
  username: str,
  tag_line: str | None = None,
  queue_type: str = 'RANKED_SOLO_5x5'
) -> str:
  """
  `rank_format` recebe todos os textos e variaveis que formarão o texto resposta.
  Exemplo:
    URL: http://localhost:8000/league/v2/tier-rank-leaguePoints-PDL?username=growingsky%235500
    Response: "GOLD IV 70 PDL"
  """
  queue_info = get_queue_info(username, tag_line, queue_type)
  rank_informations = rank_format.split('-')
  response_words = []
  for info in rank_informations:
    if info in queue_info:
      response_words.append(str(queue_info[info]))
    else:
      response_words.append(str(info))
  
  return ' '.join(response_words)
