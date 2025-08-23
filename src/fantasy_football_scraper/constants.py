"""
This module contains constant values used throughout the fantasy football scraper application.
"""

# --- API Endpoints ---
LEAGUE_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leagues/997575?view=mRoster&view=mTeam"
PLAYERS_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leagues/997575?scoringPeriodId=0&view=kona_player_info"

# --- Output ---
OUTPUT_CSV_FILE = 'fantasy_players.csv'

# --- Mappings ---
POSITION_MAP = {
    0: 'QB', 1: 'TQB', 2: 'RB', 3: 'RB/WR', 4: 'WR', 5: 'WR/TE', 6: 'TE',
    7: 'OP', 8: 'DT', 9: 'DE', 10: 'LB', 11: 'DL', 12: 'CB', 13: 'S',
    14: 'DB', 15: 'DP', 16: 'D/ST', 17: 'K', 18: 'P', 19: 'HC',
    20: 'Bench', 21: 'IR', 23: 'Flex'
}

# Positions to filter out for the 'PrimaryPosition' field
FILTER_POSITIONS = {3, 5, 7, 20, 21, 23}

PRO_TEAM_MAP = {
    0: 'Free Agent', 1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE',
    6: 'DAL', 7: 'DEN', 8: 'DET', 9: 'GB', 10: 'TEN', 11: 'IND',
    12: 'KC', 13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN', 17: 'NE',
    18: 'NO', 19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT',
    24: 'LAC', 25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WAS', 29: 'CAR',
    30: 'JAX', 33: 'BAL', 34: 'HOU'
}
