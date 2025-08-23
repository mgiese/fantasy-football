# Full Requirements (Detailed Specification)

### 1. Introduction

This document specifies the requirements for a Python-based command-line application that scrapes, processes, and exports fantasy football data from the ESPN API. The application will generate a CSV "cheatsheet" file containing aggregated player data, rankings, and fantasy team ownership information for a specific, private fantasy league.

### 2. System Architecture

The application consists of four main Python modules:
*   `main.py`: The main entry point. It handles the overall workflow orchestration, initializes other components, and manages the command-line interface (using `rich`).
*   `api_client.py`: A dedicated class (`APIClient`) responsible for all communication with the ESPN API. It will handle constructing URLs, setting authentication headers, and executing HTTP requests.
*   `processor.py`: A class (`DataProcessor`) that contains the business logic for transforming the raw JSON data from the API into the structured format required for the final output.
*   `writer.py`: A class (`CSVWriter`) responsible for taking the processed player data and writing it to a CSV file.

### 3. Functional Requirements

#### FR-1: Authentication
*   **FR-1.1:** The system must authenticate requests to the ESPN API using cookies.
*   **FR-1.2:** The required cookies are `swid` and `espn_s2`.
*   **FR-1.3:** These cookie values must be stored as configurable variables, likely within a `src/fantasy_football_scraper/auth.py` file, which will be imported by the `APIClient`.

#### FR-2: Data Fetching (`APIClient`)
*   **FR-2.1:** The `APIClient` class shall be responsible for all HTTP requests. It will use the `requests` library.
*   **FR-2.2:** It must fetch league data (including rosters).
    *   **Pseudocode:**
        ```python
        def get_league_data(self):
            url = f"{constants.LEAGUE_URL_BASE}/{self.league_id}?view=m_league_seasons&view=m_roster"
            response = requests.get(url, cookies=self.cookies, headers=self.headers)
            response.raise_for_status()
            return response.json()
        ```
*   **FR-2.3:** It must fetch the master list of all players.
    *   **Pseudocode:**
        ```python
        def get_all_players_data(self):
            url = f"{constants.LEAGUE_URL_BASE}/{self.league_id}?view=m_player_info&scoringPeriodId=0"
            response = requests.get(url, cookies=self.cookies, headers=self.headers)
            response.raise_for_status()
            return response.json()
        ```
*   **FR-2.4:** The client must handle potential HTTP errors gracefully by raising a `requests.exceptions.RequestException`.

#### FR-3: Data Processing (`DataProcessor`)
*   **FR-3.1: Fantasy Team Mapping:**
    *   The `DataProcessor` will contain a method `get_fantasy_team_map(league_data)`.
    *   This method will iterate through `league_data['teams']`. For each team, it will iterate through `team['roster']['entries']`.
    *   It will build and return a dictionary mapping `entry['playerId']` to the team's full name (e.g., `f"{team['location']} {team['nickname']}"`).
*   **FR-3.2: Player Data Transformation:**
    *   The `DataProcessor` will contain a method `process_players(all_players_data, player_team_map)`.
    *   This method will initialize an empty list, `processed_players`, and a dictionary to track positional ranks, `positional_rank_counters`.
    *   It will iterate through the `all_players_data['players']` list using `enumerate` to get an `overall_rank`.
    *   **For each player, it will construct a dictionary with the following key-value pairs:**
        *   `OverallRank`: The 1-based index from the enumeration.
        *   `PlayerID`: from `player['player']['id']`.
        *   `PlayerName`: from `player['player']['fullName']`.
        *   `FantasyTeam`: Look up `PlayerID` in `player_team_map`. If not found, use the string 'Free Agent'.
        *   `Status`: from `player['status']`.
        *   `PrimaryPosition`: Extract the first eligible position from `player['player']['eligibleSlots']` that is not a filtered position (e.g., 'BE', 'IR'), then map it using `constants.POSITION_MAP`.
        *   `PositionalRank`: Increment and assign the value from `positional_rank_counters` for the player's `PrimaryPosition`.
        *   `ProTeam`: Map `player['player']['proTeamId']` using `constants.PRO_TEAM_MAP`.
        *   `ADP`: from `player['player']['ownership']['averageDraftPosition']`.
        *   `ProjectedPoints`: from the stats object where `id` is `'102025'`, get `appliedTotal`.
        *   `2024_TotalPoints`: from the stats object where `id` is `'002024'`, get `appliedTotal`.
        *   `PercentOwned`: from `player['player']['ownership']['percentOwned']`.
        *   `PercentStarted`: from `player['player']['ownership']['percentStarted']`.
    *   The method will return the final `processed_players` list.

#### FR-4: Output (`CSVWriter`)
*   **FR-4.1:** The `CSVWriter` class will be initialized with the output file path.
*   **FR-4.2:** It will have a method `write_players(processed_players)`.
*   **FR-4.3:** This method will open the specified file path for writing.
*   **FR-4.4:** It will use Python's `csv.DictWriter` to write the data.
*   **FR-4.5:** The header row will be determined from the keys of the first dictionary in the `processed_players` list.
*   **FR-4.6:** The `writeheader()` method will be called first, followed by `writerows(processed_players)`.

### 4. Non-Functional Requirements
*   **NFR-1: Usability:** The application must provide clear feedback to the user during its execution via a command-line interface, including progress indicators for long-running operations.
*   **NFR-2: Modularity:** The application's logic must be separated into distinct components for API interaction, data processing, and output writing to promote maintainability and testability.
*   **NFR-3: Error Handling:** The application must catch and report errors that occur during API requests (e.g., network issues, invalid authentication) to the user in a clear format.

### 5. Data Schema
#### 5.1. Output CSV Schema
The output CSV file will have the following columns in this order:
1.  `OverallRank` (integer)
2.  `PositionalRank` (integer)
3.  `PlayerID` (integer)
4.  `PlayerName` (string)
5.  `FantasyTeam` (string)
6.  `Status` (string)
7.  `PrimaryPosition` (string, e.g., 'QB', 'RB')
8.  `ProTeam` (string, e.g., 'Cardinals', 'Bills')
9.  `ADP` (float)
10. `AuctionValue` (integer)
11. `ProjectedPoints` (float)
12. `2024_TotalPoints` (float)
13. `2024_AvgPoints` (float)
14. `PercentOwned` (float)
15. `PercentStarted` (float)
