import json
import os

from config import api_key
import requests
from requests.auth import HTTPBasicAuth


def GetMatchData(id: int, count_matches: int):
    link = f'https://api.stratz.com/api/v1/Player/{id}/matches'
    headers = {
        "authorization": f"Bearer {api_key}",
    }
    params = {
        "lobbyType": ["7"],
        "take": count_matches
    }
    data = requests.get(link, headers=headers, params=params).json()
    return data


def GetWinrateData(id: int, count_matches: int) -> int:
    result = 0
    data = GetMatchData(id, count_matches)
    stats = []
    for el in data:
        party = False
        isRadiant = False
        for pl in el["players"]:
            if "steamAccountId" in pl and pl["steamAccountId"] == id:
                isRadiant = pl["isRadiant"]
                if "partyId" in pl:
                    party = True
                break
        stats.append({
            'isWin': isRadiant and el["didRadiantWin"] or not isRadiant and not el["didRadiantWin"],
            'isParty': party
        })
    for el in stats:
        if el["isParty"]:
            k = 20
        else:
            k = 30
        if el["isWin"]:
            result += k
        else:
            result -= k
    return result
