"""
This module contains data processing and transformation logic.
"""
from . import constants

class DataProcessor:
    """Processes raw API data into a structured format."""

    def __init__(self, console=None):
        """
        Initializes the DataProcessor.
        Args:
            console (rich.console.Console, optional): Console for rich output.
        """
        self.console = console

    def get_fantasy_team_map(self, league_data):
        """
        Creates a map of player IDs to their fantasy team names.
        Args:
            league_data (dict): The raw league data from the API.
        Returns:
            dict: A mapping of {playerId: teamName}.
        """
        player_team_map = {}
        if not league_data:
            return player_team_map
            
        for team in league_data.get('teams', []):
            team_name = f"{team.get('location', '')} {team.get('nickname', '')}".strip()
            for player_entry in team.get('roster', {}).get('entries', []):
                player_id = player_entry.get('playerId')
                player_team_map[player_id] = team_name
        return player_team_map

    def process_players(self, all_players_data, player_team_map):
        """
        Processes the raw player data into a list of dictionaries.
        Args:
            all_players_data (list): A list of player data from the API.
            player_team_map (dict): A map of player IDs to fantasy teams.
        Returns:
            list: A list of processed player dictionaries.
        """
        processed_players = []
        positional_rank_counters = {}

        if not all_players_data:
            return processed_players

        for overall_rank, p_container in enumerate(all_players_data, 1):
            p_info = p_container.get('player', {})
            if not p_info:
                continue

            player_id = p_info.get('id')
            
            primary_positions = [pos for pos in p_info.get('eligibleSlots', []) if pos not in constants.FILTER_POSITIONS]
            primary_pos_str = constants.POSITION_MAP.get(primary_positions[0], 'N/A') if primary_positions else 'N/A'
            
            positional_rank_counters[primary_pos_str] = positional_rank_counters.get(primary_pos_str, 0) + 1
            positional_rank = positional_rank_counters[primary_pos_str]

            season_stats = next((s for s in p_info.get('stats', []) if s.get('id') == '002024'), {})
            projected_stats = next((s for s in p_info.get('stats', []) if s.get('id') == '102025'), {})
            ownership_data = p_info.get('ownership', {})
            draft_ranks = p_info.get('draftRanksByRankType', {}).get('STANDARD', {})

            processed_players.append({
                'OverallRank': overall_rank,
                'PositionalRank': positional_rank,
                'PlayerID': player_id,
                'PlayerName': p_info.get('fullName'),
                'FantasyTeam': player_team_map.get(player_id, 'Free Agent'),
                'Status': p_container.get('status'),
                'PrimaryPosition': primary_pos_str,
                'ProTeam': constants.PRO_TEAM_MAP.get(p_info.get('proTeamId'), 'N/A'),
                'ADP': ownership_data.get('averageDraftPosition'),
                'AuctionValue': draft_ranks.get('auctionValue'),
                'ProjectedPoints': projected_stats.get('appliedTotal'),
                '2024_TotalPoints': season_stats.get('appliedTotal'),
                '2024_AvgPoints': season_stats.get('appliedAverage'),
                'PercentOwned': ownership_data.get('percentOwned'),
                'PercentStarted': ownership_data.get('percentStarted'),
            })
        
        return processed_players
