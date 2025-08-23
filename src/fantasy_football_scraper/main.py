"""
Main application entry point for the fantasy football scraper.

This script orchestrates the process of fetching, processing, and saving
fantasy football player data using a rich command-line interface.
"""
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

from fantasy_football_scraper.api_client import APIClient
from fantasy_football_scraper.processor import DataProcessor
from fantasy_football_scraper.writer import CSVWriter
from fantasy_football_scraper import constants

def run_scraper():
    """
    Executes the full scraper workflow with a rich CLI.
    1. Fetches league and player data from the API.
    2. Processes the raw data.
    3. Writes the processed data to a CSV file.
    """
    console = Console()

    # Initialize components
    client = APIClient(console=console)
    processor = DataProcessor(console=console)
    writer = CSVWriter(constants.OUTPUT_CSV_FILE, console=console)

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task1 = progress.add_task("[cyan]Fetching data...", total=2)
            
            league_data = client.get_league_data()
            progress.update(task1, advance=1)
            
            all_players_raw = client.get_all_players_data()
            progress.update(task1, advance=1)

            task2 = progress.add_task("[magenta]Processing data...", total=2)
            player_team_map = processor.get_fantasy_team_map(league_data)
            progress.update(task2, advance=1)

            all_players_list = all_players_raw.get('players', [])
            processed_players = processor.process_players(all_players_list, player_team_map)
            progress.update(task2, advance=1)

            task3 = progress.add_task("[green]Writing CSV...", total=1)
            writer.write_players(processed_players)
            progress.update(task3, advance=1)

        console.print("\n[bold green]Scraper finished successfully![/bold green]")
        console.print(f"Data saved to [cyan]{constants.OUTPUT_CSV_FILE}[/cyan]")

    except Exception as e:
        console.print(f"\n[bold red]An error occurred during the scraping process:[/bold red] {e}")

if __name__ == '__main__':
    run_scraper()
