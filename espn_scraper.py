import requests
import json
import csv


# --- Constants ---
LEAGUE_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leagues/997575?view=mRoster&view=mTeam"
PLAYERS_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leagues/997575?scoringPeriodId=0&view=kona_player_info"
OUTPUT_CSV_FILE = 'fantasy_players.csv'


# Cookies for authentication
COOKIES = {
    "kona_v3_teamcontrol_ffl": '{"leagueId":997575,"seasonId":2025,"teamId":4}',
    "kona_v3_environment_season_ffl": '{"leagueId":997575,"seasonId":null}',
    "SWID": "{A27D5FAC-0651-48E7-BE8C-DDE9A16BA2A5}",
    "espnAuth": '{"swid":"{A27D5FAC-0651-48E7-BE8C-DDE9A16BA2A5}"}',
    "espn_s2": "AEB%2FhuZCQ36VYF3eV6yA5g85%2FNhBk7I2m%2BlZHOrUoEORCW%2FT22GeI1fpo%2Bt8aBcSzGg7Ao0EqQZkC9uFXNNsWcwdRzo4MUSSVewK6iT6FpDXbUJgu%2Fd2DEoyQfRt8M3M9ZMebtZy8AnkgwJG%2Bd9XvTSjGh2BVO4Y6leqG8bh4FLBl2J9Pd2cucIKiyMa0U1cRcC%2ByL2twZ%2B8jhio3QK6AlOkWHXLX%2Fq9BclJF%2BSMUAyAzICQQvjp9obNXaoDrkF2%2FgfnJRanJvkUgZk6BBBXhmx2radX3Acf1RKoS%2B5WwBeK9A%3D%3D"
}


# Header to fetch all players
HEADERS = {
    'x-fantasy-filter': '{"players":{"filterStatus":{"value":["FREEAGENT","WAIVERS","ONTEAM"]},"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"limit":2000,"sortPercOwned":{"sortAsc":false,"sortPriority":1},"sortDraftRanks":{"sortPriority":100,"sortAsc":true,"value":"STANDARD"}}}'
}


# --- Mappings ---
POSITION_MAP = {
    0: 'QB', 1: 'TQB', 2: 'RB', 3: 'RB/WR', 4: 'WR', 5: 'WR/TE', 6: 'TE',
    7: 'OP', 8: 'DT', 9: 'DE', 10: 'LB', 11: 'DL', 12: 'CB', 13: 'S',
    14: 'DB', 15: 'DP', 16: 'D/ST', 17: 'K', 18: 'P', 19: 'HC',
    20: 'Bench', 21: 'IR', 23: 'Flex'
}

PRO_TEAM_MAP = {
    0: 'Free Agent', 1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE',
    6: 'DAL', 7: 'DEN', 8: 'DET', 9: 'GB', 10: 'TEN', 11: 'IND',
    12: 'KC', 13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN', 17: 'NE',
    18: 'NO', 19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT',
    24: 'LAC', 25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WAS', 29: 'CAR',
    30: 'JAX', 33: 'BAL', 34: 'HOU'
}


def get_fantasy_team_map():
    """Fetches league data and maps player IDs to fantasy team names."""
    print("Fetching fantasy team rosters...")
    response = requests.get(LEAGUE_URL, cookies=COOKIES)
    if response.status_code != 200:
        print(f"Error fetching league data: {response.status_code}")
        return {}
    
    league_data = response.json()
    player_team_map = {}
    for team in league_data.get('teams', []):
        team_name = f"{team.get('location', '')} {team.get('nickname', '')}".strip()
        for player_entry in team.get('roster', {}).get('entries', []):
            player_id = player_entry.get('playerId')
            player_team_map[player_id] = team_name
    print(f"Mapped {len(player_team_map)} players to fantasy teams.")
    return player_team_map


def main():
    """Main function to fetch data and write to CSV."""
    player_team_map = get_fantasy_team_map()

    print("Fetching all player data...")
    response = requests.get(PLAYERS_URL, cookies=COOKIES, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch player data: {response.status_code} - {response.text}")
        return

    all_players_data = response.json().get('players', [])
    print(f"Found {len(all_players_data)} total players in the league pool.")

    processed_players = []
    for p_container in all_players_data:
        p_info = p_container.get('player', {})
        if not p_info:
            continue

        player_id = p_info.get('id')
        
        # Get stats
        season_stats = next((s for s in p_info.get('stats', []) if s.get('id') == '002024'), {})
        projected_stats = next((s for s in p_info.get('stats', []) if s.get('id') == '102025'), {})

        processed_players.append({
            'PlayerID': player_id,
            'PlayerName': p_info.get('fullName'),
            'FantasyTeam': player_team_map.get(player_id, 'Free Agent'),
            'Status': p_container.get('status'),
            'InjuryStatus': p_info.get('injuryStatus'),
            'Positions': ', '.join([POSITION_MAP.get(pos, str(pos)) for pos in p_info.get('eligibleSlots', [])]),
            'ProTeam': PRO_TEAM_MAP.get(p_info.get('proTeamId'), 'N/A'),
            'ProjectedPoints': projected_stats.get('appliedTotal'),
            '2024_TotalPoints': season_stats.get('appliedTotal'),
            '2024_AvgPoints': season_stats.get('appliedAverage'),
            'PercentOwned': p_info.get('ownership', {}).get('percentOwned'),
            'PercentStarted': p_info.get('ownership', {}).get('percentStarted'),
            'PercentChange': p_info.get('ownership', {}).get('percentChange')
        })

    # Write to CSV
    if not processed_players:
        print("No players processed. Exiting.")
        return
        
    print(f"Writing {len(processed_players)} players to {OUTPUT_CSV_FILE}...")
    with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = processed_players[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_players)
    
    print("Done!")


if __name__ == '__main__':
    main()
