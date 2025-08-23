# Normal Requirements

### 1. Project Overview

The goal of this project is to create a Python script that acts as a fantasy football draft aid. The script will connect to the ESPN Fantasy Football API for a user-specified private league. It will download data on all players and the current league rosters, process this information to create a comprehensive dataset for each player, and then export this data into a single, sortable CSV file. This "cheatsheet" will help users make informed decisions during their fantasy draft by consolidating key information like player rankings, projections, and who has already been drafted by which fantasy team.

Use SOLID (or python equivalent) design philosphy, including writing unit tests where applicable.

### 2. Functional Requirements

#### 2.1. Configuration and Authentication

The application requires configuration to access a private ESPN Fantasy Football league. This is handled in the `src/fantasy_football_scraper/auth.py` and `src/fantasy_football_scraper/constants.py` files.

**Required Values:**

*   **`LEAGUE_ID`**: The unique identifier for your ESPN fantasy league. This must be updated in `src/fantasy_football_scraper/constants.py`.
*   **Authentication Cookies**: To access private league data, you must provide your personal ESPN authentication cookies.

**How to get your Authentication Cookies:**

Failure to provide valid cookies will result in a 401 or 403 (Unauthorized) error from the ESPN API.

1.  Log in to your ESPN Fantasy Football league page in your web browser (e.g., Chrome, Edge, Firefox).
2.  Open the browser's Developer Tools. You can usually do this by pressing F12 or right-clicking on the page and selecting "Inspect".
3.  Go to the "Application" tab (in Chrome/Edge) or the "Storage" tab (in Firefox).
4.  In the left-hand menu, expand the "Cookies" section and select `https://fantasy.espn.com`.
5.  You will see a list of all cookies for the site. You need to find two of them:
    *   `espn_s2`: Find this in the list and copy its entire "Cookie Value".
    *   `SWID`: Find this in the list and copy its "Cookie Value".
6.  Paste these values into the `COOKIES` dictionary within the `src/fantasy_football_scraper/auth.py` file, replacing the placeholder values.

**API Headers:**

The application also sends a specific `x-fantasy-filter` header to ensure all players (free agents, on waivers, and on a team) are returned by the API. This is pre-configured in `src/fantasy_fantasy_football_scraper/auth.py` and generally does not need to be changed.

#### 2.2. Data Acquisition
The application will make HTTP GET requests to the ESPN Fantasy API.
*   **League Data:** It will fetch league settings and team rosters from the `m_league` view endpoint. This is used to determine which players are on which fantasy teams.
    *   URL: `https://fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leagues/{LEAGUE_ID}?view=m_league_seasons&view=m_roster`
*   **Player Data:** It will fetch a list of all players from the `m_player` view endpoint. This contains player metadata, stats, and projections.
    *   URL: `https://fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leagues/{LEAGUE_ID}?view=m_player_info`

#### 2.3. Data Processing
The script will perform the following processing steps:
1.  **Create a Player-to-Team Map:** Parse the fetched league data to build a dictionary that maps each `playerId` to the name of the fantasy team that currently has them on their roster.
2.  **Process Player List:** Iterate through the list of all players obtained from the API.
3.  **Combine Data:** For each player, create a single, flat data record containing a selection of key attributes.
4.  **Calculate Ranks:**
    *   The overall rank will be based on the player's order in the API response.
    *   A positional rank will be calculated by counting how many players of the same primary position have been processed so far.
5.  **Assign Fantasy Team:** Using the map from step 1, assign the player's fantasy team owner. If the player is not in the map, they should be labeled as a "Free Agent".

#### 2.4. Output
*   The processed data for all players will be written to a CSV file.
*   The default output filename will be `fantasy_players.csv`.
*   The CSV file will contain the following columns:
    *   `OverallRank`, `PositionalRank`, `PlayerName`, `FantasyTeam`, `PrimaryPosition`, `ProTeam`, `ADP`, `ProjectedPoints`, `2024_TotalPoints`, `PercentOwned`, `PercentStarted`.

### 3. User Interface
The application will be a command-line tool. When run, it will use the `rich` library to display progress bars indicating the status of data fetching, processing, and writing. Upon successful completion, it will print a confirmation message to the console.
