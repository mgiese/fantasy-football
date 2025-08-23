"""
This module handles writing data to a CSV file.
"""
import csv

class CSVWriter:
    """Writes data to a CSV file."""

    def __init__(self, file_path, console=None):
        """
        Initializes the CSV writer.
        Args:
            file_path (str): The path to the output CSV file.
            console (rich.console.Console, optional): Console for rich output.
        """
        self.file_path = file_path
        self.console = console

    def write_players(self, players_data):
        """
        Writes a list of player data to the CSV file.
        Args:
            players_data (list): A list of player dictionaries.
        """
        if not players_data:
            if self.console:
                self.console.print("[yellow]No players to write. CSV file will not be created.[/yellow]")
            else:
                print("No players to write. CSV file will not be created.")
            return

        try:
            with open(self.file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = players_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(players_data)
        except IOError as e:
            if self.console:
                self.console.print(f"[bold red]Error writing to file {self.file_path}:[/bold red] {e}")
            else:
                print(f"Error writing to file {self.file_path}: {e}")
            raise
