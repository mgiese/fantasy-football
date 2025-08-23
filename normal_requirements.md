# Normal Requirements

### 1. Project Overview

The goal of this project is to create a Python script that acts as a fantasy football draft aid. The script will connect to the ESPN Fantasy Football API for a user-specified private league. It will download data on all players and the current league rosters, process this information to create a comprehensive dataset for each player, and then export this data into a single, sortable CSV file. This "cheatsheet" will help users make informed decisions during their fantasy draft by consolidating key information like player rankings, projections, and who has already been drafted by which fantasy team.

Use SOLID (or python equivalent) design philosphy, including writing unit tests where applicable.

### 2. Functional Requirements

#### 2.1. Configuration and Authentication: A Deep Dive

Accessing private league data from the ESPN API is the most critical and error-prone part of this application. Unlike public APIs, there is no simple API key. Instead, the application must impersonate a logged-in user who is a member of the target league. This is achieved by sending the user's browser cookies along with each request.

**If these steps are not followed precisely, the API will return a `401 Unauthorized` or `403 Forbidden` error.**

**A. Core Configuration (`constants.py`)**

These values must be set correctly in `src/fantasy_football_scraper/constants.py`:

*   `LEAGUE_ID`: The unique identifier for your ESPN fantasy league. You can find this in the URL of your league's homepage (e.g., `.../leagues/LEAGUE_ID`).
*   `SEASON_ID`: The year of the fantasy season you are targeting (e.g., `2025`).

**B. Authentication Cookies (`auth.py`)**

The application authenticates using two specific cookies that ESPN sets in your browser when you log in.

*   `SWID`: This acts as your unique user identifier across ESPN services.
*   `espn_s2`: This is your session token, proving you have an active login session.

**Step-by-Step Guide to Retrieving Your Cookies:**

1.  **Use a Standard Browser Window**: Do NOT use an Incognito or Private window. Log in to your ESPN Fantasy Football league page normally.
2.  **Open Developer Tools**: Once you are on your league's main page, open your browser's Developer Tools.
    *   **Shortcut**: Press `F12` (or `Cmd+Option+I` on Mac).
    *   **Menu**: Right-click anywhere on the page and select "Inspect".
3.  **Navigate to Cookie Storage**:
    *   In **Chrome** or **Edge**: Go to the "Application" tab.
    *   In **Firefox**: Go to the "Storage" tab.
4.  **Find the ESPN Cookies**:
    *   In the left-hand panel, look for the "Storage" section, expand "Cookies", and click on the entry for `https://fantasy.espn.com`.
5.  **Locate and Copy the Values**: You will see a table of all cookies for the site. You must find two and copy their **full, exact `Value` / `Cookie Value`**.
    *   Find the row for `espn_s2`. Copy the long string of characters from the "Value" column.
    *   Find the row for `SWID`. Copy the GUID-like string (e.g., `{ABC-123-...}`) from the "Value" column.
    *   **Common Pitfall**: Do not copy the cookie name or any other column. Only the value is needed.
6.  **Update `auth.py`**:
    *   Open the `src/fantasy_football_scraper/auth.py` file.
    *   Paste the values you copied into the `COOKIES` dictionary, replacing the placeholder strings.

**Important Notes:**
*   **Confidentiality**: These cookies are sensitive. Do not share them or commit them to a public repository. It is best practice to add `src/fantasy_football_scraper/auth.py` to your `.gitignore` file to prevent accidental commits.
*   **Expiration**: The `espn_s2` cookie will eventually expire. If you start getting authentication errors after a period of success, the first step is to repeat this process to get a fresh cookie.

**C. Critical API Header (`auth.py`)**

Authentication gets you in the door, but you still need to ask for the right data. The `x-fantasy-filter` header tells the ESPN API exactly which players to return.

*   **Purpose**: Without this header, the API returns a very limited, default set of players (e.g., only the top-ranked free agents).
*   **Configuration**: This is pre-configured in the `HEADERS` dictionary in `src/fantasy_football_scraper/auth.py` to request all players: free agents, players on waivers, and players on a team roster.
*   **Modification**: You should not need to change this header unless you are an advanced user experimenting with different API filters.

#### 2.2. Data Acquisition
The application makes HTTP GET requests to the specific ESPN Fantasy API endpoints that provide the necessary data feeds. The base URLs are constructed dynamically using the `LEAGUE_ID` and `SEASON_ID` from the `constants.py` file.

*   **League Data:** It will fetch league settings and team rosters. The `view=mRoster` and `view=mTeam` parameters are used to get the necessary roster and team details.
    *   URL: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON_ID}/segments/0/leagues/{LEAGUE_ID}?view=mRoster&view=mTeam`
*   **Player Data:** It will fetch a list of all players. The `view=kona_player_info` parameter is crucial as it returns the comprehensive player data needed for the application.
    *   URL: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON_ID}/segments/0/leagues/{LEAGUE_ID}?scoringPeriodId=0&view=kona_player_info`

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
