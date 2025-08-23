"""
This module is responsible for fetching data from the ESPN Fantasy Football API.
"""
import requests
from . import auth
from . import constants

class APIClient:
    """A client for interacting with the ESPN Fantasy Football API."""

    def __init__(self, cookies=None, headers=None, console=None):
        """
        Initializes the API client.
        Args:
            cookies (dict, optional): Cookies for authentication. Defaults to auth.COOKIES.
            headers (dict, optional): Headers for requests. Defaults to auth.HEADERS.
            console (rich.console.Console, optional): Console for rich output.
        """
        self.cookies = cookies or auth.COOKIES
        self.headers = headers or auth.HEADERS
        self.console = console

    def _get(self, url, params=None):
        """
        Performs a GET request to the specified URL.
        Args:
            url (str): The URL to request.
            params (dict, optional): URL parameters. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        try:
            response = requests.get(url, cookies=self.cookies, headers=self.headers, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            if self.console:
                self.console.print(f"[bold red]Error fetching data from {url}:[/bold red] {e}")
            else:
                print(f"Error fetching data from {url}: {e}")
            raise

    def get_league_data(self):
        """Fetches the main league data, including teams and rosters."""
        return self._get(constants.LEAGUE_URL)

    def get_all_players_data(self):
        """Fetches data for all players in the league pool."""
        return self._get(constants.PLAYERS_URL)
