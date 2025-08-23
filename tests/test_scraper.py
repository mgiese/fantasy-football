import unittest
from unittest.mock import patch, MagicMock
import os
import json

# Add src to path to allow for imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from fantasy_football_scraper.api_client import APIClient
from fantasy_football_scraper.processor import DataProcessor
from fantasy_football_scraper.writer import CSVWriter
from fantasy_football_scraper import constants

class TestFantasyScraper(unittest.TestCase):

    def setUp(self):
        """Set up test data and mocks."""
        self.mock_league_data = self._load_mock_data('mock_league_data.json')
        self.mock_players_data = self._load_mock_data('mock_players_data.json')

    def _load_mock_data(self, filename):
        """Helper to load mock JSON data."""
        path = os.path.join(os.path.dirname(__file__), 'mock_data', filename)
        with open(path, 'r') as f:
            return json.load(f)

    @patch('fantasy_football_scraper.api_client.requests.get')
    def test_api_client_success(self, mock_get):
        """Test successful API calls."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [self.mock_league_data, self.mock_players_data]
        mock_get.return_value = mock_response

        client = APIClient()
        league_data = client.get_league_data()
        players_data = client.get_all_players_data()

        self.assertEqual(league_data, self.mock_league_data)
        self.assertEqual(players_data, self.mock_players_data)
        self.assertEqual(mock_get.call_count, 2)

    def test_data_processor(self):
        """Test the data processing logic."""
        processor = DataProcessor()
        
        # Test team mapping
        team_map = processor.get_fantasy_team_map(self.mock_league_data)
        self.assertIn(3916387, team_map) # Lamar Jackson
        self.assertEqual(team_map[3916387], 'Team user')

        # Test player processing
        players_list = self.mock_players_data.get('players', [])
        processed_data = processor.process_players(players_list, team_map)
        self.assertEqual(len(processed_data), 2)
        
        # Check a specific player's data
        player_one = processed_data[0]
        self.assertEqual(player_one['PlayerName'], "Ja'Marr Chase")
        self.assertEqual(player_one['OverallRank'], 1)
        self.assertEqual(player_one['PositionalRank'], 1)
        self.assertEqual(player_one['PrimaryPosition'], 'WR')
        self.assertEqual(player_one['FantasyTeam'], 'Free Agent')

    def test_csv_writer(self):
        """Test writing data to a CSV file."""
        processor = DataProcessor()
        team_map = processor.get_fantasy_team_map(self.mock_league_data)
        players_list = self.mock_players_data.get('players', [])
        processed_data = processor.process_players(players_list, team_map)
        
        test_csv_path = 'test_players.csv'
        writer = CSVWriter(test_csv_path)
        writer.write_players(processed_data)

        self.assertTrue(os.path.exists(test_csv_path))

        # Clean up the created file
        os.remove(test_csv_path)

if __name__ == '__main__':
    # Create mock_data directory if it doesn't exist
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'mock_data')):
        os.makedirs(os.path.join(os.path.dirname(__file__), 'mock_data'))
    
    # Create dummy mock files if they don't exist
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'mock_data', 'mock_league_data.json')):
        with open(os.path.join(os.path.dirname(__file__), 'mock_data', 'mock_league_data.json'), 'w') as f:
            json.dump({"teams": [{"location": "Team", "nickname": "user", "roster": {"entries": [{"playerId": 3916387}]}}]}, f)
            
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'mock_data', 'mock_players_data.json')):
        with open(os.path.join(os.path.dirname(__file__), 'mock_data', 'mock_players_data.json'), 'w') as f:
            json.dump({"players": [
                {"player": {"id": 4362628, "fullName": "Ja'Marr Chase", "eligibleSlots": [4, 5, 23], "proTeamId": 4, "ownership": {"averageDraftPosition": 1.5}, "draftRanksByRankType": {"STANDARD": {"auctionValue": 57}}, "stats": []}},
                {"player": {"id": 4430807, "fullName": "Bijan Robinson", "eligibleSlots": [2, 3, 23], "proTeamId": 1, "ownership": {"averageDraftPosition": 2.9}, "draftRanksByRankType": {"STANDARD": {"auctionValue": 56}}, "stats": []}}
            ]}, f)

    unittest.main()
