# Bare Minimum Requirements

**Project:** Fantasy Football Draft Cheatsheet Generator

**Goal:** Create a command-line application that fetches data from the ESPN Fantasy Football API for a specific private league and generates a single CSV file. This CSV will serve as a draft cheatsheet, containing player rankings, stats, and current fantasy team ownership.

**Core Requirements:**

1.  **Authentication:** The application must be able to authenticate with the ESPN API for a private league using user-provided `league_id`, `espn_s2`, and `swid` credentials.
2.  **Data Fetching:** It must hit the necessary ESPN API endpoints to retrieve:
    *   A list of all teams in the league and their current rosters.
    *   A comprehensive list of all available players, including their stats and rankings.
3.  **Data Processing:** The application must process the raw API data to:
    *   Map each player to their current fantasy team owner (or "Free Agent").
    *   Combine player information, stats, and ownership data into a unified structure for each player.
4.  **Output:** The final processed data for all players must be written to a single CSV file named `fantasy_players.csv`.
